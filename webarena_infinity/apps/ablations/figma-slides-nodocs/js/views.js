/* ============================================================
   views.js — View renderers for Figma Slides
   ============================================================ */

const Views = {

    // ═══════════════════════════════════════════════════════════
    // Main content router
    // ═══════════════════════════════════════════════════════════
    renderContent() {
        switch (AppState.currentView) {
            case 'editor': return this.renderEditor();
            case 'presenter': return this.renderPresenter();
            default: return this.renderDashboard();
        }
    },

    // ═══════════════════════════════════════════════════════════
    // DASHBOARD VIEW
    // ═══════════════════════════════════════════════════════════
    renderDashboard() {
        const presentations = AppState.getFilteredPresentations();
        const allTags = AppState.getAllTags();
        const user = AppState.getCurrentUser();

        let html = `<div class="dashboard">`;

        // Header
        html += `<div class="dashboard-header">
            <div class="dashboard-title">
                <h1>Presentations</h1>
                <span class="count-badge">${AppState.presentations.length}</span>
            </div>
            <div class="dashboard-actions">
                <button class="btn btn-primary" data-action="new-presentation">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="3" x2="8" y2="13"/><line x1="3" y1="8" x2="13" y2="8"/></svg>
                    New Presentation
                </button>
            </div>
        </div>`;

        // Filters & search
        html += `<div class="dashboard-filters">
            <div class="search-box">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#888" stroke-width="1.5"><circle cx="7" cy="7" r="4.5"/><line x1="10.5" y1="10.5" x2="14" y2="14"/></svg>
                <input type="text" class="search-input" placeholder="Search presentations..." value="${Components.escapeAttr(AppState.searchQuery)}" data-input="search" />
            </div>
            <div class="filter-group">
                ${Components.dropdown('filterStatus', [
                    { value: '', label: 'All Statuses' },
                    { value: 'published', label: 'Published' },
                    { value: 'draft', label: 'Draft' },
                    { value: 'archived', label: 'Archived' }
                ], AppState.filterStatus, 'All Statuses')}
                ${Components.dropdown('filterTag', [
                    { value: '', label: 'All Tags' },
                    ...allTags.map(t => ({ value: t, label: t }))
                ], AppState.filterTag, 'All Tags')}
                ${Components.dropdown('sortBy', [
                    { value: 'updatedAt', label: 'Last Modified' },
                    { value: 'createdAt', label: 'Created Date' },
                    { value: 'title', label: 'Title A-Z' }
                ], AppState.sortBy, 'Sort by')}
                <button class="btn btn-icon" data-action="toggle-sort-order" title="Toggle sort order">
                    ${AppState.sortOrder === 'desc' ? '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 3v10M4 9l4 4 4-4"/></svg>' : '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 13V3M4 7l4-4 4 4"/></svg>'}
                </button>
            </div>
        </div>`;

        // Results count
        html += `<div class="results-info">${presentations.length} of ${AppState.presentations.length} presentations</div>`;

        // Presentation grid
        if (presentations.length === 0) {
            html += Components.emptyState(
                '<svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="#ccc" stroke-width="2"><rect x="6" y="10" width="36" height="28" rx="3"/><line x1="6" y1="18" x2="42" y2="18"/></svg>',
                'No presentations found',
                AppState.searchQuery ? 'Try adjusting your search or filters' : 'Create your first presentation to get started'
            );
        } else {
            html += `<div class="presentation-grid">`;
            presentations.forEach(pres => {
                html += this._renderPresentationCard(pres);
            });
            html += `</div>`;
        }

        html += `</div>`;

        // Modals
        if (AppState.activeModal === 'new-presentation') {
            html += this._renderNewPresentationModal();
        }
        if (AppState.activeModal === 'delete-presentation') {
            html += Components.confirmDialog('Delete Presentation', 'Are you sure you want to delete this presentation? This cannot be undone.', 'Delete', 'confirm-delete-presentation');
        }

        return html;
    },

    _renderPresentationCard(pres) {
        const author = AppState.getUserById(pres.createdBy);
        const slides = AppState.getSlidesForPresentation(pres.id);
        const firstSlide = slides[0];
        const commentCount = AppState.getCommentsForPresentation(pres.id).length;

        let html = `<div class="presentation-card" data-pres-id="${pres.id}">`;

        // Thumbnail
        html += `<div class="card-thumbnail" data-action="open-presentation" data-id="${pres.id}">`;
        if (firstSlide) {
            html += `<div class="card-thumb-inner" style="background:${firstSlide.backgroundColor || '#fff'}">`;
            const scale = 280 / CANVAS_WIDTH;
            (firstSlide.elements || []).slice(0, 5).forEach(el => {
                const ex = Math.round(el.x * scale);
                const ey = Math.round(el.y * scale);
                const ew = Math.round(el.width * scale);
                const eh = Math.round(el.height * scale);
                if (el.type === 'text' && el.content) {
                    const fs = Math.max(4, Math.round((el.style ? el.style.fontSize : 16) * scale));
                    const color = el.style ? el.style.color : '#000';
                    html += `<div style="position:absolute;left:${ex}px;top:${ey}px;width:${ew}px;height:${eh}px;font-size:${fs}px;color:${color};overflow:hidden;line-height:1.2;font-weight:${el.style && el.style.fontWeight ? el.style.fontWeight : 'normal'}">${Components.escapeHtml(el.content.substring(0, 40))}</div>`;
                } else if (el.type === 'shape') {
                    const r = el.shapeType === 'circle' ? '50%' : ((el.cornerRadius || 0) * scale) + 'px';
                    html += `<div style="position:absolute;left:${ex}px;top:${ey}px;width:${ew}px;height:${eh}px;background:${el.fill || '#ccc'};border-radius:${r};opacity:${el.opacity || 1}"></div>`;
                } else if (el.type === 'image') {
                    html += `<div style="position:absolute;left:${ex}px;top:${ey}px;width:${ew}px;height:${eh}px;background:${el.imagePlaceholder || '#e0e0e0'};border-radius:2px"></div>`;
                }
            });
            html += `</div>`;
        } else {
            html += `<div class="card-thumb-inner" style="background:#f5f5f5;display:flex;align-items:center;justify-content:center"><svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="#ccc" stroke-width="1.5"><rect x="4" y="8" width="24" height="16" rx="2"/></svg></div>`;
        }
        html += `</div>`;

        // Info
        html += `<div class="card-info">`;
        html += `<div class="card-title-row">
            <h3 class="card-title" data-action="open-presentation" data-id="${pres.id}" title="${Components.escapeAttr(pres.title)}">${Components.escapeHtml(pres.title)}</h3>
            <button class="btn btn-icon btn-star ${pres.starred ? 'starred' : ''}" data-action="toggle-star" data-id="${pres.id}" title="${pres.starred ? 'Unstar' : 'Star'}">
                ${pres.starred ? '<svg width="16" height="16" viewBox="0 0 16 16" fill="#FFC700" stroke="#FFC700" stroke-width="1"><path d="M8 1l2.1 4.3 4.7.7-3.4 3.3.8 4.7L8 11.8 3.8 14l.8-4.7L1.2 6l4.7-.7L8 1z"/></svg>' : '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#999" stroke-width="1"><path d="M8 1l2.1 4.3 4.7.7-3.4 3.3.8 4.7L8 11.8 3.8 14l.8-4.7L1.2 6l4.7-.7L8 1z"/></svg>'}
            </button>
        </div>`;
        html += `<div class="card-meta">`;
        html += `${Components.statusBadge(pres.status)}`;
        html += `<span class="meta-item">${pres.slideCount} slide${pres.slideCount !== 1 ? 's' : ''}</span>`;
        if (commentCount > 0) html += `<span class="meta-item">${commentCount} comment${commentCount !== 1 ? 's' : ''}</span>`;
        html += `</div>`;
        html += `<div class="card-tags">`;
        (pres.tags || []).slice(0, 3).forEach(t => { html += Components.tag(t); });
        if ((pres.tags || []).length > 3) html += `<span class="tag-more">+${pres.tags.length - 3}</span>`;
        html += `</div>`;
        html += `<div class="card-footer">`;
        html += `<div class="card-author">${Components.avatar(author, 20)} <span>${Components.escapeHtml(author ? author.name : 'Unknown')}</span></div>`;
        html += `<span class="card-date">${Components.timeAgo(pres.updatedAt)}</span>`;
        html += `</div>`;
        html += `<div class="card-actions">
            <button class="btn btn-sm btn-ghost" data-action="present" data-id="${pres.id}" title="Present"><svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><path d="M3 1.5v11l9-5.5z"/></svg></button>
            <button class="btn btn-sm btn-ghost" data-action="duplicate-presentation" data-id="${pres.id}" title="Duplicate"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="4" width="8" height="8" rx="1"/><path d="M2 10V3a1 1 0 011-1h7"/></svg></button>
            <button class="btn btn-sm btn-ghost" data-action="share-presentation" data-id="${pres.id}" title="Share"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 8.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM10 3.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM10 13.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/><path d="M6.3 7.1l1.4-2.7M6.3 7.9l1.4 2.7"/></svg></button>
            <button class="btn btn-sm btn-ghost btn-danger-hover" data-action="delete-presentation" data-id="${pres.id}" title="Delete"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 4h10M5 4V2.5a.5.5 0 01.5-.5h3a.5.5 0 01.5.5V4M11 4v8a1 1 0 01-1 1H4a1 1 0 01-1-1V4"/></svg></button>
        </div>`;
        html += `</div></div>`;
        return html;
    },

    _renderNewPresentationModal() {
        const body = `
            <div class="form-group">
                <label class="form-label">Title</label>
                ${Components.textInput('new-pres-title', '', 'Enter presentation title')}
            </div>
            <div class="form-group">
                <label class="form-label">Description</label>
                ${Components.textArea('new-pres-description', '', 'Brief description (optional)', 2)}
            </div>
            <div class="form-group">
                <label class="form-label">Theme</label>
                ${Components.dropdown('new-pres-theme', [
                    { value: 'minimal', label: 'Minimal' },
                    { value: 'corporate', label: 'Corporate' },
                    { value: 'creative', label: 'Creative' },
                    { value: 'nature', label: 'Nature' },
                    { value: 'warm', label: 'Warm' },
                    { value: 'ocean', label: 'Ocean' },
                    { value: 'dark', label: 'Dark' },
                    { value: 'sunset', label: 'Sunset' }
                ], 'minimal', 'Choose theme')}
            </div>
            <div class="form-group">
                <label class="form-label">Tags (comma-separated)</label>
                ${Components.textInput('new-pres-tags', '', 'e.g. design, product, q1')}
            </div>`;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="confirm-new-presentation">Create Presentation</button>`;
        return Components.modal('newPresentationModal', 'New Presentation', body, footer);
    },

    // ═══════════════════════════════════════════════════════════
    // EDITOR VIEW
    // ═══════════════════════════════════════════════════════════
    renderEditor() {
        const pres = AppState.getPresentationById(AppState.currentPresentationId);
        if (!pres) return `<div class="error-state"><h2>Presentation not found</h2><button class="btn btn-primary" data-action="go-dashboard">Back to Dashboard</button></div>`;

        const slides = AppState.getSlidesForPresentation(pres.id);
        const currentSlide = slides[AppState.currentSlideIndex] || slides[0];
        if (!currentSlide && slides.length === 0) {
            return `<div class="error-state"><h2>No slides</h2><button class="btn btn-primary" data-action="add-slide">Add a slide</button></div>`;
        }

        const canvasScale = AppState.zoom / 100;

        let html = `<div class="editor-layout">`;

        // ─── Toolbar ───
        html += this._renderToolbar(pres);

        // ─── Main area (3 panels) ───
        html += `<div class="editor-main">`;

        // Left: Slide filmstrip
        html += `<div class="slide-panel">`;
        html += `<div class="slide-panel-header"><span>Slides</span><span class="slide-count">${slides.length}</span></div>`;
        html += `<div class="slide-list">`;
        slides.forEach((s, i) => {
            html += Components.slideThumbnail(s, i, i === AppState.currentSlideIndex);
        });
        html += `</div>`;
        html += `<div class="slide-panel-footer">
            <button class="btn btn-sm btn-ghost" data-action="add-slide" title="Add blank slide"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="7" y1="2" x2="7" y2="12"/><line x1="2" y1="7" x2="12" y2="7"/></svg> Add Slide</button>
            <button class="btn btn-sm btn-ghost" data-action="open-template-gallery" title="Add from template"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="1" width="5" height="5" rx="1"/><rect x="8" y="1" width="5" height="5" rx="1"/><rect x="1" y="8" width="5" height="5" rx="1"/><rect x="8" y="8" width="5" height="5" rx="1"/></svg></button>
        </div>`;
        html += `</div>`;

        // Center: Canvas
        html += `<div class="canvas-area">`;
        html += `<div class="canvas-container" id="canvasContainer">`;
        html += `<div class="canvas" id="slideCanvas" style="width:${CANVAS_WIDTH * canvasScale}px;height:${CANVAS_HEIGHT * canvasScale}px;background:${currentSlide ? currentSlide.backgroundColor : '#fff'}">`;
        if (AppState.showGrid) {
            html += `<div class="canvas-grid" style="background-image:linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);background-size:${20 * canvasScale}px ${20 * canvasScale}px"></div>`;
        }
        if (currentSlide) {
            (currentSlide.elements || []).forEach(el => {
                html += Components.canvasElement(el, AppState.selectedElementIds.includes(el.id) || AppState.selectedElementId === el.id, canvasScale);
            });
        }
        html += `</div></div>`;

        // Speaker notes
        if (AppState.showSpeakerNotes && currentSlide) {
            html += `<div class="speaker-notes-panel">
                <div class="notes-header"><span>Speaker Notes</span><button class="btn btn-icon btn-xs" data-action="toggle-notes" title="Hide notes"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 5l3 3 3-3"/></svg></button></div>
                <textarea class="notes-textarea" data-input="speaker-notes" placeholder="Add speaker notes...">${Components.escapeHtml(currentSlide.speakerNotes || '')}</textarea>
            </div>`;
        }
        html += `</div>`;

        // Right: Properties panel
        if (AppState.propertiesPanelOpen) {
            html += this._renderPropertiesPanel(currentSlide);
        }

        html += `</div>`; // editor-main
        html += `</div>`; // editor-layout

        // Modals
        if (AppState.activeModal === 'template-gallery') html += this._renderTemplateGalleryModal();
        if (AppState.activeModal === 'share') html += this._renderShareModal(pres);
        if (AppState.activeModal === 'export') html += this._renderExportModal(pres);
        if (AppState.activeModal === 'transition') html += this._renderTransitionModal(currentSlide);
        if (AppState.activeModal === 'animation') html += this._renderAnimationModal(currentSlide);
        if (AppState.activeModal === 'comments') html += this._renderCommentsModal(pres, currentSlide);
        if (AppState.activeModal === 'delete-slide') html += Components.confirmDialog('Delete Slide', 'Delete this slide? This cannot be undone.', 'Delete', 'confirm-delete-slide');
        if (AppState.activeModal === 'save-template') html += this._renderSaveTemplateModal();

        return html;
    },

    _renderToolbar(pres) {
        const currentSlide = AppState.getCurrentSlide();
        const slides = AppState.getSlidesForPresentation(pres.id);
        const commentCount = AppState.getCommentsForPresentation(pres.id).filter(c => !c.resolved).length;

        let html = `<div class="editor-toolbar">`;
        html += `<div class="toolbar-left">
            <button class="btn btn-icon" data-action="go-dashboard" title="Back to dashboard"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M11 4L6 9l5 5"/></svg></button>
            <span class="toolbar-title" title="${Components.escapeAttr(pres.title)}">${Components.escapeHtml(pres.title)}</span>
            ${Components.statusBadge(pres.status)}
        </div>`;

        // Tools
        html += `<div class="toolbar-center">`;
        const tools = [
            { id: 'select', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 2l3 12 2.5-4.5L13 7z"/></svg>', label: 'Select' },
            { id: 'text', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 3h10M8 3v10M5 13h6"/></svg>', label: 'Text' },
            { id: 'rectangle', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="3" width="12" height="10" rx="1"/></svg>', label: 'Rectangle' },
            { id: 'circle', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="6"/></svg>', label: 'Circle' },
            { id: 'line', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="2" y1="14" x2="14" y2="2"/></svg>', label: 'Line' },
            { id: 'arrow', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="2" y1="14" x2="14" y2="2"/><path d="M8 2h6v6"/></svg>', label: 'Arrow' },
            { id: 'image', icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="12" height="12" rx="1"/><circle cx="5.5" cy="5.5" r="1.5"/><path d="M14 10l-3.5-3.5L3 14"/></svg>', label: 'Image' }
        ];
        tools.forEach(t => {
            const active = AppState.activeTool === t.id ? ' active' : '';
            html += `<button class="tool-btn${active}" data-action="set-tool" data-value="${t.id}" title="${t.label}">${t.icon}</button>`;
        });
        html += `</div>`;

        // Right actions
        html += `<div class="toolbar-right">
            <button class="btn btn-icon ${AppState.showGrid ? 'active' : ''}" data-action="toggle-grid" title="Toggle grid"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 5.5h14M1 10.5h14M5.5 1v14M10.5 1v14"/></svg></button>
            <button class="btn btn-icon ${AppState.showSpeakerNotes ? 'active' : ''}" data-action="toggle-notes" title="Toggle notes"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="12" height="12" rx="1"/><line x1="5" y1="6" x2="11" y2="6"/><line x1="5" y1="9" x2="9" y2="9"/></svg></button>
            <button class="btn btn-icon" data-action="open-comments" title="Comments${commentCount > 0 ? ` (${commentCount} unresolved)` : ''}">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 2h12v9H5L2 14V2z"/></svg>
                ${commentCount > 0 ? `<span class="comment-badge">${commentCount}</span>` : ''}
            </button>
            <div class="toolbar-divider"></div>
            <div class="zoom-control">
                <button class="btn btn-icon btn-xs" data-action="zoom-out" title="Zoom out"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="3" y1="6" x2="9" y2="6"/></svg></button>
                <span class="zoom-label">${AppState.zoom}%</span>
                <button class="btn btn-icon btn-xs" data-action="zoom-in" title="Zoom in"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="6" y1="3" x2="6" y2="9"/><line x1="3" y1="6" x2="9" y2="6"/></svg></button>
            </div>
            <div class="toolbar-divider"></div>
            <button class="btn btn-sm btn-ghost" data-action="share-presentation" data-id="${pres.id}">Share</button>
            <button class="btn btn-sm btn-ghost" data-action="export-presentation" data-id="${pres.id}">Export</button>
            <button class="btn btn-primary btn-sm" data-action="present" data-id="${pres.id}">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><path d="M3 1.5v11l9-5.5z"/></svg> Present
            </button>
        </div>`;

        html += `</div>`;
        return html;
    },

    _renderPropertiesPanel(slide) {
        const selectedEl = slide && AppState.selectedElementId ? slide.elements.find(e => e.id === AppState.selectedElementId) : null;

        let html = `<div class="properties-panel">`;
        html += `<div class="panel-header">
            <span>${selectedEl ? 'Element' : 'Slide'} Properties</span>
            <button class="btn btn-icon btn-xs" data-action="toggle-properties" title="Close panel"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="2" y1="2" x2="10" y2="10"/><line x1="10" y1="2" x2="2" y2="10"/></svg></button>
        </div>`;

        if (selectedEl) {
            html += this._renderElementProperties(selectedEl, slide);
        } else if (slide) {
            html += this._renderSlideProperties(slide);
        }

        html += `</div>`;
        return html;
    },

    _renderSlideProperties(slide) {
        let html = `<div class="props-section">`;
        html += `<h4>Background</h4>`;
        html += Components.colorPalette('slide-bg', slide.backgroundColor);
        html += `</div>`;

        html += `<div class="props-section">`;
        html += `<h4>Layout</h4>`;
        html += Components.dropdown('slide-layout', LAYOUT_TYPES.map(l => ({ value: l, label: l.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) })), slide.layout, 'Select layout');
        html += `</div>`;

        html += `<div class="props-section">`;
        html += `<h4>Transition</h4>`;
        html += `<button class="btn btn-sm btn-ghost btn-block" data-action="open-transition">
            ${slide.transition.type === 'none' ? 'No transition' : slide.transition.type + ' (' + slide.transition.duration + 'ms)'}
        </button>`;
        html += `</div>`;

        html += `<div class="props-section">`;
        html += `<h4>Actions</h4>`;
        html += `<button class="btn btn-sm btn-ghost btn-block" data-action="duplicate-slide" data-id="${slide.id}">Duplicate Slide</button>`;
        html += `<button class="btn btn-sm btn-ghost btn-block" data-action="apply-template-to-slide" data-id="${slide.id}">Apply Template</button>`;
        html += `<button class="btn btn-sm btn-ghost btn-block" data-action="save-as-template" data-id="${slide.id}">Save as Template</button>`;
        html += `<button class="btn btn-sm btn-danger btn-block" data-action="delete-slide-confirm" data-id="${slide.id}">Delete Slide</button>`;
        html += `</div>`;
        return html;
    },

    _renderElementProperties(el, slide) {
        let html = '';

        // Position & size
        html += `<div class="props-section">
            <h4>Position & Size</h4>
            <div class="props-grid">
                <div class="prop-field"><label>X</label><input type="number" class="prop-input" data-prop="x" value="${el.x}"/></div>
                <div class="prop-field"><label>Y</label><input type="number" class="prop-input" data-prop="y" value="${el.y}"/></div>
                <div class="prop-field"><label>W</label><input type="number" class="prop-input" data-prop="width" value="${el.width}"/></div>
                <div class="prop-field"><label>H</label><input type="number" class="prop-input" data-prop="height" value="${el.height}"/></div>
            </div>
            <div class="props-row">
                <div class="prop-field"><label>Rotation</label><input type="number" class="prop-input" data-prop="rotation" value="${el.rotation}" min="-360" max="360"/></div>
                <div class="prop-field"><label>Opacity</label><input type="number" class="prop-input" data-prop="opacity" value="${el.opacity}" min="0" max="1" step="0.1"/></div>
            </div>
        </div>`;

        // Text properties
        if (el.type === 'text' && el.style) {
            html += `<div class="props-section">
                <h4>Text</h4>
                <div class="form-group">
                    <label class="form-label-sm">Font</label>
                    ${Components.dropdown('font-family', FONT_FAMILIES.map(f => ({ value: f, label: f })), el.style.fontFamily, 'Font')}
                </div>
                <div class="props-grid">
                    <div class="prop-field"><label>Size</label><input type="number" class="prop-input" data-prop="fontSize" value="${el.style.fontSize}" min="8" max="200"/></div>
                    <div class="prop-field"><label>Weight</label>
                        ${Components.dropdown('font-weight', [
                            { value: 'normal', label: 'Regular' },
                            { value: '500', label: 'Medium' },
                            { value: '600', label: 'Semibold' },
                            { value: 'bold', label: 'Bold' }
                        ], el.style.fontWeight, 'Weight')}
                    </div>
                </div>
                <div class="props-row">
                    <button class="tool-btn ${el.style.italic ? 'active' : ''}" data-action="toggle-italic" title="Italic"><em>I</em></button>
                    <button class="tool-btn ${el.style.underline ? 'active' : ''}" data-action="toggle-underline" title="Underline"><u>U</u></button>
                    <button class="tool-btn ${el.style.textAlign === 'left' ? 'active' : ''}" data-action="set-align" data-value="left" title="Left">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="1" y1="2" x2="13" y2="2"/><line x1="1" y1="5" x2="9" y2="5"/><line x1="1" y1="8" x2="11" y2="8"/><line x1="1" y1="11" x2="8" y2="11"/></svg>
                    </button>
                    <button class="tool-btn ${el.style.textAlign === 'center' ? 'active' : ''}" data-action="set-align" data-value="center" title="Center">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="1" y1="2" x2="13" y2="2"/><line x1="3" y1="5" x2="11" y2="5"/><line x1="2" y1="8" x2="12" y2="8"/><line x1="4" y1="11" x2="10" y2="11"/></svg>
                    </button>
                    <button class="tool-btn ${el.style.textAlign === 'right' ? 'active' : ''}" data-action="set-align" data-value="right" title="Right">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="1" y1="2" x2="13" y2="2"/><line x1="5" y1="5" x2="13" y2="5"/><line x1="3" y1="8" x2="13" y2="8"/><line x1="6" y1="11" x2="13" y2="11"/></svg>
                    </button>
                </div>
                <div class="form-group">
                    <label class="form-label-sm">Color</label>
                    ${Components.colorPalette('text-color', el.style.color)}
                </div>
                <div class="form-group">
                    <label class="form-label-sm">List Type</label>
                    ${Components.dropdown('list-type', [
                        { value: 'none', label: 'None' },
                        { value: 'bullet', label: 'Bullet List' },
                        { value: 'numbered', label: 'Numbered List' }
                    ], el.style.listType || 'none', 'List type')}
                </div>
                <div class="props-grid">
                    <div class="prop-field"><label>Line Height</label><input type="number" class="prop-input" data-prop="lineHeight" value="${el.style.lineHeight}" step="0.1" min="0.5" max="3"/></div>
                    <div class="prop-field"><label>Letter Spacing</label><input type="number" class="prop-input" data-prop="letterSpacing" value="${el.style.letterSpacing}" step="0.5" min="-5" max="20"/></div>
                </div>
                <div class="form-group">
                    <label class="form-label-sm">Content</label>
                    <textarea class="form-textarea form-textarea-sm" data-input="element-content" rows="4">${Components.escapeHtml(el.content || '')}</textarea>
                </div>
            </div>`;
        }

        // Shape properties
        if (el.type === 'shape') {
            html += `<div class="props-section">
                <h4>Shape</h4>
                <div class="form-group">
                    <label class="form-label-sm">Type</label>
                    ${Components.dropdown('shape-type', SHAPE_TYPES.map(s => ({ value: s, label: s.charAt(0).toUpperCase() + s.slice(1) })), el.shapeType, 'Shape')}
                </div>
                <div class="form-group">
                    <label class="form-label-sm">Fill</label>
                    ${Components.colorPalette('shape-fill', el.fill)}
                </div>
                <div class="form-group">
                    <label class="form-label-sm">Stroke</label>
                    ${Components.colorPalette('shape-stroke', el.stroke)}
                </div>
                <div class="props-grid">
                    <div class="prop-field"><label>Stroke Width</label><input type="number" class="prop-input" data-prop="strokeWidth" value="${el.strokeWidth}" min="0" max="20"/></div>
                    <div class="prop-field"><label>Corner Radius</label><input type="number" class="prop-input" data-prop="cornerRadius" value="${el.cornerRadius}" min="0" max="100"/></div>
                </div>
            </div>`;
        }

        // Animation
        html += `<div class="props-section">
            <h4>Animation</h4>
            <button class="btn btn-sm btn-ghost btn-block" data-action="open-animation">
                ${el.animation && el.animation.type !== 'none' ? el.animation.type + ' (' + el.animation.duration + 'ms)' : 'No animation'}
            </button>
        </div>`;

        // Element actions
        html += `<div class="props-section">
            <h4>Actions</h4>
            ${Components.toggle('element-locked', el.locked, 'Lock element')}
            <button class="btn btn-sm btn-danger btn-block" style="margin-top:8px" data-action="delete-element" data-id="${el.id}">Delete Element</button>
        </div>`;

        return html;
    },

    // ─── Template Gallery Modal ───
    _renderTemplateGalleryModal() {
        const categories = ['all', 'basic', 'business', 'creative', 'custom'];
        let body = `<div class="template-gallery">`;
        body += `<div class="template-categories">`;
        categories.forEach(cat => {
            body += `<button class="btn btn-sm ${cat === 'all' ? 'btn-primary' : 'btn-ghost'}" data-action="filter-templates" data-value="${cat}">${cat.charAt(0).toUpperCase() + cat.slice(1)}</button>`;
        });
        body += `</div>`;
        body += `<div class="template-grid">`;
        AppState.templates.forEach(tmpl => {
            body += `<div class="template-card" data-action="apply-template" data-value="${tmpl.id}">
                <div class="template-preview" style="background:${tmpl.previewColor || '#f5f5f5'}">
                    <span class="template-layout-label">${Components.escapeHtml(tmpl.layout)}</span>
                </div>
                <div class="template-name">${Components.escapeHtml(tmpl.name)}</div>
                <div class="template-desc">${Components.escapeHtml(tmpl.description || '')}</div>
            </div>`;
        });
        body += `</div></div>`;
        return Components.modal('templateGalleryModal', 'Template Gallery', body, '', true);
    },

    // ─── Share Modal ───
    _renderShareModal(pres) {
        const ss = pres.shareSettings;
        const body = `<div class="share-settings">
            <div class="form-group">
                <label class="form-label">Visibility</label>
                ${Components.dropdown('share-visibility', [
                    { value: 'private', label: 'Private — Only you and shared people' },
                    { value: 'team', label: 'Team — Your team can view' },
                    { value: 'organization', label: 'Organization — Everyone in org' },
                    { value: 'public', label: 'Public — Anyone with the link' }
                ], ss.visibility, 'Select visibility')}
            </div>
            <div class="form-group">
                ${Components.toggle('allow-comments', ss.allowComments, 'Allow comments')}
            </div>
            <div class="form-group">
                ${Components.toggle('allow-editing', ss.allowEditing, 'Allow editing')}
            </div>
            <div class="form-group">
                <label class="form-label">Share Link</label>
                <div class="input-with-button">
                    ${Components.textInput('share-link', ss.shareLink, 'No share link generated')}
                    <button class="btn btn-sm btn-ghost" data-action="copy-share-link">Copy</button>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Embed Link</label>
                <div class="input-with-button">
                    ${Components.textInput('embed-link', ss.embedLink, 'No embed link generated')}
                    <button class="btn btn-sm btn-ghost" data-action="copy-embed-link">Copy</button>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Shared With</label>
                <div class="shared-users">
                    ${(ss.sharedWith || []).map(uid => {
                        const u = AppState.getUserById(uid);
                        return u ? `<div class="shared-user">${Components.avatar(u, 24)} <span>${Components.escapeHtml(u.name)}</span> <button class="btn btn-icon btn-xs" data-action="remove-shared-user" data-value="${uid}">&times;</button></div>` : '';
                    }).join('')}
                </div>
                <div class="add-user-row">
                    ${Components.dropdown('add-shared-user', AppState.users.filter(u => !(ss.sharedWith || []).includes(u.id)).map(u => ({ value: u.id, label: u.name })), '', 'Add person...')}
                </div>
            </div>
        </div>`;
        return Components.modal('shareModal', 'Share Presentation', body,
            `<button class="btn btn-secondary" data-action="close-modal">Done</button>`);
    },

    // ─── Export Modal ───
    _renderExportModal(pres) {
        const body = `<div class="export-options">
            <div class="export-option" data-action="export-pdf">
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="#F24822" stroke-width="1.5"><rect x="4" y="2" width="24" height="28" rx="2"/><path d="M10 14h12M10 18h8M10 10h12"/></svg>
                <div>
                    <h4>Export as PDF</h4>
                    <p>All slides in a single PDF document</p>
                </div>
            </div>
            <div class="export-option" data-action="export-png">
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="#14AE5C" stroke-width="1.5"><rect x="4" y="4" width="24" height="24" rx="2"/><circle cx="11" cy="11" r="3"/><path d="M28 20l-7-7L4 28"/></svg>
                <div>
                    <h4>Export Slides as PNG</h4>
                    <p>Individual slide images at high resolution</p>
                </div>
            </div>
            <div class="export-option" data-action="export-svg">
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="#7B61FF" stroke-width="1.5"><rect x="4" y="4" width="24" height="24" rx="2"/><path d="M10 22V10l6 8 6-8v12"/></svg>
                <div>
                    <h4>Export as SVG</h4>
                    <p>Vector format for each slide</p>
                </div>
            </div>
        </div>`;
        return Components.modal('exportModal', 'Export Presentation', body, '');
    },

    // ─── Transition Modal ───
    _renderTransitionModal(slide) {
        if (!slide) return '';
        const body = `<div class="transition-settings">
            <div class="form-group">
                <label class="form-label">Transition Type</label>
                ${Components.dropdown('transition-type', TRANSITION_TYPES.map(t => ({ value: t, label: t.charAt(0).toUpperCase() + t.slice(1) })), slide.transition.type, 'Select transition')}
            </div>
            <div class="form-group">
                <label class="form-label">Duration (ms)</label>
                <input type="number" class="form-input" data-input="transition-duration" value="${slide.transition.duration}" min="100" max="3000" step="100" />
            </div>
            <div class="transition-preview">
                <div class="preview-label">Preview</div>
                <div class="preview-box" id="transitionPreview">
                    <div class="preview-slide">Slide ${AppState.currentSlideIndex + 1}</div>
                </div>
            </div>
        </div>`;
        return Components.modal('transitionModal', 'Slide Transition', body,
            `<button class="btn btn-secondary" data-action="close-modal">Cancel</button>
             <button class="btn btn-primary" data-action="save-transition">Apply</button>`);
    },

    // ─── Animation Modal ───
    _renderAnimationModal(slide) {
        if (!slide) return '';
        const el = slide.elements.find(e => e.id === AppState.selectedElementId);
        if (!el) return '';
        const anim = el.animation || { type: 'none', duration: 300, delay: 0, order: 0 };
        const body = `<div class="animation-settings">
            <div class="form-group">
                <label class="form-label">Animation Type</label>
                ${Components.dropdown('animation-type', ANIMATION_TYPES.map(t => ({ value: t, label: t.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) })), anim.type, 'Select animation')}
            </div>
            <div class="form-group">
                <label class="form-label">Duration (ms)</label>
                <input type="number" class="form-input" data-input="animation-duration" value="${anim.duration}" min="100" max="3000" step="100" />
            </div>
            <div class="form-group">
                <label class="form-label">Delay (ms)</label>
                <input type="number" class="form-input" data-input="animation-delay" value="${anim.delay}" min="0" max="5000" step="100" />
            </div>
            <div class="form-group">
                <label class="form-label">Order</label>
                <input type="number" class="form-input" data-input="animation-order" value="${anim.order}" min="0" max="20" />
            </div>
        </div>`;
        return Components.modal('animationModal', 'Element Animation', body,
            `<button class="btn btn-secondary" data-action="close-modal">Cancel</button>
             <button class="btn btn-primary" data-action="save-animation">Apply</button>`);
    },

    // ─── Comments Modal ───
    _renderCommentsModal(pres, currentSlide) {
        const allComments = AppState.getCommentsForPresentation(pres.id);
        const slideComments = currentSlide ? allComments.filter(c => c.slideId === currentSlide.id) : [];
        const otherComments = currentSlide ? allComments.filter(c => c.slideId !== currentSlide.id) : allComments;

        let body = `<div class="comments-panel">`;

        // Current slide comments
        if (currentSlide) {
            body += `<div class="comments-section">
                <h4>Slide ${AppState.currentSlideIndex + 1} Comments (${slideComments.length})</h4>`;
            if (slideComments.length === 0) {
                body += `<p class="text-muted">No comments on this slide.</p>`;
            }
            slideComments.forEach(c => { body += this._renderComment(c); });
            body += `<div class="add-comment">
                <textarea class="form-textarea" data-input="new-comment" placeholder="Add a comment..." rows="2"></textarea>
                <button class="btn btn-sm btn-primary" data-action="add-comment" style="margin-top:8px">Comment</button>
            </div>`;
            body += `</div>`;
        }

        // Other comments
        if (otherComments.length > 0) {
            body += `<div class="comments-section">
                <h4>Other Slides (${otherComments.length})</h4>`;
            otherComments.forEach(c => { body += this._renderComment(c, true); });
            body += `</div>`;
        }

        body += `</div>`;
        return Components.modal('commentsModal', 'Comments', body, '', true);
    },

    _renderComment(comment, showSlideRef) {
        const author = AppState.getUserById(comment.authorId);
        let html = `<div class="comment ${comment.resolved ? 'resolved' : ''}" data-comment-id="${comment.id}">`;
        html += `<div class="comment-header">
            ${Components.avatar(author, 24)}
            <div class="comment-meta">
                <strong>${Components.escapeHtml(author ? author.name : 'Unknown')}</strong>
                <span class="text-muted">${Components.timeAgo(comment.createdAt)}</span>
                ${showSlideRef ? `<span class="text-muted">on slide ${this._getSlideNumber(comment.slideId)}</span>` : ''}
            </div>
            <div class="comment-actions">
                <button class="btn btn-icon btn-xs" data-action="toggle-resolve-comment" data-id="${comment.id}" title="${comment.resolved ? 'Unresolve' : 'Resolve'}">
                    ${comment.resolved ? '<svg width="14" height="14" viewBox="0 0 14 14" fill="#14AE5C" stroke="#14AE5C" stroke-width="1.5"><path d="M3 7l3 3 5-5"/></svg>' : '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="#999" stroke-width="1.5"><circle cx="7" cy="7" r="5"/></svg>'}
                </button>
                <button class="btn btn-icon btn-xs" data-action="delete-comment" data-id="${comment.id}" title="Delete"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="#999" stroke-width="1.5"><line x1="2" y1="2" x2="10" y2="10"/><line x1="10" y1="2" x2="2" y2="10"/></svg></button>
            </div>
        </div>`;
        html += `<div class="comment-body">${Components.escapeHtml(comment.content)}</div>`;

        // Replies
        if (comment.replies && comment.replies.length > 0) {
            html += `<div class="comment-replies">`;
            comment.replies.forEach(r => {
                const rAuthor = AppState.getUserById(r.authorId);
                html += `<div class="reply">
                    <div class="reply-header">${Components.avatar(rAuthor, 20)} <strong>${Components.escapeHtml(rAuthor ? rAuthor.name : 'Unknown')}</strong> <span class="text-muted">${Components.timeAgo(r.createdAt)}</span></div>
                    <div class="reply-body">${Components.escapeHtml(r.content)}</div>
                </div>`;
            });
            html += `</div>`;
        }

        html += `<div class="reply-input">
            <input type="text" class="form-input form-input-sm" data-input="reply-${comment.id}" placeholder="Reply..." />
            <button class="btn btn-xs btn-ghost" data-action="add-reply" data-id="${comment.id}">Reply</button>
        </div>`;
        html += `</div>`;
        return html;
    },

    _getSlideNumber(slideId) {
        const slide = AppState.getSlideById(slideId);
        return slide ? slide.order + 1 : '?';
    },

    // ─── Save Template Modal ───
    _renderSaveTemplateModal() {
        const body = `<div class="form-group">
            <label class="form-label">Template Name</label>
            ${Components.textInput('template-name', '', 'My Custom Template')}
        </div>
        <div class="form-group">
            <label class="form-label">Category</label>
            ${Components.dropdown('template-category', [
                { value: 'custom', label: 'Custom' },
                { value: 'basic', label: 'Basic' },
                { value: 'business', label: 'Business' },
                { value: 'creative', label: 'Creative' }
            ], 'custom', 'Select category')}
        </div>`;
        return Components.modal('saveTemplateModal', 'Save as Template', body,
            `<button class="btn btn-secondary" data-action="close-modal">Cancel</button>
             <button class="btn btn-primary" data-action="confirm-save-template">Save Template</button>`);
    },

    // ═══════════════════════════════════════════════════════════
    // PRESENTER VIEW
    // ═══════════════════════════════════════════════════════════
    renderPresenter() {
        const pres = AppState.getPresentationById(AppState.currentPresentationId);
        if (!pres) return '';
        const slides = AppState.getSlidesForPresentation(pres.id);
        const slideIndex = AppState.presenterSlideIndex;
        const currentSlide = slides[slideIndex];
        if (!currentSlide) return '';

        const scale = Math.min(window.innerWidth / CANVAS_WIDTH, (window.innerHeight - 60) / CANVAS_HEIGHT);

        let html = `<div class="presenter-mode">`;

        // Main slide
        html += `<div class="presenter-slide-wrapper" style="width:${CANVAS_WIDTH * scale}px;height:${CANVAS_HEIGHT * scale}px">`;
        html += `<div class="presenter-canvas" style="width:${CANVAS_WIDTH * scale}px;height:${CANVAS_HEIGHT * scale}px;background:${currentSlide.backgroundColor || '#fff'}">`;
        (currentSlide.elements || []).forEach(el => {
            html += Components.canvasElement(el, false, scale);
        });
        html += `</div></div>`;

        // Controls bar
        html += `<div class="presenter-controls">
            <div class="presenter-left">
                <button class="btn btn-ghost" data-action="exit-presenter" title="Exit">
                    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="4" y1="4" x2="14" y2="14"/><line x1="14" y1="4" x2="4" y2="14"/></svg>
                    Exit
                </button>
            </div>
            <div class="presenter-center">
                <button class="btn btn-ghost" data-action="presenter-prev" ${slideIndex <= 0 ? 'disabled' : ''}>
                    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M11 4L6 9l5 5"/></svg>
                </button>
                <span class="presenter-progress">${slideIndex + 1} / ${slides.length}</span>
                <button class="btn btn-ghost" data-action="presenter-next" ${slideIndex >= slides.length - 1 ? 'disabled' : ''}>
                    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M7 4l5 5-5 5"/></svg>
                </button>
            </div>
            <div class="presenter-right">
                <span class="presenter-timer" id="presenterTimer">00:00</span>
                <button class="btn btn-ghost btn-sm" data-action="toggle-presenter-notes" title="Notes">Notes</button>
            </div>
        </div>`;

        // Speaker notes (if visible)
        if (AppState.showSpeakerNotes && currentSlide.speakerNotes) {
            html += `<div class="presenter-notes">
                <strong>Speaker Notes:</strong>
                <p>${Components.escapeHtml(currentSlide.speakerNotes)}</p>
            </div>`;
        }

        html += `</div>`;
        return html;
    }
};
