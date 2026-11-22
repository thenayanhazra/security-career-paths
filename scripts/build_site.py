#!/usr/bin/env python3
"""Build the static documentation site and structured JSON data for security-career-paths.

Zero third-party dependencies (Python 3.12 standard library only).
Reads directly from canonical Markdown files so the site and JSON datasets never drift.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as validator  # noqa: E402

REPO_URL = "https://github.com/thenayanhazra/security-career-paths"
FAMILY_ORDER = [
    "Defend",
    "Attack and assess",
    "Build",
    "Govern",
    "AI security",
    "Leadership",
]
FAMILY_CLASSES = {
    "Defend": "fam-defend",
    "Attack and assess": "fam-attack",
    "Build": "fam-build",
    "Govern": "fam-govern",
    "AI security": "fam-ai",
    "Leadership": "fam-leadership",
}
WORK_STYLE_KEYS = [
    ("making things work", "building"),
    ("finding the flaw", "breaking"),
    ("spotting the signal", "defending"),
    ("bringing order", "organising"),
    ("weighing trade-offs", "governing"),
]
CODING_LEVEL_MAP = [
    ("daily", ("daily", "Daily, seriously")),
    ("regularly", ("regularly", "Regularly, for automation")),
    ("occasionally", ("occasionally", "Occasionally, scripts & queries")),
    ("rarely", ("rarely", "Rarely")),
]


def strip_md_inline(text: str) -> str:
    """Strip inline Markdown formatting to plain text."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def rewrite_link_target(target: str, source_rel: Path) -> str:
    """Rewrite relative Markdown links to built HTML links."""
    if re.match(r"^(https?://|mailto:|#)", target):
        return target
    path_part, sep, anchor = target.partition("#")
    if not path_part:
        return target
    resolved = (ROOT / source_rel.parent / path_part).resolve()
    try:
        rel_from_root = resolved.relative_to(ROOT)
    except ValueError:
        return target

    if rel_from_root.name == "LICENSE":
        return f"{REPO_URL}/blob/main/LICENSE"
    if rel_from_root.name == "CONTRIBUTING.md":
        return f"{REPO_URL}/blob/main/CONTRIBUTING.md"

    if rel_from_root == Path("README.md"):
        dest_rel = Path("index.html")
    elif rel_from_root.suffix == ".md":
        dest_rel = rel_from_root.with_suffix(".html")
    else:
        dest_rel = rel_from_root

    # Compute relative path from source_rel's built HTML location
    src_html_dir = source_rel.parent
    depth = 0 if src_html_dir == Path(".") else len(src_html_dir.parts)
    prefix = "../" * depth
    out = f"{prefix}{dest_rel.as_posix()}"
    if sep and anchor:
        out = f"{out}#{anchor}"
    return out


def render_inline(text: str, source_rel: Path) -> str:
    """Render inline Markdown (code, links, bold, italic) safely to HTML."""
    # Protect inline code first
    code_tokens: list[str] = []

    def _code_repl(m: re.Match[str]) -> str:
        code_tokens.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00CODE{len(code_tokens) - 1}\x00"

    s = re.sub(r"`([^`]+)`", _code_repl, text)

    # Protect links next
    link_tokens: list[str] = []

    def _link_repl(m: re.Match[str]) -> str:
        label = render_inline_formatting_only(m.group(1))
        raw_href = m.group(2).strip()
        href = rewrite_link_target(raw_href, source_rel)
        external = bool(re.match(r"^https?://", href))
        extra = ' target="_blank" rel="noopener noreferrer"' if external else ""
        link_tokens.append(f'<a href="{html.escape(href, quote=True)}"{extra}>{label}</a>')
        return f"\x00LINK{len(link_tokens) - 1}\x00"

    s = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", _link_repl, s)
    s = render_inline_formatting_only(s)

    for idx, tok in enumerate(link_tokens):
        s = s.replace(f"\x00LINK{idx}\x00", tok)
    for idx, tok in enumerate(code_tokens):
        s = s.replace(f"\x00CODE{idx}\x00", tok)
    return s


