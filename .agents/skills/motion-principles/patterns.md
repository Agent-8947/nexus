# UI Motion Patterns: Motion Principles

## 🌊 The Sequential Reveal (Stagger)
**When to use**: Lists, cards, or text modules.
**How**: 
```javascript
gsap.from(".card", {
  y: 30,
  opacity: 0,
  duration: 0.8,
  stagger: 0.1,
  ease: "power2.out"
});
```
**Goal**: Create a sense of flow and orientation.

## 🧭 The Directional Transition
**When to use**: Switching screens or slides (e.g. Solara C015).
**How**: Move elements in the direction of the interaction (e.g. Next Slide -> Move elements Left).
**Logic**: reinforces the spatial mental model of the interface.

## 📈 The Stat Count (Hardcoded Fallback)
**When to use**: KPI numbers.
**V5 Rule**: Avoid jittery counters. Use a simple fade-in or a quick (200ms) blur-to-focus transition on the final hardcoded value.
**GSAP**: 
```javascript
gsap.from("#stat", {
  filter: "blur(10px)",
  opacity: 0,
  duration: 0.3
});
```

## 🤏 The Micro-Interaction (Hover)
**When to use**: Buttons, links.
**How**: Subtle scale (1.05) and opacity shift.
**Timing**: Extremely fast (<100ms) to ensure responsiveness.
