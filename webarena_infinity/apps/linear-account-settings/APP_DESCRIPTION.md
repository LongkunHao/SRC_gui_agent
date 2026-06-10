# Linear Account Settings

## Summary

A faithful replica of Linear's Account Settings pages, covering four sections: Profile, Preferences, Notifications, and Security & Access. Users can manage their personal profile information, customize workflow preferences, configure notification channels and types, and manage sessions, passkeys, API keys, and authorized OAuth applications.

## Main Sections

### 1. Profile (`#/profile`)
- **Profile card**: Displays user avatar (initials on colored background), full name, username, and email. Each field is inline-editable via a pencil icon that opens a modal.
- **Avatar**: Click to cycle through 8 preset colors. Shows initials from the user's full name.
- **Email change modal**: Includes validation (format check, duplicate check), warning about all-workspace impact.
- **Connected Accounts**: List of third-party integrations (GitHub, GitLab, Slack, Figma, Google). Each shows provider icon, account name, "Connected" status badge. Hover reveals "Disconnect" button which opens confirmation modal.
- **Workspaces**: List of workspaces the user belongs to. Shows workspace avatar (colored initial), name, role, member count. "Leave workspace" button opens confirmation modal.

### 2. Preferences (`#/preferences`)
Four settings groups with dropdowns and toggles:

**General:**
- Default home view (dropdown): All issues, Active issues, Current cycle, Inbox, My Issues, Favorited Views, Favorited Projects
- Display full names (toggle)
- First day of the week (dropdown): Sunday through Saturday
- Convert text emoticons into emojis (toggle)

**Interface and theme:**
- Theme (dropdown): Light, Dark, System, Light - Contrast, Dark - Contrast
- Font size (dropdown): Small, Default, Large
- Use pointer cursor (toggle)

**Desktop application:**
- Open in desktop app (toggle)
- Notification badge (toggle)
- Spell check (toggle)

**Automations and workflows:**
- Auto-assign on create (toggle)
- Auto-assign on started (toggle)
- Git attachment format (dropdown): Title only, Title and repository
- On git branch copy, move to started (toggle)
- On git branch copy, auto-assign (toggle)

### 3. Notifications (`#/notifications`)
**Notification channels** (expandable cards with green/gray status dot):
- Desktop, Mobile, Email, Slack
- Each channel expands to show:
  - Master enable/disable toggle
  - Individual notification type toggles (all disabled when channel is off):
    - Issue assigned to you
    - Status changes
    - Comments on subscribed issues
    - Mentions
    - Project updates
    - Cycle updates
  - Email channel has extra "Delivery preferences":
    - Send urgent immediately (toggle)
    - Delay low priority outside hours (toggle)

**Communications** (separate section):
- Changelogs (toggle)
- DPA updates (toggle)
- Product updates (toggle)

### 4. Security & Access (`#/security`)

**Sessions:**
- List of 8 sessions showing device icon, device name, location, time ago
- Current session highlighted with "Current" badge
- Click to expand: shows IP address, browser, OS, location, sign-in date, last seen date
- Hover reveals "Revoke access" button (not on current session)
- "Revoke all" button at top (revokes all except current)

**Passkeys:**
- List of registered passkeys with name, creation date, last used
- "Add passkey" button opens modal to register new passkey with name
- "Remove" button on each passkey opens confirmation modal

**Personal API keys:**
- List of API keys with label, key prefix (monospace), created date, last used, expiry
- "Create key" button opens modal with label input
- "Revoke" button on each key opens confirmation modal

**Authorized applications:**
- List of OAuth apps with name, description, authorized date, last accessed, permission badges
- "Revoke access" button on each app opens confirmation modal

## Data Model

### Entities and Fields

**currentUser:**
- id, fullName, username, email, avatarUrl, avatarColor, timezone, createdAt, updatedAt

**workspaces[] (3 items):**
- id, name, slug, role, memberCount, joinedAt, avatarColor, urlKey

