// ============================================================
// app.js — Routing, event delegation, and initialization
// ============================================================

const App = {
    _sseConnection: null,
    _openDropdownId: null,
    _expandedChannels: new Set(),

    // ============================================================
    // Router
    // ============================================================

    parseRoute() {
        const hash = window.location.hash || '#/profile';
        const section = hash.replace('#/', '') || 'profile';
        const valid = ['profile', 'preferences', 'notifications', 'security'];
        AppState.currentSection = valid.includes(section) ? section : 'profile';
    },

    navigate(section) {
        window.location.hash = '#/' + section;
    },

    // ============================================================
    // Render
    // ============================================================

    render() {
        const sidebar = document.getElementById('sidebarNav');
        if (sidebar) sidebar.innerHTML = Views.renderSidebar();

        const content = document.getElementById('mainContent');
        if (content) content.innerHTML = Views.renderContent();

        const modalContainer = document.getElementById('modalContainer');
        if (modalContainer) modalContainer.innerHTML = Views.renderModal();

        // Re-expand notification channels that were open
        this._expandedChannels.forEach(channel => {
            const el = document.getElementById('channel-' + channel);
            if (el) {
                const body = el.querySelector('.channel-body');
                const arrow = el.querySelector('.channel-expand-arrow');
                if (body) body.style.display = 'block';
                if (arrow) arrow.classList.add('rotated');
            }
        });

        // Focus modal inputs
        if (AppState.activeModal) {
            setTimeout(() => {
                const input = document.querySelector('.modal-input');
                if (input) input.focus();
            }, 50);
        }
    },

    // ============================================================
    // Event Handlers
    // ============================================================

    handleClick(e) {
        const target = e.target;

        // Close dropdowns on outside click
        if (this._openDropdownId && !target.closest('.custom-dropdown')) {
            this._closeAllDropdowns();
        }

        // ---- Data-action based routing ----
        const actionEl = target.closest('[data-action]');
        if (actionEl) {
            const action = actionEl.dataset.action;
            e.preventDefault();
            e.stopPropagation();

            switch (action) {
                case 'navigate':
                    this.navigate(actionEl.dataset.section);
                    break;

                // Profile
                case 'editFullName':
                    AppState.activeModal = 'editFullName';
                    this.render();
                    break;
                case 'editUsername':
                    AppState.activeModal = 'editUsername';
                    this.render();
                    break;
                case 'editEmail':
                    AppState.activeModal = 'editEmail';
                    this.render();
                    break;
                case 'changeAvatar':
                    this._cycleAvatarColor();
                    break;
                case 'disconnectAccount':
                    const accId = actionEl.dataset.accountId;
                    const acc = AppState.connectedAccounts.find(a => a.id === accId);
                    AppState.modalData = acc;
                    AppState.activeModal = 'disconnectAccount';
                    this.render();
                    break;
                case 'leaveWorkspace':
                    const wsId = actionEl.dataset.workspaceId;
                    const ws = AppState.workspaces.find(w => w.id === wsId);
                    AppState.modalData = ws;
                    AppState.activeModal = 'leaveWorkspace';
                    this.render();
                    break;

                // Notifications
                case 'toggleChannelExpand':
                    this._toggleChannelExpand(actionEl.dataset.channel);
                    break;

                // Security
                case 'toggleSessionDetails':
                    const sessId = actionEl.dataset.sessionId;
                    AppState.expandedSessionId = AppState.expandedSessionId === sessId ? null : sessId;
                    this.render();
                    break;
                case 'revokeSession':
                    e.stopPropagation();
                    const rSessId = actionEl.dataset.sessionId;
                    const rSess = AppState.sessions.find(s => s.id === rSessId);
                    AppState.modalData = rSess;
                    AppState.activeModal = 'revokeSession';
                    this.render();
                    break;
                case 'revokeAllSessions':
                    AppState.activeModal = 'revokeAllSessions';
                    this.render();
                    break;
                case 'addPasskey':
                    AppState.activeModal = 'addPasskey';
                    this.render();
                    break;
                case 'deletePasskey':
                    const pkId = actionEl.dataset.passkeyId;
                    const pk = AppState.passkeys.find(p => p.id === pkId);
                    AppState.modalData = pk;
                    AppState.activeModal = 'deletePasskey';
                    this.render();
                    break;
                case 'createApiKey':
                    AppState.activeModal = 'createApiKey';
                    this.render();
                    break;
                case 'revokeApiKey':
                    const keyId = actionEl.dataset.keyId;
                    const key = AppState.apiKeys.find(k => k.id === keyId);
                    AppState.modalData = key;
                    AppState.activeModal = 'revokeApiKey';
                    this.render();
                    break;
                case 'revokeApp':
                    const appId = actionEl.dataset.appId;
                    const oauthApp = AppState.authorizedApps.find(a => a.id === appId);
                    AppState.modalData = oauthApp;
                    AppState.activeModal = 'revokeApp';
                    this.render();
                    break;

                // Modal actions
                case 'closeModal':
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    this.render();
                    break;
                case 'confirmEditField':
                    this._confirmEditField(actionEl.dataset.field);
                    break;
                case 'confirmEditEmail':
                    this._confirmEditEmail();
                    break;
                case 'confirmLeaveWorkspace':
                    AppState.leaveWorkspace(actionEl.dataset.workspaceId);
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    AppState.showToast('You have left the workspace.');
                    this.render();
                    break;
                case 'confirmRevokeSession':
                    AppState.revokeSession(actionEl.dataset.sessionId);
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    AppState.showToast('Session revoked.');
                    this.render();
                    break;
                case 'confirmRevokeAllSessions':
                    AppState.revokeAllSessions();
                    AppState.activeModal = null;
                    AppState.showToast('All other sessions revoked.');
                    this.render();
                    break;
                case 'confirmDeletePasskey':
                    AppState.deletePasskey(actionEl.dataset.passkeyId);
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    AppState.showToast('Passkey removed.');
                    this.render();
                    break;
                case 'confirmAddPasskey':
                    this._confirmAddPasskey();
                    break;
                case 'confirmCreateApiKey':
                    this._confirmCreateApiKey();
                    break;
                case 'confirmRevokeApiKey':
                    AppState.revokeApiKey(actionEl.dataset.keyId);
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    AppState.showToast('API key revoked.');
                    this.render();
                    break;
                case 'confirmRevokeApp':
                    AppState.revokeAuthorizedApp(actionEl.dataset.appId);
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    AppState.showToast('Application access revoked.');
                    this.render();
                    break;
                case 'confirmDisconnectAccount':
                    AppState.disconnectAccount(actionEl.dataset.accountId);
                    AppState.activeModal = null;
                    AppState.modalData = null;
                    AppState.showToast('Account disconnected.');
                    this.render();
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

        // ---- Dropdown item ----
        const dropdownItem = target.closest('.dropdown-item');
        if (dropdownItem) {
            const ddId = dropdownItem.dataset.dropdownId;
            const value = dropdownItem.dataset.value;
            this._selectDropdownValue(ddId, value);
            return;
        }

        // ---- Toggle switch ----
        const toggleSwitch = target.closest('.toggle-switch');
        if (toggleSwitch && !toggleSwitch.classList.contains('disabled')) {
            const toggleId = toggleSwitch.dataset.toggleId;
            this._handleToggle(toggleId, toggleSwitch);
            return;
        }

        // ---- Modal overlay click (close) ----
        if (target.classList.contains('modal-overlay')) {
            AppState.activeModal = null;
            AppState.modalData = null;
            this.render();
            return;
        }
    },

    handleKeydown(e) {
        // Enter in modal input → confirm
        if (e.key === 'Enter' && AppState.activeModal) {
            const confirmBtn = document.querySelector('.modal-footer .btn-primary, .modal-footer .btn-danger');
            if (confirmBtn && !confirmBtn.disabled) {
                confirmBtn.click();
            }
        }
        // Escape → close modal or dropdown
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
        // Email validation in modal
        if (e.target.id === 'modal-input-email') {
            const val = e.target.value.trim();
            const btn = document.getElementById('confirm-email-btn');
            const msg = document.getElementById('email-validation-msg');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!val) {
                if (btn) btn.disabled = true;
                if (msg) msg.textContent = '';
            } else if (!emailRegex.test(val)) {
                if (btn) btn.disabled = true;
                if (msg) { msg.textContent = 'Please enter a valid email address.'; msg.classList.add('error'); }
            } else if (val === AppState.currentUser.email) {
                if (btn) btn.disabled = true;
                if (msg) { msg.textContent = 'This is your current email address.'; msg.classList.add('error'); }
            } else {
                if (btn) btn.disabled = false;
                if (msg) { msg.textContent = ''; msg.classList.remove('error'); }
            }
        }
    },

    // ============================================================
    // Dropdown Helpers
    // ============================================================

    _toggleDropdown(ddId) {
        const dd = document.getElementById(ddId);
        if (!dd) return;
        const menu = dd.querySelector('.dropdown-menu');
        if (!menu) return;

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

        // Map dropdown IDs to preference keys
        const prefMap = {
            'pref-home-view': 'defaultHomeView',
            'pref-first-day': 'firstDayOfWeek',
            'pref-theme': 'interfaceTheme',
            'pref-font-size': 'fontSize',
            'pref-git-format': 'gitAttachmentFormat'
        };

        if (prefMap[ddId]) {
            AppState.updatePreference(prefMap[ddId], value);
        }

        this.render();
    },

    // ============================================================
    // Toggle Helpers
    // ============================================================

    _handleToggle(toggleId, el) {
        // Preferences toggles
        const prefToggleMap = {
            'pref-display-full-names': 'displayFullNames',
            'pref-convert-emojis': 'convertTextEmojis',
            'pref-pointer-cursor': 'usePointerCursor',
            'pref-open-desktop': 'openInDesktopApp',
            'pref-notif-badge': 'desktopNotificationBadge',
            'pref-spell-check': 'enableSpellCheck',
            'pref-auto-assign-create': 'autoAssignOnCreate',
            'pref-auto-assign-started': 'autoAssignOnStarted',
            'pref-git-move-started': 'onGitBranchCopyMoveToStarted',
            'pref-git-auto-assign': 'onGitBranchCopyAutoAssign'
        };

        if (prefToggleMap[toggleId]) {
            const key = prefToggleMap[toggleId];
            AppState.updatePreference(key, !AppState.preferences[key]);
            this.render();
            return;
        }

        // Notification channel enabled toggles
        const channelEnabledMatch = toggleId.match(/^notif-(desktop|mobile|email|slack)-enabled$/);
        if (channelEnabledMatch) {
            const channel = channelEnabledMatch[1];
            AppState.toggleNotificationChannel(channel);
            this.render();
            return;
        }

        // Notification type toggles
        const channelTypeMatch = toggleId.match(/^notif-(desktop|mobile|email|slack)-(.+)$/);
        if (channelTypeMatch) {
            const channel = channelTypeMatch[1];
            const key = channelTypeMatch[2];
            // Handle email-specific settings
            if (key === 'urgent') {
                AppState.updateNotificationChannel(channel, 'sendUrgentImmediately', !AppState.notificationSettings[channel].sendUrgentImmediately);
            } else if (key === 'delay-low') {
                AppState.updateNotificationChannel(channel, 'delayLowPriorityOutsideHours', !AppState.notificationSettings[channel].delayLowPriorityOutsideHours);
            } else {
                const notifKey = el.dataset.notifKey || key;
                const currentVal = AppState.notificationSettings[channel][notifKey];
                AppState.updateNotificationChannel(channel, notifKey, !currentVal);
            }
            this.render();
            return;
        }

        // Communication toggles
        const commToggleMap = {
            'notif-changelogs': 'receiveChangelogs',
            'notif-dpa': 'receiveDpaUpdates',
            'notif-product': 'receiveProductUpdates'
        };

        if (commToggleMap[toggleId]) {
            const key = commToggleMap[toggleId];
            AppState.updateNotificationComm(key, !AppState.notificationSettings[key]);
            this.render();
            return;
        }
    },

    // ============================================================
    // Notification Channel Expand
    // ============================================================

    _toggleChannelExpand(channel) {
        const el = document.getElementById('channel-' + channel);
        if (!el) return;
        const body = el.querySelector('.channel-body');
        const arrow = el.querySelector('.channel-expand-arrow');
        if (!body) return;

        if (body.style.display === 'none' || !body.style.display) {
            body.style.display = 'block';
            if (arrow) arrow.classList.add('rotated');
            this._expandedChannels.add(channel);
        } else {
            body.style.display = 'none';
            if (arrow) arrow.classList.remove('rotated');
            this._expandedChannels.delete(channel);
        }
    },

    // ============================================================
    // Modal Confirmations
    // ============================================================

    _confirmEditField(field) {
        const input = document.getElementById('modal-input-field');
        if (!input) return;
        const value = input.value.trim();
        if (!value) return;

        if (field === 'fullName') {
            AppState.updateUserFullName(value);
            AppState.showToast('Name updated.');
        } else if (field === 'username') {
            AppState.updateUserUsername(value);
            AppState.showToast('Username updated.');
        }
        AppState.activeModal = null;
        AppState.modalData = null;
        this.render();
    },

    _confirmEditEmail() {
        const input = document.getElementById('modal-input-email');
        if (!input) return;
        const value = input.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!value || !emailRegex.test(value)) return;

        AppState.updateUserEmail(value);
        AppState.activeModal = null;
        AppState.modalData = null;
        AppState.showToast('Email update confirmation sent to both addresses.');
        this.render();
    },

    _confirmAddPasskey() {
        const input = document.getElementById('modal-input-passkey-name');
        if (!input) return;
        const name = input.value.trim() || 'New Passkey';
        AppState.addPasskey(name);
        AppState.activeModal = null;
        AppState.modalData = null;
        AppState.showToast('Passkey registered.');
        this.render();
    },

    _confirmCreateApiKey() {
        const input = document.getElementById('modal-input-api-label');
        if (!input) return;
        const label = input.value.trim() || 'Untitled API Key';
        AppState.createApiKey(label);
        AppState.activeModal = null;
        AppState.modalData = null;
        AppState.showToast('API key created.');
        this.render();
    },

    // ============================================================
    // Avatar Color Cycling
    // ============================================================

    _cycleAvatarColor() {
        const colors = ['#5E6AD2', '#26B5CE', '#F2994A', '#EB5757', '#BB6BD9', '#2F80ED', '#27AE60', '#F2C94C'];
        const current = AppState.currentUser.avatarColor;
        const idx = colors.indexOf(current);
        const next = colors[(idx + 1) % colors.length];
        AppState.currentUser.avatarColor = next;
        AppState.currentUser.updatedAt = new Date().toISOString();
        AppState.notify();
        this.render();
    },

    // ============================================================
    // SSE
    // ============================================================

    _initSSE() {
        this._sseConnection = new EventSource('/api/events');
        this._sseConnection.onmessage = (e) => {
            if (e.data === 'reset') {
                AppState.resetToSeedData();
                this._expandedChannels.clear();
                window.location.hash = '#/profile';
                this.render();
            }
        };
    },

    // ============================================================
    // Init
    // ============================================================

    init() {
        AppState.init();

        // Subscribe to state changes
        AppState.subscribe(() => this.render());

        // Parse route and render
        this.parseRoute();
        this.render();

        // Push initial state to server
        AppState._pushStateToServer();

        // Event delegation
        document.addEventListener('click', (e) => this.handleClick(e));
        document.addEventListener('keydown', (e) => this.handleKeydown(e));
        document.addEventListener('input', (e) => this.handleInput(e));

        // Hash change
        window.addEventListener('hashchange', () => {
            this.parseRoute();
            this.render();
        });

        // SSE
        this._initSSE();
    }
};

// Boot
document.addEventListener('DOMContentLoaded', () => App.init());
