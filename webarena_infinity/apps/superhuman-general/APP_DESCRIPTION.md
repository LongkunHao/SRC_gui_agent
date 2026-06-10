# Superhuman Mail - App Description

## Summary
A functional replica of the Superhuman email client - a keyboard-first, speed-focused email application. The app implements inbox management with split inbox, email triage (Mark Done, Remind Me), compose/reply/forward, snippets, calendar integration, read receipts, auto labels, command palette, and comprehensive settings. Built as a single-page app with vanilla HTML/CSS/JS.

## Main Sections/Pages

### Inbox (Split Inbox)
- **Important** split: Person-to-person messages
- **Other** split: Automated notifications, newsletters, service emails
- **Calendar** split: Calendar invites and scheduling emails
- **Feeds** split: Newsletter-specific view
- **Notifications** split: Automated notification view
- Navigate between splits via tabs at top of email list or Tab/Shift+Tab keyboard shortcuts

### Email Detail View
- Full email body with thread messages (earlier conversation history)
- Sender info, recipients (To/Cc), date, labels
- Attachments section with file names and sizes
- Read receipt details (opened count, reader names, devices, timestamps)
- Instant Reply buttons (3 AI-suggested quick responses)
- Action buttons: Reply, Reply All, Forward, Mark Done, Remind, Star, Label, Move, Unsubscribe, Trash

### Done (Archive)
- Emails marked as Done/archived via E key or Done button
- Emails return to inbox if someone replies

### Reminders
- Emails with reminders set (via H key or Remind button)
- Options: Later today, Tomorrow, This weekend, Next week, In 2 weeks, Next month, Custom date/time

### Sent
- All emails sent by the current user
- Shows read receipt status (opened/not opened)

### Drafts
- Unsent email drafts

### Starred
- Emails marked with a star

### Recent Opens
- Real-time feed showing when recipients open sent emails
- Displays reader name, email subject, timestamp, device type

### Snippets
- Reusable email templates with variables in {curly_brackets}
- Create, edit, delete snippets
- Share snippets with team (toggle)
- Snippet metrics: sends count, open rate, response rate
- Insert snippets while composing (via ; key or Snippet button)
- Prefix naming convention for sub-team organization (e.g., [Sales], [HR], [Engineering])

### Spam / Trash
- Spam and trash folders for filtered/deleted emails

### Labels
- User-created labels with custom colors
- Apply labels to emails via label picker
- Navigate to label-specific views from sidebar
- Remove labels from email detail view

### Calendar
- **Day View** (toggle via calendar button or 0 key): Shows events for selected date in right sidebar
- **Week View** (via week button or 2 key): 7-column grid showing full week
- Create new events with title, date, time, location, description, attendees
- Navigate between days/weeks with arrow buttons
- Jump to today

### Settings Panel (right overlay)
Tabs: General, Read Statuses, Reminders, Auto Labels, Splits, Calendar, Booking Pages, Shortcuts, Signature, Auto Archive

### Command Palette
- Cmd+K (or button) opens centered overlay
- Search/filter commands
- Quick access to all major actions and navigation

## Complete List of Implemented Features

### Email Operations
- Compose new email (C key or Compose button)
- Reply (R key), Reply All (Enter key), Forward (F key)
- Send email with To, Cc, Bcc, Subject, Body
- Save drafts
- Mark Done / Archive (E key)
- Set Reminder / Snooze (H key) with preset and custom time options
- Star / Unstar emails
- Move to folder (V key) - Inbox, Done, Trash, Spam
- Apply / remove labels
- Mark as Read / Unread
- Unsubscribe (Cmd+U) - blocks sender
- Move to Trash
- Mark as Spam
- Instant Reply (3 AI-suggested quick responses)
- Select multiple emails (checkboxes)
- Bulk actions on selected emails (Done, Remind, Trash, Star, Label, Mark Read/Unread)
- Get Me To Zero (archives emails older than 7 days)

### Inbox Organization
- Split Inbox with 5 splits (Important, Other, Calendar, Feeds, Notifications)
- Auto Labels (library + custom) for automatic categorization
- Auto Archive based on Auto Label rules
- Label management (create with name + color, delete)
- Search with operators: from:, to:, subject:, has:attachment
- General text search across subject, snippet, sender, body
- Pagination (25 per page)

### Calendar & Scheduling
- Day view in right sidebar
- Week view in main content area
- Create events with full details
- View event times, locations, meeting links, attendees
- Navigate between days/weeks
- Booking Pages: create, toggle active/inactive, delete

### Read Receipts & Tracking
- Read receipt indicators on sent emails (checkmarks)
- Recent Opens feed showing who opened your emails
- Detailed read receipt info: reader name, device, timestamp, open count
- Team read status sharing (setting)

### Snippets / Templates
- Create, edit, delete snippets
- Variable support: {first_name}, {topic}, etc.
- Share with team toggle
- Snippet metrics (sends, open rate, response rate)
- Insert into compose via picker (;)
- Search snippets by name

