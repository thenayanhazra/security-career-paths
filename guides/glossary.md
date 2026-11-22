# Glossary

*Last reviewed: November 2026*

Security uses a large number of acronyms and specialist terms. This page defines the ones that appear most often across the paths and guides, in plain language.

## Operations and defence

| Term | Meaning |
|---|---|
| **ATT&CK** | MITRE's public catalogue of adversary tactics, techniques and procedures (TTPs), used as a shared language across defence, detection and intelligence. |
| **CTI** | Cyber threat intelligence: collecting and analysing information about adversaries to support security decisions. |
| **CVSS** | Common Vulnerability Scoring System: a 0–10 technical severity score for vulnerabilities. Useful as a starting point, not a complete measure of real-world risk. |
| **DFIR** | Digital forensics and incident response: investigating intrusions, preserving evidence and containing damage. |
| **EDR** | Endpoint detection and response: software running on laptops and servers to monitor processes, files and network activity and help contain threats. |
| **EPSS** | Exploit Prediction Scoring System: a daily probability estimate (0–100%) that a published vulnerability will be exploited in the wild within 30 days. |
| **IOC** | Indicator of compromise: an artefact linked to an attack, such as a file hash, IP address or domain name. |
| **KEV** | Known Exploited Vulnerabilities: CISA's catalogue of vulnerabilities confirmed to be actively exploited by attackers. |
| **KQL / SPL** | Query languages used to search logs in Microsoft Sentinel/Defender (KQL) and Splunk (SPL). |
| **MSSP / MDR** | Managed security service provider / managed detection and response: external firms that monitor and respond to threats on an organisation's behalf. |
| **SIEM** | Security information and event management: a platform that collects logs from across an organisation so analysts and rules can search and alert on them. |
| **Sigma** | An open, vendor-neutral YAML format for writing log detection rules that can be converted into many SIEM query languages. |
| **SOAR** | Security orchestration, automation and response: tooling that automates repetitive triage, enrichment and containment steps. |
| **SOC** | Security operations centre: the team responsible for continuous monitoring, alert triage and initial response. |
| **SSVC** | Stakeholder-Specific Vulnerability Categorisation: a decision-tree approach to prioritising vulnerabilities based on exploitation status, exposure and business impact. |
| **STIX** | Structured Threat Information Expression: a standard JSON format for exchanging threat intelligence between tools and teams. |
| **TTP** | Tactics, techniques and procedures: the patterns of behaviour an adversary uses, harder for attackers to change than IP addresses or hashes. |
| **YARA** | A pattern-matching language used to identify and classify malware files or suspicious artefacts in memory and on disk. |

## Attack, software and application security

| Term | Meaning |
|---|---|
| **ASPM** | Application security posture management: aggregating and prioritising findings from code, dependency, container and runtime scanners in one view. |
| **ASVS** | OWASP Application Security Verification Standard: a detailed checklist of security requirements for designing, building and testing web applications. |
| **CI/CD** | Continuous integration and continuous delivery: automated pipelines that build, test and deploy code. |
| **CVE** | Common Vulnerabilities and Exposures: a public identifier (such as `CVE-2026-12345`) for a specific disclosed software vulnerability. |
| **DAST** | Dynamic application security testing: testing a running application from the outside to find vulnerabilities. |
| **Fuzzing** | Feeding huge volumes of malformed or unexpected inputs into a programme automatically to trigger crashes and uncover unknown bugs. |
| **IDOR** | Insecure direct object reference: an access-control flaw where changing an identifier (such as a record ID) lets a user read or alter someone else's data. |
| **SAST** | Static application security testing: analysing source code without running it to spot potential security flaws. |
| **SBOM** | Software bill of materials: a structured inventory of the libraries and components inside a piece of software. |
| **SCA** | Software composition analysis: scanning a project's third-party dependencies for known vulnerabilities and licence risks. |
| **SLSA** | Supply-chain Levels for Software Artifacts: a framework for protecting how software is built, signed and distributed. |
| **SSRF** | Server-side request forgery: a flaw that lets an attacker make a server send HTTP or network requests to internal or unintended destinations. |
| **Threat modelling** | Structuring what can go wrong in a system before it is built, deciding which risks matter and choosing mitigations. |

