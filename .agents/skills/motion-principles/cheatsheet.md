# Cheatsheet: GSAP & Motion Rules

## 📉 GSAP Core Timings
- **Snap**: 0.2s (Fast, responsive)
- **Smooth**: 0.5s - 0.8s (Cinematic)
- **Stagger**: 0.05s - 0.1s (Rhythmic)

## 🎚 Easing Presets
- `ease: "none"` — Linear (Constant speed)
- `ease: "power2.out"` — Arrival (Slowing down)
- `ease: "power2.in"` — Departure (Speeding up)
- `ease: "expo.inOut"` — High impact (Sharp acceleration/deceleration)
- `ease: "back.out(1.7)"` — Overshoot (Bounce effect)

## 📐 Properties to Animate
- **Transform**: `x`, `y`, `z`, `rotation`, `scale`.
- **Filters**: `blur()`, `brightness()`.
- **Opacity**: `autoAlpha` (GSAP specific: combines opacity and visibility).

## 🚫 Motion Anti-Patterns
1. **Never** animate properties that cause layout reflow (`width`, `height`, `top`, `left`). Use `scale`, `x`, `y` instead.
2. **Avoid** too many simultaneous animations (causes cognitive overload).
3. **Avoid** duration > 1.2s for UI elements unless it's a slow cinematic reveal.
