# Handshake Career Exploration

## Summary

A faithful replica of Handshake's student-facing career exploration platform. The app allows a student (Maya Chen, Stanford University CS '27) to explore career opportunities through a social feed, job search, employer discovery, event browsing, employer messaging, career center appointments, Q&A community, and career interest management. All features are based on Handshake's official student/alumni documentation for career exploration.

## Main Sections / Pages

The app uses hash-based routing (`#/page`) with a persistent left sidebar for navigation.

### 1. Feed (`#/feed`)
- Social feed showing posts from employers and students
- **Filters**: All, Employers, Top Posts, Intros (filter chips at top)
- **Tabs**: Feed (main feed), Saved (bookmarked posts)
- **Create Post**: Click "Share something with the community..." box to open a modal
  - Text content (max 3,000 characters with live counter)
  - Audience selector: "Everyone on Handshake" or "People at your school"
  - Only available when profile visibility is "Community"
- **Post Interactions**: Like (heart icon), Comment (bubble icon), Bookmark/Save (bookmark icon)
- **Comments**: View all comments on a post via modal, post new comments (optionally anonymous)
- **Employer posts**: Show employer name (clickable to brand page), Follow button if not following

### 2. Jobs (`#/jobs`)
- Searchable, filterable list of 30 job postings
- **Search**: Full-text search across title, description, and company name
- **Filters** (custom dropdowns):
  - Job Type: Internship, Full-time, Part-time
  - Location: 10 major US cities
  - Label: School-defined labels (STEM, Top Employer, Finance, etc.)
- **Job cards**: Show title, company avatar, location, type, salary, labels, posted time
- **Save/unsave**: Bookmark icon on each job card
- **Pagination info**: "Showing X of Y results"

### 3. Job Detail (`#/job/{id}`)
- Full job posting with description, qualifications, metadata
- Save/unsave button
- Employer mini-card with follow/unfollow
- Metadata: location, type, salary, posted date, deadline, applicant count
- Labels and role tags displayed

### 4. Employers (`#/employers`)
- Grid of 20 employer cards
- **Search**: By name, industry, or location
- **Cards show**: Logo avatar, name, industry, location, size, type, follower count
- **Follow/unfollow**: Button on each card

### 5. Employer Detail / Brand Page (`#/employer/{id}`)
- **Header**: Banner with logo, name, industry, location, size, type, follower count, website, Follow button
- **Tabs**: Overview, Jobs, Posts
- **Overview tab**:
  - About section (company description)
  - Work Life section (benefits, culture)
  - Testimonials (employee reviews with name, role, school, major, grad year)
  - Recent Jobs (up to 3, link to full list)
  - Upcoming Events (if any)
  - Recent Posts (up to 2, link to full list)
  - Affiliated Employers (badge chips)
- **Jobs tab**: All active jobs from this employer
- **Posts tab**: All feed posts from this employer

### 6. Events (`#/events`)
- List of 12 events (career fairs, info sessions, tech talks, workshops, panels)
- **Search**: Full-text across title, employer, description
- **Filters**:
  - Event Type dropdown: All Types, Info Session, Career Fair, Tech Talk, Workshop, Panel, Speaker Event, Virtual Session
  - Virtual only checkbox
- **Sections**: Upcoming Events, Past Events
- **Event cards**: Date badge, title, employer, type, time, location, labels, RSVP count, RSVP/Cancel button
- Virtual events labeled with green "Virtual" badge

### 7. Event Detail (`#/event/{id}`)
- Full event info: title, employer, date, time, location, type, attendee count, description
- RSVP / Cancel RSVP button
- Link to employer profile

### 8. Messages (`#/messages`)
- Inbox of 12 employer messages
- **Filter tabs**: All, Unread (with count), Top Match
- **Mark all as read** button
- **Message rows**: Employer avatar, sender name, Top Match badge (gold), subject, preview, time, unread dot
- Unread messages highlighted with distinct background

### 9. Message Detail (`#/message/{id}`)
- Full message with employer avatar, subject, from line, Top Match badge, timestamp
- Full message body rendered
- Link to employer profile

