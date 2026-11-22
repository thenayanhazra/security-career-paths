# Detection engineering

*Last reviewed: November 2026*

> Build, test and maintain the rules and telemetry pipelines that turn raw logs into reliable alerts.

Detection engineers treat threat detection as a software engineering discipline. Rather than working an alert queue shift by shift, they study how attackers operate, check whether the organisation collects the right logs to see them, write detections as version-controlled code, test them against simulated attacks and continuously strip out noise.

## What the work involves

- Translating attacker techniques and intrusion reports into high-signal detection rules
- Treating detections as code: version control, peer review, automated testing and CI/CD deployment
- Designing and tuning log pipelines across endpoints, identity providers, cloud accounts and networks
- Measuring coverage against threat models and frameworks such as MITRE ATT&CK, and closing telemetry gaps
- Working with SOC analysts and incident responders to retire noisy rules and capture lessons from real incidents
- Running purple-team exercises with offensive teams to verify detections actually fire

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | Junior detection engineer, SOC analyst focusing on content | Tune existing rules; write straightforward queries with review |
| Mid | Detection engineer, detection and response engineer | Own detection-as-code pipelines; design telemetry; test against adversary simulations |
| Senior | Senior/staff detection engineer, detection engineering lead | Set detection strategy and coverage metrics; architect telemetry platforms at scale |

**Framework names:** NICE *Defensive Cybersecurity* and *Systems Security Analysis*; ECSF *Cyber Incident Responder* and *Cybersecurity Implementer*.

## Skills that matter

- Query languages and rule formats: KQL, SPL, SQL, [Sigma](https://github.com/SigmaHQ/sigma) and [YARA](https://github.com/VirusTotal/yara)
- Software engineering habits: Python or Go, Git, unit testing and CI/CD pipelines
- Deep understanding of Windows, Linux, identity and cloud audit logs—what normal looks like and where attackers hide
- Attacker tradecraft and [MITRE ATT&CK](https://attack.mitre.org/)
- Data engineering basics: log schemas, parsing, cost control and pipeline reliability

## How people get in

From two main directions: SOC analysts who learn software engineering and detections-as-code, and software or data engineers who learn attacker techniques and log analysis. It is rarely a first job straight out of study, because writing good detections requires knowing both how attacks unfold and how noisy enterprise environments behave.

## Trade-offs

- **Unending maintenance:** software updates and normal IT changes constantly break assumptions and turn quiet rules noisy.
- **Telemetry limits:** you are often constrained by missing logs, vendor ingestion costs and teams reluctant to enable verbose auditing.
- **Invisible success:** good detection work is quiet until a real intrusion occurs, which can make demonstrating value harder than closing tickets.

## Learn for free

- [Sigma](https://github.com/SigmaHQ/sigma): the open, vendor-neutral detection rule format with thousands of community rules to study
- [Elastic Detection Rules](https://github.com/elastic/detection-rules): a large public repository of production-grade detections with tests and documentation
- [YARA](https://github.com/VirusTotal/yara): pattern matching for files, binaries and memory artefacts
- [The DFIR Report](https://thedfirreport.com/): step-by-step intrusion reconstructions showing exact attacker commands and log artefacts
- [Microsoft Learn: SC-200 learning path](https://learn.microsoft.com/en-us/credentials/certifications/security-operations-analyst/): KQL and Microsoft Sentinel/Defender detection concepts

## Practise

- Run [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) or [Stratus Red Team](https://github.com/DataDog/stratus-red-team) techniques in a lab, inspect the resulting logs, and write a [Sigma](https://github.com/SigmaHQ/sigma) rule that detects the behaviour rather than a single hardcoded command
- Put a small set of detection rules in a Git repository with positive and negative test log samples and a CI check that validates syntax and test cases on every change
- Take a noisy rule from a public ruleset, test it against realistic benign activity in your lab or [Boss of the SOC](https://github.com/splunk/botsv3) data, and document how you tuned false positives without losing true detections
- Pick one intrusion from [The DFIR Report](https://thedfirreport.com/), list every log source needed to catch it early, and write two detections targeting different stages of the attack chain

## Ready to apply

You are ready to interview for a detection engineering role when you can:

- Write a behavioural detection in KQL, SPL, SQL or Sigma from raw logs and explain its blind spots and likely false positives
- Explain how to store, test, review and deploy detections as code using Git and CI
- Diagnose why a simulated attack failed to trigger an alert (missing telemetry, broken parsing, wrong logic or alert suppression)
- Balance detection coverage against alert fatigue and log-ingestion cost

## Certifications

Starting: Security+. Building: CySA+, Certified CyberDefender, Microsoft SC-200. Advanced: GIAC GCDA or GCIA. A public GitHub repository of tested Sigma/YARA rules and write-ups often carries as much weight as any exam. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Security operations](security-operations.md) · [Incident response and forensics](incident-response-forensics.md) · [Threat intelligence](threat-intelligence.md) · [Cloud security](cloud-security.md) · [Security engineering and architecture](security-engineering-architecture.md) · [Offensive security](offensive-security.md)

---

[← All paths](../README.md#the-paths) · [Guides](../README.md#start-here)
