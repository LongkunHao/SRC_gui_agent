const Components = {

    escapeHtml(str) {
        if (str == null) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    },

    escapeAttr(str) {
        if (str == null) return '';
        return String(str).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    },

    formatDate(isoStr) {
        if (!isoStr) return '';
        const d = new Date(isoStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },

    formatDateTime(isoStr) {
        if (!isoStr) return '';
        const d = new Date(isoStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true });
    },

    formatRelativeDate(isoStr) {
        if (!isoStr) return '';
        const d = new Date(isoStr);
        const now = new Date();
        const diffDays = Math.floor((now - d) / 86400000);
        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        return Components.formatDate(isoStr);
    },

    showToast(message, duration) {
        const container = document.getElementById('toastContainer');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `<span>${Components.escapeHtml(message)}</span>`;
        container.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('removing');
            setTimeout(() => toast.remove(), 300);
        }, duration || 4000);
    },

    showModal(title, bodyHtml, footerHtml) {
        const overlay = document.getElementById('modalOverlay');
        if (!overlay) return;
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('modalBody').innerHTML = bodyHtml;
        document.getElementById('modalFooter').innerHTML = footerHtml || '';
        overlay.style.display = 'flex';
    },

    closeModal() {
        const overlay = document.getElementById('modalOverlay');
        if (overlay) overlay.style.display = 'none';
    },

    badge(text, type) {
        const cls = type ? `badge badge-${type}` : 'badge';
        return `<span class="${cls}">${Components.escapeHtml(text)}</span>`;
    },

    statusBadge(status) {
        const map = {
            active: { label: 'Active', type: 'success' },
            discontinued: { label: 'Discontinued', type: 'danger' },
            canceled: { label: 'Canceled', type: 'danger' },
            pending: { label: 'Pending', type: 'warning' },
            approved: { label: 'Approved', type: 'success' },
            denied: { label: 'Denied', type: 'danger' }
        };
        const info = map[status] || { label: status, type: 'default' };
        return Components.badge(info.label, info.type);
    },

    severityBadge(severity) {
        const map = {
            major: 'danger',
            moderate: 'warning',
            minor: 'info',
            Severe: 'danger',
            Moderate: 'warning',
            Mild: 'info'
        };
        return Components.badge(severity, map[severity] || 'default');
    },

    formularyBadge(status) {
        const map = {
            preferred: { label: 'Preferred', type: 'success' },
            on_formulary: { label: 'On Formulary', type: 'info' },
            non_formulary: { label: 'Non-Formulary', type: 'warning' },
            non_reimbursable: { label: 'Non-Reimbursable', type: 'danger' }
        };
        const info = map[status] || { label: 'Unknown', type: 'default' };
        return Components.badge(info.label, info.type);
    },

    dropdown(id, options, selectedValue, placeholder, triggerClass) {
        const selected = options.find(o => (o.id || o.value) === selectedValue);
        const displayText = selected ? (selected.name || selected.label || selected.text) : (placeholder || 'Select...');
        let html = `<div class="custom-dropdown" id="${Components.escapeAttr(id)}" data-testid="${Components.escapeAttr(id)}">`;
        html += `<div class="dropdown-trigger ${triggerClass || ''}" data-dropdown="${Components.escapeAttr(id)}">`;
        html += `<span class="dropdown-trigger-text">${Components.escapeHtml(displayText)}</span>`;
        html += `<span class="dropdown-arrow">&#9662;</span></div>`;
        html += `<div class="dropdown-menu" id="${Components.escapeAttr(id)}-menu">`;
        for (const opt of options) {
            const val = opt.id || opt.value;
            const label = opt.name || opt.label || opt.text;
            const isSelected = val === selectedValue;
            const desc = opt.description ? `<span class="dropdown-item-desc">${Components.escapeHtml(opt.description)}</span>` : '';
            html += `<div class="dropdown-item${isSelected ? ' selected' : ''}" data-value="${Components.escapeAttr(val)}" data-dropdown-id="${Components.escapeAttr(id)}" data-testid="${Components.escapeAttr(id)}-option-${Components.escapeAttr(val)}">`;
            if (isSelected) html += '<span class="check">&#10003;</span>';
            else html += '<span class="check"></span>';
            html += `<span class="dropdown-item-label">${Components.escapeHtml(label)}</span>${desc}`;
            html += '</div>';
        }
        html += '</div></div>';
        return html;
    },

    textInput(id, value, placeholder, required, label) {
        let html = '';
        if (label) {
            html += `<label class="form-label" for="${Components.escapeAttr(id)}">${Components.escapeHtml(label)}`;
            if (required) html += ' <span class="required">*</span>';
            html += '</label>';
        }
        html += `<input type="text" class="form-input" id="${Components.escapeAttr(id)}" data-testid="${Components.escapeAttr(id)}" value="${Components.escapeAttr(value || '')}" placeholder="${Components.escapeAttr(placeholder || '')}"${required ? ' required' : ''}>`;
        return html;
    },

    numberInput(id, value, placeholder, required, label, min, max) {
        let html = '';
        if (label) {
            html += `<label class="form-label" for="${Components.escapeAttr(id)}">${Components.escapeHtml(label)}`;
            if (required) html += ' <span class="required">*</span>';
            html += '</label>';
        }
        html += `<input type="number" class="form-input" id="${Components.escapeAttr(id)}" data-testid="${Components.escapeAttr(id)}" value="${Components.escapeAttr(value != null ? String(value) : '')}" placeholder="${Components.escapeAttr(placeholder || '')}"`;
        if (min != null) html += ` min="${min}"`;
        if (max != null) html += ` max="${max}"`;
        if (required) html += ' required';
        html += '>';
        return html;
    },

    textarea(id, value, placeholder, rows, label) {
        let html = '';
        if (label) {
            html += `<label class="form-label" for="${Components.escapeAttr(id)}">${Components.escapeHtml(label)}</label>`;
        }
        html += `<textarea class="form-input form-textarea" id="${Components.escapeAttr(id)}" data-testid="${Components.escapeAttr(id)}" rows="${rows || 3}" placeholder="${Components.escapeAttr(placeholder || '')}">${Components.escapeHtml(value || '')}</textarea>`;
        return html;
    },

    checkbox(id, checked, label) {
        let html = `<label class="checkbox-label" data-testid="${Components.escapeAttr(id)}">`;
        html += `<input type="checkbox" id="${Components.escapeAttr(id)}"${checked ? ' checked' : ''}>`;
        html += `<span class="checkbox-custom"></span>`;
        html += `<span class="checkbox-text">${Components.escapeHtml(label)}</span></label>`;
        return html;
    },

    toggle(id, checked, label, description) {
        let html = '<div class="toggle-row">';
        html += '<div class="toggle-info">';
        html += `<div class="toggle-label">${Components.escapeHtml(label)}</div>`;
        if (description) html += `<div class="toggle-desc">${Components.escapeHtml(description)}</div>`;
        html += '</div>';
        html += `<label class="toggle-switch" data-testid="${Components.escapeAttr(id)}">`;
        html += `<input type="checkbox" id="${Components.escapeAttr(id)}"${checked ? ' checked' : ''}>`;
        html += '<span class="toggle-slider"></span></label></div>';
        return html;
    },

    radioGroup(name, options, selectedValue) {
        let html = '<div class="radio-group">';
        for (const opt of options) {
            const val = opt.value || opt.id;
            const isSelected = val === selectedValue;
            html += `<label class="radio-label" data-testid="${Components.escapeAttr(name)}-${Components.escapeAttr(val)}">`;
            html += `<input type="radio" name="${Components.escapeAttr(name)}" value="${Components.escapeAttr(val)}"${isSelected ? ' checked' : ''}>`;
            html += `<span class="radio-custom"></span>`;
            html += `<span class="radio-text">${Components.escapeHtml(opt.label || opt.name)}</span></label>`;
        }
        html += '</div>';
        return html;
    },

    alertBox(type, title, message) {
        const iconMap = { info: 'i', warning: '!', error: '&#10005;', success: '&#10003;' };
        let html = `<div class="alert-box alert-${type}" data-testid="alert-${type}">`;
        html += `<span class="alert-icon">${iconMap[type] || 'i'}</span>`;
        html += '<div class="alert-content">';
        if (title) html += `<div class="alert-title">${Components.escapeHtml(title)}</div>`;
        html += `<div class="alert-message">${Components.escapeHtml(message)}</div>`;
        html += '</div></div>';
        return html;
    },

    drugInteractionAlert(interaction) {
        const borderClass = interaction.severity === 'major' ? 'alert-error' : interaction.severity === 'moderate' ? 'alert-warning' : 'alert-info';
        let html = `<div class="drug-interaction-alert ${borderClass}" data-testid="drug-interaction-${Components.escapeAttr(interaction.id)}">`;
        html += `<div class="dia-header">`;
        html += `<span class="dia-severity">${Components.severityBadge(interaction.severity)}</span>`;
        html += `<span class="dia-drugs">${Components.escapeHtml(interaction.drug1)} + ${Components.escapeHtml(interaction.drug2)}</span>`;
        html += '</div>';
        html += `<div class="dia-description">${Components.escapeHtml(interaction.description)}</div>`;
        html += `<div class="dia-recommendation"><strong>Recommendation:</strong> ${Components.escapeHtml(interaction.recommendation)}</div>`;
        html += '</div>';
        return html;
    },

    allergyAlert(alert) {
        let html = `<div class="drug-interaction-alert alert-error" data-testid="allergy-alert">`;
        html += `<div class="dia-header">`;
        html += `<span class="dia-severity">${Components.badge('Drug-Allergy Alert', 'danger')}</span>`;
        html += `<span class="dia-drugs">${Components.escapeHtml(alert.medication)} - Allergy: ${Components.escapeHtml(alert.allergen)}</span>`;
        html += '</div>';
        html += `<div class="dia-description">Patient is allergic to ${Components.escapeHtml(alert.allergen)}. Reaction: ${Components.escapeHtml(alert.reaction)} (Severity: ${Components.escapeHtml(alert.severity)})</div>`;
        html += '</div>';
        return html;
    },

    emptyState(icon, message) {
        return `<div class="empty-state"><div class="empty-state-icon">${icon || ''}</div><div class="empty-state-text">${Components.escapeHtml(message)}</div></div>`;
    },

    icon(name) {
        const icons = {
            pill: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 0l-3 3m6-3l3 3"/></svg>',
            rx: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><text x="4" y="18" font-size="16" fill="currentColor" stroke="none" font-weight="bold">Rx</text></svg>',
            search: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>',
            plus: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
            check: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>',
            x: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
            refresh: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>',
            settings: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
            clock: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
            trash: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>',
            edit: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
            alert: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            pharmacy: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>',
            chevronDown: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>',
            chevronRight: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>',
            list: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>',
            inbox: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
            user: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
            file: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
            shield: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
        };
        return icons[name] || '';
    }
};
