# Changelog

Notable dated editions and content updates to **Security Career Paths**.

This guide uses dated releases (`YYYY.MM`) to record major industry refreshes—certification changes, new frameworks, added paths and tooling improvements.

## [2026.11] — November 2026

Initial comprehensive edition, expanded across four milestones:

### Career paths (18 paths across 6 families)
- **Defend:** Security operations, Detection engineering, Vulnerability management, Incident response and digital forensics, Threat intelligence
- **Attack and assess:** Offensive security, Vulnerability research
- **Build:** Application and product security, Cloud security, Security engineering and architecture, Identity and access management, OT and industrial security
- **Govern:** Governance, risk and compliance, Privacy
- **AI security:** AI security engineering, AI red teaming, AI governance and assurance
- **Leadership:** Security leadership
- Every path includes uniform sections covering daily work, role progression mapped to **NICE v2.2.0** (April 2026) and **ENISA ECSF**, skills, routes in, candid **Trade-offs**, free learning resources, 4–5 hands-on practice exercises, concrete **Ready to apply** checkpoints, certifications, and reciprocal neighbouring paths.

### Cross-cutting guides (12 guides)
- *How to choose a path*, *Foundations*, *Getting your first role*, *Interviews and portfolios*, *Where security teams sit* (employer types and US, EU, UK, India, Australia/ASD Essentials & Singapore context), *Moving between paths*, *Advancing past mid-level* (Staff+ IC and management), *Certifications by path and level*, *Practice labs and platforms*, *Working with AI in security*, *Staying current*, and *Glossary*.
- Reflects 2026 certification updates: CompTIA Security+ V8 (`SY0-801`), CompTIA `SecAI+`, GIAC `GAIPS`/`GASAE`, ISACA `AAISM`/`AAIA`/`AAIR`, ISC2 CC free programme closure (May 2026), and OWASP Top 10 for LLM and Agentic Applications (2026).

### Web edition, interactive tools & machine-readable data
- Published searchable static documentation site on GitHub Pages with light/dark theme, sticky family sidebar, TOC scrollspy and keyboard search (`/` or `⌘K`).
- Added three client-side tools built directly from canonical Markdown: **Interactive Path Finder**, **Certifications Explorer**, and **Career Transition Map**.
- Exported CC BY 4.0 JSON datasets (`paths.json`, `certifications.json`, `transitions.json`, `guides.json`, `search-index.json`).

### Quality & community automation
- Automated structure, cross-reference, Mermaid diagram, certification-parity and local-link validation (`scripts/validate.py`).
- Automated static site build and internal HTML link checks (`scripts/build_site.py --check`).
- Weekly external link checking (`links.yml`) with automatic issue reporting on scheduled failures, plus monthly review-staleness checks (`staleness.yml`).
- Issue templates for resources, corrections, and new path / regional perspective proposals, plus PR checklist and Code of Conduct.
