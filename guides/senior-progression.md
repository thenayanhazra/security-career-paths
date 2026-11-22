# Advancing past mid-level

*Last reviewed: November 2026*

Getting into security is one challenge; moving from a capable mid-level practitioner to a senior, staff, principal or management role is a different one. Past mid-level, working harder on individual tickets, findings or audits stops scaling. Progression depends on changing the scope of the problems you solve.

## Two tracks after senior

Most mature organisations split senior progression into two parallel tracks. Neither is "above" the other, and people sometimes switch between them once or twice.

| Track | Typical titles | Primary leverage | What fills your week |
|---|---|---|---|
| **Individual contributor (Staff+)** | Staff security engineer, principal researcher, principal security architect, distinguished engineer | Technical strategy, architecture, paved roads, cross-team alignment | Design reviews, RFCs, high-risk incidents, eliminating entire classes of flaws, mentoring senior engineers |
| **Management and leadership** | Security manager, head of AppSec/SOC/GRC, director, VP security, CISO | People, priorities, budgets, organisational alignment | Hiring and developing teams, setting roadmaps, negotiating with executives, owning risk accountability |

See [Security leadership](../paths/security-leadership.md) for the management track in detail.

## What changes from mid-level to Staff+

- **From fixing instances to eliminating classes.** A mid-level AppSec engineer finds and helps fix twenty SQL injection bugs. A staff engineer introduces a parameterised query wrapper and a CI check so that class of bug stops appearing.
- **From owning a tool to owning an outcome.** Running a vulnerability scanner or SIEM well is mid-level work. Proving that mean time to contain or exposure on internet-facing assets dropped measurably is senior and staff work.
- **Influence without authority.** The people who must adopt your secure default, patch schedule or architecture rarely report to you. Writing clear proposals (RFCs), listening to engineering constraints and making the safe path the easiest path matter as much as technical depth.
- **Multiplying other people.** Reviewing designs, pairing with juniors, writing reusable runbooks and raising the bar for the whole team creates far more security than heroics from one person.
- **Explicit trade-offs.** Senior practitioners stop saying "this is insecure" and start saying "here are three options, what each costs in engineering time, and the residual risk of each."

## How to build the case for promotion

1. **Pick one messy, cross-team problem nobody owns.** Examples: non-human identity sprawl, noisy detections nobody trusts, slow third-party risk reviews, or ungoverned AI tool adoption.
2. **Write the problem down clearly.** A two-page document stating the current risk, evidence, options and proposed plan often creates leadership buy-in faster than months of informal complaints.
3. **Measure before and after.** Track a simple baseline—false-positive rate, overdue critical exposures, percentage of services using SSO or short-lived credentials—so the impact is visible.
4. **Broaden beyond your home path.** T-shaped practitioners—deep in one path, fluent in two or three neighbouring paths—handle ambiguous senior problems far better than narrow specialists. See [Moving between paths](moving-between-paths.md).

## Common traps

- **Moving into management only for pay or status.** If you hate people management, performance reviews and budget politics, you will be miserable and your team will feel it. Look for organisations with a genuine Staff+ IC ladder instead.
- **Becoming a single point of failure.** Being the only person who understands the SIEM or the IAM platform feels like job security, but it blocks you from stepping up to larger work.
- **Chasing complexity over impact.** Senior work is often unglamorous—asset inventory, phishing-resistant MFA, killing static credentials, simplifying a broken exception process—because those are the things that actually prevent breaches.

---

[← Overview](../README.md) · [All paths](../README.md#the-paths)
