# Elation Health — Patient Communication

Elation Health is an electronic health record (EHR) platform for primary care practices. This environment covers the **Patient Communication** module, which handles messaging between providers and patients.

## Components to Implement

### Message Inbox
- List of patient messages with columns: patient name, subject/topic, date received, status (unread, read, replied, resolved)
- Filter by status, date range, provider, message category
- Search by patient name or message content
- Unread count badge
- Sort by date or patient name

### Message Thread View
- Conversation thread with patient (chronological messages)
- Each message shows: sender (patient or provider), timestamp, message body
- Attachments (lab results, documents, images) displayed inline or as download links
- Reply text area with send button
- Mark as resolved / reopen controls
- Assign to different provider option

### Compose New Message
- Patient selection (searchable by name, DOB, or MRN)
- Message category/type (general inquiry, prescription refill, appointment request, lab results, referral, billing)
- Subject line
- Message body editor
- Attach file/document
- Urgency flag (routine, urgent)
- Send or save as draft

### Patient Portal Settings
- Enable/disable patient portal messaging
- Auto-reply message configuration (e.g., out-of-office)
- Message routing rules (route by category to specific providers or staff)
- Response time expectations display setting
- Allowed message categories toggle

### Appointment Reminders
- Enable/disable automated appointment reminders
- Reminder timing configuration (e.g., 24 hours before, 48 hours before)
- Reminder delivery method (email, SMS, both)
- Reminder message template customization
- Confirmation/cancellation link inclusion toggle

### Broadcast Messages
- Create broadcast message to patient groups
- Patient group selection (all patients, by condition, by last visit date, by provider panel, custom list)
- Message template editor
- Schedule send (immediate or future date)
- Delivery status tracking (sent, delivered, opened)

### Communication Templates
- List of reusable message templates
- Create/edit/delete templates
- Template categories (follow-up, lab results, appointment, general)
- Template variables/placeholders (patient name, appointment date, etc.)
