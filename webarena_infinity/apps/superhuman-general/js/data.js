// ============================================================
// data.js — Rich, realistic seed data for Superhuman Mail
// ============================================================
const SEED_DATA_VERSION = 1;

// ---- Current User ----
const CURRENT_USER = {
    id: 'user_1',
    name: 'Alex Morgan',
    email: 'alex.morgan@acmecorp.com',
    avatarColor: '#6C4FF7',
    plan: 'business',
    timezone: 'America/New_York',
    signature: 'Best,\nAlex Morgan\nVP of Product, Acme Corp'
};

// ---- Contacts ----
const CONTACTS = [
    { id: 'ct_01', name: 'Sarah Chen', email: 'sarah.chen@acmecorp.com', avatarColor: '#E54D89', company: 'Acme Corp', isFrequent: true, isTeammate: true },
    { id: 'ct_02', name: 'Marcus Williams', email: 'marcus.w@designhub.io', avatarColor: '#34A853', company: 'DesignHub', isFrequent: true, isTeammate: false },
    { id: 'ct_03', name: 'Emily Rodriguez', email: 'emily.r@venturelabs.co', avatarColor: '#FBBC04', company: 'Venture Labs', isFrequent: true, isTeammate: false },
    { id: 'ct_04', name: 'James O\'Brien', email: 'james.obrien@legalwise.com', avatarColor: '#4285F4', company: 'LegalWise', isFrequent: false, isTeammate: false },
    { id: 'ct_05', name: 'Priya Sharma', email: 'priya.sharma@acmecorp.com', avatarColor: '#9C27B0', company: 'Acme Corp', isFrequent: true, isTeammate: true },
    { id: 'ct_06', name: 'David Kim', email: 'david.kim@financeplus.com', avatarColor: '#FF5722', company: 'FinancePlus', isFrequent: true, isTeammate: false },
    { id: 'ct_07', name: 'Lisa Nakamura', email: 'lisa.n@creativeagency.co', avatarColor: '#009688', company: 'Creative Agency', isFrequent: false, isTeammate: false },
    { id: 'ct_08', name: 'Tom Bradley', email: 'tom.bradley@acmecorp.com', avatarColor: '#795548', company: 'Acme Corp', isFrequent: true, isTeammate: true },
    { id: 'ct_09', name: 'Ana Gutierrez', email: 'ana.g@globalhealth.org', avatarColor: '#E91E63', company: 'Global Health', isFrequent: true, isTeammate: false },
    { id: 'ct_10', name: 'Robert Singh', email: 'robert.singh@university.edu', avatarColor: '#3F51B5', company: 'State University', isFrequent: false, isTeammate: false },
    { id: 'ct_11', name: 'Michelle Park', email: 'michelle.park@mediaco.tv', avatarColor: '#FF9800', company: 'MediaCo', isFrequent: true, isTeammate: false },
    { id: 'ct_12', name: 'Carlos Mendez', email: 'carlos.m@logisticspro.net', avatarColor: '#607D8B', company: 'LogisticsPro', isFrequent: false, isTeammate: false },
    { id: 'ct_13', name: 'Rachel Foster', email: 'rachel.foster@acmecorp.com', avatarColor: '#8BC34A', company: 'Acme Corp', isFrequent: true, isTeammate: true },
    { id: 'ct_14', name: 'Kevin Zhao', email: 'kevin.zhao@quantumlab.tech', avatarColor: '#00BCD4', company: 'QuantumLab', isFrequent: true, isTeammate: false },
    { id: 'ct_15', name: 'Sophie Laurent', email: 'sophie.l@eurodesign.fr', avatarColor: '#673AB7', company: 'EuroDesign', isFrequent: false, isTeammate: false },
    { id: 'ct_16', name: 'Nate Patel', email: 'nate.patel@acmecorp.com', avatarColor: '#2196F3', company: 'Acme Corp', isFrequent: true, isTeammate: true },
    { id: 'ct_17', name: 'Hannah Brooks', email: 'hannah.b@fitnessfirst.com', avatarColor: '#F44336', company: 'FitnessFirst', isFrequent: false, isTeammate: false },
    { id: 'ct_18', name: 'Omar Al-Rashid', email: 'omar.ar@consulting.group', avatarColor: '#CDDC39', company: 'Consulting Group', isFrequent: false, isTeammate: false },
    { id: 'ct_19', name: 'Jennifer Wu', email: 'jennifer.wu@biomedresearch.com', avatarColor: '#FF6F00', company: 'BioMed Research', isFrequent: true, isTeammate: false },
    { id: 'ct_20', name: 'Daniel Thompson', email: 'daniel.t@architectsllp.com', avatarColor: '#455A64', company: 'Architects LLP', isFrequent: false, isTeammate: false },
    { id: 'ct_21', name: 'Maya Patel', email: 'maya.patel@acmecorp.com', avatarColor: '#7B1FA2', company: 'Acme Corp', isFrequent: true, isTeammate: true },
    { id: 'ct_22', name: 'Chris Evans', email: 'chris.evans@sportsnews.com', avatarColor: '#1B5E20', company: 'SportsNews', isFrequent: false, isTeammate: false },
    { id: 'ct_23', name: 'Aisha Mohammed', email: 'aisha.m@edtech.academy', avatarColor: '#BF360C', company: 'EdTech Academy', isFrequent: false, isTeammate: false },
    { id: 'ct_24', name: 'Ryan Cooper', email: 'ryan.cooper@saasplatform.io', avatarColor: '#0097A7', company: 'SaaS Platform', isFrequent: true, isTeammate: false },
    { id: 'ct_25', name: 'Lena Johansson', email: 'lena.j@nordicventures.se', avatarColor: '#5D4037', company: 'Nordic Ventures', isFrequent: false, isTeammate: false },
    { id: 'ct_26', name: 'Ben Carter', email: 'ben.carter@acmecorp.com', avatarColor: '#00695C', company: 'Acme Corp', isFrequent: true, isTeammate: true },
    { id: 'ct_27', name: 'Yuki Tanaka', email: 'yuki.t@tokyotech.jp', avatarColor: '#AD1457', company: 'TokyoTech', isFrequent: false, isTeammate: false },
    { id: 'ct_28', name: 'Michael Foster', email: 'michael.f@cloudscale.dev', avatarColor: '#1565C0', company: 'CloudScale', isFrequent: true, isTeammate: false },
    { id: 'ct_29', name: 'Diana Reyes', email: 'diana.r@marketingpro.co', avatarColor: '#C62828', company: 'MarketingPro', isFrequent: true, isTeammate: false },
    { id: 'ct_30', name: 'Patrick O\'Neil', email: 'patrick.oneil@acmecorp.com', avatarColor: '#33691E', company: 'Acme Corp', isFrequent: true, isTeammate: true }
];

// ---- Labels ----
const LABELS = [
    // System folders
    { id: 'INBOX', name: 'Inbox', type: 'system', color: null },
    { id: 'DONE', name: 'Done', type: 'system', color: null },
    { id: 'REMINDERS', name: 'Reminders', type: 'system', color: null },
    { id: 'SENT', name: 'Sent', type: 'system', color: null },
    { id: 'DRAFTS', name: 'Drafts', type: 'system', color: null },
    { id: 'SPAM', name: 'Spam', type: 'system', color: null },
    { id: 'TRASH', name: 'Trash', type: 'system', color: null },
    { id: 'STARRED', name: 'Starred', type: 'system', color: null },
    { id: 'OPENS', name: 'Recent Opens', type: 'system', color: null },
    { id: 'SNIPPETS', name: 'Snippets', type: 'system', color: null },

    // User labels
    { id: 'label_1', name: 'Work', type: 'user', color: '#6C4FF7' },
    { id: 'label_2', name: 'Personal', type: 'user', color: '#34A853' },
    { id: 'label_3', name: 'Finance', type: 'user', color: '#FF9800' },
    { id: 'label_4', name: 'Clients', type: 'user', color: '#E54D89' },
    { id: 'label_5', name: 'Urgent', type: 'user', color: '#F44336' },
    { id: 'label_6', name: 'Travel', type: 'user', color: '#00BCD4' },
    { id: 'label_7', name: 'Newsletters', type: 'user', color: '#9C27B0' },
    { id: 'label_8', name: 'Recruiting', type: 'user', color: '#795548' },
    { id: 'label_9', name: 'Legal', type: 'user', color: '#607D8B' },
    { id: 'label_10', name: 'Product', type: 'user', color: '#2196F3' },
    { id: 'label_11', name: 'Engineering', type: 'user', color: '#4CAF50' },
    { id: 'label_12', name: 'Marketing', type: 'user', color: '#E91E63' },
    { id: 'label_13', name: 'Receipts', type: 'user', color: '#CDDC39' },
    { id: 'label_14', name: 'Events', type: 'user', color: '#FF5722' }
];

// ---- Auto Labels ----
const AUTO_LABELS = [
    { id: 'al_1', name: 'Pitch', type: 'library', enabled: true, criteria: { ai: 'Sales or partnership pitches' } },
    { id: 'al_2', name: 'Newsletter', type: 'library', enabled: true, criteria: { ai: 'Email newsletters and digests' } },
    { id: 'al_3', name: 'Notification', type: 'library', enabled: true, criteria: { ai: 'Automated notifications from services' } },
    { id: 'al_4', name: 'Calendar Invite', type: 'library', enabled: true, criteria: { ai: 'Calendar invitations and scheduling' } },
    { id: 'al_5', name: 'Shipping Update', type: 'library', enabled: false, criteria: { ai: 'Package and delivery notifications' } },
    { id: 'al_6', name: 'Team Update', type: 'custom', enabled: true, criteria: { from: '@acmecorp.com', ai: 'Team status updates and standup notes' } },
    { id: 'al_7', name: 'Investor', type: 'custom', enabled: true, criteria: { from: 'venturelabs.co OR nordicventures.se', subject: 'funding OR investment OR round' } },
    { id: 'al_8', name: 'Support Ticket', type: 'custom', enabled: false, criteria: { from: 'support@', subject: 'ticket OR case OR issue' } }
];

// ---- Splits ----
const SPLITS = [
    { id: 'split_important', name: 'Important', position: 0, isDefault: true, criteria: { type: 'important' }, description: 'Person-to-person messages' },
    { id: 'split_other', name: 'Other', position: 1, isDefault: true, criteria: { type: 'other' }, description: 'Automated and mailing list emails' },
    { id: 'split_calendar', name: 'Calendar', position: 2, isDefault: true, criteria: { type: 'calendar' }, description: 'Calendar invites and scheduling' },
    { id: 'split_feeds', name: 'Feeds', position: 3, isDefault: false, criteria: { autoLabel: 'Newsletter' }, description: 'Newsletters and digests' },
    { id: 'split_notifications', name: 'Notifications', position: 4, isDefault: false, criteria: { autoLabel: 'Notification' }, description: 'Automated notifications' }
];

