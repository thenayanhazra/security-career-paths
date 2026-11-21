#!/usr/bin/env python3
"""Validate structure, cross-links and consistency across security-career-paths."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PATH_HEADINGS = [
    "What the work involves",
    "Roles along the way",
    "Skills that matter",
    "How people get in",
    "Learn for free",
    "Practise",
    "Certifications",
    "Neighbouring paths",
]


def github_slug(heading: str) -> str:
    """Convert a Markdown heading to a GitHub-compatible anchor slug."""
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def heading_slugs(text: str) -> set[str]:
    """Return all heading anchor slugs in a Markdown document."""
    counts: dict[str, int] = {}
    slugs: set[str] = set()
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^#{1,6}\s+(.*)$", line)
        if not match:
            continue
        base = github_slug(match.group(1))
        seen = counts.get(base, 0)
        slugs.add(base if seen == 0 else f"{base}-{seen}")
        counts[base] = seen + 1
    return slugs


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split a Markdown document into (h2_title, body) pairs."""
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    buf: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence:
            match = re.match(r"^##\s+(.*)$", line)
            if match:
                if current_title is not None:
                    sections.append((current_title, "\n".join(buf)))
                current_title = match.group(1).strip()
                buf = []
                continue
        if current_title is not None:
            buf.append(line)
    if current_title is not None:
        sections.append((current_title, "\n".join(buf)))
    return sections


def extract_links(text: str) -> list[str]:
    """Extract Markdown link targets, ignoring fenced code blocks."""
    cleaned = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", cleaned)


def validate() -> list[str]:
    errors: list[str] = []

    readme_path = ROOT / "README.md"
    certs_path = ROOT / "guides" / "certifications.md"
    choose_path = ROOT / "guides" / "choosing-a-path.md"
    moving_path = ROOT / "guides" / "moving-between-paths.md"
    resource_tmpl = ROOT / ".github" / "ISSUE_TEMPLATE" / "resource.yml"

    readme_text = readme_path.read_text(encoding="utf-8")
    certs_text = certs_path.read_text(encoding="utf-8")
    choose_text = choose_path.read_text(encoding="utf-8")
    moving_text = moving_path.read_text(encoding="utf-8")
    resource_text = resource_tmpl.read_text(encoding="utf-8")

    path_files = sorted((ROOT / "paths").glob("*.md"))
    guide_files = sorted((ROOT / "guides").glob("*.md"))

    readme_links = set(extract_links(readme_text))
    certs_links = set(extract_links(certs_text))
    choose_links = set(extract_links(choose_text))
    moving_links = set(extract_links(moving_text))

    # 1. Every guide is linked from README.md
    for g in guide_files:
        rel = f"guides/{g.name}"
        if rel not in readme_links:
            errors.append(f"README.md does not link to {rel}")

    # 2. Every path follows template and is registered in README, guides and resource template
    neighbours: dict[str, list[str]] = {}
    resource_options = {
        m.group(1).strip()
        for m in re.finditer(r"^\s*-\s+(.+)$", resource_text, flags=re.M)
    }

    for p in path_files:
        text = p.read_text(encoding="utf-8")
        rel_readme = f"paths/{p.name}"
        rel_guide = f"../paths/{p.name}"

        if rel_readme not in readme_links:
            errors.append(f"README.md does not link to {rel_readme}")
        if rel_guide not in certs_links:
            errors.append(f"guides/certifications.md does not link to {rel_guide}")
        if rel_guide not in choose_links:
            errors.append(f"guides/choosing-a-path.md does not link to {rel_guide}")
        if rel_guide not in moving_links:
            errors.append(f"guides/moving-between-paths.md does not link to {rel_guide}")

        h1_match = re.match(r"^#\s+(.+)$", text, flags=re.M)
        if not h1_match:
            errors.append(f"{rel_readme}: missing top-level heading")
        else:
            title = h1_match.group(1).strip()
            # Match issue template option (allowing minor naming shortening like 'and digital forensics' -> 'and forensics')
            normalised_options = {
                opt.lower().replace(" and digital ", " and ")
                for opt in resource_options
            }
            if title.lower().replace(" and digital ", " and ") not in normalised_options:
                errors.append(
                    f".github/ISSUE_TEMPLATE/resource.yml is missing option for '{title}'"
                )

        if "*Last reviewed:" not in text:
            errors.append(f"{rel_readme}: missing '*Last reviewed:' line")
        if not re.search(r"^>\s+\S", text, flags=re.M):
            errors.append(f"{rel_readme}: missing summary blockquote")

        sections = split_sections(text)
        titles = [t for t, _ in sections]
        if titles != REQUIRED_PATH_HEADINGS:
            errors.append(
                f"{rel_readme}: section headings {titles} do not match expected {REQUIRED_PATH_HEADINGS}"
            )

        section_map = dict(sections)
        roles_body = section_map.get("Roles along the way", "")
        if "**Framework names:**" not in roles_body:
            errors.append(f"{rel_readme}: missing '**Framework names:**' in Roles along the way")

        certs_body = section_map.get("Certifications", "")
        if "../guides/certifications.md" not in certs_body:
            errors.append(f"{rel_readme}: Certifications section does not link to ../guides/certifications.md")

        neigh_body = section_map.get("Neighbouring paths", "").split("\n---", 1)[0]
        neigh_links = [
            link for link in extract_links(neigh_body) if link.endswith(".md") and "/" not in link
        ]
        if not neigh_links:
            errors.append(f"{rel_readme}: Neighbouring paths has no links")
        neighbours[p.name] = neigh_links

    # 3. Reciprocal Neighbouring paths links
    for src, targets in neighbours.items():
        for dst in targets:
            if dst not in neighbours:
                errors.append(f"paths/{src}: neighbouring path '{dst}' does not exist")
            elif src not in neighbours[dst]:
                errors.append(
                    f"Asymmetric neighbouring paths: paths/{src} links to {dst}, but paths/{dst} does not link back"
                )

    # 4. All local relative links and anchors across Markdown files resolve
    md_files = [readme_path, ROOT / "CONTRIBUTING.md", *guide_files, *path_files]
    slug_cache: dict[Path, set[str]] = {}
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        for target in extract_links(text):
            if re.match(r"^(https?://|mailto:)", target):
                continue
            path_part, _, anchor = target.partition("#")
            resolved = (md.parent / path_part).resolve() if path_part else md.resolve()
            if not resolved.exists():
                errors.append(f"{md.relative_to(ROOT)}: broken local link '{target}'")
                continue
            if anchor and resolved.suffix == ".md":
                if resolved not in slug_cache:
                    slug_cache[resolved] = heading_slugs(resolved.read_text(encoding="utf-8"))
                if anchor not in slug_cache[resolved]:
                    errors.append(
                        f"{md.relative_to(ROOT)}: broken anchor '#{anchor}' in '{target}'"
                    )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"\nValidation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("Validation passed: all paths, guides, cross-links and anchors are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
