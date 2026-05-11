---
name: refactoring-ui
description: Practical, logic-driven UI design principles for building professional interfaces. Based on "Refactoring UI" by Adam Wathan & Steve Schoger.
when_to_use: UI refinement, layout, hierarchy, color selection, component design, spacing, typography, professional UI, visual polish
allowed-tools: Read Grep
argument-hint: [UI problem or component]
---

# Refactoring UI: NEXUS Edition
**Sources**: Adam Wathan & Steve Schoger | **Version**: 2024

## 📐 Core UI Logic

### 1. Hierarchy is everything
Don't just use font size to create hierarchy. Use **font weight** and **color** (e.g., using gray for secondary text instead of just smaller black text).
- **Rule**: De-emphasize secondary information rather than over-emphasizing primary information.

### 2. Spacing and Alignment
- **Limit your choices**: Don't use arbitrary spacing. Use a fixed scale (e.g., 4px, 8px, 16px, 24px, 32px, 48px, 64px).
- **Rule**: More whitespace is almost always better. If it looks "crowded", increase the padding.

### 3. Layout and Grids
- **Establish a system**: Use a 12-column grid for complex layouts, but don't be afraid to break it for specific components.
- **Rule**: Avoid "boxed" designs. Use subtle shadows or whitespace instead of heavy borders to separate content.

### 4. Color and Contrast
- **Start with Grayscale**: Design your entire UI in grayscale first to ensure the hierarchy works without color.
- **Palette**: Use a limited palette. Define one primary brand color and use variations (shades/tints) of that color.

---

## 🛠 Usage in NEXUS

- **/refactoring-ui** — Load master UI rules.
- **/refactoring-ui spacing** — Load the spacing system.
- **/refactoring-ui color** — Load the color hierarchy rules.

---

## 📁 Supporting Files
- [cheatsheet.md](cheatsheet.md) — Quick reference for UI components.