// ---- Snippets ----
const SNIPPETS = [
    {
        id: 'snip_1', name: 'Meeting Follow-up', body: 'Hi {first_name},\n\nThank you for meeting with me today. As discussed, here are the next steps:\n\n1. {action_item_1}\n2. {action_item_2}\n\nPlease let me know if you have any questions.\n\nBest,\nAlex',
        variables: ['first_name', 'action_item_1', 'action_item_2'],
        isShared: true, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-01-15T10:00:00Z',
        metrics: { sends: 47, openRate: 0.89, responseRate: 0.72 }
    },
    {
        id: 'snip_2', name: 'Introduction', body: 'Hi {first_name},\n\nI wanted to introduce you to {contact_name} ({contact_email}). {contact_name} is {contact_role} and I think you two would have a great conversation about {topic}.\n\nI\'ll let you both take it from here!\n\nBest,\nAlex',
        variables: ['first_name', 'contact_name', 'contact_email', 'contact_role', 'topic'],
        isShared: true, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-01-20T14:30:00Z',
        metrics: { sends: 23, openRate: 0.91, responseRate: 0.78 }
    },
    {
        id: 'snip_3', name: 'Scheduling Request', body: 'Hi {first_name},\n\nI\'d love to find some time to connect. Would any of these times work for you?\n\n{available_times}\n\nAlternatively, feel free to book directly: {booking_link}\n\nLooking forward to it!\n\nBest,\nAlex',
        variables: ['first_name', 'available_times', 'booking_link'],
        isShared: false, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-02-01T09:00:00Z',
        metrics: { sends: 65, openRate: 0.85, responseRate: 0.81 }
    },
    {
        id: 'snip_4', name: '[Sales] Product Demo', body: 'Hi {first_name},\n\nThank you for your interest in Acme. I\'d love to schedule a demo to show you how we can help with {use_case}.\n\nThe demo typically takes 30 minutes and covers:\n- Core platform features\n- Integration capabilities\n- Pricing and plans\n\nWould {suggested_time} work for you?\n\nBest,\nAlex',
        variables: ['first_name', 'use_case', 'suggested_time'],
        isShared: true, author: 'Sarah Chen', authorId: 'ct_01',
        createdAt: '2026-02-05T11:00:00Z',
        metrics: { sends: 112, openRate: 0.76, responseRate: 0.45 }
    },
    {
        id: 'snip_5', name: '[Sales] Proposal Follow-up', body: 'Hi {first_name},\n\nI wanted to follow up on the proposal I sent over on {date_sent}. Have you had a chance to review it?\n\nI\'m happy to walk through any questions or adjust the terms. The offer is valid until {expiry_date}.\n\nLooking forward to hearing from you.\n\nBest,\nAlex',
        variables: ['first_name', 'date_sent', 'expiry_date'],
        isShared: true, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-02-10T16:00:00Z',
        metrics: { sends: 34, openRate: 0.82, responseRate: 0.56 }
    },
    {
        id: 'snip_6', name: 'Out of Office', body: 'Hi {first_name},\n\nThank you for your email. I\'m currently out of the office and will return on {return_date}.\n\nFor urgent matters, please reach out to {backup_contact}.\n\nI\'ll get back to you as soon as I can.\n\nBest,\nAlex',
        variables: ['first_name', 'return_date', 'backup_contact'],
        isShared: false, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-02-15T08:00:00Z',
        metrics: { sends: 18, openRate: 0.94, responseRate: 0.11 }
    },
    {
        id: 'snip_7', name: '[HR] Interview Confirmation', body: 'Hi {first_name},\n\nWe\'re excited to confirm your interview for the {position} role at Acme Corp.\n\nDetails:\n- Date: {interview_date}\n- Time: {interview_time}\n- Format: {format}\n- Interviewer(s): {interviewers}\n\nPlease let me know if you need to reschedule.\n\nBest regards,\nAlex Morgan',
        variables: ['first_name', 'position', 'interview_date', 'interview_time', 'format', 'interviewers'],
        isShared: true, author: 'Rachel Foster', authorId: 'ct_13',
        createdAt: '2026-02-18T10:00:00Z',
        metrics: { sends: 28, openRate: 0.96, responseRate: 0.89 }
    },
    {
        id: 'snip_8', name: 'Thank You', body: 'Hi {first_name},\n\nJust wanted to say thank you for {reason}. It really made a difference and I appreciate it.\n\nBest,\nAlex',
        variables: ['first_name', 'reason'],
        isShared: false, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-02-20T13:00:00Z',
        metrics: { sends: 41, openRate: 0.88, responseRate: 0.34 }
    },
    {
        id: 'snip_9', name: '[Engineering] Bug Report Response', body: 'Hi {first_name},\n\nThank you for reporting this issue. We\'ve logged it as {ticket_id} and assigned it to the {team} team.\n\nPriority: {priority}\nExpected resolution: {eta}\n\nWe\'ll keep you updated on progress.\n\nBest,\nAlex',
        variables: ['first_name', 'ticket_id', 'team', 'priority', 'eta'],
        isShared: true, author: 'Nate Patel', authorId: 'ct_16',
        createdAt: '2026-02-22T09:30:00Z',
        metrics: { sends: 56, openRate: 0.71, responseRate: 0.28 }
    },
    {
        id: 'snip_10', name: 'Quick Check-in', body: 'Hi {first_name},\n\nJust checking in on {topic}. Any updates on your end?\n\nLet me know if there\'s anything I can help with.\n\nBest,\nAlex',
        variables: ['first_name', 'topic'],
        isShared: false, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-02-25T15:00:00Z',
        metrics: { sends: 89, openRate: 0.83, responseRate: 0.67 }
    },
    {
        id: 'snip_11', name: '[Marketing] Event Invitation', body: 'Hi {first_name},\n\nYou\'re invited to {event_name}!\n\nDate: {event_date}\nLocation: {location}\nRSVP: {rsvp_link}\n\n{event_description}\n\nHope to see you there!\n\nBest,\nAlex',
        variables: ['first_name', 'event_name', 'event_date', 'location', 'rsvp_link', 'event_description'],
        isShared: true, author: 'Diana Reyes', authorId: 'ct_29',
        createdAt: '2026-02-28T11:00:00Z',
        metrics: { sends: 145, openRate: 0.68, responseRate: 0.42 }
    },
    {
        id: 'snip_12', name: 'Decline Politely', body: 'Hi {first_name},\n\nThank you for thinking of me. Unfortunately, I\'m not able to {request} at this time due to {reason}.\n\nI appreciate your understanding and wish you all the best with it.\n\nBest,\nAlex',
        variables: ['first_name', 'request', 'reason'],
        isShared: false, author: 'Alex Morgan', authorId: 'user_1',
        createdAt: '2026-03-01T14:00:00Z',
        metrics: { sends: 15, openRate: 0.93, responseRate: 0.20 }
    }
];

// ---- Calendar Events ----
const CALENDAR_EVENTS = [
    {
        id: 'evt_1', title: 'Product Roadmap Review', date: '2026-03-07',
        startTime: '09:00', endTime: '10:00', location: 'Zoom',
        description: 'Review Q2 product roadmap with leads',
        attendees: ['sarah.chen@acmecorp.com', 'nate.patel@acmecorp.com', 'maya.patel@acmecorp.com'],
        meetingLink: 'https://zoom.us/j/123456789', isAllDay: false, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#6C4FF7'
    },
    {
        id: 'evt_2', title: 'Weekly Standup', date: '2026-03-07',
        startTime: '10:30', endTime: '11:00', location: 'Google Meet',
        description: 'Team standup - share updates and blockers',
        attendees: ['sarah.chen@acmecorp.com', 'tom.bradley@acmecorp.com', 'rachel.foster@acmecorp.com', 'nate.patel@acmecorp.com'],
        meetingLink: 'https://meet.google.com/abc-defg-hij', isAllDay: false, calendarId: 'work',
        organizer: 'tom.bradley@acmecorp.com', status: 'confirmed', color: '#34A853'
    },
    {
        id: 'evt_3', title: 'Lunch with Marcus', date: '2026-03-07',
        startTime: '12:00', endTime: '13:00', location: 'Blue Bottle Coffee, 450 Hayes St',
        description: 'Catch up on DesignHub partnership',
        attendees: ['marcus.w@designhub.io'],
        meetingLink: null, isAllDay: false, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#FF9800'
    },
    {
        id: 'evt_4', title: 'Board Meeting Prep', date: '2026-03-07',
        startTime: '14:00', endTime: '15:30', location: 'Conference Room A',
        description: 'Prepare materials for Q1 board meeting',
        attendees: ['priya.sharma@acmecorp.com', 'ben.carter@acmecorp.com'],
        meetingLink: null, isAllDay: false, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#E54D89'
    },
    {
        id: 'evt_5', title: '1:1 with Sarah', date: '2026-03-07',
        startTime: '16:00', endTime: '16:30', location: 'Zoom',
        description: 'Weekly 1:1 check-in',
        attendees: ['sarah.chen@acmecorp.com'],
        meetingLink: 'https://zoom.us/j/987654321', isAllDay: false, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#6C4FF7'
    },
    {
        id: 'evt_6', title: 'Yoga Class', date: '2026-03-07',
        startTime: '18:00', endTime: '19:00', location: 'FitnessFirst Downtown',
        description: 'Evening yoga',
        attendees: [],
        meetingLink: null, isAllDay: false, calendarId: 'personal',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#009688'
    },
    {
        id: 'evt_7', title: 'Sprint Planning', date: '2026-03-08',
        startTime: '09:00', endTime: '10:30', location: 'Google Meet',
        description: 'Plan Sprint 24 priorities and assignments',
        attendees: ['nate.patel@acmecorp.com', 'maya.patel@acmecorp.com', 'tom.bradley@acmecorp.com', 'ben.carter@acmecorp.com'],
        meetingLink: 'https://meet.google.com/xyz-uvwx-yz', isAllDay: false, calendarId: 'work',
        organizer: 'nate.patel@acmecorp.com', status: 'confirmed', color: '#2196F3'
    },
    {
        id: 'evt_8', title: 'Client Demo - FinancePlus', date: '2026-03-08',
        startTime: '11:00', endTime: '12:00', location: 'Zoom',
        description: 'Product demo for FinancePlus team',
        attendees: ['david.kim@financeplus.com', 'sarah.chen@acmecorp.com'],
        meetingLink: 'https://zoom.us/j/111222333', isAllDay: false, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#FF5722'
    },
    {
        id: 'evt_9', title: 'Design Review', date: '2026-03-08',
        startTime: '14:00', endTime: '15:00', location: 'Figma / Zoom',
        description: 'Review new dashboard designs with Marcus',
        attendees: ['marcus.w@designhub.io', 'maya.patel@acmecorp.com'],
        meetingLink: 'https://zoom.us/j/444555666', isAllDay: false, calendarId: 'work',
        organizer: 'marcus.w@designhub.io', status: 'confirmed', color: '#34A853'
    },
    {
        id: 'evt_10', title: 'Dentist Appointment', date: '2026-03-09',
        startTime: '09:00', endTime: '10:00', location: 'Dr. Smith, 123 Main St',
        description: 'Regular checkup',
        attendees: [],
        meetingLink: null, isAllDay: false, calendarId: 'personal',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#F44336'
    },
    {
        id: 'evt_11', title: 'All-Hands Meeting', date: '2026-03-09',
        startTime: '15:00', endTime: '16:00', location: 'Zoom',
        description: 'Monthly all-hands company meeting',
        attendees: ['sarah.chen@acmecorp.com', 'priya.sharma@acmecorp.com', 'tom.bradley@acmecorp.com', 'rachel.foster@acmecorp.com', 'nate.patel@acmecorp.com', 'maya.patel@acmecorp.com', 'ben.carter@acmecorp.com', 'patrick.oneil@acmecorp.com'],
        meetingLink: 'https://zoom.us/j/777888999', isAllDay: false, calendarId: 'work',
        organizer: 'patrick.oneil@acmecorp.com', status: 'confirmed', color: '#6C4FF7'
    },
    {
        id: 'evt_12', title: 'Q1 Board Meeting', date: '2026-03-10',
        startTime: '10:00', endTime: '12:00', location: 'Acme HQ - Board Room',
        description: 'Quarterly board review and strategy session',
        attendees: ['emily.r@venturelabs.co', 'lena.j@nordicventures.se', 'priya.sharma@acmecorp.com', 'patrick.oneil@acmecorp.com'],
        meetingLink: null, isAllDay: false, calendarId: 'work',
        organizer: 'patrick.oneil@acmecorp.com', status: 'confirmed', color: '#E54D89'
    },
    {
        id: 'evt_13', title: 'Investor Lunch', date: '2026-03-10',
        startTime: '12:30', endTime: '14:00', location: 'The Capital Grille',
        description: 'Lunch with Emily from Venture Labs',
        attendees: ['emily.r@venturelabs.co'],
        meetingLink: null, isAllDay: false, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#FBBC04'
    },
    {
        id: 'evt_14', title: 'Team Offsite', date: '2026-03-12',
        startTime: '09:00', endTime: '17:00', location: 'Cavallo Point, Sausalito',
        description: 'Annual product team offsite - strategy and team building',
        attendees: ['sarah.chen@acmecorp.com', 'nate.patel@acmecorp.com', 'maya.patel@acmecorp.com', 'tom.bradley@acmecorp.com', 'ben.carter@acmecorp.com', 'rachel.foster@acmecorp.com'],
        meetingLink: null, isAllDay: true, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#009688'
    },
    {
        id: 'evt_15', title: 'Flight to NYC', date: '2026-03-15',
        startTime: '07:00', endTime: '15:30', location: 'SFO → JFK (UA 234)',
        description: 'United Airlines Flight 234',
        attendees: [],
        meetingLink: null, isAllDay: false, calendarId: 'personal',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#607D8B'
    },
    {
        id: 'evt_16', title: 'NYC Partner Meeting', date: '2026-03-16',
        startTime: '10:00', endTime: '11:30', location: 'WeWork, 115 Broadway',
        description: 'Partnership discussion with MediaCo',
        attendees: ['michelle.park@mediaco.tv'],
        meetingLink: null, isAllDay: false, calendarId: 'work',
        organizer: 'alex.morgan@acmecorp.com', status: 'tentative', color: '#FF9800'
    },
    {
        id: 'evt_17', title: 'Birthday Dinner - Mom', date: '2026-03-18',
        startTime: '19:00', endTime: '21:00', location: 'Chez Panisse',
        description: 'Mom\'s birthday dinner',
        attendees: [],
        meetingLink: null, isAllDay: false, calendarId: 'personal',
        organizer: 'alex.morgan@acmecorp.com', status: 'confirmed', color: '#E91E63'
    },
    {
        id: 'evt_18', title: 'Quarterly OKR Review', date: '2026-03-11',
        startTime: '13:00', endTime: '14:30', location: 'Zoom',
        description: 'Review Q1 OKR progress and set Q2 objectives',
        attendees: ['sarah.chen@acmecorp.com', 'priya.sharma@acmecorp.com', 'patrick.oneil@acmecorp.com'],
        meetingLink: 'https://zoom.us/j/321654987', isAllDay: false, calendarId: 'work',
        organizer: 'priya.sharma@acmecorp.com', status: 'confirmed', color: '#6C4FF7'
    }
];

