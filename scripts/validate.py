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
    "Trade-offs",
    "Learn for free",
    "Practise",
    "Ready to apply",
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


GUIDE_FOOTER = "[← Overview](../README.md) · [All paths](../README.md#the-paths)"

# Non-certification acronyms/abbreviations that may appear in Certifications text
NON_CERT_TOKENS = {
    "AI",
    "AWS",
    "EC",
    "GIAC",
    "IAPP",
    "IEC",
    "INE",
    "ISA",
    "ISACA",
    "ISC2",
    "ISO",
    "IT",
    "MBA",
    "TCM",
    "US",
    "V8",
    "YARA",
}


def normalise_path_title(title: str) -> str:
    """Normalise minor title variants (e.g. 'and digital forensics' -> 'and forensics')."""
    cleaned = re.sub(r"<br\s*/?>.*$", "", title, flags=re.I).strip()
    return cleaned.lower().replace(" and digital ", " and ")


def extract_markdown_tables(text: str) -> list[str]:
    """Return each contiguous Markdown pipe-table block in a document."""
    tables: list[str] = []
    current: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            if current:
                tables.append("\n".join(current))
                current = []
            continue
        if in_fence:
            continue
        if line.strip().startswith("|"):
            current.append(line)
        elif current:
            tables.append("\n".join(current))
            current = []
    if current:
        tables.append("\n".join(current))
    return tables


def extract_mermaid_labels(text: str) -> set[str]:
    """Extract normalised node labels from the first Mermaid block in text."""
    match = re.search(r"```mermaid\s*(.*?)```", text, flags=re.S)
    if not match:
        return set()
    return {
        normalise_path_title(m.group(1))
        for m in re.finditer(r'\["([^"]+)"\]', match.group(1))
    }


def extract_cert_codes(text: str) -> set[str]:
    """Extract recognisable certification codes/acronyms for parity checking."""
    # Remove Markdown link URLs and prerequisite parenthetical notes
    stripped = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    stripped = re.sub(r"\(for [^)]+\)", "", stripped, flags=re.I)
    # Match tokens like Security+, CySA+, SecAI+, SC-200, AZ-500, CIPP/E, eJPT, OSCP, CISSP, CIDPRO
    pattern = re.compile(
        r"(?<!\w)(?:[A-Za-z]+\+(?!\w)|(?:eJPT|[A-Z]{2}-\d{3}|CIPP/[A-Z]{1,2}|[A-Z]{3,6})(?!\w))"
    )
    return {m.group(0) for m in pattern.finditer(stripped) if m.group(0) not in NON_CERT_TOKENS}


