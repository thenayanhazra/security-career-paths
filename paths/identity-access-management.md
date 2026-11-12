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

## Learn for free

- [Microsoft Learn: Identity and Access Administrator path](https://learn.microsoft.com/en-us/credentials/certifications/identity-and-access-administrator/)
- [OAuth.net](https://oauth.net/) and [OpenID Foundation](https://openid.net/developers/how-connect-works/): the protocols explained
- [IDPro Body of Knowledge](https://bok.idpro.org/): a free, peer-reviewed reference for identity professionals
- [FIDO Alliance: passkeys](https://fidoalliance.org/passkeys/)

## Practise

- Set up a free developer tenant with an identity provider, connect a sample application with OpenID Connect, and enforce MFA
- Build an automated joiner-mover-leaver flow with a script and an API

## Certifications

Starting: Microsoft SC-900. Building: Microsoft SC-300, Okta certifications. Advanced: CIDPRO, CISSP. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Security engineering](security-engineering-architecture.md) · [Cloud security](cloud-security.md) · [Governance, risk and compliance](governance-risk-compliance.md)
