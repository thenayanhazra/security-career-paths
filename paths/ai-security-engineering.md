# AI security engineering

*Last reviewed: November 2026*

> Secure applications and agents built on large language models and other AI systems, from design through to production.

AI systems bring familiar risks in a new form and some genuinely new ones. A model can be instructed by any text it reads, so a web page or an email can redirect an agent that holds real credentials. AI security engineers design systems that stay safe when that happens: separating instructions from data, limiting what agents can do, vetting tools and models, and monitoring behaviour in production.

The field is young. Many of the people doing this work today were application, cloud or ML engineers two or three years ago.

## What the work involves

- Threat modelling AI applications and agents
- Defending against prompt injection, data leakage and tool misuse
- Designing least-privilege access for agents, and approval steps for consequential actions
- Vetting third-party models, MCP servers, plugins and skills before they are used
- Securing retrieval pipelines, embeddings and agent memory
- Building guardrails, output filtering and monitoring
- Testing AI systems before release and in CI, with measurable thresholds

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | Rarely an entry role; usually AppSec, cloud security or ML engineering first | Learn AI risks while doing an adjacent job |
| Mid | AI security engineer, ML security engineer, product security engineer (AI) | Secure AI features end to end; build guardrails and tests |
| Senior | Staff AI security engineer, AI security architect, head of AI security | Set AI security standards and architecture across products |

**Framework names:** neither NICE nor ECSF has an AI-specific security role yet. The closest are NICE *Secure Software Development* and *Cybersecurity Architecture*, and ECSF *Cybersecurity Architect*.

## Skills that matter

- Application security fundamentals: this is AppSec applied to a new kind of system
- How LLMs, retrieval, tool calling and agents actually work
- Prompt injection in its direct and indirect forms, and why it cannot be fully solved inside the model
- Identity and authorisation for non-human actors
- Python, and familiarity with common AI frameworks and the Model Context Protocol (MCP)
- Evaluation: measuring whether a defence works rather than assuming it does

## How people get in

From application security, cloud security or ML engineering, usually by taking ownership of security for an AI feature in a current job. Building and publishing small tools or research is the most effective way to show ability in a field this new.

## Learn for free

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) (2026 edition) and the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [MITRE ATLAS](https://atlas.mitre.org/): adversary techniques against AI systems, with real case studies
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) and its [Generative AI Profile (NIST AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices): attacks and mitigations for agent tool servers
- [Simon Willison's writing on prompt injection](https://simonwillison.net/tags/prompt-injection/): the clearest ongoing commentary on the problem
- [Agentic AI reference threat model](https://github.com/thenayanhazra/ai-security-governance/blob/main/threat-models/agentic-ai-reference-threat-model.md): seventeen common threats to agents, with controls and tests

## Practise

- [PortSwigger: Web LLM attacks](https://portswigger.net/web-security/llm-attacks) labs
- Build a small agent with one tool, attack it with indirect prompt injection, then redesign it so the attack no longer matters
- Scan agent instruction files and MCP configurations with [agentlint](https://github.com/thenayanhazra/agentlint)
- Test an MCP server with [MCP Adversarial Harness](https://github.com/thenayanhazra/mcp-adversarial-harness)
- Measure a system prompt's resistance with [LLM Prompt Injection Fuzzer](https://github.com/thenayanhazra/llm-prompt-injection-fuzzer) or open-source tools such as [promptfoo](https://github.com/promptfoo/promptfoo)

## Certifications

Building: CompTIA SecAI+, CAISP. Advanced: GIAC GAIPS, GASAE. These are all new; a portfolio of work carries more weight for now. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Application security](application-security.md) · [Cloud security](cloud-security.md) · [AI red teaming](ai-red-teaming.md) · [AI governance and assurance](ai-governance-assurance.md)
