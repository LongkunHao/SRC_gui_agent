// ============================================================
// components.js — Reusable UI components for PayPal My Wallet
// ============================================================

const Components = {

    // ---- Toast Notification ----
    showToast(message, type = 'success') {
        const existing = document.querySelector('.toast-notification');
        if (existing) existing.remove();
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        const icons = { success: 'check_circle', error: 'error', warning: 'warning', info: 'info' };
        toast.innerHTML = `
            <span class="toast-icon material-icons">${icons[type] || 'info'}</span>
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    },

    // ---- Modal ----
    openModal(id, title, bodyHtml, footerHtml, options = {}) {
        const existing = document.getElementById('modal-overlay');
        if (existing) existing.remove();
        const width = options.width || '520px';
        const modal = document.createElement('div');
        modal.id = 'modal-overlay';
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal" style="max-width:${width}">
                <div class="modal-header">
                    <h2>${title}</h2>
                    <button class="modal-close-btn" data-action="close-modal">&times;</button>
                </div>
                <div class="modal-body" id="modal-body-content">
                    ${bodyHtml}
                </div>
                ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
            </div>
        `;
        document.body.appendChild(modal);
        AppState.modalOpen = id;
        setTimeout(() => modal.classList.add('show'), 10);
    },

    closeModal() {
        const modal = document.getElementById('modal-overlay');
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 200);
        }
        AppState.modalOpen = null;
        AppState.modalData = null;
    },

    // ---- Confirmation Dialog ----
    confirmDialog(title, message, onConfirm, confirmText = 'Confirm', danger = false) {
        const bodyHtml = `<p class="confirm-message">${message}</p>`;
        const footerHtml = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn ${danger ? 'btn-danger' : 'btn-primary'}" data-action="confirm-dialog">${confirmText}</button>
        `;
        this.openModal('confirm', title, bodyHtml, footerHtml);
        AppState._confirmCallback = onConfirm;
    },

    // ---- Custom Dropdown ----
    renderDropdown(id, options, selectedValue, placeholder = 'Select...', disabled = false) {
        const selected = options.find(o => o.value === selectedValue);
        return `
            <div class="custom-dropdown ${disabled ? 'disabled' : ''}" id="${id}" data-dropdown="${id}">
                <div class="dropdown-trigger" data-action="toggle-dropdown" data-dropdown-id="${id}">
                    <span class="dropdown-value">${selected ? selected.label : placeholder}</span>
                    <span class="dropdown-arrow material-icons">expand_more</span>
                </div>
                <div class="dropdown-menu" id="${id}-menu">
                    ${options.map(o => `
                        <div class="dropdown-item ${o.value === selectedValue ? 'selected' : ''}"
                             data-action="select-dropdown-item"
                             data-dropdown-id="${id}"
                             data-value="${o.value}">
                            ${o.label}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    },

    toggleDropdown(dropdownId) {
        const menu = document.getElementById(`${dropdownId}-menu`);
        if (!menu) return;
        const isOpen = menu.classList.contains('open');
        document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
        if (!isOpen) menu.classList.add('open');
    },

    // ---- Card Icons ----
    getCardBrandIcon(brand) {
        const icons = {
            'Visa': '<span class="card-brand visa">VISA</span>',
            'Mastercard': '<span class="card-brand mastercard">MC</span>',
            'American Express': '<span class="card-brand amex">AMEX</span>',
            'Discover': '<span class="card-brand discover">DISC</span>'
        };
        return icons[brand] || `<span class="card-brand">${brand}</span>`;
    },

    // ---- Format Helpers ----
    formatCurrency(amount, currency = 'USD') {
        const curr = CURRENCIES.find(c => c.code === currency);
        const symbol = curr ? curr.symbol : '$';
        const absAmount = Math.abs(amount);
        if (currency === 'JPY' || currency === 'HUF') {
            return `${amount < 0 ? '-' : ''}${symbol}${Math.round(absAmount).toLocaleString()}`;
        }
        return `${amount < 0 ? '-' : ''}${symbol}${absAmount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    },

    formatDate(dateStr) {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },

    formatDateTime(dateStr) {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
    },

    formatRelativeDate(dateStr) {
        const d = new Date(dateStr);
        const now = new Date();
        const diff = now - d;
        const mins = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);
        if (mins < 1) return 'Just now';
        if (mins < 60) return `${mins}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;
        return this.formatDate(dateStr);
    },

    formatPercent(value) {
        return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
    },

    // ---- Status Badges ----
    renderStatusBadge(status) {
        const labels = {
            'confirmed': 'Confirmed',
            'pending_confirmation': 'Pending',
            'expired': 'Expired',
            'active': 'Active',
            'completed': 'Completed',
            'upcoming': 'Upcoming',
            'paid': 'Paid',
            'saved': 'Saved',
            'available': 'Available',
            'used': 'Used',
            'partially_used': 'Partially Used',
            'pending': 'Pending'
        };
        const classes = {
            'confirmed': 'badge-success',
            'active': 'badge-success',
            'completed': 'badge-success',
            'paid': 'badge-success',
            'pending_confirmation': 'badge-warning',
            'pending': 'badge-warning',
            'upcoming': 'badge-info',
            'available': 'badge-info',
            'saved': 'badge-primary',
            'expired': 'badge-danger',
            'used': 'badge-neutral',
            'partially_used': 'badge-warning'
        };
        return `<span class="status-badge ${classes[status] || 'badge-neutral'}">${labels[status] || status}</span>`;
    },

    // ---- Empty State ----
    renderEmptyState(icon, title, subtitle) {
        return `
            <div class="empty-state">
                <span class="material-icons empty-state-icon">${icon}</span>
                <h3>${title}</h3>
                <p>${subtitle}</p>
            </div>
        `;
    },

    // ---- Pagination ----
    renderPagination(currentPage, totalPages, totalCount) {
        if (totalPages <= 1) return '';
        const start = (currentPage - 1) * AppState.itemsPerPage + 1;
        const end = Math.min(currentPage * AppState.itemsPerPage, totalCount);
        let pages = '';
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
                pages += `<button class="page-btn ${i === currentPage ? 'active' : ''}" data-action="go-to-page" data-page="${i}">${i}</button>`;
            } else if (i === currentPage - 2 || i === currentPage + 2) {
                pages += '<span class="page-ellipsis">...</span>';
            }
        }
        return `
            <div class="pagination">
                <span class="pagination-info">${start}-${end} of ${totalCount}</span>
                <div class="pagination-controls">
                    <button class="page-btn" data-action="go-to-page" data-page="${Math.max(1, currentPage - 1)}" ${currentPage === 1 ? 'disabled' : ''}>
                        <span class="material-icons">chevron_left</span>
                    </button>
                    ${pages}
                    <button class="page-btn" data-action="go-to-page" data-page="${Math.min(totalPages, currentPage + 1)}" ${currentPage === totalPages ? 'disabled' : ''}>
                        <span class="material-icons">chevron_right</span>
                    </button>
                </div>
            </div>
        `;
    },

    // ---- Toggle Switch ----
    renderToggle(id, checked, label, name) {
        return `
            <div class="toggle-row">
                <label class="toggle-label" for="${id}">${label}</label>
                <div class="toggle-switch ${checked ? 'on' : ''}" id="${id}" data-action="toggle-switch" data-toggle-name="${name || id}">
                    <div class="toggle-track">
                        <div class="toggle-thumb"></div>
                    </div>
                </div>
            </div>
        `;
    },

    // ---- Info Row ----
    renderInfoRow(label, value, actionHtml) {
        return `
            <div class="info-row">
                <span class="info-label">${label}</span>
                <div class="info-value-group">
                    <span class="info-value">${value}</span>
                    ${actionHtml || ''}
                </div>
            </div>
        `;
    },

    // ---- Section Header ----
    renderSectionHeader(title, actionHtml) {
        return `
            <div class="section-header">
                <h3>${title}</h3>
                ${actionHtml ? `<div class="section-actions">${actionHtml}</div>` : ''}
            </div>
        `;
    },

    // ---- Progress Bar ----
    renderProgressBar(current, total, label) {
        const pct = total > 0 ? Math.min(100, (current / total) * 100) : 0;
        return `
            <div class="progress-container">
                ${label ? `<div class="progress-label">${label}</div>` : ''}
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${pct}%"></div>
                </div>
            </div>
        `;
    },

    // ---- Tabs ----
    renderTabs(tabs, activeTab) {
        return `
            <div class="tab-bar">
                ${tabs.map(t => `
                    <button class="tab-btn ${t.id === activeTab ? 'active' : ''}" data-action="switch-tab" data-tab="${t.id}">
                        ${t.icon ? `<span class="material-icons tab-icon">${t.icon}</span>` : ''}
                        ${t.label}
                        ${t.count !== undefined ? `<span class="tab-count">${t.count}</span>` : ''}
                    </button>
                `).join('')}
            </div>
        `;
    },

    // ---- Transaction Type Icon ----
    getTransactionIcon(type) {
        const icons = {
            'payment': 'shopping_cart',
            'received': 'arrow_downward',
            'transfer_in': 'account_balance',
            'transfer_out': 'account_balance',
            'crypto_buy': 'currency_bitcoin',
            'crypto_sell': 'currency_bitcoin',
            'refund': 'replay',
            'savings_deposit': 'savings',
            'savings_withdrawal': 'savings',
            'currency_convert': 'currency_exchange',
            'gift_card': 'card_giftcard',
            'pending': 'schedule'
        };
        return icons[type] || 'payment';
    },

    // ---- Card Visual ----
    renderCardVisual(card, compact = false) {
        const brandClass = card.brand.toLowerCase().replace(/\s+/g, '-');
        if (compact) {
            return `
                <div class="card-visual-compact ${brandClass}">
                    ${this.getCardBrandIcon(card.brand)}
                    <span class="card-last-four">&bull;&bull;&bull;&bull; ${card.lastFour}</span>
                    <span class="card-type-label">${card.type === 'credit' ? 'Credit' : 'Debit'}</span>
                </div>
            `;
        }
        return `
            <div class="card-visual ${brandClass}">
                <div class="card-visual-top">
                    ${this.getCardBrandIcon(card.brand)}
                    ${card.isPreferred ? '<span class="preferred-badge">Preferred</span>' : ''}
                    ${card.isBackup ? '<span class="backup-badge">Backup</span>' : ''}
                </div>
                <div class="card-visual-number">&bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; ${card.lastFour}</div>
                <div class="card-visual-bottom">
                    <div class="card-visual-name">${card.cardholderName}</div>
                    <div class="card-visual-exp">${String(card.expirationMonth).padStart(2, '0')}/${card.expirationYear}</div>
                </div>
            </div>
        `;
    },

    // ---- Crypto Sparkline (simple) ----
    renderCryptoChange(returnPercent) {
        const isPositive = returnPercent >= 0;
        return `
            <span class="crypto-change ${isPositive ? 'positive' : 'negative'}">
                <span class="material-icons">${isPositive ? 'trending_up' : 'trending_down'}</span>
                ${this.formatPercent(returnPercent)}
            </span>
        `;
    },

    // ---- Form Input ----
    renderInput(id, label, value, type = 'text', options = {}) {
        const { placeholder, required, pattern, maxlength, disabled, error, helpText } = options;
        return `
            <div class="form-group ${error ? 'has-error' : ''}">
                <label class="form-label" for="${id}">${label}${required ? ' <span class="required">*</span>' : ''}</label>
                <input class="form-input" type="${type}" id="${id}" name="${id}"
                    value="${value || ''}"
                    ${placeholder ? `placeholder="${placeholder}"` : ''}
                    ${required ? 'required' : ''}
                    ${pattern ? `pattern="${pattern}"` : ''}
                    ${maxlength ? `maxlength="${maxlength}"` : ''}
                    ${disabled ? 'disabled' : ''}
                >
                ${error ? `<span class="form-error">${error}</span>` : ''}
                ${helpText ? `<span class="form-help">${helpText}</span>` : ''}
            </div>
        `;
    }
};
