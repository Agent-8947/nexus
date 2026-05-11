<!-- Source URL:  -->

![Screenshot of Anthropic](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fd469cba4-c448-4a43-a033-883f8bfcdc42-1777557477590-preview-detail-poster.jpg&w=3840&q=75)

PreviewDESIGN.mdTailwind v4CSS VariablesDesign Tokens

![Screenshot of Anthropic](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fd469cba4-c448-4a43-a033-883f8bfcdc42-1777557477590-preview-detail-poster.jpg&w=3840&q=75)

# Anthropic

![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://anthropic.com&size=128)

Research journal printed on warm stone — authoritative typographic composition where word-level underlines replace color as the primary emphasis mechanism, and the only warmth comes from the paper itself.

Anthropic's site runs on warm ivory parchment (#faf9f5) — not white, not gray, but the color of aged paper under good light. The palette is almost entirely achromatic, with the entire chromatic budget spent on a single earthy terracotta accent (#d97757) held in reserve in CSS tokens but largely absent from the visible UI. Two custom type families do all the personality work: Anthropic Sans drives navigation and UI at tight tracking, while Anthropic Serif delivers editorial weight in headlines and featured content — the serif-plus-grotesque pairing signals research institution, not startup. Headlines use a thick double-underline on key words (visible on 'research' and 'products') as the sole decorative device — it replaces color as the emphasis mechanism. The massive feature cards flip to near-black (#141413) background, creating hard-edged alternating surface bands with zero gradient or shadow softening.

[https://anthropic.com](https://anthropic.com/)

## Color Palette

Accent

Copy

Clay#d97757Accent CTA elements, highlight states — warm terracotta held in reserve for moments of intentional warmth against the achromatic base

Copy

Accent Ember#c6613fDeeper accent state, hover/pressed clay interactions

Copy

Olive#788c5dThematic tag or category label color variant

Copy

Sky#6a9bccThematic tag or category label color variant

Copy

Fig#c46686Thematic tag or category label color variant

Copy

Cactus#bcd1caThematic tag or category label color variant

Neutrals

Copy

Slate Dark#141413Primary text, borders, nav items, icon fills, card backgrounds — the near-black that appears on both light and dark surfaces, making it function as both foreground and background

Copy

Slate Medium#3d3d3aMid-dark borders, focus rings on light surfaces

Copy

Slate Light#5e5d59Tertiary text, captions, footer secondary content

Copy

Cloud Dark#87867fSecondary text, meta labels, timestamps

Copy

Cloud Medium#b0aea5Disabled/muted borders, secondary interactive borders, subdued UI chrome

Copy

Cloud Light#d1cfc5Dividers, hairline borders, inactive states

Copy

Oat#e3daccTertiary surface backgrounds, warm mid-tone fills

Copy

Ivory Dark#e8e6dcBody text on dark backgrounds, dividers, subtle borders

Copy

Ivory Medium#f0eee6Nav backgrounds, secondary surface level, border highlights

Copy

Ivory Light#faf9f5Page background, button fills, light surface base — the warm off-white that gives the site its parchment character instead of clinical white

## Typography

Type Scale

Major Third (1.25) from 12px base

display91px · 400 · 1.1

The quick brown fox jumps

heading-lg61px · 700 · 1.1

The quick brown fox jumps

heading24px · 600 · 1.3

The quick brown fox jumps

heading-sm20px · 400 · 1.4

The quick brown fox jumps

subheading18px · 600 · 1.4

The quick brown fox jumps

16px16px · 400 · 1

The quick brown fox jumps

body-sm15px · 400 · 1.4

The quick brown fox jumps

caption12px · 400 · 1.4

The quick brown fox jumps

Fonts

PrimaryAnthropic Sans

Weight400, 500, 600, 700

Sizes12–61px · 5 values

Line height1.00–1.40

Letter spacing-0.02em at display sizes (61px), -0.005em at mid sizes (24px), -0.002em at body sizes (15-16px)

FallbackInter, DM Sans

All UI chrome: navigation, buttons, labels, badges, footer, body copy. The custom grotesque with tight negative tracking at large sizes — at 61px with -0.02em it reads as architectural lettering, not typical web type. Used at weight 700 for the hero headline, weight 400 for body, weight 500–600 for interactive elements.

DisplayAnthropic Serif

Weight400, 600

Sizes18px, 20px, 24px, 91px

Line height1.10–1.40

Letter spacingnormal

FallbackPlayfair Display, Lora

Feature card headlines, editorial hero text, project titles. At 91px it dominates the dark feature cards — the serif at display scale against near-black reads as a printed broadsheet masthead. Weight 600 for emphasis within editorial contexts.

CodeAnthropic Mono

Weight400

Sizes16px

Line height1.40

Letter spacingnormal

FallbackJetBrains Mono, IBM Plex Mono

Technical labels, metadata fields, category tags. Appears sparingly — its presence signals 'data' or 'classification' within otherwise typographic layouts.

## Spacing & Shape

Spacing

| Purpose | Value | Preview |
| --- | --- | --- |
| Density | compact |  |
| Base unit | 4px |  |
| Max width | 1200px |  |
| Section gap | 61px |  |
| Card padding | 31px |  |
| Element gap | 8-16px |  |

Border Radius

| Element | Value | Preview |
| --- | --- | --- |
| cards | 8px |  |
| panels | 16px |  |
| featuredCards | 24px |  |

## Guidelines

Do

- Use #faf9f5 (Ivory Light) as the page base — never pure white (#ffffff) or neutral gray.
- Apply borderRadius 0px to all buttons and interactive controls except the primary 'Try Claude' CTA which uses 0px 0px 8px 8px (asymmetric: flat top, rounded bottom only).
- Emphasize headline keywords with a thick text-decoration underline only — never color, bold weight increase, or highlight backgrounds — as the sole decorative emphasis mechanism.
- Use Anthropic Serif at display sizes (91px, weight 400) exclusively within dark (#141413) surface cards; use Anthropic Sans for all light-surface headlines.
- Restrict chromatic color to the CSS accent palette (Clay #d97757, Olive #788c5d, etc.) and deploy it sparingly — one accent per section maximum; default state uses zero chromatic color.
- Set dark editorial feature cards to borderRadius 24px and keep them full content-column width with hard clipping of interior imagery at the same radius.
- Use Anthropic Mono 16px for metadata field labels (DATE, CATEGORY) in card footers — the mono/grotesque contrast signals structured data within editorial layout.

Don't

- Never use pure white (#ffffff) or pure black (#000000) as a surface background — all surfaces must come from the ivory/slate token range.
- Never add box-shadows or drop-shadows to any component — surface contrast and border lines are the only depth signals.
- Never round button corners uniformly — the 0px radius is a deliberate formal signal; avoid introducing 4px, 6px, or pill buttons.
- Never use Anthropic Serif on the page's ivory background at large sizes — the serif display scale is reserved for the dark card inversion.
- Never apply multiple chromatic accent colors within a single section — the palette tokens (Clay, Sky, Fig, Olive) are categorical variants, not combinable accents.
- Never use background fills for badge or label components — metadata labels are pure text with no chip, pill, or capsule treatment.
- Never replace the underline emphasis mechanic with color emphasis on headlines — links within headlines underline, they do not change color.

## Component Preview

AI-generated examples showing how this design system looks when applied to real UI components.

Latest Releases Card Grid

## Latest releases

Claude Opus 4.6

Introducing the world's most powerful model for coding, agents, and professional work.

[Read announcement →](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#)

DATEFebruary 5, 2026

CATEGORYProduct

Claude is a space to think

No ads. No sponsored content. Just genuinely helpful conversations.

[Read announcement →](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#)

DATEFebruary 4, 2026

CATEGORYProduct

Claude on Mars

The first AI-assisted drive on another planet. Claude helped NASA's Perseverance rover travel four hundred meters on Mars.

[Read announcement →](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#)

DATEJanuary 30, 2026

CATEGORYResearch

Feature Card (Dark Editorial)

Featured Research

Project

Glasswing

Rethinking how AI systems can be built to support human oversight and accountability for the AI era.

[Continue reading](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#)

Button Group — Primary, Ghost & Metadata Label

Primary CTA

[Try Claude](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#)

Ghost / Navigation

[Research](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#) [Commitments](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#) [Learn](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#)

Muted / Disabled

Coming soon

Text Link

[Read announcement →](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#) [Model details →](https://styles.refero.design/style/d469cba4-c448-4a43-a033-883f8bfcdc42#)

Metadata Labels

DATEFebruary 5, 2026

CATEGORYProduct

TYPEAnnouncement

## More like this

[![Together AI](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775923621441-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://together.ai&size=128)\\
\\
**Together AI** \\
\\
Shifting geometric planes under a…](https://styles.refero.design/style/461da0f0-fde6-46bc-8137-7eca006260a8) [![Aboard](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777510407125-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://aboard.com&size=128)\\
\\
**Aboard** \\
\\
Warm earth against dark steel](https://styles.refero.design/style/7b083729-e694-4b66-82a3-befb08451722) [![OpenAI](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fdc541737-8bf2-4b31-b729-0352f696e82f-1777560520281-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://openai.com&size=128)\\
\\
**OpenAI** \\
\\
Blank page before the first word —…](https://styles.refero.design/style/dc541737-8bf2-4b31-b729-0352f696e82f) [![Midjourney](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775930636038-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://midjourney.com&size=128)\\
\\
**Midjourney** \\
\\
Deep-ocean bioluminescent…](https://styles.refero.design/style/225059ac-0450-49d3-b2b7-d0e98b7ae938) [![Panxo](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F8b5cfe6d-a2bd-4edb-854e-9185cec46c09-1777559925243-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://panxo.com&size=128)\\
\\
**Panxo** \\
\\
Data terminal in warm ink — every…](https://styles.refero.design/style/8b5cfe6d-a2bd-4edb-854e-9185cec46c09) [![Claude](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F47cb86b6-cb2d-41c8-94ba-8607cd7c41cd-1777566873735-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://claude.ai&size=128)\\
\\
**Claude** \\
\\
Academic Journal on Vellum — a…](https://styles.refero.design/style/47cb86b6-cb2d-41c8-94ba-8607cd7c41cd) [![Cohere](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775923740564-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://cohere.com&size=128)\\
\\
**Cohere** \\
\\
Deep charcoal on white, with…](https://styles.refero.design/style/f1bff240-fa05-41db-9ae1-b165ea6ea2cb) [![Scale](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fe81d4724-9615-4159-8678-cef35f986cab-1777555918992-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://scale.com&size=128)\\
\\
**Scale** \\
\\
Midnight Command Center: An…](https://styles.refero.design/style/e81d4724-9615-4159-8678-cef35f986cab) [![Hume AI](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775932573314-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://hume.ai&size=128)\\
\\
**Hume AI** \\
\\
Warm pastel research lab. Soft,…](https://styles.refero.design/style/2e67105f-9f9a-45b5-9281-29734e753bd6) [![General Intelligence Company](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F34baa524-5d5b-4165-bbab-d01f05e6d6b9-1777583046194-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://generalintelligencecompany.com&size=128)\\
\\
**General Intelligence Company** \\
\\
Architectural Night Sky](https://styles.refero.design/style/34baa524-5d5b-4165-bbab-d01f05e6d6b9) [![ElevenLabs](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F031056ff-7af1-46db-8daa-115f731c5d26-1777565093172-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://elevenlabs.io&size=128)\\
\\
**ElevenLabs** \\
\\
Architect's blueprint on warm…](https://styles.refero.design/style/031056ff-7af1-46db-8daa-115f731c5d26) [![Integrated Biosciences](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777508494642-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://integratedbiosciences.com&size=128)\\
\\
**Integrated Biosciences** \\
\\
Dark Academia Laboratory: A…](https://styles.refero.design/style/80099f79-72b7-4367-b2e9-6a3d4a3e9e6a) [![Giga](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777508520866-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://giga.ai&size=128)\\
\\
**Giga** \\
\\
Deep night, mountain vista – a…](https://styles.refero.design/style/607e0dbf-e2fc-45c9-b939-946b8981c156) [![Raycast](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F3b6a17f0-3bdf-418c-a95e-0b89e5a8b2f8-1777565414980-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://raycast.com&size=128)\\
\\
**Raycast** \\
\\
Obsidian command terminal — a…](https://styles.refero.design/style/3b6a17f0-3bdf-418c-a95e-0b89e5a8b2f8) [![Inngest](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F62e8e59e-17a5-4eba-a6c6-1c7f67ded518-1777561710943-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://inngest.com&size=128)\\
\\
**Inngest** \\
\\
Midnight Grid Console — where…](https://styles.refero.design/style/62e8e59e-17a5-4eba-a6c6-1c7f67ded518) [![WRITER](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775923786277-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://writer.com&size=128)\\
\\
**WRITER** \\
\\
AI-powered clarity on a pristine…](https://styles.refero.design/style/ddd9ffaa-d831-4cb4-a5bf-a1efce421dca) [![Symbolic.ai](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777508279174-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://symbolic.ai&size=128)\\
\\
**Symbolic.ai** \\
\\
Paper-white canvas, ink-on-page UI.](https://styles.refero.design/style/694723e9-0df7-4b9f-ba07-83fc598532d6) [![Ciridae](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1776008651273-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://ciridae.com&size=128)\\
\\
**Ciridae** \\
\\
Monochrome Grid, Abstract Glow.…](https://styles.refero.design/style/a1b78a21-a304-482b-8ce5-f612d95d44fe) [![Branding](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777518442538-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://svz.io&size=128)\\
\\
**Branding** \\
\\
Midnight atelier of digital…](https://styles.refero.design/style/4d4772a3-e1da-415f-a6d7-658dcefdcecd) [![mymind](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F5bfe6c1d-1b15-4f8d-b0c9-677a33291c5d-1777556900670-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://mymind.com&size=128)\\
\\
**mymind** \\
\\
Sunlit personal archive — a warm…](https://styles.refero.design/style/5bfe6c1d-1b15-4f8d-b0c9-677a33291c5d)

DESIGN.mdTailwind v4CSS VariablesDesign Tokens

CompactExtended

Copy.md

````
# Anthropic — Style Reference
> Research journal printed on warm stone — authoritative typographic composition where word-level underlines replace color as the primary emphasis mechanism, and the only warmth comes from the paper itself.

**Theme:** light

Anthropic's site runs on warm ivory parchment (#faf9f5) — not white, not gray, but the color of aged paper under good light. The palette is almost entirely achromatic, with the entire chromatic budget spent on a single earthy terracotta accent (#d97757) held in reserve in CSS tokens but largely absent from the visible UI. Two custom type families do all the personality work: Anthropic Sans drives navigation and UI at tight tracking, while Anthropic Serif delivers editorial weight in headlines and featured content — the serif-plus-grotesque pairing signals research institution, not startup. Headlines use a thick double-underline on key words (visible on 'research' and 'products') as the sole decorative device — it replaces color as the emphasis mechanism. The massive feature cards flip to near-black (#141413) background, creating hard-edged alternating surface bands with zero gradient or shadow softening.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Slate Dark | `#141413` | `--color-slate-dark` | Primary text, borders, nav items, icon fills, card backgrounds — the near-black that appears on both light and dark surfaces, making it function as both foreground and background |
| Ivory Light | `#faf9f5` | `--color-ivory-light` | Page background, button fills, light surface base — the warm off-white that gives the site its parchment character instead of clinical white |
| Ivory Medium | `#f0eee6` | `--color-ivory-medium` | Nav backgrounds, secondary surface level, border highlights |
| Ivory Dark | `#e8e6dc` | `--color-ivory-dark` | Body text on dark backgrounds, dividers, subtle borders |
| Oat | `#e3dacc` | `--color-oat` | Tertiary surface backgrounds, warm mid-tone fills |
| Cloud Medium | `#b0aea5` | `--color-cloud-medium` | Disabled/muted borders, secondary interactive borders, subdued UI chrome |
| Cloud Light | `#d1cfc5` | `--color-cloud-light` | Dividers, hairline borders, inactive states |
| Cloud Dark | `#87867f` | `--color-cloud-dark` | Secondary text, meta labels, timestamps |
| Slate Medium | `#3d3d3a` | `--color-slate-medium` | Mid-dark borders, focus rings on light surfaces |
| Slate Light | `#5e5d59` | `--color-slate-light` | Tertiary text, captions, footer secondary content |
| Clay | `#d97757` | `--color-clay` | Accent CTA elements, highlight states — warm terracotta held in reserve for moments of intentional warmth against the achromatic base |
| Accent Ember | `#c6613f` | `--color-accent-ember` | Deeper accent state, hover/pressed clay interactions |
| Olive | `#788c5d` | `--color-olive` | Thematic tag or category label color variant |
| Sky | `#6a9bcc` | `--color-sky` | Thematic tag or category label color variant |
| Fig | `#c46686` | `--color-fig` | Thematic tag or category label color variant |
| Cactus | `#bcd1ca` | `--color-cactus` | Thematic tag or category label color variant |

## Tokens — Typography

### Anthropic Sans — All UI chrome: navigation, buttons, labels, badges, footer, body copy. The custom grotesque with tight negative tracking at large sizes — at 61px with -0.02em it reads as architectural lettering, not typical web type. Used at weight 700 for the hero headline, weight 400 for body, weight 500–600 for interactive elements. · `--font-anthropic-sans`
- **Substitute:** Inter, DM Sans
- **Weights:** 400, 500, 600, 700
- **Sizes:** 12px, 15px, 16px, 24px, 61px
- **Line height:** 1.00–1.40
- **Letter spacing:** -0.02em at display sizes (61px), -0.005em at mid sizes (24px), -0.002em at body sizes (15-16px)
- **OpenType features:** `standard`
- **Role:** All UI chrome: navigation, buttons, labels, badges, footer, body copy. The custom grotesque with tight negative tracking at large sizes — at 61px with -0.02em it reads as architectural lettering, not typical web type. Used at weight 700 for the hero headline, weight 400 for body, weight 500–600 for interactive elements.

### Anthropic Serif — Feature card headlines, editorial hero text, project titles. At 91px it dominates the dark feature cards — the serif at display scale against near-black reads as a printed broadsheet masthead. Weight 600 for emphasis within editorial contexts. · `--font-anthropic-serif`
- **Substitute:** Playfair Display, Lora
- **Weights:** 400, 600
- **Sizes:** 18px, 20px, 24px, 91px
- **Line height:** 1.10–1.40
- **Letter spacing:** normal
- **Role:** Feature card headlines, editorial hero text, project titles. At 91px it dominates the dark feature cards — the serif at display scale against near-black reads as a printed broadsheet masthead. Weight 600 for emphasis within editorial contexts.

### Anthropic Mono — Technical labels, metadata fields, category tags. Appears sparingly — its presence signals 'data' or 'classification' within otherwise typographic layouts. · `--font-anthropic-mono`
- **Substitute:** JetBrains Mono, IBM Plex Mono
- **Weights:** 400
- **Sizes:** 16px
- **Line height:** 1.40
- **Letter spacing:** normal
- **Role:** Technical labels, metadata fields, category tags. Appears sparingly — its presence signals 'data' or 'classification' within otherwise typographic layouts.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| caption | 12px | 1.3 | — | `--text-caption` |
| body-sm | 15px | 1.4 | -0.03px | `--text-body-sm` |
| subheading | 18px | 1.4 | — | `--text-subheading` |
| heading-sm | 20px | 1.4 | — | `--text-heading-sm` |
| heading | 24px | 1.3 | -0.12px | `--text-heading` |
| heading-lg | 61px | 1.1 | -1.22px | `--text-heading-lg` |
| display | 91px | 1.1 | — | `--text-display` |

## Tokens — Spacing & Shapes

**Base unit:** 4px

**Density:** compact

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 8 | 8px | `--spacing-8` |
| 12 | 12px | `--spacing-12` |
| 16 | 16px | `--spacing-16` |
| 32 | 32px | `--spacing-32` |
| 76 | 76px | `--spacing-76` |
| 84 | 84px | `--spacing-84` |

### Border Radius

| Element | Value |
|---------|-------|
| cards | 8px |
| badges | 0px |
| panels | 16px |
| buttons | 0px |
| featuredCards | 24px |

### Layout

- **Page max-width:** 1200px
- **Section gap:** 61px
- **Card padding:** 31px
- **Element gap:** 8-16px

## Components

### Primary Nav Button (Try Claude)
**Role:** Main CTA in top navigation

backgroundColor #faf9f5, color #141413, border 1px solid #141413, borderRadius 0px 0px 8px 8px (flat top, rounded bottom — a signature asymmetric radius), padding 12px 31px. Anthropic Sans weight 500, 15px. No hover shadow — border color shifts to indicate state. The asymmetric radius (flat top/rounded bottom) is a deliberate formal signature unique to this nav CTA.

### Ghost Nav Button (Transparent)
**Role:** Secondary nav actions, dropdown triggers

backgroundColor transparent, color #141413, border 1px solid #141413, borderRadius 0px, padding 22px 12px. Anthropic Sans 15px weight 400. Used for 'Commitments' and 'Learn' dropdown triggers in the nav bar.

### Muted Ghost Button
**Role:** Disabled or secondary-secondary action

backgroundColor transparent, color #b0aea5, border 1px solid #b0aea5, borderRadius 0px, no padding. Anthropic Sans 15px weight 400. Used for inactive or de-emphasized interactive elements.

### Inline Text Link with Underline Emphasis
**Role:** Hero-level keyword emphasis links

No background, color #141413, text-decoration underline with visible thick underline style (visible on 'research' and 'products' in the hero). Anthropic Sans weight 700, 61px. The underline is the sole decorative device — functions as emphasis in place of color. Only appears on selected keywords within headlines, not standard body links.

### Feature Card (Dark)
**Role:** Full-width editorial feature sections

backgroundColor #141413, borderRadius 24px, padding 31px. Anthropic Serif 91px weight 400 in #faf9f5 for the headline. Contains right-aligned 3D/abstract imagery. The dark card with serif display type creates a broadsheet editorial break within the ivory page. Full-bleed within content column.

### Release Card (Light)
**Role:** Content listing cards in the 'Latest releases' grid

backgroundColor #f0eee6 or #e3dacc, borderRadius 8px, padding 31px. Headline in Anthropic Sans weight 600, 20px, #141413. Body text Anthropic Sans weight 400, 15px, #141413. Footer metadata row with 'DATE' label in Anthropic Mono 16px. 'Read announcement →' link in Anthropic Sans 15px #141413 with arrow. No border, no shadow — card surface is the sole differentiator from page background.

### Metadata Badge / Label
**Role:** Category and date labels on cards

backgroundColor transparent, color #141413, borderRadius 0px, no padding. Anthropic Mono 16px or Anthropic Sans 12px weight 500. Zero visual chrome — pure typographic label with no pill or chip treatment. 'DATE', 'CATEGORY' appear as uppercase tracking labels above values.

### Arrow Text Link
**Role:** Read more / announcement CTAs within cards

No background, no border. Anthropic Sans 15px weight 400, color #141413. Arrow glyph '→' appended directly to text. No underline until hover. Used for 'Read announcement →', 'Read the story', 'Model details'.

### Continue Reading Button (On Dark)
**Role:** CTA within dark feature card

backgroundColor #faf9f5, color #141413, border 1px solid #141413, borderRadius 0px, padding 12px 31px. Anthropic Sans 15px weight 500. Ivory fill on dark card background — same button component as Primary Nav Button but without the asymmetric radius on dark surfaces.

### Top Navigation Bar
**Role:** Site-wide primary navigation

backgroundColor #f0eee6 or #faf9f5, position sticky, height ~68px. Left: 'ANTHROPIC\' wordmark in Anthropic Sans weight 700, 16px, #141413. Center: nav links in Anthropic Sans 15px weight 400, #141413, transparent background. Right: 'Try Claude' asymmetric-radius button. No bottom border on default state, subtle #3d3d3a border in scroll state.

## Do's and Don'ts

### Do
- Use #faf9f5 (Ivory Light) as the page base — never pure white (#ffffff) or neutral gray.
- Apply borderRadius 0px to all buttons and interactive controls except the primary 'Try Claude' CTA which uses 0px 0px 8px 8px (asymmetric: flat top, rounded bottom only).
- Emphasize headline keywords with a thick text-decoration underline only — never color, bold weight increase, or highlight backgrounds — as the sole decorative emphasis mechanism.
- Use Anthropic Serif at display sizes (91px, weight 400) exclusively within dark (#141413) surface cards; use Anthropic Sans for all light-surface headlines.
- Restrict chromatic color to the CSS accent palette (Clay #d97757, Olive #788c5d, etc.) and deploy it sparingly — one accent per section maximum; default state uses zero chromatic color.
- Set dark editorial feature cards to borderRadius 24px and keep them full content-column width with hard clipping of interior imagery at the same radius.
- Use Anthropic Mono 16px for metadata field labels (DATE, CATEGORY) in card footers — the mono/grotesque contrast signals structured data within editorial layout.

### Don't
- Never use pure white (#ffffff) or pure black (#000000) as a surface background — all surfaces must come from the ivory/slate token range.
- Never add box-shadows or drop-shadows to any component — surface contrast and border lines are the only depth signals.
- Never round button corners uniformly — the 0px radius is a deliberate formal signal; avoid introducing 4px, 6px, or pill buttons.
- Never use Anthropic Serif on the page's ivory background at large sizes — the serif display scale is reserved for the dark card inversion.
- Never apply multiple chromatic accent colors within a single section — the palette tokens (Clay, Sky, Fig, Olive) are categorical variants, not combinable accents.
- Never use background fills for badge or label components — metadata labels are pure text with no chip, pill, or capsule treatment.
- Never replace the underline emphasis mechanic with color emphasis on headlines — links within headlines underline, they do not change color.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 1 | Page Base | `#faf9f5` | Root page background, button fills, default surface |
| 2 | Nav / Elevated Light | `#f0eee6` | Navigation bar background, secondary card surfaces |
| 3 | Oat Card | `#e3dacc` | Tertiary card backgrounds, callout sections |
| 4 | Feature Dark | `#141413` | Editorial feature cards, inverted content blocks — maximum contrast against page base |

## Elevation

Zero box-shadows throughout. Surface depth is achieved entirely through background color contrast — ivory (#faf9f5) vs near-black (#141413) vs oat (#e3dacc) — with hard-edged transitions and no blurring. Cards sit flush in their grid with no lift. This flat-but-high-contrast approach reads as print design transferred to screen: depth through ink density, not light simulation.

## Imagery

Dominated by a single recurring 3D abstract graphic — a dark mesh or lattice of hexagonal/irregular cells with glowing white edges, resembling a biological cell structure or neural network under a microscope. Rendered as a high-contrast dark-field image (near-black background, luminous white wireframe lines) and placed large within the dark feature cards. This is not photography or illustration — it's a 3D scientific visualization rendered with a biological aesthetic, suggesting AI safety as a kind of material science. The image is always contained within the dark card boundary with hard-edged radius clipping (24px). Text-to-image density is high — imagery is used as a single dramatic visual accent per section, not a repeating motif. The rest of the page is entirely text-dominant with no decorative imagery, icons, or illustration.

## Layout

Max-width centered layout (~1200px) on ivory background. Hero is split-column: large weight-700 headline on left (spanning ~55% width) with a brief descriptive paragraph on right at ~30% width, both sitting on the ivory page background with generous top padding (~80px). Below the hero, full-width dark cards (borderRadius 24px) break the ivory field — left half carries Anthropic Serif display headline + CTA, right half holds the 3D visualization image. These dark editorial cards are full-column-width but not full-bleed to the browser edge. Below that, a 3-column card grid for 'Latest releases' with equal-width release cards on oat/ivory-dark backgrounds. Section gaps are ~61px. Navigation is a sticky top bar spanning full width at ~68px height. No sidebar. No mega-menu — dropdown triggers are inline in the nav with chevrons. The overall rhythm is: hero → dark editorial band → light card grid → repeat, creating a strict alternating thermal pattern.

## Agent Prompt Guide

**Quick Color Reference**
- Page background: #faf9f5 (Ivory Light)
- Primary text: #141413 (Slate Dark)
- Dark card surface: #141413
- Light card surface: #f0eee6 / #e3dacc
- Muted / disabled: #b0aea5
- Accent (use sparingly): #d97757 (Clay)
- Border default: #141413 (1px solid)

**Example Component Prompts**

1. **Hero Section:** Ivory (#faf9f5) background. Left column: headline 'AI research and products' at 61px Anthropic Sans weight 700, #141413, letter-spacing -1.22px; the words 'research' and 'products' have a thick underline text-decoration. Right column: body text 18px Anthropic Sans weight 400, #141413, max-width ~320px. No background image. 80px top padding.

2. **Dark Editorial Feature Card:** backgroundColor #141413, borderRadius 24px, padding 31px. Left: project title at 91px Anthropic Serif weight 400, #faf9f5, line-height 1.10. Subtitle at 20px Anthropic Sans weight 400, #e8e6dc. CTA button: backgroundColor #faf9f5, color #141413, border 1px solid #141413, borderRadius 0px, padding 12px 31px, Anthropic Sans 15px weight 500. Right: dark-field 3D mesh visualization image clipped to 24px radius.

3. **Release Card Grid (3-col):** Each card backgroundColor #f0eee6, borderRadius 8px, padding 31px. Headline: Anthropic Sans 20px weight 600, #141413. Body: Anthropic Sans 15px weight 400, #141413, line-height 1.40. Footer row: 'DATE' label in Anthropic Mono 16px #87867f, value #141413. Arrow link 'Read announcement →' Anthropic Sans 15px #141413. No border, no shadow.

4. **Top Navigation Bar:** backgroundColor #f0eee6, height 68px, full-width. Left: wordmark 'ANTHROPIC\' Anthropic Sans 16px weight 700 #141413. Center: nav links 15px weight 400 #141413, transparent bg, 0px radius, padding 22px 12px, 1px solid #141413 border. Right: 'Try Claude' button backgroundColor #faf9f5, border 1px solid #141413, borderRadius 0px 0px 8px 8px, padding 12px 31px, Anthropic Sans 15px weight 500.

5. **Metadata Label + Value Pair:** Label 'DATE' or 'CATEGORY' in Anthropic Mono 16px weight 400, #87867f, uppercase, no background, no border. Value below in Anthropic Sans 15px weight 400 #141413. Zero padding, zero border-radius — pure typographic structure.

## Typographic Emphasis System

Anthropic uses underline as the primary (and only) visual emphasis device. In the hero headline, key nouns ('research', 'products') receive a thick text-decoration underline — this replaces the conventional approach of using accent color or bold weight increases for emphasis. The system's near-zero chromatic color palette makes this underline-as-accent approach necessary: with no color to draw the eye, typographic decoration carries all the semantic weight. This pattern should be applied consistently: underline selected keywords in display-scale headlines, never change their color or weight. Body text uses no emphasis decorations — only display and heading-lg scales use the underline treatment.

## Surface Alternation System

Page rhythm is defined by strict light/dark alternation. Ivory (#faf9f5) page base → dark editorial cards (#141413, radius 24px) → light card grids (#f0eee6/#e3dacc, radius 8px) → repeat. Transitions are hard-edged (no gradient fade between bands). The dark cards are not full viewport-width but full content-column-width with a 24px radius creating a 'contained inversion' rather than a full-bleed band. This means the ivory background peeks around all four corners of the dark card, maintaining the sense that dark is a surface element, not a background takeover.

## Similar Brands

- **OpenAI** — Same achromatic-dominant palette with warm off-white page base and editorial serif-plus-grotesque type pairing for research content
- **DeepMind** — Research institution aesthetic with dark editorial feature blocks against a light base and zero decorative chrome
- **Are.na** — Near-zero-color palette, typographic hierarchy as sole visual structure, flat surfaces with hard edges and no shadows
- **Stripe Press** — Warm ivory background, serif at editorial scale, printed-page aesthetic applied to a digital interface
- **Substack** — Serif-grotesque pairing, text-dominant layout, light warm background with near-black type — editorial gravity over product UI

## Quick Start

### CSS Custom Properties

```css
:root {
/* Colors */
  --color-slate-dark: #141413;
  --color-ivory-light: #faf9f5;
  --color-ivory-medium: #f0eee6;
  --color-ivory-dark: #e8e6dc;
  --color-oat: #e3dacc;
  --color-cloud-medium: #b0aea5;
  --color-cloud-light: #d1cfc5;
  --color-cloud-dark: #87867f;
  --color-slate-medium: #3d3d3a;
  --color-slate-light: #5e5d59;
  --color-clay: #d97757;
  --color-accent-ember: #c6613f;
  --color-olive: #788c5d;
  --color-sky: #6a9bcc;
  --color-fig: #c46686;
  --color-cactus: #bcd1ca;

/* Typography — Font Families */
  --font-anthropic-sans: 'Anthropic Sans', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-anthropic-serif: 'Anthropic Serif', ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-anthropic-mono: 'Anthropic Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

/* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.3;
  --text-body-sm: 15px;
  --leading-body-sm: 1.4;
  --tracking-body-sm: -0.03px;
  --text-subheading: 18px;
  --leading-subheading: 1.4;
  --text-heading-sm: 20px;
  --leading-heading-sm: 1.4;
  --text-heading: 24px;
  --leading-heading: 1.3;
  --tracking-heading: -0.12px;
  --text-heading-lg: 61px;
  --leading-heading-lg: 1.1;
  --tracking-heading-lg: -1.22px;
  --text-display: 91px;
  --leading-display: 1.1;

/* Typography — Weights */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

/* Spacing */
  --spacing-unit: 4px;
  --spacing-4: 4px;
  --spacing-8: 8px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-32: 32px;
  --spacing-76: 76px;
  --spacing-84: 84px;

/* Layout */
  --page-max-width: 1200px;
  --section-gap: 61px;
  --card-padding: 31px;
  --element-gap: 8-16px;

/* Border Radius */
  --radius-lg: 8px;
  --radius-2xl: 16px;
  --radius-3xl: 24px;

/* Named Radii */
  --radius-cards: 8px;
  --radius-badges: 0px;
  --radius-panels: 16px;
  --radius-buttons: 0px;
  --radius-featuredcards: 24px;

/* Surfaces */
  --surface-page-base: #faf9f5;
  --surface-nav-elevated-light: #f0eee6;
  --surface-oat-card: #e3dacc;
  --surface-feature-dark: #141413;
}
```

### Tailwind v4

```css
@theme {
/* Colors */
  --color-slate-dark: #141413;
  --color-ivory-light: #faf9f5;
  --color-ivory-medium: #f0eee6;
  --color-ivory-dark: #e8e6dc;
  --color-oat: #e3dacc;
  --color-cloud-medium: #b0aea5;
  --color-cloud-light: #d1cfc5;
  --color-cloud-dark: #87867f;
  --color-slate-medium: #3d3d3a;
  --color-slate-light: #5e5d59;
  --color-clay: #d97757;
  --color-accent-ember: #c6613f;
  --color-olive: #788c5d;
  --color-sky: #6a9bcc;
  --color-fig: #c46686;
  --color-cactus: #bcd1ca;

/* Typography */
  --font-anthropic-sans: 'Anthropic Sans', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-anthropic-serif: 'Anthropic Serif', ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-anthropic-mono: 'Anthropic Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

/* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.3;
  --text-body-sm: 15px;
  --leading-body-sm: 1.4;
  --tracking-body-sm: -0.03px;
  --text-subheading: 18px;
  --leading-subheading: 1.4;
  --text-heading-sm: 20px;
  --leading-heading-sm: 1.4;
  --text-heading: 24px;
  --leading-heading: 1.3;
  --tracking-heading: -0.12px;
  --text-heading-lg: 61px;
  --leading-heading-lg: 1.1;
  --tracking-heading-lg: -1.22px;
  --text-display: 91px;
  --leading-display: 1.1;

/* Spacing */
  --spacing-4: 4px;
  --spacing-8: 8px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-32: 32px;
  --spacing-76: 76px;
  --spacing-84: 84px;

/* Border Radius */
  --radius-lg: 8px;
  --radius-2xl: 16px;
  --radius-3xl: 24px;
}
```
````

Anthropic — Refero Styles