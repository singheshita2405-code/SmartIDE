# SmartIDE Frontend — Complete Code Documentation

> This document explains **every file, every folder, every function, every CSS class, and every JavaScript feature** of the SmartIDE software portal frontend. Everything here is taken directly from the actual project code — nothing is assumed or made up.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Folder and File Structure](#2-folder-and-file-structure)
3. [Design System and Color Palette](#3-design-system-and-color-palette)
4. [Shared Assets — static/style.css](#4-shared-assets--staticstylecss)
5. [Page-by-Page Breakdown](#5-page-by-page-breakdown)
   - [home.html](#51-homehtml)
   - [dashboard.html](#52-dashboardhtml)
   - [login.html](#53-loginhtml)
   - [register.html](#54-registerhtml)
   - [about.html](#55-abouthtml)
   - [features.html](#56-featureshtml)
   - [downloads.html](#57-downloadshtml)
   - [documentation.html](#58-documentationhtml)
6. [How All Files Connect Together](#6-how-all-files-connect-together)
7. [User Flow and Navigation](#7-user-flow-and-navigation)
8. [JavaScript Functions Reference](#8-javascript-functions-reference)
9. [CSS Classes Reference](#9-css-classes-reference)
10. [Backend API Calls from Frontend](#10-backend-api-calls-from-frontend)

---

## 1. Project Overview

SmartIDE is a **Python Flask web application** that acts as both a marketing/information website and a functional browser-based IDE. The frontend is built with:

- **HTML** — structure of every page (Jinja2 template syntax used for Flask dynamic rendering)
- **CSS (Vanilla)** — all styles are written directly inside each HTML file's `<style>` block, plus a shared `static/style.css`
- **JavaScript (Vanilla)** — all interactivity and API calls are written in `<script>` blocks inside HTML files
- **Google Fonts** — `Inter` (main UI font) and `JetBrains Mono` (code/terminal font)
- **Google Material Symbols** — icon library loaded via CDN

---

## 2. Folder and File Structure

```
smartide_software_portal/
|
|-- app.py                          <- Flask backend (Python)
|-- READ.md                         <- This documentation file
|
|-- static/                         <- Public static files served directly
|   |-- style.css                   <- Global shared CSS (design tokens, mascot, toast)
|   |-- images/                     <- All image assets
|       |-- pixel_mascot.svg        <- The floating pixel mascot (SVG)
|       |-- smartidelogo.png        <- SmartIDE brand logo
|       |-- home.png                <- Screenshot of the home page
|       |-- about.png               <- Screenshot of the about page
|       |-- features.png            <- Screenshot of the features page
|       |-- documentation.png       <- Screenshot of documentation
|       |-- donwloads.png           <- Screenshot of downloads page
|       |-- ai_assistant.png        <- AI assistant image
|       |-- blog.png                <- Blog section image
|       |-- community.png           <- Community section image
|       |-- contact.png             <- Contact section image
|       |-- roadmap.png             <- Roadmap section image
|
|-- templates/                      <- All HTML pages (Jinja2 templates)
|   |-- home.html                   <- Landing/marketing home page
|   |-- dashboard.html              <- The full browser-based IDE workspace
|   |-- login.html                  <- Sign-in page
|   |-- register.html               <- Account creation page
|   |-- about.html                  <- About SmartIDE page (dark theme)
|   |-- features.html               <- Product features showcase
|   |-- downloads.html              <- Download page (Windows / macOS / Linux)
|   |-- documentation.html         <- Full documentation with sidebar
|
|-- smartide_design_system/
|   |-- DESIGN.md                   <- Design system reference (color palette, theme specs)
|
|-- instance/                       <- Flask instance folder (database lives here)
|-- workspace/                      <- The actual workspace files users edit in the IDE
```

---

## 3. Design System and Color Palette

The entire frontend uses a consistent **Peach & White / Peach & Black** design system. All color values come from CSS custom properties (`--variables`) defined in every page's `<style>` block.

### Peach Color Scale

| Variable | Hex Value | Usage |
|---|---|---|
| `--peach-50` | `#fff9f5` | Lightest background tints |
| `--peach-100` | `#fff0e6` | Input backgrounds, hover backgrounds |
| `--peach-200` | `#ffe4d2` | Subtle fills, badges |
| `--peach-300` | `#ffcfb2` | Modal borders, light accents |
| `--peach-400` | `#ffa574` | Scrollbar, arrows, borders on hover |
| `--peach-500` | `#ff7836` | Primary accent, buttons, active states |
| `--peach-600` | `#f05a18` | CTA buttons, active nav links, icons |
| `--peach-700` | `#d64508` | Active tab text, deepest peach |
| `--coral` | `#ff6565` | Error or close-button accent |

### Text Colors

| Variable | Hex Value | Usage |
|---|---|---|
| `--text-dark` | `#2b1810` | Main body text (light theme) |
| `--text-medium` | `#613c2c` | Secondary text, labels |
| `--text-light` | `#946956` | Muted text, placeholders |

### Theme Modes

- **Light Mode (Peach & White)** — Used in `home.html`, `features.html`, `downloads.html`, `login.html`, `register.html`. Background is warm ivory `#fffdfb`.
- **Dark Mode (Peach & Black)** — Used in `about.html` and `documentation.html`. Background is near-black `#0e0c0d` or `#0f0a07`.
- **Desktop IDE Mode** — Used in `dashboard.html`. A hybrid — white editor area, peach sidebars and titlebar.

---

## 4. Shared Assets — `static/style.css`

**File:** `static/style.css` (167 lines)

This is the **only globally shared CSS file**. All pages load it via:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### What it contains:

#### CSS Custom Properties (`:root`)
Defines the same peach palette and light/dark theme variables that are also repeated inside each template's `<style>` block. This serves as the base token set.

#### Global Reset
```css
* { box-sizing: border-box; margin: 0; padding: 0; }
```
Removes all default browser margins, padding, and switches to `border-box` sizing.

#### Body Font
```css
body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
code, pre, .font-mono { font-family: 'JetBrains Mono', Consolas, Monaco, monospace; }
```

#### Custom Scrollbar
Makes the browser scrollbar peach-colored on webkit browsers (Chrome, Edge):
```css
::-webkit-scrollbar-thumb { background: var(--peach-400); border-radius: 4px; }
```

#### Floating Pixel Mascot (`.floating-mascot-container`)
Every page shows a floating pixel mascot (`pixel_mascot.svg`). This class controls its behaviour:
- `position: fixed` — stays on screen as you scroll
- `pointer-events: auto` — you can hover and click on it
- `transition: transform 0.3s cubic-bezier(...)` — springy bounce animation on hover
- `.floating-mascot-img` — applies a `floatMascot` keyframe animation that makes it gently bob up and down
- `.mascot-speech-bubble` — a tooltip that appears above the mascot on hover, with a CSS triangle arrow at the bottom

Two position classes:
- `.floating-mascot-top-right` — top: 90px, right: 28px (used on most pages)
- `.floating-mascot-bottom-left` — bottom: 30px, left: 28px (used on about page as second mascot)

#### Keyframe Animations in style.css
```css
@keyframes floatMascot { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px) rotate(-3deg); } ... }
@keyframes pulseGlow { ... }   /* Orange glow pulse */
@keyframes slideUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
```

#### Toast Notification (`.toast-msg`)
A fixed bottom-right notification component styled with peach border and shadow. Uses `slideUp` animation when displayed.

---

## 5. Page-by-Page Breakdown

---

### 5.1 `home.html`

**File:** `templates/home.html` — 1,319 lines  
**URL Route:** `/`  
**Theme:** Light — Peach & White

#### Purpose
The main landing/marketing page. Introduces SmartIDE, shows the three OS download buttons, displays an interactive IDE mockup, and lists key features.

---

#### HTML Structure (top-level sections)

| HTML Element | CSS Class / ID | What it Is |
|---|---|---|
| `<div class="bg-animated">` | `.bg-animated`, `.bg-blob` | Fixed animated background with 3 floating blobs |
| `<header>` | `.header-inner`, `.logo`, `nav` | Fixed top navigation bar |
| `<div class="floating-mascot-container">` | `.floating-mascot-top-right` | The pixel mascot (top-right) |
| `<section class="hero">` | `.hero`, `.pill-badge`, `.launch-downloads` | Hero text + 3 download buttons |
| `<div class="mockup-container">` | `.ide-window` | Interactive IDE mockup |
| `<section class="features-section">` | `.features-grid`, `.feat-card` | 6 feature cards |
| `<div class="modal-overlay">` | `#downloadModal` | Download confirmation modal popup |
| `<footer>` | `.footer-grid`, `.foot-col` | Footer with links |

---

#### Key CSS in `home.html`

**Background Animated Blobs:**
Three large, soft-blurred circles that slowly float using the `blobFloat` keyframe.
```css
.bg-blob { position: absolute; border-radius: 50%; filter: blur(90px); animation: blobFloat 12s ease-in-out infinite; }
.blob-1  { width: 600px; background: radial-gradient(circle, #ffcfb2, #ffa574); top: -200px; left: -150px; }
```

**Navigation Bar:**
Fixed header with glass-blur effect. Nav links have an animated peach underline that slides in on hover using `transform: scaleX(0) to scaleX(1)`.
```css
header { position: fixed; top: 0; width: 100%; backdrop-filter: blur(20px); }
```

**Logo Text (gradient):**
```css
.logo-text { background: linear-gradient(135deg, #d64508, #ff7836); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
```

**Download Buttons Grid (`.dl-buttons-grid`):**
Three OS download buttons in a 3-column grid. Each `.os-btn` has:
- A colored icon box (blue for Windows, grey for macOS, orange for Linux)
- A peach gradient top bar that slides in on hover (`::before` pseudo-element)
- A right arrow icon that shifts on hover

**IDE Mockup — inner elements:**

| CSS Class | Element Role |
|---|---|
| `.ide-titlebar` | Top bar with red/yellow/green traffic light dots |
| `.ide-activity` | Left vertical icon rail (Explorer, Search, AI, Settings) |
| `.ide-explorer` | File tree panel showing `main.py`, `calculator.py`, `welcome.txt` |
| `.ide-tabs` | Tab bar above the editor |
| `.ide-gutters` | Line numbers column |
| `.ide-code-view` | Syntax-highlighted code content area |
| `.ide-terminal` | Bottom terminal/output drawer |

**Syntax Highlighting Classes (applied on `<span>` tags inside `.ide-code-view`):**
```css
.kw  { color: #d64508; font-weight: 600; }   /* def, return, if, for, class */
.fn  { color: #d97706; }                       /* function names */
.str { color: #15803d; }                       /* string literals */
.cm  { color: #946956; font-style: italic; }  /* comments */
.num { color: #0284c7; }                       /* numbers */
```

**Feature Cards (`.feat-card`):**
```css
.feat-card:hover { border-color: var(--peach-400); transform: translateY(-6px); box-shadow: 0 16px 40px rgba(240, 90, 24, 0.12); }
```
Cards lift 6px with a stronger peach shadow on hover.

**Download Modal (`.modal-overlay`):**
```css
.modal-overlay { display: none; position: fixed; inset: 0; z-index: 1000; backdrop-filter: blur(8px); }
```
Hidden by default, shown by JavaScript when a download button is clicked.

---

#### JavaScript in `home.html`

**`triggerDownloadModal(osName, filename)`**  
Called via `onclick` on each OS download button.  
- Updates `#modalTitle` (e.g. "Downloading for Windows")
- Updates `#modalSub` with the filename
- Sets `#modalDirectLink` href to the correct `/download/platform` URL
- Sets `#downloadModal` to `display: 'flex'` to show it

**`closeDownloadModal()`**  
Sets `#downloadModal` display back to `'none'`.

**`demoFiles` object**  
A JavaScript object with 3 keys: `main`, `calc`, `welcome`. Each contains:
```js
{
  title: 'main.py',
  lines: 11,
  code: `...HTML with syntax highlighted spans...`,
  output: `$ python main.py<br>...`
}
```

**`switchPreview(key)`**  
Called when a file name is clicked in the mockup file explorer.
- Reads the matching entry from `demoFiles`
- Updates `#tabTitle`, `#codeView`, and `#termOutput` innerHTML
- Rebuilds line numbers in `#gutters` by looping from 1 to `item.lines`
- Removes `.active` from all `.exp-file` elements, adds to the clicked one

**`runDemo()`**  
Called by the "Run in Terminal" button.
- Shows "Running active script..." in orange
- After 400ms (setTimeout), shows "[Execution completed successfully in 0.04s]"

---

#### Jinja2 / Flask Template Tags Used

```html
{{ url_for('home') }}
{{ url_for('about') }}
{{ url_for('download_platform', platform='windows') }}
{% if session.get('user_name') %}
  {{ session['user_name'] }}
{% else %}
  ...Sign In / Get Started buttons...
{% endif %}
```

---

### 5.2 `dashboard.html`

**File:** `templates/dashboard.html` — 1,212 lines  
**URL Route:** `/dashboard`  
**Theme:** Desktop IDE — white editor with peach accent panels

#### Purpose
The most complex page. This is the **full browser-based IDE** where users write and run Python code. It looks and behaves like a real desktop IDE application.

---

#### HTML Structure

| Layer | Element / ID | Description |
|---|---|---|
| Title Bar | `.desktop-titlebar` | Top bar with traffic dots, window title, Save/Run/About/Home/Docs buttons |
| Menu Bar | `.desktop-menubar` | File, Edit, View, Run, Terminal, Help menus |
| Workspace | `.workspace-layout` | Main flex container |
| Activity Bar | `.activity-bar` | Left icon rail |
| Sidebar Panel | `.side-panel` | File tree or AI panel |
| Editor | `.editor-container` | Tab bar + code textarea + bottom terminal |
| Status Bar | `.status-bar` | Bottom bar showing Git branch, position, Python version |
| About Dialog | `#aboutDialog` | Modal popup for app info |

---

#### Key CSS in `dashboard.html`

**Full-screen layout (fills viewport like a desktop app):**
```css
html, body { height: 100%; width: 100%; overflow: hidden; display: flex; flex-direction: column; }
.workspace-layout { flex: 1; display: flex; overflow: hidden; }
```

**Traffic Light Dots:**
```css
.dot-close { background: #ff5f56; }   /* clicking navigates to / */
.dot-min   { background: #ffbd2e; }
.dot-max   { background: #27c93f; }   /* clicking toggles fullscreen */
```

**Menu Bar Dropdowns:**
```css
.dropdown-menu           { display: none; }
.menu-item.active .dropdown-menu { display: block; }
```

**Active File in Sidebar:**
```css
.tree-item.active { background: #ffe3d1; border-left: 3px solid var(--peach-600); }
```

**Dirty (Unsaved) File Dot:**
```css
.dirty-dot          { display: none; background: var(--peach-500); }
.tab.dirty .dirty-dot { display: inline-block; }
```

**Code Editor:**
```css
.code-textarea { font-family: 'JetBrains Mono', monospace; font-size: 13.5px; line-height: 22px; white-space: pre; tab-size: 4; }
```

**Status Bar (peach gradient):**
```css
.status-bar { height: 24px; background: linear-gradient(90deg, #f05a18, #ff7836); color: #ffffff; }
```

---

#### JavaScript Variables (State)

```js
let currentFile = 'main.py';     // Currently open file name
let openTabs    = ['main.py'];    // Array of all open tab filenames
let dirtyFiles  = new Set();      // Set of filenames with unsaved changes
let filesCache  = {};             // { filename: content } — in-memory cache
```

#### JavaScript DOM References

```js
const codeEditor     = document.getElementById('codeEditor');
const lineGutter     = document.getElementById('lineGutter');
const posIndicator   = document.getElementById('posIndicator');
const terminalOutput = document.getElementById('terminalOutput');
const termInput      = document.getElementById('termCommandInput');
```

---

#### JavaScript Functions in `dashboard.html`

**`DOMContentLoaded` init block:**
1. Calls `loadWorkspaceFiles()` and `openFile('main.py')`
2. Attaches `input` listener: updates line numbers + marks file dirty
3. Attaches `keyup` / `click` listeners: updates cursor position
4. Attaches `keydown` listener: Tab key inserts 4 spaces, Ctrl+S triggers save
5. Global `click` listener: closes menus when clicking outside

**`updateCursorPos()`**  
Counts `\n` characters before `selectionStart` to get line and column number. Updates `posIndicator` text ("Ln X, Col Y").

**`updateLineNumbers()`**  
Counts newlines in `codeEditor.value`, builds `"1\n2\n3..."` string, sets as `lineGutter.textContent`.

**`toggleMenu(id)`**  
Calls `closeAllMenus()` first, then adds `.active` to the clicked menu item.

**`closeAllMenus()`**  
Removes `.active` from all `.menu-item` elements.

**`switchSideView(view)`**  
Hides both `#viewExplorer` and `#viewAI`, then shows the requested one and activates its activity bar icon.

**`loadWorkspaceFiles()`** *(async)*  
`GET /api/files` → calls `renderFileTree(data.files)` on success.

**`renderFileTree(files)`**  
Creates `.tree-item` divs with file icons, click handlers, and delete buttons. `main.py` has no delete button (protected).

**`openFile(filename)`** *(async)*  
`POST /api/get-file` with `{ filename }` → loads content into `codeEditor.value`, adds to `openTabs`, updates title bar, calls `renderTabs()` and `updateLineNumbers()`.

**`renderTabs()`**  
Clears `#tabBar` and renders one tab per file in `openTabs`. Active and dirty states applied via CSS classes.

**`closeTab(e, file)`**  
Removes file from `openTabs`, ensures `main.py` always remains, opens the last remaining tab if needed.

**`saveActiveFile()`** *(async)*  
`POST /api/save-file` with `{ filename, content }` → on success removes from `dirtyFiles`, appends save confirmation to terminal.

**`promptNewFile()`** *(async)*  
`prompt()` dialog for filename → `POST /api/new-file` → refreshes tree and opens new file.

**`deleteWorkspaceFile(e, name)`** *(async)*  
`confirm()` → `POST /api/delete-file` → calls `closeTab()` and refreshes tree.

**`executeCurrentCode()`** *(async)*  
Saves file, then `POST /run-code` → appends Python output and exit code to terminal.

**`handleTermInput(e)`**  
Listens for Enter key on terminal input. Reads command and calls `executeCommand(cmd)`.

**`executeCommand(cmd)`**  
Routes commands:
- `clear` → `clearTerminal()`
- `help` → prints command list
- `ls` / `dir` → fetches file list from `/api/files` and prints names + sizes
- `python <file>` → calls `/run-code` for that file
- `date` → prints `new Date().toString()`
- Anything else → sends to `/run-code` as raw Python expression

**`appendTerminal(text)`**  
`terminalOutput.textContent += text` then auto-scrolls to bottom.

**`clearTerminal()`**  
Resets terminal to `"$ "`.

**`toggleBottomPanel()`**  
Shows or hides the `#bottomPanel` terminal drawer.

**`switchPanelTab(tab)`**  
Switches active state between TERMINAL and OUTPUT tab labels.

**`askAI(promptText)`** *(simulated)*  
Shows a thinking message, then after 400ms shows a hardcoded response based on whether prompt contains "Explain", "bugs", or other text.

**`showAboutDialog()` / `hideAboutDialog()`**  
Shows or hides the `#aboutDialog` modal overlay.

**`toggleFullScreen()`**  
Uses the browser Fullscreen API: `requestFullscreen()` or `exitFullscreen()`.

---

### 5.3 `login.html`

**File:** `templates/login.html` — 392 lines  
**URL Route:** `/login`  
**Theme:** Split-screen — left peach gradient panel, right white form

#### Layout
Body is `display: flex`, creating a **two-column layout**:
- **Left (`.left-panel`)** — 50% width: logo, mini IDE mockup showing `auth_session.py`, tagline
- **Right (`.right-panel`)** — 50% width: the actual login form

On screens under 900px, the left panel is hidden and the form takes full width.

#### Flash Messages (Flask)
```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% for category, message in messages %}
    <div class="flash-msg flash-{{ category }}">{{ message }}</div>
  {% endfor %}
{% endwith %}
```
Shows `.flash-error` (red) or `.flash-success` (green) messages sent from Flask.

#### Login Form
```html
<form method="POST" action="{{ url_for('login') }}">
  <input type="email"    id="email"    name="email"    required autofocus>
  <input type="password" id="password" name="password" required>
  <button type="submit" class="btn-submit">Sign In to SmartIDE</button>
</form>
```
Each input has a Material Symbol icon inside using absolute positioning within `.input-wrap`.

A "Continue as Guest" link navigates directly to `/dashboard` without authentication.

---

### 5.4 `register.html`

**File:** `templates/register.html` — 410 lines  
**URL Route:** `/register`  
**Theme:** Same split-screen layout as login

#### Differences from Login
- Left panel shows `create_profile.py` themed IDE mockup
- Form has **4 fields**: Full Name, Email, Password, Confirm Password
- Submit button says "Create SmartIDE Account"

#### Form Fields
```html
<input type="text"     id="name"             name="name">
<input type="email"    id="email"            name="email">
<input type="password" id="password"         name="password">
<input type="password" id="confirm_password" name="confirm_password">
```
All submitted as `POST` to `/register`. Password validation happens on the Flask backend.

---

### 5.5 `about.html`

**File:** `templates/about.html` — 1,078 lines  
**URL Route:** `/about`  
**Theme:** Dark — Peach & Black

Only major public page with a **dark theme**:
```css
--bg-dark: #0e0c0d;    --card-dark: #191417;
--text-main: #fef6f2;  --text-muted: #d6aba0;
```

#### Two Floating Mascots
Unlike other pages, `about.html` uses two mascots:
- Top-right: "Hi! Welcome to About SmartIDE 🍑"
- Bottom-left: "Peach & Black Theme Active! ⚡"

#### Sections in Order
1. **Hero** — large gradient headline + two call-to-action buttons
2. **Intro Grid** — 2-column `.intro-card` dark cards
3. **Key Features** — 3-column `.feature-card` grid with peach top-bar hover animation
4. **Tech Stack** — 4-column `.tech-item` grid
5. **How it Works Timeline** — 4-column `.timeline-step` grid with numbered circles
6. **Vision Banner** — 2-column layout with vision checklist
7. **Team** — 3-column `.team-card` grid with avatar circles and roles
8. **GitHub CTA** — centered open-source call to action box
9. **Footer** — 4-column footer

#### Feature Card Hover Effect
```css
.feature-card::before { height: 3px; background: linear-gradient(90deg, #ff7836, #ffa87a); opacity: 0; }
.feature-card:hover::before { opacity: 1; }
```
A peach gradient bar fades in at the top of each card on hover.

---

### 5.6 `features.html`

**File:** `templates/features.html` — 510 lines  
**URL Route:** `/features`  
**Theme:** Light — Peach & White

#### Sections
1. **Header** — fixed nav
2. **Floating Mascot** — "Explore SmartIDE Features! 🍑"
3. **Hero (`.feat-hero`)** — "Crafted for Pure Focus" with gradient text
4. **Features Grid (`.features-container`)** — 6 feature cards in 3-column grid
5. **CTA Banner (`.cta-banner`)** — peach gradient banner with Download and Launch buttons
6. **Footer** — 4-column footer

#### The 6 Feature Cards

| Card Title | Material Icon |
|---|---|
| Centralized Workspace | `hub` |
| Zero-Config Environment | `school` |
| Integrated DB & Previews | `dns` |
| Unified Platform | `web` |
| Built-In Databases | `storage` |
| Rapid Live Previews | `visibility` |

#### Top-strip Hover Animation
```css
.feature-card::before { height: 3px; background: linear-gradient(90deg, #ffa574, #f05a18); transform: scaleX(0); }
.feature-card:hover::before { transform: scaleX(1); }
```

#### Session-based Nav (Jinja2)
```html
{% if session.get('user_name') %}
  <a>{{ session['user_name'] }}</a>  <a>Sign Out</a>
{% else %}
  <a>Sign In</a>  <a>Get Started</a>
{% endif %}
```
Header buttons change based on login state.

---

### 5.7 `downloads.html`

**File:** `templates/downloads.html` — 595 lines  
**URL Route:** `/downloads`  
**Theme:** Light — Peach & White

#### Sections
1. **Header** — fixed nav
2. **Floating Mascot** — "Download SmartIDE Desktop! 🍑"
3. **Hero (`.dl-hero`)** — version chip + heading "Download for Your Platform"
4. **Download Cards Grid (`.dl-grid`)** — 3 platform download cards
5. **System Requirements Table (`.specs-section`)** — compatibility table
6. **Footer** — 4-column footer

#### Three Download Cards
Each `.dl-card` has a modifier class (`.win`, `.mac`, `.linux`) for colored icon boxes:
- `.dl-card.win` — blue gradient icon, `window` icon
- `.dl-card.mac` — grey gradient icon, `desktop_mac` icon
- `.dl-card.linux` — orange gradient icon, `terminal` icon

Contents per card:
- 72×72px platform icon
- `<h2>` platform name
- `.dl-desc` description paragraph
- `.dl-main-btn` — full-width download button linking to `/download/platform`
- `.dl-alt-options` — alternative formats and file size info

#### Card Hover
```css
.dl-card:hover { border-color: var(--peach-400); transform: translateY(-8px); box-shadow: 0 20px 50px ...; }
```

#### System Requirements Table
An HTML `<table class="specs-table">` showing Platform, Min OS, RAM, Storage, Package Type for Windows, macOS, and Linux.

---

### 5.8 `documentation.html`

**File:** `templates/documentation.html` — 808 lines  
**URL Route:** `/documentation`  
**Theme:** Dark — Peach & Brown-Black  
Variables: `--bg-base: #0f0a07`, `--text-primary: #f0e8e0`

#### Two-Column Layout
```css
.doc-layout { display: flex; margin-top: 70px; }
.doc-sidebar { width: 290px; position: fixed; top: 70px; bottom: 0; overflow-y: auto; }
.doc-content { flex: 1; margin-left: 290px; padding: 40px 60px 100px; }
```
Fixed left sidebar + scrollable main content area.

#### Sidebar Contents
- **Search box** — `#docSearch` input with `onkeyup="filterDocs()"` for live search
- **Navigation groups** (`<div class="doc-nav-group">`) linking to page anchors:
  - Getting Started: Quick Tour, Windows Setup, macOS Setup, Linux Setup
  - SmartIDE Features: 6 feature sections
  - Support: FAQ & Help

#### Documentation Sections

| Section ID | Heading |
|---|---|
| `#quickstart` | Quick Tour + Python code box |
| `#install-win` | Installing on Windows (4-step list) |
| `#install-mac` | Installing on macOS (4-step list) |
| `#install-linux` | Installing on Linux (bash code box) |
| `#centralized-workspace` | Centralized Workspace |
| `#unified-platform` | Unified Platform + bullet list |
| `#database-system` | Built-In Databases + table |
| `#live-preview` | Rapid Live Previews |
| `#monaco-editor` | Monaco Editor + bullet list |
| `#sql-console` | Integrated SQL Console |
| `#faq` | FAQ & Help |

#### Code Boxes (`.code-box`)
```html
<div class="code-box">
  <div class="code-box-header">
    <span>Python Sample</span>
    <button class="copy-btn" onclick="copySnippet(this)">Copy</button>
  </div>
  <div class="code-content">...code content...</div>
</div>
```

#### JavaScript in `documentation.html`

**`copySnippet(btn)`**  
- Traverses up to the parent `.code-box` with `btn.closest('.code-box')`
- Gets `.code-content` text
- Copies with `navigator.clipboard.writeText(content)`
- Temporarily changes button to "✓ Copied!", reverts after 2 seconds

**`filterDocs()`**  
- Gets value from `#docSearch`, lowercased
- Loops through all `.doc-section` elements
- Shows/hides each based on whether its text includes the search query

---

## 6. How All Files Connect Together

```
User visits URL
     |
     v
Flask app.py (Python backend)
     |  Renders a Jinja2 template
     v
templates/*.html
     |  Every page loads:
     |---> static/style.css         (global tokens, mascot, toast styles)
     |---> Google Fonts CDN         (Inter, JetBrains Mono)
     |---> Google Material Symbols  (icon library)
          |
          |  Each page has its own <style> block (page-specific CSS)
          |  Each page has its own <script> block (page-specific JS)
          |
          v
     dashboard.html makes fetch() calls to Flask APIs:
          |
          |---> GET  /api/files        (list workspace files)
          |---> POST /api/get-file     (read file content)
          |---> POST /api/save-file    (write content back)
          |---> POST /api/new-file     (create new file)
          |---> POST /api/delete-file  (delete a file)
          |---> POST /run-code         (execute Python, get output)
```

### How Navigation Works
Every page's `<nav>` uses `{{ url_for('route_name') }}` — Flask generates correct URLs. The active page marks its link with `class="active"` for the underline highlight.

### How Login State is Shown
Pages check `{% if session.get('user_name') %}` to show either:
- **Logged in**: username + Sign Out
- **Logged out**: Sign In + Get Started

### How the Pixel Mascot Appears on Every Page
`static/style.css` defines the `.floating-mascot-container` classes. Each template adds its own `<div class="floating-mascot-container ...">` with `pixel_mascot.svg` and a unique speech bubble message.

---

## 7. User Flow and Navigation

```
[Home Page /]
    |
    |-- Click "Download for Windows/macOS/Linux"
    |       --> Opens download modal
    |           --> Links to /download/windows (or /mac, /linux)
    |
    |-- Click "Get Started" (header)
    |       --> /register
    |           --> /login
    |               --> /dashboard
    |
    |-- Click "Sign In" (header)
    |       --> /login --> /dashboard
    |
    |-- Click "Dashboard" (header)
    |       --> /dashboard (works for guests too)
    |
    |-- Click nav "About"          --> /about
    |-- Click nav "Features"       --> /features
    |-- Click nav "Documentation"  --> /documentation
    |-- Click nav "Downloads"      --> /downloads

[Dashboard /dashboard]
    |
    |-- File Tree: click filename   --> opens file in editor
    |-- File Tree: click +          --> prompt new filename, creates file
    |-- File Tree: click x on file  --> confirm, deletes file
    |-- Tab: click filename         --> switch active file
    |-- Tab: click x on tab         --> closes tab
    |-- Click "Save" or Ctrl+S      --> saves current file to server
    |-- Click "Run" or F5           --> saves then executes Python code
    |-- Type in terminal input      --> runs commands (help, ls, date, python...)
    |-- Menu > View > AI            --> switches sidebar to AI Assistant panel
    |-- AI panel: quick buttons     --> gets simulated AI response in sidebar
    |-- Green dot in titlebar       --> toggles fullscreen mode
    |-- Red dot in titlebar         --> navigates back to /
```

---

## 8. JavaScript Functions Reference

| Function | File | What it Does |
|---|---|---|
| `triggerDownloadModal(osName, filename)` | home.html | Opens download confirmation modal with platform info |
| `closeDownloadModal()` | home.html | Closes the download modal |
| `switchPreview(key)` | home.html | Switches the IDE mockup to show a different demo file |
| `runDemo()` | home.html | Simulates running a script in the IDE mockup terminal |
| `updateCursorPos()` | dashboard.html | Updates "Ln X, Col Y" in the status bar |
| `updateLineNumbers()` | dashboard.html | Rebuilds the line number gutter based on textarea content |
| `toggleMenu(id)` | dashboard.html | Opens a menu dropdown, closes all others |
| `closeAllMenus()` | dashboard.html | Hides all dropdown menus |
| `switchSideView(view)` | dashboard.html | Switches sidebar between Explorer and AI panels |
| `loadWorkspaceFiles()` | dashboard.html | Fetches file list from `/api/files` |
| `renderFileTree(files)` | dashboard.html | Dynamically renders the file tree HTML |
| `openFile(filename)` | dashboard.html | Loads file content from server into the editor |
| `renderTabs()` | dashboard.html | Re-renders all open file tabs |
| `closeTab(e, file)` | dashboard.html | Removes a tab, opens next available |
| `saveActiveFile()` | dashboard.html | Sends editor content to `/api/save-file` |
| `promptNewFile()` | dashboard.html | Prompts for filename, creates file via `/api/new-file` |
| `deleteWorkspaceFile(e, name)` | dashboard.html | Confirms and deletes file via `/api/delete-file` |
| `executeCurrentCode()` | dashboard.html | Saves then runs current file via `/run-code` |
| `handleTermInput(e)` | dashboard.html | Handles Enter key press in terminal input box |
| `executeCommand(cmd)` | dashboard.html | Routes terminal commands to appropriate handlers |
| `appendTerminal(text)` | dashboard.html | Appends text to terminal output and auto-scrolls |
| `clearTerminal()` | dashboard.html | Resets terminal content to `"$ "` |
| `toggleBottomPanel()` | dashboard.html | Shows or hides the bottom terminal drawer |
| `switchPanelTab(tab)` | dashboard.html | Switches between TERMINAL and OUTPUT tab labels |
| `askAI(promptText)` | dashboard.html | Shows simulated AI response in sidebar panel |
| `showAboutDialog()` | dashboard.html | Shows the About info dialog |
| `hideAboutDialog()` | dashboard.html | Hides the About info dialog |
| `toggleFullScreen()` | dashboard.html | Enters or exits browser fullscreen mode |
| `copySnippet(btn)` | documentation.html | Copies code box content to clipboard, shows "Copied!" feedback |
| `filterDocs()` | documentation.html | Filters visible documentation sections by search query |

---

## 9. CSS Classes Reference

| Class | File | Description |
|---|---|---|
| `.floating-mascot-container` | style.css | Fixed-position mascot wrapper with hover spring animation |
| `.floating-mascot-img` | style.css | The SVG mascot image with floating bob animation |
| `.mascot-speech-bubble` | style.css | Tooltip bubble that appears above the mascot on hover |
| `.floating-mascot-top-right` | style.css | Positions mascot at top-right of viewport |
| `.floating-mascot-bottom-left` | style.css | Positions mascot at bottom-left of viewport |
| `.toast-msg` | style.css | Fixed bottom-right notification box |
| `.bg-animated` | multiple | Fixed full-screen background gradient layer |
| `.bg-blob` | multiple | Blurred floating decoration blob |
| `.header-inner` | multiple | Max-width centered flex container inside header |
| `.logo`, `.logo-text`, `.logo-icon` | multiple | Brand logo and gradient text components |
| `.logo-badge` | home.html, about.html | Small pill badge next to logo text |
| `.btn-cta` | multiple | Primary peach gradient call-to-action button |
| `.btn-ghost` | multiple | Outlined transparent secondary button |
| `.btn-secondary`, `.btn-primary` | about.html | Dark-theme specific button variants |
| `.hero` | home.html | Hero section with top padding and centered content |
| `.pill-badge` | home.html | Rounded pill badge with a pulse dot inside |
| `.pulse-dot` | home.html | Animated pulsing orange dot |
| `.gradient-text` | multiple | Text with peach gradient fill using `-webkit-background-clip` |
| `.launch-downloads` | home.html | The download buttons container box |
| `.dl-buttons-grid` | home.html | 3-column grid for OS download buttons |
| `.os-btn` | home.html | Single OS download button |
| `.os-icon-box` | home.html | Colored icon container inside download button |
| `.os-arrow` | home.html | Right arrow icon that shifts on hover |
| `.ide-window` | home.html | The IDE mockup outer container |
| `.ide-titlebar` | home.html | Top bar with traffic lights and title |
| `.ide-activity` | home.html | Left vertical icon rail |
| `.ide-explorer` | home.html | File explorer panel in mockup |
| `.exp-file.active` | home.html | Currently active file in mockup explorer |
| `.ide-tabs`, `.ide-tab` | home.html | Tab bar and individual tabs |
| `.ide-gutters` | home.html | Line numbers column |
| `.ide-code-view` | home.html | Syntax-highlighted code display area |
| `.ide-terminal` | home.html | Bottom terminal drawer in mockup |
| `.kw`, `.fn`, `.str`, `.cm`, `.num` | home, login, register | Syntax highlighting color classes |
| `.modal-overlay` | home.html | Full-screen modal backdrop |
| `.modal-box` | home.html | White centered modal card |
| `.modal-step` | home.html | Numbered step inside download modal |
| `.feat-card` | home.html | Feature card with lift-hover effect |
| `.features-grid` | home.html | 3-column grid for feature cards |
| `.footer-grid` | multiple | 4-column footer layout grid |
| `.foot-brand` | multiple | Footer brand/logo column |
| `.foot-col` | multiple | Footer navigation column |
| `.foot-bottom` | multiple | Bottom row of footer with copyright |
| `.desktop-titlebar` | dashboard.html | Top titlebar of the IDE application |
| `.traffic-controls`, `.traffic-dot` | dashboard.html | macOS-style traffic light dots |
| `.titlebar-center` | dashboard.html | Center area showing window title and environment badge |
| `.titlebar-actions` | dashboard.html | Right-side action buttons in titlebar |
| `.top-btn` | dashboard.html | Small action button in titlebar |
| `.top-btn.run-btn` | dashboard.html | Peach gradient Run button in titlebar |
| `.desktop-menubar` | dashboard.html | Application menu bar |
| `.menu-item`, `.menu-trigger` | dashboard.html | Menu item and clickable label |
| `.dropdown-menu`, `.dropdown-row` | dashboard.html | Dropdown panel and individual menu items |
| `.dropdown-divider` | dashboard.html | 1px divider line inside dropdown |
| `.workspace-layout` | dashboard.html | Main flex container for IDE layout |
| `.activity-bar` | dashboard.html | Left icon strip in the IDE |
| `.act-icon` | dashboard.html | Individual activity bar icon |
| `.act-icon.active` | dashboard.html | Active icon with peach left border |
| `.side-panel` | dashboard.html | Left sidebar (file tree or AI panel) |
| `.side-head` | dashboard.html | Header row of the sidebar |
| `.file-tree` | dashboard.html | Scrollable file list container |
| `.tree-item` | dashboard.html | Single file in the file tree |
| `.tree-item.active` | dashboard.html | Currently open file in the tree |
| `.tree-label` | dashboard.html | Icon + filename row inside tree item |
| `.tree-del` | dashboard.html | Delete icon (hidden by default, shown on hover) |
| `.ai-view` | dashboard.html | AI assistant sidebar panel |
| `.ai-bubble` | dashboard.html | Chat bubble style text box |
| `.ai-quick-btn` | dashboard.html | Quick prompt action buttons in AI panel |
| `.editor-container` | dashboard.html | Main editor + terminal column |
| `.tab-bar` | dashboard.html | Horizontal open-file tabs row |
| `.tab` | dashboard.html | Individual editor tab |
| `.tab.active` | dashboard.html | Currently selected tab |
| `.tab.dirty` | dashboard.html | Tab with unsaved changes |
| `.dirty-dot` | dashboard.html | Orange dot indicator for unsaved files |
| `.tab-close` | dashboard.html | Close button on each tab |
| `.editor-body` | dashboard.html | Container for line numbers + textarea |
| `.line-numbers` | dashboard.html | Line number gutter column |
| `.code-textarea` | dashboard.html | The actual code editing textarea |
| `.bottom-panel` | dashboard.html | Collapsible terminal/output drawer |
| `.panel-tabs-bar` | dashboard.html | Tab switcher row inside bottom panel |
| `.panel-tab.active` | dashboard.html | Active bottom panel tab |
| `.terminal-console` | dashboard.html | Terminal text output area |
| `.term-input-row` | dashboard.html | Command input row at bottom of terminal |
| `.term-prompt` | dashboard.html | The `>` prompt symbol |
| `.term-input` | dashboard.html | The command input field |
| `.status-bar` | dashboard.html | Orange gradient bottom status bar |
| `.status-item` | dashboard.html | Individual item in status bar |
| `.dialog-overlay` | dashboard.html | Full-screen about dialog backdrop |
| `.dialog-box` | dashboard.html | White about dialog card |
| `.doc-layout` | documentation.html | Flex container for sidebar + content |
| `.doc-sidebar` | documentation.html | Fixed left sidebar |
| `.search-box` | documentation.html | Search input container in sidebar |
| `.doc-nav-group` | documentation.html | Group of sidebar nav links |
| `.doc-nav-title` | documentation.html | Section title inside a nav group |
| `.doc-link` | documentation.html | Individual sidebar navigation link |
| `.doc-link.active` | documentation.html | Currently active sidebar link |
| `.doc-content` | documentation.html | Main content area with left margin |
| `.doc-section` | documentation.html | A single documentation section |
| `.code-box` | documentation.html | Dark themed code sample container |
| `.code-box-header` | documentation.html | Header with label and Copy button |
| `.copy-btn` | documentation.html | Code copy button |
| `.code-content` | documentation.html | The pre-formatted code area |
| `.shortcut-table` | documentation.html | Dark themed data/feature table |
| `.key-badge` | documentation.html | Keyboard shortcut display badge |
| `.dl-hero` | downloads.html | Hero section for downloads page |
| `.version-chip` | downloads.html | Monospaced version label chip |
| `.dl-grid` | downloads.html | 3-column grid for platform cards |
| `.dl-card` | downloads.html | Platform download card |
| `.dl-card.win/.mac/.linux` | downloads.html | Platform modifier classes |
| `.dl-platform-icon` | downloads.html | Large platform icon box |
| `.dl-desc` | downloads.html | Short description under platform name |
| `.dl-main-btn` | downloads.html | Full-width download button inside a card |
| `.dl-alt-options` | downloads.html | Alternative download links and file size info |
| `.specs-section`, `.specs-box` | downloads.html | System requirements section and container |
| `.specs-table` | downloads.html | System requirements HTML table |
| `.feat-hero` | features.html | Hero section for features page |
| `.features-container` | features.html | 3-column grid for feature cards |
| `.feat-icon-box` | features.html | Peach gradient icon box inside feature card |
| `.cta-banner` | features.html | Peach gradient call-to-action section |
| `.intro-grid`, `.intro-card` | about.html | 2-column intro section with dark cards |
| `.features-grid`, `.feature-card` | about.html | 3-column dark feature cards |
| `.feature-icon-box` | about.html | Dark-theme icon box in feature card |
| `.tech-stack-container` | about.html | Container for tech stack section |
| `.tech-grid`, `.tech-item` | about.html | 4-column tech stack items |
| `.timeline`, `.timeline-step` | about.html | 4-column how-it-works steps |
| `.step-number` | about.html | Numbered circle in timeline steps |
| `.vision-banner` | about.html | 2-column vision statement section |
| `.vision-content` | about.html | Left text column inside vision banner |
| `.vision-list` | about.html | Bullet list with peach check icons |
| `.team-grid`, `.team-card` | about.html | 3-column team section with dark cards |
| `.team-avatar` | about.html | Circular avatar placeholder |
| `.github-cta` | about.html | Centered open-source CTA box |
| `.hero-badge` | about.html | Dark-theme pill badge in hero |
| `.hero-buttons` | about.html | Flex row of hero action buttons |
| `.left-panel`, `.right-panel` | login, register | Split-screen two-column layout panels |
| `.bg-half` | login, register | Fixed peach gradient on the left half |
| `.ide-preview` | login, register | Mini decorative IDE mockup on left panel |
| `.ide-bar` | login, register | Top bar of mini IDE preview |
| `.ide-content` | login, register | Code content inside mini IDE |
| `.tagline` | login, register | Motivational text below mini IDE |
| `.form-header` | login, register | Form title and subtitle |
| `.field` | login, register | Form field wrapper with label |
| `.input-wrap`, `.icon` | login, register | Input with absolutely-positioned icon inside |
| `.btn-submit` | login, register | Full-width peach gradient submit button |
| `.divider` | login, register | "or" text with horizontal lines on both sides |
| `.signup-link` | login, register | "Create account / Sign in" redirect link |
| `.flash-msg` | login, register | Flash notification bar from Flask |
| `.flash-error` | login, register | Red error flash message |
| `.flash-success` | login, register | Green success flash message |
| `.section-head` | home.html | Centered section heading + subtitle |

---

## 10. Backend API Calls from Frontend

The `dashboard.html` page makes these **`fetch()` HTTP requests** to the Flask backend. All POST requests send JSON and receive JSON.

| Method | Endpoint | Request Payload | Response |
|---|---|---|---|
| `GET` | `/api/files` | — | `{ success: true, files: [{ name, size, is_dir }] }` |
| `POST` | `/api/get-file` | `{ filename: "main.py" }` | `{ success: true, content: "..." }` |
| `POST` | `/api/save-file` | `{ filename: "main.py", content: "..." }` | `{ success: true }` |
| `POST` | `/api/new-file` | `{ filename: "utils.py" }` | `{ success: true }` |
| `POST` | `/api/delete-file` | `{ filename: "utils.py" }` | `{ success: true }` |
| `POST` | `/run-code` | `{ filename: "main.py", code: "..." }` | `{ output: "...", exit_code: 0 }` |

All requests use this pattern:
```js
const res = await fetch('/api/endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ ...payload })
});
const data = await res.json();
```

---

*This READ.md was generated by analyzing every line of actual frontend code in the SmartIDE software portal project. No assumptions were made — every detail comes directly from the HTML, CSS, and JavaScript in the project files.*

**© 2026 SmartIDE — Peach & White Desktop Edition v2.4.1**
