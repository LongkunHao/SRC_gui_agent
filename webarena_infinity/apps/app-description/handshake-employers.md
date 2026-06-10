# Handshake — Employers Portal

Handshake is a career services platform connecting college students with employers. This environment covers the **Employers** portal where companies manage job postings, candidates, and campus recruiting.

## Components to Implement

### Employer Dashboard
- Overview metrics: active job postings count, total applicants, pending reviews, upcoming events
- Recent activity feed (new applications, messages, event RSVPs)
- Quick action buttons (post a job, view candidates, schedule event)

### Job Posting Management
- List of job postings with status (draft, active, paused, closed, expired)
- Create new job posting form:
  - Job title, description (rich text), qualifications, responsibilities
  - Job type (full-time, part-time, internship, co-op)
  - Location(s) with remote/hybrid/on-site option
  - Salary range (optional, display toggle)
  - Application deadline
  - Required documents (resume, cover letter, transcript checkboxes)
  - Target schools (search and select specific universities)
  - Target majors / degree levels
  - Work authorization requirements
- Edit, pause, close, duplicate, or delete posting
- Posting analytics (views, applications, conversion rate)

### Candidate Management
- Applicant list per job posting
- Candidate card: name, university, major, GPA, graduation date, application date
- Filter candidates by school, major, GPA, graduation year, status
- Application status pipeline (new, reviewed, phone screen, interview, offered, rejected, hired)
- Move candidate through pipeline stages (drag or dropdown)
- Bulk actions (advance, reject, message)
- View candidate full profile and submitted documents
- Add notes/ratings to candidate

### Messaging
- Message inbox with student/candidate threads
- Compose message to candidate(s) — individual or bulk
- Message templates (create, edit, use templates for common communications)
- Automated messages (application received confirmation, rejection, next steps)

### Event Management
- Create campus event (career fair, info session, workshop, on-campus interview day)
  - Event name, description, date/time, location (virtual link or physical address)
  - Target schools, max attendees
  - Registration requirements
- View event RSVPs and attendee list
- Edit or cancel event
- Check-in attendees

### Employer Profile / Branding
- Company page editor: logo, cover photo, about/description, industry, size, headquarters, culture section, photos, perks & benefits
- Social media links
- Preview company page as students see it

### Analytics & Reports
- Applicant demographics breakdown (school, major, graduation year)
- Pipeline conversion metrics
- Job posting performance comparison
- Diversity metrics (if available)
- Export reports (CSV)

### Team & Permissions
- Team members list (name, email, role)
- Invite new team member
- Role management (admin, recruiter, viewer)
- Remove team member
