# Contributing

Thank you for helping keep this guide accurate and useful. The most valuable contributions are:

1. **Corrections.** A certification renamed or retired, a programme closed, a link that now goes somewhere else, a fact that has gone out of date.
2. **Resources you genuinely used.** Something that helped you learn or get hired, especially if it is free.
3. **Missing perspective.** How a path works in your country or sector, if it differs from what is written here.

## How to contribute

- **Quick suggestion:** open an issue using the [resource](https://github.com/thenayanhazra/security-career-paths/issues/new?template=resource.yml), [correction](https://github.com/thenayanhazra/security-career-paths/issues/new?template=correction.yml) or [new path / regional perspective](https://github.com/thenayanhazra/security-career-paths/issues/new?template=perspective.yml) template.
- **Direct edit:** open a pull request. Keep each one to a single change or a closely related set, so it can be reviewed quickly.

## What gets added

A resource is a good fit when it is:

- **Free or has a meaningful free tier.** Paid resources are included only when nothing free comes close.
- **Maintained.** Updated within the last two years, or timeless (a classic text, a standard).
- **Better than what is already listed,** or covers something that is not. Each page lists a few strong resources, not every resource.
- **Not primarily marketing.** Vendor training is fine when it teaches the subject, not just the product.

Resources the maintainer has written are allowed, but held to the same standard as everything else.

## Page structure

Every path page follows the same order, so readers can compare paths side by side:

1. Title, a *Last reviewed* line, and a one-sentence summary in a block quote
2. A short introduction
3. **What the work involves**
4. **Roles along the way**: a table of entry, mid and senior titles, then the closest NICE and ECSF role names
5. **Skills that matter**
6. **How people get in**
7. **Trade-offs**: three candid points on what people find hard or dislike about the path
8. **Learn for free**
9. **Practise**
10. **Ready to apply**: concrete, observable checkpoints for interview readiness
11. **Certifications**, by level, linking to the certifications guide
12. **Neighbouring paths**

When you add a path, also update the README table and diagram, the [certifications guide](guides/certifications.md), the resource issue template, and any relevant rows in [choosing a path](guides/choosing-a-path.md), [getting your first role](guides/first-role.md) and [moving between paths](guides/moving-between-paths.md).

## Style

- British English spelling (organisation, prioritise, defence).
- Plain, direct sentences. Write for someone intelligent who is new to the field.
- State facts that can be checked, with dates where they matter ("launched in February 2026", not "recently launched").
- No hype. If a path is hard to enter, say so.
- When you change a page, update its *Last reviewed* line.

## Checks and links

Structure, cross-references (README diagram and table, choosing-a-path tables, certifications parity), local links, anchors, guide footers and reciprocal neighbouring-path links are checked automatically on every pull request with `python3 scripts/validate.py`. External links are checked weekly and on every pull request. A few sites block automated checkers even though the page works; those are listed in [`.lycheeignore`](.lycheeignore). Add a site there only after confirming the page loads in a browser.
