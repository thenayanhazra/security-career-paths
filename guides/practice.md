# Practice labs and platforms

*Last reviewed: November 2026*

Hands-on practice is what turns knowledge into skill, and what gives you something to talk about in interviews. Most of the platforms below have a free tier; several are entirely free.

## General platforms

| Platform | Best for | Cost |
|---|---|---|
| [TryHackMe](https://tryhackme.com/) | Guided rooms for beginners across both attack and defence | Free tier; paid subscription |
| [Hack The Box](https://www.hackthebox.com/) | Realistic machines and challenges, from easy to very hard | Free tier; paid subscription |
| [Hack The Box Academy](https://academy.hackthebox.com/) | Structured modules with theory and labs | Free and paid modules |
| [picoCTF](https://picoctf.org/) | Capture-the-flag challenges designed for learners | Free |
| [OverTheWire](https://overthewire.org/wargames/) | Linux, web and binary wargames that teach fundamentals | Free |

## Defence

| Platform | Best for | Cost |
|---|---|---|
| [CyberDefenders](https://cyberdefenders.org/) | Blue-team investigations with real artefacts | Free tier; paid |
| [Blue Team Labs Online](https://blueteamlabs.online/) | Investigations and incident response challenges | Free tier; paid |
| [LetsDefend](https://letsdefend.io/) | Simulated SOC analyst work: alerts, triage, cases | Free tier; paid |
| [Splunk Boss of the SOC datasets](https://github.com/splunk/botsv3) | Hunting through a large, realistic dataset in your own Splunk instance | Free |
| [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) | Running small attack simulations to test your detections | Free |
| [Velociraptor](https://docs.velociraptor.app/) | Collecting endpoint forensic artefacts and hunting across lab hosts | Free |

## Web and application security

| Platform | Best for | Cost |
|---|---|---|
| [PortSwigger Web Security Academy](https://portswigger.net/web-security) | The best free web security course available, with hundreds of labs | Free |
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | A deliberately insecure web application to attack locally | Free |
| [crAPI](https://github.com/OWASP/crAPI) | A deliberately vulnerable API | Free |

## Cloud

| Platform | Best for | Cost |
|---|---|---|
| [flaws.cloud](http://flaws.cloud/) and [flaws2.cloud](http://flaws2.cloud/) | Learning common AWS mistakes, from attacker and defender sides | Free |
| [CloudGoat](https://github.com/RhinoSecurityLabs/cloudgoat) | Deploying vulnerable AWS scenarios in your own account | Free; you pay for AWS usage |
| [Kubernetes Goat](https://github.com/madhuakula/kubernetes-goat) | Finding and fixing common Kubernetes and container misconfigurations locally | Free |
| [Stratus Red Team](https://github.com/DataDog/stratus-red-team) | Detonating cloud attack techniques across AWS, Azure, Google Cloud, Kubernetes and Entra ID to test detections | Free; you pay for cloud usage |

## AI security

| Platform | Best for | Cost |
|---|---|---|
| [Gandalf](https://gandalf.lakera.ai/) | Prompt injection by trial and error, in levels | Free |
| [PortSwigger: Web LLM attacks](https://portswigger.net/web-security/llm-attacks) | LLM vulnerabilities in web applications, with labs | Free |
| [Damn Vulnerable LLM Agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent) | Attacking an intentionally vulnerable agent | Free |
| [LLM Prompt Injection Fuzzer](https://github.com/thenayanhazra/llm-prompt-injection-fuzzer) | Measuring how often a model or system prompt can be injected; includes a simulated target that needs no API key | Free |
| [MCP Adversarial Harness](https://github.com/thenayanhazra/mcp-adversarial-harness) | Testing MCP tool servers for tool poisoning and data exfiltration, with a bundled vulnerable server | Free |

## Specialist paths

| Platform | Path | Best for | Cost |
|---|---|---|---|
| [Greenbone Community Edition](https://greenbone.github.io/docs/latest/) | [Vulnerability management](../paths/vulnerability-management.md) | Scanning a home lab and practising risk-based prioritisation | Free |
| [MISP](https://www.misp-project.org/) and [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) | [Threat intelligence](../paths/threat-intelligence.md) | Managing indicator feeds, enriching events and mapping adversary techniques | Free |
| [Keycloak](https://github.com/keycloak/keycloak) | [Identity and access management](../paths/identity-access-management.md) | Running an identity provider locally to practise OIDC, SAML, MFA and API automation | Free |
| [OpenPLC](https://github.com/Autonomy-Logic/openplc-runtime) and [ICS-pcap](https://github.com/automayt/ICS-pcap) | [OT and industrial security](../paths/ot-industrial-security.md) | Simulating a PLC locally and inspecting industrial protocol captures | Free |
| [pwn.college](https://pwn.college/) | [Vulnerability research](../paths/vulnerability-research.md) | Structured binary exploitation and low-level systems labs | Free |
| [CNIL PIA](https://github.com/LINCnil/pia) | [Privacy](../paths/privacy.md) | Running a structured data protection impact assessment | Free |

## Making practice count

- **Write it up.** A short write-up of each machine or investigation shows how you think. Do not publish solutions to active challenges where the platform forbids it.
- **Go past the flag.** After solving a challenge, ask how you would have detected it, or how you would fix it. That second half is what most jobs pay for.
- **Mix sides.** Attackers who understand detection and defenders who understand attacks are both more valuable.

---

[← Overview](../README.md) · [All paths](../README.md#the-paths)
