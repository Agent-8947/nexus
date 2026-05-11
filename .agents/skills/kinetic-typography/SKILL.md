---
name: kinetic-typography
description: Advanced rules for typography in motion. Synthesized from "Transforming Type" (Barbara Brownie) and "Typemotion" (Peter Weibel).
when_to_use: kinetic typography, moving text, video text, animated titles, type in motion, readability, legibility, expressivity, text behavior
allowed-tools: Read Grep
argument-hint: [behavior or type style]
---

# Kinetic Typography: NEXUS Master Class
**Sources**: Barbara Brownie, Peter Weibel | **Version**: 2025.05

## 🌀 Text Behaviors in Motion

### 1. Fluidity vs. Rigidity
- **Fluid**: Text that deforms, flows, or morphs. Use for organic, emotional storytelling.
- **Rigid**: Text that moves as a solid block (translation, rotation). Use for structural, informative content (e.g., Solara KPI cards).

### 2. Temporal Legibility
- **Rule**: Text must remain on screen long enough to be read.
- **Formula**: `200ms + (number of words * 300ms)`. For short headers, target 1.5s - 2s minimum.

### 3. Spatial Behavior
- **Perspective**: Use 3D space to create depth. Moving text "closer" to the camera increases urgency.
- **Pathing**: Text doesn't have to move in straight lines. Use arcs for a more natural, cinematic feel.

---

## 📐 Design Rules for Moving Type

- **Contrast**: Higher contrast is required for moving type than for static type to maintain legibility.
- **Weight**: Bold and Heavy weights perform better in motion; thin serifs tend to "flicker" or disappear at high speeds.
- **Motion Blur**: Use CSS `filter: blur()` or SVG filters to simulate natural motion blur during fast movements.

---

## 🛠 Usage in NEXUS

- **/kinetic-typography** — Load all kinetic rules.
- **/kinetic-typography timing** — Load legibility formulas.
- **/kinetic-typography 3d** — Load spatial behavior rules.