**connectedAccounts[] (5 items):**
- id, provider, providerIcon, accountName, accountEmail, connectedAt, status, scopes[]

**preferences (object):**
- defaultHomeView, displayFullNames, firstDayOfWeek, convertTextEmojis
- interfaceTheme, fontSize, usePointerCursor
- openInDesktopApp, desktopNotificationBadge, enableSpellCheck
- autoAssignOnCreate, autoAssignOnStarted, gitAttachmentFormat
- onGitBranchCopyMoveToStarted, onGitBranchCopyAutoAssign

**notificationSettings (object):**
- desktop/mobile/email/slack: { enabled, issueAssigned, issueStatusChanged, issueCommented, issueMentioned, projectUpdated, cycleUpdated }
- email also has: sendUrgentImmediately, delayLowPriorityOutsideHours
- Top-level: receiveChangelogs, receiveDpaUpdates, receiveProductUpdates

**sessions[] (8 items):**
- id, deviceName, deviceType, browser, os, ipAddress, location, lastSeenAt, signedInAt, isCurrent

**passkeys[] (3 items):**
- id, name, createdAt, lastUsedAt, credentialType

**apiKeys[] (5 items):**
- id, label, keyPrefix, createdAt, lastUsedAt, expiresAt

**authorizedApps[] (6 items):**
- id, name, description, icon, authorizedAt, lastAccessedAt, permissions[]

## Navigation

- Sidebar with 4 items: Profile, Preferences, Notifications, Security & Access
- URL hash routing: `#/profile`, `#/preferences`, `#/notifications`, `#/security`
- Default view: Profile

## Form Controls Summary

**Dropdowns (5):**
| ID | Current Value | Options |
|---|---|---|
| pref-home-view | Active issues | All issues, Active issues, Current cycle, Inbox, My Issues, Favorited Views, Favorited Projects |
| pref-first-day | Monday | Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday |
| pref-theme | System | Light, Dark, System, Light - Contrast, Dark - Contrast |
| pref-font-size | Default | Small, Default, Large |
| pref-git-format | Title only | Title only, Title and repository |

**Toggles (22):**
| ID | Default |
|---|---|
| pref-display-full-names | ON |
| pref-convert-emojis | ON |
| pref-pointer-cursor | OFF |
| pref-open-desktop | ON |
| pref-notif-badge | ON |
| pref-spell-check | ON |
| pref-auto-assign-create | OFF |
| pref-auto-assign-started | OFF |
| pref-git-move-started | ON |
| pref-git-auto-assign | ON |
| notif-desktop-enabled | ON |
| notif-mobile-enabled | ON |
| notif-email-enabled | ON |
| notif-slack-enabled | OFF |
| notif-changelogs | ON |
| notif-dpa | ON |
| notif-product | OFF |
| notif-email-urgent | ON |
| notif-email-delay-low | ON |
| + per-channel notification type toggles (6 types x 4 channels = 24) |

## Seed Data Summary

**User:** Alex Morgan (alexmorgan), alex.morgan@acmecorp.io

**Workspaces (3):**
- Acme Corp (Admin, 47 members)
- Side Project Labs (Member, 8 members)
- Open Source Collective (Member, 124 members)

**Connected Accounts (5):** GitHub, GitLab, Slack, Figma, Google

**Sessions (8):**
- Chrome on macOS (current), Safari on iPhone, Linear Desktop on macOS, Firefox on Windows, Chrome on Linux, Safari on iPad, Chrome on Android, Edge on Windows

**Passkeys (3):** MacBook Pro Touch ID, YubiKey 5C NFC, iPhone Face ID

**API Keys (5):** CI/CD Pipeline, Slack Bot Integration, Data Export Script, Mobile App Testing, Monitoring Dashboard

**Authorized Apps (6):** Raycast, Notion Integration, Zapier, Linear Exporter, Screenful, Marker.io
