# Gmail — Organize and Manage

Gmail is Google's email service. This environment covers the **Organize and Manage** features for email organization, filtering, and inbox management.

## Components to Implement

### Labels
- Sidebar showing system labels (Inbox, Starred, Snoozed, Sent, Drafts, Trash, Spam) and custom labels
- Create new label (name, optional nesting under parent label)
- Edit label (rename, nest/unnest)
- Delete label
- Show/hide labels in sidebar and label list
- Label color coding (background + text color selection)
- Apply label to email(s) — single or bulk

### Filters and Blocked Addresses
- List of existing filters with summary (from, to, subject, has words, actions)
- Create new filter:
  - Criteria: from, to, subject, has the words, doesn't have, size, has attachment, date within
  - Actions: skip inbox, mark as read, star it, apply label, forward, delete, never send to spam, always/never mark important, categorize as
- Edit or delete existing filter
- Import/export filters
- Blocked addresses list with add/remove

### Inbox Categories / Tabs
- Inbox type selection (default, important first, unread first, starred first, priority inbox, multiple inboxes)
- Category tabs configuration: enable/disable tabs (Primary, Social, Promotions, Updates, Forums)
- Include starred in Primary toggle
- Bundling settings per category

### Stars and Importance
- Star presets configuration (select which star types to use: yellow star, blue star, red bang, orange guillemet, etc.)
- Star rotation order
- Importance markers (show/hide importance markers)
- Override importance filters (use my actions to predict, don't use actions)

### Snooze
- Snooze email to return at a future date/time
- Preset snooze options (later today, tomorrow, this weekend, next week, custom)
- View snoozed emails list

### Multiple Inbox Configuration (if selected)
- Section configuration (up to 5 sections)
- Per-section search query, name, and max messages
- Section position (right of inbox or below inbox)

### Auto-Advance
- After archive/delete behavior: show next conversation, previous conversation, or conversation list

### Nudges
- Suggest emails to reply to toggle
- Suggest emails to follow up on toggle

### Email Threading
- Conversation view on/off toggle

### Density & Display
- Display density: default, comfortable, compact
- Reading pane position: no split, right of inbox, below inbox
