const Components = {
    avatar(user, size) {
        size = size || 32;
        const fontSize = Math.round(size * 0.4);
        return `<div class="avatar" style="width:${size}px;height:${size}px;background:${user.avatarColor || '#666'};font-size:${fontSize}px;line-height:${size}px;" title="${this._esc(user.name || '')}">${user.initials || '??'}</div>`;
    },

    avatarStack(users, max) {
        max = max || 5;
        const shown = users.slice(0, max);
        const remaining = users.length - max;
        let html = '<div class="avatar-stack">';
        shown.forEach(u => { html += this.avatar(u, 28); });
        if (remaining > 0) {
            html += `<div class="avatar avatar-more" style="width:28px;height:28px;font-size:11px;line-height:28px;">+${remaining}</div>`;
        }
        html += '</div>';
        return html;
    },

    dropdown(id, currentValue, options, label) {
        const selected = options.find(o => o.id === currentValue || o.value === currentValue);
        const displayText = selected ? (selected.name || selected.label) : (currentValue || 'Select...');
        let html = `<div class="custom-dropdown" id="${id}" data-dropdown-id="${id}" data-value="${currentValue || ''}">`;
        if (label) html += `<label class="dropdown-label">${this._esc(label)}</label>`;
        html += `<div class="dropdown-trigger" data-action="toggleDropdown" data-dropdown-id="${id}">
            <span class="dropdown-text">${this._esc(displayText)}</span>
            <span class="dropdown-arrow">&#9662;</span>
        </div>
        <div class="dropdown-menu">`;
        options.forEach(opt => {
            const isSelected = (opt.id === currentValue || opt.value === currentValue) ? ' selected' : '';
            html += `<div class="dropdown-item${isSelected}" data-action="selectDropdownItem" data-dropdown-id="${id}" data-value="${opt.id || opt.value}">${this._esc(opt.name || opt.label)}</div>`;
        });
        html += '</div></div>';
        return html;
    },

    toggle(id, checked, label) {
        return `<div class="toggle-row">
            ${label ? `<span class="toggle-label">${this._esc(label)}</span>` : ''}
            <label class="toggle-switch" data-toggle-id="${id}">
                <input type="checkbox" ${checked ? 'checked' : ''} data-action="toggle" data-toggle-id="${id}">
                <span class="toggle-slider"></span>
            </label>
        </div>`;
    },

    modal(id, title, bodyHtml, footerHtml, size) {
        return `<div class="modal-overlay active" id="modal-${id}" data-modal-id="${id}">
            <div class="modal ${size || ''}">
                <div class="modal-header">
                    <h2>${this._esc(title)}</h2>
                    <button class="modal-close" data-action="closeModal">&times;</button>
                </div>
                <div class="modal-body">${bodyHtml}</div>
                ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
            </div>
        </div>`;
    },

    confirmModal(id, title, message, confirmText, confirmClass) {
        return this.modal(id, title,
            `<p>${this._esc(message)}</p>`,
            `<button class="btn btn-secondary" data-action="closeModal">Cancel</button>
             <button class="btn ${confirmClass || 'btn-danger'}" data-action="confirmModal" data-modal-id="${id}">${this._esc(confirmText || 'Confirm')}</button>`
        );
    },

    colorPicker(id, currentColor, label) {
        const presetColors = ['#FFFFFF', '#000000', '#F24E1E', '#FF7262', '#FFAC33', '#F7C948', '#0ACF83', '#00B894', '#1ABCFE', '#0052CC', '#7B61FF', '#A259FF', '#E0E0E0', '#888888', '#404040', '#1E1E1E'];
        let html = `<div class="color-picker" id="${id}">`;
        if (label) html += `<label class="color-picker-label">${this._esc(label)}</label>`;
        html += `<div class="color-picker-current">
            <div class="color-swatch" style="background:${currentColor || '#FFFFFF'}" data-action="toggleColorPicker" data-picker-id="${id}"></div>
            <input type="text" class="color-input" value="${currentColor || '#FFFFFF'}" data-action="colorInput" data-picker-id="${id}" maxlength="7">
        </div>
        <div class="color-picker-panel" data-picker-id="${id}">
            <div class="color-presets">`;
        presetColors.forEach(c => {
            html += `<div class="color-preset${c === currentColor ? ' active' : ''}" style="background:${c}" data-action="selectColor" data-picker-id="${id}" data-color="${c}"></div>`;
        });
        html += '</div></div></div>';
        return html;
    },

    textInput(id, value, placeholder, label) {
        let html = '';
        if (label) html += `<label class="input-label" for="${id}">${this._esc(label)}</label>`;
        html += `<input type="text" class="text-input" id="${id}" value="${this._esc(value || '')}" placeholder="${this._esc(placeholder || '')}" data-input-id="${id}">`;
        return html;
    },

    textarea(id, value, placeholder, label, rows) {
        let html = '';
        if (label) html += `<label class="input-label" for="${id}">${this._esc(label)}</label>`;
        html += `<textarea class="text-input textarea" id="${id}" placeholder="${this._esc(placeholder || '')}" data-input-id="${id}" rows="${rows || 4}">${this._esc(value || '')}</textarea>`;
        return html;
    },

    numberInput(id, value, min, max, step, label) {
        let html = '';
        if (label) html += `<label class="input-label" for="${id}">${this._esc(label)}</label>`;
        html += `<input type="number" class="text-input number-input" id="${id}" value="${value}" min="${min}" max="${max}" step="${step || 1}" data-input-id="${id}">`;
        return html;
    },

    slider(id, value, min, max, step, label) {
        let html = `<div class="slider-row">`;
        if (label) html += `<label class="slider-label">${this._esc(label)}</label>`;
        html += `<div class="slider-control">
            <input type="range" class="slider" id="${id}" value="${value}" min="${min}" max="${max}" step="${step || 1}" data-slider-id="${id}">
            <span class="slider-value">${value}</span>
        </div></div>`;
        return html;
    },

    tabs(id, tabs, activeTab) {
        let html = `<div class="tab-bar" id="${id}">`;
        tabs.forEach(tab => {
            html += `<button class="tab-btn${tab.id === activeTab ? ' active' : ''}" data-action="switchTab" data-tab-id="${tab.id}" data-tab-group="${id}">${this._esc(tab.label)}</button>`;
        });
        html += '</div>';
        return html;
    },

    badge(text, type) {
        return `<span class="badge badge-${type || 'default'}">${this._esc(text)}</span>`;
    },

    iconButton(icon, action, title, extraClass) {
        return `<button class="icon-btn ${extraClass || ''}" data-action="${action}" title="${this._esc(title || '')}">${icon}</button>`;
    },

    emptyState(icon, message, actionText, action) {
        let html = `<div class="empty-state">
            <div class="empty-state-icon">${icon}</div>
            <p class="empty-state-message">${this._esc(message)}</p>`;
        if (actionText && action) {
            html += `<button class="btn btn-primary" data-action="${action}">${this._esc(actionText)}</button>`;
        }
        html += '</div>';
        return html;
    },

    contextMenu(items, x, y) {
        let html = `<div class="context-menu" style="left:${x}px;top:${y}px;">`;
        items.forEach(item => {
            if (item.separator) {
                html += '<div class="context-menu-separator"></div>';
                return;
            }
            const disabled = item.disabled ? ' disabled' : '';
            html += `<div class="context-menu-item${disabled}" data-action="${item.action}" ${item.data ? Object.entries(item.data).map(([k,v]) => `data-${k}="${v}"`).join(' ') : ''}>${this._esc(item.label)}</div>`;
        });
        html += '</div>';
        return html;
    },

    toast(message) {
        return `<div class="toast-notification">${this._esc(message)}</div>`;
    },

    searchBar(id, value, placeholder) {
        return `<div class="search-bar">
            <span class="search-icon">&#128269;</span>
            <input type="text" class="search-input" id="${id}" value="${this._esc(value || '')}" placeholder="${this._esc(placeholder || 'Search...')}" data-input-id="${id}">
            ${value ? `<button class="search-clear" data-action="clearSearch" data-search-id="${id}">&times;</button>` : ''}
        </div>`;
    },

    progressBar(value, max, label) {
        const pct = Math.round((value / max) * 100);
        let html = '';
        if (label) html += `<div class="progress-label">${this._esc(label)}</div>`;
        html += `<div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>`;
        return html;
    },

    _esc(str) {
        if (typeof str !== 'string') return String(str || '');
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }
};
