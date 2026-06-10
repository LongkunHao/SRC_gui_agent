// ============================================================
// components.js — Reusable UI components for Superhuman Mail
// ============================================================

const Components = {

    escapeHtml(str) {
        if (!str) return '';
        return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
    },

    escapeAttr(str) {
        return this.escapeHtml(str);
    },

    formatDate(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        const now = new Date();
        const diff = now - d;
        const oneDay = 86400000;

        if (diff < oneDay && d.getDate() === now.getDate()) {
            return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
        }
        if (diff < 7 * oneDay) {
            return d.toLocaleDateString('en-US', { weekday: 'short' });
        }
        if (d.getFullYear() === now.getFullYear()) {
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },

    formatFullDate(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) +
            ' at ' + d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
    },

    formatTime(time) {
        if (!time) return '';
        const [h, m] = time.split(':');
        const hour = parseInt(h);
        const ampm = hour >= 12 ? 'PM' : 'AM';
        const h12 = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
        return `${h12}:${m} ${ampm}`;
    },

    formatDateShort(dateStr) {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    },

    avatar(name, color, size) {
        size = size || 32;
        const initials = (name || '?').split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
        return `<div class="avatar" style="width:${size}px;height:${size}px;background:${color || '#6C4FF7'};font-size:${Math.floor(size * 0.4)}px" data-testid="avatar-${this.escapeAttr(name)}">${initials}</div>`;
    },

    badge(count) {
        if (!count || count <= 0) return '';
        return `<span class="badge">${count > 99 ? '99+' : count}</span>`;
    },

    toggle(id, checked, label, description) {
        return `<div class="toggle-row" data-testid="toggle-${id}">
            <div class="toggle-info">
                <div class="toggle-label">${this.escapeHtml(label)}</div>
                ${description ? `<div class="toggle-description">${this.escapeHtml(description)}</div>` : ''}
            </div>
            <label class="toggle-switch">
                <input type="checkbox" id="${id}" name="${id}" ${checked ? 'checked' : ''} data-testid="toggle-input-${id}">
                <span class="toggle-slider"></span>
            </label>
        </div>`;
    },

    dropdown(id, options, selectedValue, label) {
        const selectedOpt = options.find(o => o.value === selectedValue) || options[0];
        return `<div class="dropdown-wrapper" data-testid="dropdown-${id}">
            ${label ? `<label class="dropdown-label">${this.escapeHtml(label)}</label>` : ''}
            <div class="custom-dropdown" id="${id}" data-value="${this.escapeAttr(selectedValue || '')}">
                <div class="dropdown-trigger" data-action="toggle-dropdown" data-dropdown-id="${id}" data-testid="dropdown-trigger-${id}">
                    <span class="dropdown-value">${this.escapeHtml(selectedOpt ? selectedOpt.label : 'Select...')}</span>
                    <span class="dropdown-arrow">&#9662;</span>
                </div>
                <div class="dropdown-menu" id="${id}-menu" style="display:none">
                    ${options.map(o => `<div class="dropdown-item${o.value === selectedValue ? ' selected' : ''}" data-action="select-dropdown" data-dropdown-id="${id}" data-value="${this.escapeAttr(o.value)}" data-testid="dropdown-option-${id}-${this.escapeAttr(o.value)}">${this.escapeHtml(o.label)}</div>`).join('')}
                </div>
            </div>
        </div>`;
    },

    radioGroup(name, options, selectedValue) {
        return `<div class="radio-group" data-testid="radio-${name}">
            ${options.map(o => `<label class="radio-option${o.value === selectedValue ? ' selected' : ''}">
                <input type="radio" name="${name}" value="${this.escapeAttr(o.value)}" ${o.value === selectedValue ? 'checked' : ''} data-testid="radio-${name}-${this.escapeAttr(o.value)}">
                <span class="radio-dot"></span>
                <span class="radio-label">${this.escapeHtml(o.label)}</span>
                ${o.description ? `<span class="radio-desc">${this.escapeHtml(o.description)}</span>` : ''}
            </label>`).join('')}
        </div>`;
    },

    textInput(id, value, placeholder, label) {
        return `<div class="input-wrapper" data-testid="input-${id}">
            ${label ? `<label class="input-label" for="${id}">${this.escapeHtml(label)}</label>` : ''}
            <input type="text" id="${id}" name="${id}" value="${this.escapeAttr(value || '')}" placeholder="${this.escapeAttr(placeholder || '')}" class="text-input" data-testid="input-field-${id}">
        </div>`;
    },

    // Toast notification
    showToast(message, type, duration) {
        type = type || 'info';
        duration = duration || 3000;
        const container = document.getElementById('toastContainer');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `<span>${this.escapeHtml(message)}</span>`;
        container.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('toast-visible'));
        setTimeout(() => {
            toast.classList.remove('toast-visible');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    // Confirmation modal
    showModal(title, bodyHtml, actions) {
        const overlay = document.getElementById('modalOverlay');
        const titleEl = document.getElementById('modalTitle');
        const bodyEl = document.getElementById('modalBody');
        const footerEl = document.getElementById('modalFooter');
        if (!overlay) return;

        titleEl.textContent = title;
        bodyEl.innerHTML = bodyHtml;
        footerEl.innerHTML = (actions || []).map(a =>
            `<button class="btn ${a.primary ? 'btn-primary' : 'btn-secondary'} ${a.danger ? 'btn-danger' : ''}" data-action="${a.action}" data-testid="modal-${a.action}">${this.escapeHtml(a.label)}</button>`
        ).join('');
        overlay.style.display = 'flex';
    },

    closeModal() {
        const overlay = document.getElementById('modalOverlay');
        if (overlay) overlay.style.display = 'none';
    },

    // Star icon
    starIcon(isStarred) {
        if (isStarred) {
            return '<span class="star-icon starred" title="Starred">&#9733;</span>';
        }
        return '<span class="star-icon" title="Star">&#9734;</span>';
    },

    // Read receipt indicator
    readReceiptIcon(receipt) {
        if (!receipt) return '';
        if (receipt.opened) {
            return `<span class="read-receipt read-receipt-opened" title="Opened ${receipt.openCount || 1} time(s)">&#10003;&#10003;</span>`;
        }
        return '<span class="read-receipt read-receipt-sent" title="Sent">&#10003;</span>';
    },

    // Attachment icon
    attachmentIcon() {
        return '<span class="attachment-icon" title="Has attachments">&#128206;</span>';
    },

    // Unread dot
    unreadDot(type) {
        const colors = { unread: '#4A90FF', reminder: '#9B59B6', starred: '#F5A623' };
        return `<span class="unread-dot" style="background:${colors[type] || colors.unread}"></span>`;
    },

    // Reminder time options
    reminderOptions() {
        const now = new Date();
        const options = [];

        // Later today (3 hours from now)
        const laterToday = new Date(now.getTime() + 3 * 3600000);
        options.push({ label: 'Later today', sublabel: this.formatTime(laterToday.getHours() + ':00'), value: laterToday.toISOString() });

        // Tomorrow morning
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(9, 0, 0, 0);
        options.push({ label: 'Tomorrow', sublabel: 'Tomorrow 9:00 AM', value: tomorrow.toISOString() });

        // This weekend
        const daysUntilSat = (6 - now.getDay() + 7) % 7 || 7;
        const weekend = new Date(now);
        weekend.setDate(weekend.getDate() + daysUntilSat);
        weekend.setHours(9, 0, 0, 0);
        options.push({ label: 'This weekend', sublabel: this.formatDateShort(weekend.toISOString()), value: weekend.toISOString() });

        // Next week (next Monday)
        const daysUntilMon = (1 - now.getDay() + 7) % 7 || 7;
        const nextWeek = new Date(now);
        nextWeek.setDate(nextWeek.getDate() + daysUntilMon);
        nextWeek.setHours(9, 0, 0, 0);
        options.push({ label: 'Next week', sublabel: this.formatDateShort(nextWeek.toISOString()), value: nextWeek.toISOString() });

        // In 2 weeks
        const twoWeeks = new Date(nextWeek);
        twoWeeks.setDate(twoWeeks.getDate() + 7);
        options.push({ label: 'In 2 weeks', sublabel: this.formatDateShort(twoWeeks.toISOString()), value: twoWeeks.toISOString() });

        // Next month
        const nextMonth = new Date(now);
        nextMonth.setMonth(nextMonth.getMonth() + 1, 1);
        nextMonth.setHours(9, 0, 0, 0);
        options.push({ label: 'Next month', sublabel: this.formatDateShort(nextMonth.toISOString()), value: nextMonth.toISOString() });

        return options;
    },

    // Label chip
    labelChip(label, removable) {
        return `<span class="label-chip" style="background:${label.color || '#666'}" data-testid="label-${this.escapeAttr(label.id)}">
            ${this.escapeHtml(label.name)}
            ${removable ? `<span class="label-remove" data-action="remove-label-chip" data-label-id="${label.id}">&times;</span>` : ''}
        </span>`;
    },

    // Color palette for labels
    colorPalette(selectedColor) {
        const colors = ['#6C4FF7', '#E54D89', '#F44336', '#FF5722', '#FF9800', '#FBBC04', '#CDDC39', '#8BC34A', '#4CAF50', '#34A853', '#009688', '#00BCD4', '#2196F3', '#3F51B5', '#673AB7', '#9C27B0', '#795548', '#607D8B'];
        return `<div class="color-palette" data-testid="color-palette">
            ${colors.map(c => `<div class="color-swatch${c === selectedColor ? ' selected' : ''}" style="background:${c}" data-action="select-color" data-color="${c}" data-testid="color-${c}"></div>`).join('')}
        </div>`;
    },

    // Empty state
    emptyState(icon, title, description) {
        return `<div class="empty-state" data-testid="empty-state">
            <div class="empty-state-icon">${icon || ''}</div>
            <div class="empty-state-title">${this.escapeHtml(title)}</div>
            ${description ? `<div class="empty-state-desc">${this.escapeHtml(description)}</div>` : ''}
        </div>`;
    },

    // Keyboard shortcut hint
    shortcutHint(key) {
        return `<kbd class="shortcut-key">${this.escapeHtml(key)}</kbd>`;
    }
};
