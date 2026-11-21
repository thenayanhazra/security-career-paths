# Security engineering and architecture

*Last reviewed: November 2026*

> Design, build and run the security controls everything else depends on, and make sure they fit together.

Security engineers build and operate security infrastructure: identity platforms, endpoint protection, network controls, logging pipelines, encryption and secrets management. Security architects take a wider view, deciding how controls fit together across the organisation and making trade-offs between security, cost and usability explicit.

## What the work involves

- Deploying and running security platforms: EDR, SIEM, firewalls, email security, secrets management
- Building automation that connects them
- Hardening systems and setting secure baselines
- Reviewing designs for new systems and changes
- Creating reference architectures and standards
- Designing for zero trust: no implicit trust based on network location

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | Security engineer (junior), security administrator | Run and maintain platforms |
| Mid | Security engineer, infrastructure security engineer | Design and build controls; automate; own platforms end to end |
| Senior | Senior/principal security engineer, security architect, enterprise security architect | Set architecture and standards; review major designs; decide trade-offs |

**Framework names:** NICE *Cybersecurity Architecture*, *Enterprise Architecture*, *Systems Security Analysis*; ECSF *Cybersecurity Architect*, *Cybersecurity Implementer*.

## Skills that matter

- Breadth across networks, systems, identity, cloud and applications
- Depth in at least one of them
- Automation and infrastructure as code
- Clear design documents and diagrams
- The ability to say no constructively, by offering a safer way to get the same result

## How people get in

Security engineering is usually a second or third role, after system administration, networking, cloud engineering or security operations. Architecture typically follows several years of engineering.

## Learn for free

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks): configuration baselines for common systems (free registration)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [Open Security Architecture](https://www.opensecurityarchitecture.org/): patterns and control catalogues

## Practise

- Harden a Linux server against a CIS Benchmark, automate both the configuration and compliance checks with a script or Ansible, and verify it passes
- Design the security architecture for a fictional 500-person company (identity, network segmentation, logging, secrets management and CI/CD), document the trade-offs explicitly, and ask experienced practitioners to critique it
- Replace static credentials in a lab application with short-lived tokens or a local secrets manager and centralise its audit logs
- Take an existing system diagram and write a one-page architecture review noting trust boundaries, single points of failure and three pragmatic mitigations

## Certifications

Building: CySA+ and cloud security certifications. Advanced: CISSP, CompTIA SecurityX (formerly CASP+), Microsoft SC-100, SABSA. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Cloud security](cloud-security.md) · [Identity and access management](identity-access-management.md) · [Application security](application-security.md) · [Security operations](security-operations.md) · [Vulnerability management](vulnerability-management.md) · [OT and industrial security](ot-industrial-security.md) · [Security leadership](security-leadership.md)
