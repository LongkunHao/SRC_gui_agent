/* ============================================================
   Elation Patient Communication — Reusable UI Components
   ============================================================ */

const Components = {

    escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },

    escapeAttr(str) {
        if (!str) return '';
        return str.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    },

    // ── Date Formatting ─────────────────────────────────────
    formatDate(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        const now = new Date();
        const diff = now - d;
        if (diff < 86400000 && d.getDate() === now.getDate()) {
            return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
        }
        if (diff < 604800000) {
            return d.toLocaleDateString('en-US', { weekday: 'short' });
        }
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    },

    formatFullDate(dateStr) {
        if (!dateStr) return '';
        return new Date(dateStr).toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        });
    },

    formatDateTime(dateStr) {
        if (!dateStr) return '';
        return new Date(dateStr).toLocaleDateString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: 'numeric', minute: '2-digit'
        });
    },

    formatShortDate(dateStr) {
        if (!dateStr) return '';
        return new Date(dateStr).toLocaleDateString('en-US', {
            month: '2-digit', day: '2-digit', year: 'numeric'
        });
    },

    formatTime(dateStr) {
        if (!dateStr) return '';
        return new Date(dateStr).toLocaleTimeString('en-US', {
            hour: 'numeric', minute: '2-digit'
        });
    },

    timeAgo(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        const now = new Date();
        const diff = Math.floor((now - d) / 1000);
        if (diff < 60) return 'just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
        return this.formatDate(dateStr);
    },

    // ── Avatar ──────────────────────────────────────────────
    avatar(name, color, size) {
        size = size || 36;
        const initials = (name || '?').split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
        return `<div class="avatar" style="width:${size}px;height:${size}px;background:${color || '#6B7280'};font-size:${Math.round(size * 0.4)}px" title="${this.escapeAttr(name)}">${this.escapeHtml(initials)}</div>`;
    },

    // ── Passport Status Badge ───────────────────────────────
    passportBadge(status) {
        const map = {
            'registered': { cls: 'badge-green', text: 'Registered', icon: '&#x1F310;' },
            'invited': { cls: 'badge-yellow', text: 'Invited', icon: '&#x1F310;' },
            'not_invited': { cls: 'badge-gray', text: 'Not Invited', icon: '&#x1F310;' }
        };
        const m = map[status] || map['not_invited'];
        return `<span class="passport-badge ${m.cls}" data-testid="passport-status-${status}"><span class="passport-icon">${m.icon}</span> ${m.text}</span>`;
    },

    // ── SMS Opt-In Badge ────────────────────────────────────
    smsOptInBadge(status) {
        const map = {
            'opted_in': { cls: 'badge-green', text: 'SMS Opted In' },
            'opted_out': { cls: 'badge-red', text: 'SMS Opted Out' },
            'never': { cls: 'badge-gray', text: 'SMS Not Opted In' }
        };
        const m = map[status] || map['never'];
        return `<span class="sms-badge ${m.cls}" data-testid="sms-status-${status}">${m.text}</span>`;
    },

    // ── Custom Dropdown ─────────────────────────────────────
    dropdown(id, options, selectedValue, opts) {
        const label = opts?.label || '';
        const placeholder = opts?.placeholder || 'Select...';
        const selected = options.find(o => o.value === selectedValue);
        const displayText = selected ? this.escapeHtml(selected.label) : placeholder;
        let html = '';
        if (label) html += `<label class="form-label">${this.escapeHtml(label)}</label>`;
        html += `<div class="custom-dropdown" id="${id}" data-dropdown="${id}" data-testid="${id}">`;
        html += `<div class="dropdown-trigger" data-dropdown="${id}">${displayText}<span class="dropdown-arrow">&#x25BC;</span></div>`;
        html += `<div class="dropdown-menu" id="${id}-menu">`;
        for (const opt of options) {
            const sel = opt.value === selectedValue ? ' selected' : '';
            html += `<div class="dropdown-item${sel}" data-value="${this.escapeAttr(String(opt.value))}" data-dropdown-id="${id}">${this.escapeHtml(opt.label)}</div>`;
        }
        html += '</div></div>';
        return html;
    },

    // ── Custom Toggle ───────────────────────────────────────
    toggle(id, checked, label, description) {
        let html = `<div class="toggle-row" data-testid="${id}">`;
        html += `<div class="toggle-info">`;
        if (label) html += `<div class="toggle-label">${this.escapeHtml(label)}</div>`;
        if (description) html += `<div class="toggle-description">${this.escapeHtml(description)}</div>`;
        html += `</div>`;
        html += `<label class="toggle-switch"><input type="checkbox" id="${id}" ${checked ? 'checked' : ''} data-toggle="${id}"><span class="toggle-slider"></span></label>`;
        html += '</div>';
        return html;
    },

    // ── Text Input ──────────────────────────────────────────
    textInput(id, value, opts) {
        const label = opts?.label || '';
        const placeholder = opts?.placeholder || '';
        const type = opts?.type || 'text';
        const required = opts?.required ? ' required' : '';
        let html = '';
        if (label) html += `<label class="form-label" for="${id}">${this.escapeHtml(label)}${opts?.required ? ' <span class="required">*</span>' : ''}</label>`;
        html += `<input type="${type}" id="${id}" class="form-input" value="${this.escapeAttr(value || '')}" placeholder="${this.escapeAttr(placeholder)}" data-testid="${id}"${required}>`;
        return html;
    },

    // ── Text Area ───────────────────────────────────────────
    textArea(id, value, opts) {
        const label = opts?.label || '';
        const placeholder = opts?.placeholder || '';
        const rows = opts?.rows || 4;
        let html = '';
        if (label) html += `<label class="form-label" for="${id}">${this.escapeHtml(label)}${opts?.required ? ' <span class="required">*</span>' : ''}</label>`;
        html += `<textarea id="${id}" class="form-textarea" rows="${rows}" placeholder="${this.escapeAttr(placeholder)}" data-testid="${id}">${this.escapeHtml(value || '')}</textarea>`;
        return html;
    },

    // ── Checkbox ────────────────────────────────────────────
    checkbox(id, checked, label) {
        return `<label class="checkbox-label" data-testid="${id}"><input type="checkbox" id="${id}" ${checked ? 'checked' : ''} data-checkbox="${id}"><span class="checkbox-text">${this.escapeHtml(label)}</span></label>`;
    },

    // ── Radio Group ─────────────────────────────────────────
    radioGroup(name, options, selectedValue) {
        let html = `<div class="radio-group" data-radio-group="${name}">`;
        for (const opt of options) {
            const checked = opt.value === selectedValue ? ' checked' : '';
            html += `<label class="radio-option"><input type="radio" name="${name}" value="${this.escapeAttr(String(opt.value))}"${checked} data-radio="${name}"><span class="radio-text">${this.escapeHtml(opt.label)}</span>`;
            if (opt.description) html += `<span class="radio-description">${this.escapeHtml(opt.description)}</span>`;
            html += '</label>';
        }
        html += '</div>';
        return html;
    },

    // ── Tag ─────────────────────────────────────────────────
    tag(text, opts) {
        const removable = opts?.removable ? `<span class="tag-remove" data-action="remove-tag" data-tag="${this.escapeAttr(text)}" data-patient="${opts.patientId || ''}">&times;</span>` : '';
        const cls = opts?.cls || '';
        return `<span class="tag ${cls}">${this.escapeHtml(text)}${removable}</span>`;
    },

    // ── Info/Warning/Error Boxes ────────────────────────────
    infoBox(text) {
        return `<div class="info-box"><span class="box-icon">i</span> ${this.escapeHtml(text)}</div>`;
    },

    warningBox(text) {
        return `<div class="warning-box"><span class="box-icon">!</span> ${this.escapeHtml(text)}</div>`;
    },

    errorBox(text) {
        return `<div class="error-box"><span class="box-icon">x</span> ${this.escapeHtml(text)}</div>`;
    },

    successBox(text) {
        return `<div class="success-box"><span class="box-icon">&#x2713;</span> ${this.escapeHtml(text)}</div>`;
    },

    // ── Modal ───────────────────────────────────────────────
    showModal(title, bodyHtml, footerHtml) {
        const overlay = document.getElementById('modalOverlay');
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('modalBody').innerHTML = bodyHtml;
        document.getElementById('modalFooter').innerHTML = footerHtml || '';
        overlay.style.display = 'flex';
    },

    closeModal() {
        document.getElementById('modalOverlay').style.display = 'none';
    },

    confirm(title, message, onConfirm) {
        this.showModal(title, `<p>${this.escapeHtml(message)}</p>`,
            `<button class="btn btn-secondary" data-action="close-modal">Cancel</button>
             <button class="btn btn-primary" data-action="confirm-modal">Confirm</button>`
        );
        window._modalConfirmCallback = onConfirm;
    },

    confirmDanger(title, message, onConfirm) {
        this.showModal(title, `<p>${this.escapeHtml(message)}</p>`,
            `<button class="btn btn-secondary" data-action="close-modal">Cancel</button>
             <button class="btn btn-danger" data-action="confirm-modal">Confirm</button>`
        );
        window._modalConfirmCallback = onConfirm;
    },

    // ── Toast ───────────────────────────────────────────────
    showToast(message, type) {
        type = type || 'info';
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    // ── Empty State ─────────────────────────────────────────
    emptyState(icon, title, text) {
        return `<div class="empty-state"><div class="empty-icon">${icon}</div><h3>${this.escapeHtml(title)}</h3><p>${this.escapeHtml(text)}</p></div>`;
    },

    // ── Pagination ──────────────────────────────────────────
    pagination(page, totalPages, total) {
        if (totalPages <= 1) return '';
        const start = (page - 1) * AppState.patientListPageSize + 1;
        const end = Math.min(page * AppState.patientListPageSize, total);
        let html = `<div class="pagination" data-testid="pagination">`;
        html += `<span class="page-info">${start}-${end} of ${total}</span>`;
        html += `<button class="btn btn-icon" data-action="prev-page" ${page <= 1 ? 'disabled' : ''}>&#x25C0;</button>`;
        html += `<button class="btn btn-icon" data-action="next-page" ${page >= totalPages ? 'disabled' : ''}>&#x25B6;</button>`;
        html += '</div>';
        return html;
    },

    // ── Attachment Display ───────────────────────────────────
    attachment(att) {
        return `<div class="attachment-chip"><span class="attachment-icon">&#x1F4CE;</span><span class="attachment-name">${this.escapeHtml(att.name)}</span><span class="attachment-size">${this.escapeHtml(att.size || '')}</span></div>`;
    }
};
