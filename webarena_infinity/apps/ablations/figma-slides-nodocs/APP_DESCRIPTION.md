# Figma Slides — App Description

## Summary

Figma Slides is a collaborative presentation tool built into a design platform. It allows users to create, edit, organize, and present slide decks. The app features a dashboard for managing presentations, a full-featured slide editor with element manipulation tools, a template gallery, slide transitions and animations, speaker notes, comments/collaboration, share/export settings, and a full-screen presenter mode.

## Main Sections / Pages

### 1. Dashboard (`#/` or `#/dashboard`)
- Grid of presentation cards showing thumbnails, titles, metadata, tags
- Search bar for filtering by title, description, or tags
- Dropdown filters: status (published, draft, archived), tags, sort order (last modified, created date, title)
- Create new presentation button (opens modal)
- Each card has actions: present, duplicate, share, delete, toggle star

### 2. Slide Editor (`#/editor/{presentationId}`)
Three-panel layout:
- **Left Panel (Filmstrip):** Scrollable list of slide thumbnails with slide numbers, click to navigate, add slide and template buttons
- **Center (Canvas):** Main slide editing area with zoomable canvas (960×540 px at 100%), element rendering, drag-to-move, resize handles, grid overlay toggle
- **Right Panel (Properties):** Context-sensitive properties for selected element or current slide
- **Bottom (Speaker Notes):** Collapsible textarea for editing per-slide notes
- **Top Toolbar:** Back button, presentation title, tool palette (select/text/rectangle/circle/line/arrow/image), grid toggle, notes toggle, comments button, zoom controls, share/export/present buttons

### 3. Presenter Mode (`#/presenter/{presentationId}`)
- Full-screen slide display scaled to viewport
- Navigation: previous/next buttons, keyboard arrows, space/enter
- Progress indicator (slide N of M)
- Running timer (MM:SS)
- Speaker notes panel (toggleable)
- Exit button (returns to editor)

## Complete List of Implemented Features

### Presentation Management
- Create presentation (title, description, theme, tags)
- Edit presentation metadata (title, description, status, tags)
- Delete presentation (with confirmation dialog)
- Duplicate presentation (deep copy of all slides and elements)
- Toggle star/favorite
- Search presentations by title, description, or tags
- Filter by status: published, draft, archived
- Filter by tag (all tags extracted from presentations)
- Sort by: last modified, created date, title A-Z
- Toggle sort direction (ascending/descending)

### Slide Management
- Add blank slide (inserts after current)
- Add slide from template
- Delete slide (with confirmation, cannot delete last slide)
- Duplicate slide
- Navigate slides via filmstrip thumbnails
- Slide ordering (each slide has an `order` field)
- Apply template to existing slide (replaces elements)
- Save current slide as custom template

### Element Tools (Canvas)
- **Select tool (V):** Click to select elements, drag to move, resize handles
- **Text tool (T):** Click on canvas to add text element
- **Rectangle tool (R):** Click to add rectangle shape
- **Circle tool (O):** Click to add circle shape
- **Line tool (L):** Click to add line
- **Arrow tool:** Click to add arrow
- **Image tool:** Click to add image placeholder
- Drag elements to reposition
- Resize elements via corner handles (NW, NE, SW, SE)
- Delete elements (Delete/Backspace key or properties panel button)
- Lock/unlock elements (prevents movement when locked)

### Element Properties (Properties Panel)
**All elements:**
- Position: X, Y (pixel coordinates)
- Size: Width, Height
- Rotation (degrees)
- Opacity (0–1)
- Lock toggle
- Animation settings (type, duration, delay, order)
- Delete button

**Text elements:**
- Font family dropdown: Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Source Sans Pro, Playfair Display, Merriweather, Fira Code
- Font size (8–200)
- Font weight: Regular, Medium, Semibold, Bold
- Italic toggle
- Underline toggle
- Text alignment: left, center, right
- Text color (color palette picker)
- List type: None, Bullet, Numbered
- Line height (0.5–3.0)
- Letter spacing (-5 to 20)
- Content textarea (multiline editing)

**Shape elements:**
- Shape type dropdown: rectangle, circle, line, arrow, triangle, diamond, star, polygon
- Fill color (color palette picker)
- Stroke color (color palette picker)
- Stroke width (0–20)
- Corner radius (0–100)

### Slide Properties (Properties Panel — no element selected)
- Background color (color palette with 22 colors)
- Layout type dropdown: title, title-content, two-column, section-header, blank, image-focused
- Transition settings button (opens modal)
- Slide actions: duplicate, apply template, save as template, delete

