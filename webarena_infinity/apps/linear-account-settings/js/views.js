// ============================================================
// views.js — Rendering for all sections of Linear Account Settings
// ============================================================

const Views = {

    // ============================================================
    // Sidebar Navigation
    // ============================================================

    renderSidebar() {
        const sections = [
            { id: 'profile', label: 'Profile', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 8a3 3 0 100-6 3 3 0 000 6zm-5 6s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3z"/></svg>' },
            { id: 'preferences', label: 'Preferences', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 4.754a3.246 3.246 0 100 6.492 3.246 3.246 0 000-6.492zM5.754 8a2.246 2.246 0 114.492 0 2.246 2.246 0 01-4.492 0z"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 01-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 01-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 01.52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 011.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 011.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 01.52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 01-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 01-1.255-.52l-.094-.319z"/></svg>' },
            { id: 'notifications', label: 'Notifications', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 16a2 2 0 002-2H6a2 2 0 002 2zM8 1.918l-.797.161A4.002 4.002 0 004 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4.002 4.002 0 00-3.203-3.92L8 1.917z"/></svg>' },
            { id: 'security', label: 'Security & Access', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0c-.69 0-1.281.476-1.478 1.117L5.532 2H3.5A1.5 1.5 0 002 3.5v10A1.5 1.5 0 003.5 15h9a1.5 1.5 0 001.5-1.5v-10A1.5 1.5 0 0012.5 2h-2.032l-.99-.883A1.5 1.5 0 008 0zm.5 4.75a.75.75 0 00-1.5 0v2.5h-2.5a.75.75 0 000 1.5h2.5v2.5a.75.75 0 001.5 0v-2.5h2.5a.75.75 0 000-1.5h-2.5v-2.5z"/></svg>' }
        ];

        return `
            <div class="sidebar-section-label">Account</div>
            ${sections.map(s => `
                <div class="sidebar-item ${AppState.currentSection === s.id ? 'active' : ''}"
                     data-action="navigate" data-section="${s.id}">
                    <span class="sidebar-icon">${s.icon}</span>
                    <span class="sidebar-text">${s.label}</span>
                </div>
            `).join('')}
        `;
    },

    // ============================================================
    // Main Content Router
    // ============================================================

    renderContent() {
        switch (AppState.currentSection) {
            case 'profile': return this.renderProfile();
            case 'preferences': return this.renderPreferences();
            case 'notifications': return this.renderNotifications();
            case 'security': return this.renderSecurity();
            default: return this.renderProfile();
        }
    },

    // ============================================================
    // Profile Section
    // ============================================================

    renderProfile() {
        const user = AppState.currentUser;
        if (!user) return '<div class="empty-state">No user data</div>';

        return `
            <div class="content-section">
                ${Components.sectionHeader('Profile', 'Manage your personal profile information.')}

                <div class="profile-card">
                    <div class="profile-avatar-section">
                        <div class="profile-avatar-wrapper" data-action="changeAvatar" title="Change profile picture">
                            ${Components.avatar(user, 'large')}
                            <div class="avatar-edit-overlay">
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M11.013 1.427a1.75 1.75 0 012.474 0l1.086 1.086a1.75 1.75 0 010 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 01-.927-.928l.929-3.25a1.75 1.75 0 01.445-.758l8.61-8.61z"/></svg>
                            </div>
                        </div>
                    </div>

                    <div class="profile-fields">
                        ${Components.inlineEditField('field-fullname', 'Full name', user.fullName, 'editFullName')}
                        ${Components.inlineEditField('field-username', 'Username', user.username, 'editUsername')}
                        ${Components.inlineEditField('field-email', 'Email', user.email, 'editEmail')}
                    </div>
                </div>

                <div class="content-divider"></div>

                ${Components.sectionHeader('Connected Accounts', 'Manage your connected third-party accounts.')}

                <div class="connected-accounts-list">
                    ${AppState.connectedAccounts.map(acc => `
                        <div class="connected-account-row" data-account-id="${acc.id}">
                            <div class="connected-account-icon">${Components.providerIcon(acc.providerIcon)}</div>
                            <div class="connected-account-info">
                                <div class="connected-account-provider">${acc.provider}</div>
                                <div class="connected-account-name">${acc.accountName}</div>
                            </div>
                            <div class="connected-account-status">
                                ${Components.statusBadge('Connected', 'success')}
                            </div>
                            <button class="btn-subtle btn-disconnect" data-action="disconnectAccount" data-account-id="${acc.id}" title="Disconnect ${acc.provider}">
                                Disconnect
                            </button>
                        </div>
                    `).join('')}
                    ${AppState.connectedAccounts.length === 0 ? '<div class="empty-state">No connected accounts</div>' : ''}
                </div>

                <div class="content-divider"></div>

                ${Components.sectionHeader('Workspaces', 'Workspaces you are a member of.')}

                <div class="workspaces-list">
                    ${AppState.workspaces.map(ws => `
                        <div class="workspace-row" data-workspace-id="${ws.id}">
                            ${Components.workspaceAvatar(ws)}
                            <div class="workspace-info">
                                <div class="workspace-name">${ws.name}</div>
                                <div class="workspace-meta">${ws.role} &middot; ${ws.memberCount} members</div>
                            </div>
                            <button class="btn-danger-subtle" data-action="leaveWorkspace" data-workspace-id="${ws.id}">
                                Leave workspace
                            </button>
                        </div>
                    `).join('')}
                    ${AppState.workspaces.length === 0 ? '<div class="empty-state">No workspaces</div>' : ''}
                </div>
            </div>
        `;
    },

    // ============================================================
    // Preferences Section
    // ============================================================

    renderPreferences() {
        const prefs = AppState.preferences;
        return `
            <div class="content-section">
                ${Components.sectionHeader('Preferences', 'Adjust your preferences to personalize your workflow.')}

                <div class="settings-group">
                    <h3 class="settings-group-title">General</h3>

                    ${Components.settingRow(
                        'Default home view',
                        'The default view that opens when you log in.',
                        Components.dropdown('pref-home-view', prefs.defaultHomeView, HOME_VIEW_OPTIONS)
                    )}

                    ${Components.settingRow(
                        'Display full names',
                        'Show full names instead of usernames.',
                        Components.toggle('pref-display-full-names', prefs.displayFullNames)
                    )}

                    ${Components.settingRow(
                        'First day of the week',
                        'Personalize how calendars display your weeks.',
                        Components.dropdown('pref-first-day', prefs.firstDayOfWeek, FIRST_DAY_OPTIONS)
                    )}

                    ${Components.settingRow(
                        'Convert text emoticons into emojis',
                        'Automatically convert text like :) into emojis.',
                        Components.toggle('pref-convert-emojis', prefs.convertTextEmojis)
                    )}
                </div>

                <div class="settings-group">
                    <h3 class="settings-group-title">Interface and theme</h3>

                    ${Components.settingRow(
                        'Theme',
                        'Choose your preferred theme.',
                        Components.dropdown('pref-theme', prefs.interfaceTheme, THEME_OPTIONS)
                    )}

                    ${Components.settingRow(
                        'Font size',
                        'Adjust the font size of the interface.',
                        Components.dropdown('pref-font-size', prefs.fontSize, FONT_SIZE_OPTIONS)
                    )}

                    ${Components.settingRow(
                        'Use pointer cursor',
                        'Show pointer cursor when hovering over interactive elements.',
                        Components.toggle('pref-pointer-cursor', prefs.usePointerCursor)
                    )}
                </div>

                <div class="settings-group">
                    <h3 class="settings-group-title">Desktop application</h3>

                    ${Components.settingRow(
                        'Open in desktop app',
                        'Attempt to open Linear URLs in the desktop app.',
                        Components.toggle('pref-open-desktop', prefs.openInDesktopApp)
                    )}

                    ${Components.settingRow(
                        'Notification badge',
                        'Show notification badges on the desktop app icon.',
                        Components.toggle('pref-notif-badge', prefs.desktopNotificationBadge)
                    )}

                    ${Components.settingRow(
                        'Spell check',
                        'Enable spell check in the desktop app.',
                        Components.toggle('pref-spell-check', prefs.enableSpellCheck)
                    )}
                </div>

                <div class="settings-group">
                    <h3 class="settings-group-title">Automations and workflows</h3>

                    ${Components.settingRow(
                        'Auto-assign on create',
                        'Automatically assign issues you create to yourself.',
                        Components.toggle('pref-auto-assign-create', prefs.autoAssignOnCreate)
                    )}

                    ${Components.settingRow(
                        'Auto-assign on started',
                        'Auto-assign issues you move to a started status.',
                        Components.toggle('pref-auto-assign-started', prefs.autoAssignOnStarted)
                    )}

                    ${Components.settingRow(
                        'Git attachment format',
                        'How git attachments are displayed.',
                        Components.dropdown('pref-git-format', prefs.gitAttachmentFormat, GIT_ATTACHMENT_FORMAT_OPTIONS)
                    )}

                    ${Components.settingRow(
                        'On git branch copy, move to started',
                        'Move issue to started status when you copy the git branch name.',
                        Components.toggle('pref-git-move-started', prefs.onGitBranchCopyMoveToStarted)
                    )}

                    ${Components.settingRow(
                        'On git branch copy, auto-assign',
                        'Auto-assign the issue to yourself when you copy the git branch name.',
                        Components.toggle('pref-git-auto-assign', prefs.onGitBranchCopyAutoAssign)
                    )}
                </div>
            </div>
        `;
    },

    // ============================================================
    // Notifications Section
    // ============================================================

    renderNotifications() {
        const ns = AppState.notificationSettings;
        return `
            <div class="content-section">
                ${Components.sectionHeader('Notifications', 'Manage how and when you receive notifications.')}

                <div class="notification-channels">
                    ${this._renderNotificationChannel('desktop', 'Desktop', ns.desktop)}
                    ${this._renderNotificationChannel('mobile', 'Mobile', ns.mobile)}
                    ${this._renderNotificationChannel('email', 'Email', ns.email)}
                    ${this._renderNotificationChannel('slack', 'Slack', ns.slack)}
                </div>

                <div class="content-divider"></div>

                <div class="settings-group">
                    <h3 class="settings-group-title">Communications</h3>

                    ${Components.settingRow(
                        'Changelogs',
                        'Receive updates about new Linear features and improvements.',
                        Components.toggle('notif-changelogs', ns.receiveChangelogs)
                    )}

                    ${Components.settingRow(
                        'DPA updates',
                        'Receive updates about data processing agreement changes.',
                        Components.toggle('notif-dpa', ns.receiveDpaUpdates)
                    )}

                    ${Components.settingRow(
                        'Product updates',
                        'Receive other product-related communications.',
                        Components.toggle('notif-product', ns.receiveProductUpdates)
                    )}
                </div>
            </div>
        `;
    },

    _renderNotificationChannel(channel, label, settings) {
        const enabled = settings.enabled;
        const dotClass = enabled ? 'dot-active' : 'dot-inactive';
        const icon = Components.channelIcon(channel);

        const notifTypes = [
            { key: 'issueAssigned', label: 'Issue assigned to you' },
            { key: 'issueStatusChanged', label: 'Status changes' },
            { key: 'issueCommented', label: 'Comments on subscribed issues' },
            { key: 'issueMentioned', label: 'Mentions' },
            { key: 'projectUpdated', label: 'Project updates' },
            { key: 'cycleUpdated', label: 'Cycle updates' }
        ];

        let extraSettings = '';
        if (channel === 'email') {
            extraSettings = `
                <div class="channel-extra-settings">
                    <div class="extra-setting-divider"></div>
                    <h4 class="extra-setting-title">Delivery preferences</h4>
                    ${Components.settingRow(
                        'Send urgent immediately',
                        'Send notification email immediately for urgent issues or SLA breaches.',
                        Components.toggle(`notif-${channel}-urgent`, settings.sendUrgentImmediately)
                    )}
                    ${Components.settingRow(
                        'Delay low priority outside hours',
                        'Delay low priority email notifications outside work hours (8am-6pm).',
                        Components.toggle(`notif-${channel}-delay-low`, settings.delayLowPriorityOutsideHours)
                    )}
                </div>
            `;
        }

        return `
            <div class="notification-channel" data-channel="${channel}" id="channel-${channel}">
                <div class="channel-header" data-action="toggleChannelExpand" data-channel="${channel}">
                    <div class="channel-icon">${icon}</div>
                    <div class="channel-info">
                        <span class="channel-name">${label}</span>
                        <span class="channel-status-dot ${dotClass}"></span>
                    </div>
                    <svg class="channel-expand-arrow" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M6.22 3.22a.75.75 0 011.06 0l4.25 4.25a.75.75 0 010 1.06l-4.25 4.25a.75.75 0 01-1.06-1.06L9.94 8 6.22 4.28a.75.75 0 010-1.06z"/></svg>
                </div>
                <div class="channel-body" style="display:none;">
                    ${Components.settingRow(
                        'Enable ' + label.toLowerCase() + ' notifications',
                        '',
                        Components.toggle(`notif-${channel}-enabled`, enabled)
                    )}
                    <div class="channel-notification-types ${!enabled ? 'disabled' : ''}">
                        ${notifTypes.map(nt => `
                            <div class="notif-type-row">
                                <span class="notif-type-label">${nt.label}</span>
                                <div class="toggle-switch ${settings[nt.key] ? 'active' : ''} ${!enabled ? 'disabled' : ''}"
                                     data-toggle-id="notif-${channel}-${nt.key}"
                                     data-channel="${channel}"
                                     data-notif-key="${nt.key}">
                                    <div class="toggle-knob"></div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    ${extraSettings}
                </div>
            </div>
        `;
    },

    // ============================================================
    // Security & Access Section
    // ============================================================

    renderSecurity() {
        return `
            <div class="content-section">
                ${Components.sectionHeader('Security & Access', 'Manage your account security, sessions, and access.')}

                <div class="settings-group">
                    <div class="settings-group-header">
                        <h3 class="settings-group-title">Sessions</h3>
                        <button class="btn-danger-subtle" data-action="revokeAllSessions"
                            ${AppState.sessions.filter(s => !s.isCurrent).length === 0 ? 'disabled' : ''}>
                            Revoke all
                        </button>
                    </div>
                    <p class="settings-group-description">Devices that are currently signed in to your account. Inactive sessions expire after 30 days.</p>

                    <div class="sessions-list">
                        ${AppState.sessions.map(sess => this._renderSessionRow(sess)).join('')}
                        ${AppState.sessions.length === 0 ? '<div class="empty-state">No active sessions</div>' : ''}
                    </div>
                </div>

                <div class="content-divider"></div>

                <div class="settings-group">
                    <div class="settings-group-header">
                        <h3 class="settings-group-title">Passkeys</h3>
                        <button class="btn-primary-small" data-action="addPasskey">Add passkey</button>
                    </div>
                    <p class="settings-group-description">Passkeys allow secure and fast login without passwords. Supported by all major browsers and password managers.</p>

                    <div class="passkeys-list">
                        ${AppState.passkeys.map(pk => `
                            <div class="passkey-row" data-passkey-id="${pk.id}">
                                <div class="passkey-icon">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
                                </div>
                                <div class="passkey-info">
                                    <div class="passkey-name">${pk.name}</div>
                                    <div class="passkey-meta">Created ${Components.formatDate(pk.createdAt)} &middot; Last used ${Components.timeAgo(pk.lastUsedAt)}</div>
                                </div>
                                <button class="btn-subtle" data-action="deletePasskey" data-passkey-id="${pk.id}">Remove</button>
                            </div>
                        `).join('')}
                        ${AppState.passkeys.length === 0 ? '<div class="empty-state">No passkeys registered</div>' : ''}
                    </div>
                </div>

                <div class="content-divider"></div>

                <div class="settings-group">
                    <div class="settings-group-header">
                        <h3 class="settings-group-title">Personal API keys</h3>
                        <button class="btn-primary-small" data-action="createApiKey">Create key</button>
                    </div>
                    <p class="settings-group-description">Create or revoke API keys associated with your account.</p>

                    <div class="api-keys-list">
                        ${AppState.apiKeys.map(key => `
                            <div class="api-key-row" data-key-id="${key.id}">
                                <div class="api-key-icon">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 11-7.778 7.778 5.5 5.5 0 017.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>
                                </div>
                                <div class="api-key-info">
                                    <div class="api-key-label">${key.label}</div>
                                    <div class="api-key-meta">
                                        <span class="api-key-prefix">${key.keyPrefix}...</span>
                                        &middot; Created ${Components.formatDate(key.createdAt)}
                                        ${key.lastUsedAt ? '&middot; Last used ' + Components.timeAgo(key.lastUsedAt) : ''}
                                        ${key.expiresAt ? '&middot; Expires ' + Components.formatDate(key.expiresAt) : ''}
                                    </div>
                                </div>
                                <button class="btn-danger-subtle" data-action="revokeApiKey" data-key-id="${key.id}">Revoke</button>
                            </div>
                        `).join('')}
                        ${AppState.apiKeys.length === 0 ? '<div class="empty-state">No API keys</div>' : ''}
                    </div>
                </div>

                <div class="content-divider"></div>

                <div class="settings-group">
                    <h3 class="settings-group-title">Authorized applications</h3>
                    <p class="settings-group-description">OAuth applications with access to your account.</p>

                    <div class="authorized-apps-list">
                        ${AppState.authorizedApps.map(app => `
                            <div class="oauth-app-row" data-app-id="${app.id}">
                                <div class="oauth-app-icon">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/></svg>
                                </div>
                                <div class="oauth-app-info">
                                    <div class="oauth-app-name">${app.name}</div>
                                    <div class="oauth-app-description">${app.description}</div>
                                    <div class="oauth-app-meta">
                                        Authorized ${Components.formatDate(app.authorizedAt)}
                                        &middot; Last accessed ${Components.timeAgo(app.lastAccessedAt)}
                                    </div>
                                    <div class="oauth-app-permissions">
                                        ${app.permissions.map(p => `<span class="permission-badge">${p}</span>`).join('')}
                                    </div>
                                </div>
                                <button class="btn-danger-subtle" data-action="revokeApp" data-app-id="${app.id}">Revoke access</button>
                            </div>
                        `).join('')}
                        ${AppState.authorizedApps.length === 0 ? '<div class="empty-state">No authorized applications</div>' : ''}
                    </div>
                </div>
            </div>
        `;
    },

    _renderSessionRow(sess) {
        const isExpanded = AppState.expandedSessionId === sess.id;
        return `
            <div class="session-row ${sess.isCurrent ? 'current-session' : ''} ${isExpanded ? 'expanded' : ''}" data-session-id="${sess.id}">
                <div class="session-summary" data-action="toggleSessionDetails" data-session-id="${sess.id}">
                    <div class="session-device-icon">${Components.deviceIcon(sess.deviceType)}</div>
                    <div class="session-info">
                        <div class="session-device-name">
                            ${sess.deviceName}
                            ${sess.isCurrent ? '<span class="current-badge">Current</span>' : ''}
                        </div>
                        <div class="session-meta">${sess.location} &middot; ${Components.timeAgo(sess.lastSeenAt)}</div>
                    </div>
                    ${!sess.isCurrent ? `
                        <button class="btn-danger-subtle session-revoke-btn" data-action="revokeSession" data-session-id="${sess.id}">
                            Revoke access
                        </button>
                    ` : ''}
                </div>
                ${isExpanded ? `
                    <div class="session-details">
                        <div class="session-detail-row"><span class="detail-label">IP Address</span><span class="detail-value">${sess.ipAddress}</span></div>
                        <div class="session-detail-row"><span class="detail-label">Browser</span><span class="detail-value">${sess.browser}</span></div>
                        <div class="session-detail-row"><span class="detail-label">Operating System</span><span class="detail-value">${sess.os}</span></div>
                        <div class="session-detail-row"><span class="detail-label">Location</span><span class="detail-value">${sess.location}</span></div>
                        <div class="session-detail-row"><span class="detail-label">Signed in</span><span class="detail-value">${Components.formatDateTime(sess.signedInAt)}</span></div>
                        <div class="session-detail-row"><span class="detail-label">Last seen</span><span class="detail-value">${Components.formatDateTime(sess.lastSeenAt)}</span></div>
                    </div>
                ` : ''}
            </div>
        `;
    },

    // ============================================================
    // Modal Rendering
    // ============================================================

    renderModal() {
        const modal = AppState.activeModal;
        if (!modal) return '';

        switch (modal) {
            case 'editFullName': return this._renderEditFieldModal('Edit full name', 'fullName', AppState.currentUser.fullName);
            case 'editUsername': return this._renderEditFieldModal('Edit username', 'username', AppState.currentUser.username);
            case 'editEmail': return this._renderEditEmailModal();
            case 'leaveWorkspace': return this._renderLeaveWorkspaceModal();
            case 'revokeSession': return this._renderRevokeSessionModal();
            case 'revokeAllSessions': return this._renderRevokeAllSessionsModal();
            case 'deletePasskey': return this._renderDeletePasskeyModal();
            case 'createApiKey': return this._renderCreateApiKeyModal();
            case 'revokeApiKey': return this._renderRevokeApiKeyModal();
            case 'revokeApp': return this._renderRevokeAppModal();
            case 'disconnectAccount': return this._renderDisconnectAccountModal();
            case 'addPasskey': return this._renderAddPasskeyModal();
            default: return '';
        }
    },

    _renderEditFieldModal(title, field, currentValue) {
        const body = `
            <div class="modal-form">
                <label class="modal-form-label">${title}</label>
                <input type="text" class="modal-input" id="modal-input-field" value="${(currentValue || '').replace(/"/g, '&quot;')}" autocomplete="off" />
            </div>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-primary" data-action="confirmEditField" data-field="${field}">Save</button>
        `;
        return Components.modal('editFieldModal', title, body, footer);
    },

    _renderEditEmailModal() {
        const body = `
            <div class="modal-form">
                <p class="modal-warning">Changing your email address will change it for <strong>all</strong> workspaces using the current email. A confirmation email will be sent to both old and new addresses.</p>
                <label class="modal-form-label">New email address</label>
                <input type="email" class="modal-input" id="modal-input-email" value="" placeholder="Enter new email address" autocomplete="off" />
                <div class="modal-validation-msg" id="email-validation-msg"></div>
            </div>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-primary" data-action="confirmEditEmail" id="confirm-email-btn" disabled>Update email</button>
        `;
        return Components.modal('editEmailModal', 'Change email address', body, footer);
    },

    _renderLeaveWorkspaceModal() {
        const ws = AppState.modalData;
        const body = `
            <p>Are you sure you want to leave <strong>${ws ? ws.name : 'this workspace'}</strong>? You will lose access and an admin will need to re-invite you.</p>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-danger" data-action="confirmLeaveWorkspace" data-workspace-id="${ws ? ws.id : ''}">Leave workspace</button>
        `;
        return Components.modal('leaveWorkspaceModal', 'Leave workspace', body, footer);
    },

    _renderRevokeSessionModal() {
        const sess = AppState.modalData;
        const body = `
            <p>Are you sure you want to revoke access for <strong>${sess ? sess.deviceName : 'this session'}</strong>?</p>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-danger" data-action="confirmRevokeSession" data-session-id="${sess ? sess.id : ''}">Revoke access</button>
        `;
        return Components.modal('revokeSessionModal', 'Revoke session', body, footer);
    },

    _renderRevokeAllSessionsModal() {
        const count = AppState.sessions.filter(s => !s.isCurrent).length;
        const body = `
            <p>This will revoke <strong>${count}</strong> session${count !== 1 ? 's' : ''} (all except your current session). You will need to sign in again on those devices.</p>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-danger" data-action="confirmRevokeAllSessions">Revoke all sessions</button>
        `;
        return Components.modal('revokeAllSessionsModal', 'Revoke all sessions', body, footer);
    },

    _renderDeletePasskeyModal() {
        const pk = AppState.modalData;
        const body = `
            <p>Are you sure you want to remove the passkey <strong>${pk ? pk.name : ''}</strong>? You will no longer be able to use it to sign in.</p>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-danger" data-action="confirmDeletePasskey" data-passkey-id="${pk ? pk.id : ''}">Remove passkey</button>
        `;
        return Components.modal('deletePasskeyModal', 'Remove passkey', body, footer);
    },

    _renderCreateApiKeyModal() {
        const body = `
            <div class="modal-form">
                <label class="modal-form-label">Label</label>
                <input type="text" class="modal-input" id="modal-input-api-label" placeholder="e.g., CI/CD Pipeline" autocomplete="off" />
            </div>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-primary" data-action="confirmCreateApiKey">Create key</button>
        `;
        return Components.modal('createApiKeyModal', 'Create API key', body, footer);
    },

    _renderRevokeApiKeyModal() {
        const key = AppState.modalData;
        const body = `
            <p>Are you sure you want to revoke the API key <strong>${key ? key.label : ''}</strong> (${key ? key.keyPrefix : ''}...)? Any integrations using this key will stop working.</p>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-danger" data-action="confirmRevokeApiKey" data-key-id="${key ? key.id : ''}">Revoke key</button>
        `;
        return Components.modal('revokeApiKeyModal', 'Revoke API key', body, footer);
    },

    _renderRevokeAppModal() {
        const app = AppState.modalData;
        const body = `
            <p>Are you sure you want to revoke access for <strong>${app ? app.name : 'this application'}</strong>? The application will no longer be able to access your Linear data.</p>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-danger" data-action="confirmRevokeApp" data-app-id="${app ? app.id : ''}">Revoke access</button>
        `;
        return Components.modal('revokeAppModal', 'Revoke application access', body, footer);
    },

    _renderDisconnectAccountModal() {
        const acc = AppState.modalData;
        const body = `
            <p>Are you sure you want to disconnect <strong>${acc ? acc.provider : 'this account'}</strong> (${acc ? acc.accountName : ''})? Linear will no longer be able to associate actions from this integration with your account.</p>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-danger" data-action="confirmDisconnectAccount" data-account-id="${acc ? acc.id : ''}">Disconnect</button>
        `;
        return Components.modal('disconnectAccountModal', 'Disconnect account', body, footer);
    },

    _renderAddPasskeyModal() {
        const body = `
            <div class="modal-form">
                <label class="modal-form-label">Passkey name</label>
                <input type="text" class="modal-input" id="modal-input-passkey-name" placeholder="e.g., MacBook Pro Touch ID" autocomplete="off" />
            </div>
        `;
        const footer = `
            <button class="btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn-primary" data-action="confirmAddPasskey">Register passkey</button>
        `;
        return Components.modal('addPasskeyModal', 'Register new passkey', body, footer);
    }
};
