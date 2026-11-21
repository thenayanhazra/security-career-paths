# Security operations

*Last reviewed: November 2026*

> Watch an organisation's systems, spot attacks as they happen and start the response.

The security operations centre (SOC) is where most defenders start. It is the front line: alerts arrive from many tools, and analysts decide which ones matter, investigate them and escalate real incidents. It is also the most common entry point into the whole field.

## What the work involves

- Triaging alerts from a SIEM, endpoint detection and response (EDR), email security and cloud tools
- Investigating suspicious activity: following a login, a process or a network connection to work out whether it is malicious
- Escalating confirmed incidents and handing them over cleanly
- Tuning noisy detections and writing new ones
- Hunting proactively for threats that no alert caught

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | SOC analyst (tier 1), security monitoring analyst | Follow runbooks; triage and escalate |
| Mid | SOC analyst (tier 2/3), detection engineer, threat hunter | Investigate end to end; write detections; mentor juniors |
| Senior | Senior detection engineer, SOC lead, security operations manager | Design detection strategy; measure coverage; run the team |

**Framework names:** NICE *Defensive Cybersecurity*; ECSF *Cyber Incident Responder*.

## Skills that matter

- Reading logs from Windows, Linux, network devices and cloud platforms
- Query languages for SIEMs, such as KQL, SPL or SQL
- How attacks unfold, using [MITRE ATT&CK](https://attack.mitre.org/) as the shared language
- Scripting for automation (Python or PowerShell)
- Calm, clear writing: your ticket notes are how the next person picks up the case

## How people get in

The most direct route is applying for tier 1 analyst roles with a foundation certification and a home lab. IT support and service desk staff often move into SOC roles internally. Managed security service providers (MSSPs) hire many juniors and offer broad exposure, at the cost of high volume and shift work.

## Learn for free

- [Splunk's free training courses](https://www.splunk.com/en_us/training/free-courses/overview.html): search and SIEM fundamentals
- [Microsoft Learn: SC-200 learning path](https://learn.microsoft.com/en-us/credentials/certifications/security-operations-analyst/): Microsoft Sentinel and Defender
- [Sigma](https://github.com/SigmaHQ/sigma): the open format for writing detections, with thousands of examples
- [The DFIR Report](https://thedfirreport.com/): detailed write-ups of real intrusions, ideal for learning what attacks look like in logs

## Practise

- [LetsDefend](https://letsdefend.io/) for simulated SOC alert handling
- [CyberDefenders](https://cyberdefenders.org/) and [Blue Team Labs Online](https://blueteamlabs.online/) for investigations
- [Boss of the SOC](https://github.com/splunk/botsv3) datasets in your own Splunk instance
- Build a lab with an open-source SIEM such as [Wazuh](https://wazuh.com/) or [Security Onion](https://securityonionsolutions.com/), attack it with [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team), and write detections for what you see

## Certifications

Starting: Security+. Building: CySA+, Blue Team Level 1, Certified CyberDefender, Microsoft SC-200. Advanced: GIAC GCIA or GCDA. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Incident response and forensics](incident-response-forensics.md) · [Vulnerability management](vulnerability-management.md) · [Threat intelligence](threat-intelligence.md) · [Security engineering](security-engineering-architecture.md) · [Cloud security](cloud-security.md) · [OT and industrial security](ot-industrial-security.md)

---

[← All paths](../README.md#the-paths) · [Guides](../README.md#start-here)