### 10. Career Center / Appointments (`#/career-center`)
- **"Schedule a New Appointment" button** at top
- **Sections**: Upcoming Appointments, Past Appointments
- **Appointment cards**: Date/time, type, staff name, duration, medium, category, status badge
- **Status badges**: Requested (yellow), Approved (green), Completed (blue), Declined (red), Cancelled (red)

### 11. Appointment Detail (`#/appointment/{id}`)
- Full appointment info: type, category, date, time, duration, medium, location, staff
- Status badge
- Details section (what the student wants help with)
- Virtual appointment: "Start Video Appointment" button (disabled, available 5 min before)
- Comments thread (back-and-forth with career advisor)
- Add comment textarea
- Cancel button (for requested/approved appointments)

### 12. Schedule Appointment (`#/schedule-appointment`)
- Multi-step form:
  1. **Category** dropdown (6 categories: Career Counseling, Job & Internship Search, Resume & Cover Letter, Interview Preparation, Graduate School, Networking & Professional Development)
  2. **Appointment Type** dropdown (populated based on category, 3 types each)
  3. **Staff Member** dropdown (optional, 6 staff members)
  4. **Date** grid (15 available dates, filtered by staff availability)
  5. **Time** grid (shown after date selection)
  6. **Medium** dropdown: In Person, Virtual on Handshake, Phone
  7. **Details** textarea
- Submit button enabled only when all required fields filled
- Creates appointment with "requested" status

### 13. Q&A Community (`#/qa`)
- **Tabs**: All Questions, My Questions, My Answers
- **Search**: Across questions and answers
- **Ask a Question**: Textarea + Submit button (creates pending question)
- **Question cards**: Author, school, major, grad year, question text, answer count, views, time
- Pending questions show yellow "Pending" badge

### 14. Question Detail (`#/question/{id}`)
- Full question with author info, text, view count, answer count
- **Answers list**: Each answer shows author (or "Anonymous"), school, major, grad year, text, helpful count
- **Mark as Helpful** button on each answer
- Pending answers shown with dashed border
- **Submit Answer form**:
  - Answer textarea
  - Visibility radio buttons: Fully visible (name, photo, school, year, major) or Semi-anonymous (hide name/photo)
  - Submit button

### 15. Profile (`#/profile`)
- **Profile card**: Avatar, name, school, major, grad year, location
- **About section**: Bio, email, phone, LinkedIn, website (each with Edit button opening modal)
- **Looking For section**: Current status, roles, industries, locations (tag chips), "Edit Career Interests" button
- **Profile Visibility dropdown**: Community, Employers, Private
- **Work Experience**: Cards with title, company, dates, description
- **Skills**: Tag chips
- **Organizations**: Tag chips

### 16. Career Interests (`#/career-interests`)
- Comprehensive form to update career preferences:
  - **Job Type** checkboxes: Full-time, Internship, Part-time, On-campus
  - **How can Handshake help?** checkboxes: Job, Internship, Grad school, Events, Network, Exploring
  - **Post-graduation** checkboxes: Working, Grad school, Gap year, Military, Volunteering, Fellowship, Not sure
  - **Job Roles**: Tag chips with dropdown to add (26 role options)
  - **Locations**: Tag chips with dropdown to add (20 location options)
  - **Career Community** dropdown (10 options)
  - **Industries** checkboxes (24 industry options)
  - **Job Functions** checkboxes (18 function options)
  - **Expected Graduation Date** dropdown (8 options)
  - **Save My Career Interests** button (green)

## Data Model

### CurrentUser (Student)
- `id`, `firstName`, `lastName`, `fullName`, `email`, `school`, `major`, `minor`, `graduationYear`, `expectedGraduation`, `gpa`
- `profileVisibility` (Community | Employers | Private)
- `avatarColor`, `bio`, `phone`, `location`, `linkedinUrl`, `websiteUrl`
- `careerInterests`: { jobTypes[], helpWith[], postGraduation[], roles[], locations[], careerCommunity, industries[], jobFunctions[], expectedGraduationDate }
- `lookingFor` (current job search status)
- `skills[]`, `workExperience[]`, `education[]`, `organizations[]`
- `followedEmployerIds[]`, `savedPostIds[]`, `savedJobIds[]`
- `createdAt`, `updatedAt`

