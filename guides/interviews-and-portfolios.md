# Interviews and portfolios

*Last reviewed: November 2026*

Most candidates who reach an interview already have similar CVs. What separates the people who get offers is clear evidence of practical work and the ability to reason aloud through unfamiliar problems. This guide covers what makes a portfolio stand out and what interviews actually test across each family of paths.

## What makes a strong portfolio

Hiring managers rarely spend more than five minutes looking at a candidate's GitHub or blog before an interview. A small number of complete, well-explained projects beats a long list of half-finished tutorials.

| Weak portfolio item | Strong portfolio item |
|---|---|
| A screenshot of completing a guided room | A short write-up explaining the vulnerability or alert, how you investigated it, and how you would detect or fix it |
| A fork of someone else's script with no notes | A small tool you wrote yourself, with a clear README, sample input/output, and known limitations |
| "Built a home lab" with no details | An architecture diagram, what telemetry you collected, one attack you simulated, and the detection rule or control change that followed |
| A generic policy copied from a template | A policy or risk assessment tailored to a realistic company, explicitly stating trade-offs and what you chose not to require |

Every project should answer three questions in its first paragraph: **what problem it solves, how you tested it, and what you would improve next.**

## Sample interview questions by family

You will rarely be asked to recite definitions from memory. Expect open-ended scenarios where the interviewer wants to see how you structure a problem, what questions you ask, and where you stop to verify assumptions.

### Defend (SOC, detection engineering, vulnerability management, DFIR, CTI)

- **Alert triage:** "A workstation ran an encoded PowerShell command at 03:00 that reached out to a newly registered domain. Walk through your first fifteen minutes."
- **Detection design:** "An alert fires 200 times a day with a 95% false-positive rate. How do you investigate and fix it without creating a blind spot?"
- **Prioritisation:** "A critical CVE with CVSS 9.8 is announced on Friday afternoon affecting 400 servers. How do you decide what gets patched tonight versus next month?"
- **Forensics and intelligence:** "How would you verify whether an attacker moved laterally from a compromised laptop, and how would you express your confidence to an executive?"

### Attack and assess (offensive security, vulnerability research)

- **Methodology:** "You are testing a web application with a login page, an API and a file upload feature. How do you plan your first day?"
- **Impact over trivia:** "You find a low-severity misconfiguration and a subtle authorisation bug. How do you explain the difference in risk to a non-technical client?"
- **Root cause:** "Pick a vulnerability class you know well (such as SSRF, IDOR or a heap overflow). Explain how it happens in code, how to exploit it and how to eliminate the class."

### Build (AppSec, cloud, security engineering, IAM, OT)

- **Threat modelling:** "A team wants to add a webhook feature that fetches user-supplied URLs and stores the response. Walk through the threats and the three controls you would ask for first."
- **Cloud and identity:** "How does a cloud provider decide whether an API call is allowed? Walk through a compromise starting from a leaked access key."
- **Trade-offs:** "Engineers say your proposed security control will double deployment time. How do you respond?"
- **OT and safety:** "Why can you not run an active vulnerability scanner across a live factory network, and what do you do instead?"

### Govern (GRC, privacy, AI governance)

- **Evidence over paper:** "A team claims they run quarterly access reviews. What evidence would you ask for to be confident the control actually works?"
- **Risk decisions:** "A critical vendor refuses to fix a medium-severity finding before a product launch. How do you frame the decision for leadership?"
- **Privacy and AI:** "A product team wants to feed customer support tickets into a third-party LLM to summarise trends. What questions do you ask before approving it?"

### AI security (AI security engineering, AI red teaming)

- **Trust boundaries:** "An internal agent reads customer emails and has permission to issue refunds. Show how indirect prompt injection could abuse it, and redesign the workflow so the model's mistake cannot cause harm."
- **Measurement:** "You changed a system prompt and tried five attacks that failed. Is that enough evidence to ship? What would you build instead?"

### Leadership

- **Prioritisation:** "You inherit a team of four and a list of twenty urgent risks. How do you build your first 90-day plan?"
- **Communication:** "Explain a major vulnerability or incident to a board in three minutes without jargon or fear-mongering."

## Handling take-home exercises and live scenarios

- **Clarify scope early.** In both live scenarios and take-home tasks, ask what assumptions you may make (company size, cloud provider, budget, regulatory context). Asking sensible questions is a positive signal.
- **Think out loud.** Interviewers cannot grade silence. State your hypothesis, what data you would check to confirm or falsify it, and what you would do next.
- **Never bluff.** Saying "I have not used that specific tool, but based on how similar tools work I would check X" is far stronger than guessing.
- **Close with the fix or decision.** Candidates often stop once they spot the flaw. Explaining the mitigation, detection or business decision is what distinguishes strong performers.

## Questions worth asking the interviewer

Interviews go both ways. Useful questions that reveal how a team actually works:

- What does a normal week look like compared with a bad week?
- What is the balance between reactive work (tickets, alerts, audits) and proactive improvement?
- How does security work with engineering or IT when there is a disagreement?
- What would someone in this role need to achieve in their first six months to be considered successful?

---

[← Overview](../README.md) · [All paths](../README.md#the-paths)
