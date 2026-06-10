const Components = {
    // ---- Avatar
    avatar(name, color, size) {
        const sizeClass = size || 'medium';
        const initials = (name || 'U').split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
        return `<div class="avatar avatar-${sizeClass}" style="background-color: ${color || '#5E6AD2'}">${initials}</div>`;
    },

    // ---- Custom Dropdown
    dropdown(id, currentValue, options, placeholder) {
        const displayVal = currentValue || placeholder || 'Select...';
        return `
            <div class="custom-dropdown" id="${id}" data-value="${(currentValue || '').replace(/"/g, '&quot;')}">
                <div class="dropdown-trigger" data-dropdown-id="${id}">
                    <span class="dropdown-value">${displayVal}</span>
                    <span class="dropdown-arrow"><svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></span>
                </div>
                <div class="dropdown-menu">
                    ${options.map(opt => `
                        <div class="dropdown-item ${opt === currentValue ? 'selected' : ''}"
                             data-dropdown-id="${id}"
                             data-value="${String(opt).replace(/"/g, '&quot;')}">
                            ${opt}
                            ${opt === currentValue ? '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    },

    // ---- Toggle Switch
    toggle(id, checked) {
        return `
            <div class="toggle-switch ${checked ? 'active' : ''}" id="${id}" data-toggle-id="${id}">
                <div class="toggle-knob"></div>
            </div>
        `;
    },

    // ---- Checkbox
    checkbox(id, checked, label) {
        return `
            <label class="checkbox-row" data-checkbox-id="${id}">
                <div class="custom-checkbox ${checked ? 'checked' : ''}" id="${id}">
                    ${checked ? '<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6L5 9L10 3" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>' : ''}
                </div>
                <span class="checkbox-label">${label}</span>
            </label>
        `;
    },

    // ---- Tag/Chip
    tag(text, removable, removeAction) {
        return `
            <span class="tag">
                ${text}
                ${removable ? `<button class="tag-remove" data-action="${removeAction}" data-value="${text.replace(/"/g, '&quot;')}">&times;</button>` : ''}
            </span>
        `;
    },

    // ---- Status Badge
    statusBadge(text, type) {
        return `<span class="status-badge status-${type || 'default'}">${text}</span>`;
    },

    // ---- Search Input
    searchInput(id, placeholder, value) {
        return `
            <div class="search-input-wrapper">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M11 11L14 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                <input type="text" class="search-input" id="${id}" placeholder="${placeholder || 'Search...'}" value="${(value || '').replace(/"/g, '&quot;')}" autocomplete="off" />
            </div>
        `;
    },

    // ---- Modal
    modal(id, title, bodyHtml, footerHtml, size) {
        return `
            <div class="modal-overlay" id="${id}">
                <div class="modal ${size || ''}">
                    <div class="modal-header">
                        <h3 class="modal-title">${title}</h3>
                        <button class="modal-close" data-action="closeModal">&times;</button>
                    </div>
                    <div class="modal-body">${bodyHtml}</div>
                    ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
                </div>
            </div>
        `;
    },

    // ---- Empty State
    emptyState(icon, title, subtitle) {
        return `
            <div class="empty-state">
                <div class="empty-state-icon">${icon || ''}</div>
                <h3 class="empty-state-title">${title}</h3>
                ${subtitle ? `<p class="empty-state-subtitle">${subtitle}</p>` : ''}
            </div>
        `;
    },

    // ---- Button
    btn(text, action, variant, disabled, extraAttrs) {
        return `<button class="btn btn-${variant || 'primary'}" data-action="${action}" ${disabled ? 'disabled' : ''} ${extraAttrs || ''}>${text}</button>`;
    },

    // ---- Time formatting
    timeAgo(dateStr) {
        if (!dateStr) return 'Never';
        const date = new Date(dateStr);
        const now = new Date('2026-03-07T10:00:00Z');
        const diffMs = now - date;
        const diffMin = Math.floor(diffMs / 60000);
        if (diffMin < 0) return 'Just now';
        if (diffMin < 1) return 'Just now';
        if (diffMin < 60) return `${diffMin}m ago`;
        const diffHrs = Math.floor(diffMin / 60);
        if (diffHrs < 24) return `${diffHrs}h ago`;
        const diffDays = Math.floor(diffHrs / 24);
        if (diffDays < 7) return `${diffDays}d ago`;
        if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: date.getFullYear() !== 2026 ? 'numeric' : undefined });
    },

    formatDate(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
    },

    formatDateShort(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    },

    // ---- Truncate text
    truncate(text, maxLen) {
        if (!text) return '';
        if (text.length <= maxLen) return text;
        return text.substring(0, maxLen) + '...';
    },

    // ---- Tab Bar
    tabBar(tabs, activeTab, tabAction) {
        return `
            <div class="tab-bar">
                ${tabs.map(t => `
                    <button class="tab-item ${t.id === activeTab ? 'active' : ''}" data-action="${tabAction}" data-tab="${t.id}">
                        ${t.label}
                        ${t.count !== undefined ? `<span class="tab-count">${t.count}</span>` : ''}
                    </button>
                `).join('')}
            </div>
        `;
    },

    // ---- Filter Chips
    filterChips(options, active, action) {
        return `
            <div class="filter-chips">
                ${options.map(opt => `
                    <button class="filter-chip ${opt === active ? 'active' : ''}" data-action="${action}" data-value="${opt.replace(/"/g, '&quot;')}">${opt}</button>
                `).join('')}
            </div>
        `;
    },

    // ---- Card
    card(content, extraClass) {
        return `<div class="card ${extraClass || ''}">${content}</div>`;
    },

    // ---- Notification dot
    notificationDot(count) {
        if (!count || count <= 0) return '';
        return `<span class="notification-dot">${count > 99 ? '99+' : count}</span>`;
    },

    // ---- Typeahead input
    typeaheadInput(id, placeholder, suggestions, selectedValues, addAction, removeAction) {
        return `
            <div class="typeahead-container" id="${id}-container">
                <div class="typeahead-tags">
                    ${(selectedValues || []).map(v => Components.tag(v, true, removeAction)).join('')}
                </div>
                <div class="typeahead-input-wrapper">
                    <input type="text" class="typeahead-input" id="${id}" placeholder="${placeholder || 'Type to search...'}" autocomplete="off" data-typeahead-id="${id}" />
                    <div class="typeahead-suggestions" id="${id}-suggestions">
                        ${(suggestions || []).map(s => `
                            <div class="typeahead-suggestion" data-action="${addAction}" data-value="${s.replace(/"/g, '&quot;')}">${s}</div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    },

    // ---- Pagination info
    paginationInfo(showing, total) {
        return `<div class="pagination-info">Showing ${showing} of ${total} results</div>`;
    },

    // ---- Section header
    sectionHeader(title, subtitle) {
        return `
            <div class="section-header">
                <h2 class="section-title">${title}</h2>
                ${subtitle ? `<p class="section-subtitle">${subtitle}</p>` : ''}
            </div>
        `;
    }
};
