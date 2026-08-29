---
name: SmartIDE Design System
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#c0c6d8'
  on-tertiary: '#2a303e'
  tertiary-container: '#8a91a1'
  on-tertiary-container: '#232a37'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#dce2f5'
  tertiary-fixed-dim: '#c0c6d8'
  on-tertiary-fixed: '#151c29'
  on-tertiary-fixed-variant: '#404756'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
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
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
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
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 80px
  gutter: 20px
  container-max: 1280px
---

## Brand & Style
The design system is engineered for high-performance software development environments. It balances the high-density information requirements of an IDE with a premium, modern aesthetic. The style is a hybrid of **Corporate Modern** and **Glassmorphism**, emphasizing precision, technical capability, and "dark mode first" workflows.

The visual narrative focuses on "The Flow State." By utilizing deep backgrounds and vibrant accents, the UI recedes to let the code and logic take center stage. High-fidelity touches like subtle backdrop blurs and micro-gradients provide a sense of depth and quality that distinguishes it from standard utilitarian editors.

- **Target Audience:** Software engineers, architects, and technical leaders.
- **Emotional Response:** Focus, empowerment, reliability, and technical sophistication.

## Colors
The palette is built on a "Deep Sea" foundation to reduce eye strain during long coding sessions.

- **Primary & Secondary:** Vibrant Blue and Purple are used for interactive states, primary actions, and syntax highlighting. They should be used sparingly to maintain focus.
- **Surface Strategy:** The background (#0B0F19) is the base layer. Surfaces (#131A27) are used for panels, sidebars, and cards to create structural hierarchy.
- **Accent Gradients:** Use a linear gradient (45deg) from Primary to Secondary for high-impact elements like "Get Started" buttons or featured cards.
- **Status Colors:** Use standard semantic reds for errors, amber for warnings, and emerald for success, but desaturate them slightly (approx 10%) to match the dark theme's vibrance.

## Typography
The typography system uses **Inter** for all UI and marketing elements due to its exceptional legibility and modern geometric feel. For all code-related content, data tables, and technical labels, **JetBrains Mono** is required to maintain the engineering focus.

- **Scale:** Use a 1.25x (Major Third) scale for marketing pages and a more compact 1.125x (Major Second) scale for the IDE interface.
- **Contrast:** Always use Text Primary (#F8FAFC) for headings. Use Text Secondary (#94A3B8) for body text and descriptive labels to establish a clear information hierarchy.
- **Mobile:** For screens narrower than 768px, `display-lg` should scale down to 36px.

## Layout & Spacing
The design system utilizes a **4px baseline grid** to ensure mathematical alignment across complex IDE panels.

- **Desktop Layout:** A 12-column fluid grid for marketing pages. For the application UI, use a flexible "Dock" system with fixed-width sidebars (default 240px) and a fluid central editor.
- **Margins:** 24px (lg) on desktop, 16px (md) on tablet, and 12px on mobile.
- **Density:** The IDE interface should use "Compact" spacing (8px-12px) for list items and tree views to maximize data visibility. Marketing pages should use "Spacious" spacing (40px-80px) to evoke a premium feel.

## Elevation & Depth
This design system uses a combination of **Tonal Layers** and **Glassmorphism** to define depth.

- **Layer 0 (Background):** #0B0F19. The base "canvas."
- **Layer 1 (Panels):** #131A27. Used for sidebars and top navigation. No shadow, defined by a 1px border (#1E293B).
- **Layer 2 (Cards/Modals):** Glassmorphic surfaces. Use 20% opacity of #131A27 with a 12px backdrop-filter (blur). 
- **Shadows:** Use large, ultra-soft shadows for floating elements. 
  - *Token:* `0 20px 40px rgba(0, 0, 0, 0.4)`.
- **Borders:** Every elevated element must have a 1px "inner-glow" border using #FFFFFF at 10% opacity to catch light and define edges in the dark environment.

## Shapes
The shape language is **Soft (0.25rem)**, reflecting the precision of engineering tools.

- **Buttons & Inputs:** Use the 4px (0.25rem) default radius.
- **Cards & Modals:** Use 8px (0.5rem) to provide a slightly friendlier feel for larger containers.
- **Active Indicators:** Tabs and selection highlights should use a 2px radius or remain sharp to indicate "system-level" precision.

## Components
- **Buttons:** 
  - *Primary:* Gradient (Primary to Secondary), white text, 4px radius. 
  - *Ghost:* No background, 1px border (#1E293B), transitions to Surface on hover.
- **Input Fields:** Background #0B0F19, 1px border #1E293B. On focus, the border glows with the Primary color and a 4px soft outer shadow.
- **Glassmorphic Cards:** Applied to feature highlights. Includes a 12px blur, a subtle 1px border, and a 5% white overlay to create a "frosted" effect over the deep navy background.
- **Sleek Nav Bar:** Fixed at the top, #0B0F19 at 80% opacity with backdrop-blur (16px). Uses Text Secondary for links, switching to Primary and a bottom 2px gradient line for active states.
- **Chips:** Monospaced font (JetBrains Mono), 2px radius, background #1E293B, used for language tags (e.g., "Python", "Rust").
- **Code Block:** Background #131A27, custom syntax highlighting using the Primary, Secondary, and Emerald hues. Includes a "Copy" button appearing only on hover.