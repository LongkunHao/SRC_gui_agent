/* ============================================================
   components.js — Reusable UI component factories
   ============================================================ */

const Components = {

    // ── Custom Dropdown ──
    dropdown(id, currentValue, options, extraClass) {
        const cls = extraClass ? `custom-dropdown ${extraClass}` : 'custom-dropdown';
        const displayValue = currentValue || 'Select...';
        const optionsHtml = options.map(opt => {
            const val = typeof opt === 'object' ? opt.value : opt;
            const label = typeof opt === 'object' ? opt.label : opt;
            const selected = val === currentValue ? ' selected' : '';
            return `<div class="dropdown-item${selected}" data-value="${this.escAttr(val)}">${this.esc(label)}</div>`;
        }).join('');
        return `<div class="${cls}" data-dropdown-id="${id}">
            <div class="dropdown-trigger" data-dropdown-trigger="${id}">
                <span class="dropdown-value">${this.esc(displayValue)}</span>
                <span class="dropdown-arrow">&#9662;</span>
            </div>
            <div class="dropdown-menu" data-dropdown-menu="${id}">
                ${optionsHtml}
            </div>
        </div>`;
    },

    // ── Toggle Switch ──
    toggle(id, checked, label) {
        const activeClass = checked ? ' active' : '';
        return `<div class="toggle-row">
            <span class="toggle-label">${this.esc(label || '')}</span>
            <div class="toggle-switch${activeClass}" data-toggle-id="${id}">
                <div class="toggle-knob"></div>
            </div>
        </div>`;
    },

    // ── Modal ──
    modal(id, title, bodyHtml, footerHtml, size) {
        const sizeClass = size ? ` modal-${size}` : '';
        return `<div class="modal-overlay" data-modal-id="${id}">
            <div class="modal${sizeClass}">
                <div class="modal-header">
                    <h2>${this.esc(title)}</h2>
                    <button class="modal-close" data-action="close-modal">&times;</button>
                </div>
                <div class="modal-body">${bodyHtml}</div>
                ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
            </div>
        </div>`;
    },

    // ── Section Header ──
    sectionHeader(title, subtitle, actions) {
        return `<div class="section-header">
            <div class="section-header-text">
                <h2>${this.esc(title)}</h2>
                ${subtitle ? `<p class="section-subtitle">${this.esc(subtitle)}</p>` : ''}
            </div>
            ${actions ? `<div class="section-header-actions">${actions}</div>` : ''}
        </div>`;
    },

    // ── Status Badge ──
    statusBadge(text, type) {
        return `<span class="status-badge status-${type || 'default'}">${this.esc(text)}</span>`;
    },

    // ── Patient Tag ──
    patientTag(tag, removable, patientId) {
        const removeBtn = removable ? ` <span class="tag-remove" data-action="remove-tag" data-patient-id="${patientId}" data-tag="${this.escAttr(tag)}">&times;</span>` : '';
        const starred = tag.startsWith('*') ? ' tag-starred' : '';
        return `<span class="patient-tag${starred}">${this.esc(tag)}${removeBtn}</span>`;
    },

    // ── Info Box ──
    infoBox(type, message) {
        const icons = { info: 'i', warning: '!', error: '&times;', success: '&#10003;' };
        return `<div class="info-box info-${type}">
            <span class="info-icon">${icons[type] || 'i'}</span>
            <span>${message}</span>
        </div>`;
    },

    // ── Table ──
    table(headers, rows, id) {
        const headHtml = headers.map(h => `<th>${this.esc(h)}</th>`).join('');
        const bodyHtml = rows.map(row => {
            const cells = row.map(cell => `<td>${cell}</td>`).join('');
            return `<tr>${cells}</tr>`;
        }).join('');
        return `<table class="data-table" ${id ? `id="${id}"` : ''}>
            <thead><tr>${headHtml}</tr></thead>
            <tbody>${bodyHtml}</tbody>
        </table>`;
    },

    // ── Search Input ──
    searchInput(id, placeholder, value) {
        return `<div class="search-box">
            <span class="search-icon">&#128269;</span>
            <input type="text" class="search-input" id="${id}" placeholder="${this.escAttr(placeholder || 'Search...')}" value="${this.escAttr(value || '')}">
        </div>`;
    },

    // ── Button ──
    button(label, action, type, extra) {
        const cls = type ? `btn btn-${type}` : 'btn';
        const extraAttrs = extra || '';
        return `<button class="${cls}" data-action="${action}" ${extraAttrs}>${label}</button>`;
    },

    // ── Tabs ──
    tabs(items, activeId) {
        return `<div class="tabs">${items.map(item =>
            `<div class="tab${item.id === activeId ? ' active' : ''}" data-action="switch-tab" data-tab="${item.id}">${this.esc(item.label)}</div>`
        ).join('')}</div>`;
    },

    // ── Empty State ──
    emptyState(message, actionBtn) {
        return `<div class="empty-state">
            <p>${this.esc(message)}</p>
            ${actionBtn || ''}
        </div>`;
    },

    // ── Vitals Display Card ──
    vitalValue(label, value, unit) {
        if (value === null || value === undefined || value === '') return '';
        return `<div class="vital-item">
            <span class="vital-label">${this.esc(label)}</span>
            <span class="vital-value">${this.esc(String(value))}${unit ? ' ' + this.esc(unit) : ''}</span>
        </div>`;
    },

    // ── Date/Time Formatting ──
    formatDate(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    },

    formatDateTime(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
    },

    formatDateInput(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toISOString().split('T')[0];
    },

    timeAgo(dateStr) {
        if (!dateStr) return '';
        const now = new Date();
        const d = new Date(dateStr);
        const diffMs = now - d;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 30) return `${diffDays}d ago`;
        return this.formatDate(dateStr);
    },

    // ── Patient Age ──
    calculateAge(dob) {
        const today = new Date();
        const birth = new Date(dob);
        let age = today.getFullYear() - birth.getFullYear();
        const m = today.getMonth() - birth.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
        return age;
    },

    // ── Escaping ──
    esc(str) {
        if (str === null || str === undefined) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    },

    escAttr(str) {
        if (str === null || str === undefined) return '';
        return String(str).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
};
