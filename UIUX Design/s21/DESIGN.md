---
name: Clinical Precision
colors:
  surface: '#f9f9ff'
  surface-dim: '#d0daf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e8eeff'
  surface-container-high: '#dfe8ff'
  surface-container-highest: '#d9e3fb'
  on-surface: '#111c2d'
  on-surface-variant: '#424754'
  inverse-surface: '#273143'
  inverse-on-surface: '#ecf0ff'
  outline: '#727785'
  outline-variant: '#c2c6d6'
  surface-tint: '#005ac2'
  primary: '#0058be'
  on-primary: '#ffffff'
  primary-container: '#2170e4'
  on-primary-container: '#fefcff'
  inverse-primary: '#adc6ff'
  secondary: '#0051d5'
  on-secondary: '#ffffff'
  secondary-container: '#316bf3'
  on-secondary-container: '#fefcff'
  tertiary: '#555c6e'
  on-tertiary: '#ffffff'
  tertiary-container: '#6e7487'
  on-tertiary-container: '#fefcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#b4c5ff'
  on-secondary-fixed: '#00174b'
  on-secondary-fixed-variant: '#003ea8'
  tertiary-fixed: '#dce2f7'
  tertiary-fixed-dim: '#c0c6db'
  on-tertiary-fixed: '#141b2b'
  on-tertiary-fixed-variant: '#404758'
  background: '#f9f9ff'
  on-background: '#111c2d'
  surface-variant: '#d9e3fb'
typography:
  display-kpi:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
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
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1440px
  gutter: 24px
  margin-desktop: 40px
  margin-mobile: 16px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style
The design system is engineered for high-stakes enterprise healthcare environments, where clarity, speed of cognition, and trust are paramount. The brand personality is "Clinical Precision"—it is authoritative yet empathetic, utilizing a refined **Corporate / Modern** aesthetic that leans into high-end minimalism.

The visual narrative focuses on reducing cognitive load for clinicians and administrators. By leveraging a "White-Space First" philosophy, the UI breathes, ensuring that critical patient data and KPIs are never obscured by decorative elements. The emotional response is one of calm reliability and technological sophistication.

## Colors
The palette is rooted in "Medical Blue" tones to reinforce trust and hygiene. 
- **Primary & Secondary:** Used for high-emphasis actions, active states, and brand touchpoints.
- **Surface Strategy:** We use a layered background approach. The main canvas is a cool, desaturated blue-gray (#F4F7FA), while interactive surfaces and cards use pure White (#FFFFFF) to create a clear "lift" from the page.
- **Semantic Logic:** Status colors follow industry standards but are slightly desaturated to maintain the premium feel. Red and Orange are reserved strictly for clinical alerts and critical system errors to prevent "alert fatigue."
- **Typography:** Deep Charcoal (#111827) provides maximum contrast for legibility, while Slate (#667085) is used for secondary metadata.

## Typography
The typographic system utilizes a dual-font approach. **Manrope** is used for headings and high-impact KPIs to provide a modern, rounded, and tech-forward character. **Inter** is used for all body copy and UI labels due to its exceptional legibility in data-heavy tables and forms.

- **KPIs:** Use `display-kpi` for executive dashboards to highlight patient counts or revenue metrics.
- **Labels:** Use `label-md` for table headers and muted metadata, always with a slightly increased letter spacing for clarity at small sizes.
- **Mobile Adaptation:** Headlines scale down significantly on mobile to ensure patient names and medical records remain readable without excessive wrapping.

## Layout & Spacing
This design system employs a **12-column fixed-grid** for desktop (max-width 1440px) to ensure consistent data visualization layouts. 

- **Vertical Rhythm:** A strict 8px baseline grid governs all spacing. 
- **The "Breathable" Rule:** For enterprise SaaS, we intentionally increase margins and gutters (24px) to prevent the "cluttered dashboard" effect typical of legacy healthcare software.
- **Breakpoints:** 
    - **Desktop (1024px+):** 12 columns, 40px side margins.
    - **Tablet (768px-1023px):** 8 columns, 24px side margins.
    - **Mobile (<767px):** 4 columns, 16px side margins.

## Elevation & Depth
Depth is conveyed through **Tonal Layers** and **Ambient Shadows**. This system avoids heavy borders in favor of soft shadows that suggest a physical stack of papers.

- **Level 0 (Background):** #F4F7FA. Lowest layer.
- **Level 1 (Cards/Surfaces):** White (#FFFFFF) with a `0px 4px 20px rgba(0, 0, 0, 0.03)` shadow and a 1px border of #EEF3F7.
- **Level 2 (Dropdowns/Modals):** White (#FFFFFF) with a more pronounced `0px 12px 32px rgba(0, 0, 0, 0.08)` shadow to indicate temporary overlay and high priority.
- **Interactions:** Hovering over a card should slightly deepen the shadow and move the element -2px on the Y-axis to provide tactile feedback.

## Shapes
Shapes are defined by "Soft-Professional" curves. 
- **Standard UI (Inputs/Buttons):** 0.5rem (8px) roundedness provides a modern, friendly feel.
- **Feature Cards:** Use `rounded-lg` (16px) or `rounded-xl` (24px) for large dashboard containers to create a softer, high-fidelity appearance.
- **Navigation Pills:** Use a full "Pill" shape (9999px) for active states in the top navigation and status tags (Chips).

## Components
- **Top Navigation:** A horizontal bar with a white background. Active items are represented by a dark (#111827) pill-shaped container with white text.
- **Buttons:**
    - *Primary:* Pill-shaped, Primary Blue (#3B82F6) background, white text.
    - *Secondary:* Pill-shaped, white background, #EEF3F7 border, #111827 text.
- **Cards:** The core of the system. 16px–20px corner radius, 32px internal padding. Title in `headline-sm`, content in `body-md`.
- **Inputs:** Soft-rectangular (8px radius), 1px border (#D1D5DB). Active state uses a 2px Primary Blue focus ring with a soft glow.
- **Chips/Status:** Pill-shaped, using a light tint of the status color for the background (e.g., Success background: #DCFCE7) and the dark status color for text.
- **Icons:** Use Lucide or similar 2px stroke-width icons. Icons should be monochrome (#667085) unless they are part of a status indicator or primary action.
- **Data Viz:** Use Primary and Deep Blue for primary data series. Use thin, light-gray gridlines (#F1F5F9). Hide axes where possible for a cleaner "executive" look.