// ---- Settings ----
const SETTINGS = {
    readReceipts: { enabled: true, teamSharing: true },
    autoReminders: { mode: 'ai', defaultTime: '09:00', enabled: true },
    autoDrafts: { enabled: true, type: 'follow-up', ccTeammate: false, ccEmail: '' },
    smartSend: { enabled: true },
    theme: 'light',
    notifications: { desktop: true, sound: true, calendarAlerts: true, alertMinutes: 10 },
    meetingLink: { provider: 'zoom', autoAdd: true },
    keyboard: { shortcuts: true },
    signature: CURRENT_USER.signature,
    timezone: 'America/New_York',
    secondaryTimezone: 'Europe/London',
    swipeLeft: 'done',
    swipeRight: 'remind',
    autoArchive: { enabled: true, labels: ['al_3'] },
    instantReply: { enabled: true },
    askAi: { enabled: true, searchYears: 5 }
};

// ---- Helper: create email ----
const _u = CURRENT_USER;
const _to = [{ name: _u.name, email: _u.email }];

function _e(id, threadId, from, subject, snippet, date, opts = {}) {
    return {
        id, threadId: 'thread_' + threadId,
        from, to: opts.to || _to, cc: opts.cc || [], bcc: [],
        subject, snippet, body: opts.body || snippet,
        date,
        isRead: opts.isRead !== undefined ? opts.isRead : true,
        isStarred: opts.isStarred || false,
        isDone: opts.isDone || false,
        isTrashed: opts.isTrashed || false,
        isSpam: opts.isSpam || false,
        isDraft: opts.isDraft || false,
        labels: opts.labels || [],
        hasAttachments: opts.hasAttachments || false,
        attachments: opts.attachments || [],
        splitCategory: opts.splitCategory || 'important',
        remindAt: opts.remindAt || null,
        readReceipt: opts.readReceipt || null,
        autoLabel: opts.autoLabel || null,
        replyDraftingTeammate: opts.replyDraftingTeammate || null,
        threadMessages: opts.threadMessages || null
    };
}

function _from(contactId) {
    const c = CONTACTS.find(c => c.id === contactId);
    return { name: c.name, email: c.email };
}

function _sentTo(emails) {
    return emails.map(e => {
        const c = CONTACTS.find(c => c.email === e);
        return c ? { name: c.name, email: c.email } : { name: e.split('@')[0], email: e };
    });
}

