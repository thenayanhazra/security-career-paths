# Identity and access management

*Last reviewed: November 2026*

> Decide who and what can access which systems, make that easy for the right people and impossible for the wrong ones, and prove it to auditors.

Identity is now the main security boundary: most attacks begin with a stolen or abused account. IAM specialists run single sign-on, multi-factor authentication, access requests and reviews, privileged access, and increasingly the identities of machines, services and AI agents.

## What the work involves

- Running identity providers and single sign-on
- Rolling out phishing-resistant authentication such as passkeys
- Designing roles and access policies
- Running joiner, mover and leaver processes, and periodic access reviews
- Managing privileged access
- Securing non-human identities: service accounts, API keys, workload identities and agents

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | IAM analyst, identity administrator | Process access requests; run reviews; support users |
| Mid | IAM engineer, identity engineer | Integrate applications; automate lifecycle; design roles |
| Senior | IAM architect, identity lead | Set identity strategy, including for machines and agents |

**Framework names:** NICE *Systems Administration*, *Systems Security Analysis*; ECSF *Cybersecurity Implementer*.

## Skills that matter

- Identity protocols: SAML, OAuth 2.0, OpenID Connect, SCIM
- Directory services, especially Active Directory and Microsoft Entra ID
- Scripting and APIs for automation
- Understanding of audit and compliance requirements for access
- Patience with people: IAM touches everyone in the organisation

## How people get in

IT administrators and service desk staff move into IAM naturally, because they already manage accounts. It is one of the most accessible technical security paths, and demand for it has grown steadily.

## Trade-offs

- **High visibility when things break:** a misconfigured SSO policy or conditional access rule locks out hundreds of people instantly, making IAM work high-stakes.
- **Unplanned ticket queues:** entry-level IAM can feel heavily operational—access requests, broken integrations and audit evidence—until you automate the lifecycle.
- **Hard human politics:** removing long-standing admin privileges or retiring shared accounts meets persistent resistance across the business.

## Learn for free

- [Microsoft Learn: Identity and Access Administrator path](https://learn.microsoft.com/en-us/credentials/certifications/identity-and-access-administrator/)
- [OAuth.net](https://oauth.net/) and [OpenID Foundation](https://openid.net/developers/how-connect-works/): the protocols explained
- [IDPro Body of Knowledge](https://bok.idpro.org/): a free, peer-reviewed reference for identity professionals
- [FIDO Alliance: passkeys](https://fidoalliance.org/passkeys/)

## Practise

- Run [Keycloak](https://github.com/keycloak/keycloak) locally in a container, connect a sample application with OpenID Connect, and enforce passkey or TOTP MFA
- Build an automated joiner-mover-leaver script against Keycloak's Admin REST API (or a free developer tenant) that assigns roles on creation and revokes active sessions on departure
- Write a short access-review script that flags dormant accounts, stale API keys and over-privileged service accounts from exported JSON or CSV data
- Trace an OAuth 2.0 authorisation code flow with PKCE in browser developer tools, and document what each token contains and how the application validates it

## Ready to apply

You are ready to interview for an IAM role when you can:

- Explain the difference between authentication and authorisation, and trace a SAML or OpenID Connect sign-in flow end to end
- Design a clean joiner-mover-leaver lifecycle using SCIM or API automation that revokes access promptly when someone leaves
- Explain why phishing-resistant MFA (passkeys / FIDO2) beats SMS or push-notification prompts
- Describe how to inventory, scope and rotate non-human identities such as service accounts, API keys and workload credentials

## Certifications

Starting: Microsoft SC-900. Building: Microsoft SC-300, Okta certifications. Advanced: CIDPRO, CISSP. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Security engineering](security-engineering-architecture.md) · [Cloud security](cloud-security.md) · [AI security engineering](ai-security-engineering.md) · [Governance, risk and compliance](governance-risk-compliance.md)

---

[← All paths](../README.md#the-paths) · [Guides](../README.md#start-here)