### AI Features (settings)
- Instant Reply toggle
- Smart Send toggle (optimal send time)
- Ask AI toggle
- Auto Reminders (AI mode, external mode, off)
- Auto Drafts (follow-up or scheduling)

### Settings
- Theme: Light / Dark / System
- Desktop notifications toggle
- Sound notifications toggle
- Swipe left action: Done / Trash / Spam
- Swipe right action: Remind / Star / Unread
- Read receipts enable/disable
- Team read statuses
- Auto reminders mode and default time
- Auto drafts type and Cc teammate option
- Calendar alerts and alert timing
- Meeting link provider (Zoom, Google Meet, Teams)
- Auto-add meeting links
- Primary and secondary timezone
- Keyboard shortcuts enable/disable
- Email signature editor
- Auto archive enable/disable with label selection
- Split inbox management (create, delete custom splits)

### Keyboard Shortcuts
- Cmd+K: Command Palette
- C: Compose
- E: Mark Done
- H: Remind Me
- R: Reply
- Enter: Reply All (in email detail)
- F: Forward
- V: Move to folder
- /: Focus search
- ;: Insert snippet (in compose)
- 0: Toggle calendar day view
- 2: Toggle calendar week view
- Tab/Shift+Tab: Navigate between splits
- B: Create event
- ?: Ask AI (opens command palette)
- Cmd+A: Select all
- Cmd+U: Unsubscribe
- Cmd+Enter: Send email
- Escape: Close overlays / go back

## Data Model

### Email
- id (number), threadId (string)
- from: { name, email }
- to: [{ name, email }], cc: [{ name, email }], bcc: []
- subject, snippet, body (strings)
- date (ISO string)
- isRead, isStarred, isDone, isTrashed, isSpam, isDraft (booleans)
- labels: [labelId strings]
- hasAttachments (boolean), attachments: [{ name, size }]
- splitCategory: 'important' | 'other' | 'calendar'
- remindAt: ISO string or null
- readReceipt: { opened, openedAt, device, openCount, readers? } or null
- autoLabel: string or null
- replyDraftingTeammate: string or null (team reply indicator)
- threadMessages: [{ id, from, date, body }] or null

### Contact
- id, name, email, avatarColor, company, isFrequent, isTeammate

### Label
- id, name, type ('system' | 'user'), color

### Auto Label
- id, name, type ('library' | 'custom'), enabled, criteria: { from?, subject?, ai? }

### Split
- id, name, position, isDefault, criteria: { type? | autoLabel? }, description

### Snippet
- id, name, body, variables: [string], isShared, author, authorId, createdAt
- metrics: { sends, openRate, responseRate }

### Calendar Event
- id, title, date, startTime, endTime, location, description
- attendees: [email strings], meetingLink, isAllDay, calendarId, organizer, status, color

### Booking Page
- id, title, duration, location, description, availability: { days, startTime, endTime }, link, isActive

### Settings
- readReceipts: { enabled, teamSharing }
- autoReminders: { mode, defaultTime, enabled }
- autoDrafts: { enabled, type, ccTeammate, ccEmail }
- smartSend: { enabled }
- theme: 'light' | 'dark' | 'auto'
- notifications: { desktop, sound, calendarAlerts, alertMinutes }
- meetingLink: { provider, autoAdd }
- keyboard: { shortcuts }
- signature (string)
- timezone, secondaryTimezone
- swipeLeft, swipeRight
- autoArchive: { enabled, labels: [autoLabelId] }
- instantReply: { enabled }
- askAi: { enabled, searchYears }
- blockedSenders: [email strings]

### Recent Opens
- emailId, reader (name), openedAt, device

## Navigation Structure

- **Sidebar** (always visible):
  - Compose button
  - System folders: Inbox, Starred, Done, Reminders, Sent, Drafts, Recent Opens, Snippets, Spam, Trash
  - Labels section with user-created labels
- **Top bar**:
  - Logo, Search bar, Calendar toggle, Week view, Command Palette, Settings, User avatar
- **Hash-based routing**:
  - `#/inbox` - Inbox with split tabs
  - `#/email/{id}` - Email detail
  - `#/done` - Archived emails
  - `#/reminders` - Snoozed emails
  - `#/sent` - Sent emails
  - `#/drafts` - Draft emails
  - `#/starred` - Starred emails
  - `#/opens` - Recent Opens feed
  - `#/snippets` - Snippet management
  - `#/spam` - Spam folder
  - `#/trash` - Trash folder
  - `#/label/{labelId}` - Label-specific view
  - `#/search` - Search results

## Available Form Controls

