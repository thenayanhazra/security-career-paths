# AI red teaming

*Last reviewed: November 2026*

> Find the ways AI models and agents can be made to fail, misbehave or be misused, before real adversaries do.

AI red teamers probe AI systems adversarially. Some focus on security: injecting instructions, extracting hidden context, turning an agent's tools against its user. Others focus on safety: getting a model to produce harmful content or behave in ways its developers did not intend. Many roles cover both. The output is the same as any red team: findings, evidence and recommendations.

## What the work involves

- Designing attack scenarios for models, applications and agents
- Prompt injection, jailbreaking and extraction of system prompts or training data
- Attacking agent tools, memory and multi-agent workflows
- Building automated attack tooling and evaluation datasets
- Measuring results consistently so fixes can be verified
- Writing findings that engineers can act on

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | Rare as a first role; usually offensive security or ML first | Contribute test cases and findings under guidance |
| Mid | AI red teamer, AI security researcher, adversarial ML engineer | Lead assessments; build tooling; publish |
| Senior | AI red team lead, principal AI security researcher | Set methodology; lead programmes at AI labs or large enterprises |

**Framework names:** no AI-specific role yet in NICE or ECSF. Closest: NICE *Vulnerability Analysis* and *Technology Research and Development*; ECSF *Penetration Tester* and *Cybersecurity Researcher*.

## Skills that matter

- An offensive security mindset and methodology
- How models, retrieval and agents work, and where their trust boundaries are
- Python and automation, because manual testing does not scale
- Careful measurement: a single successful jailbreak is an anecdote; a bypass rate is evidence
- Responsible handling of harmful outputs and disclosure

## How people get in

Mostly from offensive security, ML engineering or safety research. AI labs, large technology companies and specialist consultancies hire most AI red teamers. Public findings, competition results and open-source tooling are the strongest evidence of ability.

## Learn for free

- [MITRE ATLAS](https://atlas.mitre.org/): the adversary techniques and real-world case studies
- [OWASP GenAI Security Project](https://genai.owasp.org/): including its red teaming guidance
- [PyRIT](https://github.com/Azure/PyRIT): Microsoft's open-source framework for AI red teaming
- [garak](https://github.com/NVIDIA/garak): NVIDIA's open-source LLM vulnerability scanner
- [Microsoft's lessons from red teaming 100 generative AI products](https://www.microsoft.com/en-us/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)

## Practise

- [Gandalf](https://gandalf.lakera.ai/): prompt injection in levels
- [PortSwigger: Web LLM attacks](https://portswigger.net/web-security/llm-attacks)
- [Damn Vulnerable LLM Agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent)
- Run [LLM Prompt Injection Fuzzer](https://github.com/thenayanhazra/llm-prompt-injection-fuzzer) against a local model and compare bypass rates across system prompts
- Run [MCP Adversarial Harness](https://github.com/thenayanhazra/mcp-adversarial-harness) against its bundled vulnerable server, then write a detection for each finding

## Certifications

There is no established certification for this path yet. CompTIA SecAI+ covers the basics, an offensive security certification such as OSCP shows methodology, and GIAC GASAE covers AI-driven automation. A portfolio of findings matters most. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Offensive security](offensive-security.md) · [AI security engineering](ai-security-engineering.md) · [Vulnerability research](vulnerability-research.md)