### Employer (20 entities)
- `id`, `name`, `industry`, `location`, `size`, `type`, `website`, `isPremium`
- `logoColor`, `followCount`
- `about`, `workLife`
- `testimonials[]`: { name, role, school, major, gradYear, text }
- `gallery[]`, `affiliatedEmployers[]`

### Job (30 entities)
- `id`, `employerId`, `title`, `type` (Internship/Full-time/Part-time), `location`, `salary`
- `postedAt`, `deadline`, `roles[]`, `labels[]`, `status` (active/closed)
- `description`, `qualifications`, `applicants`

### FeedPost (20 entities)
- `id`, `authorType` (employer/student), `authorId`, `authorName`, `authorAvatarColor`
- `content`, `audience` (everyone/school), `likes`, `bookmarked`
- `comments[]`: { id, authorName, authorSchool, authorAvatarColor, text, createdAt, isAnonymous }
- `hasImage`, `hasVideo`, `createdAt`

### Event (12 entities)
- `id`, `employerId`, `employerName`, `title`, `type`
- `date`, `time`, `location`, `isVirtual`
- `description`, `rsvpCount`, `rsvped`, `status` (upcoming/past)
- `labels[]`

### Appointment (8 entities)
- `id`, `category`, `type`, `staffId`, `staffName`
- `date`, `time`, `duration`, `medium` (In Person/Virtual on Handshake/Phone)
- `location`, `status` (requested/approved/completed/declined/cancelled)
- `details`, `comments[]`: { author, text, createdAt }
- `createdAt`

### AppointmentCategory (6 entities)
- `id`, `name`, `types[]` (3 appointment types each)

### AppointmentStaff (6 entities)
- `id`, `name`, `title`, `specialties[]`

### AvailableSlots (15 date slots)
- `date`, `times[]`, `staffAvailable[]`

### QAQuestion (12 entities)
- `id`, `authorName`, `authorSchool`, `authorMajor`, `authorGradYear`, `authorAvatarColor`
- `question`, `status` (pending/approved), `createdAt`, `views`
- `answers[]`: { id, authorName, authorSchool, authorMajor, authorGradYear, authorAvatarColor, text, visibility (full/semi-anonymous), status, createdAt, helpful }

### Message (12 entities)
- `id`, `employerId`, `employerName`, `subject`, `body`
- `isTopMatch`, `isRead`, `createdAt`, `type` (recruiting/promotional/event)

## Navigation Structure

- **Sidebar** (always visible, left side):
  - Feed, Jobs, Employers, Events, Messages (with unread count badge), Career Center, Q&A
  - User avatar + name at bottom (click to go to Profile)
- **Detail pages**: Back button returns to parent list
- **Profile** -> Career Interests (separate page)
- **Career Center** -> Schedule Appointment (separate page)

## Available Form Controls, Dropdowns, Toggles

### Custom Dropdowns (14 total)
| ID | Location | Options |
|----|----------|---------|
| `jobTypeFilter` | Jobs page | (empty), Internship, Full-time, Part-time |
| `jobLocationFilter` | Jobs page | (empty), 10 US cities |
| `jobLabelFilter` | Jobs page | (empty), 21 school labels |
| `eventTypeFilter` | Events page | All Types + 7 event types |
| `profileVisibility` | Profile page | Community, Employers, Private |
| `addRoleDropdown` | Career Interests | 26 roles (minus already selected) |
| `addLocationDropdown` | Career Interests | 20 locations (minus already selected) |
| `careerCommunity` | Career Interests | 10 career communities |
| `expectedGradDate` | Career Interests | 8 graduation dates |
| `schedCategory` | Schedule Appointment | 6 appointment categories |
| `schedType` | Schedule Appointment | 3 types (per category) |
| `schedStaff` | Schedule Appointment | (empty) + 6 staff names |
| `schedMedium` | Schedule Appointment | In Person, Virtual on Handshake, Phone |
| `postAudience` | Create Post modal | Everyone on Handshake, People at your school |