### Slide Transitions
- Transition types: none, fade, slide, dissolve, push
- Duration control: 100–3000ms in 100ms steps
- Configured per-slide via modal dialog

### Element Animations
- Animation types: none, appear, fade-in, move-in-left, move-in-right, move-in-up, move-in-down, scale-in, bounce-in
- Duration: 100–3000ms
- Delay: 0–5000ms
- Order: 0–20 (controls sequence)
- Configured per-element via modal dialog

### Templates
- 12 built-in templates across 3 categories:
  - **Basic (6):** Title Slide, Title + Content, Two Column, Section Header, Blank, Image + Text
  - **Business (4):** Big Number, Comparison, Three Cards, Timeline
  - **Creative (2):** Quote, Team Intro
- Template gallery modal with category filter buttons
- Apply template to new slide or replace current slide contents
- Save any slide as custom template (category: custom)

### Speaker Notes
- Collapsible panel below the canvas
- Per-slide rich text area
- Toggle visibility via toolbar button
- Visible during presenter mode

### Comments & Collaboration
- Comments modal showing current slide comments + other slide comments
- Add comment on current slide
- Reply to existing comments
- Resolve/unresolve comments (toggle)
- Delete comments
- Comment count badge in toolbar (shows unresolved count)
- Each comment shows author avatar, name, timestamp, and content
- Each reply shows author avatar, name, timestamp

### Share & Export
**Share settings (per presentation):**
- Visibility: private, team, organization, public
- Allow comments toggle
- Allow editing toggle
- Share link display with copy button
- Embed link display with copy button
- Shared users list with remove buttons
- Add user dropdown to add new shared users

**Export options (modal):**
- Export as PDF (all slides)
- Export slides as PNG (individual images)
- Export as SVG (vector format)

### Presenter Mode
- Full-screen presentation view with scaled slide rendering
- Previous/Next slide navigation buttons
- Keyboard navigation: ArrowRight/Space/Enter (next), ArrowLeft/Backspace (prev), Escape (exit)
- Slide progress indicator (N / total)
- Running timer display (MM:SS from start)
- Toggleable speaker notes panel
- Exit button returns to editor

### Canvas Features
- Zoom: 25%–200% in 10% increments (zoom in/out buttons)
- Grid overlay toggle (20px grid at 100%)
- Canvas dimensions: 960×540 pixels (16:9 aspect ratio)

### Keyboard Shortcuts (Editor)
- V: Select tool
- T: Text tool
- R: Rectangle tool
- O: Circle tool
- L: Line tool
- Delete/Backspace: Delete selected element
- Escape: Deselect element or close modal

## Data Model

### Users
| Field | Type | Description |
|-------|------|-------------|
| id | string | e.g. `user_001` |
| name | string | Full name |
| email | string | Email address |
| initials | string | Two-letter initials for avatar |
| color | string | Hex color for avatar background |
| role | string | `owner`, `editor`, or `viewer` |

### Presentations
| Field | Type | Description |
|-------|------|-------------|
| id | string | e.g. `pres_001` |
| title | string | Presentation title |
| description | string | Brief description |
| createdAt | ISO string | Creation timestamp |
| updatedAt | ISO string | Last modification timestamp |
| createdBy | string | User ID of creator |
| theme | string | Theme name (corporate, creative, minimal, etc.) |
| tags | string[] | Array of tag strings |
| starred | boolean | Favorited flag |
| status | string | `published`, `draft`, or `archived` |
| slideCount | number | Number of slides |
| shareSettings | object | See share settings below |

### Share Settings (nested in Presentation)
| Field | Type | Description |
|-------|------|-------------|
| visibility | string | `private`, `team`, `organization`, or `public` |
| allowComments | boolean | Whether comments are enabled |
| allowEditing | boolean | Whether editing is allowed for shared users |
| shareLink | string | Shareable URL |
| embedLink | string | Embeddable URL |
| sharedWith | string[] | Array of user IDs |

### Slides
| Field | Type | Description |
|-------|------|-------------|
| id | string | e.g. `slide_001_00` |
| presentationId | string | Parent presentation ID |
| order | number | Position in deck (0-based) |
| layout | string | `title`, `title-content`, `two-column`, `section-header`, `blank`, `image-focused` |
| backgroundColor | string | Hex color |
| transition | object | `{ type: string, duration: number }` |
| speakerNotes | string | Presenter notes text |
| elements | Element[] | Array of canvas elements |

