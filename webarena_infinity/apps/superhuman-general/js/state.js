// ============================================================
// state.js — Centralized state management for Superhuman Mail
// ============================================================

const AppState = {
    // ---- Persistent State ----
    emails: [],
    contacts: [],
    labels: [],
    autoLabels: [],
    splits: [],
    snippets: [],
    calendarEvents: [],
    settings: {},
    currentUser: null,
    recentOpens: [],
    bookingPages: [],

    // ---- ID Counters ----
    _nextEmailId: 200,
    _nextLabelId: 30,
    _nextSnippetId: 30,
    _nextEventId: 30,
    _nextAutoLabelId: 20,
    _nextSplitId: 20,
    _nextBookingPageId: 10,

    // ---- UI State (not persisted) ----
    currentView: 'inbox',
    currentSplit: 'split_important',
    currentEmailId: null,
    selectedEmailIds: new Set(),
    searchQuery: '',
    searchResults: null,
    composeOpen: false,
    composeDraft: null,
    commandPaletteOpen: false,
    reminderPickerOpen: false,
    reminderPickerEmailId: null,
    labelPickerOpen: false,
    labelPickerEmailId: null,
    movePickerOpen: false,
    movePickerEmailId: null,
    settingsOpen: false,
    settingsTab: 'general',
    calendarView: 'none',
    calendarSelectedDate: null,
    currentPage: 1,
    pageSize: 25,
    toastMessage: null,
    replyMode: null,
    replyToEmailId: null,
    snippetPickerOpen: false,

    // ---- Listeners ----
    _listeners: [],

    subscribe(fn) {
        this._listeners.push(fn);
    },

    notify() {
        this._persist();
        this._pushStateToServer();
        for (const fn of this._listeners) {
            try { fn(); } catch (e) { console.error('Listener error:', e); }
        }
    },

    // ---- Initialization ----
    init() {
        const persisted = this._loadPersistedData();
        if (persisted) {
            this.emails = persisted.emails || [];
            this.contacts = persisted.contacts || [];
            this.labels = persisted.labels || [];
            this.autoLabels = persisted.autoLabels || [];
            this.splits = persisted.splits || [];
            this.snippets = persisted.snippets || [];
            this.calendarEvents = persisted.calendarEvents || [];
            this.settings = persisted.settings || {};
            this.currentUser = persisted.currentUser || null;
            this.recentOpens = persisted.recentOpens || [];
            this.bookingPages = persisted.bookingPages || [];
            this._nextEmailId = persisted._nextEmailId || 200;
            this._nextLabelId = persisted._nextLabelId || 30;
            this._nextSnippetId = persisted._nextSnippetId || 30;
            this._nextEventId = persisted._nextEventId || 30;
            this._nextAutoLabelId = persisted._nextAutoLabelId || 20;
            this._nextSplitId = persisted._nextSplitId || 20;
            this._nextBookingPageId = persisted._nextBookingPageId || 10;
        } else {
            this._loadSeedData();
        }
    },

    _loadSeedData() {
        this.currentUser = JSON.parse(JSON.stringify(CURRENT_USER));
        this.emails = JSON.parse(JSON.stringify(EMAILS));
        this.contacts = JSON.parse(JSON.stringify(CONTACTS));
        this.labels = JSON.parse(JSON.stringify(LABELS));
        this.autoLabels = JSON.parse(JSON.stringify(AUTO_LABELS));
        this.splits = JSON.parse(JSON.stringify(SPLITS));
        this.snippets = JSON.parse(JSON.stringify(SNIPPETS));
        this.calendarEvents = JSON.parse(JSON.stringify(CALENDAR_EVENTS));
        this.settings = JSON.parse(JSON.stringify(SETTINGS));
        this.recentOpens = JSON.parse(JSON.stringify(RECENT_OPENS));
        this.bookingPages = JSON.parse(JSON.stringify(BOOKING_PAGES));
        this._nextEmailId = Math.max(...this.emails.map(e => e.id)) + 1;
        this._nextLabelId = 30;
        this._nextSnippetId = 30;
        this._nextEventId = 30;
    },

    resetToSeedData() {
        localStorage.removeItem('superhumanAppState');
        this._loadSeedData();
        this.currentView = 'inbox';
        this.currentSplit = 'split_important';
        this.currentEmailId = null;
        this.selectedEmailIds = new Set();
        this.searchQuery = '';
        this.searchResults = null;
        this.composeOpen = false;
        this.composeDraft = null;
        this.settingsOpen = false;
        this.calendarView = 'none';
        this.commandPaletteOpen = false;
    },

    _loadPersistedData() {
        try {
            const saved = localStorage.getItem('superhumanAppState');
            if (!saved) return null;
            const parsed = JSON.parse(saved);
            if (parsed._seedVersion !== SEED_DATA_VERSION) {
                localStorage.removeItem('superhumanAppState');
                return null;
            }
            return parsed;
        } catch (e) {
            return null;
        }
    },

    // ---- Persistence ----
    _persist() {
        const state = this.getSerializableState();
        localStorage.setItem('superhumanAppState', JSON.stringify(state));
    },

    _pushStateToServer() {
        const state = this.getSerializableState();
        fetch('/api/state', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(state)
        }).catch(() => {});
    },

    getSerializableState() {
        return {
            _seedVersion: SEED_DATA_VERSION,
            emails: this.emails,
            contacts: this.contacts,
            labels: this.labels,
            autoLabels: this.autoLabels,
            splits: this.splits,
            snippets: this.snippets,
            calendarEvents: this.calendarEvents,
            settings: this.settings,
            currentUser: this.currentUser,
            recentOpens: this.recentOpens,
            bookingPages: this.bookingPages,
            _nextEmailId: this._nextEmailId,
            _nextLabelId: this._nextLabelId,
            _nextSnippetId: this._nextSnippetId,
            _nextEventId: this._nextEventId,
            _nextAutoLabelId: this._nextAutoLabelId,
            _nextSplitId: this._nextSplitId,
            _nextBookingPageId: this._nextBookingPageId
        };
    },

    // ---- Email Queries ----
    getInboxEmails() {
        return this.emails.filter(e => !e.isDone && !e.isTrashed && !e.isSpam && !e.isDraft && !e.remindAt);
    },

    getInboxEmailsBySplit(splitId) {
        const inbox = this.getInboxEmails();
        const split = this.splits.find(s => s.id === splitId);
        if (!split) return inbox;

        if (split.criteria.type === 'important') {
            return inbox.filter(e => e.splitCategory === 'important');
        } else if (split.criteria.type === 'other') {
            return inbox.filter(e => e.splitCategory === 'other');
        } else if (split.criteria.type === 'calendar') {
            return inbox.filter(e => e.splitCategory === 'calendar');
        } else if (split.criteria.autoLabel) {
            return inbox.filter(e => e.autoLabel === split.criteria.autoLabel);
        }
        return inbox;
    },

    getDoneEmails() {
        return this.emails.filter(e => e.isDone && !e.isTrashed);
    },

    getReminderEmails() {
        return this.emails.filter(e => e.remindAt !== null && !e.isTrashed);
    },

    getSentEmails() {
        return this.emails.filter(e => e.from.email === this.currentUser.email && !e.isDraft && !e.isTrashed);
    },

    getDraftEmails() {
        return this.emails.filter(e => e.isDraft && !e.isTrashed);
    },

    getStarredEmails() {
        return this.emails.filter(e => e.isStarred && !e.isTrashed);
    },

    getSpamEmails() {
        return this.emails.filter(e => e.isSpam && !e.isTrashed);
    },

    getTrashEmails() {
        return this.emails.filter(e => e.isTrashed);
    },

    getEmailsByLabel(labelId) {
        return this.emails.filter(e => e.labels && e.labels.includes(labelId) && !e.isTrashed);
    },

    getEmail(id) {
        return this.emails.find(e => e.id === id);
    },

    getUnreadCount(view) {
        let emails;
        switch (view) {
            case 'inbox': emails = this.getInboxEmails(); break;
            case 'spam': emails = this.getSpamEmails(); break;
            default: return 0;
        }
        return emails.filter(e => !e.isRead).length;
    },

    getSplitUnreadCount(splitId) {
        return this.getInboxEmailsBySplit(splitId).filter(e => !e.isRead).length;
    },

    // ---- Email Mutations ----
    markAsRead(emailIds) {
        const ids = Array.isArray(emailIds) ? emailIds : [emailIds];
        ids.forEach(id => {
            const email = this.emails.find(e => e.id === id);
            if (email) email.isRead = true;
        });
        this.notify();
    },

    markAsUnread(emailIds) {
        const ids = Array.isArray(emailIds) ? emailIds : [emailIds];
        ids.forEach(id => {
            const email = this.emails.find(e => e.id === id);
            if (email) email.isRead = false;
        });
        this.notify();
    },

    toggleStar(emailId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.isStarred = !email.isStarred;
            this.notify();
        }
    },

    markDone(emailIds) {
        const ids = Array.isArray(emailIds) ? emailIds : [emailIds];
        ids.forEach(id => {
            const email = this.emails.find(e => e.id === id);
            if (email) {
                email.isDone = true;
                email.isRead = true;
                email.remindAt = null;
            }
        });
        this.selectedEmailIds = new Set();
        this.notify();
    },

    undoMarkDone(emailId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.isDone = false;
            this.notify();
        }
    },

    setReminder(emailId, remindAt) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.remindAt = remindAt;
            email.isRead = true;
            this.notify();
        }
    },

    clearReminder(emailId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.remindAt = null;
            this.notify();
        }
    },

    moveToTrash(emailIds) {
        const ids = Array.isArray(emailIds) ? emailIds : [emailIds];
        ids.forEach(id => {
            const email = this.emails.find(e => e.id === id);
            if (email) {
                email.isTrashed = true;
                email.isDone = false;
                email.remindAt = null;
            }
        });
        this.selectedEmailIds = new Set();
        this.notify();
    },

    restoreFromTrash(emailId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.isTrashed = false;
            this.notify();
        }
    },

    markAsSpam(emailIds) {
        const ids = Array.isArray(emailIds) ? emailIds : [emailIds];
        ids.forEach(id => {
            const email = this.emails.find(e => e.id === id);
            if (email) {
                email.isSpam = true;
                email.isDone = false;
                email.remindAt = null;
            }
        });
        this.selectedEmailIds = new Set();
        this.notify();
    },

    unmarkSpam(emailId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.isSpam = false;
            this.notify();
        }
    },

    addLabel(emailId, labelId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email && !email.labels.includes(labelId)) {
            email.labels.push(labelId);
            this.notify();
        }
    },

    removeLabel(emailId, labelId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.labels = email.labels.filter(l => l !== labelId);
            this.notify();
        }
    },

    moveToFolder(emailId, folder) {
        const email = this.emails.find(e => e.id === emailId);
        if (!email) return;
        // Reset state
        email.isDone = false;
        email.isTrashed = false;
        email.isSpam = false;
        email.remindAt = null;

        switch (folder) {
            case 'DONE': email.isDone = true; break;
            case 'TRASH': email.isTrashed = true; break;
            case 'SPAM': email.isSpam = true; break;
            case 'INBOX': break; // already reset
        }
        this.notify();
    },

    // ---- Compose ----
    sendEmail(draft) {
        const email = {
            id: this._nextEmailId++,
            threadId: 'thread_' + this._nextEmailId,
            from: { name: this.currentUser.name, email: this.currentUser.email },
            to: draft.to || [],
            cc: draft.cc || [],
            bcc: draft.bcc || [],
            subject: draft.subject || '(no subject)',
            snippet: (draft.body || '').substring(0, 100),
            body: draft.body || '',
            date: new Date().toISOString(),
            isRead: true,
            isStarred: false,
            isDone: false,
            isTrashed: false,
            isSpam: false,
            isDraft: false,
            labels: [],
            hasAttachments: false,
            attachments: [],
            splitCategory: 'important',
            remindAt: null,
            readReceipt: { opened: false },
            autoLabel: null,
            replyDraftingTeammate: null,
            threadMessages: null
        };
        this.emails.unshift(email);
        this.notify();
        return email;
    },

    saveDraft(draft) {
        const existing = this.emails.find(e => e.isDraft && e.id === draft.id);
        if (existing) {
            Object.assign(existing, {
                to: draft.to || [],
                cc: draft.cc || [],
                subject: draft.subject || '',
                body: draft.body || '',
                snippet: (draft.body || '').substring(0, 100),
                date: new Date().toISOString()
            });
        } else {
            const email = {
                id: this._nextEmailId++,
                threadId: 'thread_' + this._nextEmailId,
                from: { name: this.currentUser.name, email: this.currentUser.email },
                to: draft.to || [],
                cc: draft.cc || [],
                bcc: [],
                subject: draft.subject || '',
                snippet: (draft.body || '').substring(0, 100),
                body: draft.body || '',
                date: new Date().toISOString(),
                isRead: true, isStarred: false, isDone: false, isTrashed: false,
                isSpam: false, isDraft: true, labels: [], hasAttachments: false,
                attachments: [], splitCategory: 'important', remindAt: null,
                readReceipt: null, autoLabel: null, replyDraftingTeammate: null,
                threadMessages: null
            };
            this.emails.unshift(email);
        }
        this.notify();
    },

    deleteDraft(emailId) {
        this.emails = this.emails.filter(e => e.id !== emailId);
        this.notify();
    },

    // ---- Labels ----
    createLabel(name, color) {
        const label = {
            id: 'label_' + this._nextLabelId++,
            name,
            type: 'user',
            color: color || '#6C4FF7'
        };
        this.labels.push(label);
        this.notify();
        return label;
    },

    updateLabel(labelId, updates) {
        const label = this.labels.find(l => l.id === labelId);
        if (label && label.type === 'user') {
            Object.assign(label, updates);
            this.notify();
        }
    },

    deleteLabel(labelId) {
        this.labels = this.labels.filter(l => l.id !== labelId);
        this.emails.forEach(e => {
            e.labels = e.labels.filter(l => l !== labelId);
        });
        this.notify();
    },

    // ---- Auto Labels ----
    createAutoLabel(name, criteria, type) {
        const al = {
            id: 'al_' + this._nextAutoLabelId++,
            name, type: type || 'custom',
            enabled: true, criteria
        };
        this.autoLabels.push(al);
        this.notify();
        return al;
    },

    toggleAutoLabel(id) {
        const al = this.autoLabels.find(a => a.id === id);
        if (al) {
            al.enabled = !al.enabled;
            this.notify();
        }
    },

    deleteAutoLabel(id) {
        this.autoLabels = this.autoLabels.filter(a => a.id !== id);
        this.notify();
    },

    // ---- Splits ----
    createSplit(name, criteria) {
        const split = {
            id: 'split_' + this._nextSplitId++,
            name,
            position: this.splits.length,
            isDefault: false,
            criteria: criteria || {}
        };
        this.splits.push(split);
        this.notify();
        return split;
    },

    deleteSplit(splitId) {
        const split = this.splits.find(s => s.id === splitId);
        if (split && !split.isDefault) {
            this.splits = this.splits.filter(s => s.id !== splitId);
            if (this.currentSplit === splitId) {
                this.currentSplit = 'split_important';
            }
            this.notify();
        }
    },

    reorderSplits(orderedIds) {
        orderedIds.forEach((id, i) => {
            const split = this.splits.find(s => s.id === id);
            if (split) split.position = i;
        });
        this.splits.sort((a, b) => a.position - b.position);
        this.notify();
    },

    // ---- Snippets ----
    createSnippet(data) {
        const snippet = {
            id: 'snip_' + this._nextSnippetId++,
            name: data.name || 'Untitled',
            body: data.body || '',
            variables: data.variables || [],
            isShared: data.isShared || false,
            author: this.currentUser.name,
            authorId: this.currentUser.id,
            createdAt: new Date().toISOString(),
            metrics: { sends: 0, openRate: 0, responseRate: 0 }
        };
        this.snippets.push(snippet);
        this.notify();
        return snippet;
    },

    updateSnippet(snippetId, updates) {
        const snippet = this.snippets.find(s => s.id === snippetId);
        if (snippet) {
            Object.assign(snippet, updates);
            this.notify();
        }
    },

    deleteSnippet(snippetId) {
        this.snippets = this.snippets.filter(s => s.id !== snippetId);
        this.notify();
    },

    toggleSnippetSharing(snippetId) {
        const snippet = this.snippets.find(s => s.id === snippetId);
        if (snippet) {
            snippet.isShared = !snippet.isShared;
            this.notify();
        }
    },

    // ---- Calendar ----
    createEvent(data) {
        const event = {
            id: 'evt_' + this._nextEventId++,
            title: data.title || 'New Event',
            date: data.date,
            startTime: data.startTime || '09:00',
            endTime: data.endTime || '10:00',
            location: data.location || '',
            description: data.description || '',
            attendees: data.attendees || [],
            meetingLink: data.meetingLink || null,
            isAllDay: data.isAllDay || false,
            calendarId: data.calendarId || 'work',
            organizer: this.currentUser.email,
            status: 'confirmed',
            color: data.color || '#6C4FF7'
        };
        this.calendarEvents.push(event);
        this.notify();
        return event;
    },

    updateEvent(eventId, updates) {
        const event = this.calendarEvents.find(e => e.id === eventId);
        if (event) {
            Object.assign(event, updates);
            this.notify();
        }
    },

    deleteEvent(eventId) {
        this.calendarEvents = this.calendarEvents.filter(e => e.id !== eventId);
        this.notify();
    },

    getEventsForDate(date) {
        return this.calendarEvents.filter(e => e.date === date).sort((a, b) => {
            if (a.isAllDay && !b.isAllDay) return -1;
            if (!a.isAllDay && b.isAllDay) return 1;
            return a.startTime.localeCompare(b.startTime);
        });
    },

    // ---- Booking Pages ----
    createBookingPage(data) {
        const bp = {
            id: 'bp_' + this._nextBookingPageId++,
            title: data.title || 'Meeting',
            duration: data.duration || 30,
            location: data.location || 'Zoom',
            description: data.description || '',
            availability: data.availability || { days: ['Mon','Tue','Wed','Thu','Fri'], startTime: '09:00', endTime: '17:00' },
            link: 'https://cal.superhuman.com/' + this.currentUser.email.split('@')[0] + '/' + (data.title || 'meeting').toLowerCase().replace(/\s+/g, '-'),
            isActive: true
        };
        this.bookingPages.push(bp);
        this.notify();
        return bp;
    },

    toggleBookingPage(bpId) {
        const bp = this.bookingPages.find(b => b.id === bpId);
        if (bp) {
            bp.isActive = !bp.isActive;
            this.notify();
        }
    },

    deleteBookingPage(bpId) {
        this.bookingPages = this.bookingPages.filter(b => b.id !== bpId);
        this.notify();
    },

    // ---- Settings ----
    updateSetting(path, value) {
        const keys = path.split('.');
        let obj = this.settings;
        for (let i = 0; i < keys.length - 1; i++) {
            if (!obj[keys[i]]) obj[keys[i]] = {};
            obj = obj[keys[i]];
        }
        obj[keys[keys.length - 1]] = value;
        this.notify();
    },

    updateUserProfile(updates) {
        Object.assign(this.currentUser, updates);
        this.notify();
    },

    // ---- Search ----
    searchEmails(query) {
        if (!query || !query.trim()) {
            this.searchResults = null;
            return;
        }
        const q = query.toLowerCase().trim();
        const allEmails = this.emails.filter(e => !e.isTrashed && !e.isSpam);

        // Parse search operators
        const fromMatch = q.match(/from:(\S+)/);
        const toMatch = q.match(/to:(\S+)/);
        const subjectMatch = q.match(/subject:(.+?)(?:\s+(?:from|to|has|subject):|$)/);
        const hasAttachment = q.includes('has:attachment');

        let results = allEmails;

        if (fromMatch) {
            const fromQ = fromMatch[1].toLowerCase();
            results = results.filter(e => e.from.email.toLowerCase().includes(fromQ) || e.from.name.toLowerCase().includes(fromQ));
        }
        if (toMatch) {
            const toQ = toMatch[1].toLowerCase();
            results = results.filter(e => e.to.some(t => t.email.toLowerCase().includes(toQ) || t.name.toLowerCase().includes(toQ)));
        }
        if (subjectMatch) {
            const subQ = subjectMatch[1].toLowerCase().trim();
            results = results.filter(e => e.subject.toLowerCase().includes(subQ));
        }
        if (hasAttachment) {
            results = results.filter(e => e.hasAttachments);
        }

        // If no operators, do general text search
        if (!fromMatch && !toMatch && !subjectMatch && !hasAttachment) {
            results = results.filter(e =>
                e.subject.toLowerCase().includes(q) ||
                e.snippet.toLowerCase().includes(q) ||
                e.from.name.toLowerCase().includes(q) ||
                e.from.email.toLowerCase().includes(q) ||
                (e.body && e.body.toLowerCase().includes(q))
            );
        }

        this.searchResults = results.sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    // ---- Pagination ----
    getPagedEmails(emails) {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return {
            items: emails.slice(start, end),
            total: emails.length,
            start: start + 1,
            end: Math.min(end, emails.length),
            hasNext: end < emails.length,
            hasPrev: start > 0
        };
    },

    // ---- Unsubscribe ----
    unsubscribe(emailId) {
        const email = this.emails.find(e => e.id === emailId);
        if (email) {
            email.isDone = true;
            email.isRead = true;
            // Block future emails from this sender
            const senderEmail = email.from.email;
            if (!this.settings.blockedSenders) {
                this.settings.blockedSenders = [];
            }
            if (!this.settings.blockedSenders.includes(senderEmail)) {
                this.settings.blockedSenders.push(senderEmail);
            }
            this.notify();
        }
    }
};
