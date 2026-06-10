/* ============================================================
   Elation Patient Communication — View Renderers
   ============================================================ */

const Views = {

    // ── Sidebar ─────────────────────────────────────────────
    renderSidebar() {
        const unread = AppState.getUnreadInboxCount();
        const drafts = AppState.getDraftLetters().length;
        const reminders = AppState.getUnacknowledgedReminders().length;
        const v = AppState.currentView;

        let html = '<nav class="sidebar-nav">';
        html += `<div class="nav-item ${v === 'home' ? 'active' : ''}" data-route="home" data-testid="nav-home"><span class="nav-icon">&#x1F3E0;</span><span class="nav-text">Practice Home</span></div>`;
        html += `<div class="nav-item ${v === 'inbox' ? 'active' : ''}" data-route="inbox" data-testid="nav-inbox"><span class="nav-icon">&#x1F4E8;</span><span class="nav-text">Patient Letters</span>${unread > 0 ? `<span class="nav-badge">${unread}</span>` : ''}</div>`;
        html += `<div class="nav-item ${v === 'sent' ? 'active' : ''}" data-route="sent" data-testid="nav-sent"><span class="nav-icon">&#x1F4E4;</span><span class="nav-text">Sent</span></div>`;
        html += `<div class="nav-item ${v === 'drafts' ? 'active' : ''}" data-route="drafts" data-testid="nav-drafts"><span class="nav-icon">&#x1F4DD;</span><span class="nav-text">Drafts</span>${drafts > 0 ? `<span class="nav-badge">${drafts}</span>` : ''}</div>`;
        html += `<div class="nav-item ${v === 'reminders' ? 'active' : ''}" data-route="reminders" data-testid="nav-reminders"><span class="nav-icon">&#x1F514;</span><span class="nav-text">Reminders</span>${reminders > 0 ? `<span class="nav-badge">${reminders}</span>` : ''}</div>`;
        html += '<div class="nav-divider"></div>';
        html += `<div class="nav-item ${v === 'patients' ? 'active' : ''}" data-route="patients" data-testid="nav-patients"><span class="nav-icon">&#x1F465;</span><span class="nav-text">Patients</span></div>`;
        html += `<div class="nav-item ${v === 'appointments' ? 'active' : ''}" data-route="appointments" data-testid="nav-appointments"><span class="nav-icon">&#x1F4C5;</span><span class="nav-text">Appointments</span></div>`;
        html += `<div class="nav-item ${v === 'bulk-letters' ? 'active' : ''}" data-route="bulk-letters" data-testid="nav-bulk-letters"><span class="nav-icon">&#x1F4E7;</span><span class="nav-text">Bulk Letters</span></div>`;
        html += '<div class="nav-divider"></div>';
        html += `<div class="nav-item ${v === 'settings' ? 'active' : ''}" data-route="settings" data-testid="nav-settings"><span class="nav-icon">&#x2699;</span><span class="nav-text">Settings</span></div>`;
        html += '</nav>';
        return html;
    },

    // ── Practice Home (Dashboard) ───────────────────────────
    renderHome() {
        const inboxLetters = AppState.getInboxLetters().slice(0, 10);
        const reminders = AppState.getUnacknowledgedReminders();
        const upcoming = AppState.getUpcomingAppointments().slice(0, 5);
        const unread = AppState.getUnreadInboxCount();

        let html = '<div class="page-content" data-testid="practice-home">';
        html += '<h1 class="page-title">Practice Home</h1>';
        html += '<div class="dashboard-grid">';

        // Patient Letters section
        html += '<div class="dashboard-card">';
        html += `<div class="card-header"><h2>Patient Letters</h2>${unread > 0 ? `<span class="card-badge">${unread} unread</span>` : ''}</div>`;
        if (inboxLetters.length === 0) {
            html += '<div class="card-empty">No patient letters</div>';
        } else {
            html += '<div class="letter-list">';
            for (const ltr of inboxLetters) {
                const patient = AppState.getPatient(ltr.patientId);
                const pName = patient ? `${patient.firstName} ${patient.lastName}` : 'Unknown';
                html += `<div class="letter-item ${!ltr.isRead ? 'unread' : ''}" data-action="open-conversation" data-conversation="${ltr.conversationId}" data-patient="${ltr.patientId}" data-testid="letter-${ltr.id}">`;
                html += `<div class="letter-sender">${Components.escapeHtml(pName)}</div>`;
                html += `<div class="letter-subject">${Components.escapeHtml(ltr.category || ltr.subject)}</div>`;
                html += `<div class="letter-preview">${Components.escapeHtml(ltr.body.substring(0, 80))}...</div>`;
                html += `<div class="letter-date">${Components.formatDate(ltr.sentAt)}</div>`;
                html += '</div>';
            }
            html += '</div>';
            html += `<div class="card-footer"><a data-route="inbox" class="link">View all patient letters</a></div>`;
        }
        html += '</div>';

        // Reminders section
        html += '<div class="dashboard-card">';
        html += `<div class="card-header"><h2>Reminders</h2>${reminders.length > 0 ? `<span class="card-badge">${reminders.length}</span>` : ''}</div>`;
        if (reminders.length === 0) {
            html += '<div class="card-empty">No pending reminders</div>';
        } else {
            html += '<div class="reminder-list">';
            for (const rem of reminders) {
                html += `<div class="reminder-item" data-testid="reminder-${rem.id}">`;
                html += `<div class="reminder-text">${Components.escapeHtml(rem.description)}</div>`;
                html += `<div class="reminder-date">${Components.timeAgo(rem.createdAt)}</div>`;
                html += '<div class="reminder-actions">';
                if (rem.type === 'unread_alert') {
                    html += `<button class="btn btn-sm btn-secondary" data-action="reminder-resend" data-reminder="${rem.id}" data-patient="${rem.patientId}">Resend</button>`;
                    html += `<button class="btn btn-sm btn-secondary" data-action="reminder-write" data-reminder="${rem.id}" data-patient="${rem.patientId}">Write Message</button>`;
                }
                html += `<button class="btn btn-sm btn-secondary" data-action="acknowledge-reminder" data-reminder="${rem.id}">Acknowledge</button>`;
                html += '</div></div>';
            }
            html += '</div>';
            html += `<div class="card-footer"><a data-route="reminders" class="link">View all reminders</a></div>`;
        }
        html += '</div>';

        // Upcoming appointments
        html += '<div class="dashboard-card">';
        html += `<div class="card-header"><h2>Upcoming Appointments</h2></div>`;
        if (upcoming.length === 0) {
            html += '<div class="card-empty">No upcoming appointments</div>';
        } else {
            html += '<div class="appointment-list">';
            for (const appt of upcoming) {
                const patient = AppState.getPatient(appt.patientId);
                const pName = patient ? `${patient.firstName} ${patient.lastName}` : 'Unknown';
                const isVirtual = appt.place === 'virtual';
                html += `<div class="appointment-item" data-testid="appt-${appt.id}">`;
                html += `<div class="appt-date">${Components.formatShortDate(appt.date)}<br><span class="appt-time">${Components.formatTime(appt.date)}</span></div>`;
                html += '<div class="appt-details">';
                html += `<div class="appt-patient">${Components.escapeHtml(pName)}</div>`;
                html += `<div class="appt-reason">${Components.escapeHtml(appt.reason)}</div>`;
                html += `<div class="appt-type ${isVirtual ? 'virtual' : 'in-person'}">${isVirtual ? '&#x1F4F9; Virtual' : '&#x1F3E5; In-person'}</div>`;
                html += '</div>';
                if (isVirtual) {
                    html += `<button class="btn btn-sm btn-primary" data-action="start-video" data-appointment="${appt.id}" data-testid="start-video-${appt.id}">Start Video</button>`;
                }
                html += '</div>';
            }
            html += '</div>';
            html += `<div class="card-footer"><a data-route="appointments" class="link">View all appointments</a></div>`;
        }
        html += '</div>';

        html += '</div></div>';
        return html;
    },

    // ── Inbox (Patient Letters) ─────────────────────────────
    renderInbox() {
        const letters = AppState.getInboxLetters();
        let html = '<div class="page-content" data-testid="inbox-page">';
        html += '<div class="page-header"><h1 class="page-title">Patient Letters</h1>';
        html += '<button class="btn btn-primary" data-action="compose-letter" data-testid="compose-btn">New Letter</button></div>';

        if (letters.length === 0) {
            html += Components.emptyState('&#x1F4E8;', 'No Patient Letters', 'Patient messages will appear here.');
        } else {
            html += '<div class="letter-list full-list">';
            for (const ltr of letters) {
                const patient = AppState.getPatient(ltr.patientId);
                const pName = patient ? `${patient.firstName} ${patient.lastName}` : 'Unknown';
                html += `<div class="letter-item ${!ltr.isRead ? 'unread' : ''}" data-action="open-conversation" data-conversation="${ltr.conversationId}" data-patient="${ltr.patientId}" data-testid="letter-${ltr.id}">`;
                html += `<div class="letter-sender">${Components.escapeHtml(pName)}</div>`;
                html += `<div class="letter-subject">${Components.escapeHtml(ltr.category || ltr.subject)}</div>`;
                html += `<div class="letter-preview">${Components.escapeHtml(ltr.body.substring(0, 120))}</div>`;
                html += `<div class="letter-date">${Components.formatDate(ltr.sentAt)}</div>`;
                html += '</div>';
            }
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    // ── Sent Letters ────────────────────────────────────────
    renderSent() {
        const letters = AppState.getSentLetters();
        let html = '<div class="page-content" data-testid="sent-page">';
        html += '<div class="page-header"><h1 class="page-title">Sent Letters</h1></div>';

        if (letters.length === 0) {
            html += Components.emptyState('&#x1F4E4;', 'No Sent Letters', 'Letters you send will appear here.');
        } else {
            html += '<div class="letter-list full-list">';
            for (const ltr of letters) {
                const patient = AppState.getPatient(ltr.patientId);
                const pName = patient ? `${patient.firstName} ${patient.lastName}` : 'Unknown';
                const stateIcon = ltr.conversationState === 'ended' ? '<span class="conv-ended" title="Conversation ended">&#x1F512;</span>' : '';
                html += `<div class="letter-item" data-action="open-conversation" data-conversation="${ltr.conversationId}" data-patient="${ltr.patientId}" data-testid="sent-${ltr.id}">`;
                html += `<div class="letter-sender">To: ${Components.escapeHtml(pName)}</div>`;
                html += `<div class="letter-subject">${stateIcon} ${Components.escapeHtml(ltr.subject)}</div>`;
                html += `<div class="letter-preview">${Components.escapeHtml(ltr.body.substring(0, 120))}</div>`;
                html += `<div class="letter-date">${Components.formatDate(ltr.sentAt)}</div>`;
                html += '</div>';
            }
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    // ── Drafts ──────────────────────────────────────────────
    renderDrafts() {
        const drafts = AppState.getDraftLetters();
        let html = '<div class="page-content" data-testid="drafts-page">';
        html += '<div class="page-header"><h1 class="page-title">Drafts</h1></div>';

        if (drafts.length === 0) {
            html += Components.emptyState('&#x1F4DD;', 'No Drafts', 'Draft letters will appear here.');
        } else {
            html += '<div class="letter-list full-list">';
            for (const ltr of drafts) {
                const patient = AppState.getPatient(ltr.patientId);
                const pName = patient ? `${patient.firstName} ${patient.lastName}` : 'Unknown';
                html += `<div class="letter-item draft" data-action="edit-draft" data-letter="${ltr.id}" data-testid="draft-${ltr.id}">`;
                html += `<div class="letter-sender">To: ${Components.escapeHtml(pName)}</div>`;
                html += `<div class="letter-subject">${Components.escapeHtml(ltr.subject || '(no subject)')}</div>`;
                html += `<div class="letter-preview">${Components.escapeHtml(ltr.body.substring(0, 120))}</div>`;
                html += `<div class="letter-actions"><button class="btn btn-sm btn-danger" data-action="delete-draft" data-letter="${ltr.id}">Delete</button></div>`;
                html += '</div>';
            }
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    // ── Reminders ───────────────────────────────────────────
    renderReminders() {
        const all = AppState.reminders.sort((a, b) => {
            if (a.acknowledged !== b.acknowledged) return a.acknowledged ? 1 : -1;
            return new Date(b.createdAt) - new Date(a.createdAt);
        });
        let html = '<div class="page-content" data-testid="reminders-page">';
        html += '<div class="page-header"><h1 class="page-title">Reminders</h1></div>';

        if (all.length === 0) {
            html += Components.emptyState('&#x1F514;', 'No Reminders', 'Notifications will appear here.');
        } else {
            html += '<div class="reminder-list full-list">';
            for (const rem of all) {
                const typeLabel = rem.type === 'unread_alert' ? 'Unread Alert' :
                    rem.type === 'appointment_reminder' ? 'Appointment' :
                    rem.type === 'passport_invitation' ? 'Passport' : rem.type;
                html += `<div class="reminder-item ${rem.acknowledged ? 'acknowledged' : ''}" data-testid="reminder-${rem.id}">`;
                html += `<div class="reminder-type-badge type-${rem.type}">${typeLabel}</div>`;
                html += `<div class="reminder-content">`;
                html += `<div class="reminder-text">${Components.escapeHtml(rem.description)}</div>`;
                html += `<div class="reminder-date">${Components.formatDateTime(rem.createdAt)}</div>`;
                html += '</div>';
                html += '<div class="reminder-actions">';
                if (!rem.acknowledged) {
                    if (rem.type === 'unread_alert' && rem.patientLetterId) {
                        html += `<button class="btn btn-sm btn-secondary" data-action="reminder-resend" data-reminder="${rem.id}" data-patient="${rem.patientId}">Resend</button>`;
                        html += `<button class="btn btn-sm btn-secondary" data-action="reminder-write" data-reminder="${rem.id}" data-patient="${rem.patientId}">Write Message</button>`;
                    }
                    if (rem.type === 'passport_invitation') {
                        html += `<button class="btn btn-sm btn-secondary" data-action="open-patient" data-patient="${rem.patientId}">View Patient</button>`;
                    }
                    html += `<button class="btn btn-sm btn-primary" data-action="acknowledge-reminder" data-reminder="${rem.id}">Acknowledge</button>`;
                } else {
                    html += '<span class="acknowledged-label">Acknowledged</span>';
                }
                html += '</div></div>';
            }
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    // ── Conversation Detail ─────────────────────────────────
    renderConversation(conversationId, patientId) {
        const letters = AppState.getConversationLetters(conversationId);
        const patient = AppState.getPatient(patientId);
        if (!patient || letters.length === 0) {
            return '<div class="page-content"><p>Conversation not found.</p></div>';
        }
        const pName = `${patient.firstName} ${patient.lastName}`;
        const lastLetter = letters[letters.length - 1];
        const isEnded = lastLetter.conversationState === 'ended';
        const noReply = lastLetter.doNotAllowResponse;

        // Mark unread from-patient letters as read
        for (const l of letters) {
            if (l.direction === 'from_patient' && !l.isRead) {
                AppState.markLetterRead(l.id);
            }
        }

        let html = '<div class="page-content conversation-page" data-testid="conversation-page">';
        html += `<div class="page-header"><button class="btn btn-secondary" data-action="go-back" data-testid="back-btn">&#x2190; Back</button>`;
        html += `<div class="conv-header-info"><h1 class="page-title">${Components.escapeHtml(letters[0].subject)}</h1>`;
        html += `<span class="conv-patient">with ${Components.escapeHtml(pName)}</span>`;
        if (isEnded) html += '<span class="conv-status ended">Conversation Ended</span>';
        html += '</div></div>';

        html += '<div class="conversation-thread">';
        for (const ltr of letters) {
            const isProvider = ltr.direction === 'to_patient';
            const senderName = isProvider ? AppState.getProviderName(ltr.senderId) : pName;
            const senderColor = isProvider ? '#4A90D9' : '#6B7280';
            html += `<div class="message-card ${isProvider ? 'provider' : 'patient'}" data-testid="message-${ltr.id}">`;
            html += '<div class="message-header">';
            html += Components.avatar(senderName, senderColor, 32);
            html += `<div class="message-meta"><strong>${Components.escapeHtml(senderName)}</strong>`;
            if (ltr.category) html += ` <span class="message-category">${Components.escapeHtml(ltr.category)}</span>`;
            html += `<span class="message-time">${Components.formatDateTime(ltr.sentAt)}</span></div>`;
            html += '</div>';
            html += `<div class="message-body">${Components.escapeHtml(ltr.body).replace(/\n/g, '<br>')}</div>`;
            if (ltr.attachments && ltr.attachments.length > 0) {
                html += '<div class="message-attachments">';
                for (const att of ltr.attachments) {
                    html += Components.attachment(att);
                }
                html += '</div>';
            }
            html += '</div>';
        }
        html += '</div>';

        // Reply area
        if (!isEnded && !noReply) {
            html += `<div class="reply-area" data-testid="reply-area">`;
            html += `<textarea id="replyBody" class="form-textarea" rows="3" placeholder="Type your reply..." data-testid="reply-input"></textarea>`;
            html += '<div class="reply-actions">';
            html += `<button class="btn btn-primary" data-action="send-reply" data-conversation="${conversationId}" data-testid="send-reply-btn">Reply</button>`;
            html += `<button class="btn btn-secondary" data-action="sign-off-conversation" data-conversation="${conversationId}" data-testid="sign-off-btn">Sign Off &amp; End Conversation</button>`;
            html += '</div></div>';
        }

        html += '</div>';
        return html;
    },

    // ── Patient List ────────────────────────────────────────
    renderPatients() {
        const paged = AppState.getPagedPatients();
        const f = AppState.patientListFilter;

        let html = '<div class="page-content" data-testid="patients-page">';
        html += '<div class="page-header"><h1 class="page-title">Patients</h1></div>';

        // Filters
        html += '<div class="filters-bar">';
        html += '<div class="filter-group">';
        html += '<div class="search-box"><input type="text" id="patientSearch" class="form-input search-input" placeholder="Search patients..." value="' + Components.escapeAttr(f.search) + '" data-testid="patient-search"></div>';
        html += '</div>';
        html += '<div class="filter-group">';
        const provOpts = [{ value: 'all', label: 'All Providers' }, ...AppState.providers.map(p => ({ value: p.id, label: `${p.firstName} ${p.lastName}` }))];
        html += Components.dropdown('providerFilter', provOpts, f.providerId, { placeholder: 'All Providers' });
        html += '</div>';
        html += '<div class="filter-group passport-filters">';
        html += '<span class="filter-label">Passport Status:</span>';
        html += Components.checkbox('filter-registered', f.passportStatus.includes('registered'), 'Registered');
        html += Components.checkbox('filter-invited', f.passportStatus.includes('invited'), 'Invited');
        html += Components.checkbox('filter-not_invited', f.passportStatus.includes('not_invited'), 'Not Invited');
        html += '</div>';
        html += '</div>';

        // Patient table
        html += '<div class="patient-table-container">';
        html += '<table class="patient-table" data-testid="patient-table">';
        html += '<thead><tr><th><input type="checkbox" id="selectAllPatients" data-action="select-all-patients"></th><th>Name</th><th>Email</th><th>Phone</th><th>DOB</th><th>Provider</th><th>Passport</th><th>SMS</th><th>Tags</th></tr></thead>';
        html += '<tbody>';
        for (const p of paged.patients) {
            const provName = AppState.getProviderName(p.assignedProviderId);
            const selected = AppState.selectedPatientIds.includes(p.id);
            html += `<tr class="patient-row ${selected ? 'selected' : ''}" data-patient="${p.id}" data-testid="patient-${p.id}">`;
            html += `<td><input type="checkbox" class="patient-checkbox" data-patient-select="${p.id}" ${selected ? 'checked' : ''}></td>`;
            html += `<td><a class="patient-name-link" data-action="open-patient" data-patient="${p.id}">${Components.escapeHtml(p.lastName)}, ${Components.escapeHtml(p.firstName)}</a></td>`;
            html += `<td class="email-cell">${Components.escapeHtml(p.email || '-')}</td>`;
            html += `<td>${Components.escapeHtml(p.cellPhone || '-')}</td>`;
            html += `<td>${Components.formatShortDate(p.dateOfBirth)}</td>`;
            html += `<td>${Components.escapeHtml(provName)}</td>`;
            html += `<td>${Components.passportBadge(p.passportStatus)}</td>`;
            html += `<td>${Components.smsOptInBadge(p.smsOptInStatus)}</td>`;
            html += '<td class="tags-cell">';
            for (const t of (p.tags || []).slice(0, 3)) {
                html += Components.tag(t);
            }
            if (p.tags && p.tags.length > 3) html += `<span class="more-tags">+${p.tags.length - 3}</span>`;
            html += '</td></tr>';
        }
        html += '</tbody></table></div>';

        // Pagination and actions
        html += '<div class="patient-footer">';
        if (AppState.selectedPatientIds.length > 0) {
            html += `<div class="bulk-actions"><span>${AppState.selectedPatientIds.length} selected</span>`;
            html += '<button class="btn btn-primary btn-sm" data-action="bulk-send-letter" data-testid="bulk-send-btn">Send Bulk Letter</button>';
            html += '<button class="btn btn-secondary btn-sm" data-action="bulk-invite-passport" data-testid="bulk-invite-btn">Send Passport Invitation</button>';
            html += '</div>';
        }
        html += Components.pagination(paged.page, paged.totalPages, paged.total);
        html += '</div>';

        html += '</div>';
        return html;
    },

    // ── Patient Detail ──────────────────────────────────────
    renderPatientDetail(patientId) {
        const patient = AppState.getPatient(patientId);
        if (!patient) return '<div class="page-content"><p>Patient not found.</p></div>';

        const provName = AppState.getProviderName(patient.assignedProviderId);
        const letters = AppState.getPatientLetters(patientId);
        const appointments = AppState.getPatientAppointments(patientId);
        const visitSummaries = AppState.getPatientVisitSummaries(patientId);

        let html = '<div class="page-content patient-detail-page" data-testid="patient-detail">';
        html += `<div class="page-header"><button class="btn btn-secondary" data-action="go-back" data-testid="back-btn">&#x2190; Back</button>`;
        html += `<h1 class="page-title">${Components.escapeHtml(patient.firstName)} ${Components.escapeHtml(patient.lastName)}</h1>`;
        html += '<div class="header-actions">';
        html += `<button class="btn btn-primary" data-action="compose-to-patient" data-patient="${patient.id}" data-testid="compose-to-patient">Write Letter</button>`;
        html += `<button class="btn btn-secondary passport-globe-btn" data-action="open-passport-dialog" data-patient="${patient.id}" data-testid="passport-globe-btn" title="Passport Settings">&#x1F310;</button>`;
        html += '</div></div>';

        html += '<div class="patient-detail-grid">';

        // Demographics card
        html += '<div class="detail-card" data-testid="demographics-card">';
        html += '<h2>Demographics</h2>';
        html += '<div class="detail-rows">';
        html += this._detailRow('Email', patient.email || '-');
        html += this._detailRow('Cell Phone', patient.cellPhone || '-');
        html += this._detailRow('Date of Birth', Components.formatFullDate(patient.dateOfBirth));
        html += this._detailRow('Provider', provName);
        if (patient.emergencyContact) {
            html += this._detailRow('Emergency Contact', `${patient.emergencyContact.name} (${patient.emergencyContact.relationship}) - ${patient.emergencyContact.phone}`);
        }
        html += `<button class="btn btn-sm btn-text" data-action="edit-emergency-contact" data-patient="${patient.id}" data-testid="edit-emergency-contact-btn">${patient.emergencyContact ? 'Edit' : '+ Add'} Emergency Contact</button>`;
        html += '</div>';
        html += '<div class="detail-section">';
        html += '<h3>Tags</h3><div class="tags-list">';
        for (const t of patient.tags) {
            html += Components.tag(t, { removable: true, patientId: patient.id });
        }
        html += `<button class="btn btn-sm btn-text" data-action="add-tag" data-patient="${patient.id}" data-testid="add-tag-btn">+ Add Tag</button>`;
        html += '</div></div>';
        html += '<div class="detail-section">';
        html += `<h3>SMS Status</h3>${Components.smsOptInBadge(patient.smsOptInStatus)}`;
        if (patient.smsOptInStatus !== 'opted_in') {
            html += `<button class="btn btn-sm btn-text" data-action="request-sms-optin" data-patient="${patient.id}" data-testid="request-optin-btn">Request Opt-In</button>`;
        } else {
            html += `<button class="btn btn-sm btn-danger" data-action="opt-out-sms" data-patient="${patient.id}" data-testid="opt-out-sms-btn">Opt Out of SMS</button>`;
        }
        html += '</div></div>';

        // Passport card
        html += '<div class="detail-card" data-testid="passport-card">';
        html += '<h2>Patient Passport</h2>';
        html += `<div class="passport-status-large">${Components.passportBadge(patient.passportStatus)}</div>`;
        html += '<div class="detail-rows">';
        html += this._detailRow('Sharing Level', AppState.sharingLevels[patient.passportSharingLevel]?.name || 'Unknown');
        if (patient.invitedAt) html += this._detailRow('Invited', Components.formatFullDate(patient.invitedAt));
        if (patient.registeredAt) html += this._detailRow('Registered', Components.formatFullDate(patient.registeredAt));
        if (patient.invitationCode && patient.passportStatus === 'invited') {
            html += this._detailRow('Invitation Code', `<span class="invitation-code" data-testid="invitation-code">${patient.invitationCode}</span>`);
        }
        if (patient.passportAccountDisabled) html += this._detailRow('Account Status', '<span class="text-danger">Disabled</span>');
        html += '</div>';
        html += '<div class="passport-actions">';
        if (patient.passportStatus === 'not_invited') {
            html += `<button class="btn btn-primary" data-action="send-passport-invite" data-patient="${patient.id}" data-testid="send-invite-btn">Send Invitation</button>`;
        } else if (patient.passportStatus === 'invited') {
            html += `<button class="btn btn-secondary" data-action="resend-passport-invite" data-patient="${patient.id}" data-testid="resend-invite-btn">Re-send Invitation</button>`;
            html += `<button class="btn btn-sm btn-text" data-action="view-invitation-code" data-patient="${patient.id}" data-testid="view-code-btn">View Invitation Code</button>`;
            html += `<button class="btn btn-danger btn-sm" data-action="disable-passport" data-patient="${patient.id}" data-testid="disable-passport-btn">Disable Passport Account</button>`;
        } else if (patient.passportStatus === 'registered' && !patient.passportAccountDisabled) {
            html += `<button class="btn btn-danger btn-sm" data-action="disable-passport" data-patient="${patient.id}" data-testid="disable-passport-btn">Disable Passport Account</button>`;
        }
        html += '</div></div>';

        // Clinical Profile card
        html += '<div class="detail-card wide" data-testid="clinical-profile-card">';
        html += '<h2>Clinical Profile</h2>';
        const cp = patient.clinicalProfile || {};
        html += '<div class="clinical-grid">';
        html += this._clinicalSection('Allergies', cp.allergies);
        html += this._clinicalSection('Drug Intolerances', cp.drugIntolerances);
        html += this._clinicalSection('Medications', cp.medications);
        html += this._clinicalSection('Vaccines', cp.vaccines);
        html += this._clinicalSection('Problem List', cp.problemList);
        html += this._clinicalSection('History', cp.history);
        html += '</div></div>';

        // Letters card
        html += '<div class="detail-card wide" data-testid="letters-card">';
        html += `<h2>Patient Letters</h2>`;
        if (letters.length === 0) {
            html += '<div class="card-empty">No letters</div>';
        } else {
            html += '<div class="letter-list">';
            for (const ltr of letters.slice(0, 10)) {
                const isFrom = ltr.direction === 'from_patient';
                const senderName = isFrom ? `${patient.firstName} ${patient.lastName}` : AppState.getProviderName(ltr.senderId);
                const stateIcon = ltr.conversationState === 'ended' ? '<span class="conv-ended">&#x1F512;</span>' : '';
                const draftLabel = ltr.isDraft ? '<span class="draft-label">DRAFT</span>' : '';
                html += `<div class="letter-item ${!ltr.isRead && isFrom ? 'unread' : ''}" data-action="open-conversation" data-conversation="${ltr.conversationId}" data-patient="${patient.id}" data-testid="pletter-${ltr.id}">`;
                html += `<div class="letter-direction">${isFrom ? '&#x2190; From' : '&#x2192; To'}</div>`;
                html += `<div class="letter-subject">${draftLabel}${stateIcon} ${Components.escapeHtml(ltr.subject)}</div>`;
                html += `<div class="letter-date">${Components.formatDate(ltr.sentAt)}</div>`;
                html += '</div>';
            }
            html += '</div>';
        }
        html += '</div>';

        // Appointments card
        html += '<div class="detail-card" data-testid="appointments-card">';
        html += '<h2>Appointments</h2>';
        if (appointments.length === 0) {
            html += '<div class="card-empty">No appointments</div>';
        } else {
            for (const appt of appointments.slice(0, 5)) {
                const isVirtual = appt.place === 'virtual';
                html += `<div class="appointment-mini" data-testid="patient-appt-${appt.id}">`;
                html += `<span class="appt-mini-date">${Components.formatShortDate(appt.date)} ${Components.formatTime(appt.date)}</span>`;
                html += `<span class="appt-mini-type">${isVirtual ? '&#x1F4F9;' : '&#x1F3E5;'}</span>`;
                html += `<span class="appt-mini-reason">${Components.escapeHtml(appt.reason)}</span>`;
                html += `<span class="appt-mini-status">${appt.status}</span>`;
                html += '</div>';
            }
        }
        html += '</div>';

        // Visit Summaries card
        html += '<div class="detail-card" data-testid="visit-summaries-card">';
        html += '<h2>Visit Summaries</h2>';
        if (visitSummaries.length === 0) {
            html += '<div class="card-empty">No visit summaries</div>';
        } else {
            for (const vs of visitSummaries) {
                html += `<div class="visit-summary-mini" data-action="view-visit-summary" data-summary="${vs.id}" data-testid="vs-${vs.id}">`;
                html += `<span class="vs-date">${Components.formatShortDate(vs.date)}</span>`;
                html += `<span class="vs-category">${Components.escapeHtml(vs.category)}</span>`;
                html += `<span class="vs-provider">${AppState.getProviderName(vs.providerId)}</span>`;
                html += '</div>';
            }
        }
        html += '</div>';

        html += '</div></div>';
        return html;
    },

    _detailRow(label, value) {
        return `<div class="detail-row"><span class="detail-label">${Components.escapeHtml(label)}</span><span class="detail-value">${value}</span></div>`;
    },

    _clinicalSection(title, items) {
        let html = `<div class="clinical-section"><h4>${Components.escapeHtml(title)}</h4>`;
        if (!items || items.length === 0) {
            html += '<div class="clinical-empty">None recorded</div>';
        } else {
            html += '<ul class="clinical-list">';
            for (const item of items) {
                html += `<li>${Components.escapeHtml(item)}</li>`;
            }
            html += '</ul>';
        }
        html += '</div>';
        return html;
    },

    // ── Appointments Page ───────────────────────────────────
    renderAppointments() {
        const upcoming = AppState.getUpcomingAppointments();
        const past = AppState.getPastAppointments().slice(0, 15);

        let html = '<div class="page-content" data-testid="appointments-page">';
        html += '<div class="page-header"><h1 class="page-title">Appointments</h1>';
        html += '<button class="btn btn-primary" data-action="new-appointment" data-testid="new-appt-btn">New Appointment</button></div>';

        html += '<h2 class="section-title">Upcoming</h2>';
        if (upcoming.length === 0) {
            html += '<div class="card-empty">No upcoming appointments</div>';
        } else {
            html += '<div class="appointments-table-container"><table class="appointments-table" data-testid="upcoming-appts">';
            html += '<thead><tr><th>Date</th><th>Time</th><th>Patient</th><th>Provider</th><th>Type</th><th>Reason</th><th>Actions</th></tr></thead><tbody>';
            for (const appt of upcoming) {
                const pName = AppState.getPatientName(appt.patientId);
                const provName = AppState.getProviderName(appt.providerId);
                const isVirtual = appt.place === 'virtual';
                html += `<tr data-testid="appt-row-${appt.id}">`;
                html += `<td>${Components.formatShortDate(appt.date)}</td>`;
                html += `<td>${Components.formatTime(appt.date)}</td>`;
                html += `<td><a class="link" data-action="open-patient" data-patient="${appt.patientId}">${Components.escapeHtml(pName)}</a></td>`;
                html += `<td>${Components.escapeHtml(provName)}</td>`;
                html += `<td class="${isVirtual ? 'virtual' : 'in-person'}">${isVirtual ? '&#x1F4F9; Virtual' : '&#x1F3E5; In-person'}</td>`;
                html += `<td>${Components.escapeHtml(appt.reason)}</td>`;
                html += '<td>';
                if (isVirtual) html += `<button class="btn btn-sm btn-primary" data-action="start-video" data-appointment="${appt.id}">Start Video</button>`;
                html += `<button class="btn btn-sm btn-danger" data-action="cancel-appointment" data-appointment="${appt.id}">Cancel</button>`;
                html += '</td></tr>';
            }
            html += '</tbody></table></div>';
        }

        html += '<h2 class="section-title">Past Appointments</h2>';
        if (past.length === 0) {
            html += '<div class="card-empty">No past appointments</div>';
        } else {
            html += '<div class="appointments-table-container"><table class="appointments-table">';
            html += '<thead><tr><th>Date</th><th>Time</th><th>Patient</th><th>Provider</th><th>Type</th><th>Reason</th><th>Status</th><th>Actions</th></tr></thead><tbody>';
            for (const appt of past) {
                const pName = AppState.getPatientName(appt.patientId);
                const provName = AppState.getProviderName(appt.providerId);
                html += `<tr class="past-appt">`;
                html += `<td>${Components.formatShortDate(appt.date)}</td>`;
                html += `<td>${Components.formatTime(appt.date)}</td>`;
                html += `<td>${Components.escapeHtml(pName)}</td>`;
                html += `<td>${Components.escapeHtml(provName)}</td>`;
                html += `<td>${appt.place === 'virtual' ? '&#x1F4F9; Virtual' : '&#x1F3E5; In-person'}</td>`;
                html += `<td>${Components.escapeHtml(appt.reason)}</td>`;
                html += `<td><span class="status-${appt.status}">${appt.status}</span></td>`;
                html += `<td>${appt.status === 'scheduled' ? `<button class="btn btn-sm btn-danger" data-action="cancel-appointment" data-appointment="${appt.id}">Cancel</button>` : ''}</td>`;
                html += '</tr>';
            }
            html += '</tbody></table></div>';
        }

        html += '</div>';
        return html;
    },

    // ── Bulk Letters Page ───────────────────────────────────
    renderBulkLetters() {
        const bulks = AppState.bulkLetters.sort((a, b) => new Date(b.sentAt) - new Date(a.sentAt));

        let html = '<div class="page-content" data-testid="bulk-letters-page">';
        html += '<div class="page-header"><h1 class="page-title">Bulk Letters</h1>';
        html += '<button class="btn btn-primary" data-action="new-bulk-letter" data-testid="new-bulk-btn">New Bulk Letter</button></div>';

        if (bulks.length === 0) {
            html += Components.emptyState('&#x1F4E7;', 'No Bulk Letters', 'Bulk letters you send will appear here.');
        } else {
            html += '<div class="bulk-letter-list">';
            for (const b of bulks) {
                html += `<div class="bulk-letter-item" data-testid="bulk-${b.id}">`;
                html += `<div class="bulk-header">`;
                html += `<strong>${Components.escapeHtml(b.description)}</strong>`;
                html += `<span class="bulk-date">${Components.formatDateTime(b.sentAt)}</span>`;
                html += '</div>';
                html += `<div class="bulk-subject">Subject: ${Components.escapeHtml(b.subject)}</div>`;
                html += `<div class="bulk-info">Sent to ${b.targetCount} patients by ${AppState.getProviderName(b.sentBy)}</div>`;
                html += `<div class="bulk-body">${Components.escapeHtml(b.body.substring(0, 200))}${b.body.length > 200 ? '...' : ''}</div>`;
                html += '</div>';
            }
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    // ── Settings Page ───────────────────────────────────────
    renderSettings() {
        const tab = AppState.settingsTab;
        let html = '<div class="page-content settings-page" data-testid="settings-page">';
        html += '<h1 class="page-title">Settings</h1>';

        html += '<div class="settings-tabs">';
        html += `<div class="settings-tab ${tab === 'user' ? 'active' : ''}" data-settings-tab="user" data-testid="tab-user">User Settings</div>`;
        html += `<div class="settings-tab ${tab === 'admin' ? 'active' : ''}" data-settings-tab="admin" data-testid="tab-admin">Admin Settings</div>`;
        html += `<div class="settings-tab ${tab === 'routing' ? 'active' : ''}" data-settings-tab="routing" data-testid="tab-routing">Message Routing</div>`;
        html += `<div class="settings-tab ${tab === 'telehealth' ? 'active' : ''}" data-settings-tab="telehealth" data-testid="tab-telehealth">Telehealth</div>`;
        html += `<div class="settings-tab ${tab === 'locations' ? 'active' : ''}" data-settings-tab="locations" data-testid="tab-locations">Practice Locations</div>`;
        html += `<div class="settings-tab ${tab === 'billing' ? 'active' : ''}" data-settings-tab="billing" data-testid="tab-billing">Billing Codes</div>`;
        html += '</div>';

        html += '<div class="settings-content">';
        switch (tab) {
            case 'user': html += this._renderUserSettings(); break;
            case 'admin': html += this._renderAdminSettings(); break;
            case 'routing': html += this._renderRoutingSettings(); break;
            case 'telehealth': html += this._renderTelehealthSettings(); break;
            case 'locations': html += this._renderLocationsSettings(); break;
            case 'billing': html += this._renderBillingSettings(); break;
        }
        html += '</div></div>';
        return html;
    },

    _renderUserSettings() {
        const user = AppState.currentUser;
        const prov = AppState.providers.find(p => p.id === user.id);
        if (!prov) return '<p>Provider not found.</p>';

        const sharingOpts = Object.values(AppState.sharingLevels).map(s => ({
            value: s.level,
            label: `Level ${s.level}: ${s.name}`
        }));
        const notifOpts = AppState.notificationTimeframes.map(n => ({
            value: n.value,
            label: n.label
        }));

        let html = '<div class="settings-section" data-testid="user-settings">';
        html += '<h2>Patient Sharing Defaults</h2>';
        html += Components.infoBox('Changes to sharing defaults only apply to newly invited patients, not existing ones.');
        html += '<div class="setting-group">';
        html += Components.dropdown('sharingDefault', sharingOpts, prov.sharingDefault, { label: 'Clinical Profile Sharing Default' });
        html += '</div>';

        // Show sharing level details
        const currentLevel = AppState.sharingLevels[prov.sharingDefault];
        if (currentLevel) {
            html += `<div class="sharing-detail"><strong>${currentLevel.name}</strong><p>${currentLevel.description}</p></div>`;
        }

        html += '<h2>Notification Preferences</h2>';
        html += '<div class="setting-group">';
        html += Components.dropdown('notificationTimeframe', notifOpts, prov.notificationTimeframe, { label: 'Unread Letter Alert Timeframe' });
        html += Components.infoBox('How long to wait before receiving a notification about unopened Patient Letters.');
        html += '</div>';

        html += '<div class="settings-save-bar">';
        html += '<button class="btn btn-primary" data-action="save-user-settings" data-testid="save-user-settings">Save Changes</button>';
        html += '</div>';
        html += '</div>';
        return html;
    },

    _renderAdminSettings() {
        const ps = AppState.practiceSettings;

        let html = '<div class="settings-section" data-testid="admin-settings">';
        html += '<h2>Patient Passport Messages</h2>';
        html += Components.toggle('allowPatientMessaging', ps.allowPatientMessaging, 'Allow patients to send messages to the practice', 'When enabled, patients can initiate conversations through Passport.');
        html += '<div class="setting-divider"></div>';

        html += '<h2>Booking Site Preferences</h2>';
        html += Components.toggle('bookingSiteAutoInvite', ps.bookingSiteAutoInvite, 'Auto-invite patients to Passport after online booking', 'Automatically send patients an email invitation to join Patient Passport after they book online.');

        if (ps.bookingSiteUrl) {
            html += this._detailRow('Booking Site URL', `<a href="${Components.escapeAttr(ps.bookingSiteUrl)}" class="link">${Components.escapeHtml(ps.bookingSiteUrl)}</a>`);
        }

        html += '<div class="settings-save-bar">';
        html += '<button class="btn btn-primary" data-action="save-admin-settings" data-testid="save-admin-settings">Save Changes</button>';
        html += '</div>';

        html += '<div class="setting-divider"></div>';
        html += '<h2>Provider Notification Settings</h2>';
        html += Components.infoBox('Manage unread letter alert timeframes for all providers in the practice.');
        const notifOpts = AppState.notificationTimeframes.map(n => ({ value: n.value, label: n.label }));
        for (const p of AppState.providers) {
            html += '<div class="provider-notif-row" data-testid="provider-notif-' + p.id + '">';
            html += `<span class="provider-notif-name"><strong>${Components.escapeHtml(p.firstName)} ${Components.escapeHtml(p.lastName)}</strong> <span class="provider-role-label">(${AppState.formatRole(p.role)})</span></span>`;
            html += Components.dropdown('providerNotif_' + p.id, notifOpts, p.notificationTimeframe, { label: 'Alert Timeframe' });
            html += '</div>';
        }
        html += '<div class="settings-save-bar">';
        html += '<button class="btn btn-primary" data-action="save-provider-notifications" data-testid="save-provider-notifications">Save Notification Settings</button>';
        html += '</div>';

        html += '</div>';
        return html;
    },

    _renderRoutingSettings() {
        const ps = AppState.practiceSettings;
        const cats = AppState.messageCategories;
        const routing = AppState.messageRouting;

        let html = '<div class="settings-section" data-testid="routing-settings">';
        html += '<h2>Message Routing</h2>';

        if (!ps.allowPatientMessaging) {
            html += Components.warningBox('Patient messaging is currently disabled. Enable it in Admin Settings to configure routing.');
            html += '</div>';
            return html;
        }

        html += Components.infoBox('Configure where patient messages are routed based on the message category.');

        // Provider selector
        html += '<div class="routing-provider-select">';
        const provOpts = AppState.providers.map(p => ({ value: p.id, label: `${p.firstName} ${p.lastName} (${AppState.formatRole(p.role)})` }));
        html += Components.dropdown('routingProvider', provOpts, AppState._routingSelectedProvider || AppState.currentUser.id, { label: 'Configure routing for' });
        html += `<button class="btn btn-secondary btn-sm" data-action="update-all-routing" data-testid="update-all-routing">Update Routing for All Providers</button>`;
        html += '</div>';

        const selectedProvId = AppState._routingSelectedProvider || AppState.currentUser.id;
        const provRouting = routing[selectedProvId] || {};

        html += '<table class="routing-table" data-testid="routing-table">';
        html += '<thead><tr><th>Message Category</th><th>Route To</th><th>Actions</th></tr></thead><tbody>';
        for (const cat of cats) {
            const recipients = provRouting[cat] || [];
            html += `<tr data-category="${Components.escapeAttr(cat)}">`;
            html += `<td>${Components.escapeHtml(cat)}</td>`;
            html += '<td class="routing-recipients">';
            for (const r of recipients) {
                const isGroup = r.startsWith('ug_');
                const name = isGroup
                    ? (AppState.userGroups.find(g => g.id === r)?.name || r)
                    : AppState.getProviderName(r);
                html += `<span class="routing-recipient ${isGroup ? 'group' : 'provider'}" data-recipient="${r}" data-category="${Components.escapeAttr(cat)}">${Components.escapeHtml(name)}<span class="remove-recipient" data-action="remove-routing-recipient" data-provider="${selectedProvId}" data-category="${Components.escapeAttr(cat)}" data-recipient="${r}">&times;</span></span>`;
            }
            html += '</td>';
            html += `<td><button class="btn btn-sm btn-text" data-action="add-routing-recipient" data-provider="${selectedProvId}" data-category="${Components.escapeAttr(cat)}" data-testid="add-route-${cat.replace(/\s+/g, '-').toLowerCase()}">+ Add</button></td>`;
            html += '</tr>';
        }
        html += '</tbody></table>';
        html += '</div>';
        return html;
    },

    _renderTelehealthSettings() {
        const user = AppState.currentUser;
        const prov = AppState.providers.find(p => p.id === user.id);
        const vs = AppState.practiceSettings.videoSettings;

        let html = '<div class="settings-section" data-testid="telehealth-settings">';
        html += '<h2>Virtual Visit Settings</h2>';

        // Per-provider activation
        html += '<div class="telehealth-provider-settings">';
        for (const p of AppState.providers) {
            html += `<div class="telehealth-provider-card" data-testid="telehealth-${p.id}">`;
            html += `<div class="telehealth-provider-header"><strong>${Components.escapeHtml(p.firstName)} ${Components.escapeHtml(p.lastName)}</strong> <span class="provider-role-label">(${AppState.formatRole(p.role)})</span>`;
            html += `<span class="telehealth-status ${p.virtualVisitActivated ? 'active' : 'inactive'}">${p.virtualVisitActivated ? 'Activated' : 'Not Activated'}</span>`;
            html += '</div>';
            if (p.virtualVisitActivated) {
                html += `<div class="telehealth-instructions">${Components.escapeHtml(p.virtualVisitInstructions || 'No instructions configured')}</div>`;
                html += '<div class="telehealth-actions">';
                html += `<button class="btn btn-sm btn-secondary" data-action="edit-telehealth-instructions" data-provider="${p.id}" data-testid="edit-instructions-${p.id}">Edit Instructions</button>`;
                html += `<button class="btn btn-sm btn-danger" data-action="deactivate-telehealth" data-provider="${p.id}" data-testid="deactivate-${p.id}">Deactivate</button>`;
                html += '</div>';
            } else {
                html += `<button class="btn btn-sm btn-primary" data-action="activate-telehealth" data-provider="${p.id}" data-testid="activate-${p.id}">Activate</button>`;
            }
            html += '</div>';
        }
        html += '</div>';

        html += '<div class="setting-divider"></div>';
        html += '<h2>Video Session Settings</h2>';
        html += Components.toggle('screenSharingPatients', vs.screenSharingPatients, 'Allow patient screen sharing', 'Patients can share their screen during virtual visits.');
        html += '<div class="setting-group">';
        html += Components.dropdown('chatMode', [
            { value: 'everyone_in_meeting', label: 'Everyone in Meeting' },
            { value: 'everyone_in_waiting_room', label: 'Everyone in Waiting Room' },
            { value: 'host_only', label: 'Host Only' }
        ], vs.chatMode, { label: 'Chat Mode' });
        html += '</div>';
        html += Components.toggle('waitingRoomAudioNotification', vs.waitingRoomAudioNotification, 'Waiting room audio notification', 'Play a sound when a patient arrives in the waiting room.');

        html += '<div class="settings-save-bar">';
        html += '<button class="btn btn-primary" data-action="save-telehealth-settings" data-testid="save-telehealth">Save Changes</button>';
        html += '</div>';
        html += '</div>';
        return html;
    },

    _renderLocationsSettings() {
        const locs = AppState.practiceSettings.practiceLocations;

        let html = '<div class="settings-section" data-testid="locations-settings">';
        html += '<h2>Practice Locations</h2>';
        html += '<button class="btn btn-primary btn-sm" data-action="add-location" data-testid="add-location-btn">+ Add Practice Location</button>';

        html += '<table class="locations-table" data-testid="locations-table">';
        html += '<thead><tr><th>Name</th><th>Address</th><th>POS Code</th><th>POS Description</th><th>Actions</th></tr></thead><tbody>';
        for (const loc of locs) {
            html += `<tr data-testid="loc-${loc.id}">`;
            html += `<td>${Components.escapeHtml(loc.name)}</td>`;
            html += `<td>${Components.escapeHtml(loc.address)}</td>`;
            html += `<td>${Components.escapeHtml(loc.posCode)}</td>`;
            html += `<td>${Components.escapeHtml(loc.posDescription)}</td>`;
            html += `<td><button class="btn btn-sm btn-secondary" data-action="edit-location" data-location="${loc.id}">Edit</button> <button class="btn btn-sm btn-danger" data-action="remove-location" data-location="${loc.id}">Remove</button></td>`;
            html += '</tr>';
        }
        html += '</tbody></table>';
        html += '</div>';
        return html;
    },

    _renderBillingSettings() {
        const codes = AppState.practiceSettings.cptCodes;

        let html = '<div class="settings-section" data-testid="billing-settings">';
        html += '<h2>CPT Codes</h2>';
        html += '<button class="btn btn-primary btn-sm" data-action="add-cpt-code" data-testid="add-cpt-btn">+ Add CPT Code</button>';
        html += Components.infoBox('CPT codes must match exactly between Elation and your Practice Management System.');

        html += '<table class="cpt-table" data-testid="cpt-table">';
        html += '<thead><tr><th>Code</th><th>Description</th><th>Actions</th></tr></thead><tbody>';
        for (const c of codes) {
            html += `<tr data-testid="cpt-${c.code}">`;
            html += `<td><code>${Components.escapeHtml(c.code)}</code></td>`;
            html += `<td>${Components.escapeHtml(c.description)}</td>`;
            html += `<td><button class="btn btn-sm btn-danger" data-action="remove-cpt" data-code="${c.code}">Remove</button></td>`;
            html += '</tr>';
        }
        html += '</tbody></table>';
        html += '</div>';
        return html;
    },

    // ── Compose Letter Modal ────────────────────────────────
    renderComposeModal(patientId, opts) {
        const patient = patientId ? AppState.getPatient(patientId) : null;
        const isReply = opts?.conversationId;
        const isDraft = opts?.draft;

        let html = '<div class="compose-form" data-testid="compose-form">';
        html += '<div class="compose-header">';
        html += `<h2>${isDraft ? 'Edit Draft' : isReply ? 'Reply' : 'New Letter to Patient'}</h2>`;
        html += '<button class="btn btn-icon" data-action="close-compose">&times;</button>';
        html += '</div>';

        if (!patient) {
            html += '<div class="compose-field">';
            html += Components.textInput('composeTo', '', { label: 'To (Patient)', placeholder: 'Search patient name...', required: true });
            html += '<div id="patientSuggestions" class="suggestions-dropdown"></div>';
            html += '</div>';
        } else {
            html += `<div class="compose-field"><label class="form-label">To</label><div class="compose-to-display">${Components.escapeHtml(patient.firstName)} ${Components.escapeHtml(patient.lastName)} (${Components.escapeHtml(patient.email || 'no email')})</div>`;
            html += `<input type="hidden" id="composePatientId" value="${patient.id}"></div>`;
        }

        html += '<div class="compose-field">';
        html += Components.textInput('composeSubject', opts?.subject || '', { label: 'Subject', placeholder: 'Enter subject...', required: true });
        html += '</div>';

        html += '<div class="compose-field">';
        html += Components.textArea('composeBody', opts?.body || '', { label: 'Message Body', placeholder: 'Type your message...', rows: 8, required: true });
        html += '</div>';

        // Options
        html += '<div class="compose-options">';
        html += '<div class="compose-option-group">';
        html += Components.dropdown('composeUnreadAlert', AppState.notificationTimeframes.map(n => ({ value: n.value, label: n.label })), opts?.unreadAlertTimeframe || 'none', { label: 'Unread Alert' });
        html += '</div>';
        html += '<div class="compose-option-group">';
        html += Components.checkbox('composeNoReply', opts?.doNotAllowResponse || false, 'Do not allow patient to respond');
        html += '</div>';
        html += '</div>';

        html += '<div class="compose-actions">';
        if (isDraft) {
            html += `<button class="btn btn-primary" data-action="send-draft" data-letter="${opts.letterId}" data-testid="send-draft-btn">Sign &amp; Send</button>`;
            html += `<button class="btn btn-secondary" data-action="update-draft" data-letter="${opts.letterId}" data-testid="update-draft-btn">Save Draft</button>`;
        } else {
            html += '<button class="btn btn-primary" data-action="send-composed-letter" data-testid="send-letter-btn">Sign &amp; Send</button>';
            html += '<button class="btn btn-secondary" data-action="save-as-draft" data-testid="save-draft-btn">Save as Draft</button>';
        }
        html += '<button class="btn btn-text" data-action="close-compose">Discard</button>';
        html += '</div>';
        html += '</div>';
        return html;
    },

    // ── Passport Dialog ─────────────────────────────────────
    renderPassportDialog(patientId) {
        const patient = AppState.getPatient(patientId);
        if (!patient) return '';

        const isRegistered = patient.passportStatus === 'registered';
        const isInvited = patient.passportStatus === 'invited';
        const isNotInvited = patient.passportStatus === 'not_invited';

        const sharingOpts = Object.values(AppState.sharingLevels).map(s => ({
            value: s.level,
            label: `Level ${s.level}: ${s.name}`
        }));

        let html = '<div class="passport-dialog" data-testid="passport-dialog">';
        html += `<h3>Passport Settings for ${Components.escapeHtml(patient.firstName)} ${Components.escapeHtml(patient.lastName)}</h3>`;
        html += `<div class="passport-status-row">${Components.passportBadge(patient.passportStatus)}</div>`;

        if (isInvited && patient.invitationCode) {
            html += `<div class="passport-code-section"><strong>Invitation Code:</strong> <span class="invitation-code" data-testid="modal-invitation-code">${patient.invitationCode}</span></div>`;
        }

        html += '<div class="passport-form">';
        html += Components.textInput('passportEmail', patient.email || '', { label: 'Email Address', placeholder: 'patient@email.com', required: true });
        html += Components.textInput('passportPhone', patient.cellPhone || '', { label: 'US Mobile Phone', placeholder: '(555) 555-0000' });

        html += '<div class="passport-sharing">';
        html += '<h4>Passport Sharing Options</h4>';
        html += Components.dropdown('passportSharingLevel', sharingOpts, patient.passportSharingLevel, { label: 'Clinical Profile Sharing Level' });
        const currentLevel = AppState.sharingLevels[patient.passportSharingLevel];
        if (currentLevel) {
            html += `<div class="sharing-detail-small">${Components.escapeHtml(currentLevel.description)}</div>`;
        }
        html += '</div>';

        html += '<div class="passport-dialog-actions">';
        if (isNotInvited || isInvited) {
            html += `<button class="btn btn-primary" data-action="confirm-send-invite" data-patient="${patient.id}" data-testid="confirm-invite-btn">${isInvited ? 'Re-send Invitation & Close' : 'Send Invitation & Close'}</button>`;
        }
        if (isRegistered) {
            html += `<button class="btn btn-primary" data-action="confirm-save-passport" data-patient="${patient.id}" data-testid="save-passport-btn">Save Settings Changes &amp; Close</button>`;
            html += `<button class="btn btn-danger btn-sm" data-action="disable-passport" data-patient="${patient.id}" data-testid="disable-passport-modal-btn">Disable Patient Passport</button>`;
        }
        html += '<button class="btn btn-secondary" data-action="close-modal">Cancel</button>';
        html += '</div></div></div>';
        return html;
    },

    // ── Bulk Letter Compose ─────────────────────────────────
    renderBulkComposeModal() {
        const selected = AppState.selectedPatientIds;
        let html = '<div class="bulk-compose-form" data-testid="bulk-compose-form">';
        html += '<h2>Send Bulk Letter</h2>';
        html += `<div class="bulk-target-info">Sending to ${selected.length} selected patient(s)</div>`;

        html += Components.textInput('bulkDescription', '', { label: 'Short Description (internal only)', placeholder: 'e.g., Annual flu reminder', required: true });
        html += Components.textInput('bulkSubject', '', { label: 'Subject', placeholder: 'Enter subject...', required: true });
        html += Components.textArea('bulkBody', '', { label: 'Letter Body', placeholder: 'Type your message...', rows: 8, required: true });

        html += '<div class="bulk-options">';
        html += Components.checkbox('bulkAllowResponse', false, 'Allow patients to respond');
        html += '</div>';

        html += '<div class="bulk-compose-actions">';
        html += '<button class="btn btn-primary" data-action="confirm-send-bulk" data-testid="confirm-bulk-btn">Send Bulk Letter</button>';
        html += '<button class="btn btn-secondary" data-action="close-modal">Cancel</button>';
        html += '</div>';
        html += '</div>';
        return html;
    },

    // ── Emergency Contact Modal ────────────────────────────
    renderEmergencyContactModal(patientId) {
        const patient = AppState.getPatient(patientId);
        const ec = patient?.emergencyContact || {};
        let html = '<div class="emergency-contact-form" data-testid="emergency-contact-form">';
        html += `<div class="form-group"><label class="form-label">Name</label><input type="text" id="ec-name" class="form-input" value="${Components.escapeAttr(ec.name || '')}" data-testid="ec-name"></div>`;
        html += `<div class="form-group"><label class="form-label">Phone</label><input type="text" id="ec-phone" class="form-input" value="${Components.escapeAttr(ec.phone || '')}" data-testid="ec-phone"></div>`;
        html += `<div class="form-group"><label class="form-label">Relationship</label><input type="text" id="ec-relationship" class="form-input" value="${Components.escapeAttr(ec.relationship || '')}" data-testid="ec-relationship"></div>`;
        html += `<button class="btn btn-primary" data-action="save-emergency-contact" data-patient="${patientId}" data-testid="save-ec-btn">Save</button>`;
        html += '</div>';
        return html;
    },

    // ── New Appointment Modal ───────────────────────────────
    renderNewAppointmentModal() {
        const provOpts = AppState.providers.map(p => ({ value: p.id, label: `${p.firstName} ${p.lastName}` }));
        const placeOpts = [{ value: 'in_person', label: 'In-person' }, { value: 'virtual', label: 'Virtual' }];

        let html = '<div class="appointment-form" data-testid="appointment-form">';
        html += '<h2>New Appointment</h2>';
        html += Components.textInput('apptPatientSearch', '', { label: 'Patient', placeholder: 'Search patient name...' });
        html += '<div id="apptPatientSuggestions" class="suggestions-dropdown"></div>';
        html += `<input type="hidden" id="apptPatientId" value="">`;
        html += Components.textInput('apptDate', '', { label: 'Date', placeholder: 'YYYY-MM-DD', required: true });
        html += Components.textInput('apptTime', '', { label: 'Time', placeholder: 'HH:MM', required: true });
        html += Components.dropdown('apptProvider', provOpts, AppState.currentUser.id, { label: 'Provider' });
        html += Components.dropdown('apptPlace', placeOpts, 'in_person', { label: 'Visit Type' });
        html += Components.textInput('apptReason', '', { label: 'Reason', placeholder: 'Reason for visit...' });

        html += '<div class="appointment-form-actions">';
        html += '<button class="btn btn-primary" data-action="confirm-new-appointment" data-testid="confirm-appt-btn">Schedule Appointment</button>';
        html += '<button class="btn btn-secondary" data-action="close-modal">Cancel</button>';
        html += '</div>';
        html += '</div>';
        return html;
    },

    // ── Visit Summary Detail ────────────────────────────────
    renderVisitSummary(summaryId) {
        const vs = AppState.visitSummaries.find(v => v.id === summaryId);
        if (!vs) return '<p>Visit summary not found.</p>';

        const patient = AppState.getPatient(vs.patientId);
        const pName = patient ? `${patient.firstName} ${patient.lastName}` : 'Unknown';

        let html = '<div class="visit-summary-detail" data-testid="visit-summary-detail">';
        html += `<h2>Visit Summary - ${Components.formatFullDate(vs.date)}</h2>`;
        html += `<p><strong>Patient:</strong> ${Components.escapeHtml(pName)} | <strong>Provider:</strong> ${AppState.getProviderName(vs.providerId)} | <strong>Category:</strong> ${Components.escapeHtml(vs.category)}</p>`;

        if (vs.vitals) {
            html += '<div class="vs-section"><h3>Vitals</h3><div class="vitals-grid">';
            if (vs.vitals.bp) html += `<div class="vital-item"><span class="vital-label">BP</span><span class="vital-value">${vs.vitals.bp}</span></div>`;
            if (vs.vitals.hr) html += `<div class="vital-item"><span class="vital-label">HR</span><span class="vital-value">${vs.vitals.hr} bpm</span></div>`;
            if (vs.vitals.temp) html += `<div class="vital-item"><span class="vital-label">Temp</span><span class="vital-value">${vs.vitals.temp}</span></div>`;
            if (vs.vitals.weight) html += `<div class="vital-item"><span class="vital-label">Weight</span><span class="vital-value">${vs.vitals.weight}</span></div>`;
            if (vs.vitals.bmi) html += `<div class="vital-item"><span class="vital-label">BMI</span><span class="vital-value">${vs.vitals.bmi}</span></div>`;
            html += '</div></div>';
        }
        if (vs.procedures && vs.procedures.length) {
            html += '<div class="vs-section"><h3>Procedures</h3><ul>';
            for (const p of vs.procedures) html += `<li>${Components.escapeHtml(p)}</li>`;
            html += '</ul></div>';
        }
        if (vs.treatments && vs.treatments.length) {
            html += '<div class="vs-section"><h3>Treatments</h3><ul>';
            for (const t of vs.treatments) html += `<li>${Components.escapeHtml(t)}</li>`;
            html += '</ul></div>';
        }
        if (vs.carePlan) {
            html += `<div class="vs-section"><h3>Care Plan</h3><p>${Components.escapeHtml(vs.carePlan)}</p></div>`;
        }
        if (vs.followUp) {
            html += `<div class="vs-section"><h3>Follow-up</h3><p>${Components.escapeHtml(vs.followUp)}</p></div>`;
        }
        html += '</div>';
        return html;
    },

    // ── Add Routing Recipient Modal ─────────────────────────
    renderAddRoutingRecipientModal(providerId, category) {
        const allRecipients = [
            ...AppState.providers.map(p => ({ id: p.id, name: `${p.firstName} ${p.lastName}`, type: 'provider' })),
            ...AppState.userGroups.map(g => ({ id: g.id, name: g.name, type: 'group' }))
        ];
        const currentRouting = (AppState.messageRouting[providerId] || {})[category] || [];

        let html = '<div class="routing-recipient-form" data-testid="routing-recipient-form">';
        html += `<h3>Add Recipients for "${Components.escapeHtml(category)}"</h3>`;
        html += '<div class="recipient-list">';
        for (const r of allRecipients) {
            const isAdded = currentRouting.includes(r.id);
            html += `<div class="recipient-option ${isAdded ? 'added' : ''}">`;
            html += `<span class="recipient-name">${Components.escapeHtml(r.name)}</span>`;
            html += `<span class="recipient-type">${r.type}</span>`;
            if (isAdded) {
                html += '<span class="recipient-added">Added</span>';
            } else {
                html += `<button class="btn btn-sm btn-primary" data-action="confirm-add-routing" data-provider="${providerId}" data-category="${Components.escapeAttr(category)}" data-recipient="${r.id}">Add</button>`;
            }
            html += '</div>';
        }
        html += '</div>';
        html += '<button class="btn btn-secondary" data-action="close-modal">Close</button>';
        html += '</div>';
        return html;
    },

    // ── Add Tag Modal ───────────────────────────────────────
    renderAddTagModal(patientId) {
        const patient = AppState.getPatient(patientId);
        if (!patient) return '';
        const available = AppState.patientTags.filter(t => !patient.tags.includes(t));

        let html = '<div class="add-tag-form" data-testid="add-tag-form">';
        html += '<h3>Add Tag</h3>';
        html += '<div class="tag-options">';
        for (const t of available) {
            html += `<button class="btn btn-sm btn-secondary tag-option" data-action="confirm-add-tag" data-patient="${patientId}" data-tag="${Components.escapeAttr(t)}">${Components.escapeHtml(t)}</button>`;
        }
        if (available.length === 0) {
            html += '<p>All tags have been assigned.</p>';
        }
        html += '</div>';
        html += '<button class="btn btn-secondary" data-action="close-modal">Close</button>';
        html += '</div>';
        return html;
    },

    // ── Location Edit Modal ─────────────────────────────────
    renderLocationModal(location) {
        const isEdit = !!location;
        const loc = location || { name: '', address: '', posCode: '', posDescription: '' };

        let html = '<div class="location-form" data-testid="location-form">';
        html += `<h2>${isEdit ? 'Edit' : 'Add'} Practice Location</h2>`;
        html += Components.textInput('locName', loc.name, { label: 'Location Name', required: true, placeholder: 'e.g., Main Office' });
        html += Components.textInput('locAddress', loc.address, { label: 'Address', required: true, placeholder: 'Full address' });
        html += Components.textInput('locPosCode', loc.posCode, { label: 'Place of Service (POS) Code', required: true, placeholder: 'e.g., 11' });
        html += Components.textInput('locPosDesc', loc.posDescription, { label: 'POS Description', placeholder: 'e.g., Office' });

        html += '<div class="location-form-actions">';
        html += `<button class="btn btn-primary" data-action="${isEdit ? 'confirm-edit-location' : 'confirm-add-location'}" ${isEdit ? `data-location="${loc.id}"` : ''} data-testid="save-location-btn">Save</button>`;
        html += '<button class="btn btn-secondary" data-action="close-modal">Cancel</button>';
        html += '</div></div>';
        return html;
    },

    // ── CPT Code Add Modal ──────────────────────────────────
    renderCptCodeModal() {
        let html = '<div class="cpt-form" data-testid="cpt-form">';
        html += '<h2>Add CPT Code</h2>';
        html += Components.textInput('cptCode', '', { label: 'CPT Code', required: true, placeholder: 'e.g., 99213' });
        html += Components.textInput('cptDescription', '', { label: 'Description', required: true, placeholder: 'e.g., Office visit, established patient' });
        html += '<div class="cpt-form-actions">';
        html += '<button class="btn btn-primary" data-action="confirm-add-cpt" data-testid="save-cpt-btn">Add Code</button>';
        html += '<button class="btn btn-secondary" data-action="close-modal">Cancel</button>';
        html += '</div></div>';
        return html;
    },

    // ── Telehealth Instructions Edit Modal ──────────────────
    renderTelehealthInstructionsModal(providerId) {
        const prov = AppState.providers.find(p => p.id === providerId);
        if (!prov) return '';

        let html = '<div class="telehealth-edit-form" data-testid="telehealth-edit-form">';
        html += `<h2>Edit Virtual Visit Instructions for ${Components.escapeHtml(prov.firstName)} ${Components.escapeHtml(prov.lastName)}</h2>`;
        html += Components.textArea('telehealthInstructions', prov.virtualVisitInstructions, { label: 'Virtual Visit Instructions', rows: 6, placeholder: 'Enter instructions for patients joining virtual visits...' });
        html += '<div class="telehealth-edit-actions">';
        html += `<button class="btn btn-primary" data-action="confirm-edit-instructions" data-provider="${providerId}" data-testid="save-instructions-btn">Save Instructions</button>`;
        html += '<button class="btn btn-secondary" data-action="close-modal">Cancel</button>';
        html += '</div></div>';
        return html;
    }
};
