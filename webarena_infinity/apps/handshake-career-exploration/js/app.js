const App = {
    _sseConnection: null,
    _openDropdownId: null,

    // ============================================================
    // ROUTING
    // ============================================================
    parseRoute() {
        const hash = window.location.hash || '#/feed';
        const parts = hash.replace('#/', '').split('/');
        const page = parts[0] || 'feed';
        const validPages = ['feed', 'jobs', 'employers', 'events', 'messages', 'career-center', 'qa', 'profile', 'career-interests'];

        if (validPages.includes(page)) {
            AppState.currentPage = page;
        } else if (page === 'employer' && parts[1]) {
            AppState.currentPage = 'employer-detail';
            AppState.selectedEmployerId = parts[1];
            AppState.selectedEmployerTab = 'overview';
        } else if (page === 'job' && parts[1]) {
            AppState.currentPage = 'job-detail';
            AppState.selectedJobId = parts[1];
        } else if (page === 'event' && parts[1]) {
            AppState.currentPage = 'event-detail';
            AppState.selectedEventId = parts[1];
        } else if (page === 'message' && parts[1]) {
            AppState.currentPage = 'message-detail';
            AppState.selectedMessageId = parts[1];
        } else if (page === 'appointment' && parts[1]) {
            AppState.currentPage = 'appointment-detail';
            AppState.selectedAppointmentId = parts[1];
        } else if (page === 'schedule-appointment') {
            AppState.currentPage = 'schedule-appointment';
        } else if (page === 'question' && parts[1]) {
            AppState.currentPage = 'question-detail';
            AppState.selectedQuestionId = parts[1];
        } else {
            AppState.currentPage = 'feed';
        }
    },

    navigate(page, id) {
        if (id) {
            window.location.hash = `#/${page}/${id}`;
        } else {
            window.location.hash = `#/${page}`;
        }
    },

    // ============================================================
    // RENDERING
    // ============================================================
    render() {
        const sidebar = document.getElementById('sidebarNav');
        if (sidebar) sidebar.innerHTML = Views.renderSidebar();

        const content = document.getElementById('mainContent');
        if (content) content.innerHTML = Views.renderContent();

        const modalContainer = document.getElementById('modalContainer');
        if (modalContainer) modalContainer.innerHTML = Views.renderModal();

        const toast = document.getElementById('toast');
        if (toast) toast.innerHTML = Views.renderToast();

        // Focus modal inputs
        if (AppState.activeModal) {
            setTimeout(() => {
                const input = document.querySelector('.modal-input, .modal .form-input, .modal .form-textarea');
                if (input) input.focus();
            }, 50);
        }

        // Restore scroll position for detail pages
        if (AppState.currentPage.includes('detail') || AppState.currentPage === 'schedule-appointment' || AppState.currentPage === 'career-interests') {
            window.scrollTo(0, 0);
        }
    },

    // ============================================================
    // EVENT DELEGATION
    // ============================================================
    handleClick(e) {
        const target = e.target;

        // Close dropdowns on outside click
        if (this._openDropdownId && !target.closest('.custom-dropdown')) {
            this._closeAllDropdowns();
        }

        // ---- Data-action based dispatch ----
        const actionEl = target.closest('[data-action]');
        if (actionEl) {
            const action = actionEl.dataset.action;

            switch (action) {
                // Navigation
                case 'navigate':
                    e.preventDefault();
                    e.stopPropagation();
                    this.navigate(actionEl.dataset.page);
                    break;

                // Feed
                case 'setFeedFilter':
                    AppState.feedFilter = actionEl.dataset.value;
                    this.render();
                    break;
                case 'setFeedTab':
                    AppState.feedTab = actionEl.dataset.tab;
                    this.render();
                    break;
                case 'openCreatePost':
                    AppState.activeModal = 'createPost';
                    this.render();
                    break;
                case 'confirmCreatePost':
                    this._handleCreatePost();
                    break;
                case 'likePost':
                    e.stopPropagation();
                    AppState.likePost(actionEl.dataset.postId);
                    this.render();
                    break;
                case 'bookmarkPost':
                    e.stopPropagation();
                    AppState.bookmarkPost(actionEl.dataset.postId);
                    this.render();
                    break;
                case 'openComments':
                    e.stopPropagation();
                    AppState.activeModal = 'comments';
                    AppState.modalData = { postId: actionEl.dataset.postId };
                    this.render();
                    break;
                case 'confirmAddComment':
                    this._handleAddComment(actionEl.dataset.postId);
                    break;

                // Jobs
                case 'viewJob':
                    e.stopPropagation();
                    this.navigate('job', actionEl.dataset.jobId);
                    break;
                case 'saveJob':
                    e.stopPropagation();
                    AppState.saveJob(actionEl.dataset.jobId);
                    AppState.showToast('Job saved');
                    this.render();
                    break;
                case 'unsaveJob':
                    e.stopPropagation();
                    AppState.unsaveJob(actionEl.dataset.jobId);
                    AppState.showToast('Job unsaved');
                    this.render();
                    break;

                // Employers
                case 'viewEmployer':
                    e.stopPropagation();
                    this.navigate('employer', actionEl.dataset.employerId);
                    break;
                case 'followEmployer':
                    e.stopPropagation();
                    AppState.followEmployer(actionEl.dataset.employerId);
                    AppState.showToast('Following employer');
                    this.render();
                    break;
                case 'unfollowEmployer':
                    e.stopPropagation();
                    AppState.unfollowEmployer(actionEl.dataset.employerId);
                    AppState.showToast('Unfollowed employer');
                    this.render();
                    break;
                case 'setEmployerTab':
                    AppState.selectedEmployerTab = actionEl.dataset.tab;
                    this.render();
                    break;

                // Events
                case 'viewEvent':
                    e.stopPropagation();
                    this.navigate('event', actionEl.dataset.eventId);
                    break;
                case 'rsvpEvent':
                    e.stopPropagation();
                    AppState.rsvpEvent(actionEl.dataset.eventId);
                    AppState.showToast('RSVP confirmed');
                    this.render();
                    break;
                case 'cancelRsvp':
                    e.stopPropagation();
                    AppState.cancelRsvp(actionEl.dataset.eventId);
                    AppState.showToast('RSVP cancelled');
                    this.render();
                    break;

                // Messages
                case 'viewMessage':
                    AppState.markMessageRead(actionEl.dataset.messageId);
                    this.navigate('message', actionEl.dataset.messageId);
                    break;
                case 'markAllRead':
                    AppState.markAllMessagesRead();
                    AppState.showToast('All messages marked as read');
                    this.render();
                    break;
                case 'setMessageFilter':
                    AppState.messageFilter = actionEl.dataset.tab;
                    this.render();
                    break;

                // Appointments
                case 'viewAppointment':
                    this.navigate('appointment', actionEl.dataset.appointmentId);
                    break;
                case 'cancelAppointment':
                    AppState.cancelAppointment(actionEl.dataset.appointmentId);
                    AppState.showToast('Appointment cancelled');
                    this.render();
                    break;
                case 'addAppointmentComment':
                    this._handleAddAppointmentComment(actionEl.dataset.appointmentId);
                    break;
                case 'selectAppointmentDate':
                    AppState.appointmentScheduling.date = actionEl.dataset.date;
                    AppState.appointmentScheduling.time = null;
                    this.render();
                    break;
                case 'selectAppointmentTime':
                    AppState.appointmentScheduling.time = actionEl.dataset.time;
                    this.render();
                    break;
                case 'submitAppointment':
                    this._handleSubmitAppointment();
                    break;

                // Q&A
                case 'viewQuestion':
                    this.navigate('question', actionEl.dataset.questionId);
                    break;
                case 'setQATab':
                    AppState.qaTab = actionEl.dataset.tab;
                    this.render();
                    break;
                case 'submitQuestion':
                    this._handleSubmitQuestion();
                    break;
                case 'submitAnswer':
                    this._handleSubmitAnswer(actionEl.dataset.questionId);
                    break;
                case 'markHelpful':
                    AppState.markAnswerHelpful(actionEl.dataset.questionId, actionEl.dataset.answerId);
                    this.render();
                    break;

                // Profile
                case 'editProfileField':
                    AppState.activeModal = 'editProfile';
                    AppState.modalData = { field: actionEl.dataset.field };
                    this.render();
                    break;
                case 'confirmEditProfile':
                    this._handleEditProfile(actionEl.dataset.field);
                    break;

                // Career Interests
                case 'removeRole':
                    AppState.removeCareerInterestRole(actionEl.dataset.value);
                    this.render();
                    break;
                case 'removeLocation':
                    AppState.removeCareerInterestLocation(actionEl.dataset.value);
                    this.render();
                    break;
                case 'saveCareerInterests':
                    AppState.showToast('Career interests saved!');
                    this.navigate('profile');
                    break;

                // Modal
                case 'closeModal':
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    this.render();
                    break;

                default:
                    break;
            }
            return;
        }

        // ---- Dropdown trigger ----
        const dropdownTrigger = target.closest('.dropdown-trigger');
        if (dropdownTrigger) {
            const ddId = dropdownTrigger.dataset.dropdownId;
            this._toggleDropdown(ddId);
            return;
        }

        // ---- Dropdown item selection ----
        const dropdownItem = target.closest('.dropdown-item');
        if (dropdownItem) {
            const ddId = dropdownItem.dataset.dropdownId;
            const value = dropdownItem.dataset.value;
            this._selectDropdownValue(ddId, value);
            return;
        }

        // ---- Checkbox toggle ----
        const checkboxRow = target.closest('[data-checkbox-id]');
        if (checkboxRow) {
            const cbId = checkboxRow.dataset.checkboxId;
            this._handleCheckbox(cbId);
            return;
        }

        // ---- Toggle switch ----
        const toggleSwitch = target.closest('.toggle-switch');
        if (toggleSwitch) {
            const toggleId = toggleSwitch.dataset.toggleId;
            this._handleToggle(toggleId);
            return;
        }

        // ---- Modal overlay click ----
        if (target.classList.contains('modal-overlay')) {
            AppState.activeModal = null;
            AppState.modalData = null;
            this.render();
            return;
        }
    },

    handleKeydown(e) {
        if (e.key === 'Enter' && !e.shiftKey && AppState.activeModal) {
            const confirmBtn = document.querySelector('.modal-footer .btn-primary');
            if (confirmBtn && !confirmBtn.disabled) {
                confirmBtn.click();
            }
        }
        if (e.key === 'Escape') {
            if (AppState.activeModal) {
                AppState.activeModal = null;
                AppState.modalData = null;
                this.render();
            } else if (this._openDropdownId) {
                this._closeAllDropdowns();
            }
        }
    },

    handleInput(e) {
        const target = e.target;

        // Search inputs
        if (target.id === 'jobSearch') {
            AppState.jobSearchQuery = target.value;
            this._debounceRender();
        } else if (target.id === 'employerSearch') {
            AppState.employerSearchQuery = target.value;
            this._debounceRender();
        } else if (target.id === 'eventSearch') {
            AppState.eventSearchQuery = target.value;
            this._debounceRender();
        } else if (target.id === 'qaSearch') {
            AppState.qaSearchQuery = target.value;
            this._debounceRender();
        }

        // Create post character count
        if (target.id === 'newPostContent') {
            const count = target.value.length;
            const countEl = document.getElementById('charCount');
            if (countEl) countEl.textContent = count;
            const btn = document.getElementById('postSubmitBtn');
            if (btn) btn.disabled = count === 0 || count > 3000;
        }

        // Schedule appointment details
        if (target.id === 'schedDetails') {
            AppState.appointmentScheduling.details = target.value;
        }
    },

    // ============================================================
    // DROPDOWN HELPERS
    // ============================================================
    _toggleDropdown(ddId) {
        const dd = document.getElementById(ddId);
        if (!dd) return;
        const menu = dd.querySelector('.dropdown-menu');
        if (this._openDropdownId === ddId) {
            this._closeAllDropdowns();
        } else {
            this._closeAllDropdowns();
            menu.classList.add('open');
            dd.classList.add('open');
            this._openDropdownId = ddId;
        }
    },

    _closeAllDropdowns() {
        document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
        document.querySelectorAll('.custom-dropdown.open').forEach(d => d.classList.remove('open'));
        this._openDropdownId = null;
    },

    _selectDropdownValue(ddId, value) {
        this._closeAllDropdowns();

        // Job filters
        if (ddId === 'jobTypeFilter') {
            AppState.jobFilters.type = value;
            this.render();
            return;
        }
        if (ddId === 'jobLocationFilter') {
            AppState.jobFilters.location = value;
            this.render();
            return;
        }
        if (ddId === 'jobLabelFilter') {
            AppState.jobFilters.label = value;
            this.render();
            return;
        }

        // Event type filter
        if (ddId === 'eventTypeFilter') {
            AppState.eventTypeFilter = value;
            this.render();
            return;
        }

        // Profile visibility
        if (ddId === 'profileVisibility') {
            AppState.setProfileVisibility(value);
            this.render();
            return;
        }

        // Career interests dropdowns
        if (ddId === 'addRoleDropdown' && value) {
            AppState.addCareerInterestRole(value);
            this.render();
            return;
        }
        if (ddId === 'addLocationDropdown' && value) {
            AppState.addCareerInterestLocation(value);
            this.render();
            return;
        }
        if (ddId === 'careerCommunity') {
            AppState.setCareerCommunity(value);
            this.render();
            return;
        }
        if (ddId === 'expectedGradDate') {
            AppState.setExpectedGraduation(value);
            this.render();
            return;
        }

        // Appointment scheduling
        if (ddId === 'schedCategory') {
            AppState.appointmentScheduling.category = value;
            AppState.appointmentScheduling.type = null;
            AppState.appointmentScheduling.date = null;
            AppState.appointmentScheduling.time = null;
            this.render();
            return;
        }
        if (ddId === 'schedType') {
            AppState.appointmentScheduling.type = value;
            this.render();
            return;
        }
        if (ddId === 'schedStaff') {
            AppState.appointmentScheduling.staff = value || null;
            AppState.appointmentScheduling.date = null;
            AppState.appointmentScheduling.time = null;
            this.render();
            return;
        }
        if (ddId === 'schedMedium') {
            AppState.appointmentScheduling.medium = value;
            this.render();
            return;
        }

        // Post audience in create modal
        if (ddId === 'postAudience') {
            AppState.newPostAudience = value;
            this.render();
            return;
        }
    },

    // ============================================================
    // CHECKBOX HELPER
    // ============================================================
    _handleCheckbox(cbId) {
        // Career interest checkboxes
        if (cbId.startsWith('jobType-')) {
            const val = cbId.replace('jobType-', '').replace(/-/g, ' ');
            const match = JOB_TYPE_OPTIONS.find(o => o.replace(/\s/g, '-') === cbId.replace('jobType-', ''));
            if (match) AppState.toggleCareerInterestJobType(match);
            this.render();
            return;
        }
        if (cbId.startsWith('helpWith-')) {
            const match = HELP_WITH_OPTIONS.find(o => o.replace(/\s/g, '-') === cbId.replace('helpWith-', ''));
            if (match) AppState.toggleCareerInterestHelpWith(match);
            this.render();
            return;
        }
        if (cbId.startsWith('postGrad-')) {
            const match = POST_GRADUATION_OPTIONS.find(o => o.replace(/\s/g, '-') === cbId.replace('postGrad-', ''));
            if (match) AppState.toggleCareerInterestPostGrad(match);
            this.render();
            return;
        }
        if (cbId.startsWith('industry-')) {
            const match = INDUSTRY_OPTIONS.find(o => o.replace(/[\s&]/g, '-') === cbId.replace('industry-', ''));
            if (match) AppState.toggleCareerInterestIndustry(match);
            this.render();
            return;
        }
        if (cbId.startsWith('jobFunction-')) {
            const match = JOB_FUNCTION_OPTIONS.find(o => o.replace(/[\s&]/g, '-') === cbId.replace('jobFunction-', ''));
            if (match) AppState.toggleCareerInterestJobFunction(match);
            this.render();
            return;
        }
        if (cbId === 'virtualOnly') {
            AppState.eventShowVirtualOnly = !AppState.eventShowVirtualOnly;
            this.render();
            return;
        }
        if (cbId === 'anonymousComment') {
            const el = document.getElementById(cbId);
            if (el) {
                el.classList.toggle('checked');
            }
            return;
        }
    },

    _handleToggle(toggleId) {
        // No toggles currently, placeholder
    },

    // ============================================================
    // ACTION HANDLERS
    // ============================================================
    _handleCreatePost() {
        const textarea = document.getElementById('newPostContent');
        if (!textarea || !textarea.value.trim()) return;
        const audience = AppState.newPostAudience === 'People at your school' ? 'school' : 'everyone';
        AppState.createPost(textarea.value, audience);
        AppState.activeModal = null;
        AppState.newPostAudience = 'Everyone on Handshake';
        AppState.showToast('Post shared!');
        this.render();
    },

    _handleAddComment(postId) {
        const textarea = document.getElementById('newCommentText');
        if (!textarea || !textarea.value.trim()) return;
        const anonCheckbox = document.getElementById('anonymousComment');
        const isAnonymous = anonCheckbox && anonCheckbox.classList.contains('checked');
        AppState.addComment(postId, textarea.value, isAnonymous);
        AppState.showToast('Comment posted');
        this.render();
    },

    _handleAddAppointmentComment(appointmentId) {
        const textarea = document.getElementById('appointmentComment');
        if (!textarea || !textarea.value.trim()) return;
        AppState.addAppointmentComment(appointmentId, textarea.value);
        AppState.showToast('Comment posted');
        this.render();
    },

    _handleSubmitAppointment() {
        const sched = AppState.appointmentScheduling;
        if (!sched.category || !sched.type || !sched.date || !sched.time || !sched.medium) return;

        const staffObj = sched.staff ? AppState.appointmentStaff.find(s => s.name === sched.staff) : AppState.appointmentStaff[0];

        AppState.requestAppointment({
            category: sched.category,
            type: sched.type,
            staffId: staffObj ? staffObj.id : 'staff_01',
            staffName: staffObj ? staffObj.name : 'Career Advisor',
            date: sched.date,
            time: sched.time,
            medium: sched.medium,
            details: sched.details
        });

        // Reset scheduling state
        AppState.appointmentScheduling = { category: null, type: null, staff: null, date: null, time: null, medium: null, details: '' };
        AppState.showToast('Appointment requested!');
        this.navigate('career-center');
    },

    _handleSubmitQuestion() {
        const textarea = document.getElementById('newQuestion');
        if (!textarea || !textarea.value.trim()) return;
        AppState.submitQuestion(textarea.value);
        AppState.showToast('Question submitted! It will be reviewed before appearing.');
        this.render();
    },

    _handleSubmitAnswer(questionId) {
        const textarea = document.getElementById('answerText');
        if (!textarea || !textarea.value.trim()) return;
        const visibilityEl = document.querySelector('input[name="answerVisibility"]:checked');
        const visibility = visibilityEl ? visibilityEl.value : 'full';
        AppState.submitAnswer(questionId, textarea.value, visibility);
        AppState.showToast('Answer submitted! It will be reviewed before appearing.');
        this.render();
    },

    _handleEditProfile(field) {
        const input = document.getElementById('editProfileInput');
        if (!input) return;
        AppState.updateProfileField(field, input.value.trim());
        AppState.activeModal = null;
        AppState.modalData = null;
        AppState.showToast('Profile updated');
        this.render();
    },

    // ============================================================
    // DEBOUNCE
    // ============================================================
    _debounceTimer: null,
    _debounceRender() {
        clearTimeout(this._debounceTimer);
        this._debounceTimer = setTimeout(() => this.render(), 200);
    },

    // ============================================================
    // SSE
    // ============================================================
    _initSSE() {
        this._sseConnection = new EventSource('/api/events');
        this._sseConnection.onmessage = (e) => {
            if (e.data === 'reset') {
                AppState.resetToSeedData();
                window.location.hash = '#/feed';
                this.render();
            }
        };
    },

    // ============================================================
    // INITIALIZATION
    // ============================================================
    init() {
        AppState.init();
        AppState.subscribe(() => this.render());

        this.parseRoute();
        this.render();

        AppState._pushStateToServer();

        document.addEventListener('click', (e) => this.handleClick(e));
        document.addEventListener('keydown', (e) => this.handleKeydown(e));
        document.addEventListener('input', (e) => this.handleInput(e));

        window.addEventListener('hashchange', () => {
            this.parseRoute();
            this.render();
        });

        this._initSSE();
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