### Dropdowns (custom, no native select)
- Theme: Light, Dark, System
- Swipe Left: Mark Done, Trash, Spam
- Swipe Right: Remind Me, Star, Mark Unread
- Auto Reminder Time: 9 AM, 10 AM, 2 PM, 5 PM
- Alert Minutes: 5, 10, 15, 30 minutes before
- Meeting Provider: Zoom, Google Meet, Microsoft Teams, None
- Primary Timezone: ET, CT, MT, PT, GMT, CET, JST
- Secondary Timezone: None, ET, PT, GMT, CET, JST
- Booking Page Duration: 15, 30, 45, 60 minutes
- Booking Page Location: Zoom, Google Meet, Phone, In-person
- Split Criteria Type: Based on Auto Label, Based on sender

### Toggles
- Desktop notifications, Sound, Instant Reply, Smart Send, Ask AI
- Read Receipts enabled, Team Read Statuses
- Auto Reminders enabled, Auto Drafts enabled, Auto Drafts Cc teammate
- Calendar alerts, Auto-add meeting link
- Keyboard shortcuts, Auto Archive enabled

### Radio Groups
- Auto Reminder Mode: AI-detected, All external, No auto
- Auto Draft Type: Follow-up, Scheduling

### Text Inputs
- Search bar, Command palette input
- Compose: To, Cc, Bcc, Subject, Body
- Reminder custom date/time
- Label name, Label color
- Auto Label: name, from criteria, subject criteria, AI description
- Split: name, criteria value
- Event: title, date, start time, end time, location, description, attendees
- Snippet: name, body, search
- Booking Page: title, description
- Signature textarea

### Color Palette
- 18 color swatches for label creation

## Seed Data Summary

### Current User
- Alex Morgan, alex.morgan@acmecorp.com, VP of Product at Acme Corp, Business plan

### Contacts (30)
- 8 Acme Corp teammates: Sarah Chen, Priya Sharma, Tom Bradley, Rachel Foster, Nate Patel, Maya Patel, Ben Carter, Patrick O'Neil
- 22 external contacts across companies: DesignHub, Venture Labs, LegalWise, FinancePlus, Creative Agency, Global Health, State University, MediaCo, LogisticsPro, QuantumLab, EuroDesign, FitnessFirst, Consulting Group, BioMed Research, Architects LLP, SportsNews, EdTech Academy, SaaS Platform, Nordic Ventures, TokyoTech, CloudScale, MarketingPro

### Emails (128)
- ~24 inbox/important (person-to-person): roadmap reviews, term sheets, partnerships, infrastructure updates, budget approvals, hiring, brand assets, sponsorships, legal reviews, media coverage
- ~20 inbox/other (automated): GitHub notifications, Slack, Linear, newsletters (The Information, TechCrunch, Morning Brew, Product Hunt, HN, Y Combinator), service alerts (AWS, Datadog, Sentry, PagerDuty, Cloudflare)
- 6 inbox/calendar: Google Calendar reminders, Calendly bookings, event invitations
- ~14 done/archived emails
- 4 reminder/snoozed emails (with future remindAt dates)
- 5 sent emails (with read receipts)
- 2 drafts
- 3 spam emails
- 2 trash emails
- 3 starred emails
- Various emails with: attachments, thread messages, read receipts, labels, auto labels, reply drafting indicators

### Labels (14 user labels)
- Work, Personal, Finance, Clients, Urgent, Travel, Newsletters, Recruiting, Legal, Product, Engineering, Marketing, Receipts, Events

### Auto Labels (8)
- Library: Pitch, Newsletter, Notification, Calendar Invite, Shipping Update
- Custom: Team Update, Investor, Support Ticket

### Splits (5)
- Default: Important, Other, Calendar
- Custom: Feeds, Notifications

### Snippets (12)
- Meeting Follow-up, Introduction, Scheduling Request, [Sales] Product Demo, [Sales] Proposal Follow-up, Out of Office, [HR] Interview Confirmation, Thank You, [Engineering] Bug Report Response, Quick Check-in, [Marketing] Event Invitation, Decline Politely
- Mix of shared/personal, with realistic metrics

### Calendar Events (18)
- Today (March 7): Product Roadmap Review, Weekly Standup, Lunch with Marcus, Board Meeting Prep, 1:1 with Sarah, Yoga Class
- March 8: Sprint Planning, Client Demo, Design Review
- March 9-18: Dentist, All-Hands, Board Meeting, Investor Lunch, OKR Review, Team Offsite, Flight, NYC Meeting, Birthday Dinner

### Booking Pages (3)
- Chat with Alex (30 min, Zoom, active)
- Product Demo (45 min, Zoom, active)
- Quick Sync (15 min, Google Meet, inactive)

### Settings
- Read receipts enabled with team sharing
- Auto reminders in AI mode, default 9 AM
- Auto drafts enabled (follow-up type)
- Smart Send enabled
- Light theme
- Desktop + sound notifications on
- Calendar alerts 10 min before
- Zoom meeting links auto-added
- Eastern Time primary, London secondary
- Keyboard shortcuts enabled
- Signature configured
- Auto archive enabled for Notification label