def render_inline_formatting_only(text: str) -> str:
    """Escape HTML and apply bold/italic emphasis."""
    s = html.escape(text)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def render_markdown(
    md_text: str,
    source_rel: Path,
    *,
    strip_footer: bool = False,
    strip_h1: bool = False,
    enhance_neighbours: bool = False,
) -> tuple[str, list[tuple[str, str]]]:
    """Convert Markdown text into clean semantic HTML plus a list of (id, title) h2 TOC items."""
    lines = md_text.splitlines()
    if strip_footer:
        # Remove trailing navigation footer (`---` followed by `[← ...]` line)
        for i in range(len(lines) - 1, max(-1, len(lines) - 6), -1):
            if lines[i].strip() == "---":
                tail = "\n".join(lines[i + 1 :]).strip()
                if tail.startswith("[←"):
                    lines = lines[:i]
                    break

    out: list[str] = []
    toc: list[tuple[str, str]] = []
    slug_counts: dict[str, int] = {}
    i = 0
    n = len(lines)
    current_h2 = ""

    def next_slug(heading_text: str) -> str:
        base = validator.github_slug(heading_text)
        seen = slug_counts.get(base, 0)
        slug_counts[base] = seen + 1
        return base if seen == 0 else f"{base}-{seen}"

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            buf: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # consume closing fence
            if lang != "mermaid":
                code_html = html.escape("\n".join(buf))
                out.append(f'<pre><code>{code_html}</code></pre>')
            continue

        # Horizontal rule
        if stripped == "---":
            out.append("<hr>")
            i += 1
            continue

        # Heading
        h_match = re.match(r"^(#{1,4})\s+(.*)$", line)
        if h_match:
            level = len(h_match.group(1))
            raw_title = h_match.group(2).strip()
            slug = next_slug(raw_title)
            if level == 1 and strip_h1:
                i += 1
                continue
            if level == 2:
                current_h2 = raw_title
                toc.append((slug, strip_md_inline(raw_title)))
            out.append(f'<h{level} id="{slug}">{render_inline(raw_title, source_rel)}</h{level}>')
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            q_lines: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                q_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append(f'<blockquote><p>{render_inline(" ".join(q_lines), source_rel)}</p></blockquote>')
            continue

        # Pipe table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            header_cells = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # skip header + separator
            body_rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                row_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                body_rows.append(row_cells)
                i += 1
            thead = "".join(f"<th>{render_inline(c, source_rel)}</th>" for c in header_cells)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{render_inline(c, source_rel)}</td>" for c in row) + "</tr>"
                for row in body_rows
            )
            out.append(
                f'<div class="table-wrap"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>'
            )
            continue

        # Unordered list
        if re.match(r"^-\s+", stripped):
            items: list[str] = []
            while i < n and re.match(r"^-\s+", lines[i].strip()):
                items.append(re.sub(r"^-\s+", "", lines[i].strip()))
                i += 1
            lis = "".join(f"<li>{render_inline(it, source_rel)}</li>" for it in items)
            out.append(f"<ul>{lis}</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            lis = "".join(f"<li>{render_inline(it, source_rel)}</li>" for it in items)
            out.append(f"<ol>{lis}</ol>")
            continue

        # Paragraph (accumulate consecutive plain lines)
        p_lines: list[str] = []
        while (
            i < n
            and lines[i].strip()
            and not lines[i].strip().startswith(("#", ">", "|", "```", "---"))
            and not re.match(r"^(?:-\s+|\d+\.\s+)", lines[i].strip())
        ):
            p_lines.append(lines[i].strip())
            i += 1
        para = " ".join(p_lines)

        if para.startswith("*Last reviewed:") and para.endswith("*"):
            out.append(f'<p class="last-reviewed">{html.escape(para.strip("*"))}</p>')
        elif enhance_neighbours and current_h2 == "Neighbouring paths":
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", para)
            chips = "".join(
                f'<a class="chip-link" href="{html.escape(rewrite_link_target(href, source_rel), quote=True)}">'
                f"{html.escape(label)}</a>"
                for label, href in links
            )
            out.append(f'<div class="neighbour-chips">{chips}</div>')
        else:
            out.append(f"<p>{render_inline(para, source_rel)}</p>")

    return "\n".join(out), toc


def parse_readme_paths(readme_text: str) -> list[dict[str, str]]:
    """Extract ordered path entries from README.md's main table."""
    entries: list[dict[str, str]] = []
    for line in readme_text.splitlines():
        if not line.strip().startswith("|") or "paths/" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        m = re.search(r"\[([^\]]+)\]\(paths/([a-z0-9-]+)\.md\)", cells[1])
        if not m:
            continue
        entries.append(
            {
                "family": cells[0],
                "slug": m.group(2),
                "readme_title": m.group(1),
                "one_line": cells[2],
                "typical_entry": cells[3],
            }
        )
    return entries


def parse_choosing_facets(choose_text: str) -> tuple[dict[str, list[str]], dict[str, tuple[str, str]]]:
    """Parse work styles and coding levels per path slug from guides/choosing-a-path.md."""
    tables = validator.extract_markdown_tables(choose_text)
    work_styles: dict[str, list[str]] = {}
    coding: dict[str, tuple[str, str]] = {}

    if len(tables) >= 1:
        for line in tables[0].splitlines()[2:]:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            row_label = cells[0].lower()
            style_key = next((k for prefix, k in WORK_STYLE_KEYS if prefix in row_label), None)
            if not style_key:
                continue
            for slug in re.findall(r"\.\./paths/([a-z0-9-]+)\.md", cells[1]):
                work_styles.setdefault(slug, [])
                if style_key not in work_styles[slug]:
                    work_styles[slug].append(style_key)

    if len(tables) >= 2:
        for line in tables[1].splitlines()[2:]:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            row_label = cells[0].lower()
            code_pair = next((v for prefix, v in CODING_LEVEL_MAP if row_label.startswith(prefix)), None)
            if not code_pair:
                continue
            for slug in re.findall(r"\.\./paths/([a-z0-9-]+)\.md", cells[1]):
                coding[slug] = code_pair

    return work_styles, coding


def parse_certifications_data(certs_text: str, path_meta: dict[str, dict]) -> dict:
    """Build structured JSON entries from guides/certifications.md."""
    entries: list[dict[str, str]] = []
    sections = dict(validator.split_sections(certs_text))
    by_path = sections.get("By path", "")

    for line in by_path.splitlines():
        if not line.strip().startswith("|") or "../paths/" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        m = re.search(r"\.\./paths/([a-z0-9-]+)\.md", cells[0])
        if not m:
            continue
        slug = m.group(1)
        pinfo = path_meta.get(slug, {})
        for level_name, raw_cell in zip(("Starting", "Building", "Advanced"), cells[1:4]):
            cleaned = raw_cell.strip()
            if not cleaned or cleaned in ("—", "-"):
                continue
            # Split semicolon-separated certification entries while preserving notes
            parts = [part.strip() for part in cleaned.split(";") if part.strip()]
            for part in parts:
                entries.append(
                    {
                        "name": strip_md_inline(part),
                        "level": level_name,
                        "path_slug": slug,
                        "path_title": pinfo.get("title", slug),
                        "family": pinfo.get("family", ""),
                        "path_url": f"paths/{slug}.html",
                    }
                )

    return {"entries": entries}


def parse_transitions_data(moving_text: str) -> dict:
    """Parse career transition rows from guides/moving-between-paths.md."""
    moves: list[dict] = []
    sections = dict(validator.split_sections(moving_text))
    common = sections.get("Common moves", "")
    for line in common.splitlines():
        if not line.strip().startswith("|") or line.strip().startswith("| From") or line.strip().startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        from_slugs = re.findall(r"\.\./paths/([a-z0-9-]+)\.md", cells[0])
        to_slugs = re.findall(r"\.\./paths/([a-z0-9-]+)\.md", cells[1])
        moves.append(
            {
                "from_label": strip_md_inline(cells[0]),
                "from_slugs": from_slugs,
                "to_label": strip_md_inline(cells[1]),
                "to_slugs": to_slugs,
                "carries_over": strip_md_inline(cells[2]),
                "to_add": strip_md_inline(cells[3]),
            }
        )
    return {"moves": moves}


def parse_glossary_terms(glossary_text: str) -> list[dict[str, str]]:
    """Extract glossary terms for inclusion in the client-side search index."""
    terms: list[dict[str, str]] = []
    for line in glossary_text.splitlines():
        if not line.strip().startswith("|") or line.strip().startswith("| Term") or line.strip().startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        term = strip_md_inline(cells[0])
        defn = strip_md_inline(cells[1])
        if term and defn:
            terms.append({"term": term, "definition": defn})
    return terms


def render_shell(
    *,
    title: str,
    description: str,
    site_root: str,
    active_nav: str,
    body_html: str,
    include_tools_js: bool = False,
    has_sidebar: bool = False,
) -> str:
    """Wrap page content in the shared HTML5 editorial shell."""
    nav_items = [
        ("home", "Overview", f"{site_root}index.html"),
        ("finder", "Path Finder", f"{site_root}finder.html"),
        ("certifications", "Certifications", f"{site_root}certifications.html"),
        ("map", "Transition Map", f"{site_root}map.html"),
        ("glossary", "Glossary", f"{site_root}guides/glossary.html"),
    ]
    nav_html = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == active_nav else ""}>{label}</a>'
        for key, label, href in nav_items
    )
    menu_btn_html = (
        '<button id="menu-toggle" class="icon-btn menu-btn" type="button" '
        'aria-label="Toggle navigation menu" aria-expanded="false">☰</button>'
        if has_sidebar
        else ""
    )
    tools_script = (
        f'<script src="{site_root}assets/tools.js" defer></script>' if include_tools_js else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="site-root" content="{site_root}">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <title>{html.escape(title)} — Security Career Paths</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{site_root}assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>

  <header class="site-header">
    <div class="header-inner">
      <div class="header-left">
        {menu_btn_html}
        <a class="brand" href="{site_root}index.html">
          <span class="brand-mark" aria-hidden="true">SC</span>
          <span>Security Career Paths</span>
        </a>
      </div>

      <nav class="top-nav" aria-label="Primary navigation">
        {nav_html}
      </nav>

      <div class="header-actions">
        <button class="search-trigger" type="button" data-open-search aria-label="Search paths, guides and certifications">
          <span aria-hidden="true">⌕</span>
          <span class="search-label">Search…</span>
          <span class="kbd">/</span>
        </button>
        <button id="theme-toggle" class="icon-btn" type="button" aria-label="Toggle dark theme">☾</button>
        <a class="icon-btn" href="{REPO_URL}" target="_blank" rel="noopener noreferrer" aria-label="View repository on GitHub" title="View on GitHub">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 .5C5.65.5.5 5.65.5 12c0 5.09 3.29 9.4 7.86 10.92.58.11.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.26.45-2.29 1.19-3.09-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.18 1.18a11.05 11.05 0 0 1 5.79 0c2.21-1.49 3.18-1.18 3.18-1.18.63 1.59.23 2.76.11 3.05.74.8 1.19 1.83 1.19 3.09 0 4.41-2.69 5.39-5.26 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.8-.01 3.18 0 .31.21.68.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <main id="main-content">
    {body_html}
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div>Security Career Paths · CC BY 4.0 · Mapped to NICE v2.2.0 &amp; ENISA ECSF</div>
      <div class="footer-links">
        <a href="{site_root}finder.html">Path Finder</a>
        <a href="{site_root}certifications.html">Certifications</a>
        <a href="{site_root}map.html">Transition Map</a>
        <a href="{site_root}data/paths.json">JSON Data</a>
        <a href="{REPO_URL}" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a href="{REPO_URL}/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer">Contribute</a>
      </div>
    </div>
  </footer>

  <div id="search-backdrop" class="search-backdrop" aria-hidden="true">
    <div class="search-dialog" role="dialog" aria-modal="true" aria-label="Search site">
      <div class="search-input-row">
        <span aria-hidden="true" style="color:var(--ink-muted);">⌕</span>
        <input id="search-input" type="search" placeholder="Search paths, certifications, acronyms, guides…" autocomplete="off">
        <span class="kbd">ESC</span>
      </div>
      <div id="search-results" class="search-results"></div>
    </div>
  </div>

  <script src="{site_root}assets/app.js" defer></script>
  {tools_script}
</body>
</html>
"""


def build_sidebar_html(
    paths: list[dict],
    guides: list[dict],
    site_root: str,
    current_rel: str,
) -> str:
    """Render the sticky left navigation sidebar grouped by Guides and 6 Path Families."""
    blocks: list[str] = []

    guide_links = "".join(
        f'<li><a href="{site_root}{g["url"]}"'
        f'{" aria-current=\"page\"" if g["url"] == current_rel else ""}>'
        f'{html.escape(g["title"])}</a></li>'
        for g in guides
    )
    blocks.append(
        f'<div class="sidebar-group"><h2 class="sidebar-heading">Guides</h2>'
        f'<ul class="sidebar-list">{guide_links}</ul></div>'
    )

    for family in FAMILY_ORDER:
        fam_paths = [p for p in paths if p["family"] == family]
        if not fam_paths:
            continue
        links = "".join(
            f'<li><a href="{site_root}{p["url"]}"'
            f'{" aria-current=\"page\"" if p["url"] == current_rel else ""}>'
            f'{html.escape(p["title"])}</a></li>'
            for p in fam_paths
        )
        blocks.append(
            f'<div class="sidebar-group"><h2 class="sidebar-heading">{html.escape(family)}</h2>'
            f'<ul class="sidebar-list">{links}</ul></div>'
        )

    return f'<aside id="docs-sidebar" class="sidebar" aria-label="Documentation navigation">{"".join(blocks)}</aside>'


def render_toc_html(toc: list[tuple[str, str]]) -> str:
    if not toc:
        return ""
    items = "".join(
        f'<li><a href="#{html.escape(slug, quote=True)}">{html.escape(label)}</a></li>'
        for slug, label in toc
    )
    return (
        '<aside class="toc" aria-label="On this page">'
        '<h2 class="toc-title">On this page</h2>'
        f"<ul>{items}</ul>"
        "</aside>"
    )


def build_site(out_dir: Path) -> None:
    """Build all HTML pages, assets, and JSON datasets into out_dir."""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "paths").mkdir(parents=True)
    (out_dir / "guides").mkdir(parents=True)
    (out_dir / "data").mkdir(parents=True)
    shutil.copytree(ROOT / "site" / "assets", out_dir / "assets")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    choose_text = (ROOT / "guides" / "choosing-a-path.md").read_text(encoding="utf-8")
    certs_text = (ROOT / "guides" / "certifications.md").read_text(encoding="utf-8")
    moving_text = (ROOT / "guides" / "moving-between-paths.md").read_text(encoding="utf-8")
    glossary_text = (ROOT / "guides" / "glossary.md").read_text(encoding="utf-8")

    readme_paths = parse_readme_paths(readme_text)
    work_styles, coding_map = parse_choosing_facets(choose_text)

    # 1. Parse all paths into structured metadata
    paths_data: list[dict] = []
    paths_by_slug: dict[str, dict] = {}
    search_index: list[dict] = []

    for rp in readme_paths:
        slug = rp["slug"]
        md_path = ROOT / "paths" / f"{slug}.md"
        text = md_path.read_text(encoding="utf-8")
        h1_m = re.match(r"^#\s+(.+)$", text, flags=re.M)
        title = h1_m.group(1).strip() if h1_m else rp["readme_title"]
        rev_m = re.search(r"^\*Last reviewed:\s*([^*]+)\*", text, flags=re.M)
        last_reviewed = rev_m.group(1).strip() if rev_m else ""
        quote_m = re.search(r"^>\s+(.+)$", text, flags=re.M)
        summary = quote_m.group(1).strip() if quote_m else rp["one_line"]

        sections = dict(validator.split_sections(text))
        fw_m = re.search(r"\*\*Framework names:\*\*\s*(.+)$", sections.get("Roles along the way", ""), flags=re.M)
        frameworks = strip_md_inline(fw_m.group(1)) if fw_m else ""

        neigh_body = sections.get("Neighbouring paths", "").split("\n---", 1)[0]
        neighbours = [
            link[:-3]
            for link in validator.extract_links(neigh_body)
            if link.endswith(".md") and "/" not in link
        ]

        trade_offs = [
            strip_md_inline(re.sub(r"^-\s+", "", line.strip()))
            for line in sections.get("Trade-offs", "").splitlines()
            if line.strip().startswith("- ")
        ]
        ready_to_apply = [
            strip_md_inline(re.sub(r"^-\s+", "", line.strip()))
            for line in sections.get("Ready to apply", "").splitlines()
            if line.strip().startswith("- ")
        ]

        coding_key, coding_label = coding_map.get(slug, ("occasionally", "Occasionally"))
        entry_lower = rp["typical_entry"].lower()
        entry_accessible = (
            "beginner-friendly" in entry_lower
            or "possible to enter directly" in entry_lower
            or "varies" in entry_lower
        )

        record = {
            "slug": slug,
            "title": title,
            "family": rp["family"],
            "one_line": rp["one_line"],
            "summary": summary,
            "typical_entry": rp["typical_entry"],
            "entry_accessible": entry_accessible,
            "coding_level": coding_key,
            "coding_label": coding_label,
            "work_styles": work_styles.get(slug, []),
            "last_reviewed": last_reviewed,
            "frameworks": frameworks,
            "neighbours": neighbours,
            "trade_offs": trade_offs,
            "ready_to_apply": ready_to_apply,
            "url": f"paths/{slug}.html",
        }
        paths_data.append(record)
        paths_by_slug[slug] = record

        search_index.append(
            {
                "title": title,
                "kind": f"Path · {rp['family']}",
                "url": f"paths/{slug}.html",
                "summary": summary,
                "meta": f"{rp['family']} {frameworks} {rp['typical_entry']}",
                "body": strip_md_inline(text),
            }
        )

    # 2. Parse guides in curated display order
    guide_order = [
        ("choosing-a-path", "Four questions and common misconceptions to pick a direction."),
        ("foundations", "Networking, Linux, Windows, scripting, cloud and home-lab basics."),
        ("first-role", "Side-door roles, CVs, communities and landing your first security job."),
        ("interviews-and-portfolios", "What strong portfolios look like and sample interview questions by family."),
        ("employers-and-markets", "MSSPs, consultancies, in-house teams, vendors and regional hiring."),
        ("moving-between-paths", "Common lateral moves, what carries over and what to add."),
        ("senior-progression", "Advancing past mid-level into Staff+ IC or leadership tracks."),
        ("certifications", "Certifications by path and level, prerequisites and 2026 changes."),
        ("practice", "Free and freemium labs, datasets and non-lab portfolio exercises."),
        ("working-with-ai", "Using AI effectively on the job and while learning without hollowing out fundamentals."),
        ("staying-current", "A sustainable reading habit, newsletters, podcasts and reports."),
        ("glossary", "Plain-English definitions for ~60 common acronyms and terms."),
    ]
    guides_data: list[dict] = []
    for slug, blurb in guide_order:
        md_path = ROOT / "guides" / f"{slug}.md"
        text = md_path.read_text(encoding="utf-8")
        h1_m = re.match(r"^#\s+(.+)$", text, flags=re.M)
        title = h1_m.group(1).strip() if h1_m else slug
        rev_m = re.search(r"^\*Last reviewed:\s*([^*]+)\*", text, flags=re.M)
        last_reviewed = rev_m.group(1).strip() if rev_m else ""
        rec = {
            "slug": slug,
            "title": title,
            "blurb": blurb,
            "last_reviewed": last_reviewed,
            "url": f"guides/{slug}.html",
        }
        guides_data.append(rec)
        search_index.append(
            {
                "title": title,
                "kind": "Guide",
                "url": f"guides/{slug}.html",
                "summary": blurb,
                "meta": f"guide {slug}",
                "body": strip_md_inline(text),
            }
        )

    # Add Glossary terms to search index for instant acronym lookups
    for term_entry in parse_glossary_terms(glossary_text):
        search_index.append(
            {
                "title": term_entry["term"],
                "kind": "Glossary",
                "url": "guides/glossary.html",
                "summary": term_entry["definition"],
                "meta": f"glossary acronym {term_entry['term']}",
                "body": term_entry["definition"],
            }
        )

    certs_data = parse_certifications_data(certs_text, paths_by_slug)
    transitions_data = parse_transitions_data(moving_text)

    # Write machine-readable JSON datasets
    (out_dir / "data" / "paths.json").write_text(
        json.dumps(paths_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "data" / "guides.json").write_text(
        json.dumps(guides_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "data" / "certifications.json").write_text(
        json.dumps(certs_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "data" / "transitions.json").write_text(
        json.dumps(transitions_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "data" / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # 3. Render individual Path pages
    for idx, p in enumerate(paths_data):
        rel_md = Path("paths") / f'{p["slug"]}.md'
        md_text = (ROOT / rel_md).read_text(encoding="utf-8")
        content_html, toc = render_markdown(
            md_text, rel_md, strip_footer=True, enhance_neighbours=True
        )
        sidebar = build_sidebar_html(paths_data, guides_data, "../", p["url"])
        toc_html = render_toc_html(toc)
        fam_cls = FAMILY_CLASSES.get(p["family"], "fam-leadership")

        prev_p = paths_data[idx - 1] if idx > 0 else None
        next_p = paths_data[idx + 1] if idx + 1 < len(paths_data) else None
        pager_parts: list[str] = []
        if prev_p:
            pager_parts.append(
                f'<a class="pager-link" href="../{prev_p["url"]}">'
                f'<span class="pager-dir">← Previous path</span>'
                f'<span class="pager-title">{html.escape(prev_p["title"])}</span></a>'
            )
        else:
            pager_parts.append("<span></span>")
        if next_p:
            pager_parts.append(
                f'<a class="pager-link" style="text-align:right;" href="../{next_p["url"]}">'
                f'<span class="pager-dir">Next path →</span>'
                f'<span class="pager-title">{html.escape(next_p["title"])}</span></a>'
            )

        body = f"""
        <div class="docs-layout">
          {sidebar}
          <article class="article-wrap prose">
            <nav class="breadcrumbs" aria-label="Breadcrumb">
              <a href="../index.html">Overview</a>
              <span aria-hidden="true">/</span>
              <a href="../index.html#the-paths">Paths</a>
              <span aria-hidden="true">/</span>
              <span>{html.escape(p["family"])}</span>
            </nav>
            <div class="article-meta-bar">
              <span class="badge {fam_cls}">{html.escape(p["family"])}</span>
              <span class="meta-pill">Entry: {html.escape(p["typical_entry"])}</span>
              <span class="meta-pill">Coding: {html.escape(p["coding_label"])}</span>
            </div>
            {content_html}
            <div class="article-pager">{"".join(pager_parts)}</div>
          </article>
          {toc_html}
        </div>
        """
        page_html = render_shell(
            title=p["title"],
            description=p["summary"],
            site_root="../",
            active_nav="",
            body_html=body,
            has_sidebar=True,
        )
        (out_dir / "paths" / f'{p["slug"]}.html').write_text(page_html, encoding="utf-8")

    # 4. Render individual Guide pages
    for idx, g in enumerate(guides_data):
        rel_md = Path("guides") / f'{g["slug"]}.md'
        md_text = (ROOT / rel_md).read_text(encoding="utf-8")
        content_html, toc = render_markdown(md_text, rel_md, strip_footer=True)
        sidebar = build_sidebar_html(paths_data, guides_data, "../", g["url"])
        toc_html = render_toc_html(toc)

        # Add a helpful link to the interactive counterpart on key guides
        tool_banner = ""
        if g["slug"] == "choosing-a-path":
            tool_banner = (
                '<p style="margin:0 0 18px;"><a class="btn btn-secondary" href="../finder.html">'
                "Try the interactive Path Finder →</a></p>"
            )
        elif g["slug"] == "certifications":
            tool_banner = (
                '<p style="margin:0 0 18px;"><a class="btn btn-secondary" href="../certifications.html">'
                "Open the filterable Certifications Explorer →</a></p>"
            )
        elif g["slug"] == "moving-between-paths":
            tool_banner = (
                '<p style="margin:0 0 18px;"><a class="btn btn-secondary" href="../map.html">'
                "Explore the interactive Career Transition Map →</a></p>"
            )

        prev_g = guides_data[idx - 1] if idx > 0 else None
        next_g = guides_data[idx + 1] if idx + 1 < len(guides_data) else None
        pager_parts = []
        if prev_g:
            pager_parts.append(
                f'<a class="pager-link" href="../{prev_g["url"]}">'
                f'<span class="pager-dir">← Previous guide</span>'
                f'<span class="pager-title">{html.escape(prev_g["title"])}</span></a>'
            )
        else:
            pager_parts.append("<span></span>")
        if next_g:
            pager_parts.append(
                f'<a class="pager-link" style="text-align:right;" href="../{next_g["url"]}">'
                f'<span class="pager-dir">Next guide →</span>'
                f'<span class="pager-title">{html.escape(next_g["title"])}</span></a>'
            )

        body = f"""
        <div class="docs-layout">
          {sidebar}
          <article class="article-wrap prose">
            <nav class="breadcrumbs" aria-label="Breadcrumb">
              <a href="../index.html">Overview</a>
              <span aria-hidden="true">/</span>
              <span>Guides</span>
            </nav>
            {tool_banner}
            {content_html}
            <div class="article-pager">{"".join(pager_parts)}</div>
          </article>
          {toc_html}
        </div>
        """
        page_html = render_shell(
            title=g["title"],
            description=g["blurb"],
            site_root="../",
            active_nav="glossary" if g["slug"] == "glossary" else "",
            body_html=body,
            has_sidebar=True,
        )
        (out_dir / "guides" / f'{g["slug"]}.html').write_text(page_html, encoding="utf-8")

    # 5. Render Home page (index.html)
    family_sections_html: list[str] = []
    for fam in FAMILY_ORDER:
        fam_paths = [p for p in paths_data if p["family"] == fam]
        fam_cls = FAMILY_CLASSES.get(fam, "fam-leadership")
        cards = "".join(
            f'<a class="path-card" href="{p["url"]}">'
            f'<div><div class="path-card-title">{html.escape(p["title"])}</div>'
            f'<p class="path-card-desc">{html.escape(p["one_line"])}</p></div>'
            f'<div class="path-card-meta">Entry: {html.escape(p["typical_entry"])}</div>'
            f"</a>"
            for p in fam_paths
        )
        family_sections_html.append(
            f'<div class="family-section">'
            f'<div class="family-heading"><span class="badge {fam_cls}">{html.escape(fam)}</span>'
            f'<h3>{len(fam_paths)} {"path" if len(fam_paths) == 1 else "paths"}</h3></div>'
            f'<div class="paths-grid">{cards}</div></div>'
        )

    guides_cards_html = "".join(
        f'<a class="guide-card" href="{g["url"]}">'
        f'<div class="guide-card-title">{html.escape(g["title"])}</div>'
        f'<p class="guide-card-sub">{html.escape(g["blurb"])}</p></a>'
        for g in guides_data
    )

    home_body = f"""
    <div class="page-shell">
      <section class="hero">
        <p class="hero-eyebrow">Open reference · Updated November 2026</p>
        <h1>A clear map of careers in security and AI security.</h1>
        <p class="hero-lead">
          Security is not one job. A detection engineer, a penetration tester, a privacy specialist and an AI red-teamer share a field and little else. Compare all {len(paths_data)} paths side by side—what the work involves, honest trade-offs, how people get in, and where to learn, mostly for free.
        </p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="finder.html">Find your path →</a>
          <a class="btn btn-secondary" href="#the-paths">Browse all {len(paths_data)} paths</a>
          <a class="btn btn-secondary" href="guides/foundations.html">Start with Foundations</a>
        </div>
        <div class="stats-strip">
          <div class="stat-item"><span class="stat-num">{len(paths_data)}</span><span class="stat-label">Career paths across 6 families</span></div>
          <div class="stat-item"><span class="stat-num">{len(guides_data)}</span><span class="stat-label">Cross-cutting career guides</span></div>
          <div class="stat-item"><span class="stat-num">{len(certs_data["entries"])}</span><span class="stat-label">Mapped certifications</span></div>
          <div class="stat-item"><span class="stat-num">NICE &amp; ECSF</span><span class="stat-label">Cross-checked to public frameworks</span></div>
        </div>
      </section>

      <section class="section-block">
        <div class="section-header">
          <div>
            <h2>Interactive tools</h2>
            <p>Narrow your choices, filter certifications and trace sideways moves between paths.</p>
          </div>
        </div>
        <div class="tools-grid">
          <a class="tool-card" href="finder.html">
            <div>
              <div class="tool-kicker">Decision aid</div>
              <h3>Interactive Path Finder</h3>
              <p>Answer five quick questions about how you like to work, coding appetite, hours and background to rank matching paths.</p>
            </div>
            <span class="tool-cta">Open Path Finder →</span>
          </a>
          <a class="tool-card" href="certifications.html">
            <div>
              <div class="tool-kicker">Filterable matrix</div>
              <h3>Certifications Explorer</h3>
              <p>Search and filter certifications across all {len(paths_data)} paths by family, level (Starting, Building, Advanced) or issuer.</p>
            </div>
            <span class="tool-cta">Explore certifications →</span>
          </a>
          <a class="tool-card" href="map.html">
            <div>
              <div class="tool-kicker">Career graph</div>
              <h3>Career Transition Map</h3>
              <p>Click any path to highlight neighbouring roles and see what carries over and what to add when switching directions.</p>
            </div>
            <span class="tool-cta">Open Transition Map →</span>
          </a>
        </div>
      </section>

      <section id="the-paths" class="section-block">
        <div class="section-header">
          <div>
            <h2>The {len(paths_data)} paths</h2>
            <p>Each page covers daily work, role levels, honest trade-offs, free resources, hands-on practice and interview readiness.</p>
          </div>
        </div>
        {"".join(family_sections_html)}
      </section>

      <section id="start-here" class="section-block">
        <div class="section-header">
          <div>
            <h2>Cross-cutting guides</h2>
            <p>Practical advice for breaking in, preparing for interviews, working with AI and advancing to senior roles.</p>
          </div>
        </div>
        <div class="guides-grid">{guides_cards_html}</div>
      </section>
    </div>
    """

    (out_dir / "index.html").write_text(
        render_shell(
            title="Overview",
            description="A map of careers in information security, cybersecurity and AI security: what each path involves, how people get in, how they progress, and where to learn, mostly for free.",
            site_root="./",
            active_nav="home",
            body_html=home_body,
        ),
        encoding="utf-8",
    )

    # 6. Render Interactive Path Finder (finder.html)
    finder_body = """
    <div class="page-shell">
      <div class="tool-header">
        <p class="hero-eyebrow">Interactive decision aid</p>
        <h1>Path Finder</h1>
        <p>Answer any combination of the five questions below to rank all 18 paths. None of these choices is permanent—use your top two or three results to try a weekend of free practice.</p>
      </div>

      <div id="path-finder-app" class="finder-grid">
        <div class="finder-panel">
          <div class="q-block">
            <p class="q-label">1. What kind of work draws you in most?</p>
            <div class="choice-group">
              <button type="button" class="choice-btn" data-q="workStyle" data-val="building" aria-pressed="false">Building, automating &amp; designing systems</button>
              <button type="button" class="choice-btn" data-q="workStyle" data-val="breaking" aria-pressed="false">Breaking systems &amp; finding flaws</button>
              <button type="button" class="choice-btn" data-q="workStyle" data-val="defending" aria-pressed="false">Spotting signals &amp; responding under pressure</button>
              <button type="button" class="choice-btn" data-q="workStyle" data-val="organising" aria-pressed="false">Bringing order to messy large-scale problems</button>
              <button type="button" class="choice-btn" data-q="workStyle" data-val="governing" aria-pressed="false">Weighing trade-offs, writing &amp; advising</button>
            </div>
          </div>

          <div class="q-block">
            <p class="q-label">2. How much do you want to code?</p>
            <div class="choice-group">
              <button type="button" class="choice-btn" data-q="coding" data-val="daily" aria-pressed="false">Daily, seriously</button>
              <button type="button" class="choice-btn" data-q="coding" data-val="regularly" aria-pressed="false">Regularly, for automation</button>
              <button type="button" class="choice-btn" data-q="coding" data-val="occasionally" aria-pressed="false">Occasionally, scripts &amp; queries</button>
              <button type="button" class="choice-btn" data-q="coding" data-val="rarely" aria-pressed="false">Rarely</button>
            </div>
          </div>

          <div class="q-block">
            <p class="q-label">3. How do you feel about shifts and emergency on-call?</p>
            <div class="choice-group">
              <button type="button" class="choice-btn" data-q="onCall" data-val="office-hours" aria-pressed="false">Prefer mostly office hours</button>
              <button type="button" class="choice-btn" data-q="onCall" data-val="shifts-ok" aria-pressed="false">Fine with shifts &amp; rapid response</button>
            </div>
          </div>

          <div class="q-block">
            <p class="q-label">4. What is your current background?</p>
            <div class="choice-group">
              <button type="button" class="choice-btn" data-q="background" data-val="new-to-tech" aria-pressed="false">New to tech / career changer</button>
              <button type="button" class="choice-btn" data-q="background" data-val="it-ops" aria-pressed="false">IT support, sysadmin or networking</button>
              <button type="button" class="choice-btn" data-q="background" data-val="dev-data" aria-pressed="false">Software or data engineering</button>
              <button type="button" class="choice-btn" data-q="background" data-val="cloud-devops" aria-pressed="false">Cloud or DevOps engineering</button>
              <button type="button" class="choice-btn" data-q="background" data-val="audit-legal" aria-pressed="false">Audit, compliance or legal</button>
              <button type="button" class="choice-btn" data-q="background" data-val="ml-ai" aria-pressed="false">Data science or ML engineering</button>
              <button type="button" class="choice-btn" data-q="background" data-val="industrial" aria-pressed="false">Control or industrial engineering</button>
              <button type="button" class="choice-btn" data-q="background" data-val="in-security" aria-pressed="false">Already working in security</button>
            </div>
          </div>

          <div class="q-block">
            <p class="q-label">5. What stage are you targeting right now?</p>
            <div class="choice-group">
              <button type="button" class="choice-btn" data-q="entryPref" data-val="beginner" aria-pressed="false">Prioritise beginner-friendly entry points</button>
              <button type="button" class="choice-btn" data-q="entryPref" data-val="specialist" aria-pressed="false">Open to mid-career &amp; specialist roles</button>
            </div>
          </div>

          <button id="finder-reset" type="button" class="btn btn-secondary" style="margin-top:6px;">Reset answers</button>
        </div>

        <div id="finder-results" class="results-panel" aria-live="polite"></div>
      </div>
    </div>
    """
    (out_dir / "finder.html").write_text(
        render_shell(
            title="Path Finder",
            description="Interactive decision tool to compare all 18 cybersecurity and AI security career paths by work style, coding level, on-call tolerance and background.",
            site_root="./",
            active_nav="finder",
            body_html=finder_body,
            include_tools_js=True,
        ),
        encoding="utf-8",
    )

    # 7. Render Filterable Certifications Explorer (certifications.html)
    # Render non-table guidance sections from guides/certifications.md without duplicating the By-path matrix
    certs_without_bypath = re.sub(
        r"\n## By path\n.*?(?=\n## )", "\n", certs_text, flags=re.S
    )
    certs_prose_html, _ = render_markdown(
        certs_without_bypath, Path("guides/certifications.md"), strip_footer=True, strip_h1=True
    )
    certs_prose_html = certs_prose_html.replace('href="../', 'href="')

    family_options = "".join(
        f'<option value="{html.escape(f)}">{html.escape(f)}</option>' for f in FAMILY_ORDER
    )
    certs_body = f"""
    <div class="page-shell">
      <div class="tool-header">
        <p class="hero-eyebrow">Updated November 2026</p>
        <h1>Certifications Explorer</h1>
        <p>Filter certifications across all {len(paths_data)} paths by keyword, path family or experience level. One entry-level certification helps get past screening; hands-on work gets you hired.</p>
      </div>

      <section id="certs-explorer-app">
        <div class="filter-bar">
          <input id="cert-search" class="filter-input" type="search" placeholder="Filter by cert, issuer or path (e.g. OSCP, GIAC, SecAI+, Cloud)…" aria-label="Filter certifications">
          <select id="cert-family" class="filter-select" aria-label="Filter by path family">
            <option value="all">All families</option>
            {family_options}
          </select>
          <div class="filter-pills" role="group" aria-label="Filter by level">
            <button type="button" class="choice-btn" data-level="all" aria-pressed="true">All levels</button>
            <button type="button" class="choice-btn" data-level="starting" aria-pressed="false">Starting</button>
            <button type="button" class="choice-btn" data-level="building" aria-pressed="false">Building</button>
            <button type="button" class="choice-btn" data-level="advanced" aria-pressed="false">Advanced</button>
          </div>
        </div>
        <p id="cert-count" class="filter-count"></p>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Certification</th>
                <th>Level</th>
                <th>Path</th>
                <th>Family</th>
              </tr>
            </thead>
            <tbody id="cert-tbody"></tbody>
          </table>
        </div>
      </section>

      <section class="prose" style="max-width:840px;margin-top:44px;">
        {certs_prose_html}
      </section>
    </div>
    """
    (out_dir / "certifications.html").write_text(
        render_shell(
            title="Certifications Explorer",
            description="Searchable, filterable matrix of cybersecurity and AI security certifications by career path and experience level.",
            site_root="./",
            active_nav="certifications",
            body_html=certs_body,
            include_tools_js=True,
        ),
        encoding="utf-8",
    )

    # 8. Render Interactive Career Transition Map (map.html)
    map_body = """
    <div class="page-shell">
      <div class="tool-header">
        <p class="hero-eyebrow">Interactive career graph</p>
        <h1>Career Transition Map</h1>
        <p>Select any path below to highlight its direct neighbouring paths and see documented transitions—what carries over and what to add when moving sideways or up.</p>
      </div>

      <div id="transition-map-app" class="map-layout">
        <div id="map-board" class="map-board" aria-label="Security career paths by family"></div>
        <aside id="map-inspector" class="map-inspector" aria-live="polite"></aside>
      </div>
    </div>
    """
    (out_dir / "map.html").write_text(
        render_shell(
            title="Career Transition Map",
            description="Interactive map of cybersecurity career paths showing neighbouring roles and what carries over when transitioning.",
            site_root="./",
            active_nav="map",
            body_html=map_body,
            include_tools_js=True,
        ),
        encoding="utf-8",
    )


def check_built_site(out_dir: Path) -> list[str]:
    """Verify all generated HTML files have valid internal links and JSON outputs are populated."""
    errors: list[str] = []

    for json_name in ("paths.json", "guides.json", "certifications.json", "transitions.json", "search-index.json"):
        jp = out_dir / "data" / json_name
        if not jp.exists():
            errors.append(f"Missing generated data file: {jp}")
            continue
        parsed = json.loads(jp.read_text(encoding="utf-8"))
        if not parsed:
            errors.append(f"Empty JSON dataset: {jp}")

    html_files = sorted(out_dir.rglob("*.html"))
    if len(html_files) < 30:
        errors.append(f"Expected at least 30 generated HTML pages, found {len(html_files)}")

    id_cache: dict[Path, set[str]] = {}
    for hf in html_files:
        text = hf.read_text(encoding="utf-8")
        id_cache[hf.resolve()] = set(re.findall(r'\bid="([^"]+)"', text))

    for hf in html_files:
        text = hf.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            if re.match(r"^(https?://|mailto:|javascript:)", href):
                continue
            path_part, _, anchor = href.partition("#")
            target = (hf.parent / path_part).resolve() if path_part else hf.resolve()
            if not target.exists():
                errors.append(f"{hf.relative_to(out_dir)}: broken internal href '{href}'")
                continue
            if anchor and target.suffix == ".html":
                ids = id_cache.get(target, set())
                if anchor not in ids:
                    errors.append(f"{hf.relative_to(out_dir)}: missing anchor '#{anchor}' in '{href}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Build security-career-paths static site.")
    parser.add_argument("--out", default="dist", help="Output directory (default: dist)")
    parser.add_argument("--check", action="store_true", help="Verify generated HTML links and JSON datasets")
    args = parser.parse_args()

    out_dir = (ROOT / args.out).resolve()
    build_site(out_dir)

    html_count = len(list(out_dir.rglob("*.html")))
    json_count = len(list((out_dir / "data").glob("*.json")))
    print(f"Built static site in {out_dir.relative_to(ROOT)}: {html_count} HTML pages, {json_count} JSON datasets.")

    if args.check:
        errors = check_built_site(out_dir)
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            print(f"\nSite check failed with {len(errors)} error(s).", file=sys.stderr)
            return 1
        print("Site check passed: all generated HTML links, anchors and JSON datasets are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