// ---- Emails ----
const EMAILS = [
    // === INBOX - Important split (person-to-person) ===
    _e(1, 1, _from('ct_01'), 'Q2 Product Roadmap - Final Review', 'Hey Alex, I\'ve compiled the final draft of our Q2 roadmap. Can you take a look before the board meeting?', '2026-03-07T08:12:00Z', {
        isRead: false, labels: ['label_1', 'label_10'], splitCategory: 'important',
        body: 'Hey Alex,\n\nI\'ve compiled the final draft of our Q2 roadmap based on yesterday\'s discussion. Key changes:\n\n1. Moved the AI search feature to P0 (from P1)\n2. Pushed the mobile redesign to Q3\n3. Added the enterprise SSO integration per client requests\n\nCan you review before the board meeting on Tuesday? The deck is attached.\n\nAlso, Kevin from QuantumLab reached out about a potential integration. Should I set up a call?\n\nThanks,\nSarah',
        hasAttachments: true, attachments: [{ name: 'Q2_Roadmap_v3.pdf', size: '2.4 MB' }],
        readReceipt: null
    }),

    _e(2, 2, _from('ct_03'), 'Re: Series B Term Sheet Discussion', 'Alex, the term sheet looks good overall. A few comments on the liquidation preference...', '2026-03-07T07:45:00Z', {
        isRead: false, labels: ['label_5'], splitCategory: 'important',
        body: 'Alex,\n\nThe term sheet looks good overall. A few comments:\n\n1. Liquidation preference: We\'d prefer 1x non-participating vs the 1.5x proposed\n2. Board seat: We\'re fine with one board seat for Venture Labs\n3. Pro-rata rights: Standard is fine\n4. Anti-dilution: Broad-based weighted average works\n\nCan we schedule a call this week to discuss? I have some availability Thursday afternoon.\n\nBest,\nEmily',
        threadMessages: [
            { id: 't2_1', from: { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, date: '2026-03-05T16:00:00Z', body: 'Emily,\n\nPlease find attached the draft term sheet for the Series B round. Let me know your thoughts.\n\nBest,\nAlex' },
            { id: 't2_2', from: _from('ct_03'), date: '2026-03-06T10:30:00Z', body: 'Thanks Alex, reviewing now. Will get back to you tomorrow.' }
        ]
    }),

    _e(3, 3, _from('ct_06'), 'Partnership Opportunity - FinancePlus x Acme', 'Hi Alex, following up on our conversation at the conference. We\'d love to explore integrating...', '2026-03-07T06:30:00Z', {
        isRead: false, labels: ['label_4'], splitCategory: 'important',
        body: 'Hi Alex,\n\nFollowing up on our conversation at the SaaS Connect conference last week. We\'d love to explore integrating FinancePlus\'s payment processing with the Acme platform.\n\nOur enterprise clients have been asking for a unified workflow, and I think there\'s a strong synergy here.\n\nWould you be open to a 30-minute call this week? I can bring our Head of Partnerships.\n\nBest regards,\nDavid Kim\nVP Business Development, FinancePlus',
        readReceipt: { opened: true, openedAt: '2026-03-07T07:15:00Z', device: 'iPhone', openCount: 2 }
    }),

    _e(4, 4, _from('ct_08'), 'Re: Infrastructure Migration Plan', 'Alex, the migration to the new k8s cluster is on track. We\'ll start Phase 2 next Monday.', '2026-03-07T05:20:00Z', {
        isRead: true, labels: ['label_1', 'label_11'], splitCategory: 'important',
        body: 'Alex,\n\nThe migration to the new k8s cluster is on track. Quick update:\n\n- Phase 1 (staging): Completed yesterday, all tests passing\n- Phase 2 (production - non-critical): Starting Monday March 10\n- Phase 3 (production - critical): March 17, pending your sign-off\n\nDowntime estimate: 15 minutes per service, rolling deployment.\n\nI\'ll send the detailed runbook by EOD Friday.\n\nTom',
        threadMessages: [
            { id: 't4_1', from: { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, date: '2026-03-04T14:00:00Z', body: 'Tom, what\'s the status on the k8s migration? Board wants an update.' },
            { id: 't4_2', from: _from('ct_08'), date: '2026-03-05T09:00:00Z', body: 'Working on the staging environment now. Should have Phase 1 done by Wednesday.' }
        ]
    }),

    _e(5, 5, _from('ct_05'), 'Budget Approval Needed - Marketing Campaign', 'Hi Alex, need your sign-off on the Q2 marketing budget. Total ask is $450K across digital...', '2026-03-06T22:15:00Z', {
        isRead: false, labels: ['label_1', 'label_3'], splitCategory: 'important',
        body: 'Hi Alex,\n\nNeed your sign-off on the Q2 marketing budget. Here\'s the breakdown:\n\n- Digital advertising: $180K\n- Content marketing: $95K\n- Events & conferences: $120K\n- PR & communications: $55K\n\nTotal: $450K (15% increase from Q1)\n\nROI projection is attached. The events budget is higher due to our sponsorship of SaaStr Annual.\n\nCan you approve by Friday so we can lock in early-bird rates?\n\nThanks,\nPriya',
        hasAttachments: true, attachments: [{ name: 'Q2_Marketing_Budget_ROI.xlsx', size: '1.1 MB' }]
    }),

    _e(6, 6, _from('ct_14'), 'Quantum Computing Integration Prototype', 'Alex, the prototype is ready for review. We\'ve achieved 3x performance improvement on the...', '2026-03-06T20:00:00Z', {
        isRead: true, labels: ['label_11'], splitCategory: 'important',
        body: 'Alex,\n\nThe prototype is ready for review. Key results:\n\n- 3x performance improvement on large dataset queries\n- 99.97% accuracy maintained\n- API latency reduced from 450ms to 120ms\n- Compatible with existing client SDKs\n\nDemo environment: https://staging.quantumlab.tech/acme-poc\nCredentials in the secure doc I shared with Nate.\n\nWould love to present this at the next engineering all-hands.\n\nBest,\nKevin',
        readReceipt: { opened: true, openedAt: '2026-03-06T20:45:00Z', device: 'MacBook Pro', openCount: 3 }
    }),

    _e(7, 7, _from('ct_16'), 'Re: Sprint 23 Retrospective Notes', 'Summarized the retro notes. Main themes: deployment pipeline needs work, on-call rotations...', '2026-03-06T18:30:00Z', {
        isRead: true, labels: ['label_11'], splitCategory: 'important',
        body: 'Summarized the retro notes. Main themes:\n\n**What went well:**\n- Shipped the notification system ahead of schedule\n- Zero P0 incidents this sprint\n- New CI pipeline reduced build times by 40%\n\n**What needs improvement:**\n- Deployment pipeline still flaky for microservices\n- On-call rotations need rebalancing (3 people handling 80% of alerts)\n- Better test coverage for the billing module\n\n**Action items:**\n1. Nate to fix deployment pipeline by Sprint 24\n2. Tom to redistribute on-call schedule\n3. Maya to add billing module tests\n\nFull doc: https://docs.acmecorp.com/retro-s23\n\n- Nate'
    }),

    _e(8, 8, _from('ct_21'), 'Design System Update - New Components Ready', 'Hi Alex, the new design system components are ready for review. Added: data tables, charts...', '2026-03-06T17:00:00Z', {
        isRead: true, labels: ['label_10'], splitCategory: 'important',
        body: 'Hi Alex,\n\nThe new design system components are ready for review:\n\n**New components:**\n- Data tables with sorting, filtering, pagination\n- Chart components (line, bar, pie, area)\n- Kanban board\n- Timeline view\n- Advanced search with filters\n\n**Updated:**\n- Button variants (added outline, ghost)\n- Form inputs (new validation states)\n- Modal sizes (added xl, full-screen)\n\nStorybook: https://design.acmecorp.com/storybook\nFigma: https://figma.com/file/acme-ds-v2\n\nLet me know if you want to walk through any of these.\n\nMaya'
    }),

    _e(9, 9, _from('ct_13'), 'Re: Engineering Manager Candidates', 'Alex, we have 3 strong candidates for the EM role. Top pick is Jordan Lee from Stripe...', '2026-03-06T15:45:00Z', {
        isRead: true, labels: ['label_8'], splitCategory: 'important',
        body: 'Alex,\n\nWe have 3 strong candidates for the Engineering Manager role:\n\n1. **Jordan Lee** (Stripe) - 8 years, managed teams of 15+, strong on infrastructure\n2. **Sam Rivera** (Netflix) - 6 years, full-stack background, great culture fit\n3. **Pat Chen** (Google) - 10 years, deep ML expertise, overqualified?\n\nI\'d recommend moving Jordan to final round. They impressed everyone in the technical panel.\n\nInterview feedback docs attached. Can you review by Monday?\n\nRachel',
        hasAttachments: true, attachments: [{ name: 'EM_Candidate_Feedback.pdf', size: '890 KB' }]
    }),

    _e(10, 10, _from('ct_02'), 'New Brand Assets - Review Needed', 'Hey Alex, the updated brand assets are ready. New logo variants, color palette, and typography...', '2026-03-06T14:30:00Z', {
        isRead: true, labels: ['label_12'], splitCategory: 'important',
        body: 'Hey Alex,\n\nThe updated brand assets are ready for your review:\n\n- Logo: 4 variants (full, icon, horizontal, vertical)\n- Color palette: Extended with 3 new accent colors\n- Typography: Switching from Inter to Plus Jakarta Sans\n- Iconography: New custom icon set (200+ icons)\n- Illustration style: Updated to be more inclusive\n\nBrand guide PDF attached. Figma library will be updated once approved.\n\nTimeline: Need approval by March 14 to hit the website relaunch date.\n\nMarcus',
        hasAttachments: true, attachments: [
            { name: 'Acme_Brand_Guide_v2.pdf', size: '15.8 MB' },
            { name: 'Logo_Assets.zip', size: '4.2 MB' }
        ]
    }),

    _e(11, 11, _from('ct_09'), 'Global Health Initiative - Sponsorship Request', 'Hi Alex, reaching out about our annual Global Health Summit (April 15-17). Would Acme be...', '2026-03-06T12:00:00Z', {
        isRead: true, labels: ['label_14'], splitCategory: 'important',
        body: 'Hi Alex,\n\nReaching out about our annual Global Health Summit (April 15-17 in San Francisco).\n\nWould Acme be interested in sponsoring? Tiers:\n\n- Platinum ($25K): Keynote slot, booth, logo on all materials\n- Gold ($15K): Workshop slot, booth\n- Silver ($5K): Logo on website and program\n\nLast year we had 2,000+ attendees from 40 countries. Great visibility for Acme\'s health-tech integrations.\n\nLet me know if you\'d like more details.\n\nBest,\nAna'
    }),

    _e(12, 12, _from('ct_30'), 'Executive Team Dinner - March 14', 'Alex, confirming dinner at Benu on March 14 at 7pm. Private room booked for 8.', '2026-03-06T11:00:00Z', {
        isRead: true, labels: ['label_1'], splitCategory: 'important',
        body: 'Alex,\n\nConfirming dinner at Benu on March 14 at 7pm. Private room booked for 8.\n\nAttending:\n- Patrick (CEO)\n- Alex (VP Product)\n- Priya (CFO)\n- Sarah (VP Sales)\n- Tom (VP Engineering)\n- Rachel (VP People)\n- Ben (VP Operations)\n- Nate (CTO)\n\nDress code: Business casual. I\'ll send the Uber codes day-of.\n\nPatrick'
    }),

    _e(13, 13, _from('ct_04'), 'Re: Vendor Agreement - CloudScale', 'Alex, I\'ve reviewed the CloudScale agreement. A few items that need attention before signing...', '2026-03-06T09:30:00Z', {
        isRead: true, labels: ['label_9'], splitCategory: 'important',
        body: 'Alex,\n\nI\'ve reviewed the CloudScale agreement. Items needing attention:\n\n1. **Section 4.2 (Data Processing)**: Needs a DPA addendum for GDPR compliance\n2. **Section 7.1 (Liability Cap)**: Currently uncapped - we need to negotiate a 12-month cap\n3. **Section 9 (Termination)**: 90-day notice is standard, but no cure period - recommend adding 30-day cure\n4. **Section 12 (IP)**: Ownership clause is ambiguous for custom integrations\n\nI can draft redlines by Wednesday. Should I loop in Michael from CloudScale directly?\n\nJames O\'Brien\nPartner, LegalWise LLP'
    }),

    _e(14, 14, _from('ct_11'), 'Exclusive: Acme Feature in TechTrends Weekly', 'Hi Alex, we\'d love to feature Acme in our upcoming issue of TechTrends Weekly. The story...', '2026-03-06T08:00:00Z', {
        isRead: true, labels: ['label_12'], splitCategory: 'important',
        body: 'Hi Alex,\n\nWe\'d love to feature Acme in our upcoming issue of TechTrends Weekly (circulation: 500K+).\n\nThe story angle: "How Acme is disrupting enterprise workflows with AI"\n\nWhat we\'d need:\n- 30-minute interview with you or your CTO\n- Product screenshots/video\n- Key metrics (ARR growth, user count, etc.)\n\nPublish date: March 20\nDeadline for content: March 12\n\nInterested?\n\nMichelle Park\nSenior Editor, MediaCo'
    }),

    _e(15, 15, _from('ct_26'), 'Office Lease Renewal - Decision Needed', 'Alex, the office lease expires April 30. The landlord is offering 3 options...', '2026-03-05T16:00:00Z', {
        isRead: true, labels: ['label_3'], splitCategory: 'important',
        body: 'Alex,\n\nThe office lease at 100 Market St expires April 30. Landlord options:\n\n1. **3-year renewal**: $45/sqft (current rate) - 5% increase each year\n2. **5-year renewal**: $42/sqft - locked rate for term\n3. **Month-to-month**: $52/sqft - flexible but expensive\n\nGiven our growth plans, I\'d recommend Option 2 with a sublease clause.\n\nNeed a decision by March 15 to avoid month-to-month auto-renewal.\n\nBen'
    }),

    _e(16, 16, _from('ct_19'), 'Research Collaboration Proposal', 'Dear Alex, writing from BioMed Research to propose a joint study on AI-driven diagnostics...', '2026-03-05T14:00:00Z', {
        isRead: true, labels: ['label_4'], splitCategory: 'important',
        body: 'Dear Alex,\n\nWriting from BioMed Research to propose a joint study on AI-driven diagnostics workflow optimization.\n\nProposal highlights:\n- 6-month study period\n- Access to our dataset of 2M+ anonymized records\n- Co-authorship on resulting publications\n- Potential NIH grant funding ($500K)\n\nWe believe Acme\'s platform could significantly improve diagnostic turnaround times.\n\nWould you be open to an exploratory call?\n\nBest regards,\nDr. Jennifer Wu\nResearch Director, BioMed Research'
    }),

    _e(17, 17, _from('ct_24'), 'SaaS Platform Integration - API Access', 'Hey Alex, we\'ve set up your sandbox API access. Here are the details...', '2026-03-05T11:30:00Z', {
        isRead: true, labels: ['label_11'], splitCategory: 'important',
        body: 'Hey Alex,\n\nSandbox API access is ready:\n\n- Base URL: https://api.saasplatform.io/v2/sandbox\n- API Key: sk_sandbox_acme_****\n- Rate limit: 1000 req/min\n- Docs: https://docs.saasplatform.io/integrations\n\nI\'ve also set up a webhook endpoint for real-time events. Your team can start testing the OAuth flow.\n\nLet me know if Nate needs any help with the integration.\n\nRyan'
    }),

    // More inbox important emails
    _e(18, 18, _from('ct_29'), 'Q1 Marketing Report - Outstanding Results', 'Alex, Q1 marketing numbers are in and they\'re great. Pipeline grew 42% QoQ...', '2026-03-05T09:00:00Z', {
        isRead: true, labels: ['label_12'], splitCategory: 'important',
        body: 'Alex,\n\nQ1 marketing numbers are in:\n\n- Pipeline: $4.2M (42% QoQ growth)\n- MQLs: 1,847 (28% increase)\n- Website traffic: 890K visits (35% increase)\n- Content downloads: 12,400\n- Event leads: 340 from SaaS Connect\n\nTop performing channels:\n1. Organic search (38% of pipeline)\n2. LinkedIn ads (24%)\n3. Content marketing (18%)\n4. Events (12%)\n5. Referrals (8%)\n\nFull report attached.\n\nDiana',
        hasAttachments: true, attachments: [{ name: 'Q1_Marketing_Report.pdf', size: '3.7 MB' }]
    }),

    _e(19, 19, _from('ct_15'), 'EuroDesign Conference - Speaker Invitation', 'Dear Alex, I\'d like to invite you to speak at EuroDesign Summit 2026 in Paris...', '2026-03-05T07:00:00Z', {
        isRead: true, labels: ['label_14', 'label_6'], splitCategory: 'important',
        body: 'Dear Alex,\n\nI\'d like to invite you to speak at EuroDesign Summit 2026 in Paris (May 22-24).\n\nProposed topic: "Building Products That Scale: Lessons from Acme"\n- 45-minute keynote on Day 2\n- 1,500+ attendees from 30 countries\n- Travel and accommodation covered\n- Speaker dinner on May 21\n\nPast speakers include leaders from Figma, Notion, and Linear.\n\nWould you be interested? We\'d need confirmation by April 1.\n\nBest regards,\nSophie Laurent\nConference Director, EuroDesign'
    }),

    _e(20, 20, _from('ct_10'), 'Guest Lecture Request - Stanford CS Department', 'Professor Morgan, I\'m reaching out from the CS department at Stanford...', '2026-03-04T19:00:00Z', {
        isRead: true, labels: ['label_14'], splitCategory: 'important',
        body: 'Dear Alex,\n\nI\'m reaching out from the CS department at Stanford University. We\'d love to have you give a guest lecture in our CS 247: Human-Computer Interaction course.\n\nTopic: "Designing AI-First Enterprise Applications"\nDate: April 8 (flexible)\nFormat: 50-minute lecture + 10-minute Q&A\nAudience: ~120 graduate students\n\nWe can offer an honorarium of $1,500.\n\nBest regards,\nProf. Robert Singh\nDepartment of Computer Science, Stanford University'
    }),

    // Important but older / read
    _e(21, 21, _from('ct_28'), 'CloudScale Contract - Ready to Sign', 'Alex, the contract is finalized per James\'s redlines. DocuSign link inside.', '2026-03-04T15:30:00Z', {
        isRead: true, labels: ['label_9', 'label_11'], splitCategory: 'important',
        body: 'Alex,\n\nThe contract is finalized per James\'s redlines. All four items addressed:\n\n- DPA addendum included\n- Liability capped at 12 months fees\n- 30-day cure period added\n- IP ownership clause clarified\n\nDocuSign link: https://docusign.com/doc/acme-cloudscale-msa\n\nOnce signed, we can begin migration within 48 hours.\n\nMichael Foster\nCEO, CloudScale'
    }),

    _e(22, 22, _from('ct_07'), 'Creative Brief - Website Redesign', 'Hi Alex, attached is the creative brief for the website redesign project...', '2026-03-04T13:00:00Z', {
        isRead: true, labels: ['label_12'], splitCategory: 'important',
        body: 'Hi Alex,\n\nAttached is the creative brief for the website redesign project.\n\nKey elements:\n- New visual direction aligned with updated brand\n- Improved conversion funnel (targeting 3% → 5%)\n- Interactive product demos\n- Customer story carousel\n- AI chatbot integration\n\nTimeline: Design phase March 15 - April 15\nDevelopment: April 15 - May 15\nLaunch: May 20\n\nPlease review and share feedback by end of week.\n\nLisa Nakamura\nCreative Director, Creative Agency',
        hasAttachments: true, attachments: [{ name: 'Acme_Web_Redesign_Brief.pdf', size: '5.3 MB' }]
    }),

    _e(23, 23, _from('ct_25'), 'Nordic Ventures - Follow-up from Board Introduction', 'Hi Alex, lovely meeting you at the Venture Labs mixer. Lena here from Nordic Ventures...', '2026-03-04T10:00:00Z', {
        isRead: true, labels: [], splitCategory: 'important',
        body: 'Hi Alex,\n\nLovely meeting you at the Venture Labs mixer. As I mentioned, Nordic Ventures is actively investing in B2B SaaS companies in the $10-50M ARR range.\n\nI\'d love to learn more about Acme\'s trajectory. Some initial questions:\n\n1. Current ARR and growth rate?\n2. Net revenue retention?\n3. Path to profitability timeline?\n\nWould a 30-minute call work sometime next week?\n\nBest,\nLena Johansson\nPartner, Nordic Ventures'
    }),

    _e(24, 24, _from('ct_12'), 'Logistics Update - Office Equipment Delivery', 'Alex, the new standing desks and monitors will arrive March 12. We need someone to...', '2026-03-04T08:00:00Z', {
        isRead: true, labels: ['label_1'], splitCategory: 'important',
        body: 'Alex,\n\nThe new standing desks and monitors will arrive March 12.\n\nDelivery details:\n- 25 standing desks (Uplift V2)\n- 30 monitors (Dell U2723QE)\n- 10 ergonomic chairs (Herman Miller Aeron)\n\nTotal: $47,800 (within approved budget)\n\nNeed someone from your team to be on-site 9am-12pm for delivery and setup.\n\nCarlos Mendez\nLogistics Manager, LogisticsPro'
    }),

    // === INBOX - Other split (automated, newsletters) ===
    _e(25, 25, { name: 'GitHub', email: 'notifications@github.com' }, '[acme/platform] PR #1842 merged: Add real-time collaboration', 'Pull request merged by nate.patel - Add real-time collaboration engine with conflict resolution', '2026-03-07T07:00:00Z', {
        isRead: false, splitCategory: 'other', autoLabel: 'Notification',
        body: 'Pull request #1842 merged into main by nate.patel\n\nAdd real-time collaboration engine with conflict resolution\n\n+2,847 -412 across 34 files\n\nReviewers: tom.bradley (approved), maya.patel (approved)\nCI: All checks passed'
    }),

    _e(26, 26, { name: 'GitHub', email: 'notifications@github.com' }, '[acme/platform] Issue #923: Memory leak in WebSocket handler', 'New issue opened by ben.carter - Memory usage grows unbounded after 1000+ concurrent connections', '2026-03-07T06:45:00Z', {
        isRead: false, splitCategory: 'other', autoLabel: 'Notification',
        body: 'New issue #923 opened by ben.carter\n\nMemory leak in WebSocket handler\n\nMemory usage grows unbounded after 1000+ concurrent WebSocket connections. Profiling shows the connection pool isn\'t properly cleaning up disconnected clients.\n\nEnvironment: Production (us-east-1)\nSeverity: P1\nAssigned: nate.patel'
    }),

    _e(27, 27, { name: 'Slack', email: 'notifications@slack.com' }, 'New messages in #product-launches', 'Sarah Chen: The beta launch metrics are looking really promising...', '2026-03-07T06:30:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(28, 28, { name: 'Linear', email: 'notifications@linear.app' }, '[ACM-4521] Bug: Dashboard charts not loading on Firefox', 'Issue ACM-4521 assigned to you by Maya Patel. Priority: High', '2026-03-07T05:15:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(29, 29, { name: 'The Information', email: 'newsletter@theinformation.com' }, 'Today\'s Briefing: AI Startup Funding Hits Record $12B in Q1', 'AI startup funding reached $12 billion in Q1 2026, led by enterprise AI companies...', '2026-03-07T05:00:00Z', {
        isRead: false, splitCategory: 'other', autoLabel: 'Newsletter',
        body: 'TODAY\'S BRIEFING\n\nAI Startup Funding Hits Record $12B in Q1\n\nAI startup funding reached $12 billion in Q1 2026, led by enterprise AI companies. Key rounds:\n- Anthropic raised $2B at $60B valuation\n- Scale AI raised $1.5B\n- Cohere raised $800M\n\nEnterprise AI adoption is accelerating, with 73% of Fortune 500 companies now using AI in production workflows.\n\nRead more: https://theinformation.com/ai-funding-q1-2026'
    }),

    _e(30, 30, { name: 'Figma', email: 'notifications@figma.com' }, 'Marcus Williams commented on "Dashboard Redesign v2"', 'Marcus Williams left a comment: "Love the new data viz approach. Can we explore..."', '2026-03-06T23:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(31, 31, { name: 'Stripe', email: 'notifications@stripe.com' }, 'Your March payout has been initiated', 'A payout of $127,450.00 has been initiated to your bank account ending in 4821.', '2026-03-06T21:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_3']
    }),

    _e(32, 32, { name: 'TechCrunch Daily', email: 'newsletter@techcrunch.com' }, 'TC Daily: The AI agent wars heat up', 'Plus: Enterprise SaaS valuations rebound, new cybersecurity threats emerge...', '2026-03-06T14:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Newsletter'
    }),

    _e(33, 33, { name: 'AWS', email: 'no-reply@aws.amazon.com' }, 'AWS Cost Alert: Acme Corp - February 2026', 'Your AWS costs for February 2026 were $23,847.12, a 12% increase from January.', '2026-03-06T12:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_3']
    }),

    _e(34, 34, { name: 'Datadog', email: 'alerts@datadog.com' }, '[RESOLVED] High API Latency - api.acmecorp.com', 'Alert resolved: API p99 latency returned to normal (< 200ms) at 2026-03-06 10:45 UTC', '2026-03-06T10:45:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_11']
    }),

    _e(35, 35, { name: 'Product Hunt', email: 'hello@producthunt.com' }, 'Product Hunt Daily Digest - March 6', 'Top products today: AIFlow, DesignOps Pro, MetricsDash...', '2026-03-06T10:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Newsletter'
    }),

    _e(36, 36, { name: 'HubSpot', email: 'notifications@hubspot.com' }, 'Weekly CRM Report - Acme Corp', '47 new leads this week, 12 deals in pipeline, 3 deals closed ($89K total)', '2026-03-06T09:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_4']
    }),

    _e(37, 37, { name: 'Sentry', email: 'alerts@sentry.io' }, '[acme-platform] New issue: TypeError in payment module', 'TypeError: Cannot read properties of undefined (reading \'amount\') in PaymentProcessor.js:247', '2026-03-06T03:20:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_11']
    }),

    _e(38, 38, { name: 'Morning Brew', email: 'crew@morningbrew.com' }, 'Morning Brew - Markets surge on Fed pivot signals', 'Markets rallied 2.3% as the Fed signaled potential rate cuts in Q3...', '2026-03-06T06:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Newsletter'
    }),

    _e(39, 39, { name: 'Google Workspace', email: 'no-reply@google.com' }, 'Storage alert: Acme Corp workspace at 85% capacity', 'Your Google Workspace storage is at 85% of your plan limit (8.5 TB of 10 TB used).', '2026-03-05T18:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(40, 40, { name: 'LinkedIn', email: 'notifications@linkedin.com' }, 'Your post about AI agents received 5,200+ views', 'Your post "The Future of AI Agents in Enterprise" is trending. 5,247 views, 312 reactions, 47 comments.', '2026-03-05T15:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(41, 41, { name: 'Notion', email: 'notifications@makenotion.com' }, 'Sarah Chen updated "Q2 Planning" in Product workspace', 'Sarah Chen edited the Q2 Planning document. Changes: Added timeline for mobile app launch...', '2026-03-05T14:30:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(42, 42, { name: 'Hacker News Digest', email: 'digest@hackernewsletter.com' }, 'HN Weekly: Show HN projects, top stories, and jobs', 'This week\'s highlights: A new approach to database indexing, Why SQLite is eating the world...', '2026-03-05T12:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Newsletter'
    }),

    _e(43, 43, { name: 'DocuSign', email: 'dse@docusign.net' }, 'Action Required: CloudScale MSA - Signature Needed', 'Michael Foster sent you a document to sign: CloudScale Master Service Agreement', '2026-03-05T10:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_9']
    }),

    // === INBOX - Calendar split ===
    _e(44, 44, { name: 'Google Calendar', email: 'calendar-notification@google.com' }, 'Reminder: Product Roadmap Review tomorrow at 9:00 AM', 'Product Roadmap Review - March 7 at 9:00 AM ET. Location: Zoom', '2026-03-06T21:00:00Z', {
        isRead: true, splitCategory: 'calendar', autoLabel: 'Calendar Invite'
    }),

    _e(45, 45, _from('ct_05'), 'Calendar: Budget Review Meeting - March 12', 'Priya Sharma has invited you to Budget Review Meeting on March 12 at 2:00 PM', '2026-03-06T16:00:00Z', {
        isRead: true, splitCategory: 'calendar', autoLabel: 'Calendar Invite',
        body: 'Priya Sharma has invited you to:\n\nBudget Review Meeting\nDate: March 12, 2026\nTime: 2:00 PM - 3:00 PM ET\nLocation: Conference Room B\n\nAgenda:\n- Q1 actuals vs budget\n- Q2 budget finalization\n- Headcount planning\n\nAccept | Decline | Tentative'
    }),

    _e(46, 46, { name: 'Calendly', email: 'notifications@calendly.com' }, 'New booking: David Kim - Partnership Discussion', 'David Kim booked a 30-min meeting with you on March 10 at 3:00 PM ET', '2026-03-06T14:30:00Z', {
        isRead: true, splitCategory: 'calendar', autoLabel: 'Calendar Invite'
    }),

    _e(47, 47, _from('ct_16'), 'Calendar: Sprint 24 Planning - March 8', 'Nate Patel has invited you to Sprint 24 Planning on March 8 at 9:00 AM', '2026-03-05T17:00:00Z', {
        isRead: true, splitCategory: 'calendar', autoLabel: 'Calendar Invite'
    }),

    _e(48, 48, { name: 'Google Calendar', email: 'calendar-notification@google.com' }, 'Event update: All-Hands moved to 3:00 PM', 'All-Hands Meeting has been rescheduled to March 9 at 3:00 PM ET (was 2:00 PM)', '2026-03-05T11:00:00Z', {
        isRead: true, splitCategory: 'calendar', autoLabel: 'Calendar Invite'
    }),

    _e(49, 49, _from('ct_30'), 'Calendar: Executive Team Dinner - March 14', 'Patrick O\'Neil has invited you to Executive Team Dinner on March 14 at 7:00 PM', '2026-03-04T16:00:00Z', {
        isRead: true, splitCategory: 'calendar', autoLabel: 'Calendar Invite'
    }),

    // === DONE (archived) emails ===
    _e(50, 50, _from('ct_01'), 'Re: Q1 Sales Numbers', 'Final Q1 numbers: $3.2M ARR added, 127% of target. Enterprise segment leading at 145%.', '2026-03-03T14:00:00Z', {
        isRead: true, isDone: true, labels: ['label_1']
    }),

    _e(51, 51, _from('ct_08'), 'Server Maintenance Complete', 'All servers updated to latest patches. Zero downtime achieved during the maintenance window.', '2026-03-03T06:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11']
    }),

    _e(52, 52, _from('ct_16'), 'Re: Code Review - Auth Module', 'LGTM! Approved the PR. Nice work on the token refresh logic.', '2026-03-02T20:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11']
    }),

    _e(53, 53, _from('ct_05'), 'Travel Expenses Approved', 'Your travel expenses for the SaaS Connect conference ($4,230) have been approved and will be reimbursed.', '2026-03-02T12:00:00Z', {
        isRead: true, isDone: true, labels: ['label_3', 'label_6']
    }),

    _e(54, 54, _from('ct_21'), 'Design Sprint Wrap-up', 'Great work on the design sprint! The new onboarding flow prototype tested really well with users.', '2026-03-01T18:00:00Z', {
        isRead: true, isDone: true, labels: ['label_10']
    }),

    _e(55, 55, { name: 'Amazon', email: 'order-update@amazon.com' }, 'Your order has been delivered', 'Your order #112-3456789-0123456 was delivered today at 2:14 PM.', '2026-03-01T14:15:00Z', {
        isRead: true, isDone: true, labels: ['label_13'], autoLabel: 'Shipping Update'
    }),

    _e(56, 56, _from('ct_02'), 'Re: Logo Concepts - Round 2', 'Going with Concept C. Updated files will be ready by Monday.', '2026-02-28T16:00:00Z', {
        isRead: true, isDone: true, labels: ['label_12']
    }),

    _e(57, 57, _from('ct_13'), 'Offer Letter Sent - Jordan Lee', 'Offer letter sent to Jordan Lee for the Engineering Manager role. Salary: $195K + equity.', '2026-02-28T11:00:00Z', {
        isRead: true, isDone: true, labels: ['label_8']
    }),

    _e(58, 58, _from('ct_09'), 'Thank You for the Donation', 'Thank you for Acme\'s generous $10,000 donation to the Global Health Initiative.', '2026-02-27T09:00:00Z', {
        isRead: true, isDone: true
    }),

    _e(59, 59, _from('ct_24'), 'Integration Testing Complete', 'All integration tests passing. The SaaS Platform connector is ready for production.', '2026-02-26T15:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11']
    }),

    _e(60, 60, _from('ct_22'), 'Article Published: "Acme\'s Rise in Enterprise SaaS"', 'The article went live this morning. Here\'s the link: https://sportsnews.com/tech/acme-enterprise', '2026-02-25T08:00:00Z', {
        isRead: true, isDone: true, labels: ['label_12']
    }),

    _e(61, 61, _from('ct_18'), 'Consulting Engagement Summary', 'Summary of our Q1 consulting engagement. Total hours: 120, key deliverables attached.', '2026-02-24T14:00:00Z', {
        isRead: true, isDone: true, labels: ['label_3']
    }),

    _e(62, 62, _from('ct_20'), 'Office Renovation Plans', 'The architect has completed the renovation plans for the 3rd floor expansion.', '2026-02-23T10:00:00Z', {
        isRead: true, isDone: true
    }),

    _e(63, 63, _from('ct_17'), 'Corporate Wellness Program Proposal', 'Here\'s our proposal for Acme\'s corporate wellness program. Includes gym memberships and wellness days.', '2026-02-22T13:00:00Z', {
        isRead: true, isDone: true
    }),

    // === REMINDERS (snoozed) ===
    _e(64, 64, _from('ct_04'), 'Patent Filing Deadline - April 15', 'Reminder: The provisional patent for the AI workflow engine expires April 15. We need to file.', '2026-02-20T10:00:00Z', {
        isRead: true, labels: ['label_9'], remindAt: '2026-03-10T09:00:00Z'
    }),

    _e(65, 65, _from('ct_06'), 'Re: Payment Terms Discussion', 'Can we revisit the NET-60 terms? Our finance team prefers NET-30 for new partnerships.', '2026-02-18T14:00:00Z', {
        isRead: true, labels: ['label_3', 'label_4'], remindAt: '2026-03-08T10:00:00Z'
    }),

    _e(66, 66, _from('ct_23'), 'EdTech Academy Partnership', 'Would love to discuss an educational partnership. Our platform serves 50K+ students.', '2026-02-15T09:00:00Z', {
        isRead: true, remindAt: '2026-03-12T09:00:00Z'
    }),

    _e(67, 67, _from('ct_27'), 'TokyoTech Conference Invitation', 'You\'re invited to speak at TokyoTech Summit in June. Topic: "Enterprise AI at Scale"', '2026-02-10T05:00:00Z', {
        isRead: true, labels: ['label_14', 'label_6'], remindAt: '2026-03-15T09:00:00Z'
    }),

    // === SENT ===
    _e(68, 68, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Re: Series B Term Sheet Discussion', 'Emily, thanks for the feedback. Let\'s discuss Thursday at 2pm PT. I\'ll send a calendar invite.', '2026-03-06T14:00:00Z', {
        isRead: true, to: _sentTo(['emily.r@venturelabs.co']), labels: ['label_5']
    }),

    _e(69, 69, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Quarterly Board Update - Q1 2026', 'Board members, please find attached the Q1 2026 quarterly update for review ahead of our March 10 meeting.', '2026-03-05T16:00:00Z', {
        isRead: true, to: _sentTo(['emily.r@venturelabs.co', 'lena.j@nordicventures.se', 'patrick.oneil@acmecorp.com']),
        hasAttachments: true, attachments: [{ name: 'Acme_Q1_Board_Update.pdf', size: '8.1 MB' }],
        readReceipt: { opened: true, openedAt: '2026-03-05T18:30:00Z', device: 'MacBook Pro', openCount: 4, readers: [
            { name: 'Emily Rodriguez', openedAt: '2026-03-05T17:15:00Z', device: 'iPhone' },
            { name: 'Lena Johansson', openedAt: '2026-03-05T18:30:00Z', device: 'MacBook Pro' },
            { name: 'Patrick O\'Neil', openedAt: '2026-03-05T19:00:00Z', device: 'Windows Desktop' }
        ]}
    }),

    _e(70, 70, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Welcome to the team, Jordan!', 'Jordan, thrilled to have you joining Acme as Engineering Manager. Your start date is March 24.', '2026-03-04T10:00:00Z', {
        isRead: true, to: [{ name: 'Jordan Lee', email: 'jordan.lee@gmail.com' }],
        cc: [{ name: 'Rachel Foster', email: 'rachel.foster@acmecorp.com' }],
        readReceipt: { opened: true, openedAt: '2026-03-04T10:15:00Z', device: 'iPhone', openCount: 5 }
    }),

    _e(71, 71, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Re: Partnership Opportunity - FinancePlus x Acme', 'David, great catching up at SaaS Connect. Let\'s schedule a call - my booking page: https://cal.superhuman.com/alex', '2026-03-03T09:00:00Z', {
        isRead: true, to: _sentTo(['david.kim@financeplus.com']),
        readReceipt: { opened: true, openedAt: '2026-03-03T09:30:00Z', device: 'MacBook Pro', openCount: 3 }
    }),

    _e(72, 72, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Team Offsite - Save the Date: March 12', 'Team, saving the date for our annual product team offsite on March 12 at Cavallo Point in Sausalito.', '2026-03-01T11:00:00Z', {
        isRead: true, to: _sentTo(['sarah.chen@acmecorp.com', 'nate.patel@acmecorp.com', 'maya.patel@acmecorp.com', 'tom.bradley@acmecorp.com', 'ben.carter@acmecorp.com', 'rachel.foster@acmecorp.com']),
        readReceipt: { opened: true, openedAt: '2026-03-01T11:30:00Z', device: 'various', openCount: 18 }
    }),

    // === DRAFTS ===
    _e(73, 73, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Re: EuroDesign Conference - Speaker Invitation', 'Hi Sophie, thank you for the invitation. I\'d be delighted to speak at EuroDesign Summit...', '2026-03-07T08:00:00Z', {
        isDraft: true, to: _sentTo(['sophie.l@eurodesign.fr']),
        body: 'Hi Sophie,\n\nThank you for the invitation. I\'d be delighted to speak at EuroDesign Summit 2026.\n\nThe proposed topic "Building Products That Scale" works well. I could also cover:\n- AI-first design principles\n- Cross-functional collaboration at scale\n- Metrics-driven product development\n\nLet me know which angle you prefer.\n\nBest,\nAlex'
    }),

    _e(74, 74, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Proposal: Acme x BioMed Research Collaboration', 'Dear Jennifer, thank you for the research collaboration proposal. We\'re very interested...', '2026-03-06T17:00:00Z', {
        isDraft: true, to: _sentTo(['jennifer.wu@biomedresearch.com']),
        body: 'Dear Jennifer,\n\nThank you for the research collaboration proposal. We\'re very interested in exploring how Acme\'s platform can improve diagnostic workflows.\n\nA few thoughts:\n- We can commit engineering resources starting Q2\n- Would love to discuss data governance and privacy frameworks\n- The NIH grant angle is very appealing\n\nShall we set up an introductory call with our respective teams?'
    }),

    // === SPAM ===
    _e(75, 75, { name: 'Prince Okafor', email: 'prince.okafor@yahoo.ng' }, 'URGENT: Inheritance Notification - $4.5M USD', 'Dear Sir/Madam, I am writing to inform you of an inheritance of $4.5 million...', '2026-03-06T04:00:00Z', {
        isRead: false, isSpam: true
    }),

    _e(76, 76, { name: 'CryptoGains Now', email: 'invest@cryptogainsnow.biz' }, 'Make $50K/day with this ONE trick!', 'Revolutionary AI trading bot guarantees 500% returns...', '2026-03-05T22:00:00Z', {
        isRead: false, isSpam: true
    }),

    _e(77, 77, { name: 'Discount Pharma', email: 'deals@pharma-discount.xyz' }, 'Limited Time: 90% Off Premium Products', 'Act now for incredible savings on premium health products...', '2026-03-05T03:00:00Z', {
        isRead: false, isSpam: true
    }),

    // === TRASH ===
    _e(78, 78, { name: 'SurveyMonkey', email: 'no-reply@surveymonkey.com' }, 'Complete Your Survey - Win a $500 Gift Card', 'You\'ve been selected to participate in our annual satisfaction survey...', '2026-03-04T12:00:00Z', {
        isRead: true, isTrashed: true
    }),

    _e(79, 79, { name: 'Webinar World', email: 'events@webinarworld.com' }, 'You\'re Invited: 10X Your Pipeline Webinar', 'Join our exclusive webinar on pipeline generation strategies...', '2026-03-03T09:00:00Z', {
        isRead: true, isTrashed: true
    }),

    // === STARRED ===
    _e(80, 80, _from('ct_05'), 'FY2026 Budget Summary', 'Final FY2026 budget: $12.4M total. Breakdown by department attached.', '2026-02-20T09:00:00Z', {
        isRead: true, isStarred: true, isDone: true, labels: ['label_3'],
        hasAttachments: true, attachments: [{ name: 'FY2026_Budget.xlsx', size: '2.1 MB' }]
    }),

    _e(81, 81, _from('ct_30'), 'Company Vision & Strategy 2026-2028', 'Team, sharing the updated company vision and 3-year strategy document.', '2026-02-15T10:00:00Z', {
        isRead: true, isStarred: true, isDone: true, labels: ['label_1'],
        hasAttachments: true, attachments: [{ name: 'Acme_Strategy_2026-2028.pdf', size: '6.5 MB' }]
    }),

    _e(82, 82, _from('ct_01'), 'Customer Success Metrics - February', 'Feb metrics: NPS 72 (+5), churn 1.2% (-0.3%), CSAT 4.6/5.0', '2026-03-01T10:00:00Z', {
        isRead: true, isStarred: true, isDone: true, labels: ['label_4']
    }),

    // More inbox emails for density
    _e(83, 83, _from('ct_26'), 'Vendor Security Assessment - Q1 Results', 'Alex, completed the quarterly vendor security assessment. 3 vendors need attention...', '2026-03-05T08:00:00Z', {
        isRead: true, labels: ['label_1'], splitCategory: 'important',
        body: 'Alex,\n\nCompleted the quarterly vendor security assessment.\n\nPassed: 12 vendors\nNeeds attention: 3 vendors\n- CloudScale: Missing SOC 2 Type II (in progress, ETA April)\n- MarketingPro: Outdated TLS 1.1 on staging servers\n- LogisticsPro: No MFA enforced for admin accounts\n\nI\'ve notified all three and set remediation deadlines.\n\nBen'
    }),

    _e(84, 84, { name: 'Greenhouse', email: 'no-reply@greenhouse.io' }, '5 new applicants for Senior Product Designer', 'You have 5 new applicants for the Senior Product Designer role.', '2026-03-06T08:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_8']
    }),

    _e(85, 85, { name: 'PagerDuty', email: 'alerts@pagerduty.com' }, '[TRIGGERED] High Error Rate - Payment Service', 'Error rate for payment-service exceeded 5% threshold. Current: 7.2%.', '2026-03-06T02:30:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_11', 'label_5']
    }),

    _e(86, 86, { name: 'PagerDuty', email: 'alerts@pagerduty.com' }, '[RESOLVED] High Error Rate - Payment Service', 'Error rate for payment-service returned to normal. Duration: 47 minutes.', '2026-03-06T03:17:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_11']
    }),

    _e(87, 87, _from('ct_21'), 'Re: User Research Findings - Onboarding Flow', 'Updated the research doc with last week\'s interviews. Key insight: users want a guided setup wizard.', '2026-03-04T17:00:00Z', {
        isRead: true, isDone: true, labels: ['label_10']
    }),

    _e(88, 88, { name: 'Zendesk', email: 'support@zendesk.com' }, 'Weekly Support Metrics - Feb 28 - Mar 6', 'Tickets opened: 234, Resolved: 219, Avg response time: 2.3 hours, CSAT: 94%', '2026-03-06T07:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(89, 89, _from('ct_11'), 'Follow-up: Media Coverage Tracking', 'Alex, tracking our media mentions this week: 12 articles, 3 podcasts, 2 TV segments.', '2026-03-05T13:00:00Z', {
        isRead: true, isDone: true, labels: ['label_12']
    }),

    _e(90, 90, { name: 'Intercom', email: 'notifications@intercom.io' }, '3 conversations need your attention', 'You have 3 unresolved conversations assigned to you in Intercom.', '2026-03-06T11:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(91, 91, _from('ct_08'), 'Re: Load Testing Results', 'Load test complete: 50K concurrent users, p99 latency 180ms, zero errors. We\'re good to go.', '2026-03-03T16:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11']
    }),

    _e(92, 92, { name: 'Expensify', email: 'reports@expensify.com' }, '4 expense reports pending your approval', 'You have 4 expense reports waiting for your approval. Total: $8,420.', '2026-03-05T09:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_3']
    }),

    _e(93, 93, _from('ct_29'), 'Content Calendar - March 2026', 'Here\'s the content calendar for March. 12 blog posts, 4 case studies, 2 whitepapers planned.', '2026-03-02T10:00:00Z', {
        isRead: true, isDone: true, labels: ['label_12']
    }),

    _e(94, 94, _from('ct_16'), 'API Rate Limiting Implementation', 'Pushed the rate limiting changes. New limits: 100 req/s per API key, 1000 req/s per org.', '2026-03-02T14:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11']
    }),

    _e(95, 95, { name: 'United Airlines', email: 'notifications@united.com' }, 'Flight Confirmation: SFO to JFK - March 15', 'Your flight UA 234 on March 15 is confirmed. Departs SFO 7:00 AM, arrives JFK 3:30 PM.', '2026-03-04T12:00:00Z', {
        isRead: true, splitCategory: 'other', labels: ['label_6'], autoLabel: 'Notification'
    }),

    _e(96, 96, { name: 'Zoom', email: 'no-reply@zoom.us' }, 'Cloud Recording Available: Product Roadmap Review', 'Your cloud recording for "Product Roadmap Review" is now available.', '2026-03-04T11:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(97, 97, _from('ct_13'), 'Re: Employee Engagement Survey Results', 'Overall engagement: 82% (+4% from last quarter). Top concerns: workload balance and career growth.', '2026-02-28T15:00:00Z', {
        isRead: true, isDone: true, labels: ['label_8']
    }),

    _e(98, 98, { name: 'Apple', email: 'no-reply@apple.com' }, 'Your Apple Developer account renewal', 'Your Apple Developer Program membership will auto-renew on March 20 for $99.', '2026-03-05T06:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_3']
    }),

    _e(99, 99, _from('ct_26'), 'SOC 2 Audit Progress Update', 'Quick update: SOC 2 Type II audit is 75% complete. On track for April certification.', '2026-03-01T09:00:00Z', {
        isRead: true, isDone: true, labels: ['label_1']
    }),

    _e(100, 100, { name: 'Twilio', email: 'alerts@twilio.com' }, 'SMS delivery rate dropped below 95%', 'Your Twilio SMS delivery rate dropped to 92.3% in the US region.', '2026-03-05T04:00:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_11']
    }),

    // More emails for volume
    _e(101, 101, _from('ct_28'), 'CloudScale Migration Checklist', 'Alex, here\'s the pre-migration checklist. 14 items, 11 completed.', '2026-02-28T10:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11']
    }),

    _e(102, 102, { name: 'Jira', email: 'notifications@atlassian.com' }, 'Sprint 23 completed - 42 of 45 stories done', 'Sprint 23 has been completed. Velocity: 42 story points. 3 stories carried over.', '2026-03-03T17:00:00Z', {
        isRead: true, splitCategory: 'other', isDone: true, autoLabel: 'Notification'
    }),

    _e(103, 103, _from('ct_01'), 'Customer Escalation - Enterprise Client', 'Heads up: MegaCorp is escalating an issue with data export. They\'re threatening to churn.', '2026-03-04T08:30:00Z', {
        isRead: true, isDone: true, labels: ['label_4', 'label_5'],
        replyDraftingTeammate: 'Sarah Chen'
    }),

    _e(104, 104, _from('ct_05'), 'Re: Headcount Planning - Q2', 'Approved 8 new hires for Q2: 4 engineering, 2 product, 1 design, 1 marketing.', '2026-02-26T11:00:00Z', {
        isRead: true, isDone: true, labels: ['label_1', 'label_8']
    }),

    _e(105, 105, { name: 'Google Analytics', email: 'analytics-noreply@google.com' }, 'Weekly Analytics Report - acmecorp.com', 'Sessions: 245K (+18%), Conversions: 1,847, Revenue: $127K', '2026-03-03T06:00:00Z', {
        isRead: true, splitCategory: 'other', isDone: true, autoLabel: 'Notification', labels: ['label_12']
    }),

    _e(106, 106, _from('ct_07'), 'Re: Website Copy Review', 'Updated the hero copy and CTA. "Transform your workflow" tested 40% better than "Optimize your process".', '2026-02-27T14:00:00Z', {
        isRead: true, isDone: true, labels: ['label_12']
    }),

    _e(107, 107, { name: 'Segment', email: 'alerts@segment.com' }, 'Data pipeline alert: 2 sources disconnected', 'HubSpot and Salesforce sources disconnected. Last sync: 6 hours ago.', '2026-03-04T03:00:00Z', {
        isRead: true, splitCategory: 'other', isDone: true, autoLabel: 'Notification', labels: ['label_11']
    }),

    _e(108, 108, _from('ct_24'), 'API v2 Documentation Ready', 'The v2 API docs are live at docs.saasplatform.io/v2. Major changes: GraphQL support, webhooks v2.', '2026-02-25T10:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11']
    }),

    _e(109, 109, _from('ct_29'), 'Case Study: How MegaCorp Saved 200 Hours/Month', 'The MegaCorp case study is ready for review. Key stat: 200 hours saved per month using Acme.', '2026-02-24T16:00:00Z', {
        isRead: true, isDone: true, labels: ['label_12', 'label_4']
    }),

    _e(110, 110, { name: 'npm', email: 'support@npmjs.com' }, 'Security advisory: 2 vulnerabilities in dependencies', 'Found 2 moderate severity vulnerabilities in your project dependencies.', '2026-03-03T08:00:00Z', {
        isRead: true, splitCategory: 'other', isDone: true, autoLabel: 'Notification', labels: ['label_11']
    }),

    // Emails with auto-reminders (sent emails awaiting reply)
    _e(111, 111, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Proposal: Enterprise Pricing Update', 'Hi David, following up on our pricing discussion. Attached is the updated enterprise tier proposal.', '2026-03-02T15:00:00Z', {
        isRead: true, to: _sentTo(['david.kim@financeplus.com']),
        remindAt: '2026-03-07T09:00:00Z',
        hasAttachments: true, attachments: [{ name: 'Enterprise_Pricing_v2.pdf', size: '1.5 MB' }],
        readReceipt: { opened: true, openedAt: '2026-03-02T16:30:00Z', device: 'MacBook Pro', openCount: 7 }
    }),

    _e(112, 112, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Re: Nordic Ventures - Follow-up', 'Lena, great meeting you too. Happy to schedule a call. Here\'s my availability next week...', '2026-03-04T11:00:00Z', {
        isRead: true, to: _sentTo(['lena.j@nordicventures.se']),
        remindAt: '2026-03-09T09:00:00Z',
        readReceipt: { opened: false }
    }),

    // A few more inbox emails for realistic volume
    _e(113, 113, _from('ct_08'), 'Database Performance Report - March', 'Monthly DB report: Query performance improved 23% after index optimization. Details inside.', '2026-03-07T04:00:00Z', {
        isRead: false, labels: ['label_11'], splitCategory: 'important',
        body: 'Monthly database performance report:\n\n- Query p50: 12ms (was 18ms)\n- Query p99: 89ms (was 145ms)\n- Connection pool utilization: 62%\n- Slow queries (>500ms): 3 (was 17)\n- Storage growth: +2.1 TB (total: 14.7 TB)\n\nOptimizations applied:\n- Added composite indexes on 4 tables\n- Partitioned the events table by month\n- Upgraded to PostgreSQL 16.2\n\nNext month focus: Read replica lag reduction.\n\nTom'
    }),

    _e(114, 114, _from('ct_21'), 'Accessibility Audit Results', 'Completed the WCAG 2.1 AA audit. 94% compliance, 12 issues found (mostly contrast ratios).', '2026-03-07T03:30:00Z', {
        isRead: false, labels: ['label_10'], splitCategory: 'important'
    }),

    _e(115, 115, { name: 'Netlify', email: 'team@netlify.com' }, 'Deploy failed: acme-marketing-site', 'Build failed for acme-marketing-site. Error: Module not found in pages/pricing.tsx', '2026-03-07T02:00:00Z', {
        isRead: false, splitCategory: 'other', autoLabel: 'Notification', labels: ['label_11']
    }),

    _e(116, 116, { name: 'CircleCI', email: 'builds@circleci.com' }, 'Build #4521 passed: acme/platform (main)', 'All 847 tests passed. Build time: 8m 42s. Coverage: 87.3%.', '2026-03-07T01:30:00Z', {
        isRead: true, splitCategory: 'other', autoLabel: 'Notification'
    }),

    _e(117, 117, _from('ct_01'), 'Re: Customer Success Playbook v2', 'Updated the CS playbook with the new onboarding flow. Ready for your review.', '2026-03-04T13:00:00Z', {
        isRead: true, isDone: true, labels: ['label_4']
    }),

    _e(118, 118, { name: 'Calendly', email: 'notifications@calendly.com' }, 'Reminder: You have 3 upcoming meetings tomorrow', 'Product Roadmap Review (9:00 AM), Weekly Standup (10:30 AM), Lunch with Marcus (12:00 PM)', '2026-03-06T20:00:00Z', {
        isRead: true, splitCategory: 'calendar', autoLabel: 'Calendar Invite'
    }),

    _e(119, 119, _from('ct_16'), 'Feature Flag Cleanup Proposal', 'We have 47 stale feature flags. Proposing to remove 32 that have been 100% rolled out for 30+ days.', '2026-03-05T16:00:00Z', {
        isRead: true, labels: ['label_11'], splitCategory: 'important'
    }),

    _e(120, 120, _from('ct_13'), 'New Employee Onboarding - Week of March 24', 'Jordan Lee starts March 24. Onboarding schedule and buddy assignments attached.', '2026-03-05T12:00:00Z', {
        isRead: true, labels: ['label_8'], splitCategory: 'important',
        hasAttachments: true, attachments: [{ name: 'Onboarding_Schedule_JordanLee.pdf', size: '420 KB' }]
    }),

    // A few more for 120+ total
    _e(121, 121, { name: 'Cloudflare', email: 'alerts@cloudflare.com' }, 'DDoS Attack Mitigated - acmecorp.com', 'A Layer 7 DDoS attack was automatically mitigated. Peak: 2.4M requests/second. Zero downtime.', '2026-03-04T01:30:00Z', {
        isRead: true, splitCategory: 'other', isDone: true, autoLabel: 'Notification', labels: ['label_11']
    }),

    _e(122, 122, _from('ct_26'), 'Re: Disaster Recovery Test Results', 'DR test successful. RTO: 4 minutes (target: 15), RPO: 0 (target: 1 hour). Full report attached.', '2026-02-28T14:00:00Z', {
        isRead: true, isDone: true, labels: ['label_11'],
        hasAttachments: true, attachments: [{ name: 'DR_Test_Report_Feb2026.pdf', size: '1.8 MB' }]
    }),

    _e(123, 123, _from('ct_05'), 'Tax Filing Reminder - March 15 Deadline', 'Reminder: Corporate estimated tax payments due March 15. Amount: $234,000.', '2026-03-03T08:00:00Z', {
        isRead: true, isDone: true, labels: ['label_3']
    }),

    _e(124, 124, { name: 'Y Combinator', email: 'newsletter@ycombinator.com' }, 'YC Newsletter: Top 10 Startups to Watch in 2026', 'This month\'s picks include companies in AI, climate tech, and healthcare...', '2026-03-01T10:00:00Z', {
        isRead: true, splitCategory: 'other', isDone: true, autoLabel: 'Newsletter'
    }),

    _e(125, 125, _from('ct_02'), 'Brand Photography Session - Schedule', 'Alex, the brand photography session is scheduled for March 20. Location: Studio on 4th, 10am-2pm.', '2026-02-27T11:00:00Z', {
        isRead: true, isDone: true, labels: ['label_12']
    }),

    _e(126, 126, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Re: Guest Lecture Request - Stanford', 'Professor Singh, I\'d be happy to give the guest lecture. April 8 works perfectly.', '2026-03-05T10:00:00Z', {
        isRead: true, to: _sentTo(['robert.singh@university.edu']),
        readReceipt: { opened: true, openedAt: '2026-03-05T10:45:00Z', device: 'iMac', openCount: 2 }
    }),

    _e(127, 127, { name: 'Alex Morgan', email: 'alex.morgan@acmecorp.com' }, 'Infrastructure Migration Sign-off', 'Tom, Phase 2 is approved. Please proceed with the production migration starting Monday.', '2026-03-06T09:00:00Z', {
        isRead: true, to: _sentTo(['tom.bradley@acmecorp.com'])
    }),

    _e(128, 128, _from('ct_30'), 'Re: Company All-Hands Agenda', 'Added the Q1 wins section and customer spotlight. Priya will present financials.', '2026-03-05T14:00:00Z', {
        isRead: true, isDone: true, labels: ['label_1']
    })
];

