# Clio — Matters

Clio is a cloud-based legal practice management platform. This environment covers the **Matters** module, which is the central organizing unit for legal work (a "matter" is essentially a legal case or project).

## Components to Implement

### Matters List View
- Table/list of all matters with columns: matter number, description, client name, practice area, status (open/pending/closed), responsible attorney, originating attorney, date opened
- Search/filter bar (by client, status, practice area, responsible attorney)
- Sort by any column
- Bulk actions (close, archive, assign)
- Pagination

### Matter Detail View
- Header with matter number, description, client name, status badge
- Tabbed interface for sub-sections (details, tasks, time entries, documents, communications, billing)

### Matter Creation / Edit Form
- Client selection (searchable dropdown)
- Matter description and number (auto-generated or custom)
- Practice area selection (dropdown: litigation, corporate, family law, real estate, IP, etc.)
- Responsible attorney and originating attorney assignment
- Status selection (open, pending, closed)
- Open date and close date
- Billing method (hourly, flat fee, contingency)
- Custom fields

### Tasks Sub-tab
- Task list associated with the matter
- Add/edit/delete tasks with name, assignee, due date, priority, status (not started, in progress, complete)
- Task completion checkbox

### Time Entries Sub-tab
- Log of time entries for the matter
- Add time entry: date, duration, description, attorney, activity type
- Edit/delete entries

### Documents Sub-tab
- List of documents attached to the matter
- Upload document functionality
- Document name, type, uploaded by, date

### Communications Sub-tab
- Notes and communication log for the matter
- Add note with date, author, content

### Billing Summary
- Total billable hours and amount
- Outstanding balance
- Billing status indicator
