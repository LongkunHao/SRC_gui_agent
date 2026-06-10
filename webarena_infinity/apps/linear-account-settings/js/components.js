// ============================================================
// components.js — Reusable UI components
// ============================================================

const Components = {

    // ---- Custom Dropdown ----
    dropdown(id, currentValue, options, extraClass = '') {
        const escaped = (currentValue || '').replace(/"/g, '&quot;');
        return `
            <div class="custom-dropdown ${extraClass}" id="${id}" data-value="${escaped}">
                <div class="dropdown-trigger" data-dropdown-id="${id}">
                    <span class="dropdown-value">${currentValue || 'Select...'}</span>
                    <span class="dropdown-arrow">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M4.427 6.427l3.396 3.396a.25.25 0 00.354 0l3.396-3.396A.25.25 0 0011.396 6H4.604a.25.25 0 00-.177.427z"/></svg>
                    </span>
                </div>
                <div class="dropdown-menu">
                    ${options.map(opt => `
                        <div class="dropdown-item ${opt === currentValue ? 'selected' : ''}"
                             data-dropdown-id="${id}"
                             data-value="${opt.replace(/"/g, '&quot;')}">
                            ${opt}
                            ${opt === currentValue ? '<svg class="check-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"/></svg>' : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    },

    // ---- Toggle Switch ----
    toggle(id, checked, label = '') {
        return `
            <div class="toggle-row">
                ${label ? `<span class="toggle-label">${label}</span>` : ''}
                <div class="toggle-switch ${checked ? 'active' : ''}" id="${id}" data-toggle-id="${id}">
                    <div class="toggle-knob"></div>
                </div>
            </div>
        `;
    },

    // ---- Section Header ----
    sectionHeader(title, subtitle = '') {
        return `
            <div class="section-header">
                <h2 class="section-title">${title}</h2>
                ${subtitle ? `<p class="section-subtitle">${subtitle}</p>` : ''}
            </div>
        `;
    },

    // ---- Setting Row ----
    settingRow(label, description, controlHtml) {
        return `
            <div class="setting-row">
                <div class="setting-info">
                    <div class="setting-label">${label}</div>
                    ${description ? `<div class="setting-description">${description}</div>` : ''}
                </div>
                <div class="setting-control">
                    ${controlHtml}
                </div>
            </div>
        `;
    },

    // ---- Avatar ----
    avatar(user, size = 'medium') {
        const sizeClass = `avatar-${size}`;
        if (user.avatarUrl) {
            return `<div class="avatar ${sizeClass}" style="background-image: url('${user.avatarUrl}')"></div>`;
        }
        const initials = (user.fullName || user.name || 'U')
            .split(' ')
            .map(w => w[0])
            .join('')
            .substring(0, 2)
            .toUpperCase();
        return `<div class="avatar ${sizeClass}" style="background-color: ${user.avatarColor || '#5E6AD2'}">${initials}</div>`;
    },

    // ---- Workspace Avatar ----
    workspaceAvatar(ws) {
        const initial = ws.name.charAt(0).toUpperCase();
        return `<div class="workspace-avatar" style="background-color: ${ws.avatarColor || '#5E6AD2'}">${initial}</div>`;
    },

    // ---- Modal ----
    modal(id, title, bodyHtml, footerHtml = '', size = '') {
        return `
            <div class="modal-overlay" id="${id}">
                <div class="modal ${size}">
                    <div class="modal-header">
                        <h3 class="modal-title">${title}</h3>
                        <button class="modal-close" data-action="closeModal">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"/></svg>
                        </button>
                    </div>
                    <div class="modal-body">${bodyHtml}</div>
                    ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
                </div>
            </div>
        `;
    },

    // ---- Inline Edit Field ----
    inlineEditField(id, label, value, actionName) {
        return `
            <div class="inline-field" id="${id}">
                <div class="inline-field-label">${label}</div>
                <div class="inline-field-value-row">
                    <span class="inline-field-value">${value || 'Not set'}</span>
                    <button class="inline-edit-btn" data-action="${actionName}" title="Edit ${label}">
                        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M11.013 1.427a1.75 1.75 0 012.474 0l1.086 1.086a1.75 1.75 0 010 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 01-.927-.928l.929-3.25a1.75 1.75 0 01.445-.758l8.61-8.61zm1.414 1.06a.25.25 0 00-.354 0L3.463 11.1a.25.25 0 00-.064.108l-.537 1.88 1.88-.537a.25.25 0 00.108-.064l8.61-8.61a.25.25 0 000-.354L12.427 2.487z"/></svg>
                    </button>
                </div>
            </div>
        `;
    },

    // ---- Notification Channel Card ----
    notificationChannelCard(channel, label, icon, settings) {
        const enabled = settings.enabled;
        const dotClass = enabled ? 'dot-active' : 'dot-inactive';
        return `
            <div class="notification-channel-card" data-channel="${channel}">
                <div class="channel-header" data-action="expandChannel" data-channel="${channel}">
                    <div class="channel-icon">${icon}</div>
                    <div class="channel-info">
                        <div class="channel-name">${label}</div>
                        <div class="channel-status-dot ${dotClass}"></div>
                    </div>
                    <svg class="channel-expand-arrow" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M6.22 3.22a.75.75 0 011.06 0l4.25 4.25a.75.75 0 010 1.06l-4.25 4.25a.75.75 0 01-1.06-1.06L9.94 8 6.22 4.28a.75.75 0 010-1.06z"/></svg>
                </div>
            </div>
        `;
    },

    // ---- Status Badge ----
    statusBadge(text, type = 'default') {
        return `<span class="status-badge status-badge-${type}">${text}</span>`;
    },

    // ---- Time Ago ----
    timeAgo(dateStr) {
        if (!dateStr) return 'Never';
        const date = new Date(dateStr);
        const now = new Date('2026-03-06T10:00:00Z');
        const diffMs = now - date;
        const diffMin = Math.floor(diffMs / 60000);
        const diffHr = Math.floor(diffMin / 60);
        const diffDay = Math.floor(diffHr / 24);

        if (diffMin < 1) return 'Just now';
        if (diffMin < 60) return `${diffMin}m ago`;
        if (diffHr < 24) return `${diffHr}h ago`;
        if (diffDay < 7) return `${diffDay}d ago`;
        if (diffDay < 30) return `${Math.floor(diffDay / 7)}w ago`;
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },

    formatDate(dateStr) {
        if (!dateStr) return 'N/A';
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },

    formatDateTime(dateStr) {
        if (!dateStr) return 'N/A';
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', {
            month: 'short', day: 'numeric', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    },

    // ---- Provider Icon ----
    providerIcon(provider) {
        const icons = {
            github: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
            gitlab: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 01-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 014.82 2a.43.43 0 01.58 0 .42.42 0 01.11.18l2.44 7.49h8.1l2.44-7.51A.42.42 0 0118.6 2a.43.43 0 01.58 0 .42.42 0 01.11.18l2.44 7.51L23 13.45a.84.84 0 01-.35.94z"/></svg>',
            slack: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312zM15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z"/></svg>',
            figma: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M15.852 8.981h-4.588V0h4.588c2.476 0 4.49 2.014 4.49 4.49s-2.014 4.491-4.49 4.491zM12.735 7.51h3.117c1.665 0 3.019-1.355 3.019-3.019s-1.354-3.019-3.019-3.019h-3.117V7.51zM8.148 24c-2.476 0-4.49-2.014-4.49-4.49s2.014-4.49 4.49-4.49h4.588v4.441c0 2.503-2.014 4.539-4.588 4.539zm-.001-7.509a3.023 3.023 0 00-3.019 3.019c0 1.665 1.354 3.019 3.019 3.019 1.665 0 3.019-1.354 3.019-3.019V16.49H8.147zM8.148 15.02a4.488 4.488 0 01-4.49-4.49c0-2.476 2.014-4.49 4.49-4.49h4.588v8.98H8.148zm0-7.51a3.023 3.023 0 00-3.019 3.019c0 1.665 1.354 3.019 3.019 3.019h3.117V7.51H8.148zM15.852 15.02h-4.588v-8.98h4.588c2.476 0 4.49 2.014 4.49 4.49s-2.014 4.49-4.49 4.49zm0-7.51h-3.117v5.96h3.117c1.665 0 3.019-1.355 3.019-3.019s-1.354-2.941-3.019-2.941z"/></svg>',
            google: '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>'
        };
        return icons[provider] || '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10"/></svg>';
    },

    // ---- Device Icon ----
    deviceIcon(deviceType) {
        if (deviceType === 'mobile') {
            return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>';
        }
        if (deviceType === 'tablet') {
            return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>';
        }
        return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>';
    },

    // ---- Notification Channel Icons ----
    channelIcon(channel) {
        const icons = {
            desktop: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
            mobile: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>',
            email: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
            slack: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313z"/></svg>'
        };
        return icons[channel] || '';
    }
};