## Cloud, identity and industrial systems

| Term | Meaning |
|---|---|
| **CSPM** | Cloud security posture management: continuous checking of cloud accounts (AWS, Azure, GCP) for misconfigurations and risky permissions. |
| **IaC** | Infrastructure as code: defining cloud networks, servers and permissions in version-controlled files (such as Terraform). |
| **IAM** | Identity and access management: controlling who and what can authenticate and what actions they are authorised to perform. |
| **ICS / OT** | Industrial control systems / operational technology: hardware and software that monitor or control physical processes (factories, power grids, water plants). |
| **MFA** | Multi-factor authentication: requiring more than one proof of identity (such as a password plus a passkey or hardware key). |
| **NHI** | Non-human identity: credentials used by software rather than people—service accounts, API keys, workload identities and AI agents. |
| **OAuth 2.0 / OIDC** | Open protocols for delegated authorisation (OAuth 2.0) and user sign-in (OpenID Connect). **PKCE** protects the sign-in flow against code interception. |
| **PAM** | Privileged access management: tightly controlling, recording and time-limiting administrator and root access. |
| **PLC / SCADA** | Programmable logic controller (industrial computer controlling machinery) and supervisory control and data acquisition (systems that monitor and control industrial sites). |
| **SAML / SCIM** | Standards for enterprise single sign-on (SAML) and automated user provisioning/deprovisioning between identity providers and apps (SCIM). |
| **Zero trust** | An architectural principle that no user, device or service is trusted merely because it sits inside a corporate network. |

## Governance, risk, compliance and privacy

| Term | Meaning |
|---|---|
| **DPIA** | Data protection impact assessment: a structured review of how a new system or process collects and uses personal data, and how privacy risks are reduced. |
| **ECSF** | ENISA's European Cybersecurity Skills Framework: twelve standard role profiles used across Europe. |
| **GDPR** | General Data Protection Regulation: the European Union's comprehensive data protection law, influential worldwide. |
| **GRC** | Governance, risk and compliance: setting security policy, assessing risk and demonstrating adherence to standards and regulations. |
| **ISO/IEC 27001** | The leading international standard for running an information security management system (ISMS). |
| **NICE Framework** | NIST's Workforce Framework for Cybersecurity (v2.2.0), defining standard security work roles, tasks and skills. |
| **PCI DSS** | Payment Card Industry Data Security Standard: security requirements for organisations that process, store or transmit payment card data. |
| **ROPA** | Record of processing activities: an inventory documenting what personal data an organisation holds, why it holds it and where it goes. |
| **SOC 2** | An independent attestation report (common in SaaS) evaluating a service provider's controls against security, availability and confidentiality criteria. |

## AI security and governance

| Term | Meaning |
|---|---|
| **ATLAS** | MITRE's public knowledge base of adversary tactics and techniques targeting AI systems. |
| **EU AI Act** | European Union legislation regulating AI systems by risk tier, with obligations for providers and deployers. |
| **ISO/IEC 42001** | The international standard for an artificial intelligence management system (AIMS). |
| **Jailbreak** | Prompting or manipulating a model to bypass its safety or behavioural guardrails. |
| **LLM** | Large language model: a neural network trained on large text corpora that generates text, code or tool calls in response to prompts. |
| **MCP** | Model Context Protocol: an open protocol connecting AI models and agents to external tools, files and data sources. |
| **Prompt injection** | Untrusted text that overrides or redirects an LLM's instructions—**direct** (from the user) or **indirect** (hidden inside a web page, email or document an agent reads). |
| **RAG** | Retrieval-augmented generation: fetching external documents (for example from a vector database) and inserting them into a model's prompt at query time. |

---

[← Overview](../README.md) · [All paths](../README.md#the-paths)