### Elements (nested in Slide)
| Field | Type | Description |
|-------|------|-------------|
| id | string | e.g. `elem_00001` |
| type | string | `text`, `shape`, or `image` |
| x | number | X position in pixels |
| y | number | Y position in pixels |
| width | number | Width in pixels |
| height | number | Height in pixels |
| rotation | number | Degrees |
| opacity | number | 0–1 |
| locked | boolean | Prevents movement |
| content | string/null | Text content (text elements) |
| style | object/null | Text style object (text elements) |
| shapeType | string/null | Shape type (shape elements) |
| fill | string/null | Fill color (shapes) |
| stroke | string/null | Stroke color (shapes) |
| strokeWidth | number | Stroke width (shapes) |
| cornerRadius | number | Border radius (shapes) |
| imageUrl | string/null | Image source URL |
| imagePlaceholder | string/null | Placeholder color |
| animation | object | `{ type, duration, delay, order }` |

### Text Style (nested in Element)
| Field | Type | Description |
|-------|------|-------------|
| fontFamily | string | Font name |
| fontSize | number | Size in pixels |
| fontWeight | string | `normal`, `500`, `600`, `bold` |
| color | string | Hex color |
| textAlign | string | `left`, `center`, `right` |
| italic | boolean | Italic flag |
| underline | boolean | Underline flag |
| lineHeight | number | Line height multiplier |
| letterSpacing | number | Tracking in pixels |
| listType | string | `none`, `bullet`, `numbered` |

### Templates
| Field | Type | Description |
|-------|------|-------------|
| id | string | e.g. `tmpl_001` |
| name | string | Template display name |
| category | string | `basic`, `business`, `creative`, `custom` |
| layout | string | Layout type |
| description | string | Brief description |
| previewColor | string | Color for preview thumbnail |
| elements | object[] | Template elements (no IDs) |

### Comments
| Field | Type | Description |
|-------|------|-------------|
| id | string | e.g. `cmt_001` |
| presentationId | string | Presentation ID |
| slideId | string | Slide ID |
| elementId | string/null | Optional element ID |
| authorId | string | Author user ID |
| content | string | Comment text |
| createdAt | ISO string | Timestamp |
| resolved | boolean | Resolution status |
| replies | Reply[] | Array of reply objects |

### Replies (nested in Comment)
| Field | Type | Description |
|-------|------|-------------|
| id | string | e.g. `reply_001` |
| authorId | string | Author user ID |
| content | string | Reply text |
| createdAt | ISO string | Timestamp |

## Navigation Structure

| Route | View | Description |
|-------|------|-------------|
| `#/` | Dashboard | Presentation list with search/filter |
| `#/editor/{presId}` | Editor | Slide editor for specific presentation |
| `#/editor/{presId}/{slideIndex}` | Editor | Editor opened to specific slide |
| `#/presenter/{presId}` | Presenter | Full-screen presentation mode |

## Available Form Controls

### Dropdowns (custom-built, not native `<select>`)
- Filter Status: All Statuses, Published, Draft, Archived
- Filter Tag: All Tags, plus all tags from presentations
- Sort By: Last Modified, Created Date, Title A-Z
- Slide Layout: Title, Title Content, Two Column, Section Header, Blank, Image Focused
- Font Family: Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Source Sans Pro, Playfair Display, Merriweather, Fira Code
- Font Weight: Regular, Medium, Semibold, Bold
- List Type: None, Bullet List, Numbered List
- Shape Type: Rectangle, Circle, Line, Arrow, Triangle, Diamond, Star, Polygon
- Transition Type: None, Fade, Slide, Dissolve, Push
- Animation Type: None, Appear, Fade In, Move In Left, Move In Right, Move In Up, Move In Down, Scale In, Bounce In
- Share Visibility: Private, Team, Organization, Public
- New Presentation Theme: Minimal, Corporate, Creative, Nature, Warm, Ocean, Dark, Sunset
- Template Category: Custom, Basic, Business, Creative
- Add Shared User: List of users not already shared with

### Toggles
- Allow Comments (share settings)
- Allow Editing (share settings)
- Lock Element (element properties)
- Show Grid (toolbar)
- Show Speaker Notes (toolbar)

### Color Palettes
- Slide Background: 22 colors (white, grays, blacks, brand colors)
- Text Color: Same 22-color palette
- Shape Fill: Same palette
- Shape Stroke: Same palette

