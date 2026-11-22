# Cloud security

*Last reviewed: November 2026*

> Secure the platforms and workloads organisations run on AWS, Azure, Google Cloud and Kubernetes.

Most new systems run in the cloud, and most cloud breaches come from misconfiguration and over-broad permissions rather than clever exploits. Cloud security engineers design secure account structures, write guardrails as code, review architectures, and find and fix risky configurations before attackers do.

## What the work involves

- Designing identity and permission models in one or more clouds
- Writing guardrails and policies as code, and building secure templates teams can reuse
- Running cloud security posture management and fixing what it finds
- Reviewing architectures for new services
- Securing containers and Kubernetes
- Detection and response for cloud environments

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | Cloud security analyst, junior cloud security engineer | Triage posture findings; fix misconfigurations |
| Mid | Cloud security engineer, platform security engineer | Build guardrails; design account structure; review architectures |
| Senior | Senior/principal cloud security engineer, cloud security architect | Set cloud security strategy across the organisation |

**Framework names:** NICE *Cybersecurity Architecture*, *Systems Security Analysis*; ECSF *Cybersecurity Architect*, *Cybersecurity Implementer*.

## Skills that matter

- Deep knowledge of one cloud provider, working knowledge of another
- Identity and access management in the cloud: roles, policies, federation
- Infrastructure as code such as Terraform
- Containers and Kubernetes
- Networking in cloud environments
- Scripting and automation

## How people get in

The most common route is from cloud, DevOps or platform engineering: you already know how the systems are built. Security operations analysts who specialise in cloud logs are another source.

## Learn for free

- [AWS Skill Builder](https://skillbuilder.aws/), [Microsoft Learn](https://learn.microsoft.com/en-us/training/) and [Google Cloud Skills Boost](https://www.cloudskillsboost.google/)
- [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/framework/security.html): cloud security design principles that carry across providers
- [CSA Security Guidance](https://cloudsecurityalliance.org/research/guidance): the body of knowledge behind the CCSK
- [Kubernetes security documentation](https://kubernetes.io/docs/concepts/security/)
- [Hacking the Cloud](https://hackingthe.cloud/): an encyclopaedia of cloud attack techniques

## Practise

- [Pwned Labs](https://pwnedlabs.io/) (free tier) and [flaws.cloud](http://flaws.cloud/) / [flaws2.cloud](http://flaws2.cloud/) for realistic cloud attack and defence scenarios
- [CloudGoat](https://github.com/RhinoSecurityLabs/cloudgoat) in your own AWS account, with a budget alert set first
- [Kubernetes Goat](https://github.com/madhuakula/kubernetes-goat) locally to practise finding and fixing common container and cluster misconfigurations
- [Stratus Red Team](https://github.com/DataDog/stratus-red-team) to detonate individual cloud attack techniques across AWS, Azure, Google Cloud or Kubernetes in a disposable test account, then verify whether your audit logs catch them
- Build a multi-account AWS or Azure landing zone in Terraform with identity boundaries, centralised logging and policy-as-code guardrails, and publish it

## Certifications

Starting: a cloud provider's foundational certification. Building: CCSK, AWS Certified Security – Specialty, Microsoft AZ-500, Google Professional Cloud Security Engineer. Advanced: CCSP, GIAC GCLD or GPCS. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Security engineering](security-engineering-architecture.md) · [Identity and access management](identity-access-management.md) · [Application security](application-security.md) · [Security operations](security-operations.md) · [Vulnerability management](vulnerability-management.md) · [AI security engineering](ai-security-engineering.md)

---

[← All paths](../README.md#the-paths) · [Guides](../README.md#start-here)
