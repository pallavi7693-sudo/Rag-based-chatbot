---
name: FundIQ
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb2b7'
  on-tertiary: '#67001b'
  tertiary-container: '#ff516a'
  on-tertiary-container: '#5b0017'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdadb'
  tertiary-fixed-dim: '#ffb2b7'
  on-tertiary-fixed: '#40000d'
  on-tertiary-fixed-variant: '#92002a'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  mono-data:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 20px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style

This design system is engineered for a high-performance fintech environment, balancing institutional precision with a modern, tech-forward aesthetic. The brand personality is professional, transparent, and authoritative, designed to evoke a sense of security and clarity in financial decision-making.

The visual style utilizes **Modern Glassmorphism** layered over a **Deep Corporate** foundation. It leverages high-contrast accents against a dark slate environment to guide user attention toward growth metrics and call-to-action points. The interface relies on subtle light-refraction effects, precise linework, and a "glowing" status language to communicate real-time data vitality.

## Colors

The palette is optimized for long-session legibility in a dark environment. 

- **Primary (Indigo):** Used for primary actions, active states, and brand-defining gradients. It represents the "intelligence" aspect of the brand.
- **Secondary (Emerald):** Reserved strictly for positive growth, success states, and "Buy" actions.
- **Tertiary (Rose):** Used for negative trends, error states, and "Sell" actions to provide immediate visual contrast.
- **Neutral (Slate):** The foundation of the UI. The base background is a deep slate (#0F172A), while elevated surfaces move toward lighter slate tones to create a sense of proximity.

## Typography

The design system employs **Inter** for core UI and headlines to ensure maximum readability and institutional trust. For data-heavy contexts, such as stock tickers, balances, and transaction IDs, **Geist** is used to provide a technical, high-precision feel that aligns with developer-grade financial tools.

- **Weight Usage:** Use SemiBold (600) for section headers and Bold (700) sparingly for primary numerical values.
- **Data Display:** Numerical values should always use tabular numbers to ensure alignment in lists and tables.

## Layout & Spacing

The system uses a **Fluid Grid** model with a base-4 spatial scale. 

- **Desktop:** 12-column grid with 20px gutters. Content is centered with a max-width of 1280px.
- **Mobile:** 4-column grid with 16px gutters and 16px side margins.
- **Rhythm:** Vertical rhythm is maintained through standard increments of 8px (e.g., 8px between a label and input, 24px between distinct card sections). 

Spacing is used to create "grouping through proximity," reducing the need for heavy divider lines in favor of clean, open layouts.

## Elevation & Depth

Depth is established through **Tonal Layering** and **Glassmorphism**. Unlike traditional elevation which uses heavy black shadows, this system uses "Inner Glows" and "Backdrop Blurs" to simulate light passing through glass.

- **Level 0 (Background):** #0F172A. Flat.
- **Level 1 (Cards/Surface):** Semi-transparent Slate (#1E293B at 60% opacity) with a 12px backdrop blur and a 1px border at 8% white.
- **Level 2 (Modals/Popovers):** Higher opacity Slate with a soft, 20% opacity indigo drop shadow (0px 10px 30px) to indicate focus.
- **Level 3 (Interaction):** Hover states on cards should trigger a subtle increase in border opacity (from 8% to 20%) and a faint primary-colored outer glow.

## Shapes

The shape language is **Refined and Intentional**. A standard radius of 8px (0.5rem) is used for most UI containers to balance approachable modernism with professional structure.

- **Standard (8px):** Buttons, Input fields, and standard list items.
- **Large (16px):** Main dashboard cards and content containers.
- **Pill (Full):** Status tags, filter chips, and primary action buttons in mobile views.

## Components

### Buttons
- **Primary:** Solid Indigo (#6366F1) with white text. Subtle 10% white inner-top border for a tactile feel.
- **Secondary:** Transparent background with a 1px Slate-400 border. Transitions to a 10% Indigo fill on hover.
- **Success (Buy):** Emerald (#10B981) with a soft glow effect in the shadow (8px blur, 15% opacity).

### Cards
All cards must utilize `backdrop-filter: blur(12px)`. Borders should be "hairline" (1px) using a linear gradient from top-left (White @ 12%) to bottom-right (White @ 2%).

### Status Pills
Status indicators (e.g., "Market Open", "Completed") use a high-saturation background at 10% opacity with a solid-color center dot and matching text color.

### Input Fields
Inputs are dark-filled (#1E293B) with a subtle 1px border. On focus, the border transitions to Primary Indigo with a 4px soft outer glow.

### Lists & Tables
Rows utilize subtle hover states (#FFFFFF at 4% opacity). Data columns containing currency should always be right-aligned and set in Geist (monospaced) for vertical decimal alignment.