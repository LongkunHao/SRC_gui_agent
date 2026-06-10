const AppState = {
    // ---- Persistent state (serialized to localStorage + server)
    currentUser: null,
    employers: [],
    jobs: [],
    feedPosts: [],
    events: [],
    appointments: [],
    appointmentCategories: [],
    appointmentStaff: [],
    availableSlots: [],
    qaQuestions: [],
    messages: [],
    schoolLabels: [],

    // ---- Counters
    _nextPostId: 100,
    _nextCommentId: 100,
    _nextAppointmentId: 100,
    _nextQuestionId: 100,
    _nextAnswerId: 100,

    // ---- UI state (not persisted)
    currentPage: 'feed',
    currentSubPage: null,
    feedFilter: 'All',
    feedTab: 'feed',
    jobSearchQuery: '',
    jobFilters: { type: '', location: '', label: '', role: '' },
    employerSearchQuery: '',
    eventSearchQuery: '',
    eventTypeFilter: 'All Types',
    eventShowVirtualOnly: false,
    qaSearchQuery: '',
    qaTab: 'all',
    messageFilter: 'all',
    activeModal: null,
    newPostAudience: 'Everyone on Handshake',
    modalData: null,
    selectedEmployerId: null,
    selectedEmployerTab: 'overview',
    selectedJobId: null,
    selectedEventId: null,
    selectedAppointmentId: null,
    selectedQuestionId: null,
    selectedMessageId: null,
    appointmentScheduling: {
        category: null,
        type: null,
        staff: null,
        date: null,
        time: null,
        medium: null,
        details: ''
    },
    toastMessage: null,
    toastTimeout: null,

    // ---- Listeners
    _listeners: [],

    subscribe(fn) {
        this._listeners.push(fn);
    },

    notify() {
        this._persist();
        this._pushStateToServer();
        for (const fn of this._listeners) {
            try { fn(); } catch (e) { console.error(e); }
        }
    },

    // ---- Initialization
    init() {
        const persisted = this._loadPersistedData();
        if (persisted) {
            this._restoreFromPersisted(persisted);
        } else {
            this._loadSeedData();
        }
    },

    _loadSeedData() {
        this.currentUser = JSON.parse(JSON.stringify(CURRENT_USER));
        this.employers = JSON.parse(JSON.stringify(EMPLOYERS));
        this.jobs = JSON.parse(JSON.stringify(JOBS));
        this.feedPosts = JSON.parse(JSON.stringify(FEED_POSTS));
        this.events = JSON.parse(JSON.stringify(EVENTS));
        this.appointments = JSON.parse(JSON.stringify(APPOINTMENTS));
        this.appointmentCategories = JSON.parse(JSON.stringify(APPOINTMENT_CATEGORIES));
        this.appointmentStaff = JSON.parse(JSON.stringify(APPOINTMENT_STAFF));
        this.availableSlots = JSON.parse(JSON.stringify(AVAILABLE_APPOINTMENT_SLOTS));
        this.qaQuestions = JSON.parse(JSON.stringify(QA_QUESTIONS));
        this.messages = JSON.parse(JSON.stringify(MESSAGES));
        this.schoolLabels = [...SCHOOL_LABELS];
        this._nextPostId = 100;
        this._nextCommentId = 100;
        this._nextAppointmentId = 100;
        this._nextQuestionId = 100;
        this._nextAnswerId = 100;
    },

    _restoreFromPersisted(data) {
        this.currentUser = data.currentUser;
        this.employers = data.employers;
        this.jobs = data.jobs;
        this.feedPosts = data.feedPosts;
        this.events = data.events;
        this.appointments = data.appointments;
        this.appointmentCategories = data.appointmentCategories;
        this.appointmentStaff = data.appointmentStaff;
        this.availableSlots = data.availableSlots;
        this.qaQuestions = data.qaQuestions;
        this.messages = data.messages;
        this.schoolLabels = data.schoolLabels;
        this._nextPostId = data._nextPostId || 100;
        this._nextCommentId = data._nextCommentId || 100;
        this._nextAppointmentId = data._nextAppointmentId || 100;
        this._nextQuestionId = data._nextQuestionId || 100;
        this._nextAnswerId = data._nextAnswerId || 100;
    },

    // ---- Persistence
    _persist() {
        const state = this.getSerializableState();
        localStorage.setItem('handshakeCareerExploration', JSON.stringify(state));
    },

    _loadPersistedData() {
        const saved = localStorage.getItem('handshakeCareerExploration');
        if (!saved) return null;
        try {
            const parsed = JSON.parse(saved);
            if (parsed._seedVersion !== SEED_DATA_VERSION) {
                localStorage.removeItem('handshakeCareerExploration');
                return null;
            }
            return parsed;
        } catch (e) {
            localStorage.removeItem('handshakeCareerExploration');
            return null;
        }
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
            currentUser: this.currentUser,
            employers: this.employers,
            jobs: this.jobs,
            feedPosts: this.feedPosts,
            events: this.events,
            appointments: this.appointments,
            appointmentCategories: this.appointmentCategories,
            appointmentStaff: this.appointmentStaff,
            availableSlots: this.availableSlots,
            qaQuestions: this.qaQuestions,
            messages: this.messages,
            schoolLabels: this.schoolLabels,
            _nextPostId: this._nextPostId,
            _nextCommentId: this._nextCommentId,
            _nextAppointmentId: this._nextAppointmentId,
            _nextQuestionId: this._nextQuestionId,
            _nextAnswerId: this._nextAnswerId
        };
    },

    resetToSeedData() {
        localStorage.removeItem('handshakeCareerExploration');
        this._loadSeedData();
        this.currentPage = 'feed';
        this.currentSubPage = null;
        this.activeModal = null;
        this.modalData = null;
        this.selectedEmployerId = null;
        this.selectedJobId = null;
        this.selectedEventId = null;
        this.selectedAppointmentId = null;
        this.selectedQuestionId = null;
        this.selectedMessageId = null;
        this.feedFilter = 'All';
        this.feedTab = 'feed';
        this.jobSearchQuery = '';
        this.jobFilters = { type: '', location: '', label: '', role: '' };
        this.employerSearchQuery = '';
        this.eventSearchQuery = '';
        this.eventTypeFilter = 'All Types';
        this.eventShowVirtualOnly = false;
        this.qaSearchQuery = '';
        this.qaTab = 'all';
        this.messageFilter = 'all';
        this.appointmentScheduling = { category: null, type: null, staff: null, date: null, time: null, medium: null, details: '' };
        this.notify();
    },

    // ---- Toast
    showToast(message) {
        this.toastMessage = message;
        if (this.toastTimeout) clearTimeout(this.toastTimeout);
        this.toastTimeout = setTimeout(() => {
            this.toastMessage = null;
            for (const fn of this._listeners) { try { fn(); } catch (e) {} }
        }, 3000);
    },

    // ============================================================
    // FEED MUTATIONS
    // ============================================================
    createPost(content, audience) {
        if (!content || !content.trim()) return;
        const id = 'post_' + String(this._nextPostId++);
        this.feedPosts.unshift({
            id,
            authorType: 'student',
            authorId: this.currentUser.id,
            authorName: this.currentUser.fullName,
            authorSchool: this.currentUser.school,
            authorAvatarColor: this.currentUser.avatarColor,
            content: content.trim(),
            audience: audience || 'everyone',
            likes: 0,
            comments: [],
            hasImage: false,
            hasVideo: false,
            createdAt: new Date().toISOString(),
            bookmarked: false
        });
        this.notify();
        return id;
    },

    likePost(postId) {
        const post = this.feedPosts.find(p => p.id === postId);
        if (post) {
            post.likes = (post.likes || 0) + 1;
            this.notify();
        }
    },

    unlikePost(postId) {
        const post = this.feedPosts.find(p => p.id === postId);
        if (post && post.likes > 0) {
            post.likes -= 1;
            this.notify();
        }
    },

    bookmarkPost(postId) {
        const post = this.feedPosts.find(p => p.id === postId);
        if (post) {
            post.bookmarked = !post.bookmarked;
            if (post.bookmarked && !this.currentUser.savedPostIds.includes(postId)) {
                this.currentUser.savedPostIds.push(postId);
            } else if (!post.bookmarked) {
                this.currentUser.savedPostIds = this.currentUser.savedPostIds.filter(id => id !== postId);
            }
            this.notify();
        }
    },

    addComment(postId, text, isAnonymous) {
        if (!text || !text.trim()) return;
        const post = this.feedPosts.find(p => p.id === postId);
        if (post) {
            const commentId = 'cmt_' + String(this._nextCommentId++);
            post.comments.push({
                id: commentId,
                authorName: isAnonymous ? 'Anonymous Student' : this.currentUser.fullName,
                authorSchool: this.currentUser.school,
                authorAvatarColor: isAnonymous ? '#95A5A6' : this.currentUser.avatarColor,
                text: text.trim(),
                createdAt: new Date().toISOString(),
                isAnonymous: !!isAnonymous
            });
            this.notify();
        }
    },

    setPostAudience(postId, audience) {
        const post = this.feedPosts.find(p => p.id === postId);
        if (post && post.authorId === this.currentUser.id) {
            post.audience = audience;
            this.notify();
        }
    },

    // ============================================================
    // EMPLOYER MUTATIONS
    // ============================================================
    followEmployer(employerId) {
        if (!this.currentUser.followedEmployerIds.includes(employerId)) {
            this.currentUser.followedEmployerIds.push(employerId);
            const emp = this.employers.find(e => e.id === employerId);
            if (emp) emp.followCount = (emp.followCount || 0) + 1;
            this.notify();
        }
    },

    unfollowEmployer(employerId) {
        this.currentUser.followedEmployerIds = this.currentUser.followedEmployerIds.filter(id => id !== employerId);
        const emp = this.employers.find(e => e.id === employerId);
        if (emp && emp.followCount > 0) emp.followCount -= 1;
        this.notify();
    },

    // ============================================================
    // JOB MUTATIONS
    // ============================================================
    saveJob(jobId) {
        if (!this.currentUser.savedJobIds.includes(jobId)) {
            this.currentUser.savedJobIds.push(jobId);
            this.notify();
        }
    },

    unsaveJob(jobId) {
        this.currentUser.savedJobIds = this.currentUser.savedJobIds.filter(id => id !== jobId);
        this.notify();
    },

    // ============================================================
    // CAREER INTERESTS MUTATIONS
    // ============================================================
    updateCareerInterests(interests) {
        this.currentUser.careerInterests = { ...this.currentUser.careerInterests, ...interests };
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    updateLookingFor(value) {
        this.currentUser.lookingFor = value;
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    addCareerInterestRole(role) {
        if (role && !this.currentUser.careerInterests.roles.includes(role)) {
            this.currentUser.careerInterests.roles.push(role);
            this.currentUser.updatedAt = new Date().toISOString();
            this.notify();
        }
    },

    removeCareerInterestRole(role) {
        this.currentUser.careerInterests.roles = this.currentUser.careerInterests.roles.filter(r => r !== role);
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    addCareerInterestLocation(location) {
        if (location && !this.currentUser.careerInterests.locations.includes(location)) {
            this.currentUser.careerInterests.locations.push(location);
            this.currentUser.updatedAt = new Date().toISOString();
            this.notify();
        }
    },

    removeCareerInterestLocation(location) {
        this.currentUser.careerInterests.locations = this.currentUser.careerInterests.locations.filter(l => l !== location);
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    toggleCareerInterestJobType(jobType) {
        const arr = this.currentUser.careerInterests.jobTypes;
        const idx = arr.indexOf(jobType);
        if (idx >= 0) arr.splice(idx, 1);
        else arr.push(jobType);
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    toggleCareerInterestHelpWith(item) {
        const arr = this.currentUser.careerInterests.helpWith;
        const idx = arr.indexOf(item);
        if (idx >= 0) arr.splice(idx, 1);
        else arr.push(item);
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    toggleCareerInterestPostGrad(item) {
        const arr = this.currentUser.careerInterests.postGraduation;
        const idx = arr.indexOf(item);
        if (idx >= 0) arr.splice(idx, 1);
        else arr.push(item);
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    toggleCareerInterestIndustry(industry) {
        const arr = this.currentUser.careerInterests.industries;
        const idx = arr.indexOf(industry);
        if (idx >= 0) arr.splice(idx, 1);
        else arr.push(industry);
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    toggleCareerInterestJobFunction(fn) {
        const arr = this.currentUser.careerInterests.jobFunctions;
        const idx = arr.indexOf(fn);
        if (idx >= 0) arr.splice(idx, 1);
        else arr.push(fn);
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    setCareerCommunity(community) {
        this.currentUser.careerInterests.careerCommunity = community;
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    setExpectedGraduation(date) {
        this.currentUser.careerInterests.expectedGraduationDate = date;
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    // ============================================================
    // PROFILE MUTATIONS
    // ============================================================
    updateProfileField(field, value) {
        if (this.currentUser.hasOwnProperty(field)) {
            this.currentUser[field] = value;
            this.currentUser.updatedAt = new Date().toISOString();
            this.notify();
        }
    },

    setProfileVisibility(visibility) {
        this.currentUser.profileVisibility = visibility;
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    // ============================================================
    // APPOINTMENT MUTATIONS
    // ============================================================
    requestAppointment(data) {
        const id = 'appt_' + String(this._nextAppointmentId++).padStart(2, '0');
        this.appointments.push({
            id,
            category: data.category,
            type: data.type,
            staffId: data.staffId,
            staffName: data.staffName,
            date: data.date,
            time: data.time,
            duration: 30,
            medium: data.medium,
            location: data.medium === 'In Person' ? 'Career Center' : null,
            status: 'requested',
            details: data.details || '',
            comments: [],
            createdAt: new Date().toISOString()
        });
        this.notify();
        return id;
    },

    cancelAppointment(appointmentId) {
        const appt = this.appointments.find(a => a.id === appointmentId);
        if (appt && (appt.status === 'requested' || appt.status === 'approved')) {
            appt.status = 'cancelled';
            this.notify();
        }
    },

    addAppointmentComment(appointmentId, text) {
        if (!text || !text.trim()) return;
        const appt = this.appointments.find(a => a.id === appointmentId);
        if (appt) {
            appt.comments.push({
                author: this.currentUser.fullName,
                text: text.trim(),
                createdAt: new Date().toISOString()
            });
            this.notify();
        }
    },

    // ============================================================
    // Q&A MUTATIONS
    // ============================================================
    submitQuestion(questionText) {
        if (!questionText || !questionText.trim()) return;
        const id = 'qa_' + String(this._nextQuestionId++).padStart(2, '0');
        this.qaQuestions.unshift({
            id,
            authorName: this.currentUser.fullName,
            authorSchool: this.currentUser.school,
            authorMajor: this.currentUser.major,
            authorGradYear: this.currentUser.graduationYear,
            authorAvatarColor: this.currentUser.avatarColor,
            question: questionText.trim(),
            status: 'pending',
            createdAt: new Date().toISOString(),
            views: 0,
            answers: []
        });
        this.notify();
        return id;
    },

    submitAnswer(questionId, answerText, visibility) {
        if (!answerText || !answerText.trim()) return;
        const q = this.qaQuestions.find(q => q.id === questionId);
        if (q) {
            const id = 'ans_' + String(this._nextAnswerId++).padStart(2, '0');
            q.answers.push({
                id,
                authorName: visibility === 'semi-anonymous' ? 'Anonymous' : this.currentUser.fullName,
                authorSchool: this.currentUser.school,
                authorMajor: this.currentUser.major,
                authorGradYear: this.currentUser.graduationYear,
                authorAvatarColor: visibility === 'semi-anonymous' ? '#95A5A6' : this.currentUser.avatarColor,
                text: answerText.trim(),
                visibility: visibility || 'full',
                status: 'pending',
                createdAt: new Date().toISOString(),
                helpful: 0
            });
            this.notify();
            return id;
        }
    },

    markAnswerHelpful(questionId, answerId) {
        const q = this.qaQuestions.find(q => q.id === questionId);
        if (q) {
            const a = q.answers.find(a => a.id === answerId);
            if (a) {
                a.helpful = (a.helpful || 0) + 1;
                this.notify();
            }
        }
    },

    // ============================================================
    // MESSAGE MUTATIONS
    // ============================================================
    markMessageRead(messageId) {
        const msg = this.messages.find(m => m.id === messageId);
        if (msg && !msg.isRead) {
            msg.isRead = true;
            this.notify();
        }
    },

    markAllMessagesRead() {
        let changed = false;
        this.messages.forEach(m => {
            if (!m.isRead) { m.isRead = true; changed = true; }
        });
        if (changed) this.notify();
    },

    // ============================================================
    // EVENT MUTATIONS
    // ============================================================
    rsvpEvent(eventId) {
        const evt = this.events.find(e => e.id === eventId);
        if (evt) {
            if (!evt.rsvped) {
                evt.rsvped = true;
                evt.rsvpCount = (evt.rsvpCount || 0) + 1;
            }
            this.notify();
        }
    },

    cancelRsvp(eventId) {
        const evt = this.events.find(e => e.id === eventId);
        if (evt && evt.rsvped) {
            evt.rsvped = false;
            if (evt.rsvpCount > 0) evt.rsvpCount -= 1;
            this.notify();
        }
    },

    // ============================================================
    // COMPUTED GETTERS
    // ============================================================
    getFilteredFeedPosts() {
        let posts = [...this.feedPosts];
        switch (this.feedFilter) {
            case 'Employers':
                posts = posts.filter(p => p.authorType === 'employer');
                break;
            case 'Top Posts':
                posts = posts.filter(p => p.likes >= 200);
                break;
            case 'Intros':
                posts = posts.filter(p => p.content.toLowerCase().includes('intro') || p.content.toLowerCase().includes('introduction') || p.content.toLowerCase().includes('hi everyone'));
                break;
        }
        return posts;
    },

    getSavedPosts() {
        return this.feedPosts.filter(p => p.bookmarked).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    },

    getFilteredJobs() {
        let jobs = [...this.jobs];
        if (this.jobSearchQuery) {
            const q = this.jobSearchQuery.toLowerCase();
            jobs = jobs.filter(j => j.title.toLowerCase().includes(q) || j.description.toLowerCase().includes(q) ||
                this.employers.find(e => e.id === j.employerId)?.name.toLowerCase().includes(q));
        }
        if (this.jobFilters.type) {
            jobs = jobs.filter(j => j.type === this.jobFilters.type);
        }
        if (this.jobFilters.location) {
            jobs = jobs.filter(j => j.location.includes(this.jobFilters.location));
        }
        if (this.jobFilters.label) {
            jobs = jobs.filter(j => j.labels && j.labels.includes(this.jobFilters.label));
        }
        if (this.jobFilters.role) {
            jobs = jobs.filter(j => j.roles && j.roles.includes(this.jobFilters.role));
        }
        return jobs;
    },

    getFilteredEmployers() {
        if (!this.employerSearchQuery) return [...this.employers];
        const q = this.employerSearchQuery.toLowerCase();
        return this.employers.filter(e => e.name.toLowerCase().includes(q) || e.industry.toLowerCase().includes(q) || e.location.toLowerCase().includes(q));
    },

    getFilteredEvents() {
        let events = [...this.events];
        if (this.eventSearchQuery) {
            const q = this.eventSearchQuery.toLowerCase();
            events = events.filter(e => e.title.toLowerCase().includes(q) || e.employerName.toLowerCase().includes(q) || e.description.toLowerCase().includes(q));
        }
        if (this.eventTypeFilter && this.eventTypeFilter !== 'All Types') {
            events = events.filter(e => e.type === this.eventTypeFilter);
        }
        if (this.eventShowVirtualOnly) {
            events = events.filter(e => e.isVirtual);
        }
        return events;
    },

    getFilteredMessages() {
        let msgs = [...this.messages];
        switch (this.messageFilter) {
            case 'unread':
                msgs = msgs.filter(m => !m.isRead);
                break;
            case 'top-match':
                msgs = msgs.filter(m => m.isTopMatch);
                break;
        }
        return msgs.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    },

    getUnreadMessageCount() {
        return this.messages.filter(m => !m.isRead).length;
    },

    getUpcomingAppointments() {
        return this.appointments.filter(a => a.status === 'requested' || a.status === 'approved')
            .sort((a, b) => new Date(a.date) - new Date(b.date));
    },

    getPastAppointments() {
        return this.appointments.filter(a => a.status === 'completed' || a.status === 'declined' || a.status === 'cancelled')
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    getEmployerById(id) {
        return this.employers.find(e => e.id === id);
    },

    getJobById(id) {
        return this.jobs.find(j => j.id === id);
    },

    getJobsByEmployer(employerId) {
        return this.jobs.filter(j => j.employerId === employerId && j.status === 'active');
    },

    getEventsByEmployer(employerId) {
        return this.events.filter(e => e.employerId === employerId && e.status === 'upcoming');
    },

    getPostsByEmployer(employerId) {
        return this.feedPosts.filter(p => p.authorType === 'employer' && p.authorId === employerId);
    }
};
