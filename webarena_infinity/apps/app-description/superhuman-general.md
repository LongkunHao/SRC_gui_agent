# Superhuman — Email Client

Superhuman is a high-performance email client designed for speed and productivity. This environment covers the **core email experience** including inbox, compose, and settings.

## Components to Implement

### Inbox / Email List
- List of email conversations with sender, subject, snippet, timestamp
- Unread/read visual distinction (bold vs normal)
- Star/favorite toggle per email
- Labels/tags displayed as colored chips
- Keyboard-navigable list (j/k to move, enter to open)
- Split view: email list on left, selected email preview on right

### Email Detail View
- Full email thread display (conversation view)
- Sender info, recipients (to, cc, bcc), timestamp
- Email body (HTML rendered)
- Attachment list with download
- Reply, Reply All, Forward action buttons

### Compose / Reply
- New email compose modal/panel
- To, CC, BCC recipient fields with autocomplete from contacts
- Subject line
- Rich text editor for email body
- Attachment upload
- Send, schedule send, discard actions
- Drafts auto-save

### Search
- Global search bar
- Search by sender, subject, keyword, date range, has attachment
- Search results list with highlighting

### Labels / Folders
- Sidebar with inbox, sent, drafts, starred, trash, spam, archive
- Custom labels with color coding
- Create/edit/delete labels
- Apply labels to emails (single or bulk)

### Snooze & Reminders
- Snooze email to reappear at a specific date/time
- Preset snooze options (later today, tomorrow, next week, custom)
- Follow-up reminder setting

### Settings
- Account info and signature editor
- Auto-advance behavior (after archive/delete: next, previous, list)
- Keyboard shortcut reference
- Notification preferences
- Theme (light/dark)
- Read receipt and send delay configuration
