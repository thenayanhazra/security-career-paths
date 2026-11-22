# Working with AI in security

*Last reviewed: November 2026*

Artificial intelligence has not just created [AI security paths](../README.md#the-paths); it has changed how every security path is practised, learned and hired for. Used well, AI tools speed up routine work and act as an always-available tutor. Used carelessly, they hollow out the fundamentals you need to pass interviews and make sound judgments under pressure.

## How AI is used across security work

In 2026, most security teams use AI assistants for parts of the job where speed and synthesis matter, while keeping humans responsible for verification and decisions:

| Family | Where AI genuinely helps | Where human judgment still decides |
|---|---|---|
| **Defend** | Drafting SIEM queries (KQL, SPL, SQL), summarising long alert timelines, explaining unfamiliar scripts or obfuscated commands | Confirming whether an alert is benign or malicious, scoping containment, managing false positives in production |
| **Attack and assess** | Reviewing unfamiliar codebases, generating test harnesses, drafting report sections from raw notes | Chaining subtle business-logic flaws, staying within scope, proving real-world impact |
| **Build** | Explaining unfamiliar cloud IAM policies, scaffolding Terraform or policy-as-code tests, first-pass code review | Setting trust boundaries, weighing usability against risk, persuading engineering teams |
| **Govern** | Cross-mapping control frameworks, summarising regulatory text, drafting policy skeletons | Assessing whether a control actually works, judging acceptable risk, briefing executives |

## The learning trap

The biggest risk for beginners and career changers is letting an assistant solve labs, write scripts or draft reports before you have struggled with the problem yourself.

- **Recognition is not recall.** Reading an AI-generated explanation of TLS, Kerberos or OAuth feels like understanding, until an interviewer asks you to trace a packet capture or debug a broken flow without a browser.
- **Plausible errors are subtle.** Models frequently invent command flags, misread cloud policy precedence or miss edge cases in detection logic. You can only catch those mistakes if you know the underlying system.
- **Unedited AI writing stands out.** Hiring managers recognise generic AI-generated write-ups and CVs immediately. Plain, specific notes in your own words carry far more weight.

## Using AI well while learning

- **Attempt first, ask second.** Write the query, script, threat model or risk summary yourself before asking a model to critique it.
- **Ask for hints and counter-arguments, not answers.** Useful prompts: *"What assumptions did I miss in this architecture review?"*, *"Give me three edge cases where this Sigma rule would produce false positives"*, or *"Quiz me on how DNS resolution works, one question at a time."*
- **Verify every claim in a lab.** Run the command, inspect the log, or read the primary documentation. Never put an unverified tool flag or framework reference in a write-up or interview answer.

## Data and confidentiality boundaries

On the job—and even in home labs or bug bounties—treat public AI chat interfaces as untrusted external services unless your employer has approved a specific enterprise tool:

- Never paste employer logs, incident details, customer personal data, source code, vulnerability reports or credentials into consumer AI tools.
- Never paste embargoed vulnerability details or private bug bounty findings into third-party models.
- Check your organisation's acceptable-use policy before connecting an AI coding agent or MCP server to internal repositories, ticketing systems or cloud accounts.

## How AI is changing entry-level hiring

Routine tier-1 tasks—summarising tickets, looking up simple indicators, drafting boilerplate policies—are increasingly automated. That raises the bar slightly for entry-level candidates, but in a predictable direction: employers look less for people who can follow a rigid script and more for people who can **verify outputs, investigate edge cases, automate repeat work and explain their reasoning clearly.**

The foundations in [Foundations](foundations.md) matter more, not less, because someone has to know when the tool is wrong.

---

[← Overview](../README.md) · [All paths](../README.md#the-paths)
