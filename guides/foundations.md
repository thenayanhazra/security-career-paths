# Foundations

*Last reviewed: November 2026*

Every security path rests on the same base: how computers, networks and software work, plus the core ideas of security itself. You do not need to master all of it before your first role, but gaps here show up quickly in interviews and on the job.

## What to learn

| Area | Enough to start | Free resources |
|---|---|---|
| **Networking** | The OSI and TCP/IP models; IP addressing and subnets; DNS, HTTP, TLS; what a firewall and a proxy do; reading a packet capture | [Professor Messer's Network+ course](https://www.professormesser.com/network-plus/n10-009/n10-009-video/n10-009-training-course/); [Wireshark sample captures](https://wiki.wireshark.org/SampleCaptures) |
| **Operating systems** | Linux command line, permissions, processes, services and logs; Windows users, groups, the registry, event logs and Active Directory basics | [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/); [Microsoft Learn](https://learn.microsoft.com/en-us/training/) |
| **Scripting** | Enough Python or PowerShell to parse a log file, call an API and automate a repetitive task | [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/) |
| **Web and APIs** | How a request becomes a response; cookies and sessions; authentication; REST and JSON | [MDN Web Docs: HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) |
| **Cloud** | What IaaS, PaaS and SaaS mean; identities and permissions in one major cloud; the shared responsibility model | [AWS Skill Builder](https://skillbuilder.aws/), [Microsoft Learn](https://learn.microsoft.com/en-us/training/) |
| **Security concepts** | Confidentiality, integrity and availability; authentication versus authorisation; least privilege; defence in depth; common attack types; risk | [Professor Messer's Security+ course](https://www.professormesser.com/security-plus/sy0-701/sy0-701-video/sy0-701-comptia-security-plus-course/) |
| **How attacks unfold** | The stages of an intrusion and the common techniques at each | [MITRE ATT&CK](https://attack.mitre.org/) |

## A sensible order

1. **Weeks 1–6: networking and Linux.** These underpin everything. Do the Bandit wargame alongside a networking course.
2. **Weeks 7–10: Windows and Active Directory.** Most corporate breaches involve them.
3. **Weeks 11–14: security concepts.** Work through a Security+-level course, whether or not you sit the exam.
4. **Throughout: scripting.** Automate something small every week.
5. **Then:** pick a path and go deeper using its page.

These timings assume a few hours of study a week alongside other commitments. Faster is possible; slower is fine.

## Build a home lab

A home lab is the single best way to turn reading into skill, and it costs little or nothing.

- Run a few virtual machines on your own computer with free hypervisors such as VirtualBox, or use free cloud tiers.
- Set up a small Windows domain, a Linux server and a logging tool, then attack and defend it.
- Write down what you did. Those notes become blog posts, and blog posts become evidence for employers.

## Where to go next

Return to the [path overview](../README.md#the-paths), or read [how to choose a path](choosing-a-path.md).
