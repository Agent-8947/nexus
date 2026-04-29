# DNA SIGNAL Domain Specification [NEXUS v5.0]
## Overview
The `DNA_SIGNAL` domain is dedicated to the ingestion, parsing, and advanced analysis of biological and physical signals. It primarily leverages the `python-neo` data standard and the `NeuroTechX` knowledge base.

## Active Agents
- **80_NEURAL_SIGNAL_ANALYST**: Core parsing and validation (based on Neo).
- **81_BCI_KNOWLEDGE_NAVIGATOR**: Resource mapping and recon (based on Awesome-BCI).
- **82_BCI_LSL_BRIDGE**: Real-time stream ingestion (based on Lab Streaming Layer).

## Synergies
- **SIGNAL -> AI_ML**: Cleaned Neo blocks from Agent 80 are fed into `DNA_AI_ML` for classification.
- **BCI_NAVIGATOR -> RECON**: Agent 81 identifies new dataset targets for `Master_Harvester`.
- **LSL_BRIDGE -> MOTION**: Real-time brain activity from Agent 82 can drive motion assets in `TG-FACTORY`.

## Technical Standards
- **Format**: Neo Object Model (Blocks, Segments, AnalogSignals).
- **Clock**: LSL Synchronization Protocol.
- **Units**: SI (via `quantities`).
