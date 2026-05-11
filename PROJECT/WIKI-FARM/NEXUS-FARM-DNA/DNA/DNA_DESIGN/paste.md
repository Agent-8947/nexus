<!-- Source URL:  -->

![Screenshot of Paste](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F742b500d-3e10-4daa-bb89-d0d26272e5f6-1777556327756-preview-detail-poster.jpg&w=3840&q=75)

PreviewDESIGN.mdTailwind v4CSS VariablesDesign Tokens

![Screenshot of Paste](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F742b500d-3e10-4daa-bb89-d0d26272e5f6-1777556327756-preview-detail-poster.jpg&w=3840&q=75)

# Paste

![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://pasteapp.io&size=128)

Amber lantern on white marble — the brand's warm gradient logo floats in vast white space, like a single lit window in a snow-covered building.

Feels like sunlight through a minimalist gallery — vast white space with black typography and a single warm-amber focal point that draws the eye like a lantern in snow. The page is dominated by pure white (#ffffff) and near-white (#f5f5f7) surfaces with near-black (#101010) text, creating extreme contrast. system-ui at display sizes (54-80px) with tight letter-spacing (-0.013em) and weight 400-700 gives headlines a native-OS feel that reinforces the Mac-utility identity. The amber-orange gradient logo (rgb(240,100,19) → rgb(254,171,48)) is the only warm element on an otherwise monochrome canvas, making it impossibly magnetic. Blue CTA buttons (#0088ff) with 100px pill radius are the sole call to action — warm brand, cool CTA, white field.

[https://pasteapp.io](https://pasteapp.io/)

## Color Palette

Brand

Copy

Amber FlameGradientLogo, brand mark, gradient start — the warm orange anchors the entire identity as the only chromatic element on a monochrome canvas

Copy

Honey Glow#feab30Logo gradient end, warm highlight — lifts the amber into golden territory, visible in section headings and brand accents

Accent

Copy

Signal Blue#0088ffPrimary CTA buttons, interactive links — cool blue against warm-amber brand creates intentional temperature contrast that separates identity from action

Copy

Bright Blue#1c95ffHover/active state for blue CTAs, secondary interactive highlights

Neutrals

Copy

True Black#000000Maximum contrast text, nav links, icon color

Copy

Ink#101010Primary heading and body text color

Copy

Charcoal#272727Dark surface backgrounds in dark sections

Copy

Smoke#6e6e73Tertiary text, metadata, footnotes

Copy

Pewter#ababb0Secondary body text, captions, muted labels

Copy

Silver#d0d0d3Borders, decorative dividers

Copy

Mist#f0f0f0Divider backgrounds, subtle containers

Copy

Snow Gray#f5f5f7Alternating section backgrounds, subtle surface differentiation from white

Copy

Pure White#ffffffPrimary page background, card surfaces, hero sections

Semantic

Copy

Vivid Green#34c759Feature category indicator, privacy/security highlights

Copy

Electric Magenta#cb30e0Feature category indicator, collaboration highlights

Copy

Alert Red#ff383cFeature category indicator, emphasis highlights

## Typography

Type Scale

Minor Third (1.2) from 12px base

display80px · 700 · 1

The quick brown fox jumps

60px60px · 700 · 1.03

The quick brown fox jumps

heading-lg54px · 700 · 0.96

The quick brown fox jumps

heading40px · 700 · 1.05

The quick brown fox jumps

24px24px · 400 · 1.25

The quick brown fox jumps

heading-sm22px · 700 · 1.18

The quick brown fox jumps

subheading18px · 600 · 1.22

The quick brown fox jumps

body16px · 400 · 1.5

The quick brown fox jumps

Show all 11 steps

Fonts

Primarysystem-ui

Weight400, 500, 600, 700

Sizes15–80px · 9 values

Line height0.96–1.67 (tight at display sizes, relaxed at body)

Letter spacing-1.04px at 80px, -0.78px at 60px, -0.70px at 54px; positive +0.36–1.01px tracking at small sizes (15-18px) for legibility at caption scale

FallbackSF Pro Display / SF Pro Text (system default on Apple), Inter on non-Apple systems

Primary typeface for all content — headlines, body, subheadings. Using the system font stack is a deliberate choice that makes the app feel native to macOS/iOS, reinforcing the clipboard-manager-as-OS-extension identity. Weight 400 for body, 600-700 for headlines.

CaptionInter

Weight400

Sizes14px

Line height1.29

Letter spacing-0.41px at 14px — tight tracking for compact labels

FallbackInter (Google Fonts)

Used for press/media logos section labels — small metadata text where system-ui's metrics may not be optimal

## Spacing & Shape

Spacing

| Purpose | Value | Preview |
| --- | --- | --- |
| Density | comfortable |  |
| Max width | 1200px |  |
| Section gap | 80-120px |  |
| Card padding | 20-30px |  |
| Element gap | 16-20px |  |

Border Radius

| Element | Value | Preview |
| --- | --- | --- |
| cards | 16-20px |  |
| images | 16-24px |  |
| containers | 24-40px |  |
| badges | 100px |  |
| buttons | 100px |  |

Elevation

Feature Card

## Guidelines

Do

- Use 100px border-radius for ALL buttons, badges, and pill-shaped elements — this is non-negotiable and defines the visual identity
- Alternate page sections between #ffffff and #f5f5f7 backgrounds to create rhythm without visible dividers
- Set display headlines (40px+) in system-ui weight 600-700 with negative letter-spacing (-0.7px to -1.04px) — tight tracking at large sizes is essential
- Reserve the amber-orange gradient (rgb(240,100,19) → rgb(254,171,48)) for brand mark and occasional headline accents — never for backgrounds or large surfaces
- Keep all CTA buttons in #0088ff with white text — the warm brand / cool CTA temperature split is the core interaction pattern
- Use #6e6e73 or #ababb0 for secondary/body text to maintain the high-contrast headline / low-contrast body hierarchy
- Apply the soft ambient shadow (rgba(16,16,16,0.1) 0px 0px 30px) to elevated cards — never sharp directional shadows

Don't

- Never use the amber-orange gradient as a button fill — it is reserved for the logo and decorative headline accents only
- Never mix sharp-corner containers (0px radius) with the pill-radius system — minimum radius for any container is 8px, with 16-20px for cards
- Never use more than one chromatic accent color (#0088ff) in a single CTA context — the four category colors (#34c759, #cb30e0, #ff383c) are for indicators, not buttons
- Never set body text in weight 700 — reserve 700 for headlines at 40px+; body stays at 400-500
- Never add visible border lines between sections — use background color shifts (#ffffff ↔ #f5f5f7) and spacing instead
- Never use directional or hard-edged shadows — the only shadow in the system is the ambient 30px blur at 10% opacity
- Never apply positive letter-spacing to headlines — display type always uses negative tracking; positive spacing is only for small (14-18px) labels

## Component Preview

AI-generated examples showing how this design system looks when applied to real UI components.

Primary CTA Button Group

## Your clipboard,  supercharged and secure

Paste keeps everything you copy organized and searchable. Lightweight, intuitive, and private by design.

[Try for free](https://styles.refero.design/style/742b500d-3e10-4daa-bb89-d0d26272e5f6#) [View pricing](https://styles.refero.design/style/742b500d-3e10-4daa-bb89-d0d26272e5f6#)

Free 14-day trialNo credit card requiredMac, iPhone & iPad

Social Proof / Press Logos Bar

Invaluable Utility

4.5100+ RATINGS

TNW

9to5Mac

life **hacker**

Feature Cards Grid

## Do more with what  you've already done

### Unlimited History

Never lose anything you've copied. Paste stores your entire clipboard history automatically.

PRODUCTIVITY

### Private by Design

Your data stays on your device. End-to-end encrypted sync via iCloud — no third-party servers.

PRIVACY

### iCloud Sync

Seamlessly share your clipboard across Mac, iPhone, and iPad in real time.

COLLABORATION

### Instant Search

Find anything you've ever copied in seconds. Full-text search across all content types.

POWER

## More like this

[![Apple](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc9cabb96-32fa-4896-837a-f2497ce1c856-1777582724518-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://apple.com&size=128)\\
\\
**Apple** \\
\\
Gallery wall at natural light —…](https://styles.refero.design/style/c9cabb96-32fa-4896-837a-f2497ce1c856) [![Raycast](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F3b6a17f0-3bdf-418c-a95e-0b89e5a8b2f8-1777565414980-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://raycast.com&size=128)\\
\\
**Raycast** \\
\\
Obsidian command terminal — a…](https://styles.refero.design/style/3b6a17f0-3bdf-418c-a95e-0b89e5a8b2f8) [![Things](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fec0f5bca-8367-49e7-b8aa-73b3fa09a4a0-1777561673612-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://culturedcode.com&size=128)\\
\\
**Things** \\
\\
organized desktop, clean and bright](https://styles.refero.design/style/ec0f5bca-8367-49e7-b8aa-73b3fa09a4a0) [![Base44](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fe869e214-f672-4ac3-bfc2-bd25de7b003b-1777562967062-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://base44.com&size=128)\\
\\
**Base44** \\
\\
Softly Lit Gradient Canvas](https://styles.refero.design/style/e869e214-f672-4ac3-bfc2-bd25de7b003b) [![Amie](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777496407562-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://amie.so&size=128)\\
\\
**Amie** \\
\\
Sunlit productivity dashboard — a…](https://styles.refero.design/style/29567671-da1e-4f85-ae52-8b611fecc384) [![Apple](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fa48ef430-8c6a-42d8-8c53-ab7bb43cf33b-1777560879986-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://apple.com&size=128)\\
\\
**Apple** \\
\\
Precise Canvas, Vivid Product. A…](https://styles.refero.design/style/a48ef430-8c6a-42d8-8c53-ab7bb43cf33b) [![Cursor](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F4e3b4717-84c8-4599-baaf-a343c3d619b6-1777551922358-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://cursor.com&size=128)\\
\\
**Cursor** \\
\\
Warm ivory software studio.](https://styles.refero.design/style/4e3b4717-84c8-4599-baaf-a343c3d619b6) [![Moving Parts](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Ffb459c9d-c089-4d0b-b5b0-d147b1c4ebd7-1777582760806-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://movingparts.io&size=128)\\
\\
**Moving Parts** \\
\\
High-contrast geometric clarity](https://styles.refero.design/style/fb459c9d-c089-4d0b-b5b0-d147b1c4ebd7) [![mymind](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F5bfe6c1d-1b15-4f8d-b0c9-677a33291c5d-1777556900670-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://mymind.com&size=128)\\
\\
**mymind** \\
\\
Sunlit personal archive — a warm…](https://styles.refero.design/style/5bfe6c1d-1b15-4f8d-b0c9-677a33291c5d) [![Designmodo](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc60a19c1-259a-4001-95d9-6a3826f5c06e-1777567269000-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://designmodo.com&size=128)\\
\\
**Designmodo** \\
\\
Forest clearing at dawn — dark…](https://styles.refero.design/style/c60a19c1-259a-4001-95d9-6a3826f5c06e) [![Legend](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777508320444-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://legend.xyz&size=128)\\
\\
**Legend** \\
\\
Architectural blueprint on white…](https://styles.refero.design/style/63bd1ed9-b161-45fd-8734-85282bd945ec) [![Tapbots](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775926068028-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://tapbots.com&size=128)\\
\\
**Tapbots** \\
\\
Cosmic playful precision. Imagine…](https://styles.refero.design/style/8ce08850-085e-4954-a2f0-16acfb8dce23) [![21n](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775933489320-thumb.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://memotron.app&size=128)\\
\\
**21n** \\
\\
Architectural blueprint on white…](https://styles.refero.design/style/68d18deb-bb09-4258-8024-001af9c844c0) [![Apple](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fa4f123f2-cd4b-4d26-998f-a3d3ee158024-1777559561703-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://apple.com&size=128)\\
\\
**Apple** \\
\\
Polished lens on innovation —…](https://styles.refero.design/style/a4f123f2-cd4b-4d26-998f-a3d3ee158024) [![Panxo](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F8b5cfe6d-a2bd-4edb-854e-9185cec46c09-1777559925243-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://panxo.com&size=128)\\
\\
**Panxo** \\
\\
Data terminal in warm ink — every…](https://styles.refero.design/style/8b5cfe6d-a2bd-4edb-854e-9185cec46c09) [![Dia Browser](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fb458ca1a-70f0-4f85-b745-f879a4d08457-1777555664260-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://diabrowser.com&size=128)\\
\\
**Dia Browser** \\
\\
Prism on white stationery — light…](https://styles.refero.design/style/b458ca1a-70f0-4f85-b745-f879a4d08457) [![Payments](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F123a15b8-4e17-4812-83ec-899cce45db5b-1777568023664-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://lemonsqueezy.com&size=128)\\
\\
**Payments** \\
\\
Grape Soda & Lemon Zest. A bold…](https://styles.refero.design/style/123a15b8-4e17-4812-83ec-899cce45db5b) [![Linear](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F90ce5883-bb24-4466-93f7-801cd617b0d1-1777555512457-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://linear.app&size=128)\\
\\
**Linear** \\
\\
Midnight Command Center: A dark,…](https://styles.refero.design/style/90ce5883-bb24-4466-93f7-801cd617b0d1) [![Render](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc14bfde7-6f08-4b54-bd9b-39989d10cfef-1777557372319-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://render.com&size=128)\\
\\
**Render** \\
\\
Crisp canvas, gradient fireworks.…](https://styles.refero.design/style/c14bfde7-6f08-4b54-bd9b-39989d10cfef) [![Augen Pro](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F0f7da1b2-9d06-4ef5-b5a8-ef7f92e57ab2-1777582440018-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://augen.pro&size=128)\\
\\
**Augen Pro** \\
\\
Architectural Blueprint on White…](https://styles.refero.design/style/0f7da1b2-9d06-4ef5-b5a8-ef7f92e57ab2)

New

Refero MCP

## Give your AI agent real design taste

Thousands of real product screens and full user flows your coding agent can search and study before it builds.

[Get Refero MCP](https://refero.design/mcp)

![Refero MCP connects to Cursor, Claude, Windsurf and other AI coding tools](https://styles.refero.design/mcp-banner-light.png)

DESIGN.mdTailwind v4CSS VariablesDesign Tokens

CompactExtended

Copy.md

````
# Paste — Style Reference
> Amber lantern on white marble — the brand's warm gradient logo floats in vast white space, like a single lit window in a snow-covered building.

**Theme:** light

Feels like sunlight through a minimalist gallery — vast white space with black typography and a single warm-amber focal point that draws the eye like a lantern in snow. The page is dominated by pure white (#ffffff) and near-white (#f5f5f7) surfaces with near-black (#101010) text, creating extreme contrast. system-ui at display sizes (54-80px) with tight letter-spacing (-0.013em) and weight 400-700 gives headlines a native-OS feel that reinforces the Mac-utility identity. The amber-orange gradient logo (rgb(240,100,19) → rgb(254,171,48)) is the only warm element on an otherwise monochrome canvas, making it impossibly magnetic. Blue CTA buttons (#0088ff) with 100px pill radius are the sole call to action — warm brand, cool CTA, white field.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Amber Flame | `linear-gradient(0deg, rgb(240, 100, 19) -29.375%, rgb(254, 171, 48) 100%)` | `--color-amber-flame` | Logo, brand mark, gradient start — the warm orange anchors the entire identity as the only chromatic element on a monochrome canvas |
| Honey Glow | `#feab30` | `--color-honey-glow` | Logo gradient end, warm highlight — lifts the amber into golden territory, visible in section headings and brand accents |
| Signal Blue | `#0088ff` | `--color-signal-blue` | Primary CTA buttons, interactive links — cool blue against warm-amber brand creates intentional temperature contrast that separates identity from action |
| Bright Blue | `#1c95ff` | `--color-bright-blue` | Hover/active state for blue CTAs, secondary interactive highlights |
| Pure White | `#ffffff` | `--color-pure-white` | Primary page background, card surfaces, hero sections |
| Snow Gray | `#f5f5f7` | `--color-snow-gray` | Alternating section backgrounds, subtle surface differentiation from white |
| Mist | `#f0f0f0` | `--color-mist` | Divider backgrounds, subtle containers |
| Silver | `#d0d0d3` | `--color-silver` | Borders, decorative dividers |
| Pewter | `#ababb0` | `--color-pewter` | Secondary body text, captions, muted labels |
| Smoke | `#6e6e73` | `--color-smoke` | Tertiary text, metadata, footnotes |
| Charcoal | `#272727` | `--color-charcoal` | Dark surface backgrounds in dark sections |
| Ink | `#101010` | `--color-ink` | Primary heading and body text color |
| True Black | `#000000` | `--color-true-black` | Maximum contrast text, nav links, icon color |
| Vivid Green | `#34c759` | `--color-vivid-green` | Feature category indicator, privacy/security highlights |
| Electric Magenta | `#cb30e0` | `--color-electric-magenta` | Feature category indicator, collaboration highlights |
| Alert Red | `#ff383c` | `--color-alert-red` | Feature category indicator, emphasis highlights |

## Tokens — Typography

### system-ui — Primary typeface for all content — headlines, body, subheadings. Using the system font stack is a deliberate choice that makes the app feel native to macOS/iOS, reinforcing the clipboard-manager-as-OS-extension identity. Weight 400 for body, 600-700 for headlines. · `--font-system-ui`
- **Substitute:** SF Pro Display / SF Pro Text (system default on Apple), Inter on non-Apple systems
- **Weights:** 400, 500, 600, 700
- **Sizes:** 15px, 16px, 18px, 22px, 24px, 40px, 54px, 60px, 80px
- **Line height:** 0.96–1.67 (tight at display sizes, relaxed at body)
- **Letter spacing:** -1.04px at 80px, -0.78px at 60px, -0.70px at 54px; positive +0.36–1.01px tracking at small sizes (15-18px) for legibility at caption scale
- **Role:** Primary typeface for all content — headlines, body, subheadings. Using the system font stack is a deliberate choice that makes the app feel native to macOS/iOS, reinforcing the clipboard-manager-as-OS-extension identity. Weight 400 for body, 600-700 for headlines.

### Inter — Used for press/media logos section labels — small metadata text where system-ui's metrics may not be optimal · `--font-inter`
- **Substitute:** Inter (Google Fonts)
- **Weights:** 400
- **Sizes:** 14px
- **Line height:** 1.29
- **Letter spacing:** -0.41px at 14px — tight tracking for compact labels
- **Role:** Used for press/media logos section labels — small metadata text where system-ui's metrics may not be optimal

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| caption | 14px | 18 | -0.41px | `--text-caption` |
| body | 16px | 24 | — | `--text-body` |
| subheading | 18px | 24 | — | `--text-subheading` |
| heading-sm | 22px | 28 | — | `--text-heading-sm` |
| heading | 40px | 44 | -0.24px | `--text-heading` |
| heading-lg | 54px | 56 | -0.7px | `--text-heading-lg` |
| display | 80px | 80 | -1.04px | `--text-display` |

## Tokens — Spacing & Shapes

**Density:** comfortable

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 8 | 8px | `--spacing-8` |
| 10 | 10px | `--spacing-10` |
| 12 | 12px | `--spacing-12` |
| 16 | 16px | `--spacing-16` |
| 20 | 20px | `--spacing-20` |
| 24 | 24px | `--spacing-24` |
| 30 | 30px | `--spacing-30` |
| 36 | 36px | `--spacing-36` |
| 40 | 40px | `--spacing-40` |
| 50 | 50px | `--spacing-50` |
| 60 | 60px | `--spacing-60` |
| 70 | 70px | `--spacing-70` |
| 100 | 100px | `--spacing-100` |
| 140 | 140px | `--spacing-140` |

### Border Radius

| Element | Value |
|---------|-------|
| cards | 16-20px |
| badges | 100px |
| images | 16-24px |
| buttons | 100px |
| containers | 24-40px |

### Shadows

| Name | Value | Token |
|------|-------|-------|
| xl | `rgba(16, 16, 16, 0.1) 0px 0px 30px 0px` | `--shadow-xl` |

### Layout

- **Page max-width:** 1200px
- **Section gap:** 80-120px
- **Card padding:** 20-30px
- **Element gap:** 16-20px

## Components

### Primary CTA Button (Filled Pill)
**Role:** Main call-to-action across hero and sections

Background #0088ff, white text, 100px border-radius (full pill). Padding 8px 20px. system-ui weight 600, ~16px. No border. Hover state shifts to #1c95ff. The pill shape at 100px radius is a defining visual — every button is fully rounded.

### Ghost Pill Button (Outline)
**Role:** Secondary actions, alternative CTAs

Transparent background, border color matching text. 100px border-radius. Padding 10px 30px — slightly larger than filled variant. system-ui weight 500-600.

### Navigation Bar
**Role:** Top-level site navigation, sticky header

White background, horizontally centered. Logo (amber gradient icon + 'Paste' in black) on left. Nav links in #000000, system-ui weight 400-500 at ~16px. Right-aligned 'Try for free' pill button in #0088ff. Links include dropdowns (e.g. 'Use Cases ▾').

### Hero Section
**Role:** Primary landing area with product showcase

Pure white (#ffffff) background. Centered layout. Product screenshots (Mac, iPhone, iPad) composited together as hero image. Headline at 54-60px, system-ui weight 700, #101010, tight letter-spacing. Body text at 18px, weight 400, #6e6e73. CTA button below body text.

### Feature Section (Amber Headline)
**Role:** Section introduction with brand-colored headline

Background #f5f5f7 (Snow Gray). Large headline at 54-80px in the amber-orange brand gradient — this is the signature move: display-size text rendered in the brand gradient against a light gray surface. Body text in #101010 or #6e6e73.

### Feature Card
**Role:** Individual feature highlight within grid layouts

White (#ffffff) or Snow Gray (#f5f5f7) background. Border-radius 16-20px. Padding 20-30px. Shadow: rgba(16,16,16,0.1) 0px 0px 30px — soft ambient glow, not directional. Headline in system-ui weight 600, 22-24px. Body in weight 400, 16px, #6e6e73.

### Category Color Indicator
**Role:** Visual markers for feature categories (privacy, collaboration, etc.)

Four chromatic accents used as category identifiers: #0088ff (productivity), #34c759 (privacy/security), #cb30e0 (collaboration), #ff383c (power features). Applied as text color or border-color on body elements, never as backgrounds.

### Product Screenshot Container
**Role:** Device mockup display for product imagery

Product screenshots shown within device frames (MacBook, iPhone, iPad). Images have 16-24px border-radius when not in device frames. Composed in overlapping arrangements — devices overlap slightly to show ecosystem. No drop shadow on device frames themselves.

### Section Divider (Surface Shift)
**Role:** Visual separation between page sections

No visible divider lines — sections are separated by background color alternation between #ffffff and #f5f5f7 with large 80-120px vertical spacing. The transition itself IS the divider.

### Pricing CTA Block
**Role:** Conversion-focused pricing section

Contains 'Buy Now' and 'Try for Free' pill buttons. Likely centered layout with price information in system-ui weight 600-700 at heading scale. Blue filled button for primary action, ghost/outline variant for secondary.

## Do's and Don'ts

### Do
- Use 100px border-radius for ALL buttons, badges, and pill-shaped elements — this is non-negotiable and defines the visual identity
- Alternate page sections between #ffffff and #f5f5f7 backgrounds to create rhythm without visible dividers
- Set display headlines (40px+) in system-ui weight 600-700 with negative letter-spacing (-0.7px to -1.04px) — tight tracking at large sizes is essential
- Reserve the amber-orange gradient (rgb(240,100,19) → rgb(254,171,48)) for brand mark and occasional headline accents — never for backgrounds or large surfaces
- Keep all CTA buttons in #0088ff with white text — the warm brand / cool CTA temperature split is the core interaction pattern
- Use #6e6e73 or #ababb0 for secondary/body text to maintain the high-contrast headline / low-contrast body hierarchy
- Apply the soft ambient shadow (rgba(16,16,16,0.1) 0px 0px 30px) to elevated cards — never sharp directional shadows

### Don't
- Never use the amber-orange gradient as a button fill — it is reserved for the logo and decorative headline accents only
- Never mix sharp-corner containers (0px radius) with the pill-radius system — minimum radius for any container is 8px, with 16-20px for cards
- Never use more than one chromatic accent color (#0088ff) in a single CTA context — the four category colors (#34c759, #cb30e0, #ff383c) are for indicators, not buttons
- Never set body text in weight 700 — reserve 700 for headlines at 40px+; body stays at 400-500
- Never add visible border lines between sections — use background color shifts (#ffffff ↔ #f5f5f7) and spacing instead
- Never use directional or hard-edged shadows — the only shadow in the system is the ambient 30px blur at 10% opacity
- Never apply positive letter-spacing to headlines — display type always uses negative tracking; positive spacing is only for small (14-18px) labels

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Page Canvas | `#ffffff` | Primary page background |
| 1 | Section Alternate | `#f5f5f7` | Alternating section backgrounds for visual rhythm |
| 2 | Elevated Card | `#ffffff` | Cards and containers that float above Section Alternate with ambient shadow |

## Elevation

- **Feature Card:** `rgba(16, 16, 16, 0.1) 0px 0px 30px 0px`

## Imagery

Product-focused device mockups dominate — MacBook, iPhone, and iPad shown together in composed arrangements where devices overlap slightly to communicate ecosystem unity. Screenshots show the actual app UI with colorful clipboard items (photos, text snippets, maps, messages) providing visual interest against the monochrome page. No lifestyle photography, no abstract illustrations. The hero image is a composite of three device frames centered on white, establishing a 'product showcase in a gallery' feel. Press logos are displayed in muted gray. The amber-orange gradient appears only in the logo icon and as headline text color in feature sections — it's treated like a precious material used sparingly. Icon style mirrors Apple's SF Symbols: mono-weight, single-color, functional. Overall density is text-dominant with large product imagery as section anchors.

## Layout

Max-width ~1200px centered container. Hero is full-width white with centered headline, centered body text, and a composed multi-device product screenshot below. CTA button centered below body copy. Sticky navigation bar at top with logo left, links center, CTA right. Below hero: a thin press-logos bar (social proof). Sections alternate between #ffffff and #f5f5f7 backgrounds with 80-120px vertical gaps. Feature sections use large amber-gradient headlines centered, followed by explanatory content. Content is predominantly centered single-column — no sidebars, minimal multi-column grids. Section rhythm: hero → social proof → feature intro (amber headline on gray) → feature details → next feature section. The page reads as a vertical scroll with clear section breaks via background shifts.

## Agent Prompt Guide

**Quick Color Reference:**
- Text (primary): #101010
- Text (secondary): #6e6e73
- Text (muted): #ababb0
- Background (primary): #ffffff
- Background (alternate): #f5f5f7
- CTA: #0088ff
- Brand gradient: linear-gradient(0deg, rgb(240,100,19) -29%, rgb(254,171,48) 100%)

**Example Component Prompts:**

1. "Create a hero section: white (#ffffff) background. Centered headline at 54px system-ui weight 700, color #101010, letter-spacing -0.7px, line-height 56px. Body text below at 18px weight 400, color #6e6e73, line-height 24px. Blue pill CTA button (#0088ff, white text, 100px border-radius, 8px 20px padding, system-ui weight 600). 80px spacing below."

2. "Create a feature intro section: background #f5f5f7. Large headline at 60-80px with text rendered in the amber-orange gradient (linear-gradient(0deg, rgb(240,100,19), rgb(254,171,48)), -webkit-background-clip: text). system-ui weight 700, letter-spacing -1.04px. Center-aligned with 120px top/bottom padding."

3. "Create a navigation bar: white background, max-width 1200px centered. Left: amber gradient icon (20px square, 8px radius) + 'Paste' in #000000 system-ui weight 600 at 18px. Center: nav links at 16px weight 400 #000000 with 30px gap. Right: pill button 'Try for free' with #0088ff background, white text, 100px radius, 8px 20px padding."

4. "Create a feature card: white (#ffffff) background, 20px border-radius, 24px padding. Ambient shadow rgba(16,16,16,0.1) 0px 0px 30px. Headline at 22px system-ui weight 600 #101010. Body at 16px weight 400 #6e6e73, line-height 24px. 16px gap between headline and body."

5. "Create a press logos bar: centered row on white background. 5 gray (#ababb0) logo placeholders spaced 30px apart. Apple logo + '⭐ 4.5' rating badge at left. Inter 14px weight 400, letter-spacing -0.41px, color #ababb0."

## Gradient System

The amber-orange gradient (linear-gradient(0deg, rgb(240,100,19) -29.375%, rgb(254,171,48) 100%)) is the singular brand gradient. It appears in exactly two contexts: (1) the logo icon as a background fill, and (2) large display headlines via -webkit-background-clip: text to create gradient text. It is NEVER used as a section background, button fill, or decorative element. The gradient flows from deep burnt orange at the bottom to golden amber at top — when applied to text, it creates a warm metallic shimmer effect. No other gradients exist in the system.

## Category Color System

Four vivid chromatic colors are used as feature-category indicators, applied as text color or border accents on body-level elements — never as backgrounds or button fills:
- Blue (#0088ff): productivity/general features
- Green (#34c759): privacy and security features
- Magenta (#cb30e0): collaboration features
- Red (#ff383c): power/advanced features
These colors mirror Apple's SF Symbols palette, reinforcing the native-OS aesthetic. They appear at body text scale (16-18px) only.

## Similar Brands

- **Things (Cultured Code)** — Same Apple-native system-font aesthetic with monochrome canvas, single warm accent color, and device mockup hero compositions
- **Bear App** — Pill-shaped buttons, white-space-heavy layout, amber/warm brand accent against minimalist white page — nearly identical visual temperature
- **Fantastical (Flexibits)** — Mac/iOS utility positioning with product-screenshot-centric hero, system-ui typography, alternating white/gray sections
- **Raycast** — Developer productivity tool using pill CTAs, system font stack, single brand color against monochrome — though Raycast skews darker
- **Notion** — Alternating white/light-gray sections, centered single-column layout, device mockup compositions showing the actual product UI

## Quick Start

### CSS Custom Properties

```css
:root {
/* Colors */
  --color-amber-flame: #f06413;
  --gradient-amber-flame: linear-gradient(0deg, rgb(240, 100, 19) -29.375%, rgb(254, 171, 48) 100%);
  --color-honey-glow: #feab30;
  --color-signal-blue: #0088ff;
  --color-bright-blue: #1c95ff;
  --color-pure-white: #ffffff;
  --color-snow-gray: #f5f5f7;
  --color-mist: #f0f0f0;
  --color-silver: #d0d0d3;
  --color-pewter: #ababb0;
  --color-smoke: #6e6e73;
  --color-charcoal: #272727;
  --color-ink: #101010;
  --color-true-black: #000000;
  --color-vivid-green: #34c759;
  --color-electric-magenta: #cb30e0;
  --color-alert-red: #ff383c;

/* Typography — Font Families */
  --font-system-ui: 'system-ui', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-inter: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Typography — Scale */
  --text-caption: 14px;
  --leading-caption: 18;
  --tracking-caption: -0.41px;
  --text-body: 16px;
  --leading-body: 24;
  --text-subheading: 18px;
  --leading-subheading: 24;
  --text-heading-sm: 22px;
  --leading-heading-sm: 28;
  --text-heading: 40px;
  --leading-heading: 44;
  --tracking-heading: -0.24px;
  --text-heading-lg: 54px;
  --leading-heading-lg: 56;
  --tracking-heading-lg: -0.7px;
  --text-display: 80px;
  --leading-display: 80;
  --tracking-display: -1.04px;

/* Typography — Weights */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

/* Spacing */
  --spacing-4: 4px;
  --spacing-8: 8px;
  --spacing-10: 10px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-30: 30px;
  --spacing-36: 36px;
  --spacing-40: 40px;
  --spacing-50: 50px;
  --spacing-60: 60px;
  --spacing-70: 70px;
  --spacing-100: 100px;
  --spacing-140: 140px;

/* Layout */
  --page-max-width: 1200px;
  --section-gap: 80-120px;
  --card-padding: 20-30px;
  --element-gap: 16-20px;

/* Border Radius */
  --radius-lg: 8px;
  --radius-2xl: 16px;
  --radius-2xl-2: 20px;
  --radius-3xl: 24px;
  --radius-3xl-2: 30px;
  --radius-3xl-3: 40px;
  --radius-full: 100px;

/* Named Radii */
  --radius-cards: 16-20px;
  --radius-badges: 100px;
  --radius-images: 16-24px;
  --radius-buttons: 100px;
  --radius-containers: 24-40px;

/* Shadows */
  --shadow-xl: rgba(16, 16, 16, 0.1) 0px 0px 30px 0px;

/* Surfaces */
  --surface-page-canvas: #ffffff;
  --surface-section-alternate: #f5f5f7;
  --surface-elevated-card: #ffffff;
}
```

### Tailwind v4

```css
@theme {
/* Colors */
  --color-amber-flame: #f06413;
  --color-honey-glow: #feab30;
  --color-signal-blue: #0088ff;
  --color-bright-blue: #1c95ff;
  --color-pure-white: #ffffff;
  --color-snow-gray: #f5f5f7;
  --color-mist: #f0f0f0;
  --color-silver: #d0d0d3;
  --color-pewter: #ababb0;
  --color-smoke: #6e6e73;
  --color-charcoal: #272727;
  --color-ink: #101010;
  --color-true-black: #000000;
  --color-vivid-green: #34c759;
  --color-electric-magenta: #cb30e0;
  --color-alert-red: #ff383c;

/* Typography */
  --font-system-ui: 'system-ui', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-inter: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Typography — Scale */
  --text-caption: 14px;
  --leading-caption: 18;
  --tracking-caption: -0.41px;
  --text-body: 16px;
  --leading-body: 24;
  --text-subheading: 18px;
  --leading-subheading: 24;
  --text-heading-sm: 22px;
  --leading-heading-sm: 28;
  --text-heading: 40px;
  --leading-heading: 44;
  --tracking-heading: -0.24px;
  --text-heading-lg: 54px;
  --leading-heading-lg: 56;
  --tracking-heading-lg: -0.7px;
  --text-display: 80px;
  --leading-display: 80;
  --tracking-display: -1.04px;

/* Spacing */
  --spacing-4: 4px;
  --spacing-8: 8px;
  --spacing-10: 10px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-30: 30px;
  --spacing-36: 36px;
  --spacing-40: 40px;
  --spacing-50: 50px;
  --spacing-60: 60px;
  --spacing-70: 70px;
  --spacing-100: 100px;
  --spacing-140: 140px;

/* Border Radius */
  --radius-lg: 8px;
  --radius-2xl: 16px;
  --radius-2xl-2: 20px;
  --radius-3xl: 24px;
  --radius-3xl-2: 30px;
  --radius-3xl-3: 40px;
  --radius-full: 100px;

/* Shadows */
  --shadow-xl: rgba(16, 16, 16, 0.1) 0px 0px 30px 0px;
}
```
````

Paste — Refero Styles