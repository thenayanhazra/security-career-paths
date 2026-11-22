# Offensive security

*Last reviewed: November 2026*

> Test systems the way a real attacker would, with permission, and explain how to fix what you find.

Penetration testers and red teamers attack organisations on their behalf. Penetration tests look for as many weaknesses as possible in a defined scope. Red team engagements emulate a specific adversary to test whether defenders notice and respond. The report at the end matters as much as the hacking.

## What the work involves

- Testing web applications, networks, Active Directory, cloud environments and mobile apps
- Running red team engagements with defined objectives and rules of engagement
- Writing reports that explain risk to executives and fixes to engineers
- Building and maintaining tooling and infrastructure
- Bug bounty hunting, as a side activity or occasionally a full-time living

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | Junior penetration tester, security consultant | Test within a scope under supervision; write report sections |
| Mid | Penetration tester, red team operator | Lead tests; specialise (web, cloud, AD, mobile, hardware) |
| Senior | Principal consultant, red team lead, head of offensive security | Design engagements; manage clients and teams; build capability |

**Framework names:** NICE *Vulnerability Analysis*; ECSF *Penetration Tester*.

## Skills that matter

- Web application security in depth
- Windows and Active Directory attacks
- Networking and Linux
- Scripting and tool development
- Report writing: clear, prioritised, actionable
- Strong ethics and scrupulous respect for scope and authorisation

## How people get in

Some testers are hired straight from study with strong lab work and an entry certification. Many come from system administration, networking or development, which gives them the depth to understand what they are attacking. Consultancies are the main employers; large organisations also run internal teams.

**Only ever test systems you own or have written permission to test.** Unauthorised testing is illegal in most countries, whatever the intent.

## Trade-offs

- **Heavy competition at entry level:** far more people want to be penetration testers than there are junior roles, so the bar for first jobs is high.
- **Report writing and tight timelines:** consulting engagements are often short and compliance-driven, with 30–40% of your time spent documenting findings cleanly.
- **Repetitive findings:** you will find the same missing headers, weak passwords and misconfigurations many times before seeing a novel exploit chain.

## Learn for free

- [PortSwigger Web Security Academy](https://portswigger.net/web-security): the best free web security training anywhere
- [HackTricks](https://book.hacktricks.wiki/): an encyclopaedic reference of techniques
- [The Hacker Recipes](https://www.thehacker.recipes/): especially strong on Active Directory
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/): a structured testing methodology

## Practise

- [Hack The Box](https://www.hackthebox.com/) and [TryHackMe](https://tryhackme.com/)
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) locally
- Build a small Active Directory lab and attack it
- Bug bounty programmes on public platforms, once you have the basics, with their rules followed exactly

## Ready to apply

You are ready to interview for a junior offensive security role when you can:

- Follow a structured methodology across a web application or internal network rather than running scanners blindly
- Explain common web and Active Directory flaws (such as IDOR, SQL injection, SSRF and Kerberoasting) in terms of root cause, impact and fix
- Produce a crisp penetration-test report sample with an executive summary, reproduction steps and practical remediation advice
- Respect scope, rules of engagement and safe testing practices without prompting

## Certifications

Starting: eJPT, PenTest+. Building: PNPT, OSCP, Burp Suite Certified Practitioner, CRTO. Advanced: OSEP, OSWE, GIAC GPEN, GXPN. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Vulnerability research](vulnerability-research.md) · [Application security](application-security.md) · [AI red teaming](ai-red-teaming.md) · [Detection engineering](detection-engineering.md) · [Threat intelligence](threat-intelligence.md) · [Incident response and forensics](incident-response-forensics.md)

---

[← All paths](../README.md#the-paths) · [Guides](../README.md#start-here)
