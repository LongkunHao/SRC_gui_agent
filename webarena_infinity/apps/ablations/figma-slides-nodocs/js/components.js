/* ============================================================
   components.js — Reusable UI component generators
   ============================================================ */

const Components = {

    // ─── Utilities ───
    escapeHtml(str) {
        if (!str) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    },

    escapeAttr(str) {
        if (!str) return '';
        return String(str).replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    },

    // ─── Date formatting ───
    formatDate(iso) {
        if (!iso) return '';
        const d = new Date(iso);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },

    formatDateTime(iso) {
        if (!iso) return '';
        const d = new Date(iso);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
    },

    timeAgo(iso) {
        if (!iso) return '';
        const now = new Date();
        const d = new Date(iso);
        const diff = Math.floor((now - d) / 1000);
        if (diff < 60) return 'just now';
        if (diff < 3600) return Math.floor(diff / 60) + 'm ago';
        if (diff < 86400) return Math.floor(diff / 3600) + 'h ago';
        if (diff < 604800) return Math.floor(diff / 86400) + 'd ago';
        return this.formatDate(iso);
    },

    // ─── Avatar ───
    avatar(user, size) {
        size = size || 32;
        if (!user) return `<span class="avatar" style="width:${size}px;height:${size}px;font-size:${size * 0.4}px;background:#ccc">?</span>`;
        return `<span class="avatar" style="width:${size}px;height:${size}px;font-size:${size * 0.4}px;background:${user.color}" title="${this.escapeAttr(user.name)}">${this.escapeHtml(user.initials)}</span>`;
    },

    // ─── Tags ───
    tag(text, color) {
        color = color || '#7B61FF';
        return `<span class="tag" style="background:${color}20;color:${color};border:1px solid ${color}40">${this.escapeHtml(text)}</span>`;
    },

    statusBadge(status) {
        const colors = { published: '#14AE5C', draft: '#FFC700', archived: '#888888' };
        const color = colors[status] || '#888888';
        return `<span class="status-badge" style="background:${color}20;color:${color}"><span class="status-dot" style="background:${color}"></span>${this.escapeHtml(status)}</span>`;
    },

    // ─── Custom dropdown ───
    dropdown(name, options, selected, placeholder, extraClass) {
        const selOpt = options.find(o => o.value === selected);
        const label = selOpt ? selOpt.label : (placeholder || 'Select...');
        let html = `<div class="custom-dropdown ${extraClass || ''}" data-dropdown="${this.escapeAttr(name)}">`;
        html += `<div class="dropdown-trigger" data-dropdown-trigger="${this.escapeAttr(name)}">`;
        html += `<span class="dropdown-label">${this.escapeHtml(label)}</span>`;
        html += `<svg width="12" height="12" viewBox="0 0 12 12" class="dropdown-arrow"><path d="M3 5l3 3 3-3" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>`;
        html += `</div>`;
        html += `<div class="dropdown-menu" data-dropdown-menu="${this.escapeAttr(name)}">`;
        options.forEach(opt => {
            const active = opt.value === selected ? ' active' : '';
            html += `<div class="dropdown-item${active}" data-dropdown-item="${this.escapeAttr(name)}" data-value="${this.escapeAttr(opt.value)}">${this.escapeHtml(opt.label)}</div>`;
        });
        html += `</div></div>`;
        return html;
    },

    // ─── Modal ───
    modal(id, title, bodyHtml, footerHtml, wide) {
        return `<div class="modal-overlay" id="${id}" data-modal="${id}">
            <div class="modal ${wide ? 'modal-wide' : ''}">
                <div class="modal-header">
                    <h2>${this.escapeHtml(title)}</h2>
                    <button class="modal-close" data-action="close-modal">&times;</button>
                </div>
                <div class="modal-body">${bodyHtml}</div>
                ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
            </div>
        </div>`;
    },

    // ─── Toast ───
    showToast(message, type) {
        type = type || 'info';
        const container = document.getElementById('toastContainer');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    // ─── Close active dropdowns ───
    closeAllDropdowns() {
        document.querySelectorAll('.custom-dropdown.open').forEach(dd => dd.classList.remove('open'));
    },

    // ─── Color picker (simple palette) ───
    colorPalette(name, selected, colors) {
        colors = colors || ['#ffffff', '#f5f5f5', '#e0e0e0', '#1a1a2e', '#2c2c2c', '#000000',
            '#7B61FF', '#9747FF', '#0D99FF', '#14AE5C', '#FFC700', '#F24822',
            '#FF7262', '#FF8577', '#00B4D8', '#40916C', '#BC4749', '#F4845F',
            '#023E8A', '#16213e', '#1B4332', '#0f3460'];
        let html = `<div class="color-palette" data-color-palette="${this.escapeAttr(name)}">`;
        colors.forEach(c => {
            const active = c === selected ? ' active' : '';
            const border = (c === '#ffffff' || c === '#f5f5f5') ? 'border:1px solid #ddd;' : '';
            html += `<button class="color-swatch${active}" data-color-swatch="${this.escapeAttr(name)}" data-value="${c}" style="background:${c};${border}" title="${c}"></button>`;
        });
        html += `</div>`;
        return html;
    },

    // ─── Input field ───
    textInput(name, value, placeholder, type) {
        type = type || 'text';
        return `<input class="form-input" type="${type}" name="${this.escapeAttr(name)}" value="${this.escapeAttr(value || '')}" placeholder="${this.escapeAttr(placeholder || '')}" data-input="${this.escapeAttr(name)}" />`;
    },

    textArea(name, value, placeholder, rows) {
        return `<textarea class="form-textarea" name="${this.escapeAttr(name)}" placeholder="${this.escapeAttr(placeholder || '')}" rows="${rows || 3}" data-input="${this.escapeAttr(name)}">${this.escapeHtml(value || '')}</textarea>`;
    },

    // ─── Toggle ───
    toggle(name, checked, label) {
        return `<label class="toggle-label">
            <div class="toggle ${checked ? 'active' : ''}" data-toggle="${this.escapeAttr(name)}">
                <div class="toggle-thumb"></div>
            </div>
            ${label ? `<span>${this.escapeHtml(label)}</span>` : ''}
        </label>`;
    },

    // ─── Slide thumbnail (simplified canvas preview) ───
    slideThumbnail(slide, index, isActive, small) {
        const w = small ? 120 : 160;
        const h = small ? 67.5 : 90;
        const scale = w / CANVAS_WIDTH;
        let html = `<div class="slide-thumbnail ${isActive ? 'active' : ''}" data-slide-index="${index}" data-slide-id="${slide.id}" style="width:${w}px;height:${h}px">`;
        html += `<div class="slide-thumb-canvas" style="background:${slide.backgroundColor || '#fff'};width:${w}px;height:${h}px;position:relative;overflow:hidden;border-radius:4px">`;

        (slide.elements || []).forEach(el => {
            const ex = Math.round(el.x * scale);
            const ey = Math.round(el.y * scale);
            const ew = Math.round(el.width * scale);
            const eh = Math.round(el.height * scale);
            if (el.type === 'text' && el.content) {
                const fs = Math.max(3, Math.round((el.style ? el.style.fontSize : 16) * scale));
                const color = el.style ? el.style.color : '#000';
                html += `<div style="position:absolute;left:${ex}px;top:${ey}px;width:${ew}px;height:${eh}px;font-size:${fs}px;color:${color};overflow:hidden;line-height:1.2;font-weight:${el.style && el.style.fontWeight ? el.style.fontWeight : 'normal'}">${this.escapeHtml(el.content.substring(0, 60))}</div>`;
            } else if (el.type === 'shape') {
                const radius = el.shapeType === 'circle' ? '50%' : (el.cornerRadius ? el.cornerRadius * scale + 'px' : '0');
                html += `<div style="position:absolute;left:${ex}px;top:${ey}px;width:${ew}px;height:${eh}px;background:${el.fill || '#ccc'};border-radius:${radius};opacity:${el.opacity || 1}"></div>`;
            } else if (el.type === 'image') {
                html += `<div style="position:absolute;left:${ex}px;top:${ey}px;width:${ew}px;height:${eh}px;background:${el.imagePlaceholder || '#e0e0e0'};border-radius:2px"></div>`;
            }
        });

        html += `</div>`;
        html += `<span class="slide-number">${index + 1}</span>`;
        html += `</div>`;
        return html;
    },

    // ─── Render element on canvas ───
    canvasElement(el, isSelected, scale) {
        scale = scale || 1;
        const x = el.x * scale;
        const y = el.y * scale;
        const w = el.width * scale;
        const h = el.height * scale;
        const selected = isSelected ? ' selected' : '';
        const locked = el.locked ? ' locked' : '';
        let style = `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;opacity:${el.opacity};`;
        if (el.rotation) style += `transform:rotate(${el.rotation}deg);`;

        let inner = '';
        if (el.type === 'text') {
            const s = el.style || {};
            const fs = (s.fontSize || 20) * scale;
            inner = `<div class="canvas-text" style="font-family:'${s.fontFamily || 'Inter'}',sans-serif;font-size:${fs}px;font-weight:${s.fontWeight || 'normal'};color:${s.color || '#000'};text-align:${s.textAlign || 'left'};font-style:${s.italic ? 'italic' : 'normal'};text-decoration:${s.underline ? 'underline' : 'none'};line-height:${s.lineHeight || 1.4};letter-spacing:${(s.letterSpacing || 0) * scale}px;white-space:pre-wrap;word-wrap:break-word;width:100%;height:100%">`;
            const lines = (el.content || '').split('\n');
            if (s.listType === 'bullet') {
                inner += lines.map(l => `<div style="padding-left:${16 * scale}px;text-indent:${-12 * scale}px">• ${this.escapeHtml(l)}</div>`).join('');
            } else if (s.listType === 'numbered') {
                inner += lines.map((l, i) => `<div style="padding-left:${20 * scale}px;text-indent:${-16 * scale}px">${i + 1}. ${this.escapeHtml(l)}</div>`).join('');
            } else {
                inner += this.escapeHtml(el.content || '').replace(/\n/g, '<br>');
            }
            inner += `</div>`;
        } else if (el.type === 'shape') {
            const radius = el.shapeType === 'circle' ? '50%' : ((el.cornerRadius || 0) * scale) + 'px';
            const border = el.stroke && el.stroke !== 'none' ? `border:${(el.strokeWidth || 1) * scale}px solid ${el.stroke}` : '';
            if (el.shapeType === 'line' || el.shapeType === 'arrow') {
                inner = `<div style="width:100%;height:50%;border-bottom:${(el.strokeWidth || 2) * scale}px solid ${el.stroke || el.fill || '#333'}"></div>`;
                if (el.shapeType === 'arrow') {
                    inner += `<div style="position:absolute;right:0;top:50%;transform:translateY(-50%);width:0;height:0;border-left:${8 * scale}px solid ${el.stroke || el.fill || '#333'};border-top:${5 * scale}px solid transparent;border-bottom:${5 * scale}px solid transparent"></div>`;
                }
            } else if (el.shapeType === 'triangle') {
                inner = `<div style="width:0;height:0;border-left:${w / 2}px solid transparent;border-right:${w / 2}px solid transparent;border-bottom:${h}px solid ${el.fill || '#4A90D9'}"></div>`;
            } else if (el.shapeType === 'diamond') {
                inner = `<div style="width:${w * 0.7}px;height:${h * 0.7}px;background:${el.fill || '#4A90D9'};transform:rotate(45deg);margin:${h * 0.15}px auto;${border}"></div>`;
            } else {
                inner = `<div style="width:100%;height:100%;background:${el.fill || '#4A90D9'};border-radius:${radius};${border}"></div>`;
            }
        } else if (el.type === 'image') {
            if (el.imageUrl) {
                inner = `<img src="${this.escapeAttr(el.imageUrl)}" style="width:100%;height:100%;object-fit:cover;border-radius:${(el.cornerRadius || 0) * scale}px" alt="slide image"/>`;
            } else {
                inner = `<div style="width:100%;height:100%;background:${el.imagePlaceholder || '#e0e0e0'};border-radius:${(el.cornerRadius || 0) * scale}px;display:flex;align-items:center;justify-content:center">
                    <svg width="${24 * scale}" height="${24 * scale}" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
                </div>`;
            }
        }

        return `<div class="canvas-element${selected}${locked}" data-element-id="${el.id}" style="${style}">${inner}${isSelected ? '<div class="resize-handle resize-nw" data-resize="nw"></div><div class="resize-handle resize-ne" data-resize="ne"></div><div class="resize-handle resize-sw" data-resize="sw"></div><div class="resize-handle resize-se" data-resize="se"></div>' : ''}</div>`;
    },

    // ─── Empty state ───
    emptyState(icon, title, subtitle) {
        return `<div class="empty-state">
            <div class="empty-icon">${icon || ''}</div>
            <h3>${this.escapeHtml(title || 'Nothing here')}</h3>
            <p>${this.escapeHtml(subtitle || '')}</p>
        </div>`;
    },

    // ─── Confirm dialog ───
    confirmDialog(title, message, confirmText, action) {
        return this.modal('confirmModal', title,
            `<p>${this.escapeHtml(message)}</p>`,
            `<button class="btn btn-secondary" data-action="close-modal">Cancel</button>
             <button class="btn btn-danger" data-action="${this.escapeAttr(action)}">${this.escapeHtml(confirmText || 'Delete')}</button>`
        );
    }
};
