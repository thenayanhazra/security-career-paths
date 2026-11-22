# OT and industrial security

*Last reviewed: November 2026*

> Protect the systems that run factories, power grids, water treatment, transport and buildings, where a security failure can cause physical harm.

Operational technology (OT) and industrial control systems (ICS) follow different rules from office IT. Safety and availability come first, equipment runs for decades, and a routine scan can stop a production line. OT security specialists combine security knowledge with an understanding of industrial processes.

## What the work involves

- Building inventories of industrial assets and network connections
- Segmenting OT networks from IT and the internet
- Monitoring industrial protocols for anomalies
- Assessing risk against standards such as ISA/IEC 62443
- Working with engineers and operators on safe change and incident response
- Securing remote access for vendors and maintenance

## Roles along the way

| Level | Typical titles | What changes |
|---|---|---|
| Entry | OT security analyst, ICS security technician | Monitor; maintain inventories; support assessments |
| Mid | OT security engineer, ICS security consultant | Design segmentation; run assessments; respond to incidents |
| Senior | OT security architect, head of OT security | Set strategy across sites; manage regulatory obligations |

**Framework names:** NICE *Operational Technology (OT) Cybersecurity Engineering*, added in NICE Components v2.0.0 in March 2025; ECSF *Cybersecurity Implementer*, *Cybersecurity Architect*.

## Skills that matter

- Networking, including industrial protocols such as Modbus, DNP3 and OPC UA
- How control systems work: PLCs, HMIs, SCADA, safety systems
- The ISA/IEC 62443 series of standards
- Respect for safety culture and the people who run the plant

## How people get in

From two directions: control and automation engineers who learn security, and network or security engineers who learn industrial systems. Both are valued. Energy, utilities, manufacturing and transport are the main employers, along with specialist vendors and consultancies.

## Trade-offs

- **On-site work and travel:** factories, substations and plants cannot be secured solely from a laptop; many roles require site visits, safety gear and travel.
- **Very slow change windows:** patching may only happen during scheduled plant shutdowns once or twice a year, so you rely heavily on compensating network controls.
- **Culture gap between IT and operations:** plant operators rightly prioritise physical safety and uptime above security checklists; earning trust takes patience and humility.

## Learn for free

- [CISA ICS training](https://www.cisa.gov/resources-tools/programs/ics-training-available-through-cisa): free online courses on industrial control system security
- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final): the standard public guide to operational technology security
- [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/)
- [CISA ICS Advisories](https://www.cisa.gov/news-events/ics-advisories): current vulnerabilities affecting industrial control products
- [SANS ICS resources](https://www.sans.org/industrial-control-systems-security/): free posters, papers and webcasts

## Practise

- Run [OpenPLC](https://github.com/Autonomy-Logic/openplc-runtime) locally in a container, capture its Modbus TCP traffic in Wireshark, and observe how unauthenticated industrial commands look on the wire
- Analyse real industrial protocol captures (Modbus, DNP3, S7 and BACnet) from the [ICS-pcap](https://github.com/automayt/ICS-pcap) collection to distinguish routine polling from write commands
- Diagram an IT/OT network segmentation plan for a fictional plant using ISA/IEC 62443 zones and conduits, including audited remote access for maintenance vendors
- Map a published ICS incident to [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/) and note which detections would work passively without active scanning

## Ready to apply

You are ready to interview for an OT security role when you can:

- Explain why safety and availability outweigh confidentiality in industrial environments, and why active IT scanning can disrupt legacy PLCs
- Sketch a segmented IT/OT architecture using Purdue levels or ISA/IEC 62443 zones and conduits with controlled vendor remote access
- Read an industrial protocol capture (such as Modbus TCP) and identify unexpected write or configuration commands
- Propose practical compensating controls when an end-of-life industrial controller cannot be patched

## Certifications

Starting: Security+. Building: GIAC GICSP, ISA/IEC 62443 certificates. Advanced: GIAC GRID. See [Certifications](../guides/certifications.md).

## Neighbouring paths

[Security engineering](security-engineering-architecture.md) · [Security operations](security-operations.md) · [Incident response](incident-response-forensics.md)

---

[← All paths](../README.md#the-paths) · [Guides](../README.md#start-here)
