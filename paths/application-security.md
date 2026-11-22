# Application and product security

*Last reviewed: November 2026*

> Help engineering teams build software that is secure by design, and catch what slips through before customers do.

Application security (AppSec) engineers sit between security and software development. They threat model new features, review code, run security testing in the build pipeline and, above all, make it easy for developers to do the secure thing. In product companies the role is often called product security and extends to the whole product, including hardware and the supply chain.

## What the work involves

- Threat modelling designs before they are built
- Reviewing code and pull requests for security flaws
- Running and tuning static analysis, dependency scanning and secret scanning in CI/CD
- Testing applications and APIs
- Building secure libraries, defaults and guardrails so developers do not have to be experts
- Running a security champions programme and training engineers
- Triaging bug bounty reports and coordinating fixes

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | Application security engineer (junior), security analyst (AppSec) | Run tools; triage findings; review code with guidance |
| Mid | Application security engineer, product security engineer, DevSecOps engineer | Own security for several teams; threat model; build tooling |
| Senior | Staff/principal AppSec engineer, product security lead | Set the secure development programme; influence architecture |

**Framework names:** NICE *Secure Software Development*, *Software Security Assessment*; ECSF *Cybersecurity Implementer*, *Cybersecurity Architect*.

## Skills that matter

- Writing code in at least one mainstream language, and reading several
- Web and API vulnerability classes, as described by the [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- Threat modelling
- CI/CD pipelines and supply chain security
- Influence: you rarely fix code yourself; you persuade the people who do

## How people get in

Software developers make the move most often, and are well placed to: they understand the code and the culture. Penetration testers who want to fix as well as find are the other common source.

## Learn for free

- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OpenSSF Secure Software Development Fundamentals](https://openssf.org/training/courses/): free online courses covering secure design, implementation and verification
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/): what "secure" means, requirement by requirement
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/): concise guidance on specific problems
- [OWASP SAMM](https://owaspsamm.org/): a maturity model for building and measuring an application security programme
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/) and the [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/)
- [SLSA](https://slsa.dev/): a framework for software supply chain integrity

## Practise

- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) and [crAPI](https://github.com/OWASP/crAPI): find the flaws, then fix them in the source
- Add security scanning to a CI pipeline for one of your own projects, and tune out the noise
- Threat model an open-source application and write it up
- Review an authentication or API module in an open-source repository against [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), and write clear, developer-friendly fix guidance for what you find

## Certifications

Starting: Security+. Building: Burp Suite Certified Practitioner, GIAC GWEB, Certified DevSecOps Professional. Advanced: CSSLP, OSWE. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Offensive security](offensive-security.md) · [Vulnerability research](vulnerability-research.md) · [Vulnerability management](vulnerability-management.md) · [Cloud security](cloud-security.md) · [AI security engineering](ai-security-engineering.md) · [Security engineering](security-engineering-architecture.md) · [Privacy](privacy.md)

---

[← All paths](../README.md#the-paths) · [Guides](../README.md#start-here)
