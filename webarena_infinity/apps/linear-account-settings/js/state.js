// ============================================================
// state.js — Centralized state management for Linear Account Settings
// ============================================================

const AppState = {
    // ---- Persistent State ----
    currentUser: null,
    workspaces: [],
    connectedAccounts: [],
    preferences: {},
    notificationSettings: {},
    sessions: [],
    passkeys: [],
    apiKeys: [],
    authorizedApps: [],

    // ---- ID Counters ----
    _nextApiKeyId: 10,
    _nextPasskeyId: 10,

    // ---- UI State (not persisted) ----
    currentSection: 'profile',    // profile | preferences | notifications | security
    activeModal: null,             // null | 'editEmail' | 'editName' | 'editUsername' | 'leaveWorkspace' | 'revokeSession' | 'revokeAllSessions' | 'deletePasskey' | 'createApiKey' | 'revokeApiKey' | 'revokeApp' | 'disconnectAccount' | 'sessionDetails' | 'changeAvatar'
    modalData: null,
    toastMessage: null,
    toastTimeout: null,
    expandedSessionId: null,

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
            this.currentUser = persisted.currentUser || null;
            this.workspaces = persisted.workspaces || [];
            this.connectedAccounts = persisted.connectedAccounts || [];
            this.preferences = persisted.preferences || {};
            this.notificationSettings = persisted.notificationSettings || {};
            this.sessions = persisted.sessions || [];
            this.passkeys = persisted.passkeys || [];
            this.apiKeys = persisted.apiKeys || [];
            this.authorizedApps = persisted.authorizedApps || [];
            this._nextApiKeyId = persisted._nextApiKeyId || 10;
            this._nextPasskeyId = persisted._nextPasskeyId || 10;
        } else {
            this._loadSeedData();
        }
    },

    _loadSeedData() {
        this.currentUser = JSON.parse(JSON.stringify(CURRENT_USER));
        this.workspaces = JSON.parse(JSON.stringify(WORKSPACES));
        this.connectedAccounts = JSON.parse(JSON.stringify(CONNECTED_ACCOUNTS));
        this.preferences = JSON.parse(JSON.stringify(PREFERENCES));
        this.notificationSettings = JSON.parse(JSON.stringify(NOTIFICATION_SETTINGS));
        this.sessions = JSON.parse(JSON.stringify(SESSIONS));
        this.passkeys = JSON.parse(JSON.stringify(PASSKEYS));
        this.apiKeys = JSON.parse(JSON.stringify(API_KEYS));
        this.authorizedApps = JSON.parse(JSON.stringify(AUTHORIZED_APPS));
        this._nextApiKeyId = 10;
        this._nextPasskeyId = 10;
    },

    _loadPersistedData() {
        try {
            const saved = localStorage.getItem('linearAccountSettingsState');
            if (!saved) return null;
            const parsed = JSON.parse(saved);
            if (parsed._seedVersion !== SEED_DATA_VERSION) {
                localStorage.removeItem('linearAccountSettingsState');
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
        localStorage.setItem('linearAccountSettingsState', JSON.stringify(state));
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
            workspaces: this.workspaces,
            connectedAccounts: this.connectedAccounts,
            preferences: this.preferences,
            notificationSettings: this.notificationSettings,
            sessions: this.sessions,
            passkeys: this.passkeys,
            apiKeys: this.apiKeys,
            authorizedApps: this.authorizedApps,
            _nextApiKeyId: this._nextApiKeyId,
            _nextPasskeyId: this._nextPasskeyId
        };
    },

    resetToSeedData() {
        localStorage.removeItem('linearAccountSettingsState');
        this._loadSeedData();
        this.currentSection = 'profile';
        this.activeModal = null;
        this.modalData = null;
        this.notify();
    },

    // ---- Profile Mutations ----

    updateUserFullName(name) {
        if (!name || !name.trim()) return;
        this.currentUser.fullName = name.trim();
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    updateUserUsername(username) {
        if (!username || !username.trim()) return;
        this.currentUser.username = username.trim();
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    updateUserEmail(email) {
        if (!email || !email.trim()) return;
        this.currentUser.email = email.trim();
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    updateUserAvatar(avatarUrl) {
        this.currentUser.avatarUrl = avatarUrl;
        this.currentUser.updatedAt = new Date().toISOString();
        this.notify();
    },

    // ---- Workspace Mutations ----

    leaveWorkspace(workspaceId) {
        this.workspaces = this.workspaces.filter(w => w.id !== workspaceId);
        this.notify();
    },

    // ---- Connected Account Mutations ----

    disconnectAccount(accountId) {
        this.connectedAccounts = this.connectedAccounts.filter(a => a.id !== accountId);
        this.notify();
    },

    // ---- Preferences Mutations ----

    updatePreference(key, value) {
        this.preferences[key] = value;
        this.notify();
    },

    // ---- Notification Mutations ----

    updateNotificationChannel(channel, key, value) {
        if (this.notificationSettings[channel]) {
            this.notificationSettings[channel][key] = value;
        }
        this.notify();
    },

    toggleNotificationChannel(channel) {
        if (this.notificationSettings[channel]) {
            this.notificationSettings[channel].enabled = !this.notificationSettings[channel].enabled;
        }
        this.notify();
    },

    updateNotificationComm(key, value) {
        this.notificationSettings[key] = value;
        this.notify();
    },

    // ---- Session Mutations ----

    revokeSession(sessionId) {
        this.sessions = this.sessions.filter(s => s.id !== sessionId);
        this.notify();
    },

    revokeAllSessions() {
        this.sessions = this.sessions.filter(s => s.isCurrent);
        this.notify();
    },

    // ---- Passkey Mutations ----

    addPasskey(name) {
        const id = 'pk_' + String(this._nextPasskeyId++).padStart(2, '0');
        const now = new Date().toISOString();
        this.passkeys.push({
            id,
            name: name || 'New Passkey',
            createdAt: now,
            lastUsedAt: now,
            credentialType: 'platform'
        });
        this.notify();
    },

    renamePasskey(passkeyId, newName) {
        const pk = this.passkeys.find(p => p.id === passkeyId);
        if (pk) {
            pk.name = newName;
            this.notify();
        }
    },

    deletePasskey(passkeyId) {
        this.passkeys = this.passkeys.filter(p => p.id !== passkeyId);
        this.notify();
    },

    // ---- API Key Mutations ----

    createApiKey(label) {
        const id = 'apikey_' + String(this._nextApiKeyId++).padStart(2, '0');
        const now = new Date().toISOString();
        const prefix = 'lin_api_' + Math.random().toString(36).substring(2, 6);
        this.apiKeys.push({
            id,
            label: label || 'Untitled API Key',
            keyPrefix: prefix,
            createdAt: now,
            lastUsedAt: null,
            expiresAt: null
        });
        this.notify();
        return id;
    },

    revokeApiKey(keyId) {
        this.apiKeys = this.apiKeys.filter(k => k.id !== keyId);
        this.notify();
    },

    // ---- OAuth App Mutations ----

    revokeAuthorizedApp(appId) {
        this.authorizedApps = this.authorizedApps.filter(a => a.id !== appId);
        this.notify();
    },

    // ---- Toast ----

    showToast(message) {
        this.toastMessage = message;
        if (this.toastTimeout) clearTimeout(this.toastTimeout);
        this.toastTimeout = setTimeout(() => {
            this.toastMessage = null;
            this._renderToast();
        }, 3000);
        this._renderToast();
    },

    _renderToast() {
        const el = document.getElementById('toast');
        if (!el) return;
        if (this.toastMessage) {
            el.textContent = this.toastMessage;
            el.classList.add('visible');
        } else {
            el.classList.remove('visible');
        }
    }
};
