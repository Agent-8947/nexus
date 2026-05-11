<!-- Source URL:  -->

![Screenshot of JetBrains](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fbc4fb98b-37ec-480a-b7a9-acd197cbebb9-1777559539194-preview-detail-poster.jpg&w=3840&q=75)

PreviewDESIGN.mdTailwind v4CSS VariablesDesign Tokens

![Screenshot of JetBrains](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fbc4fb98b-37ec-480a-b7a9-acd197cbebb9-1777559539194-preview-detail-poster.jpg&w=3840&q=75)

# JetBrains

![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://jetbrains.com&size=128)

Neon nebula on obsidian — a black-ground page where violet-blue gradients bloom upward like deep-space imagery, punctuated by hot-pink neon and per-product chromatic icon light.

JetBrains' site feels like the interior of a deep-space control room — pure black (#000000) ground plane with electric violet-to-blue gradients erupting from the darkness like bioluminescent nebulae. The defining moves are the chromatic product icon ecosystem (each IDE gets a vivid multicolor badge) floating against near-black surfaces, and the blue radial glow (rgba(0,71,253,0.8) at 75% opacity) diffused behind hero content like a spotlight on a dark stage. Headlines at 72-79px use JetBrains Sans weight 600 with tight letter-spacing, while the hot-pink accent (#f31199, CSS var --main-page-pink) fires only on category labels and brand moments — a neon sign in a dark corridor. Cards use 24px radius with translucent violet or pink fills (rgba(90,31,208,0.3), rgba(243,17,180,0.2)) that glow rather than separate.

[https://jetbrains.com](https://jetbrains.com/)

## Color Palette

Brand

Copy

Electric Blue#18a3faPrimary link color, info badges, active state highlights — the most-used chromatic color site-wide, giving the dark UI its cool electric temperature

Copy

Violet Pulse#7b61ffButton borders, badge backgrounds, primary CTA outlines — the core violet brand hue from the JetBrains logo

Copy

Iris#6b57ffBadge fills, body accent — slightly darker violet variant for surfaces needing more saturation

Copy

Amethyst#8473ffHeading accent color, primary dark-theme color token (--rs-color-primary-dark-theme)

Copy

Deep Violet#2e106aCTA button background — deep space purple that pairs with Electric Blue (#18a3fa) text for a neon-on-void feel

Accent

Copy

Neon Pink#f31199Category labels ('For businesses', 'For developers'), brand highlight moments — the signature hot-pink neon that fires sparingly against black like a neon sign (--main-page-pink)

Copy

Magenta Glow#5a1fd0Gradient start color for violet nebula gradient, card border accents

Copy

Nebula VioletGradientHero gradient bloom origin

Copy

Aurora TealGradientSection accent headings, icon fills, gradient stop — teal-to-blue gradient used on feature callouts

Copy

Hero Blue GlowGradientRadial glow behind hero content — the deep blue spotlight effect that dominates the first viewport

Neutrals

Copy

Obsidian Ground#000000Page background — the absolute black base all gradients and glows emerge from

Copy

Deep Charcoal#19191cNav bar background, footer, elevated surface one step above absolute black

Copy

Graphite#343434Most-used color on site; borders, dividers, muted icon strokes, body text secondary contexts

Copy

Iron#474749Subtle borders, inactive state outlines

Copy

Ash#757577Card borders, inactive dividers

Copy

Slate#8c8c8Secondary body text, muted icon fills

Copy

Silver#a3a3a4Tertiary icons, ghost button labels, disabled states

Copy

Fog#bababbBody text on dark backgrounds, list items, secondary link labels

Copy

Pure White#ffffffPrimary headings, button labels on dark, high-emphasis body text

Semantic

Copy

Danger Red#f45c4aError states, destructive actions (--rs-color-danger)

Copy

Success Green#4dbb5fSuccess states (--rs-color-success)

Copy

Warning Amber#f3c033Warning states (--rs-color-warning)

## Typography

Type Scale

Minor Third (1.2) from 15px base

display79px · 500 · 0.9

The quick brown fox jumps

heading-lg72px · 600 · 1

The quick brown fox jumps

heading43px · 600 · 1.14

The quick brown fox jumps

heading-sm35px · 600 · 1.2

The quick brown fox jumps

subheading29px · 300 · 1.34

The quick brown fox jumps

body20px · 400 · 1.4

The quick brown fox jumps

body-sm16px · 400 · 1

The quick brown fox jumps

caption13px · 400 · 1.54

The quick brown fox jumps

Fonts

CodeJetBrains Sans

Weight300, 400, 500, 600

Sizes13–79px · 8 values

Line height0.90–1.54 (tighter at larger sizes: 0.90 at display, 1.50–1.54 at body)

Letter spacing-0.4–0.065px · 7 values

FallbackInter, Plus Jakarta Sans

The single typeface for the entire site at all sizes and weights. 600 at 72-79px for hero headlines — unusual that even at this weight the custom letterSpacing tightening (-0.005em to -0.001em) keeps the large type dense and technical rather than editorial. Weight 300 appears at mid-sizes giving subheadings a lighter counterpoint to bold display text. JetBrains Sans is custom-designed — it carries optical metrics tuned for code-adjacent contexts, slightly wider than Inter at body sizes, with liga/calt features active that echo the IDE typographic environment.

## Spacing & Shape

Spacing

| Purpose | Value | Preview |
| --- | --- | --- |
| Density | comfortable |  |
| Base unit | 8px |  |
| Max width | 1280px |  |
| Section gap | 80-120px |  |
| Card padding | 24px |  |
| Element gap | 8-16px |  |

Border Radius

| Element | Value | Preview |
| --- | --- | --- |
| badges | 4-6px |  |
| images | 16px |  |
| buttons | 20-26px |  |
| cards | 24px |  |
| modals | 24px |  |

## Guidelines

Do

- Use #000000 as the absolute page background — never a near-black like #0a0a0a or #111; the true black is what makes the gradient glows feel luminous
- Apply the radial blue glow (rgba(0,71,253,0.8) → transparent) behind hero content at ~87% width spread, centered on the content, so text appears spotlit from behind
- Use Neon Pink (#f31199) only for category labels and brand punctuation — 1-3 instances per page maximum; it reads as a signal color, not a fill color
- Set all card and feature panel border-radius to 24px; use 4px only for badges, never mix these on the same component
- Use translucent fills for card backgrounds: rgba(90,31,208,0.3) for violet-tinted cards, rgba(243,17,180,0.2) for pink-tinted cards — never opaque colored fills
- Apply JetBrains Sans with fontFeatureSettings '"calt", "kern", "liga"' active at all sizes, and apply negative letter-spacing (-0.005em) at display sizes 43px and above
- Give each JetBrains product its own distinct multicolor icon — the chromatic icon grid is the primary visual diversity mechanism; do not apply a single brand color to all icons

Don't

- Do not use #18a3fa (Electric Blue) as a fill color for buttons or large surfaces — it is a text/border/link color only; as a fill it would overpower the dark palette
- Do not add box-shadows to cards — elevation is expressed through gradient fills and translucent backgrounds, never drop shadows
- Do not use border-radius below 16px on interactive elements (buttons, cards); sharp-cornered shapes are reserved exclusively for badges (4-6px)
- Do not place white text directly on the pure black background without a gradient zone or translucent card beneath for longer body text — use #bababb for body on raw black
- Do not use Neon Pink (#f31199) as a background fill for large areas — its opacity 0.2 translucent form (rgba(243,17,180,0.2)) is the maximum surface application
- Do not add a visible border-bottom to the navigation bar — the #19191c header transitions into the hero gradient without a line
- Do not apply uniform icon color — product icons must retain their individual per-product chromatic gradient identity; monochromatic treatment breaks the identity system

## Component Preview

AI-generated examples showing how this design system looks when applied to real UI components.

Audience Segmentation Tab Row + Business Feature Card

For developersFor teamsFor businesses

Forbusinesses

## Empower your team  and succeed as a business

### Professional AI Coding.  Better Results.

Improve your developer team's productivity, satisfaction, and ROI with established AI-powered IDEs.

Explore Business Solutions

Feature Announcement Card with IDE Grid

## JetBrains IDEs 2026.1

Now Live

An open agentic platform (Junie, Claude, and Codex built in; Cursor, GitHub Copilot, and more via the ACP Registry). Deeper code insight and analysis across IDEs.

IntelliJ IDEA

PhpStorm

RustRover

DataGrip

PyCharm

WebStorm

GoLand

Rider

CLion

1 / 2

Button Group — Primary, Violet Deep, and Ghost

Button Styles

Primary — Hero CTA

Choose Your IDEFor Business

Licenses for your organization

Violet Deep — Feature Card CTA

Explore All IDEs

Status Badges

Now LiveFeatured2026.1Free for non-commercial use

Ghost Nav — Borderless

[Products](https://styles.refero.design/style/bc4fb98b-37ec-480a-b7a9-acd197cbebb9#) [Education](https://styles.refero.design/style/bc4fb98b-37ec-480a-b7a9-acd197cbebb9#) [Solutions](https://styles.refero.design/style/bc4fb98b-37ec-480a-b7a9-acd197cbebb9#) [Support](https://styles.refero.design/style/bc4fb98b-37ec-480a-b7a9-acd197cbebb9#) [Store](https://styles.refero.design/style/bc4fb98b-37ec-480a-b7a9-acd197cbebb9#)

## More like this

[![Bun](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F408a149c-702f-4442-99df-bea49d9c0d9b-1777567430937-preview-poster.jpg&w=3840&q=75)\\
\\
**Bun** \\
\\
Synthwave dark lab – precision…](https://styles.refero.design/style/408a149c-702f-4442-99df-bea49d9c0d9b) [![Raycast](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F3b6a17f0-3bdf-418c-a95e-0b89e5a8b2f8-1777565414980-preview-poster.jpg&w=3840&q=75)\\
\\
**Raycast** \\
\\
Obsidian command terminal — a…](https://styles.refero.design/style/3b6a17f0-3bdf-418c-a95e-0b89e5a8b2f8) [![Astro](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775923401594-thumb.jpg&w=3840&q=75)\\
\\
**Astro** \\
\\
Deep-space console light show.…](https://styles.refero.design/style/e8c604cc-1c8d-42a3-aeca-fcfc25e70344) [![GitHub](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc3ceca5c-d329-4559-b947-016172941ba2-1777557298416-preview-poster.jpg&w=3840&q=75)\\
\\
**GitHub** \\
\\
Midnight command center, subtly…](https://styles.refero.design/style/c3ceca5c-d329-4559-b947-016172941ba2) [![Wonder](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc81d2be0-05b7-4755-8046-f2d19fbc448c-1777581481411-preview-poster.jpg&w=3840&q=75)\\
\\
![](https://ysxnuuuj3kqhdyj2.public.blob.vercel-storage.com/1777595159441-icon.png)\\
\\
**Wonder** \\
\\
Deep canvas, fuchsia accent](https://styles.refero.design/style/c81d2be0-05b7-4755-8046-f2d19fbc448c) [![Midjourney](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775930636038-thumb.jpg&w=3840&q=75)\\
\\
**Midjourney** \\
\\
Deep-ocean bioluminescent…](https://styles.refero.design/style/225059ac-0450-49d3-b2b7-d0e98b7ae938) [![Neon](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fcc38369a-41e3-4bcd-b619-230ccffe7e8e-1777560319277-preview-poster.jpg&w=3840&q=75)\\
\\
**Neon** \\
\\
Server Room After Dark. A deep…](https://styles.refero.design/style/cc38369a-41e3-4bcd-b619-230ccffe7e8e) [![Promly](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777519002768-thumb.jpg&w=3840&q=75)\\
\\
**Promly** \\
\\
Midnight gradient with neon…](https://styles.refero.design/style/9117a4f5-6171-44ad-aa85-a387a5d80620) [![Trigger.dev](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775923436132-thumb.jpg&w=3840&q=75)\\
\\
**Trigger.dev** \\
\\
Midnight Terminal, illuminated by…](https://styles.refero.design/style/86541d12-7870-4d51-8c47-0880fdb1ea01) [![LaunchDarkly](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777518225326-thumb.jpg&w=3840&q=75)\\
\\
**LaunchDarkly** \\
\\
Midnight Terminal, Violet Haze](https://styles.refero.design/style/18a75348-513a-49d8-94f5-e2df8c118b6b) [![Linear](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F90ce5883-bb24-4466-93f7-801cd617b0d1-1777555512457-preview-poster.jpg&w=3840&q=75)\\
\\
**Linear** \\
\\
Midnight Command Center: A dark,…](https://styles.refero.design/style/90ce5883-bb24-4466-93f7-801cd617b0d1) [![Antimetal](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F9f9a4a4f-1a27-47ca-a65b-68b9850a84e4-1777561558774-preview-poster.jpg&w=3840&q=75)\\
\\
**Antimetal** \\
\\
Electric storm over a blueprint —…](https://styles.refero.design/style/9f9a4a4f-1a27-47ca-a65b-68b9850a84e4) [![Inngest](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F62e8e59e-17a5-4eba-a6c6-1c7f67ded518-1777561710943-preview-poster.jpg&w=3840&q=75)\\
\\
**Inngest** \\
\\
Midnight Grid Console — where…](https://styles.refero.design/style/62e8e59e-17a5-4eba-a6c6-1c7f67ded518) [![FlutterFlow](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775932467436-thumb.jpg&w=3840&q=75)\\
\\
**FlutterFlow** \\
\\
Deep Space Command Center.…](https://styles.refero.design/style/4e1ac04c-02ae-41cf-b588-3f6226a882f8) [![Resend](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F0d914ef0-fa84-4c60-a9aa-cef0b5eb6e5d-1777557430073-preview-poster.jpg&w=3840&q=75)\\
\\
**Resend** \\
\\
Obsidian developer terminal —…](https://styles.refero.design/style/0d914ef0-fa84-4c60-a9aa-cef0b5eb6e5d) [![N8n](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F8601c8ef-e1ea-4186-adb2-6f9a74caf436-1777556028960-preview-poster.jpg&w=3840&q=75)\\
\\
**N8n** \\
\\
Workflow engine at midnight — the…](https://styles.refero.design/style/8601c8ef-e1ea-4186-adb2-6f9a74caf436) [![Aboard](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777510407125-thumb.jpg&w=3840&q=75)\\
\\
**Aboard** \\
\\
Warm earth against dark steel](https://styles.refero.design/style/7b083729-e694-4b66-82a3-befb08451722) [![Together AI](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775923621441-thumb.jpg&w=3840&q=75)\\
\\
**Together AI** \\
\\
Shifting geometric planes under a…](https://styles.refero.design/style/461da0f0-fde6-46bc-8137-7eca006260a8) [![Replicate](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F71c21f97-ba85-4439-b259-198a66f4b3d2-1777584297798-preview-poster.jpg&w=3840&q=75)\\
\\
**Replicate** \\
\\
Neon Gradient Playground. The site…](https://styles.refero.design/style/71c21f97-ba85-4439-b259-198a66f4b3d2) [![Twingate](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F0acef011-07da-4416-b874-ccdd675140f6-1777560744773-preview-poster.jpg&w=3840&q=75)\\
\\
**Twingate** \\
\\
Midnight Terminal, Pulsing Neon. A…](https://styles.refero.design/style/0acef011-07da-4416-b874-ccdd675140f6)

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
# JetBrains — Style Reference
> Neon nebula on obsidian — a black-ground page where violet-blue gradients bloom upward like deep-space imagery, punctuated by hot-pink neon and per-product chromatic icon light.

**Theme:** dark

JetBrains' site feels like the interior of a deep-space control room — pure black (#000000) ground plane with electric violet-to-blue gradients erupting from the darkness like bioluminescent nebulae. The defining moves are the chromatic product icon ecosystem (each IDE gets a vivid multicolor badge) floating against near-black surfaces, and the blue radial glow (rgba(0,71,253,0.8) at 75% opacity) diffused behind hero content like a spotlight on a dark stage. Headlines at 72-79px use JetBrains Sans weight 600 with tight letter-spacing, while the hot-pink accent (#f31199, CSS var --main-page-pink) fires only on category labels and brand moments — a neon sign in a dark corridor. Cards use 24px radius with translucent violet or pink fills (rgba(90,31,208,0.3), rgba(243,17,180,0.2)) that glow rather than separate.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Obsidian Ground | `#000000` | `--color-obsidian-ground` | Page background — the absolute black base all gradients and glows emerge from |
| Deep Charcoal | `#19191c` | `--color-deep-charcoal` | Nav bar background, footer, elevated surface one step above absolute black |
| Graphite | `#343434` | `--color-graphite` | Most-used color on site; borders, dividers, muted icon strokes, body text secondary contexts |
| Iron | `#474749` | `--color-iron` | Subtle borders, inactive state outlines |
| Ash | `#757577` | `--color-ash` | Card borders, inactive dividers |
| Slate | `#8c8c8` | `--color-slate` | Secondary body text, muted icon fills |
| Silver | `#a3a3a4` | `--color-silver` | Tertiary icons, ghost button labels, disabled states |
| Fog | `#bababb` | `--color-fog` | Body text on dark backgrounds, list items, secondary link labels |
| Pure White | `#ffffff` | `--color-pure-white` | Primary headings, button labels on dark, high-emphasis body text |
| Electric Blue | `#18a3fa` | `--color-electric-blue` | Primary link color, info badges, active state highlights — the most-used chromatic color site-wide, giving the dark UI its cool electric temperature |
| Violet Pulse | `#7b61ff` | `--color-violet-pulse` | Button borders, badge backgrounds, primary CTA outlines — the core violet brand hue from the JetBrains logo |
| Iris | `#6b57ff` | `--color-iris` | Badge fills, body accent — slightly darker violet variant for surfaces needing more saturation |
| Amethyst | `#8473ff` | `--color-amethyst` | Heading accent color, primary dark-theme color token (--rs-color-primary-dark-theme) |
| Deep Violet | `#2e106a` | `--color-deep-violet` | CTA button background — deep space purple that pairs with Electric Blue (#18a3fa) text for a neon-on-void feel |
| Neon Pink | `#f31199` | `--color-neon-pink` | Category labels ('For businesses', 'For developers'), brand highlight moments — the signature hot-pink neon that fires sparingly against black like a neon sign (--main-page-pink) |
| Magenta Glow | `#5a1fd0` | `--color-magenta-glow` | Gradient start color for violet nebula gradient, card border accents |
| Nebula Violet | `linear-gradient(130deg, rgb(90, 31, 208) 10%, rgba(46, 16, 106, 0) 70%)` | `--color-nebula-violet` | Hero gradient bloom origin |
| Aurora Teal | `linear-gradient(90deg, rgb(8, 222, 170) -12.99%, rgb(0, 170, 250) 176.77%)` | `--color-aurora-teal` | Section accent headings, icon fills, gradient stop — teal-to-blue gradient used on feature callouts |
| Hero Blue Glow | `radial-gradient(87.36% 97.44% at 54.14% 23.32%, rgba(0, 71, 253, 0.8) 0px, rgba(0, 71, 253, 0.8) 15%, rgba(0, 0, 0, 0) 75%)` | `--color-hero-blue-glow` | Radial glow behind hero content — the deep blue spotlight effect that dominates the first viewport |
| Danger Red | `#f45c4a` | `--color-danger-red` | Error states, destructive actions (--rs-color-danger) |
| Success Green | `#4dbb5f` | `--color-success-green` | Success states (--rs-color-success) |
| Warning Amber | `#f3c033` | `--color-warning-amber` | Warning states (--rs-color-warning) |

## Tokens — Typography

### JetBrains Sans — The single typeface for the entire site at all sizes and weights. 600 at 72-79px for hero headlines — unusual that even at this weight the custom letterSpacing tightening (-0.005em to -0.001em) keeps the large type dense and technical rather than editorial. Weight 300 appears at mid-sizes giving subheadings a lighter counterpoint to bold display text. JetBrains Sans is custom-designed — it carries optical metrics tuned for code-adjacent contexts, slightly wider than Inter at body sizes, with liga/calt features active that echo the IDE typographic environment. · `--font-jetbrains-sans`
- **Substitute:** Inter, Plus Jakarta Sans
- **Weights:** 300, 400, 500, 600
- **Sizes:** 13px, 16px, 20px, 29px, 35px, 43px, 72px, 79px
- **Line height:** 0.90–1.54 (tighter at larger sizes: 0.90 at display, 1.50–1.54 at body)
- **Letter spacing:** -0.40px at large sizes (72-79px, -0.005em), -0.08px at mid sizes (29-43px, -0.001em), +0.032px at small sizes (16px, +0.002em), +0.065px at 13px (+0.005em)
- **OpenType features:** `"calt", "kern", "liga"`
- **Role:** The single typeface for the entire site at all sizes and weights. 600 at 72-79px for hero headlines — unusual that even at this weight the custom letterSpacing tightening (-0.005em to -0.001em) keeps the large type dense and technical rather than editorial. Weight 300 appears at mid-sizes giving subheadings a lighter counterpoint to bold display text. JetBrains Sans is custom-designed — it carries optical metrics tuned for code-adjacent contexts, slightly wider than Inter at body sizes, with liga/calt features active that echo the IDE typographic environment.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| caption | 13px | 1.2 | 0.065px | `--text-caption` |
| body-sm | 16px | 1.5 | 0.032px | `--text-body-sm` |
| body | 20px | 1.4 | — | `--text-body` |
| subheading | 29px | 1.34 | -0.029px | `--text-subheading` |
| heading-sm | 35px | 1.2 | -0.035px | `--text-heading-sm` |
| heading | 43px | 1.14 | -0.043px | `--text-heading` |
| heading-lg | 72px | 1 | -0.36px | `--text-heading-lg` |
| display | 79px | 0.9 | -0.395px | `--text-display` |

## Tokens — Spacing & Shapes

**Base unit:** 8px

**Density:** comfortable

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 8 | 8px | `--spacing-8` |
| 16 | 16px | `--spacing-16` |
| 24 | 24px | `--spacing-24` |
| 32 | 32px | `--spacing-32` |
| 48 | 48px | `--spacing-48` |
| 64 | 64px | `--spacing-64` |
| 96 | 96px | `--spacing-96` |
| 144 | 144px | `--spacing-144` |
| 200 | 200px | `--spacing-200` |

### Border Radius

| Element | Value |
|---------|-------|
| cards | 24px |
| badges | 4-6px |
| images | 16px |
| modals | 24px |
| buttons | 20-26px |

### Layout

- **Page max-width:** 1280px
- **Section gap:** 80-120px
- **Card padding:** 24px
- **Element gap:** 8-16px

## Components

### Hero CTA Button — Primary Dark
**Role:** Main call-to-action on hero sections

White fill (#ffffff), #19191c text, 26px border-radius (pill), 12px top/bottom padding, 32px left/right padding. JetBrains Sans 16px weight 500. Used for 'Choose Your IDE' — solid white stands out starkly against the dark gradient hero.

### CTA Button — Violet Deep
**Role:** Secondary prominent CTA on feature cards

Background #2e106a (Deep Violet), text #18a3fa (Electric Blue), border #7b61ff (Violet Pulse) 1px, 16px border-radius, 24px padding all sides. The neon-blue text on deep-violet background creates an illuminated button that reads like an active screen element inside the IDE itself.

### Ghost Button — White Outlined
**Role:** Navigation links, secondary actions with text context

Background transparent, #ffffff text, 1px #ffffff border, 20px border-radius, 8px padding all sides. Used in nav contexts and as paired secondary to primary CTAs.

### Ghost Link Button — Borderless
**Role:** Nav bar top-level items, inline text actions

Background transparent, #ffffff text, no border (0px radius, 0px top/bottom padding, 10px left/right padding). Pure text with horizontal padding only — becomes a tab-style navigation element.

### Feature Announcement Card
**Role:** Hero carousel cards for product announcements like 'JetBrains IDEs 2026.1'

Background transparent with 1px border #5a1fd0 (Magenta Glow / vivid violet), 24px radius, internal padding 24-64px. Contains product name at 29-35px weight 600, body at 16px #bababb, IDE icon grid at 32px, and a 3D/abstract gradient visual asset on the right half. The violet border glows against black.

### Business Feature Card
**Role:** Gradient content card for audience-segmented sections

Background linear-gradient(130deg, rgb(90,31,208) 10%, rgba(46,16,106,0) 70%) overlaid with organic blob shapes in deep red/purple, 24px radius, 64px padding. White headlines at 35-43px weight 600, #bababb body at 16px, white ghost pill button (26px radius, 32px horizontal padding). The gradient gives the impression of colored light bleeding from within.

### Pink Tinted Feature Card
**Role:** Highlight cards for specific product moments

Background rgba(243,17,180,0.2) (20% opacity Neon Pink), 24px radius, 23px padding. The translucent magenta tint reads as a glowing selection highlight against the dark ground.

### Violet Badge — Filled
**Role:** Status labels like 'Now Live', 'Featured', 'Free for non-commercial use'

Background #6b57ff (Iris), #ffffff text, 4px radius, 1px top/bottom padding, 7px left/right padding, JetBrains Sans 13px weight 500. Sharp-cornered relative to other components — badges are the most rectangular element in the system.

### Violet Badge — Tab Style
**Role:** Contextual tab labels attached to card tops

Background rgba(107,87,255,0.5) (50% opacity Violet Pulse), #ffffff text, border-radius 6px 6px 0px 0px (top-rounded only), 5px top/bottom padding, 11px left/right padding. The flat bottom connects visually to the card it labels.

### IDE Product Icon Badge
**Role:** Per-product identity marks in product grids and navigation

32px square icons with each IDE's distinct multicolor gradient fill (no single token — each product has unique chromatic identity: IntelliJ IDEA uses orange/red/purple, PyCharm uses green/yellow, DataGrip uses teal/dark). Displayed on 16px radius containers. These are the primary chromatic diversity element of the system — the only place vivid orange (#ff8100), vivid green (#00d886), vivid yellow (#f0eb18) appear.

### Navigation Bar
**Role:** Top-level site navigation, always visible

Full-width, 72px height, background #19191c (Deep Charcoal). JetBrains logo mark (multicolor cube icon) + 'JETBRAINS' wordmark in #ffffff weight 500 at 16px, left-aligned. Nav items (#ffffff, no border, 10px horizontal padding) centered. Utility icons (search, account, cart, language) right-aligned in #a3a3a4 at 20px. No border-bottom — the header floats above the hero gradient.

### Carousel Pagination Control
**Role:** Slide navigation for announcement cards

Left/right arrow buttons with transparent background, 1px #474749 border, 20px radius, 8px padding. Counter text '1 / 2' in #bababb at 16px between arrows. Sits below card carousels, horizontally centered.

### Audience Segmentation Tab Row
**Role:** Segment switcher for 'For developers / For teams / For businesses'

Horizontal pill-group container with transparent background, each segment as a ghost button (20px radius). Active segment uses 1px #7b61ff border, #ffffff text. Inactive segments have no border, #bababb text. The group appears as a floating pill selector centered in the content area.

## Do's and Don'ts

### Do
- Use #000000 as the absolute page background — never a near-black like #0a0a0a or #111; the true black is what makes the gradient glows feel luminous
- Apply the radial blue glow (rgba(0,71,253,0.8) → transparent) behind hero content at ~87% width spread, centered on the content, so text appears spotlit from behind
- Use Neon Pink (#f31199) only for category labels and brand punctuation — 1-3 instances per page maximum; it reads as a signal color, not a fill color
- Set all card and feature panel border-radius to 24px; use 4px only for badges, never mix these on the same component
- Use translucent fills for card backgrounds: rgba(90,31,208,0.3) for violet-tinted cards, rgba(243,17,180,0.2) for pink-tinted cards — never opaque colored fills
- Apply JetBrains Sans with fontFeatureSettings '"calt", "kern", "liga"' active at all sizes, and apply negative letter-spacing (-0.005em) at display sizes 43px and above
- Give each JetBrains product its own distinct multicolor icon — the chromatic icon grid is the primary visual diversity mechanism; do not apply a single brand color to all icons

### Don't
- Do not use #18a3fa (Electric Blue) as a fill color for buttons or large surfaces — it is a text/border/link color only; as a fill it would overpower the dark palette
- Do not add box-shadows to cards — elevation is expressed through gradient fills and translucent backgrounds, never drop shadows
- Do not use border-radius below 16px on interactive elements (buttons, cards); sharp-cornered shapes are reserved exclusively for badges (4-6px)
- Do not place white text directly on the pure black background without a gradient zone or translucent card beneath for longer body text — use #bababb for body on raw black
- Do not use Neon Pink (#f31199) as a background fill for large areas — its opacity 0.2 translucent form (rgba(243,17,180,0.2)) is the maximum surface application
- Do not add a visible border-bottom to the navigation bar — the #19191c header transitions into the hero gradient without a line
- Do not apply uniform icon color — product icons must retain their individual per-product chromatic gradient identity; monochromatic treatment breaks the identity system

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Void | `#000000` | Absolute page background — the black base from which all gradients emerge |
| 1 | Deep Charcoal | `#19191c` | Navigation bar, footer — surfaces that need to sit above the background but below content cards |
| 2 | Violet Glass | `#2e106a` | Translucent violet card fills (rgba(90,31,208,0.3)) — feature announcement cards, business section panels |
| 3 | Pink Glass | `#45173a` | Translucent pink card fills (rgba(243,17,180,0.2)) — highlight feature cards for specific products |

## Elevation

Zero box-shadows anywhere on the site. Elevation and depth are created exclusively through gradient fills, translucent backgrounds with color tint (rgba violet/pink), and radial glow effects — not shadow casting. A card 'rises' because its colored translucent fill catches the light of the background gradient behind it, not because it casts a shadow below it. This approach keeps the dark theme feeling like illumination from within rather than objects floating above a surface.

## Imagery

Heavy use of abstract 3D rendered data-mesh visuals — luminous wireframe surfaces in pink/purple/blue forming curved grid planes, as seen in the 'JetBrains IDEs 2026.1' announcement card. These renders have no photographic elements; they're pure light-on-dark mathematical geometry suggesting data structures or network topology. Product screenshots are treated as dark-themed UI mockups (the IDE itself shown with dark editor theme) with rounded 8-16px corners, embedded within dark card contexts rather than on white backgrounds. No lifestyle photography or people imagery visible. Icons are 32px product logos with individual per-product multicolor gradient fills — each is a distinct chromatic identity mark, not a unified icon set. The overall image language is code-and-compute: abstract renders + UI screenshots + chromatic product icons, with zero real-world photography.

## Layout

Full-bleed dark canvas with a max-width content container of ~1280px centered. Hero is full-viewport with centered headline text over a radial blue glow, with an IDE screenshot mockup below the fold. Section rhythm moves from the blue-glow hero → card carousel section (full-bleed black) → audience segmentation tabs with gradient feature panels → product grid sections. No alternating light/dark bands — the entire page stays on the dark black ground, with section separation achieved via gradient card backgrounds and spacing (80-120px between sections) rather than background color changes. The 'For businesses' section temporarily shifts to a near-black #19191c ground for contrast. Card grids use 2-column layouts for feature panels and 4-5 column grids for the IDE product icon array. Navigation is a fixed top bar at 72px with logo-left, nav-center, utilities-right structure.

## Gradient System

Five gradient roles operate on the site: (1) HERO GLOW — radial-gradient(87.36% 97.44% at 54.14% 23.32%, rgba(0,71,253,0.8) 0px, rgba(0,71,253,0.8) 15%, rgba(0,0,0,0) 75%) — the defining visual of the homepage, a blue spotlight over absolute black. (2) VIOLET NEBULA — linear-gradient(130deg, rgb(90,31,208) 10%, rgba(46,16,106,0) 70%) — used on announcement card backgrounds, creates directional light bloom. (3) AURORA SWEEP — linear-gradient(90deg, rgb(8,222,170) -12.99%, rgb(0,170,250) 176.77%) — teal-to-blue, used on feature callout headings and icon fills. (4) EMERALD FADE — linear-gradient(130deg, rgba(33,215,137,0.6) -10%, rgba(106,16,70,0) 80%) — green-to-void, used as secondary section accent. (5) PRODUCT ILLUSTRATION — complex teal-to-navy multi-stop gradient (linear-gradient(0deg, rgb(78,197,185) 2.53%, ... rgb(22,24,27) 99.4%)) used in specific product feature visuals. All gradients fade to transparent or near-black — none have hard stops on both ends.

## Agent Prompt Guide

QUICK COLOR REFERENCE:
• Text (primary): #ffffff
• Text (secondary): #bababb
• Page background: #000000
• Nav/footer surface: #19191c
• CTA border/badge fill: #7b61ff
• CTA button text: #18a3fa
• CTA button background: #2e106a
• Accent/category label: #f31199
• Border (subtle): #474749

EXAMPLE COMPONENT PROMPTS:

1. HERO SECTION: Black background (#000000) with centered radial glow (rgba(0,71,253,0.8) spreading to transparent over ~87% width). Headline 'Purpose-Built IDEs for Every Language and Stack' at 72px JetBrains Sans weight 600, #ffffff, letter-spacing -0.36px, line-height 1.0, centered. Subtext at 20px weight 400, #bababb, centered below. Two CTA buttons side by side: (a) White pill button — #ffffff bg, #19191c text, 26px radius, 12px/32px padding, 16px weight 500; (b) Ghost outline — transparent bg, #ffffff text, 1px #ffffff border, 20px radius, 8px padding.

2. ANNOUNCEMENT CARD: Full-width card, 24px radius, 1px solid #5a1fd0 border, background linear-gradient(130deg, rgb(90,31,208) 10%, rgba(46,16,106,0) 70%). Left half: headline at 35px weight 600 #ffffff, badge 'Now Live' at 13px weight 500 #ffffff on #6b57ff bg 4px radius 7px padding. Product icon grid at 32px, labels at 13px #bababb. Right half: abstract 3D mesh illustration. Overall padding 24-64px.

3. AUDIENCE TAB ROW: Horizontally centered pill selector, three tabs ('For developers' / 'For teams' / 'For businesses'). Each tab: JetBrains Sans 16px weight 400, 20px radius, 8px padding. Active state: 1px solid #7b61ff border, #ffffff text, transparent background. Inactive: no border, #bababb text.

4. FEATURE CARD — PINK TINTED: 24px radius, background rgba(243,17,180,0.2), 23px padding all sides. Category label in #f31199 at 16px weight 500 above headline. Headline 29-35px weight 600 #ffffff. Body 16px #bababb. No border, no shadow.

5. BADGE: Background #6b57ff, #ffffff text, 4px radius, 1px vertical padding, 7px horizontal padding, JetBrains Sans 13px weight 500, font-features calt/kern/liga active.

## Similar Brands

- **GitHub** — Same black-ground dark theme with blue radial hero glow and product screenshot embedded in the hero
- **Vercel** — Absolute black (#000) page background with white type and gradient accent cards — no shadows, gradient-as-elevation approach
- **Linear** — Dark developer tool site with violet as primary brand accent color and pill-shaped navigation segmentation tabs
- **Raycast** — Dark UI with translucent gradient card panels, chromatic icon ecosystem per product/extension, and black-void backgrounds
- **Framer** — Abstract 3D mesh/grid visuals on dark backgrounds as primary hero imagery, with vivid accent gradients bleeding into pure black

## Quick Start

### CSS Custom Properties

```css
:root {
/* Colors */
  --color-obsidian-ground: #000000;
  --color-deep-charcoal: #19191c;
  --color-graphite: #343434;
  --color-iron: #474749;
  --color-ash: #757577;
  --color-slate: #8c8c8;
  --color-silver: #a3a3a4;
  --color-fog: #bababb;
  --color-pure-white: #ffffff;
  --color-electric-blue: #18a3fa;
  --color-violet-pulse: #7b61ff;
  --color-iris: #6b57ff;
  --color-amethyst: #8473ff;
  --color-deep-violet: #2e106a;
  --color-neon-pink: #f31199;
  --color-magenta-glow: #5a1fd0;
  --color-nebula-violet: #5a1fd0;
  --gradient-nebula-violet: linear-gradient(130deg, rgb(90, 31, 208) 10%, rgba(46, 16, 106, 0) 70%);
  --color-aurora-teal: #08deaa;
  --gradient-aurora-teal: linear-gradient(90deg, rgb(8, 222, 170) -12.99%, rgb(0, 170, 250) 176.77%);
  --color-hero-blue-glow: #0047fd;
  --gradient-hero-blue-glow: radial-gradient(87.36% 97.44% at 54.14% 23.32%, rgba(0, 71, 253, 0.8) 0px, rgba(0, 71, 253, 0.8) 15%, rgba(0, 0, 0, 0) 75%);
  --color-danger-red: #f45c4a;
  --color-success-green: #4dbb5f;
  --color-warning-amber: #f3c033;

/* Typography — Font Families */
  --font-jetbrains-sans: 'JetBrains Sans', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Typography — Scale */
  --text-caption: 13px;
  --leading-caption: 1.2;
  --tracking-caption: 0.065px;
  --text-body-sm: 16px;
  --leading-body-sm: 1.5;
  --tracking-body-sm: 0.032px;
  --text-body: 20px;
  --leading-body: 1.4;
  --text-subheading: 29px;
  --leading-subheading: 1.34;
  --tracking-subheading: -0.029px;
  --text-heading-sm: 35px;
  --leading-heading-sm: 1.2;
  --tracking-heading-sm: -0.035px;
  --text-heading: 43px;
  --leading-heading: 1.14;
  --tracking-heading: -0.043px;
  --text-heading-lg: 72px;
  --leading-heading-lg: 1;
  --tracking-heading-lg: -0.36px;
  --text-display: 79px;
  --leading-display: 0.9;
  --tracking-display: -0.395px;

/* Typography — Weights */
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;

/* Spacing */
  --spacing-unit: 8px;
  --spacing-8: 8px;
  --spacing-16: 16px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-48: 48px;
  --spacing-64: 64px;
  --spacing-96: 96px;
  --spacing-144: 144px;
  --spacing-200: 200px;

/* Layout */
  --page-max-width: 1280px;
  --section-gap: 80-120px;
  --card-padding: 24px;
  --element-gap: 8-16px;

/* Border Radius */
  --radius-md: 4px;
  --radius-2xl: 16px;
  --radius-2xl-2: 20px;
  --radius-3xl: 24px;

/* Named Radii */
  --radius-cards: 24px;
  --radius-badges: 4-6px;
  --radius-images: 16px;
  --radius-modals: 24px;
  --radius-buttons: 20-26px;

/* Surfaces */
  --surface-void: #000000;
  --surface-deep-charcoal: #19191c;
  --surface-violet-glass: #2e106a;
  --surface-pink-glass: #45173a;
}
```

### Tailwind v4

```css
@theme {
/* Colors */
  --color-obsidian-ground: #000000;
  --color-deep-charcoal: #19191c;
  --color-graphite: #343434;
  --color-iron: #474749;
  --color-ash: #757577;
  --color-slate: #8c8c8;
  --color-silver: #a3a3a4;
  --color-fog: #bababb;
  --color-pure-white: #ffffff;
  --color-electric-blue: #18a3fa;
  --color-violet-pulse: #7b61ff;
  --color-iris: #6b57ff;
  --color-amethyst: #8473ff;
  --color-deep-violet: #2e106a;
  --color-neon-pink: #f31199;
  --color-magenta-glow: #5a1fd0;
  --color-nebula-violet: #5a1fd0;
  --color-aurora-teal: #08deaa;
  --color-hero-blue-glow: #0047fd;
  --color-danger-red: #f45c4a;
  --color-success-green: #4dbb5f;
  --color-warning-amber: #f3c033;

/* Typography */
  --font-jetbrains-sans: 'JetBrains Sans', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Typography — Scale */
  --text-caption: 13px;
  --leading-caption: 1.2;
  --tracking-caption: 0.065px;
  --text-body-sm: 16px;
  --leading-body-sm: 1.5;
  --tracking-body-sm: 0.032px;
  --text-body: 20px;
  --leading-body: 1.4;
  --text-subheading: 29px;
  --leading-subheading: 1.34;
  --tracking-subheading: -0.029px;
  --text-heading-sm: 35px;
  --leading-heading-sm: 1.2;
  --tracking-heading-sm: -0.035px;
  --text-heading: 43px;
  --leading-heading: 1.14;
  --tracking-heading: -0.043px;
  --text-heading-lg: 72px;
  --leading-heading-lg: 1;
  --tracking-heading-lg: -0.36px;
  --text-display: 79px;
  --leading-display: 0.9;
  --tracking-display: -0.395px;

/* Spacing */
  --spacing-8: 8px;
  --spacing-16: 16px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-48: 48px;
  --spacing-64: 64px;
  --spacing-96: 96px;
  --spacing-144: 144px;
  --spacing-200: 200px;

/* Border Radius */
  --radius-md: 4px;
  --radius-2xl: 16px;
  --radius-2xl-2: 20px;
  --radius-3xl: 24px;
}
```
````

JetBrains — Refero Styles