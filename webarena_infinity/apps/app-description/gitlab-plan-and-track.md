# GitLab — Plan and Track

GitLab is a DevOps platform that provides source code management, CI/CD, and project planning tools. This environment covers the **Plan and Track** features — GitLab's project management and issue tracking capabilities.

## Components to Implement

### Issues List
- Table/list of issues with columns: title, status (open/closed), author, assignee(s), labels, milestone, weight, due date, created date, updated date
- Filter bar: by status, author, assignee, label, milestone, iteration, weight, confidential
- Search by title or description keyword
- Sort by created date, updated date, due date, priority, popularity, weight
- Bulk actions (close, assign, label, move to milestone)
- Pagination

### Issue Detail View
- Title (editable inline)
- Description with Markdown editor (supports checklists, code blocks, mentions, emoji)
- Sidebar with metadata:
  - Assignee(s) — searchable dropdown, multi-select
  - Labels — searchable dropdown, multi-select, color-coded chips
  - Milestone — dropdown selection
  - Iteration — dropdown selection
  - Weight — numeric input
  - Due date — date picker
  - Confidential toggle
  - Time tracking (estimated vs spent)
- Activity feed (comments, status changes, label changes, assignment changes)
- Comment box with Markdown editor
- Related issues / linked issues (blocking, blocked by, related to)
- Close / reopen button

### Issue Creation Form
- Title (required)
- Description (Markdown editor)
- Assignee(s), labels, milestone, iteration, weight, due date, confidential — all optional
- Issue type (issue, incident, task)
- Template selection (bug report, feature request, custom templates)

### Labels Management
- List of project labels: name, description, color swatch
- Create new label (name, description, color picker)
- Edit / delete label
- Label groups / scoped labels (e.g., `priority::high`, `status::in-progress`)
- Promote to group label

### Milestones
- List of milestones: title, due date, progress bar (open vs closed issues), status (active/closed)
- Create milestone (title, description, start date, due date)
- Edit / close / delete milestone
- Milestone detail view: list of issues in the milestone, completion percentage

### Boards (Kanban)
- Kanban board view with columns representing labels or statuses
- Default columns: Open, Closed (plus label-based lists)
- Add / remove / reorder board lists
- Drag-and-drop issues between columns
- Issue cards showing title, labels, assignee avatar, weight
- Filter board by assignee, label, milestone, iteration
- Create new issue directly from a board column

### Iterations (Sprints)
- List of iterations with title, start date, end date, status (upcoming/current/closed)
- Create iteration cadence (duration, auto-schedule)
- Create individual iteration (title, start date, end date)
- Iteration detail: assigned issues, burndown chart, completion stats
- Assign issues to iterations from issue detail or bulk actions

### Epics
- List of epics: title, status (open/closed), progress (child issues/epics completion)
- Create epic (title, description, start date, due date, labels, confidential)
- Epic detail view: description, child issues list, child epics (hierarchy), roadmap bar
- Add/remove child issues or child epics
- Epic tree / hierarchy visualization

### Roadmap
- Timeline/Gantt view of epics and milestones
- Horizontal bars showing epic duration (start to due date)
- Filter by label, author, milestone
- Zoom level controls (weeks, months, quarters)
- Drag to adjust epic dates

### Time Tracking
- Log time spent on an issue (via quick action or sidebar input)
- Time estimate input
- Time spent vs estimated comparison bar
- Time tracking report per milestone or label
- Summary: total estimated, total spent, remaining

### Quick Actions
- Slash commands in comments: `/assign @user`, `/label ~bug`, `/milestone %v1.0`, `/close`, `/weight 3`, `/due 2026-04-01`, `/estimate 2h`, `/spend 1h30m`
- Autocomplete for users, labels, milestones in slash commands

### Notifications & Subscriptions
- Subscribe/unsubscribe to issue notifications
- Notification level per project (global, watch, on mention, disabled)
- Notification feed (assigned, mentioned, status changes)