### Text Inputs
- Search box (dashboard)
- Presentation title (new presentation modal)
- Presentation description (new presentation modal)
- Tags (new presentation modal, comma-separated)
- Speaker notes (editor textarea)
- Element content (properties panel textarea)
- Comment text (comments modal textarea)
- Reply text (inline input per comment)
- Template name (save template modal)
- Share link (read-only, copyable)
- Embed link (read-only, copyable)

### Number Inputs (Properties Panel)
- X, Y, Width, Height (element position/size)
- Rotation (-360 to 360)
- Opacity (0 to 1, step 0.1)
- Font Size (8 to 200)
- Line Height (0.5 to 3.0, step 0.1)
- Letter Spacing (-5 to 20, step 0.5)
- Stroke Width (0 to 20)
- Corner Radius (0 to 100)
- Transition Duration (100 to 3000, step 100)
- Animation Duration (100 to 3000, step 100)
- Animation Delay (0 to 5000, step 100)
- Animation Order (0 to 20)

## Seed Data Summary

### Users (8)
| ID | Name | Role |
|----|------|------|
| user_001 | Sarah Chen | Owner |
| user_002 | Marcus Rivera | Editor |
| user_003 | Anika Patel | Editor |
| user_004 | James O'Brien | Editor |
| user_005 | Yuki Tanaka | Viewer |
| user_006 | Priya Sharma-Krishnamurthy | Editor |
| user_007 | David Kim | Viewer |
| user_008 | Elena Voronova | Editor |

### Presentations (18)
| ID | Title | Status | Slides | Creator | Starred |
|----|-------|--------|--------|---------|---------|
| pres_001 | Q1 2026 Product Roadmap | published | 15 | Sarah Chen | Yes |
| pres_002 | Brand Identity Guidelines v2.0 | published | 18 | Priya Sharma-Krishnamurthy | Yes |
| pres_003 | Series B Fundraising Pitch | published | 12 | Sarah Chen | Yes |
| pres_004 | User Research Findings — Mobile App | published | 16 | Anika Patel | No |
| pres_005 | Engineering Architecture Overview | published | 11 | James O'Brien | No |
| pres_006 | Annual Company All-Hands 2026 | published | 21 | Sarah Chen | Yes |
| pres_007 | Client Proposal — TechVentures Redesign | published | 14 | Sarah Chen | No |
| pres_008 | Design Sprint Week 12 Recap | published | 8 | Marcus Rivera | No |
| pres_009 | Onboarding Training Module | published | 16 | David Kim | No |
| pres_010 | Marketing Campaign: Design Without Limits | published | 12 | Elena Voronova | Yes |
| pres_011 | Accessibility Audit Results | published | 9 | Anika Patel | No |
| pres_012 | Q4 2025 Revenue Analysis | published | 13 | Yuki Tanaka | No |
| pres_013 | Mobile Design System Components | published | 25 | Priya Sharma-Krishnamurthy | Yes |
| pres_014 | Team Retrospective — Sprint 47 | published | 6 | Marcus Rivera | No |
| pres_015 | Product Demo — Enterprise Features | published | 11 | James O'Brien | No |
| pres_016 | Website Redesign Proposal — TechStartup.io | draft | 14 | James O'Brien | No |
| pres_017 | Competitor Analysis Dashboard | archived | 8 | Yuki Tanaka | No |
| pres_018 | Design Workshop Materials | draft | 5 | Anika Patel | No |

### Total Data Counts
- 234 slides across all presentations
- 616 elements across all slides (text, shapes, images)
- 12 built-in templates
- 40 comments with 24 replies
- 8 users with varied roles

### Share Settings Distribution
- Private: pres_003, pres_007, pres_012, pres_016, pres_017
- Team: pres_001, pres_004, pres_005, pres_008, pres_010, pres_011, pres_014, pres_015, pres_018
- Organization: pres_002, pres_006, pres_009, pres_013

### Tag Distribution
Tags include: product, roadmap, quarterly, brand, design-system, guidelines, fundraising, confidential, investors, research, ux, mobile, usability, engineering, architecture, technical, all-hands, company, culture, client, proposal, web-design, sprint, recap, weekly, onboarding, hr, training, marketing, campaign, ai, launch, accessibility, audit, wcag, finance, revenue, analysis, components, documentation, retro, agile, demo, enterprise, sales, strategy, competitors, market, workshop, creative, exercise

### Themes
Available themes: corporate, creative, minimal, nature, warm, ocean, dark, sunset — each with primary, secondary, accent, text, and background colors.