// ---- Read Receipts (Recent Opens feed) ----
const RECENT_OPENS = [
    { emailId: 69, reader: 'Emily Rodriguez', openedAt: '2026-03-07T08:30:00Z', device: 'iPhone' },
    { emailId: 111, reader: 'David Kim', openedAt: '2026-03-07T07:45:00Z', device: 'MacBook Pro' },
    { emailId: 69, reader: 'Lena Johansson', openedAt: '2026-03-07T07:00:00Z', device: 'Windows Desktop' },
    { emailId: 72, reader: 'Nate Patel', openedAt: '2026-03-07T06:30:00Z', device: 'iPhone' },
    { emailId: 72, reader: 'Maya Patel', openedAt: '2026-03-07T06:15:00Z', device: 'MacBook Pro' },
    { emailId: 70, reader: 'Jordan Lee', openedAt: '2026-03-07T05:00:00Z', device: 'Android' },
    { emailId: 126, reader: 'Robert Singh', openedAt: '2026-03-06T22:00:00Z', device: 'iMac' },
    { emailId: 111, reader: 'David Kim', openedAt: '2026-03-06T18:00:00Z', device: 'iPhone' },
    { emailId: 69, reader: 'Patrick O\'Neil', openedAt: '2026-03-06T17:30:00Z', device: 'MacBook Pro' },
    { emailId: 71, reader: 'David Kim', openedAt: '2026-03-06T14:00:00Z', device: 'MacBook Pro' },
    { emailId: 72, reader: 'Tom Bradley', openedAt: '2026-03-06T12:00:00Z', device: 'iPhone' },
    { emailId: 72, reader: 'Ben Carter', openedAt: '2026-03-06T11:45:00Z', device: 'MacBook Pro' },
    { emailId: 72, reader: 'Sarah Chen', openedAt: '2026-03-06T11:30:00Z', device: 'iPhone' },
    { emailId: 72, reader: 'Rachel Foster', openedAt: '2026-03-06T11:15:00Z', device: 'Windows Desktop' }
];

// ---- Booking Pages ----
const BOOKING_PAGES = [
    {
        id: 'bp_1', title: 'Chat with Alex', duration: 30, location: 'Zoom',
        description: 'Book a 30-minute chat with me.',
        availability: { days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], startTime: '09:00', endTime: '17:00' },
        link: 'https://cal.superhuman.com/alex/chat',
        isActive: true
    },
    {
        id: 'bp_2', title: 'Product Demo', duration: 45, location: 'Zoom',
        description: 'See Acme in action with a personalized demo.',
        availability: { days: ['Tue', 'Thu'], startTime: '10:00', endTime: '16:00' },
        link: 'https://cal.superhuman.com/alex/demo',
        isActive: true
    },
    {
        id: 'bp_3', title: 'Quick Sync', duration: 15, location: 'Google Meet',
        description: 'A quick 15-minute sync.',
        availability: { days: ['Mon', 'Wed', 'Fri'], startTime: '08:00', endTime: '18:00' },
        link: 'https://cal.superhuman.com/alex/quick',
        isActive: false
    }
];
