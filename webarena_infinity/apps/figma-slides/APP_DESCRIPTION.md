# Figma Slides

A web-based slide presentation editor modeled after Figma Slides, featuring a dark-themed canvas workspace with slide management, rich object editing, live interactions, template styling, and collaboration tools.

## Features

### Slide Management
- **16 slides** organized into 3 named groups ("Q3 Review", "Q4 Planning", "Team Updates") plus ungrouped slides
- Add slides from 12 layout presets (blank, title, title+body, two-column, section, etc.)
- Duplicate, delete, skip/unskip, and reorder slides
- List view and grid view toggle for the slide panel
- Collapsible slide groups with expand/collapse toggle
- Slide context menu (right-click) for quick actions
- 1 slide pre-marked as skipped (slide_012)

### Canvas & Objects
- 1200x675 coordinate system scaled to 960x540 display (0.8x factor)
- **45 objects** across slides: 27 text, 12 shape, 2 table, 1 code block, 3 live interactions
- Object selection with visual handles (NW/NE/SW/SE corners)
- Object property editing in the right sidebar (position, size, opacity, rotation, lock)
- Delete objects via keyboard (Delete/Backspace)

### Object Types
- **Text**: Font family, size, weight, color, alignment, italic; supports bold/italic markdown formatting
- **Shape**: 10 shape types (rectangle, circle, triangle, diamond, arrow, star, pentagon, hexagon, pill, line); fill, stroke, corner radius
- **Code Block**: 19 languages, 6 themes (dark, light, monokai, etc.), syntax display with header dots
- **Table**: Row/column structure with editable cells, header styling; add/remove rows and columns
- **Image**: Placeholder with fill modes (fill, fit, crop, tile)
- **Live Interactions**: Poll (with vote bars and percentages), Alignment scale (1-5 with average), Stamps (emoji reactions with counts)

### Transitions & Animations
- 8 slide transition types (none, dissolve, slide-left/right/up/down, push, zoom)
- Per-transition duration (100-3000ms) and easing (7 presets)
- 8 object animation styles (none, fade-in, slide-up/down/left/right, scale-up, bounce)
- Per-object animation delay and duration controls

### Design & Styling
- 3 template styles ("Minimal Dark", "Corporate Blue", "Warm Sunset") with color palettes and text style presets
- Per-slide background: solid color, gradient (2-stop with angle), or image URL with fill mode
- "Remix colors" to randomize template style colors
- Design mode toggle (Shift+D) for global design-focused editing
- Slide number configuration: show/hide, count mode (all/non-skipped), format (number only, with total, with title)

### Presenter Notes
- Per-slide notes visible below the canvas
- Toggle visibility on/off
- Editable inline with real-time state sync
- All 16 slides have pre-populated presenter notes

### Collaboration
- **7 collaborators** with avatar colors, roles (Editor/Viewer), online status
- Avatar stack in toolbar showing online users
- Share modal with link sharing (view/edit), invite by email, and collaborator management
- Role changes (Editor/Viewer) and collaborator removal

### Comments
- **6 comments** across multiple slides, with replies and resolved/unresolved states
- Comments modal for viewing, adding, resolving, and replying
- Filter by slide context

### Libraries
- **3 design libraries** ("DesignCraft Core", "Icon Set Pro", "Brand Assets") with component/style/variable counts
- Enable/disable libraries
- Library detail view

### Export & History
- Export modal with format options (PDF, PNG, SVG, PPTX) and quality/scale settings
- **3 export history** entries and **5 version history** entries
- Deck settings modal (name, dimensions, default transition)

### Templates
- **12 available templates** (pitch deck, product launch, quarterly review, etc.) for new slide creation

## Data Model

### Core Entities
- `slides[]` — id, title, objects[], background, transition, presenterNotes, groupId, skipped, order, slideNumber config
- `slides[].objects[]` — id, type, x, y, width, height, opacity, rotation, locked, visible, plus type-specific properties
- `deckSettings` — name, width, height, aspectRatio, teamName, projectName, shareSettings, defaultTransition
- `templateStyles[]` — id, name, colors[], textStyles[]
- `comments[]` — id, slideId, userId, text, timestamp, resolved, replies[]
- `libraries[]` — id, name, enabled, components, styles, variables
- `collaborators[]` — id, name, email, avatarColor, initials, role, online
- `currentUser` — id, name, email, role, plan, teamName
- `exportHistory[]` — id, format, timestamp, fileName, size
- `versionHistory[]` — id, timestamp, author, description

### State Management
- `AppState` object with `subscribe(fn)` / `notify()` pattern
- Persistent state: localStorage with `SEED_DATA_VERSION` check
- Server sync: `PUT /api/state` on every mutation
- UI state (not persisted): selectedSlideId, selectedObjectId, activePanel, activeModal, gridView, designMode, presenterNotesVisible

## Navigation

### Layout
- **Toolbar** (top, 48px): Logo, deck name, view toggle, object tools (text, shape, image), assets, interactions, design mode, collaborator avatars, present button, share button
- **Left Sidebar** (240px): Slide thumbnails in list or grid view, grouped sections, "New slide" button
- **Canvas** (center, flex): Selected slide rendered at scale with objects, presenter notes below
- **Right Sidebar** (280px): Design tab (template style, background, slide number, export) and Animate tab (transition, object animations)

### Modals
- Share, Present, Export, Add Slide, Shapes, Assets, Interactions, Edit Table Cell, Edit Text, Edit Code, Template Styles, Libraries, Comments, Deck Settings, Confirm Delete

### Keyboard Shortcuts
- **Escape**: Close modal or deselect object
- **Delete/Backspace**: Delete selected object
- **Cmd/Ctrl+D**: Duplicate selected slide
- **Shift+D**: Toggle design mode
- **Enter**: Confirm active modal

## Controls

All controls are custom HTML/CSS — no native OS elements:
- **Custom dropdowns**: Template style, transition type, easing, animation style, language, theme, fill mode, aspect ratio, slide number format/count, export format
- **Toggle switches**: Show slide number, include total, lock object, library enable, share link enabled
- **Color pickers**: 16-preset palette with hex input for background color, gradient stops, text color, fill, stroke
- **Sliders**: Opacity, transition duration, animation delay/duration
- **Tab bars**: Design/Animate panel, background type (Solid/Gradient/Image)
- **Context menus**: Right-click on slides (Duplicate, Skip/Unskip, Delete)
- **Modals**: Overlay-based with header, body, footer; close via X button or Escape

## Seed Data

- **Deck**: "Q4 2025 Product Strategy" by DesignCraft team
- **16 slides**: Title, Agenda, Q3 highlights/metrics/feedback, Q4 roadmap/design system/SDK preview/survey results/feature adoption, team updates, partnerships, budget, risk assessment, next steps, thank you
- **3 slide groups**: "Q3 Review" (3 slides), "Q4 Planning" (5 slides), "Team Updates" (2 slides)
- **45 objects**: Mix of text headings, body text, shapes (decorative and content), tables (metrics, feature data), code block (SDK preview), and 3 live interactions (poll, alignment scale, stamps)
- **6 comments**: Cross-slide discussion threads with replies, mix of resolved and unresolved
- **7 collaborators**: 4 online, 3 offline; 5 editors, 2 viewers
- **3 template styles** with 6 colors and 5 text styles each
- **3 libraries** with varying component/style/variable counts
- **5 version history** entries spanning Oct 8-15, 2025
- **3 export history** entries (PDF, PPTX, PNG)
- **12 available templates** for new presentations
