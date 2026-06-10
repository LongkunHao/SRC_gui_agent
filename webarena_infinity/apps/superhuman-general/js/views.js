// ============================================================
// views.js — View renderers for Superhuman Mail
// ============================================================

const Views = {

    // ---- Sidebar ----
    renderSidebar() {
        const inboxCount = AppState.getUnreadCount('inbox');
        const spamCount = AppState.getSpamEmails().length;
        const draftCount = AppState.getDraftEmails().length;
        const reminderCount = AppState.getReminderEmails().length;

        const folders = [
            { id: 'inbox', icon: '&#9993;', label: 'Inbox', count: inboxCount },
            { id: 'starred', icon: '&#9733;', label: 'Starred', count: 0 },
            { id: 'done', icon: '&#10003;', label: 'Done', count: 0 },
            { id: 'reminders', icon: '&#9200;', label: 'Reminders', count: reminderCount },
            { id: 'sent', icon: '&#10148;', label: 'Sent', count: 0 },
            { id: 'drafts', icon: '&#9998;', label: 'Drafts', count: draftCount },
            { id: 'opens', icon: '&#128065;', label: 'Recent Opens', count: 0 },
            { id: 'snippets', icon: '&#128196;', label: 'Snippets', count: 0 },
            { id: 'spam', icon: '&#9888;', label: 'Spam', count: spamCount },
            { id: 'trash', icon: '&#128465;', label: 'Trash', count: 0 }
        ];

        const userLabels = AppState.labels.filter(l => l.type === 'user');

        return `<div class="sidebar-folders">
            ${folders.map(f => `<a class="sidebar-item${AppState.currentView === f.id ? ' active' : ''}" data-action="navigate" data-route="${f.id}" data-testid="sidebar-${f.id}">
                <span class="sidebar-icon">${f.icon}</span>
                <span class="sidebar-label">${f.label}</span>
                ${f.count > 0 ? Components.badge(f.count) : ''}
            </a>`).join('')}
        </div>
        <div class="sidebar-section">
            <div class="sidebar-section-header">
                <span>Labels</span>
                <button class="sidebar-add-btn" data-action="create-label" data-testid="create-label-btn" title="Create label">+</button>
            </div>
            ${userLabels.map(l => `<a class="sidebar-item${AppState.currentView === 'label' && AppState.currentLabelId === l.id ? ' active' : ''}" data-action="navigate" data-route="label/${l.id}" data-testid="sidebar-label-${l.id}">
                <span class="label-dot" style="background:${l.color}"></span>
                <span class="sidebar-label">${Components.escapeHtml(l.name)}</span>
            </a>`).join('')}
        </div>`;
    },

    // ---- Split Tabs ----
    renderSplitTabs() {
        if (AppState.currentView !== 'inbox') return '';
        const activeSplits = AppState.splits.filter(s => {
            if (s.isDefault) return true;
            return true; // show all splits
        }).sort((a, b) => a.position - b.position);

        return `<div class="split-tabs" data-testid="split-tabs">
            ${activeSplits.map(s => {
                const count = AppState.getSplitUnreadCount(s.id);
                return `<button class="split-tab${AppState.currentSplit === s.id ? ' active' : ''}" data-action="switch-split" data-split-id="${s.id}" data-testid="split-${s.id}">
                    ${Components.escapeHtml(s.name)}${count > 0 ? ` <span class="split-count">${count}</span>` : ''}
                </button>`;
            }).join('')}
        </div>`;
    },

    // ---- Toolbar ----
    renderToolbar() {
        const hasSelection = AppState.selectedEmailIds.size > 0;
        const view = AppState.currentView;

        let leftContent = '';
        let rightContent = '';

        if (hasSelection) {
            const count = AppState.selectedEmailIds.size;
            leftContent = `<span class="toolbar-selection-count">${count} selected</span>
                <button class="toolbar-btn" data-action="mark-done-selected" data-testid="toolbar-done" title="Mark Done (E)">&#10003; Done</button>
                <button class="toolbar-btn" data-action="remind-selected" data-testid="toolbar-remind" title="Remind Me (H)">&#9200; Remind</button>
                <button class="toolbar-btn" data-action="trash-selected" data-testid="toolbar-trash" title="Trash">&#128465; Trash</button>
                <button class="toolbar-btn" data-action="star-selected" data-testid="toolbar-star" title="Star">&#9733; Star</button>
                <button class="toolbar-btn" data-action="label-selected" data-testid="toolbar-label" title="Label">&#127991; Label</button>
                <button class="toolbar-btn" data-action="mark-read-selected" data-testid="toolbar-mark-read" title="Mark Read">Mark Read</button>
                <button class="toolbar-btn" data-action="mark-unread-selected" data-testid="toolbar-mark-unread" title="Mark Unread">Mark Unread</button>`;
        } else {
            leftContent = this.renderSplitTabs();
        }

        // Pagination
        const emails = this._getEmailsForView();
        if (emails.length > 0) {
            const paged = AppState.getPagedEmails(emails);
            rightContent = `<span class="toolbar-paging">${paged.start}-${paged.end} of ${paged.total}</span>
                <button class="toolbar-btn toolbar-paging-btn" data-action="prev-page" ${!paged.hasPrev ? 'disabled' : ''} data-testid="prev-page">&lsaquo;</button>
                <button class="toolbar-btn toolbar-paging-btn" data-action="next-page" ${!paged.hasNext ? 'disabled' : ''} data-testid="next-page">&rsaquo;</button>`;
        }

        return `<div class="toolbar-left">${leftContent}</div>
                <div class="toolbar-right">${rightContent}</div>`;
    },

    _getEmailsForView() {
        switch (AppState.currentView) {
            case 'inbox': return AppState.getInboxEmailsBySplit(AppState.currentSplit);
            case 'done': return AppState.getDoneEmails();
            case 'reminders': return AppState.getReminderEmails();
            case 'sent': return AppState.getSentEmails();
            case 'drafts': return AppState.getDraftEmails();
            case 'starred': return AppState.getStarredEmails();
            case 'spam': return AppState.getSpamEmails();
            case 'trash': return AppState.getTrashEmails();
            case 'search': return AppState.searchResults || [];
            case 'label': return AppState.getEmailsByLabel(AppState.currentLabelId);
            default: return [];
        }
    },

    // ---- Email List ----
    renderEmailList() {
        if (AppState.currentView === 'opens') return this.renderRecentOpens();
        if (AppState.currentView === 'snippets') return this.renderSnippetsList();

        const emails = AppState.searchResults !== null ? AppState.searchResults : this._getEmailsForView();
        const sorted = [...emails].sort((a, b) => new Date(b.date) - new Date(a.date));
        const paged = AppState.getPagedEmails(sorted);

        if (paged.items.length === 0) {
            return this._renderEmptyState();
        }

        return `<div class="email-list" data-testid="email-list">
            ${paged.items.map(email => this.renderEmailItem(email)).join('')}
        </div>`;
    },

    renderEmailItem(email) {
        const isSelected = AppState.selectedEmailIds.has(email.id);
        const isSent = email.from.email === AppState.currentUser.email;
        const displayName = isSent ? `To: ${email.to.map(t => t.name || t.email).join(', ')}` : email.from.name;
        const labels = (email.labels || []).map(lId => AppState.labels.find(l => l.id === lId)).filter(Boolean);

        let dotType = null;
        if (!email.isRead) dotType = 'unread';
        else if (email.remindAt) dotType = 'reminder';
        else if (email.isStarred) dotType = 'starred';

        const contact = !isSent ? AppState.contacts.find(c => c.email === email.from.email) : null;
        const avatarColor = contact ? contact.avatarColor : (isSent ? AppState.currentUser.avatarColor : '#999');

        return `<div class="email-item${isSelected ? ' selected' : ''}${!email.isRead ? ' unread' : ''}" data-email-id="${email.id}" data-testid="email-${email.id}">
            <div class="email-checkbox" data-action="toggle-select" data-email-id="${email.id}" data-testid="email-checkbox-${email.id}">
                <input type="checkbox" ${isSelected ? 'checked' : ''} tabindex="-1">
            </div>
            ${dotType ? Components.unreadDot(dotType) : '<span class="dot-spacer"></span>'}
            <div class="email-avatar" data-action="open-email" data-email-id="${email.id}">
                ${Components.avatar(isSent ? (email.to[0]?.name || '?') : email.from.name, avatarColor, 36)}
            </div>
            <div class="email-content" data-action="open-email" data-email-id="${email.id}">
                <div class="email-header-row">
                    <span class="email-sender${!email.isRead ? ' bold' : ''}">${Components.escapeHtml(displayName)}</span>
                    <span class="email-date">${Components.formatDate(email.date)}</span>
                </div>
                <div class="email-subject-row">
                    <span class="email-subject${!email.isRead ? ' bold' : ''}">${Components.escapeHtml(email.subject)}</span>
                </div>
                <div class="email-snippet-row">
                    <span class="email-snippet">${Components.escapeHtml(email.snippet)}</span>
                </div>
                <div class="email-meta-row">
                    ${labels.map(l => Components.labelChip(l, false)).join('')}
                    ${email.hasAttachments ? Components.attachmentIcon() : ''}
                    ${email.readReceipt ? Components.readReceiptIcon(email.readReceipt) : ''}
                    ${email.replyDraftingTeammate ? `<span class="reply-indicator" title="${Components.escapeAttr(email.replyDraftingTeammate)} is drafting a reply">&#9998; ${Components.escapeHtml(email.replyDraftingTeammate)}</span>` : ''}
                </div>
            </div>
            <div class="email-actions">
                <button class="email-action-btn" data-action="toggle-star" data-email-id="${email.id}" data-testid="star-${email.id}" title="Star">${Components.starIcon(email.isStarred)}</button>
                <button class="email-action-btn" data-action="mark-done-single" data-email-id="${email.id}" data-testid="done-${email.id}" title="Mark Done (E)">&#10003;</button>
                <button class="email-action-btn" data-action="remind-single" data-email-id="${email.id}" data-testid="remind-${email.id}" title="Remind Me (H)">&#9200;</button>
            </div>
        </div>`;
    },

    _renderEmptyState() {
        const view = AppState.currentView;
        const icons = { inbox: '&#127881;', done: '&#10003;', reminders: '&#9200;', sent: '&#10148;', drafts: '&#9998;', starred: '&#9733;', spam: '&#9888;', trash: '&#128465;', search: '&#128269;' };
        const titles = { inbox: 'Inbox Zero!', done: 'No archived emails', reminders: 'No reminders', sent: 'No sent emails', drafts: 'No drafts', starred: 'No starred emails', spam: 'No spam', trash: 'Trash is empty', search: 'No results found' };
        const descs = { inbox: 'You\'ve processed all your emails. Great job!' };
        return Components.emptyState(icons[view] || '', titles[view] || 'Nothing here', descs[view] || '');
    },

    // ---- Email Detail ----
    renderEmailDetail(emailId) {
        const email = AppState.getEmail(emailId);
        if (!email) return Components.emptyState('&#9993;', 'Email not found');

        const isSent = email.from.email === AppState.currentUser.email;
        const contact = !isSent ? AppState.contacts.find(c => c.email === email.from.email) : null;
        const avatarColor = contact ? contact.avatarColor : (isSent ? AppState.currentUser.avatarColor : '#999');
        const labels = (email.labels || []).map(lId => AppState.labels.find(l => l.id === lId)).filter(Boolean);

        let threadHtml = '';
        if (email.threadMessages && email.threadMessages.length > 0) {
            threadHtml = `<div class="thread-messages">
                ${email.threadMessages.map(tm => {
                    const tmContact = AppState.contacts.find(c => c.email === tm.from.email);
                    const tmColor = tmContact ? tmContact.avatarColor : (tm.from.email === AppState.currentUser.email ? AppState.currentUser.avatarColor : '#999');
                    return `<div class="thread-message" data-testid="thread-msg-${tm.id}">
                        <div class="thread-msg-header">
                            ${Components.avatar(tm.from.name, tmColor, 28)}
                            <span class="thread-msg-sender">${Components.escapeHtml(tm.from.name)}</span>
                            <span class="thread-msg-date">${Components.formatFullDate(tm.date)}</span>
                        </div>
                        <div class="thread-msg-body">${Components.escapeHtml(tm.body).replace(/\n/g, '<br>')}</div>
                    </div>`;
                }).join('')}
            </div>`;
        }

        let readReceiptHtml = '';
        if (email.readReceipt && email.readReceipt.opened) {
            const r = email.readReceipt;
            readReceiptHtml = `<div class="read-receipt-detail" data-testid="read-receipt-detail">
                <div class="read-receipt-header">&#10003;&#10003; Read Receipt</div>
                <div class="read-receipt-info">Opened ${r.openCount || 1} time(s)</div>
                ${r.readers ? r.readers.map(rd => `<div class="read-receipt-reader">
                    <span>${Components.escapeHtml(rd.name)}</span>
                    <span>${Components.formatDate(rd.openedAt)} on ${Components.escapeHtml(rd.device)}</span>
                </div>`).join('') : `<div class="read-receipt-reader"><span>Opened ${Components.formatDate(r.openedAt)} on ${Components.escapeHtml(r.device)}</span></div>`}
            </div>`;
        }

        let attachmentsHtml = '';
        if (email.hasAttachments && email.attachments.length > 0) {
            attachmentsHtml = `<div class="attachments-section" data-testid="attachments">
                <div class="attachments-header">&#128206; ${email.attachments.length} attachment(s)</div>
                ${email.attachments.map(a => `<div class="attachment-item" data-testid="attachment-${Components.escapeAttr(a.name)}">
                    <span class="attachment-name">${Components.escapeHtml(a.name)}</span>
                    <span class="attachment-size">${Components.escapeHtml(a.size)}</span>
                </div>`).join('')}
            </div>`;
        }

        const reminderHtml = email.remindAt ? `<div class="reminder-banner" data-testid="reminder-banner">
            &#9200; Reminder set for ${Components.formatFullDate(email.remindAt)}
            <button class="btn-link" data-action="clear-reminder" data-email-id="${email.id}">Clear</button>
        </div>` : '';

        return `<div class="email-detail" data-testid="email-detail">
            <div class="email-detail-toolbar">
                <button class="btn-icon" data-action="back-to-list" data-testid="back-btn" title="Back">&larr;</button>
                <div class="email-detail-actions">
                    <button class="btn-icon" data-action="reply-email" data-email-id="${email.id}" data-testid="reply-btn" title="Reply (R)">&#8617; Reply</button>
                    <button class="btn-icon" data-action="reply-all-email" data-email-id="${email.id}" data-testid="reply-all-btn" title="Reply All">&#8617; Reply All</button>
                    <button class="btn-icon" data-action="forward-email" data-email-id="${email.id}" data-testid="forward-btn" title="Forward (F)">&#8618; Forward</button>
                    <button class="btn-icon" data-action="mark-done-single" data-email-id="${email.id}" data-testid="detail-done-btn" title="Mark Done (E)">&#10003; Done</button>
                    <button class="btn-icon" data-action="remind-single" data-email-id="${email.id}" data-testid="detail-remind-btn" title="Remind Me (H)">&#9200; Remind</button>
                    <button class="btn-icon" data-action="toggle-star" data-email-id="${email.id}" data-testid="detail-star-btn" title="Star">${Components.starIcon(email.isStarred)}</button>
                    <button class="btn-icon" data-action="label-email" data-email-id="${email.id}" data-testid="detail-label-btn" title="Label">&#127991;</button>
                    <button class="btn-icon" data-action="move-email" data-email-id="${email.id}" data-testid="detail-move-btn" title="Move (V)">&#128193;</button>
                    <button class="btn-icon" data-action="unsubscribe-email" data-email-id="${email.id}" data-testid="detail-unsub-btn" title="Unsubscribe (Cmd+U)">&#128683;</button>
                    <button class="btn-icon" data-action="trash-email" data-email-id="${email.id}" data-testid="detail-trash-btn" title="Trash">&#128465;</button>
                </div>
            </div>

            ${reminderHtml}

            <div class="email-detail-header">
                <div class="email-detail-avatar">${Components.avatar(email.from.name, avatarColor, 44)}</div>
                <div class="email-detail-meta">
                    <div class="email-detail-sender">
                        <strong>${Components.escapeHtml(email.from.name)}</strong>
                        <span class="email-detail-email">&lt;${Components.escapeHtml(email.from.email)}&gt;</span>
                        ${email.readReceipt ? Components.readReceiptIcon(email.readReceipt) : ''}
                    </div>
                    <div class="email-detail-recipients">
                        To: ${email.to.map(t => Components.escapeHtml(t.name || t.email)).join(', ')}
                        ${email.cc && email.cc.length > 0 ? ` | Cc: ${email.cc.map(c => Components.escapeHtml(c.name || c.email)).join(', ')}` : ''}
                    </div>
                    <div class="email-detail-date">${Components.formatFullDate(email.date)}</div>
                </div>
            </div>

            <h1 class="email-detail-subject">${Components.escapeHtml(email.subject)}</h1>

            <div class="email-detail-labels">
                ${labels.map(l => Components.labelChip(l, true)).join('')}
            </div>

            ${threadHtml}

            <div class="email-detail-body" data-testid="email-body">
                ${Components.escapeHtml(email.body || email.snippet).replace(/\n/g, '<br>')}
            </div>

            ${attachmentsHtml}
            ${readReceiptHtml}

            <div class="email-detail-reply-area">
                <div class="instant-replies" data-testid="instant-replies">
                    <button class="instant-reply-btn" data-action="instant-reply" data-email-id="${email.id}" data-reply-type="thanks" data-testid="instant-reply-thanks">Thanks for sending this over!</button>
                    <button class="instant-reply-btn" data-action="instant-reply" data-email-id="${email.id}" data-reply-type="sounds-good" data-testid="instant-reply-sounds-good">Sounds good, let's do it.</button>
                    <button class="instant-reply-btn" data-action="instant-reply" data-email-id="${email.id}" data-reply-type="will-review" data-testid="instant-reply-will-review">I'll review and get back to you.</button>
                </div>
            </div>
        </div>`;
    },

    // ---- Recent Opens ----
    renderRecentOpens() {
        const opens = AppState.recentOpens;
        if (opens.length === 0) {
            return Components.emptyState('&#128065;', 'No recent opens', 'When someone opens your email, it will appear here.');
        }
        return `<div class="opens-list" data-testid="opens-list">
            <h2 class="section-title">Recent Opens</h2>
            ${opens.map((o, i) => {
                const email = AppState.getEmail(o.emailId);
                return `<div class="opens-item" data-testid="open-${i}">
                    <div class="opens-info">
                        <strong>${Components.escapeHtml(o.reader)}</strong> opened
                        <a class="opens-email-link" data-action="open-email" data-email-id="${o.emailId}">"${Components.escapeHtml(email ? email.subject : 'Unknown')}"</a>
                    </div>
                    <div class="opens-meta">
                        <span>${Components.formatDate(o.openedAt)}</span>
                        <span class="opens-device">${Components.escapeHtml(o.device)}</span>
                    </div>
                </div>`;
            }).join('')}
        </div>`;
    },

    // ---- Snippets List ----
    renderSnippetsList() {
        const snippets = AppState.snippets;
        if (snippets.length === 0) {
            return Components.emptyState('&#128196;', 'No snippets', 'Create reusable email templates.');
        }
        return `<div class="snippets-list" data-testid="snippets-list">
            <div class="snippets-header">
                <h2 class="section-title">Snippets</h2>
                <button class="btn btn-primary btn-sm" data-action="create-snippet" data-testid="create-snippet-btn">+ New Snippet</button>
            </div>
            ${snippets.map(s => `<div class="snippet-item" data-testid="snippet-${s.id}">
                <div class="snippet-main">
                    <div class="snippet-name">${Components.escapeHtml(s.name)} ${s.isShared ? '<span class="snippet-shared-badge">Shared</span>' : ''}</div>
                    <div class="snippet-preview">${Components.escapeHtml(s.body.substring(0, 120))}...</div>
                    <div class="snippet-meta">
                        <span>By ${Components.escapeHtml(s.author)}</span>
                        ${s.metrics ? `<span class="snippet-metrics">${s.metrics.sends} sends | ${Math.round(s.metrics.openRate * 100)}% opens | ${Math.round(s.metrics.responseRate * 100)}% replies</span>` : ''}
                    </div>
                </div>
                <div class="snippet-actions">
                    <button class="btn-icon btn-sm" data-action="edit-snippet" data-snippet-id="${s.id}" data-testid="edit-snippet-${s.id}" title="Edit">&#9998;</button>
                    <button class="btn-icon btn-sm" data-action="toggle-snippet-share" data-snippet-id="${s.id}" data-testid="share-snippet-${s.id}" title="${s.isShared ? 'Unshare' : 'Share'}">${s.isShared ? '&#128101;' : '&#128100;'}</button>
                    <button class="btn-icon btn-sm" data-action="delete-snippet" data-snippet-id="${s.id}" data-testid="delete-snippet-${s.id}" title="Delete">&#128465;</button>
                </div>
            </div>`).join('')}
        </div>`;
    },

    // ---- Calendar Day View ----
    renderCalendarDay() {
        const today = AppState.calendarSelectedDate || new Date().toISOString().split('T')[0];
        const events = AppState.getEventsForDate(today);
        const dateObj = new Date(today + 'T12:00:00');
        const dateLabel = dateObj.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });

        return `<div class="calendar-day" data-testid="calendar-day">
            <div class="calendar-day-header">
                <button class="btn-icon" data-action="calendar-prev-day" data-testid="cal-prev">&lsaquo;</button>
                <h3 class="calendar-day-title">${dateLabel}</h3>
                <button class="btn-icon" data-action="calendar-next-day" data-testid="cal-next">&rsaquo;</button>
                <button class="btn-icon" data-action="calendar-today" data-testid="cal-today">Today</button>
            </div>
            <div class="calendar-events-list">
                ${events.length === 0 ? '<div class="calendar-empty">No events today</div>' :
                    events.map(evt => `<div class="calendar-event" style="border-left-color:${evt.color}" data-testid="event-${evt.id}">
                        <div class="calendar-event-time">${evt.isAllDay ? 'All Day' : `${Components.formatTime(evt.startTime)} - ${Components.formatTime(evt.endTime)}`}</div>
                        <div class="calendar-event-title">${Components.escapeHtml(evt.title)}</div>
                        <div class="calendar-event-location">${Components.escapeHtml(evt.location || '')}</div>
                        ${evt.meetingLink ? `<a class="calendar-event-link" href="${Components.escapeAttr(evt.meetingLink)}" target="_blank">Join meeting</a>` : ''}
                    </div>`).join('')}
            </div>
            <button class="btn btn-primary btn-block" data-action="create-event" data-testid="create-event-btn">+ New Event</button>
        </div>`;
    },

    // ---- Calendar Week View ----
    renderCalendarWeek() {
        const baseDate = new Date((AppState.calendarSelectedDate || new Date().toISOString().split('T')[0]) + 'T12:00:00');
        const dayOfWeek = baseDate.getDay();
        const monday = new Date(baseDate);
        monday.setDate(baseDate.getDate() - ((dayOfWeek + 6) % 7));

        const days = [];
        for (let i = 0; i < 7; i++) {
            const d = new Date(monday);
            d.setDate(monday.getDate() + i);
            const dateStr = d.toISOString().split('T')[0];
            days.push({
                date: dateStr,
                label: d.toLocaleDateString('en-US', { weekday: 'short' }),
                dayNum: d.getDate(),
                isToday: dateStr === new Date().toISOString().split('T')[0],
                events: AppState.getEventsForDate(dateStr)
            });
        }

        const weekLabel = `${days[0].label} ${days[0].dayNum} - ${days[6].label} ${days[6].dayNum}`;

        return `<div class="calendar-week" data-testid="calendar-week">
            <div class="calendar-week-header">
                <button class="btn-icon" data-action="calendar-prev-week" data-testid="cal-prev-week">&lsaquo;</button>
                <h3 class="calendar-week-title">${weekLabel}</h3>
                <button class="btn-icon" data-action="calendar-next-week" data-testid="cal-next-week">&rsaquo;</button>
                <button class="btn-icon" data-action="calendar-today" data-testid="cal-today-week">Today</button>
            </div>
            <div class="calendar-week-grid">
                ${days.map(day => `<div class="calendar-week-day${day.isToday ? ' today' : ''}" data-testid="week-day-${day.date}">
                    <div class="week-day-header">
                        <span class="week-day-label">${day.label}</span>
                        <span class="week-day-num${day.isToday ? ' today' : ''}">${day.dayNum}</span>
                    </div>
                    <div class="week-day-events">
                        ${day.events.map(evt => `<div class="week-event" style="background:${evt.color}20;border-left:3px solid ${evt.color}" data-action="open-event" data-event-id="${evt.id}" data-testid="week-event-${evt.id}">
                            <div class="week-event-time">${evt.isAllDay ? 'All day' : Components.formatTime(evt.startTime)}</div>
                            <div class="week-event-title">${Components.escapeHtml(evt.title)}</div>
                        </div>`).join('')}
                    </div>
                </div>`).join('')}
            </div>
        </div>`;
    },

    // ---- Settings ----
    renderSettings() {
        const tab = AppState.settingsTab;
        const tabs = [
            { id: 'general', label: 'General' },
            { id: 'readReceipts', label: 'Read Statuses' },
            { id: 'reminders', label: 'Reminders' },
            { id: 'autoLabels', label: 'Auto Labels' },
            { id: 'splits', label: 'Splits' },
            { id: 'calendar', label: 'Calendar' },
            { id: 'bookingPages', label: 'Booking Pages' },
            { id: 'shortcuts', label: 'Shortcuts' },
            { id: 'signature', label: 'Signature' },
            { id: 'autoArchive', label: 'Auto Archive' }
        ];

        let content = '';
        switch (tab) {
            case 'general': content = this._renderSettingsGeneral(); break;
            case 'readReceipts': content = this._renderSettingsReadReceipts(); break;
            case 'reminders': content = this._renderSettingsReminders(); break;
            case 'autoLabels': content = this._renderSettingsAutoLabels(); break;
            case 'splits': content = this._renderSettingsSplits(); break;
            case 'calendar': content = this._renderSettingsCalendar(); break;
            case 'bookingPages': content = this._renderSettingsBookingPages(); break;
            case 'shortcuts': content = this._renderSettingsShortcuts(); break;
            case 'signature': content = this._renderSettingsSignature(); break;
            case 'autoArchive': content = this._renderSettingsAutoArchive(); break;
        }

        return `<div class="settings-header">
            <h2>Settings</h2>
            <button class="btn-icon" data-action="close-settings" data-testid="close-settings">&times;</button>
        </div>
        <div class="settings-tabs">
            ${tabs.map(t => `<button class="settings-tab${t.id === tab ? ' active' : ''}" data-action="settings-tab" data-tab="${t.id}" data-testid="settings-tab-${t.id}">${t.label}</button>`).join('')}
        </div>
        <div class="settings-content" data-testid="settings-content-${tab}">
            ${content}
        </div>`;
    },

    _renderSettingsGeneral() {
        const s = AppState.settings;
        return `<div class="settings-section">
            <h3>Appearance</h3>
            ${Components.dropdown('theme', [
                { value: 'light', label: 'Light' },
                { value: 'dark', label: 'Dark' },
                { value: 'auto', label: 'System' }
            ], s.theme, 'Theme')}
        </div>
        <div class="settings-section">
            <h3>Notifications</h3>
            ${Components.toggle('notifications-desktop', s.notifications.desktop, 'Desktop notifications', 'Show notification banners')}
            ${Components.toggle('notifications-sound', s.notifications.sound, 'Sound', 'Play a sound for new emails')}
        </div>
        <div class="settings-section">
            <h3>Swipe Actions</h3>
            ${Components.dropdown('swipe-left', [
                { value: 'done', label: 'Mark Done' },
                { value: 'trash', label: 'Trash' },
                { value: 'spam', label: 'Spam' }
            ], s.swipeLeft, 'Swipe Left')}
            ${Components.dropdown('swipe-right', [
                { value: 'remind', label: 'Remind Me' },
                { value: 'star', label: 'Star' },
                { value: 'unread', label: 'Mark Unread' }
            ], s.swipeRight, 'Swipe Right')}
        </div>
        <div class="settings-section">
            <h3>AI Features</h3>
            ${Components.toggle('instant-reply', s.instantReply.enabled, 'Instant Reply', 'Show AI-suggested replies on emails')}
            ${Components.toggle('smart-send', s.smartSend.enabled, 'Smart Send', 'Recommend optimal send times')}
            ${Components.toggle('ask-ai', s.askAi.enabled, 'Ask AI', 'AI-powered search and actions')}
        </div>
        <div class="settings-section">
            <h3>Account</h3>
            <div class="settings-info-row">
                <span>Email</span>
                <span>${Components.escapeHtml(AppState.currentUser.email)}</span>
            </div>
            <div class="settings-info-row">
                <span>Plan</span>
                <span class="plan-badge">${Components.escapeHtml(AppState.currentUser.plan)}</span>
            </div>
            <div class="settings-info-row">
                <span>Timezone</span>
                <span>${Components.escapeHtml(s.timezone)}</span>
            </div>
        </div>`;
    },

    _renderSettingsReadReceipts() {
        const s = AppState.settings.readReceipts;
        return `<div class="settings-section">
            <h3>Read Statuses</h3>
            <p class="settings-desc">See when your emails are opened, what device was used, and how many times they were viewed.</p>
            ${Components.toggle('read-receipts-enabled', s.enabled, 'Enable Read Statuses', 'Track when recipients open your emails')}
            ${Components.toggle('read-receipts-team', s.teamSharing, 'Team Read Statuses', 'Share read status info with teammates')}
        </div>`;
    },

    _renderSettingsReminders() {
        const s = AppState.settings.autoReminders;
        const ad = AppState.settings.autoDrafts;
        return `<div class="settings-section">
            <h3>Auto Reminders</h3>
            <p class="settings-desc">Get reminded when your emails don't get a reply.</p>
            ${Components.toggle('auto-reminders-enabled', s.enabled, 'Enable Auto Reminders', 'Automatically remind you about unreplied emails')}
            ${Components.radioGroup('auto-reminder-mode', [
                { value: 'ai', label: 'AI-detected follow-ups', description: 'Remind only when AI detects the email needs a follow-up' },
                { value: 'external', label: 'All external emails', description: 'Remind for all emails sent to external recipients' },
                { value: 'none', label: 'No auto reminders', description: 'Only manual reminders' }
            ], s.mode)}
            ${Components.dropdown('auto-reminder-time', [
                { value: '09:00', label: '9:00 AM' },
                { value: '10:00', label: '10:00 AM' },
                { value: '14:00', label: '2:00 PM' },
                { value: '17:00', label: '5:00 PM' }
            ], s.defaultTime, 'Default reminder time')}
        </div>
        <div class="settings-section">
            <h3>Auto Drafts</h3>
            <p class="settings-desc">Automatically draft follow-up messages when reminders resurface.</p>
            ${Components.toggle('auto-drafts-enabled', ad.enabled, 'Enable Auto Drafts', 'AI drafts follow-up emails for you')}
            ${Components.radioGroup('auto-draft-type', [
                { value: 'follow-up', label: 'Follow-up', description: 'Draft a follow-up message' },
                { value: 'scheduling', label: 'Scheduling', description: 'Draft a scheduling request' }
            ], ad.type)}
            ${Components.toggle('auto-drafts-cc', ad.ccTeammate, 'Cc teammate for scheduling', 'Add a teammate on Cc when scheduling')}
        </div>`;
    },

    _renderSettingsAutoLabels() {
        const autoLabels = AppState.autoLabels;
        return `<div class="settings-section">
            <h3>Auto Labels</h3>
            <p class="settings-desc">Automatically categorize incoming emails with labels.</p>
            <div class="auto-labels-list">
                ${autoLabels.map(al => `<div class="auto-label-item" data-testid="auto-label-${al.id}">
                    <div class="auto-label-info">
                        <span class="auto-label-name">${Components.escapeHtml(al.name)}</span>
                        <span class="auto-label-type">${al.type}</span>
                    </div>
                    <div class="auto-label-actions">
                        ${Components.toggle('al-' + al.id, al.enabled, '', '')}
                        ${al.type === 'custom' ? `<button class="btn-icon btn-sm" data-action="delete-auto-label" data-auto-label-id="${al.id}" data-testid="delete-al-${al.id}">&#128465;</button>` : ''}
                    </div>
                </div>`).join('')}
            </div>
            <button class="btn btn-secondary" data-action="create-auto-label" data-testid="create-auto-label-btn">+ Create Auto Label</button>
        </div>`;
    },

    _renderSettingsSplits() {
        const splits = AppState.splits.sort((a, b) => a.position - b.position);
        return `<div class="settings-section">
            <h3>Split Inbox</h3>
            <p class="settings-desc">Organize your inbox into separate sections for faster triage.</p>
            <div class="splits-list">
                ${splits.map(s => `<div class="split-item" data-testid="split-item-${s.id}">
                    <span class="split-item-name">${Components.escapeHtml(s.name)}</span>
                    <span class="split-item-desc">${Components.escapeHtml(s.description || '')}</span>
                    ${!s.isDefault ? `<button class="btn-icon btn-sm" data-action="delete-split" data-split-id="${s.id}" data-testid="delete-split-${s.id}">&#128465;</button>` : '<span class="split-default-badge">Default</span>'}
                </div>`).join('')}
            </div>
            <button class="btn btn-secondary" data-action="create-split" data-testid="create-split-btn">+ Create Split</button>
        </div>`;
    },

    _renderSettingsCalendar() {
        const s = AppState.settings;
        return `<div class="settings-section">
            <h3>Calendar</h3>
            ${Components.toggle('calendar-alerts', s.notifications.calendarAlerts, 'Calendar alerts', 'Show notifications before events')}
            ${Components.dropdown('alert-minutes', [
                { value: '5', label: '5 minutes before' },
                { value: '10', label: '10 minutes before' },
                { value: '15', label: '15 minutes before' },
                { value: '30', label: '30 minutes before' }
            ], String(s.notifications.alertMinutes), 'Alert time')}
        </div>
        <div class="settings-section">
            <h3>Meeting Links</h3>
            ${Components.dropdown('meeting-provider', [
                { value: 'zoom', label: 'Zoom' },
                { value: 'google-meet', label: 'Google Meet' },
                { value: 'teams', label: 'Microsoft Teams' },
                { value: 'none', label: 'None' }
            ], s.meetingLink.provider, 'Default provider')}
            ${Components.toggle('meeting-auto-add', s.meetingLink.autoAdd, 'Auto-add meeting link', 'Automatically add a meeting link to new events')}
        </div>
        <div class="settings-section">
            <h3>Timezone</h3>
            ${Components.dropdown('timezone', [
                { value: 'America/New_York', label: 'Eastern Time (ET)' },
                { value: 'America/Chicago', label: 'Central Time (CT)' },
                { value: 'America/Denver', label: 'Mountain Time (MT)' },
                { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
                { value: 'Europe/London', label: 'London (GMT)' },
                { value: 'Europe/Paris', label: 'Paris (CET)' },
                { value: 'Asia/Tokyo', label: 'Tokyo (JST)' }
            ], s.timezone, 'Primary timezone')}
            ${Components.dropdown('secondary-timezone', [
                { value: '', label: 'None' },
                { value: 'America/New_York', label: 'Eastern Time (ET)' },
                { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
                { value: 'Europe/London', label: 'London (GMT)' },
                { value: 'Europe/Paris', label: 'Paris (CET)' },
                { value: 'Asia/Tokyo', label: 'Tokyo (JST)' }
            ], s.secondaryTimezone, 'Secondary timezone')}
        </div>`;
    },

    _renderSettingsBookingPages() {
        const bps = AppState.bookingPages;
        return `<div class="settings-section">
            <h3>Booking Pages</h3>
            <p class="settings-desc">Share your availability and let others book time with you.</p>
            <div class="booking-pages-list">
                ${bps.map(bp => `<div class="booking-page-item" data-testid="bp-${bp.id}">
                    <div class="bp-info">
                        <div class="bp-title">${Components.escapeHtml(bp.title)}</div>
                        <div class="bp-meta">${bp.duration} min | ${Components.escapeHtml(bp.location)} | ${bp.isActive ? 'Active' : 'Inactive'}</div>
                        <div class="bp-link">${Components.escapeHtml(bp.link)}</div>
                    </div>
                    <div class="bp-actions">
                        <button class="btn-icon btn-sm" data-action="toggle-booking-page" data-bp-id="${bp.id}" data-testid="toggle-bp-${bp.id}">${bp.isActive ? '&#9989;' : '&#10060;'}</button>
                        <button class="btn-icon btn-sm" data-action="delete-booking-page" data-bp-id="${bp.id}" data-testid="delete-bp-${bp.id}">&#128465;</button>
                    </div>
                </div>`).join('')}
            </div>
            <button class="btn btn-secondary" data-action="create-booking-page" data-testid="create-bp-btn">+ New Booking Page</button>
        </div>`;
    },

    _renderSettingsShortcuts() {
        const shortcuts = [
            { key: 'E', desc: 'Mark Done (archive)' },
            { key: 'H', desc: 'Set Reminder' },
            { key: 'R', desc: 'Reply' },
            { key: 'Enter', desc: 'Reply All' },
            { key: 'F', desc: 'Forward' },
            { key: 'J / K', desc: 'Next / Previous email' },
            { key: 'V', desc: 'Move to folder' },
            { key: 'Cmd+K', desc: 'Command Palette' },
            { key: 'Cmd+J', desc: 'Write with AI' },
            { key: 'Cmd+U', desc: 'Unsubscribe' },
            { key: 'Cmd+Enter', desc: 'Send email' },
            { key: '/', desc: 'Search' },
            { key: ';', desc: 'Insert Snippet' },
            { key: '0', desc: 'Calendar Day View' },
            { key: '2', desc: 'Calendar Week View' },
            { key: 'Tab', desc: 'Next Split' },
            { key: 'Shift+Tab', desc: 'Previous Split' },
            { key: 'G then E', desc: 'Go to Done' },
            { key: 'G then H', desc: 'Go to Reminders' },
            { key: 'Cmd+A', desc: 'Select all' },
            { key: '?', desc: 'Ask AI' }
        ];
        return `<div class="settings-section">
            <h3>Keyboard Shortcuts</h3>
            ${Components.toggle('shortcuts-enabled', AppState.settings.keyboard.shortcuts, 'Enable keyboard shortcuts')}
            <div class="shortcuts-list">
                ${shortcuts.map(s => `<div class="shortcut-row">
                    <span class="shortcut-key-display">${Components.shortcutHint(s.key)}</span>
                    <span class="shortcut-desc">${Components.escapeHtml(s.desc)}</span>
                </div>`).join('')}
            </div>
        </div>`;
    },

    _renderSettingsSignature() {
        return `<div class="settings-section">
            <h3>Email Signature</h3>
            <textarea id="signature-input" class="signature-textarea" data-testid="signature-input">${Components.escapeHtml(AppState.settings.signature || '')}</textarea>
            <button class="btn btn-primary" data-action="save-signature" data-testid="save-signature-btn">Save Signature</button>
        </div>`;
    },

    _renderSettingsAutoArchive() {
        const aa = AppState.settings.autoArchive;
        return `<div class="settings-section">
            <h3>Auto Archive</h3>
            <p class="settings-desc">Automatically archive emails matching certain Auto Labels. They remain searchable in Done.</p>
            ${Components.toggle('auto-archive-enabled', aa.enabled, 'Enable Auto Archive', 'Automatically send matching emails to Done')}
            <div class="auto-archive-labels">
                <h4>Archive emails with these labels:</h4>
                ${AppState.autoLabels.map(al => {
                    const isArchived = aa.labels.includes(al.id);
                    return `<label class="checkbox-row">
                        <input type="checkbox" ${isArchived ? 'checked' : ''} data-action="toggle-auto-archive-label" data-label-id="${al.id}" data-testid="aa-${al.id}">
                        <span>${Components.escapeHtml(al.name)}</span>
                    </label>`;
                }).join('')}
            </div>
        </div>`;
    },

    // ---- Command Palette ----
    renderCommandPalette() {
        return `<div class="command-palette-overlay" data-testid="command-palette">
            <div class="command-palette">
                <div class="command-palette-input-wrapper">
                    <input type="text" id="commandInput" class="command-palette-input" placeholder="Type a command..." data-testid="command-input" autocomplete="off">
                </div>
                <div class="command-palette-results" id="commandResults">
                    ${this._renderDefaultCommands()}
                </div>
            </div>
        </div>`;
    },

    _renderDefaultCommands() {
        const commands = [
            { action: 'cmd-compose', label: 'Compose new email', shortcut: 'C' },
            { action: 'cmd-search', label: 'Search', shortcut: '/' },
            { action: 'cmd-goto-inbox', label: 'Go to Inbox', shortcut: '' },
            { action: 'cmd-goto-done', label: 'Go to Done', shortcut: 'G E' },
            { action: 'cmd-goto-reminders', label: 'Go to Reminders', shortcut: 'G H' },
            { action: 'cmd-goto-sent', label: 'Go to Sent', shortcut: '' },
            { action: 'cmd-goto-snippets', label: 'Go to Snippets', shortcut: 'G ;' },
            { action: 'cmd-goto-opens', label: 'Go to Recent Opens', shortcut: '' },
            { action: 'cmd-calendar-day', label: 'Open Day View', shortcut: '0' },
            { action: 'cmd-calendar-week', label: 'Open Week View', shortcut: '2' },
            { action: 'cmd-settings', label: 'Open Settings', shortcut: '' },
            { action: 'cmd-create-event', label: 'Create Event', shortcut: 'B' },
            { action: 'cmd-create-snippet', label: 'Create Snippet', shortcut: '' },
            { action: 'cmd-get-me-to-zero', label: 'Get Me To Zero', shortcut: '' }
        ];
        return commands.map(c => `<div class="command-item" data-action="${c.action}" data-testid="cmd-${c.action}">
            <span class="command-label">${Components.escapeHtml(c.label)}</span>
            ${c.shortcut ? `<span class="command-shortcut">${c.shortcut}</span>` : ''}
        </div>`).join('');
    },

    // ---- Reminder Picker ----
    renderReminderPicker() {
        const options = Components.reminderOptions();
        return `<div class="picker-overlay" data-testid="reminder-picker">
            <div class="picker-panel">
                <div class="picker-header">
                    <h3>Remind Me</h3>
                    <button class="btn-icon" data-action="close-reminder-picker">&times;</button>
                </div>
                <div class="picker-options">
                    ${options.map(o => `<div class="picker-option" data-action="set-reminder-option" data-value="${o.value}" data-testid="reminder-${o.label.toLowerCase().replace(/\s+/g, '-')}">
                        <span class="picker-option-label">${Components.escapeHtml(o.label)}</span>
                        <span class="picker-option-sublabel">${Components.escapeHtml(o.sublabel)}</span>
                    </div>`).join('')}
                </div>
                <div class="picker-custom">
                    <label>Custom date & time</label>
                    <input type="text" id="customReminderDate" placeholder="YYYY-MM-DD" class="text-input" data-testid="custom-reminder-date">
                    <input type="text" id="customReminderTime" placeholder="HH:MM" class="text-input" data-testid="custom-reminder-time">
                    <button class="btn btn-primary btn-sm" data-action="set-custom-reminder" data-testid="set-custom-reminder">Set</button>
                </div>
            </div>
        </div>`;
    },

    // ---- Label Picker ----
    renderLabelPicker() {
        const userLabels = AppState.labels.filter(l => l.type === 'user');
        const emailId = AppState.labelPickerEmailId;
        const email = AppState.getEmail(emailId);
        const currentLabels = email ? email.labels : [];

        return `<div class="picker-overlay" data-testid="label-picker">
            <div class="picker-panel">
                <div class="picker-header">
                    <h3>Apply Label</h3>
                    <button class="btn-icon" data-action="close-label-picker">&times;</button>
                </div>
                <div class="picker-options">
                    ${userLabels.map(l => `<label class="picker-checkbox-option" data-testid="label-option-${l.id}">
                        <input type="checkbox" ${currentLabels.includes(l.id) ? 'checked' : ''} data-action="toggle-email-label" data-email-id="${emailId}" data-label-id="${l.id}">
                        <span class="label-dot" style="background:${l.color}"></span>
                        <span>${Components.escapeHtml(l.name)}</span>
                    </label>`).join('')}
                </div>
            </div>
        </div>`;
    },

    // ---- Move Picker ----
    renderMovePicker() {
        const folders = [
            { id: 'INBOX', label: 'Inbox' },
            { id: 'DONE', label: 'Done' },
            { id: 'TRASH', label: 'Trash' },
            { id: 'SPAM', label: 'Spam' }
        ];
        return `<div class="picker-overlay" data-testid="move-picker">
            <div class="picker-panel">
                <div class="picker-header">
                    <h3>Move to</h3>
                    <button class="btn-icon" data-action="close-move-picker">&times;</button>
                </div>
                <div class="picker-options">
                    ${folders.map(f => `<div class="picker-option" data-action="move-to-folder" data-folder="${f.id}" data-testid="move-${f.id}">
                        ${Components.escapeHtml(f.label)}
                    </div>`).join('')}
                </div>
            </div>
        </div>`;
    },

    // ---- Compose Modal ----
    renderComposeContent() {
        const draft = AppState.composeDraft || {};
        const mode = AppState.replyMode;
        let title = 'New Message';
        if (mode === 'reply') title = 'Reply';
        else if (mode === 'reply-all') title = 'Reply All';
        else if (mode === 'forward') title = 'Forward';

        return { title, draft };
    },

    // ---- Snippet Picker (for compose) ----
    renderSnippetPicker() {
        return `<div class="picker-overlay" data-testid="snippet-picker">
            <div class="picker-panel picker-panel-wide">
                <div class="picker-header">
                    <h3>Insert Snippet</h3>
                    <button class="btn-icon" data-action="close-snippet-picker">&times;</button>
                </div>
                <input type="text" id="snippetSearch" class="text-input" placeholder="Search snippets..." data-testid="snippet-search">
                <div class="picker-options" id="snippetPickerOptions">
                    ${AppState.snippets.map(s => `<div class="picker-option snippet-picker-item" data-action="insert-snippet" data-snippet-id="${s.id}" data-testid="snippet-option-${s.id}">
                        <div class="snippet-picker-name">${Components.escapeHtml(s.name)}</div>
                        <div class="snippet-picker-preview">${Components.escapeHtml(s.body.substring(0, 80))}</div>
                    </div>`).join('')}
                </div>
            </div>
        </div>`;
    }
};
