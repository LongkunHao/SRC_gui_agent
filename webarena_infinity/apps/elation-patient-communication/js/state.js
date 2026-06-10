/* ============================================================
   Elation Patient Communication — State Management
   ============================================================ */

const AppState = {
    // ── Persistent data ─────────────────────────────────────
    currentUser: null,
    providers: [],
    userGroups: [],
    patients: [],
    patientLetters: [],
    appointments: [],
    reminders: [],
    bulkLetters: [],
    visitSummaries: [],
    practiceSettings: null,
    messageRouting: {},
    messageCategories: [],
    patientTags: [],
    sharingLevels: null,
    notificationTimeframes: [],

    // ID counters
    _nextPatientId: 51,
    _nextLetterId: 100,
    _nextConversationId: 40,
    _nextAppointmentId: 21,
    _nextReminderId: 11,
    _nextBulkLetterId: 4,
    _nextVisitSummaryId: 6,
    _nextLocationId: 4,
    _nextCptCodeId: 14,

    // ── UI state (transient) ────────────────────────────────
    currentView: 'home',
    currentPatientId: null,
    currentLetterId: null,
    currentConversationId: null,
    settingsTab: 'user',
    searchQuery: '',
    searchResults: [],
    patientListFilter: {
        providerId: 'all',
        passportStatus: ['registered', 'invited', 'not_invited'],
        tags: [],
        search: ''
    },
    patientListPage: 1,
    patientListPageSize: 20,
    composeOpen: false,
    composeDraft: null,
    bulkComposeOpen: false,
    selectedPatientIds: [],

    // ── Listeners ───────────────────────────────────────────
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

    // ── Initialization ──────────────────────────────────────
    init() {
        const saved = localStorage.getItem('elationState');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                if (parsed._seedVersion === SEED_DATA_VERSION) {
                    this._restoreState(parsed);
                    this._recalcCounts();
                    return;
                }
            } catch (e) {
                console.warn('Failed to parse saved state:', e);
            }
            localStorage.removeItem('elationState');
        }
        this._loadSeedData();
    },

    _loadSeedData() {
        this.currentUser = JSON.parse(JSON.stringify(CURRENT_USER));
        this.providers = JSON.parse(JSON.stringify(PROVIDERS));
        this.userGroups = JSON.parse(JSON.stringify(USER_GROUPS));
        this.patients = JSON.parse(JSON.stringify(PATIENTS));
        this.patientLetters = JSON.parse(JSON.stringify(PATIENT_LETTERS));
        this.appointments = JSON.parse(JSON.stringify(APPOINTMENTS));
        this.reminders = JSON.parse(JSON.stringify(REMINDERS));
        this.bulkLetters = JSON.parse(JSON.stringify(BULK_LETTERS));
        this.visitSummaries = JSON.parse(JSON.stringify(VISIT_SUMMARIES));
        this.practiceSettings = JSON.parse(JSON.stringify(PRACTICE_SETTINGS));
        this.messageRouting = JSON.parse(JSON.stringify(MESSAGE_ROUTING));
        this.messageCategories = [...MESSAGE_CATEGORIES];
        this.patientTags = [...PATIENT_TAGS];
        this.sharingLevels = JSON.parse(JSON.stringify(SHARING_LEVELS));
        this.notificationTimeframes = JSON.parse(JSON.stringify(NOTIFICATION_TIMEFRAMES));

        const counters = JSON.parse(JSON.stringify(INITIAL_COUNTERS));
        Object.assign(this, counters);
        this._recalcCounts();
    },

    _restoreState(parsed) {
        const keys = [
            'currentUser', 'providers', 'userGroups', 'patients', 'patientLetters',
            'appointments', 'reminders', 'bulkLetters', 'visitSummaries',
            'practiceSettings', 'messageRouting', 'messageCategories', 'patientTags',
            'sharingLevels', 'notificationTimeframes',
            '_nextPatientId', '_nextLetterId', '_nextConversationId',
            '_nextAppointmentId', '_nextReminderId', '_nextBulkLetterId',
            '_nextVisitSummaryId', '_nextLocationId', '_nextCptCodeId'
        ];
        for (const key of keys) {
            if (parsed[key] !== undefined) {
                this[key] = parsed[key];
            }
        }
    },

    resetToSeedData() {
        localStorage.removeItem('elationState');
        this._loadSeedData();
        this.currentView = 'home';
        this.currentPatientId = null;
        this.currentLetterId = null;
        this.currentConversationId = null;
        this.settingsTab = 'user';
        this.searchQuery = '';
        this.searchResults = [];
        this.composeOpen = false;
        this.composeDraft = null;
        this.bulkComposeOpen = false;
        this.selectedPatientIds = [];
        this.notify();
    },

    // ── Serialization ───────────────────────────────────────
    getSerializableState() {
        return {
            _seedVersion: SEED_DATA_VERSION,
            currentUser: this.currentUser,
            providers: this.providers,
            userGroups: this.userGroups,
            patients: this.patients,
            patientLetters: this.patientLetters,
            appointments: this.appointments,
            reminders: this.reminders,
            bulkLetters: this.bulkLetters,
            visitSummaries: this.visitSummaries,
            practiceSettings: this.practiceSettings,
            messageRouting: this.messageRouting,
            messageCategories: this.messageCategories,
            patientTags: this.patientTags,
            sharingLevels: this.sharingLevels,
            notificationTimeframes: this.notificationTimeframes,
            _nextPatientId: this._nextPatientId,
            _nextLetterId: this._nextLetterId,
            _nextConversationId: this._nextConversationId,
            _nextAppointmentId: this._nextAppointmentId,
            _nextReminderId: this._nextReminderId,
            _nextBulkLetterId: this._nextBulkLetterId,
            _nextVisitSummaryId: this._nextVisitSummaryId,
            _nextLocationId: this._nextLocationId,
            _nextCptCodeId: this._nextCptCodeId
        };
    },

    _persist() {
        localStorage.setItem('elationState', JSON.stringify(this.getSerializableState()));
    },

    _pushStateToServer() {
        try {
            fetch('/api/state', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.getSerializableState())
            });
        } catch (e) {
            console.warn('Failed to push state to server:', e);
        }
    },

    _recalcCounts() {
        // Recalculate unread counts etc.
    },

    // ── Query Methods ───────────────────────────────────────

    getPatient(id) {
        return this.patients.find(p => p.id === id);
    },

    getProvider(id) {
        return this.providers.find(p => p.id === id);
    },

    getProviderName(id) {
        const p = this.getProvider(id);
        return p ? `${p.firstName} ${p.lastName}` : 'Unknown';
    },

    formatRole(role) {
        const roles = { physician: 'Physician', nurse_practitioner: 'Nurse Practitioner', physician_assistant: 'Physician Assistant' };
        return roles[role] || role;
    },

    getPatientName(id) {
        const p = this.getPatient(id);
        return p ? `${p.firstName} ${p.lastName}` : 'Unknown';
    },

    getConversationLetters(conversationId) {
        return this.patientLetters
            .filter(l => l.conversationId === conversationId)
            .sort((a, b) => new Date(a.sentAt || 0) - new Date(b.sentAt || 0));
    },

    getPatientLetters(patientId) {
        return this.patientLetters
            .filter(l => l.patientId === patientId)
            .sort((a, b) => new Date(b.sentAt || 0) - new Date(a.sentAt || 0));
    },

    getInboxLetters() {
        // Unread patient-sent messages, plus recent conversations
        return this.patientLetters
            .filter(l => l.direction === 'from_patient' && !l.isDraft)
            .sort((a, b) => new Date(b.sentAt) - new Date(a.sentAt));
    },

    getUnreadInboxCount() {
        return this.patientLetters
            .filter(l => l.direction === 'from_patient' && !l.isRead && !l.isDraft)
            .length;
    },

    getDraftLetters() {
        return this.patientLetters.filter(l => l.isDraft);
    },

    getSentLetters() {
        return this.patientLetters
            .filter(l => l.direction === 'to_patient' && !l.isDraft)
            .sort((a, b) => new Date(b.sentAt) - new Date(a.sentAt));
    },

    getUnacknowledgedReminders() {
        return this.reminders.filter(r => !r.acknowledged);
    },

    getUpcomingAppointments() {
        const now = new Date().toISOString();
        return this.appointments
            .filter(a => a.date >= now && a.status === 'scheduled')
            .sort((a, b) => new Date(a.date) - new Date(b.date));
    },

    getPastAppointments() {
        const now = new Date().toISOString();
        return this.appointments
            .filter(a => a.date < now || a.status === 'completed')
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    getFilteredPatients() {
        let list = [...this.patients];
        const f = this.patientListFilter;

        if (f.providerId && f.providerId !== 'all') {
            list = list.filter(p => p.assignedProviderId === f.providerId);
        }
        if (f.passportStatus && f.passportStatus.length > 0) {
            list = list.filter(p => f.passportStatus.includes(p.passportStatus));
        }
        if (f.tags && f.tags.length > 0) {
            list = list.filter(p => f.tags.some(t => p.tags.includes(t)));
        }
        if (f.search) {
            const q = f.search.toLowerCase();
            list = list.filter(p =>
                `${p.firstName} ${p.lastName}`.toLowerCase().includes(q) ||
                (p.email && p.email.toLowerCase().includes(q)) ||
                (p.cellPhone && p.cellPhone.includes(q)) ||
                p.id.toLowerCase().includes(q)
            );
        }
        return list.sort((a, b) => `${a.lastName} ${a.firstName}`.localeCompare(`${b.lastName} ${b.firstName}`));
    },

    getPagedPatients() {
        const all = this.getFilteredPatients();
        const start = (this.patientListPage - 1) * this.patientListPageSize;
        return {
            patients: all.slice(start, start + this.patientListPageSize),
            total: all.length,
            page: this.patientListPage,
            totalPages: Math.ceil(all.length / this.patientListPageSize)
        };
    },

    searchPatients(query) {
        if (!query) return [];
        const q = query.toLowerCase();
        return this.patients.filter(p =>
            `${p.firstName} ${p.lastName}`.toLowerCase().includes(q) ||
            (p.email && p.email.toLowerCase().includes(q))
        ).slice(0, 10);
    },

    getPatientAppointments(patientId) {
        return this.appointments
            .filter(a => a.patientId === patientId)
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    getPatientVisitSummaries(patientId) {
        return this.visitSummaries
            .filter(vs => vs.patientId === patientId && vs.signed)
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    // ── Mutation Methods ────────────────────────────────────

    // Patient Letters
    sendLetter(patientId, subject, body, opts) {
        const convId = opts?.conversationId || `conv_${this._nextConversationId++}`;
        const letter = {
            id: `ltr_${this._nextLetterId++}`,
            patientId,
            conversationId: convId,
            direction: 'to_patient',
            subject,
            body,
            category: null,
            senderId: this.currentUser.id,
            senderType: 'provider',
            attachments: opts?.attachments || [],
            postDate: opts?.postDate || null,
            sentAt: new Date().toISOString(),
            readAt: null,
            isRead: false,
            isDraft: false,
            conversationState: 'open',
            doNotAllowResponse: opts?.doNotAllowResponse || false,
            unreadAlertTimeframe: opts?.unreadAlertTimeframe || 'none',
            printHeader: opts?.printHeader || 'default'
        };
        this.patientLetters.push(letter);
        this.notify();
        return letter;
    },

    saveDraft(patientId, subject, body, opts) {
        const existingDraft = opts?.letterId ? this.patientLetters.find(l => l.id === opts.letterId) : null;
        if (existingDraft) {
            existingDraft.subject = subject;
            existingDraft.body = body;
            existingDraft.attachments = opts?.attachments || existingDraft.attachments;
            existingDraft.doNotAllowResponse = opts?.doNotAllowResponse || false;
            existingDraft.unreadAlertTimeframe = opts?.unreadAlertTimeframe || 'none';
            this.notify();
            return existingDraft;
        }
        const convId = opts?.conversationId || `conv_${this._nextConversationId++}`;
        const letter = {
            id: `ltr_${this._nextLetterId++}`,
            patientId,
            conversationId: convId,
            direction: 'to_patient',
            subject,
            body,
            category: null,
            senderId: this.currentUser.id,
            senderType: 'provider',
            attachments: opts?.attachments || [],
            postDate: null,
            sentAt: null,
            readAt: null,
            isRead: false,
            isDraft: true,
            conversationState: 'open',
            doNotAllowResponse: opts?.doNotAllowResponse || false,
            unreadAlertTimeframe: opts?.unreadAlertTimeframe || 'none',
            printHeader: opts?.printHeader || 'default'
        };
        this.patientLetters.push(letter);
        this.notify();
        return letter;
    },

    sendDraft(letterId) {
        const letter = this.patientLetters.find(l => l.id === letterId);
        if (letter) {
            letter.isDraft = false;
            letter.sentAt = new Date().toISOString();
            this.notify();
        }
    },

    deleteDraft(letterId) {
        const idx = this.patientLetters.findIndex(l => l.id === letterId);
        if (idx !== -1) {
            this.patientLetters.splice(idx, 1);
            this.notify();
        }
    },

    replyToConversation(conversationId, body) {
        const convLetters = this.getConversationLetters(conversationId);
        if (convLetters.length === 0) return;
        const first = convLetters[0];
        const subject = first.subject.startsWith('Re: ') ? first.subject : `Re: ${first.subject}`;
        const letter = {
            id: `ltr_${this._nextLetterId++}`,
            patientId: first.patientId,
            conversationId,
            direction: 'to_patient',
            subject,
            body,
            category: null,
            senderId: this.currentUser.id,
            senderType: 'provider',
            attachments: [],
            postDate: null,
            sentAt: new Date().toISOString(),
            readAt: null,
            isRead: false,
            isDraft: false,
            conversationState: 'open',
            doNotAllowResponse: false,
            unreadAlertTimeframe: 'none',
            printHeader: 'default'
        };
        this.patientLetters.push(letter);
        this.notify();
        return letter;
    },

    endConversation(conversationId) {
        const letters = this.patientLetters.filter(l => l.conversationId === conversationId);
        letters.forEach(l => {
            l.conversationState = 'ended';
        });
        this.notify();
    },

    markLetterRead(letterId) {
        const letter = this.patientLetters.find(l => l.id === letterId);
        if (letter && !letter.isRead) {
            letter.isRead = true;
            letter.readAt = new Date().toISOString();
            this.notify();
        }
    },

    // Passport Management
    sendPassportInvitation(patientId, opts) {
        const patient = this.getPatient(patientId);
        if (!patient) return;
        if (opts?.email) patient.email = opts.email;
        if (opts?.cellPhone) patient.cellPhone = opts.cellPhone;
        if (opts?.sharingLevel) patient.passportSharingLevel = opts.sharingLevel;
        patient.passportStatus = 'invited';
        patient.invitedAt = new Date().toISOString();
        patient.invitationCode = String(Math.floor(1000000 + Math.random() * 9000000));
        this.notify();
    },

    resendPassportInvitation(patientId) {
        const patient = this.getPatient(patientId);
        if (!patient) return;
        patient.invitedAt = new Date().toISOString();
        patient.invitationCode = String(Math.floor(1000000 + Math.random() * 9000000));
        this.notify();
    },

    disablePassportAccount(patientId) {
        const patient = this.getPatient(patientId);
        if (!patient) return;
        patient.passportAccountDisabled = true;
        patient.passportStatus = 'not_invited';
        this.notify();
    },

    updatePassportSharingLevel(patientId, level) {
        const patient = this.getPatient(patientId);
        if (!patient) return;
        patient.passportSharingLevel = level;
        this.notify();
    },

    // Patient management
    updatePatientDemographics(patientId, updates) {
        const patient = this.getPatient(patientId);
        if (!patient) return;
        Object.assign(patient, updates);
        this.notify();
    },

    addPatientTag(patientId, tag) {
        const patient = this.getPatient(patientId);
        if (!patient || patient.tags.includes(tag)) return;
        patient.tags.push(tag);
        this.notify();
    },

    removePatientTag(patientId, tag) {
        const patient = this.getPatient(patientId);
        if (!patient) return;
        patient.tags = patient.tags.filter(t => t !== tag);
        this.notify();
    },

    updateSmsOptIn(patientId, status) {
        const patient = this.getPatient(patientId);
        if (!patient) return;
        patient.smsOptInStatus = status;
        this.notify();
    },

    // Reminders
    acknowledgeReminder(reminderId) {
        const rem = this.reminders.find(r => r.id === reminderId);
        if (rem) {
            rem.acknowledged = true;
            this.notify();
        }
    },

    // Settings
    updateProviderSettings(providerId, updates) {
        const prov = this.providers.find(p => p.id === providerId);
        if (!prov) return;
        Object.assign(prov, updates);
        this.notify();
    },

    updatePracticeSettings(updates) {
        Object.assign(this.practiceSettings, updates);
        this.notify();
    },

    updateMessageRouting(providerId, category, recipients) {
        if (!this.messageRouting[providerId]) {
            this.messageRouting[providerId] = {};
        }
        this.messageRouting[providerId][category] = recipients;
        this.notify();
    },

    updateAllProvidersRouting(category, recipients) {
        for (const prov of this.providers) {
            if (!this.messageRouting[prov.id]) {
                this.messageRouting[prov.id] = {};
            }
            this.messageRouting[prov.id][category] = [...recipients];
        }
        this.notify();
    },

    toggleAllowPatientMessaging(enabled) {
        this.practiceSettings.allowPatientMessaging = enabled;
        this.notify();
    },

    toggleBookingSiteAutoInvite(enabled) {
        this.practiceSettings.bookingSiteAutoInvite = enabled;
        this.notify();
    },

    // Virtual Visit
    activateVirtualVisit(providerId, instructions) {
        const prov = this.providers.find(p => p.id === providerId);
        if (!prov) return;
        prov.virtualVisitActivated = true;
        prov.virtualVisitInstructions = instructions || prov.virtualVisitInstructions;
        this.notify();
    },

    deactivateVirtualVisit(providerId) {
        const prov = this.providers.find(p => p.id === providerId);
        if (!prov) return;
        prov.virtualVisitActivated = false;
        this.notify();
    },

    updateVirtualVisitInstructions(providerId, instructions) {
        const prov = this.providers.find(p => p.id === providerId);
        if (!prov) return;
        prov.virtualVisitInstructions = instructions;
        this.notify();
    },

    updateVideoSettings(settings) {
        Object.assign(this.practiceSettings.videoSettings, settings);
        this.notify();
    },

    // Practice Locations
    addPracticeLocation(location) {
        location.id = `loc_${this._nextLocationId++}`;
        this.practiceSettings.practiceLocations.push(location);
        this.notify();
        return location;
    },

    updatePracticeLocation(locationId, updates) {
        const loc = this.practiceSettings.practiceLocations.find(l => l.id === locationId);
        if (!loc) return;
        Object.assign(loc, updates);
        this.notify();
    },

    removePracticeLocation(locationId) {
        this.practiceSettings.practiceLocations = this.practiceSettings.practiceLocations.filter(l => l.id !== locationId);
        this.notify();
    },

    // CPT Codes
    addCptCode(code) {
        this.practiceSettings.cptCodes.push(code);
        this.notify();
    },

    removeCptCode(code) {
        this.practiceSettings.cptCodes = this.practiceSettings.cptCodes.filter(c => c.code !== code);
        this.notify();
    },

    // Appointments
    addAppointment(appt) {
        appt.id = `appt_${this._nextAppointmentId++}`;
        this.appointments.push(appt);
        this.notify();
        return appt;
    },

    updateAppointment(apptId, updates) {
        const appt = this.appointments.find(a => a.id === apptId);
        if (!appt) return;
        Object.assign(appt, updates);
        this.notify();
    },

    cancelAppointment(apptId) {
        const appt = this.appointments.find(a => a.id === apptId);
        if (appt) {
            appt.status = 'cancelled';
            this.notify();
        }
    },

    // Bulk Letters
    sendBulkLetter(data) {
        const bulk = {
            id: `bulk_${this._nextBulkLetterId++}`,
            description: data.description,
            subject: data.subject,
            body: data.body,
            sentAt: new Date().toISOString(),
            sentBy: this.currentUser.id,
            targetCount: data.targetPatientIds ? data.targetPatientIds.length : 0,
            allowResponse: data.allowResponse || false
        };
        this.bulkLetters.push(bulk);

        // Create individual letters for each patient
        if (data.targetPatientIds) {
            const convId = `conv_${this._nextConversationId++}`;
            for (const patId of data.targetPatientIds) {
                this.patientLetters.push({
                    id: `ltr_${this._nextLetterId++}`,
                    patientId: patId,
                    conversationId: `${convId}_${patId}`,
                    direction: 'to_patient',
                    subject: data.subject,
                    body: data.body,
                    category: null,
                    senderId: this.currentUser.id,
                    senderType: 'provider',
                    attachments: [],
                    postDate: null,
                    sentAt: new Date().toISOString(),
                    readAt: null,
                    isRead: false,
                    isDraft: false,
                    conversationState: data.allowResponse ? 'open' : 'ended',
                    doNotAllowResponse: !data.allowResponse,
                    unreadAlertTimeframe: 'none',
                    printHeader: 'default'
                });
            }
        }

        this.notify();
        return bulk;
    }
};
