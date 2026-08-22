---
name: Clinical Precision Mobile
colors:
  surface: '#f9f9ff'
  surface-dim: '#d0daf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3fd'
  surface-container: '#e8eeff'
  surface-container-high: '#e6e7f2'
  surface-container-highest: '#e1e2ec'
  on-surface: '#191b23'
  on-surface-variant: '#424754'
  inverse-surface: '#2e3038'
  inverse-on-surface: '#eff0fa'
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
  secondary-container: '#346cef'
  on-secondary-container: '#fefcff'
  tertiary: '#924700'
  on-tertiary: '#ffffff'
  tertiary-container: '#b75b00'
  on-tertiary-container: '#fffbff'
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
  on-secondary-fixed-variant: '#003ea7'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb786'
  on-tertiary-fixed: '#311400'
  on-tertiary-fixed-variant: '#723600'
  background: '#f9f9ff'
  on-background: '#191b23'
  surface-variant: '#e1e2ec'
  success-container: '#dcfce7'
  success-on-container: '#166534'
typography:
  display-kpi:
    fontFamily: Manrope
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 26px
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
    fontWeight: '600'
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
  touch-target: 44px
  margin-mobile: 1.25rem
  gutter-sm: 1rem
  stack-xs: 0.5rem
  stack-sm: 1rem
  stack-md: 1.5rem
  stack-lg: 2.5rem
---

## Brand & Style

The design system for the mobile patient application is a refined extension of the "Clinical Precision" enterprise dashboard, adapted for the personal, high-trust environment of a patient's own device. The brand personality is **Empathetic Accuracy**—combining the authoritative reliability of clinical software with a warm, accessible interface that empowers patients to manage their health.

The design style follows a **Corporate / Modern** aesthetic with a strong emphasis on **Minimalism** and **Tactile** feedback. The interface utilizes generous whitespace to reduce cognitive load during potentially stressful health management tasks. It maintains a "White-Space First" philosophy, ensuring that health metrics and appointment details are the primary focus, presented on clean, elevated surfaces that feel both technologically sophisticated and approachable.

## Colors

The mobile palette maintains the "Medical Blue" foundation to reinforce the connection to the enterprise dashboard while ensuring high visibility on mobile screens.

- **Primary Blue (#3b82f6):** Reserved for the most critical patient actions—booking appointments, viewing results, and primary navigation.
- **Surface Strategy:** The mobile app uses a layered approach to create a sense of hierarchy on smaller screens. The main background uses a very light cool-gray (`#f9f9ff`), while primary content sits on white containers (`#ffffff`) to provide maximum "lift" and clarity.
- **High-Contrast Metrics:** For health data (heart rate, blood pressure), deep charcoal (`#111c2d`) is used for text to ensure readability for users with varying visual acuity.
- **Semantic Feedback:** Status colors (Success/Error) are utilized for health goal tracking and alerts. These are used sparingly to avoid "alert fatigue," following the desaturated premium tone of the enterprise system.

## Typography

This design system employs a dual-font strategy to balance character with utility. **Manrope** provides a rounded, modern feel for patient-facing headings and health metrics. **Inter** is used for all functional body copy and medical instructions due to its superior legibility.

For the mobile application, typography has been optimized for touch-scale and readability:
- **KPI Display:** Used for high-impact numbers like daily steps or glucose levels.
- **Weighting:** Headings are slightly heavier than the desktop counterpart to ensure they stand out against mobile backgrounds.
- **Readability:** Body text maintains a 16px minimum (`body-md`) for medical instructions to ensure accessibility for all age groups.

## Layout & Spacing

The mobile layout transition from a 12-column grid to a **4-column fluid grid** for smartphone devices. The spacing philosophy is built around a strict 8px base unit to maintain a rigorous vertical rhythm.

- **Touch-First Design:** All interactive elements maintain a minimum hit area of 44x44px. 
- **Safe Zones:** Content is inset by a 20px (`margin-mobile`) side margin to ensure it does not hit the edge of modern bezel-less screens.
- **Vertical Stack:** We use a generous 24px (`stack-md`) spacing between content cards to allow the UI to "breathe" and prevent the screen from feeling cluttered with medical data.
- **Density:** While the enterprise dashboard is dense, the mobile app prioritizes single-column flows to guide the patient through one task at a time.

## Elevation & Depth

Depth is used strategically to signify interactivity and priority, mirroring the enterprise system's use of **Tonal Layers** and **Ambient Shadows**.

- **Level 0 (App Canvas):** The base background layer is `#f9f9ff`.
- **Level 1 (Patient Cards):** All primary content (appointment cards, health charts) uses a white background with a subtle ambient shadow: `0px 2px 12px rgba(0, 0, 0, 0.04)`.
- **Level 2 (Modals & Action Sheets):** Overlays use a more pronounced shadow `0px 8px 24px rgba(0, 0, 0, 0.12)` to pull focus to the interaction and indicate a temporary state.
- **Interactive States:** Buttons and cards do not use heavy borders. Instead, a slight elevation increase or a subtle 1px inner stroke is used to provide tactile feedback upon tapping.

## Shapes

The shape language utilizes "Rounded" (Level 2) geometry to soften the clinical nature of the application and make it feel more lifestyle-oriented.

- **Standard Elements:** Buttons and input fields use a 0.5rem (8px) radius for a modern, professional look.
- **Container Cards:** Health metric containers and appointment summaries use `rounded-lg` (1.0rem) to create a friendly, distinct visual "chunking" of information.
- **Status Tags:** Chips and active navigation states use pill-shaped (9999px) geometry for clear distinction from structural elements.

## Components

- **Primary Buttons:** High-visibility Primary Blue (#3b82f6) with 16px vertical padding. Text is centered in `body-md` (Medium weight).
- **Patient Cards:** The primary vessel for data. Features 16px internal padding, a 1.0rem corner radius, and uses `headline-sm` for titles.
- **Health Inputs:** Large, clear input fields with 1px `#c2c6d6` borders. On focus, they transition to a 2px Primary Blue border with a soft glow to guide the user's attention.
- **Bottom Navigation:** A persistent bar using a blur effect (Glassmorphism Lite) with 24px monochrome icons. The active state is indicated by a subtle blue dot or a Primary Blue icon.
- **Status Chips:** Small pill-shaped indicators for "Scheduled," "Completed," or "High" health alerts. They use low-saturation backgrounds with high-contrast text (e.g., Success: Green background #dcfce7 / Green text #166534).
- **Health Charts:** Simplified sparklines and bar charts using Primary Blue. Axes are minimized to focus on the trend rather than granular grid lines.