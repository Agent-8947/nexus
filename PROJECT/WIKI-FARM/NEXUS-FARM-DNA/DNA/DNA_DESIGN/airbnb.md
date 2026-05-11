<!-- Source URL:  -->

![Screenshot of Airbnb](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc2325884-4391-4688-85cd-e143f5107517-1777581450106-preview-detail-poster.jpg&w=3840&q=75)

PreviewDESIGN.mdTailwind v4CSS VariablesDesign Tokens

![Screenshot of Airbnb](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc2325884-4391-4688-85cd-e143f5107517-1777581450106-preview-detail-poster.jpg&w=3840&q=75)

# Airbnb

![](https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://airbnb.com&size=128)

Vacation photos pinned to a white corkboard — bright photography contained in rounded frames against a near-white surface, with a single coral pin holding everything together.

Airbnb's interface is a warm, airy marketplace built on near-white surfaces and a single coral-red brand heartbeat. The #f7f7f7 canvas with #ffffff card surfaces creates a barely-there depth — paper stacked on paper — where photography does all the visual heavy lifting. The custom Airbnb Cereal VF variable font runs at weights 400–700 across a compact, tight scale with negative letter-spacing at larger sizes, giving the UI a quiet confidence without needing decorative elements. The singular #ff385c coral-red appears exclusively on brand touchpoints (logo, active states, the search button), making it feel like a signature rather than a system color. Card images bleed edge-to-edge with 20px rounded corners — the only generous radius in an otherwise compact, information-dense layout.

[https://www.airbnb.com](https://www.airbnb.com/)

## Color Palette

Brand

Copy

Rausch Coral#ff385cBrand logo fill, active nav underline, search button icon background, carousel dot active state — the single chromatic signature that makes the interface recognizable

Copy

Rausch Deep#e00b41Hover state darkening of Rausch Coral on interactive brand elements

Neutrals

Copy

Carbon#222222Primary text, headings, borders, icon strokes — the dominant neutral forming almost all typographic content

Copy

Slate#6a6a6aSecondary text (metadata, subtext, secondary labels), secondary icon fill

Copy

Stone#b0b0b0Skeleton/loading placeholder backgrounds

Copy

Silver#c1c1c1Disabled button text and icon strokes, inactive carousel navigation arrows

Copy

Pebble#ddddddCard image placeholder backgrounds, tertiary borders, disabled borders

Copy

Mist#ebebebSubtle dividers and secondary section borders

Copy

Fog#f7f7f7Page canvas, footer background, button hover/selected state background

Copy

Cloud#ffffffCard surfaces, header background, modal/popover backgrounds, pill badge fills

## Typography

Type Scale

Major Second (1.125) from 14px base

display28px · 700 · 1.43

The quick brown fox jumps

heading22px · 500 · 1.18

The quick brown fox jumps

21px21px · 700 · 1.43

The quick brown fox jumps

heading-sm20px · 600 · 1.2

The quick brown fox jumps

16px16px · 500 · 1.25

The quick brown fox jumps

body14px · 400 · 1.43

The quick brown fox jumps

13px13px · 400 · 1.23

The quick brown fox jumps

12px12px · 400 · 1.33

The quick brown fox jumps

Show all 10 steps

Fonts

PrimaryAirbnb Cereal VF

Weight400, 500, 600, 700

Sizes8–28px · 10 values

Line height1.18–1.43

Letter spacing-0.02em at large sizes (20px+), -0.009em at mid sizes (14–16px), +0.04em at small caps/label contexts (11–12px)

FallbackInter Variable

The sole typeface for every text element across the UI. Weight 400 handles body and metadata; 500 lifts labels and secondary headings; 600 marks section titles; 700 for price display and primary emphasis. The custom variable font brings tight optical metrics at display sizes that generic fonts cannot replicate — negative letter-spacing at -0.02em pulls large numerals together. The 'salt' feature set activates alternate letterforms that distinguish it from system sans-serifs.

## Spacing & Shape

Spacing

| Purpose | Value | Preview |
| --- | --- | --- |
| Density | compact |  |
| Max width | 1760px |  |
| Section gap | 48px |  |
| Card padding | 12px |  |
| Element gap | 8px |  |

Border Radius

| Element | Value | Preview |
| --- | --- | --- |
| badges | 4px |  |
| buttons | 8px |  |
| inputs | 14px |  |
| cards | 20px |  |
| searchBar | 20px |  |
| pills | 32px |  |
| iconButtons | 50% |  |

Elevation

Search Bar / Elevated Popover

Carousel Navigation Arrow Button

Guest Favorite Badge

## Guidelines

Do

- Use #ff385c exclusively for the brand logo, the search trigger button background, and active/selected state indicators — never for decorative fills or text blocks.
- Apply 20px border-radius to all listing cards and the main search bar container; use 8px for filter pill buttons and input fields; reserve 50% (circular) for icon-only buttons.
- Set all typography in Airbnb Cereal VF (substitute: Inter Variable) with font-feature-settings: 'salt'; apply letter-spacing -0.02em at 20px+ sizes and +0.04em for small-caps labels at 11–12px.
- Layer shadows as the three-value stack — rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px 0px, rgba(0,0,0,0.1) 0px 4px 8px 0px — on elevated containers like the search bar and modals only; listing cards use no shadow.
- Maintain the surface hierarchy strictly: page canvas #f7f7f7 → card/header surface #ffffff → disabled/placeholder fills #dddddd → skeleton loaders #b0b0b0.
- Keep section headings at 22px weight 600 with the inline arrow-link pattern; use 14px weight 400 #6a6a6a for all metadata (dates, host type, review counts).
- Use 12px as the base gap for intra-card elements and 48px for vertical section rhythm between listing rows.

Don't

- Never use #ff385c for body text, headings, or decorative strokes — its appearance outside logo/search-button/active-states breaks the signature scarcity of the brand color.
- Don't add heavy drop shadows to listing cards — cards use no shadow; the #dddddd placeholder color and 20px radius carry the visual weight without elevation.
- Never set headings above weight 700 or below weight 500; Airbnb Cereal VF at weight 800+ is not in the design system and breaks the measured typographic rhythm.
- Don't use border-radius values other than 4px, 8px, 14px, 20px, 32px, or 50% — mixing arbitrary radii (e.g. 6px, 12px, 24px) disrupts the deliberate radius vocabulary.
- Never place text directly on card photography without a scrim or badge surface — overlay content uses #ffffff or semi-transparent white containers, not raw text on image.
- Don't use the blue gradient (rgb(45,60,91) → rgb(128,157,192)) as a UI surface — it is specific to the hero CTA card animation and not part of the repeatable component palette.
- Never omit the 'salt' font feature setting on Airbnb Cereal VF — without it, the alternate letterforms revert to generic shapes that undermine brand distinctiveness.

## Component Preview

AI-generated examples showing how this design system looks when applied to real UI components.

Primary Search Bar

WhereSearch destinations

WhenAdd dates

WhoAdd guests

Listing Card

## Popular homes in Madrid

Guest favorite

Apartment in Madrid

Individual host

Jul 31 – Aug 2

€ 231 total
4.83


Guest favorite

Condo in Madrid

Individual host

Jul 24 – 26

€ 352 total
4.79


Apartment in Madrid

Business host

Jul 31 – Aug 2

€ 300 total
5.0


Guest favorite

Place to stay in Madrid

Business host

Jul 17 – 19

€ 703 total
5.0


Navigation Tab Bar

[Homes](https://styles.refero.design/style/c2325884-4391-4688-85cd-e143f5107517#) [NEW\\
Experiences](https://styles.refero.design/style/c2325884-4391-4688-85cd-e143f5107517#) [NEW\\
Services](https://styles.refero.design/style/c2325884-4391-4688-85cd-e143f5107517#)

Become a host

## More like this

[![Airbnb](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777521400731-thumb.jpg&w=3840&q=75)\\
\\
**Airbnb** \\
\\
High-contrast editorial canvas](https://styles.refero.design/style/194faa2f-2f69-4bbf-9e29-290f28fa8ca2) [![Raus](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777516752504-thumb.jpg&w=3840&q=75)\\
\\
**Raus** \\
\\
Warm rustic minimalism: soft…](https://styles.refero.design/style/d28732de-1b7a-4d37-b7aa-edfa7caf428b) [![Pinterest](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775924361580-thumb.jpg&w=3840&q=75)\\
\\
**Pinterest** \\
\\
Bright Workshop Canvas — A clean,…](https://styles.refero.design/style/8ff3bfb4-6f5e-4e07-83be-56e62ce80d2f) [![Land of Ride](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777514101794-thumb.jpg&w=3840&q=75)\\
\\
**Land of Ride** \\
\\
Editorial adventurer's journal](https://styles.refero.design/style/6d3c5056-dbb9-413b-9e9d-37183cfb97f8) [![Kobu](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777508664816-thumb.jpg&w=3840&q=75)\\
\\
**Kobu** \\
\\
Gallery Wall on Linen Canvas](https://styles.refero.design/style/355d4b38-1a53-4544-911e-0f5073ab836b) [![Anna Jóna](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777513419527-thumb.jpg&w=3840&q=75)\\
\\
**Anna Jóna** \\
\\
Warm Raspberry Vignette – a soft,…](https://styles.refero.design/style/71717c5a-324a-40ed-8a09-9a35df74f1d3) [![Vacation®](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777519972832-thumb.jpg&w=3840&q=75)\\
\\
**Vacation®** \\
\\
Sun-kissed retro comfort](https://styles.refero.design/style/a0392801-aa0f-4c0c-81e1-4e1684eb832a) [![Sometimes Always](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777516365858-thumb.jpg&w=3840&q=75)\\
\\
**Sometimes Always** \\
\\
Boutique bodega postcard](https://styles.refero.design/style/e30d2fb6-e3d6-4e0a-9395-6d196d5e7c7d) [![Dialog](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fc8c22958-ec50-47f1-aedc-a131d7aeb442-1777559660996-preview-poster.jpg&w=3840&q=75)\\
\\
**Dialog** \\
\\
Neutral showroom with one warm…](https://styles.refero.design/style/c8c22958-ec50-47f1-aedc-a131d7aeb442) [![Away](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775924510994-thumb.jpg&w=3840&q=75)\\
\\
**Away** \\
\\
Luxury travel catalogue](https://styles.refero.design/style/3ddaa1f6-bebc-44e3-a6df-b653179f3fd9) [![Partiful](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F6db1057d-3457-4173-9184-df160415f060-1777559999331-preview-poster.jpg&w=3840&q=75)\\
\\
**Partiful** \\
\\
confetti landing on white marble —…](https://styles.refero.design/style/6db1057d-3457-4173-9184-df160415f060) [![Vibrants](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777520836024-thumb.jpg&w=3840&q=75)\\
\\
**Vibrants** \\
\\
white canvas, vibrant accents](https://styles.refero.design/style/f73ce3e0-4452-4b21-b36f-6fde27de2cd6) [![Dribbble](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1775924005818-thumb.jpg&w=3840&q=75)\\
\\
**Dribbble** \\
\\
Gallery Wall on White Linen —…](https://styles.refero.design/style/b8ce0a90-40c6-4518-940c-8c97ccf9c1a0) [![Hudson Gavin Martin](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777520969072-thumb.jpg&w=3840&q=75)\\
\\
**Hudson Gavin Martin** \\
\\
Architectural blueprint on white…](https://styles.refero.design/style/fece962d-a580-4365-8afd-c9905a2502b1) [![Fiasco](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777508828312-thumb.jpg&w=3840&q=75)\\
\\
**Fiasco** \\
\\
Gallery canvas, warm minimal.](https://styles.refero.design/style/ef73c742-1c3b-48b9-a174-de365ecc4691) [![O0](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777513154130-thumb.jpg&w=3840&q=75)\\
\\
**O0** \\
\\
gallery wall contrast](https://styles.refero.design/style/36752f78-1c43-471b-b125-e82152ad23dd) [![Apple](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fa48ef430-8c6a-42d8-8c53-ab7bb43cf33b-1777560879986-preview-poster.jpg&w=3840&q=75)\\
\\
**Apple** \\
\\
Precise Canvas, Vivid Product. A…](https://styles.refero.design/style/a48ef430-8c6a-42d8-8c53-ab7bb43cf33b) [![Revenuecat](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2Fb5fdba21-fd4d-427e-b551-1e22c51e42db-1777560842124-preview-poster.jpg&w=3840&q=75)\\
\\
**Revenuecat** \\
\\
precision architecture on crisp…](https://styles.refero.design/style/b5fdba21-fd4d-427e-b551-1e22c51e42db) [![Fresha](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777510305969-thumb.jpg&w=3840&q=75)\\
\\
**Fresha** \\
\\
Luminous radial gradient](https://styles.refero.design/style/066625ba-0d8d-472e-8240-4026ed7bb94e) [![Spacelab](https://styles.refero.design/_next/image?url=https%3A%2F%2Fysxnuuuj3kqhdyj2.public.blob.vercel-storage.com%2F1777514854361-thumb.jpg&w=3840&q=75)\\
\\
**Spacelab** \\
\\
Architectural blueprint on white…](https://styles.refero.design/style/7fdcf5eb-4d65-49a2-b887-60119bca4edc)

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
# Airbnb — Style Reference
> Vacation photos pinned to a white corkboard — bright photography contained in rounded frames against a near-white surface, with a single coral pin holding everything together.

**Theme:** light

Airbnb's interface is a warm, airy marketplace built on near-white surfaces and a single coral-red brand heartbeat. The #f7f7f7 canvas with #ffffff card surfaces creates a barely-there depth — paper stacked on paper — where photography does all the visual heavy lifting. The custom Airbnb Cereal VF variable font runs at weights 400–700 across a compact, tight scale with negative letter-spacing at larger sizes, giving the UI a quiet confidence without needing decorative elements. The singular #ff385c coral-red appears exclusively on brand touchpoints (logo, active states, the search button), making it feel like a signature rather than a system color. Card images bleed edge-to-edge with 20px rounded corners — the only generous radius in an otherwise compact, information-dense layout.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Rausch Coral | `#ff385c` | `--color-rausch-coral` | Brand logo fill, active nav underline, search button icon background, carousel dot active state — the single chromatic signature that makes the interface recognizable |
| Rausch Deep | `#e00b41` | `--color-rausch-deep` | Hover state darkening of Rausch Coral on interactive brand elements |
| Carbon | `#222222` | `--color-carbon` | Primary text, headings, borders, icon strokes — the dominant neutral forming almost all typographic content |
| Slate | `#6a6a6a` | `--color-slate` | Secondary text (metadata, subtext, secondary labels), secondary icon fill |
| Silver | `#c1c1c1` | `--color-silver` | Disabled button text and icon strokes, inactive carousel navigation arrows |
| Stone | `#b0b0b0` | `--color-stone` | Skeleton/loading placeholder backgrounds |
| Pebble | `#dddddd` | `--color-pebble` | Card image placeholder backgrounds, tertiary borders, disabled borders |
| Mist | `#ebebeb` | `--color-mist` | Subtle dividers and secondary section borders |
| Fog | `#f7f7f7` | `--color-fog` | Page canvas, footer background, button hover/selected state background |
| Cloud | `#ffffff` | `--color-cloud` | Card surfaces, header background, modal/popover backgrounds, pill badge fills |

## Tokens — Typography

### Airbnb Cereal VF — The sole typeface for every text element across the UI. Weight 400 handles body and metadata; 500 lifts labels and secondary headings; 600 marks section titles; 700 for price display and primary emphasis. The custom variable font brings tight optical metrics at display sizes that generic fonts cannot replicate — negative letter-spacing at -0.02em pulls large numerals together. The 'salt' feature set activates alternate letterforms that distinguish it from system sans-serifs. · `--font-airbnb-cereal-vf`
- **Substitute:** Inter Variable
- **Weights:** 400, 500, 600, 700
- **Sizes:** 8px, 11px, 12px, 13px, 14px, 16px, 20px, 21px, 22px, 28px
- **Line height:** 1.18–1.43
- **Letter spacing:** -0.02em at large sizes (20px+), -0.009em at mid sizes (14–16px), +0.04em at small caps/label contexts (11–12px)
- **OpenType features:** `"salt"`
- **Role:** The sole typeface for every text element across the UI. Weight 400 handles body and metadata; 500 lifts labels and secondary headings; 600 marks section titles; 700 for price display and primary emphasis. The custom variable font brings tight optical metrics at display sizes that generic fonts cannot replicate — negative letter-spacing at -0.02em pulls large numerals together. The 'salt' feature set activates alternate letterforms that distinguish it from system sans-serifs.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| caption | 11px | 1.29 | 0.44px | `--text-caption` |
| body | 14px | 1.43 | -0.13px | `--text-body` |
| heading-sm | 20px | 1.25 | -0.18px | `--text-heading-sm` |
| heading | 22px | 1.23 | -0.2px | `--text-heading` |
| display | 28px | 1.18 | -0.56px | `--text-display` |

## Tokens — Spacing & Shapes

**Density:** compact

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 6 | 6px | `--spacing-6` |
| 8 | 8px | `--spacing-8` |
| 10 | 10px | `--spacing-10` |
| 11 | 11px | `--spacing-11` |
| 12 | 12px | `--spacing-12` |
| 13 | 13px | `--spacing-13` |
| 15 | 15px | `--spacing-15` |
| 16 | 16px | `--spacing-16` |
| 20 | 20px | `--spacing-20` |
| 24 | 24px | `--spacing-24` |
| 28 | 28px | `--spacing-28` |
| 32 | 32px | `--spacing-32` |
| 40 | 40px | `--spacing-40` |
| 44 | 44px | `--spacing-44` |
| 48 | 48px | `--spacing-48` |

### Border Radius

| Element | Value |
|---------|-------|
| cards | 20px |
| pills | 32px |
| badges | 4px |
| inputs | 14px |
| buttons | 8px |
| searchBar | 20px |
| iconButtons | 50% |

### Shadows

| Name | Value | Token |
|------|-------|-------|
| subtle | `rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) ...` | `--shadow-subtle` |
| subtle-2 | `rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.16) ...` | `--shadow-subtle-2` |

### Layout

- **Page max-width:** 1760px
- **Section gap:** 48px
- **Card padding:** 12px
- **Element gap:** 8px

## Components

### Listing Card
**Role:** Primary browsable content unit in scrollable horizontal carousels

Background #dddddd placeholder transitioning to full-bleed photography. 20px border-radius. No visible border. No shadow by default. Image occupies full card width; below image: 12px padding wrapping title (14px weight 600 #222222), host type (12px weight 400 #6a6a6a), date range and price (14px weight 400 #222222). Star rating shown at 12px with #222222. Aspect ratio approximately 1:1 on image portion. 'Guest favorite' badge: white background, #222222 text at 11px weight 600, 4px radius, absolute positioned top-left over image.

### Guest Favorite Badge
**Role:** Trust signal overlaid on listing card images

White (#ffffff) background pill, 4px border-radius, 6px vertical / 10px horizontal padding. Text 'Guest favorite' at 11px weight 600 #222222, letter-spacing +0.04em. Positioned top-left absolute over card image with a subtle drop-shadow: rgba(0,0,0,0.25) 0px 2px 6px.

### Primary Search Bar
**Role:** Main search interface in the header

Three segmented inputs (Where / When / Who) in a single white (#ffffff) pill container with 20px radius and layered shadow: rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px 0px, rgba(0,0,0,0.1) 0px 4px 8px 0px. Label text 12px weight 600 #222222; placeholder text 14px weight 400 #6a6a6a. Dividers between segments are 1px #ebebeb. Search trigger: 40px circle button, background #ff385c, white magnifying glass icon.

### Circular Icon Button — Default
**Role:** Carousel navigation arrows, save/wishlist toggles

50% border-radius. Two states: transparent background with #222222 icon stroke (active), and #f7f7f7 background with #c1c1c1 icon stroke (disabled). No padding; button is icon-sized only. Shadow: rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.16) 0px 2px 4px 0px applied to carousel arrows.

### Rounded Pill Button — Secondary
**Role:** Filter category tabs (Popular, Beach, Cities, Historic)

Background transparent or #f7f7f7 on selected. Border 1px solid #222222. Text 14px weight 500 #222222. 8px border-radius. 10px vertical / 10px horizontal padding. On hover background shifts to #f7f7f7.

### Ghost Text Button — Nav Link
**Role:** Top navigation links: Homes, Experiences, Services

No background, no border. Text 14px weight 600 #222222. Active state shows 2px solid #222222 underline. 'NEW' badge: 11px weight 600 #ff385c, positioned top-right of label. Padding 8px vertical.

### Become a Host Button
**Role:** Tertiary CTA in global header navigation

No background fill, no border. Text 14px weight 600 #222222. On hover background #f7f7f7, 8px radius. Sits inline in the right nav cluster alongside the globe icon and hamburger menu.

### Section Header with Arrow Link
**Role:** Section title + 'See all' inline link

Heading text 22px weight 600 #222222 with letter-spacing -0.2px. Followed inline by a right-arrow icon link in #222222. 'See all' fallback link: 14px weight 500 #222222, no underline by default, underline on hover. Margin-bottom 12px before card carousel.

### Star Rating Indicator
**Role:** Listing quality signal below card image

Star icon filled #222222 at 10px. Rating number 12px weight 600 #222222. Review count 12px weight 400 #6a6a6a in parentheses. Displayed inline with 2px gap.

### Global Header
**Role:** Sticky top bar containing logo, nav, and search

White (#ffffff) background, 96px height, 1px bottom border #ebebeb. Airbnb logo left-aligned: coral (#ff385c) mark + wordmark at 30px. Center: Homes/Experiences/Services nav with active underline. Right: 'Become a host' text, globe icon button (circular), hamburger menu button (circular, #f7f7f7 background). On scroll, search collapses into a compact pill with shadow.

### Carousel Scroll Container
**Role:** Horizontal scrollable listing row per section

Cards arranged in a single horizontal row with 12px column gap. Left/right chevron navigation buttons (circular, 40px diameter, white fill with shadow) positioned at vertical center of image portion. Scroll is paginated. No visible scrollbar.

## Do's and Don'ts

### Do
- Use #ff385c exclusively for the brand logo, the search trigger button background, and active/selected state indicators — never for decorative fills or text blocks.
- Apply 20px border-radius to all listing cards and the main search bar container; use 8px for filter pill buttons and input fields; reserve 50% (circular) for icon-only buttons.
- Set all typography in Airbnb Cereal VF (substitute: Inter Variable) with font-feature-settings: 'salt'; apply letter-spacing -0.02em at 20px+ sizes and +0.04em for small-caps labels at 11–12px.
- Layer shadows as the three-value stack — rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px 0px, rgba(0,0,0,0.1) 0px 4px 8px 0px — on elevated containers like the search bar and modals only; listing cards use no shadow.
- Maintain the surface hierarchy strictly: page canvas #f7f7f7 → card/header surface #ffffff → disabled/placeholder fills #dddddd → skeleton loaders #b0b0b0.
- Keep section headings at 22px weight 600 with the inline arrow-link pattern; use 14px weight 400 #6a6a6a for all metadata (dates, host type, review counts).
- Use 12px as the base gap for intra-card elements and 48px for vertical section rhythm between listing rows.

### Don't
- Never use #ff385c for body text, headings, or decorative strokes — its appearance outside logo/search-button/active-states breaks the signature scarcity of the brand color.
- Don't add heavy drop shadows to listing cards — cards use no shadow; the #dddddd placeholder color and 20px radius carry the visual weight without elevation.
- Never set headings above weight 700 or below weight 500; Airbnb Cereal VF at weight 800+ is not in the design system and breaks the measured typographic rhythm.
- Don't use border-radius values other than 4px, 8px, 14px, 20px, 32px, or 50% — mixing arbitrary radii (e.g. 6px, 12px, 24px) disrupts the deliberate radius vocabulary.
- Never place text directly on card photography without a scrim or badge surface — overlay content uses #ffffff or semi-transparent white containers, not raw text on image.
- Don't use the blue gradient (rgb(45,60,91) → rgb(128,157,192)) as a UI surface — it is specific to the hero CTA card animation and not part of the repeatable component palette.
- Never omit the 'salt' font feature setting on Airbnb Cereal VF — without it, the alternate letterforms revert to generic shapes that undermine brand distinctiveness.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 1 | Canvas | `#f7f7f7` | Page background and footer fill — the paper beneath everything |
| 2 | Card / Header | `#ffffff` | Listing card information areas, global header bar, search bar container, modal surfaces |
| 3 | Placeholder | `#dddddd` | Image loading skeleton within cards before photo loads |
| 4 | Loader | `#b0b0b0` | Animated skeleton pulse overlay on card image placeholders |

## Elevation

- **Search Bar / Elevated Popover:** `rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) 0px 2px 6px 0px, rgba(0, 0, 0, 0.1) 0px 4px 8px 0px`
- **Carousel Navigation Arrow Button:** `rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.16) 0px 2px 4px 0px`
- **Guest Favorite Badge:** `drop-shadow(rgba(0, 0, 0, 0.25) 0px 2px 6px)`

## Imagery

Full-bleed interior and architectural photography with no color treatment — images are vibrant and unfiltered, occupying 70–75% of each listing card's visual area. Photos are contained within 20px rounded-corner cards; no sharp-edge or full-bleed-to-viewport images on the listing grid. The images are lifestyle-adjacent but product-focused: rooms, beds, living spaces shot in natural light, staged but not dramatically lit. No illustrations, no abstract graphics, no 3D renders. Icons are outlined (thin ~1.5px stroke), monochromatic in #222222, used only for functional UI (navigation, save, search, share). The design is heavily image-dense — in any section, photography accounts for roughly 4× the visual area of text — making the listing grid feel like a photo album with metadata annotations rather than a product catalog.

## Layout

Max-width approximately 1760px, centered, with ~24px horizontal page padding. The header is fixed at 96px with white fill, containing logo left, tab nav center, utility right. Below the header, a search bar pill floats centered at roughly 72px height. The main content begins at ~200px from top with a section heading + horizontal card carousel pattern that repeats every 48px of vertical rhythm. Each section is a label + scrollable single-row card strip (7–8 cards visible, paginated). Cards maintain equal width (~160–180px) with 12px gutters. There is no alternating dark/light band rhythm — every section sits on the same #f7f7f7 canvas with white card surfaces. The footer is a dense multi-column link grid on #f7f7f7. Navigation is a slim top bar with no sidebar, no mega-menu, and no sticky secondary nav.

## Agent Prompt Guide

**Quick Color Reference**
- Text primary: #222222
- Text secondary: #6a6a6a
- Background (canvas): #f7f7f7
- Surface (cards, header): #ffffff
- Border / divider: #ebebeb
- Brand accent: #ff385c
- primary action: no distinct CTA color

**Example Component Prompts**

1. **Listing Card**: White (#ffffff) info area below a full-bleed photo placeholder (#dddddd), 20px border-radius, no shadow. Below image: listing title at 14px Airbnb Cereal VF weight 600 #222222; host type + dates at 12px weight 400 #6a6a6a; price at 14px weight 600 #222222. Star icon + rating at 12px weight 600 #222222 with review count at 12px #6a6a6a. 'Guest Favorite' badge: absolute top-left, white background, 4px radius, 11px weight 600 #222222, letter-spacing +0.04em, shadow drop-shadow(rgba(0,0,0,0.25) 0px 2px 6px).

2. **Search Bar**: White (#ffffff) pill, 20px radius, shadow rgba(0,0,0,0.02) 0px 0px 0px 1px + rgba(0,0,0,0.04) 0px 2px 6px + rgba(0,0,0,0.1) 0px 4px 8px. Three inline segments (Where / When / Who) with 12px vertical padding, label 12px weight 600 #222222, placeholder 14px weight 400 #6a6a6a, separated by 1px #ebebeb dividers. Right-end: 40px circle #ff385c background with white search icon.

3. **Section Header**: Text 22px Airbnb Cereal VF weight 600 #222222, letter-spacing -0.2px, followed immediately by a →  arrow icon in #222222. Bottom margin 12px before the card carousel. Subtext (optional) 14px weight 400 #6a6a6a directly below heading.

4. **Filter Pill Button**: 8px border-radius, 1px solid #222222 border, transparent background (hover: #f7f7f7). Text 14px Airbnb Cereal VF weight 500 #222222. Padding 10px all sides. Selected state: background #222222, text #ffffff.

5. **Carousel Arrow Button**: 40px diameter circle, 50% radius. Active: white (#ffffff) background, #222222 chevron icon, shadow rgba(0,0,0,0.02) 0px 0px 0px 1px + rgba(0,0,0,0.16) 0px 2px 4px. Disabled: #f7f7f7 background, #c1c1c1 icon, no shadow.

## Motion Philosophy

Transitions run at 0.25s ease for most interactive state changes (hover backgrounds, shadow lifts), with 0.1s for immediate snap feedback (button presses). The homepage hero card stack uses a custom spring curve — linear(0 0%, 0.238367 8.33%... 1 100%) — for the stacked card fan animation, giving it a physical bounce that distinguishes it from the otherwise utilitarian transition vocabulary. Transform is the primary transitioned property (141 instances), reinforcing that the design moves things rather than fades them. The backdrop-filter: blur(32px) is used on overlay surfaces (e.g. sticky compact search on scroll).

## Similar Brands

- **Booking.com** — Same photography-dominant card grid with near-white canvas, metadata below image, and star ratings as the primary trust signal
- **Vrbo** — Identical horizontal carousel-per-section layout pattern with full-bleed card photography and rounded image containers
- **Tripadvisor** — Shared compact typographic scale using a single custom sans-serif across all text levels with a single vivid brand-color accent
- **Etsy** — Same surface hierarchy (off-white canvas → white card → no card shadow) with photography as the sole source of visual richness and a single warm-hued brand accent

## Quick Start

### CSS Custom Properties

```css
:root {
/* Colors */
  --color-rausch-coral: #ff385c;
  --color-rausch-deep: #e00b41;
  --color-carbon: #222222;
  --color-slate: #6a6a6a;
  --color-silver: #c1c1c1;
  --color-stone: #b0b0b0;
  --color-pebble: #dddddd;
  --color-mist: #ebebeb;
  --color-fog: #f7f7f7;
  --color-cloud: #ffffff;

/* Typography — Font Families */
  --font-airbnb-cereal-vf: 'Airbnb Cereal VF', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Typography — Scale */
  --text-caption: 11px;
  --leading-caption: 1.29;
  --tracking-caption: 0.44px;
  --text-body: 14px;
  --leading-body: 1.43;
  --tracking-body: -0.13px;
  --text-heading-sm: 20px;
  --leading-heading-sm: 1.25;
  --tracking-heading-sm: -0.18px;
  --text-heading: 22px;
  --leading-heading: 1.23;
  --tracking-heading: -0.2px;
  --text-display: 28px;
  --leading-display: 1.18;
  --tracking-display: -0.56px;

/* Typography — Weights */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

/* Spacing */
  --spacing-4: 4px;
  --spacing-6: 6px;
  --spacing-8: 8px;
  --spacing-10: 10px;
  --spacing-11: 11px;
  --spacing-12: 12px;
  --spacing-13: 13px;
  --spacing-15: 15px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-28: 28px;
  --spacing-32: 32px;
  --spacing-40: 40px;
  --spacing-44: 44px;
  --spacing-48: 48px;

/* Layout */
  --page-max-width: 1760px;
  --section-gap: 48px;
  --card-padding: 12px;
  --element-gap: 8px;

/* Border Radius */
  --radius-sm: 1.5px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-xl: 14px;
  --radius-2xl: 20px;
  --radius-3xl: 32px;
  --radius-full: 50px;
  --radius-full-2: 100px;

/* Named Radii */
  --radius-cards: 20px;
  --radius-pills: 32px;
  --radius-badges: 4px;
  --radius-inputs: 14px;
  --radius-buttons: 8px;
  --radius-searchbar: 20px;
  --radius-iconbuttons: 50%;

/* Shadows */
  --shadow-subtle: rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) 0px 2px 6px 0px, rgba(0, 0, 0, 0.1) 0px 4px 8px 0px;
  --shadow-subtle-2: rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.16) 0px 2px 4px 0px;

/* Surfaces */
  --surface-canvas: #f7f7f7;
  --surface-card-header: #ffffff;
  --surface-placeholder: #dddddd;
  --surface-loader: #b0b0b0;
}
```

### Tailwind v4

```css
@theme {
/* Colors */
  --color-rausch-coral: #ff385c;
  --color-rausch-deep: #e00b41;
  --color-carbon: #222222;
  --color-slate: #6a6a6a;
  --color-silver: #c1c1c1;
  --color-stone: #b0b0b0;
  --color-pebble: #dddddd;
  --color-mist: #ebebeb;
  --color-fog: #f7f7f7;
  --color-cloud: #ffffff;

/* Typography */
  --font-airbnb-cereal-vf: 'Airbnb Cereal VF', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Typography — Scale */
  --text-caption: 11px;
  --leading-caption: 1.29;
  --tracking-caption: 0.44px;
  --text-body: 14px;
  --leading-body: 1.43;
  --tracking-body: -0.13px;
  --text-heading-sm: 20px;
  --leading-heading-sm: 1.25;
  --tracking-heading-sm: -0.18px;
  --text-heading: 22px;
  --leading-heading: 1.23;
  --tracking-heading: -0.2px;
  --text-display: 28px;
  --leading-display: 1.18;
  --tracking-display: -0.56px;

/* Spacing */
  --spacing-4: 4px;
  --spacing-6: 6px;
  --spacing-8: 8px;
  --spacing-10: 10px;
  --spacing-11: 11px;
  --spacing-12: 12px;
  --spacing-13: 13px;
  --spacing-15: 15px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-28: 28px;
  --spacing-32: 32px;
  --spacing-40: 40px;
  --spacing-44: 44px;
  --spacing-48: 48px;

/* Border Radius */
  --radius-sm: 1.5px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-xl: 14px;
  --radius-2xl: 20px;
  --radius-3xl: 32px;
  --radius-full: 50px;
  --radius-full-2: 100px;

/* Shadows */
  --shadow-subtle: rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) 0px 2px 6px 0px, rgba(0, 0, 0, 0.1) 0px 4px 8px 0px;
  --shadow-subtle-2: rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.16) 0px 2px 4px 0px;
}
```
````

Airbnb — Refero Styles