### Checkboxes
- Job Type (4): Full-time, Internship, Part-time, On-campus
- How can Handshake help (6): Job, Internship, Grad school, Events, Network, Exploring
- Post-graduation (7): Working, Grad school, Gap year, Military, Volunteering, Fellowship, Not sure
- Industries (24): Technology, AI, Finance, Healthcare Tech, Consulting, Education, etc.
- Job Functions (18): Engineering, Product Management, Data Analytics, Design, etc.
- Virtual only (Events page): single checkbox
- Anonymous comment (Comments modal): single checkbox

### Radio Buttons
- Answer visibility: Fully visible / Semi-anonymous (Q&A question detail)

### Text Inputs / Textareas
- Job search, Employer search, Event search, Q&A search (search inputs with icons)
- Create post content (textarea, 3000 char limit)
- New comment (textarea)
- Appointment details (textarea)
- New question (textarea)
- New answer (textarea)
- Profile field editing (input/textarea in modal)
- Appointment comment (textarea)

### Buttons
- Follow / Following (employers)
- Like / Bookmark (feed posts)
- Save / Saved (jobs)
- RSVP / Cancel RSVP (events)
- Mark all as read (messages)
- Schedule a New Appointment
- Request Appointment (form submission)
- Cancel Appointment
- Submit Question / Submit Answer
- Mark as Helpful
- Save My Career Interests
- Various Edit buttons on profile fields

## Seed Data Summary

### Current User: Maya Chen
- Stanford University, CS '27, GPA 3.82
- Following 7 employers, 3 saved posts, 5 saved jobs
- Work experience: Meta SWE Intern, Stanford AI Lab RA, Figma Design Intern
- Career interests: Internship/Part-time, SWE/PM/DS/UX roles, Tech/AI/Finance/HealthTech industries
- Profile visibility: Community

### 20 Employers
- Big Tech: Google, Microsoft, Apple, Meta, Amazon, Salesforce
- Finance: JPMorgan Chase, Goldman Sachs
- Consulting: McKinsey, Bain, Deloitte
- Other Tech: Stripe, Anthropic, Palantir, Spotify, Tesla, Epic Systems
- Other: Nike, Teach For America, Startup Grind Labs (early stage startup)
- Follower counts range from 420 to 52,300

### 30 Jobs
- 25 internships, 5 full-time positions
- Across 15 employers
- 3 closed positions, 27 active
- Salaries from $33K/yr to $210K/yr; intern rates $38-60/hr
- Applicant counts from 89 to 5,210
- Labels: STEM, Top Employer, Finance, Consulting, AI/ML, Design, etc.

### 20 Feed Posts
- 9 employer posts, 11 student posts
- Like counts from 89 to 534
- 10 posts have comments (1-3 comments each)
- Content: job announcements, interview tips, career advice, intro posts

### 12 Events
- Types: Career Fair (2), Info Session (2), Tech Talk (2), Workshop (3), Panel (1), Speaker Event (1), Virtual Session (1)
- 10 upcoming, 2 past
- 4 virtual events
- RSVP counts from 38 to 1,256

### 8 Appointments
- Statuses: 2 requested, 1 approved, 4 completed, 1 with pending case interview prep
- Categories: Career Counseling, Job & Internship Search, Resume & Cover Letter, Interview Preparation
- Staff: 6 career center advisors with different specialties
- 15 available appointment date slots for scheduling

### 12 Q&A Questions
- Topics: interview processes, salary negotiation, career transitions, diversity programs
- 1-2 answers each (one question has 0 answers)
- View counts from 423 to 1,567
- Helpfulness ratings from 29 to 89

### 12 Messages
- From 11 different employers
- 4 unread, 8 read
- 3 with Top Match badge
- Types: recruiting, promotional, event invitations
