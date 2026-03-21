# Skill: OSINT-Tactician (Methodology & Forensics)

**OSINT Framework & Evidence Handling**
*Structured methodology based on the Intelligence Cycle and Hunchly principles.*

## Description
This skill provides a structured framework for conducting OSINT investigations within NEXUS. It combines the **Intelligence Cycle** (Direction, Collection, Processing, Analysis, Dissemination) with **Forensic Evidence Preservation** principles (inspired by Hunchly).

## Capabilities
1.  **Investigation Planning**: Create a structured investigation plan based on target criteria (Email, Domain, Person).
2.  **Evidence Logging**: Guidelines and tools for preserving digital evidence with timestamps and source metadata.
3.  **Methodology Flow**: Step-by-step workflows for:
    *   Corporate Reconnaissance
    *   People Discovery
    *   Infrastructure Mapping (DNS/IP/SSL)
4.  **Dark Web Recon**: Integration with OnionScan logic (via `hunchly-integrator/source/onionscan`).

## Core Methodology: The OSINT Cycle
1.  **Direction**: Define the investigation goals and legal boundaries.
2.  **Collection**: Gathering raw data from search engines, social media, and technical tools.
3.  **Processing**: Organizing raw data (e.g., converting names to emails, mapping domains to IPs).
4.  **Analysis**: Finding patterns, red flags, and connections.
5.  **Reporting**: Creating the final Dossier/Intelligence Report.

## Tools (Included)
- **`domain-intel`**: Technical reconnaissance.
- **`firecrawl`**: Automated data collection.
- **`INTEL-SIGHT`**: Orchestration engine.
- **`hunchly-integrator`**: Evidence preservation logic.

## Usage Guide
When starting a new case:
1.  Initialize a case directory in `PROJECT/INTEL-SIGHT/Cases/<CaseID>/`.
2.  Apply the **Direction** template to define what you are looking for.
3.  Use the **Collection** phase tools to gather data.
4.  Generate an **Intelligence Report** using the `generate_doc.py` script.