def parse_certs_by_path(certs_text: str) -> dict[str, str]:
    """Map path filenames (e.g. 'cloud-security.md') to their row text in guides/certifications.md."""
    rows: dict[str, str] = {}
    sections = dict(split_sections(certs_text))
    by_path = sections.get("By path", "")
    for line in by_path.splitlines():
        if not line.strip().startswith("|"):
            continue
        match = re.search(r"\.\./paths/([a-z0-9-]+\.md)", line)
        if match:
            rows[match.group(1)] = line
    return rows


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
    readme_mermaid_labels = extract_mermaid_labels(readme_text)
    certs_links = set(extract_links(certs_text))
    certs_rows = parse_certs_by_path(certs_text)
    choose_links = set(extract_links(choose_text))
    choose_tables = extract_markdown_tables(choose_text)
    moving_links = set(extract_links(moving_text))

    if len(choose_tables) < 2:
        errors.append("guides/choosing-a-path.md: expected at least 2 comparison tables")

    # 1. Every guide is linked from README.md and follows guide metadata/footer conventions
    for g in guide_files:
        rel = f"guides/{g.name}"
        g_text = g.read_text(encoding="utf-8")
        if rel not in readme_links:
            errors.append(f"README.md does not link to {rel}")
        if "*Last reviewed:" not in g_text:
            errors.append(f"{rel}: missing '*Last reviewed:' line")
        if GUIDE_FOOTER not in g_text:
            errors.append(f"{rel}: missing standard navigation footer '{GUIDE_FOOTER}'")

    # 2. Every path follows template and is registered in README, guides and resource template
    neighbours: dict[str, list[str]] = {}
    resource_options = {
        normalise_path_title(m.group(1))
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
        for idx, table in enumerate(choose_tables, start=1):
            if rel_guide not in set(extract_links(table)):
                errors.append(
                    f"guides/choosing-a-path.md table #{idx} is missing a link to {rel_guide}"
                )
        if rel_guide not in moving_links:
            errors.append(f"guides/moving-between-paths.md does not link to {rel_guide}")

        h1_match = re.match(r"^#\s+(.+)$", text, flags=re.M)
        if not h1_match:
            errors.append(f"{rel_readme}: missing top-level heading")
        else:
            title = h1_match.group(1).strip()
            norm_title = normalise_path_title(title)
            if norm_title not in resource_options:
                errors.append(
                    f".github/ISSUE_TEMPLATE/resource.yml is missing option for '{title}'"
                )
            if norm_title not in readme_mermaid_labels:
                errors.append(
                    f"README.md Mermaid diagram is missing a node for '{title}'"
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

        for section_name in ("Trade-offs", "Practise", "Ready to apply"):
            body = section_map.get(section_name, "")
            bullets = [
                line for line in body.splitlines() if line.lstrip().startswith("- ")
            ]
            if len(bullets) < 3:
                errors.append(
                    f"{rel_readme}: {section_name} section has only {len(bullets)} bullet(s); expected at least 3"
                )

        certs_body = section_map.get("Certifications", "")
        if "../guides/certifications.md" not in certs_body:
            errors.append(f"{rel_readme}: Certifications section does not link to ../guides/certifications.md")

        if p.name in certs_rows:
            path_certs = extract_cert_codes(certs_body)
            guide_certs = extract_cert_codes(certs_rows[p.name])
            only_in_path = sorted(path_certs - guide_certs)
            only_in_guide = sorted(guide_certs - path_certs)
            if only_in_path:
                errors.append(
                    f"{rel_readme}: Certifications mentions {only_in_path} not listed in guides/certifications.md"
                )
            if only_in_guide:
                errors.append(
                    f"guides/certifications.md: row for {p.name} lists {only_in_guide} not mentioned in {rel_readme}"
                )

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
    extra_docs = [p for p in (ROOT / "CODE_OF_CONDUCT.md", ROOT / "CHANGELOG.md") if p.exists()]
    md_files = [readme_path, ROOT / "CONTRIBUTING.md", *extra_docs, *guide_files, *path_files]
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


MONTH_INDEX = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def check_staleness(max_age_months: int) -> list[str]:
    """Return errors for any path or guide whose *Last reviewed* date exceeds max_age_months."""
    from datetime import date

    today = date.today()
    today_months = today.year * 12 + today.month
    stale: list[str] = []
    files = sorted((ROOT / "guides").glob("*.md")) + sorted((ROOT / "paths").glob("*.md"))

    for md in files:
        text = md.read_text(encoding="utf-8")
        m = re.search(r"^\*Last reviewed:\s*([A-Za-z]+)\s+(\d{4})\b", text, flags=re.M)
        rel = md.relative_to(ROOT)
        if not m:
            stale.append(f"{rel}: could not parse '*Last reviewed: Month YYYY'")
            continue
        month_num = MONTH_INDEX.get(m.group(1).lower())
        year_num = int(m.group(2))
        if not month_num:
            stale.append(f"{rel}: unrecognised review month '{m.group(1)}'")
            continue
        age_months = today_months - (year_num * 12 + month_num)
        if age_months > max_age_months:
            stale.append(
                f"{rel}: last reviewed {m.group(1)} {year_num} ({age_months} months ago, limit {max_age_months})"
            )
    return stale


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate security-career-paths structure and links.")
    parser.add_argument(
        "--max-age-months",
        type=int,
        default=None,
        help="Fail if any guide or path was last reviewed more than N months ago",
    )
    args = parser.parse_args()

    errors = validate()
    if args.max_age_months is not None:
        errors.extend(check_staleness(args.max_age_months))

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"\nValidation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("Validation passed: all paths, guides, cross-links and anchors are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
