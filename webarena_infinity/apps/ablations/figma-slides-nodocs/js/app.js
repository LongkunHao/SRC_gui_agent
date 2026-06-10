/* ============================================================
   app.js — Router, event delegation, and lifecycle
   ============================================================ */

const App = {
    _dragState: null,
    _resizeState: null,
    _presenterInterval: null,
    _pendingDeletePresId: null,

    // ═══════════════════════════════════════════════════════════
    // Init
    // ═══════════════════════════════════════════════════════════
    init() {
        AppState.init();
        this._setupSSE();
        AppState.subscribe(() => this.render());
        this._parseRoute();
        this.render();
        this._attachGlobalListeners();
    },

    // ═══════════════════════════════════════════════════════════
    // SSE
    // ═══════════════════════════════════════════════════════════
    _setupSSE() {
        const es = new EventSource('/api/events');
        es.onmessage = (e) => {
            if (e.data === 'reset') {
                AppState.resetToSeedData();
                window.location.hash = '#/';
            }
        };
    },

    // ═══════════════════════════════════════════════════════════
    // Routing
    // ═══════════════════════════════════════════════════════════
    _parseRoute() {
        const hash = window.location.hash || '#/';
        const parts = hash.replace('#/', '').split('/');
        if (parts[0] === 'editor' && parts[1]) {
            AppState.currentView = 'editor';
            AppState.currentPresentationId = parts[1];
            AppState.currentSlideIndex = parts[2] ? parseInt(parts[2]) : 0;
            AppState.selectedElementId = null;
            AppState.selectedElementIds = [];
        } else if (parts[0] === 'presenter' && parts[1]) {
            AppState.currentView = 'presenter';
            AppState.currentPresentationId = parts[1];
            AppState.presenterSlideIndex = 0;
            AppState.presenterTimerStart = Date.now();
            this._startPresenterTimer();
        } else {
            AppState.currentView = 'dashboard';
            AppState.currentPresentationId = null;
            this._stopPresenterTimer();
        }
    },

    navigate(route) {
        window.location.hash = '#/' + route;
    },

    // ═══════════════════════════════════════════════════════════
    // Render
    // ═══════════════════════════════════════════════════════════
    render() {
        const content = document.getElementById('appContent');
        if (!content) return;
        const isEditor = AppState.currentView === 'editor';
        const isPresenter = AppState.currentView === 'presenter';

        document.body.classList.toggle('view-editor', isEditor);
        document.body.classList.toggle('view-presenter', isPresenter);
        document.body.classList.toggle('view-dashboard', !isEditor && !isPresenter);

        content.innerHTML = Views.renderContent();
    },

    // ═══════════════════════════════════════════════════════════
    // Event listeners
    // ═══════════════════════════════════════════════════════════
    _attachGlobalListeners() {
        window.addEventListener('hashchange', () => { this._parseRoute(); this.render(); });
        document.addEventListener('click', (e) => this._handleClick(e));
        document.addEventListener('input', (e) => this._handleInput(e));
        document.addEventListener('change', (e) => this._handleChange(e));
        document.addEventListener('mousedown', (e) => this._handleMouseDown(e));
        document.addEventListener('mousemove', (e) => this._handleMouseMove(e));
        document.addEventListener('mouseup', (e) => this._handleMouseUp(e));
        document.addEventListener('keydown', (e) => this._handleKeyDown(e));

        // Close dropdowns on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.custom-dropdown')) {
                Components.closeAllDropdowns();
            }
        });
    },

    // ── Click handler ──
    _handleClick(e) {
        const target = e.target;

        // Dropdown trigger
        const ddTrigger = target.closest('[data-dropdown-trigger]');
        if (ddTrigger) {
            e.preventDefault();
            e.stopPropagation();
            const dd = ddTrigger.closest('.custom-dropdown');
            const wasOpen = dd.classList.contains('open');
            Components.closeAllDropdowns();
            if (!wasOpen) dd.classList.add('open');
            return;
        }

        // Dropdown item
        const ddItem = target.closest('[data-dropdown-item]');
        if (ddItem) {
            e.preventDefault();
            const name = ddItem.dataset.dropdownItem;
            const value = ddItem.dataset.value;
            this._handleDropdownSelect(name, value);
            Components.closeAllDropdowns();
            return;
        }

        // Color swatch
        const swatch = target.closest('[data-color-swatch]');
        if (swatch) {
            e.preventDefault();
            this._handleColorSelect(swatch.dataset.colorSwatch, swatch.dataset.value);
            return;
        }

        // Toggle
        const toggle = target.closest('[data-toggle]');
        if (toggle) {
            e.preventDefault();
            this._handleToggle(toggle.dataset.toggle);
            return;
        }

        // Modal overlay click
        const modalOverlay = target.closest('.modal-overlay');
        if (modalOverlay && target === modalOverlay) {
            AppState.activeModal = null;
            this.render();
            return;
        }

        // Action buttons
        const actionEl = target.closest('[data-action]');
        if (actionEl) {
            e.preventDefault();
            this._handleAction(actionEl.dataset.action, actionEl);
            return;
        }

        // Slide thumbnail click
        const thumb = target.closest('.slide-thumbnail');
        if (thumb && !target.closest('[data-action]')) {
            const index = parseInt(thumb.dataset.slideIndex);
            AppState.currentSlideIndex = index;
            AppState.selectedElementId = null;
            AppState.selectedElementIds = [];
            this.render();
            return;
        }

        // Canvas element click
        const canvasEl = target.closest('.canvas-element');
        if (canvasEl) {
            e.stopPropagation();
            const elId = canvasEl.dataset.elementId;
            AppState.selectedElementId = elId;
            AppState.selectedElementIds = [elId];
            this.render();
            return;
        }

        // Click on canvas (deselect)
        if (target.closest('.canvas') && !target.closest('.canvas-element')) {
            if (AppState.activeTool !== 'select') {
                this._handleCanvasClick(e);
            } else {
                AppState.selectedElementId = null;
                AppState.selectedElementIds = [];
                this.render();
            }
            return;
        }
    },

    // ── Action dispatch ──
    _handleAction(action, el) {
        switch (action) {
            // Dashboard
            case 'new-presentation':
                AppState.activeModal = 'new-presentation';
                this.render();
                break;
            case 'confirm-new-presentation':
                this._createPresentation();
                break;
            case 'open-presentation':
                this.navigate('editor/' + el.dataset.id);
                break;
            case 'delete-presentation':
                this._pendingDeletePresId = el.dataset.id;
                AppState.activeModal = 'delete-presentation';
                this.render();
                break;
            case 'confirm-delete-presentation':
                if (this._pendingDeletePresId) {
                    AppState.deletePresentation(this._pendingDeletePresId);
                    this._pendingDeletePresId = null;
                    AppState.activeModal = null;
                    Components.showToast('Presentation deleted', 'info');
                }
                this.render();
                break;
            case 'duplicate-presentation':
                const newId = AppState.duplicatePresentation(el.dataset.id);
                if (newId) Components.showToast('Presentation duplicated', 'success');
                this.render();
                break;
            case 'toggle-star':
                AppState.toggleStar(el.dataset.id);
                break;
            case 'toggle-sort-order':
                AppState.sortOrder = AppState.sortOrder === 'desc' ? 'asc' : 'desc';
                this.render();
                break;

            // Navigation
            case 'go-dashboard':
                AppState.activeModal = null;
                this.navigate('');
                break;
            case 'present':
                this.navigate('presenter/' + (el.dataset.id || AppState.currentPresentationId));
                break;
            case 'exit-presenter':
                this._stopPresenterTimer();
                this.navigate('editor/' + AppState.currentPresentationId);
                break;

            // Presenter
            case 'presenter-prev':
                if (AppState.presenterSlideIndex > 0) {
                    AppState.presenterSlideIndex--;
                    this.render();
                }
                break;
            case 'presenter-next': {
                const slides = AppState.getSlidesForPresentation(AppState.currentPresentationId);
                if (AppState.presenterSlideIndex < slides.length - 1) {
                    AppState.presenterSlideIndex++;
                    this.render();
                }
                break;
            }
            case 'toggle-presenter-notes':
                AppState.showSpeakerNotes = !AppState.showSpeakerNotes;
                this.render();
                break;

            // Tools
            case 'set-tool':
                AppState.activeTool = el.dataset.value;
                this.render();
                break;

            // Editor toggles
            case 'toggle-grid':
                AppState.showGrid = !AppState.showGrid;
                this.render();
                break;
            case 'toggle-notes':
                AppState.showSpeakerNotes = !AppState.showSpeakerNotes;
                this.render();
                break;
            case 'toggle-properties':
                AppState.propertiesPanelOpen = !AppState.propertiesPanelOpen;
                this.render();
                break;
            case 'zoom-in':
                AppState.zoom = Math.min(200, AppState.zoom + 10);
                this.render();
                break;
            case 'zoom-out':
                AppState.zoom = Math.max(25, AppState.zoom - 10);
                this.render();
                break;

            // Slides
            case 'add-slide':
                AppState.addSlide(AppState.currentPresentationId, AppState.currentSlideIndex);
                AppState.currentSlideIndex++;
                this.render();
                break;
            case 'duplicate-slide':
                AppState.duplicateSlide(el.dataset.id || AppState.getCurrentSlide()?.id);
                AppState.currentSlideIndex++;
                this.render();
                break;
            case 'delete-slide-confirm':
                AppState.activeModal = 'delete-slide';
                this.render();
                break;
            case 'confirm-delete-slide': {
                const current = AppState.getCurrentSlide();
                if (current) {
                    const presSlides = AppState.getSlidesForPresentation(AppState.currentPresentationId);
                    if (presSlides.length <= 1) {
                        Components.showToast('Cannot delete the only slide', 'error');
                    } else {
                        AppState.deleteSlide(current.id);
                        AppState.currentSlideIndex = Math.min(AppState.currentSlideIndex, presSlides.length - 2);
                    }
                }
                AppState.activeModal = null;
                this.render();
                break;
            }

            // Templates
            case 'open-template-gallery':
            case 'apply-template-to-slide':
                AppState.activeModal = 'template-gallery';
                this.render();
                break;
            case 'apply-template': {
                const tmplId = el.dataset.value;
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && tmplId) {
                    if (AppState.activeModal === 'template-gallery' && !curSlide.elements.length) {
                        // If applying to an empty slide, use the template
                        AppState.applyTemplateToSlide(curSlide.id, tmplId);
                    } else {
                        // Add a new slide with the template
                        AppState.addSlide(AppState.currentPresentationId, AppState.currentSlideIndex, tmplId);
                        AppState.currentSlideIndex++;
                    }
                }
                AppState.activeModal = null;
                this.render();
                break;
            }
            case 'save-as-template':
                AppState.activeModal = 'save-template';
                this.render();
                break;
            case 'confirm-save-template': {
                const nameInput = document.querySelector('[data-input="template-name"]');
                const name = nameInput ? nameInput.value.trim() : 'Custom Template';
                const curS = AppState.getCurrentSlide();
                if (curS) {
                    AppState.saveAsTemplate(curS.id, name || 'Custom Template', 'custom');
                    Components.showToast('Template saved', 'success');
                }
                AppState.activeModal = null;
                this.render();
                break;
            }

            // Share & Export
            case 'share-presentation':
                AppState.activeModal = 'share';
                if (el.dataset.id) AppState.currentPresentationId = el.dataset.id;
                this.render();
                break;
            case 'export-presentation':
                AppState.activeModal = 'export';
                this.render();
                break;
            case 'export-pdf':
            case 'export-png':
            case 'export-svg':
                Components.showToast('Export started (simulated)', 'info');
                AppState.activeModal = null;
                this.render();
                break;
            case 'copy-share-link':
            case 'copy-embed-link':
                Components.showToast('Link copied to clipboard', 'success');
                break;
            case 'remove-shared-user': {
                const pres = AppState.getPresentationById(AppState.currentPresentationId);
                if (pres) {
                    pres.shareSettings.sharedWith = (pres.shareSettings.sharedWith || []).filter(uid => uid !== el.dataset.value);
                    AppState.notify();
                }
                break;
            }

            // Transitions & Animations
            case 'open-transition':
                AppState.activeModal = 'transition';
                this.render();
                break;
            case 'save-transition': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide) {
                    const typeEl = document.querySelector('[data-dropdown="transition-type"] .dropdown-item.active');
                    const durEl = document.querySelector('[data-input="transition-duration"]');
                    const type = typeEl ? typeEl.dataset.value : curSlide.transition.type;
                    const dur = durEl ? parseInt(durEl.value) || 500 : curSlide.transition.duration;
                    AppState.updateSlide(curSlide.id, { transition: { type, duration: dur } });
                }
                AppState.activeModal = null;
                this.render();
                break;
            }
            case 'open-animation':
                AppState.activeModal = 'animation';
                this.render();
                break;
            case 'save-animation': {
                const curSlide2 = AppState.getCurrentSlide();
                if (curSlide2 && AppState.selectedElementId) {
                    const typeEl = document.querySelector('[data-dropdown="animation-type"] .dropdown-item.active');
                    const durEl = document.querySelector('[data-input="animation-duration"]');
                    const delayEl = document.querySelector('[data-input="animation-delay"]');
                    const orderEl = document.querySelector('[data-input="animation-order"]');
                    AppState.updateElement(curSlide2.id, AppState.selectedElementId, {
                        animation: {
                            type: typeEl ? typeEl.dataset.value : 'none',
                            duration: durEl ? parseInt(durEl.value) || 300 : 300,
                            delay: delayEl ? parseInt(delayEl.value) || 0 : 0,
                            order: orderEl ? parseInt(orderEl.value) || 0 : 0
                        }
                    });
                }
                AppState.activeModal = null;
                this.render();
                break;
            }

            // Comments
            case 'open-comments':
                AppState.activeModal = 'comments';
                this.render();
                break;
            case 'add-comment': {
                const textarea = document.querySelector('[data-input="new-comment"]');
                if (textarea && textarea.value.trim()) {
                    const curSlide = AppState.getCurrentSlide();
                    if (curSlide) {
                        AppState.addComment(AppState.currentPresentationId, curSlide.id, textarea.value.trim());
                        Components.showToast('Comment added', 'success');
                    }
                }
                this.render();
                break;
            }
            case 'add-reply': {
                const cmtId = el.dataset.id;
                const input = document.querySelector(`[data-input="reply-${cmtId}"]`);
                if (input && input.value.trim()) {
                    AppState.addReply(cmtId, input.value.trim());
                }
                this.render();
                break;
            }
            case 'toggle-resolve-comment':
                AppState.toggleResolveComment(el.dataset.id);
                this.render();
                break;
            case 'delete-comment':
                AppState.deleteComment(el.dataset.id);
                this.render();
                break;

            // Element actions
            case 'delete-element': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && el.dataset.id) {
                    AppState.deleteElement(curSlide.id, el.dataset.id);
                    AppState.selectedElementId = null;
                    AppState.selectedElementIds = [];
                }
                this.render();
                break;
            }
            case 'toggle-italic': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    const elem = curSlide.elements.find(e => e.id === AppState.selectedElementId);
                    if (elem && elem.style) {
                        AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { italic: !elem.style.italic } });
                    }
                }
                break;
            }
            case 'toggle-underline': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    const elem = curSlide.elements.find(e => e.id === AppState.selectedElementId);
                    if (elem && elem.style) {
                        AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { underline: !elem.style.underline } });
                    }
                }
                break;
            }
            case 'set-align': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { textAlign: el.dataset.value } });
                }
                break;
            }

            // Modal close
            case 'close-modal':
                AppState.activeModal = null;
                this.render();
                break;
        }
    },

    // ── Dropdown select ──
    _handleDropdownSelect(name, value) {
        switch (name) {
            case 'filterStatus':
                AppState.filterStatus = value;
                this.render();
                break;
            case 'filterTag':
                AppState.filterTag = value;
                this.render();
                break;
            case 'sortBy':
                AppState.sortBy = value;
                this.render();
                break;
            case 'slide-layout': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide) AppState.updateSlide(curSlide.id, { layout: value });
                break;
            }
            case 'font-family': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { fontFamily: value } });
                }
                break;
            }
            case 'font-weight': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { fontWeight: value } });
                }
                break;
            }
            case 'list-type': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { listType: value } });
                }
                break;
            }
            case 'shape-type': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { shapeType: value });
                }
                break;
            }
            case 'transition-type':
                // Handled by save button
                break;
            case 'animation-type':
                // Handled by save button
                break;
            case 'share-visibility': {
                const pres = AppState.getPresentationById(AppState.currentPresentationId);
                if (pres) {
                    AppState.updateShareSettings(AppState.currentPresentationId, { visibility: value });
                }
                this.render();
                break;
            }
            case 'add-shared-user': {
                const pres = AppState.getPresentationById(AppState.currentPresentationId);
                if (pres && value) {
                    if (!pres.shareSettings.sharedWith) pres.shareSettings.sharedWith = [];
                    if (!pres.shareSettings.sharedWith.includes(value)) {
                        pres.shareSettings.sharedWith.push(value);
                        AppState.notify();
                    }
                }
                this.render();
                break;
            }
            case 'new-pres-theme':
                // Stored for form submission
                break;
            case 'template-category':
                // Stored for form submission
                break;
        }
    },

    // ── Color select ──
    _handleColorSelect(name, value) {
        const curSlide = AppState.getCurrentSlide();
        if (!curSlide) return;

        switch (name) {
            case 'slide-bg':
                AppState.updateSlide(curSlide.id, { backgroundColor: value });
                break;
            case 'text-color':
                if (AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { color: value } });
                }
                break;
            case 'shape-fill':
                if (AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { fill: value });
                }
                break;
            case 'shape-stroke':
                if (AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { stroke: value });
                }
                break;
        }
    },

    // ── Toggle handler ──
    _handleToggle(name) {
        switch (name) {
            case 'element-locked': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    const el = curSlide.elements.find(e => e.id === AppState.selectedElementId);
                    if (el) AppState.updateElement(curSlide.id, AppState.selectedElementId, { locked: !el.locked });
                }
                break;
            }
            case 'allow-comments': {
                const pres = AppState.getPresentationById(AppState.currentPresentationId);
                if (pres) AppState.updateShareSettings(AppState.currentPresentationId, { allowComments: !pres.shareSettings.allowComments });
                this.render();
                break;
            }
            case 'allow-editing': {
                const pres = AppState.getPresentationById(AppState.currentPresentationId);
                if (pres) AppState.updateShareSettings(AppState.currentPresentationId, { allowEditing: !pres.shareSettings.allowEditing });
                this.render();
                break;
            }
        }
    },

    // ── Input handler ──
    _handleInput(e) {
        const target = e.target;
        const name = target.dataset.input;
        if (!name) {
            // Property inputs
            const prop = target.dataset.prop;
            if (prop) {
                this._handlePropertyInput(prop, target.value);
            }
            return;
        }

        switch (name) {
            case 'search':
                AppState.searchQuery = target.value;
                this.render();
                break;
            case 'speaker-notes': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide) {
                    AppState.updateSlide(curSlide.id, { speakerNotes: target.value });
                }
                break;
            }
            case 'element-content': {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    AppState.updateElement(curSlide.id, AppState.selectedElementId, { content: target.value });
                }
                break;
            }
        }
    },

    _handlePropertyInput(prop, value) {
        const curSlide = AppState.getCurrentSlide();
        if (!curSlide || !AppState.selectedElementId) return;
        const el = curSlide.elements.find(e => e.id === AppState.selectedElementId);
        if (!el) return;

        const numVal = parseFloat(value);
        if (isNaN(numVal)) return;

        const styleProps = ['fontSize', 'lineHeight', 'letterSpacing'];
        if (styleProps.includes(prop)) {
            AppState.updateElement(curSlide.id, AppState.selectedElementId, { style: { [prop]: numVal } });
        } else {
            AppState.updateElement(curSlide.id, AppState.selectedElementId, { [prop]: numVal });
        }
    },

    _handleChange(e) {
        // Handled by input event
    },

    // ── Canvas click (add element) ──
    _handleCanvasClick(e) {
        const canvas = e.target.closest('.canvas');
        if (!canvas) return;
        const curSlide = AppState.getCurrentSlide();
        if (!curSlide) return;

        const rect = canvas.getBoundingClientRect();
        const scale = AppState.zoom / 100;
        const x = Math.round((e.clientX - rect.left) / scale);
        const y = Math.round((e.clientY - rect.top) / scale);

        let elementData = null;
        switch (AppState.activeTool) {
            case 'text':
                elementData = { type: 'text', x, y, width: 300, height: 60, content: 'Double-click to edit' };
                break;
            case 'rectangle':
                elementData = { type: 'shape', x, y, width: 200, height: 150, shapeType: 'rectangle', fill: '#4A90D9' };
                break;
            case 'circle':
                elementData = { type: 'shape', x, y, width: 150, height: 150, shapeType: 'circle', fill: '#14AE5C' };
                break;
            case 'line':
                elementData = { type: 'shape', x, y, width: 200, height: 4, shapeType: 'line', fill: '#333333', stroke: '#333333', strokeWidth: 2 };
                break;
            case 'arrow':
                elementData = { type: 'shape', x, y, width: 200, height: 20, shapeType: 'arrow', fill: '#333333', stroke: '#333333', strokeWidth: 2 };
                break;
            case 'image':
                elementData = { type: 'image', x, y, width: 300, height: 200, imagePlaceholder: '#e0e0e0' };
                break;
        }

        if (elementData) {
            const newId = AppState.addElement(curSlide.id, elementData);
            AppState.selectedElementId = newId;
            AppState.selectedElementIds = [newId];
            AppState.activeTool = 'select';
        }
    },

    // ── Mouse drag (element move & resize) ──
    _handleMouseDown(e) {
        // Resize handle
        const resizeHandle = e.target.closest('.resize-handle');
        if (resizeHandle) {
            e.preventDefault();
            const canvasEl = resizeHandle.closest('.canvas-element');
            if (!canvasEl) return;
            const curSlide = AppState.getCurrentSlide();
            if (!curSlide) return;
            const el = curSlide.elements.find(x => x.id === canvasEl.dataset.elementId);
            if (!el || el.locked) return;
            const scale = AppState.zoom / 100;
            this._resizeState = {
                elementId: el.id,
                slideId: curSlide.id,
                startX: e.clientX,
                startY: e.clientY,
                origW: el.width,
                origH: el.height,
                origX: el.x,
                origY: el.y,
                handle: resizeHandle.dataset.resize,
                scale
            };
            return;
        }

        // Element drag
        const canvasEl = e.target.closest('.canvas-element');
        if (canvasEl && !e.target.closest('.resize-handle')) {
            e.preventDefault();
            const curSlide = AppState.getCurrentSlide();
            if (!curSlide) return;
            const el = curSlide.elements.find(x => x.id === canvasEl.dataset.elementId);
            if (!el || el.locked) return;
            const scale = AppState.zoom / 100;
            this._dragState = {
                elementId: el.id,
                slideId: curSlide.id,
                startX: e.clientX,
                startY: e.clientY,
                origX: el.x,
                origY: el.y,
                scale
            };
        }
    },

    _handleMouseMove(e) {
        if (this._dragState) {
            const dx = (e.clientX - this._dragState.startX) / this._dragState.scale;
            const dy = (e.clientY - this._dragState.startY) / this._dragState.scale;
            AppState.moveElement(this._dragState.slideId, this._dragState.elementId, this._dragState.origX + dx, this._dragState.origY + dy);
        }
        if (this._resizeState) {
            const rs = this._resizeState;
            const dx = (e.clientX - rs.startX) / rs.scale;
            const dy = (e.clientY - rs.startY) / rs.scale;
            let newW = rs.origW, newH = rs.origH, newX = rs.origX, newY = rs.origY;
            if (rs.handle.includes('e')) { newW = rs.origW + dx; }
            if (rs.handle.includes('w')) { newW = rs.origW - dx; newX = rs.origX + dx; }
            if (rs.handle.includes('s')) { newH = rs.origH + dy; }
            if (rs.handle.includes('n')) { newH = rs.origH - dy; newY = rs.origY + dy; }
            AppState.moveElement(rs.slideId, rs.elementId, newX, newY);
            AppState.resizeElement(rs.slideId, rs.elementId, newW, newH);
        }
    },

    _handleMouseUp(e) {
        this._dragState = null;
        this._resizeState = null;
    },

    // ── Keyboard handler ──
    _handleKeyDown(e) {
        // Presenter mode navigation
        if (AppState.currentView === 'presenter') {
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                const slides = AppState.getSlidesForPresentation(AppState.currentPresentationId);
                if (AppState.presenterSlideIndex < slides.length - 1) {
                    AppState.presenterSlideIndex++;
                    this.render();
                }
            } else if (e.key === 'ArrowLeft' || e.key === 'Backspace') {
                e.preventDefault();
                if (AppState.presenterSlideIndex > 0) {
                    AppState.presenterSlideIndex--;
                    this.render();
                }
            } else if (e.key === 'Escape') {
                this._stopPresenterTimer();
                this.navigate('editor/' + AppState.currentPresentationId);
            }
            return;
        }

        // Editor shortcuts
        if (AppState.currentView === 'editor') {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            if (e.key === 'Delete' || e.key === 'Backspace') {
                const curSlide = AppState.getCurrentSlide();
                if (curSlide && AppState.selectedElementId) {
                    e.preventDefault();
                    AppState.deleteElement(curSlide.id, AppState.selectedElementId);
                    AppState.selectedElementId = null;
                    AppState.selectedElementIds = [];
                    this.render();
                }
            }
            if (e.key === 'Escape') {
                if (AppState.activeModal) {
                    AppState.activeModal = null;
                    this.render();
                } else {
                    AppState.selectedElementId = null;
                    AppState.selectedElementIds = [];
                    this.render();
                }
            }
            // Tool shortcuts
            if (e.key === 'v' || e.key === 'V') { AppState.activeTool = 'select'; this.render(); }
            if (e.key === 't' || e.key === 'T') { AppState.activeTool = 'text'; this.render(); }
            if (e.key === 'r' || e.key === 'R') { AppState.activeTool = 'rectangle'; this.render(); }
            if (e.key === 'o' || e.key === 'O') { AppState.activeTool = 'circle'; this.render(); }
            if (e.key === 'l' || e.key === 'L') { AppState.activeTool = 'line'; this.render(); }
        }
    },

    // ── Create presentation from modal ──
    _createPresentation() {
        const titleInput = document.querySelector('[data-input="new-pres-title"]');
        const descInput = document.querySelector('[data-input="new-pres-description"]');
        const tagsInput = document.querySelector('[data-input="new-pres-tags"]');
        const themeActive = document.querySelector('[data-dropdown="new-pres-theme"] .dropdown-item.active');

        const title = titleInput ? titleInput.value.trim() : '';
        if (!title) {
            Components.showToast('Please enter a title', 'error');
            return;
        }

        const tags = tagsInput ? tagsInput.value.split(',').map(t => t.trim()).filter(Boolean) : [];
        const theme = themeActive ? themeActive.dataset.value : 'minimal';
        const description = descInput ? descInput.value.trim() : '';

        const id = AppState.createPresentation({ title, description, theme, tags });
        AppState.activeModal = null;
        Components.showToast('Presentation created', 'success');
        this.navigate('editor/' + id);
    },

    // ── Presenter timer ──
    _startPresenterTimer() {
        this._stopPresenterTimer();
        AppState.presenterTimerStart = Date.now();
        this._presenterInterval = setInterval(() => {
            const el = document.getElementById('presenterTimer');
            if (!el) return;
            const elapsed = Math.floor((Date.now() - AppState.presenterTimerStart) / 1000);
            const min = String(Math.floor(elapsed / 60)).padStart(2, '0');
            const sec = String(elapsed % 60).padStart(2, '0');
            el.textContent = `${min}:${sec}`;
        }, 1000);
    },

    _stopPresenterTimer() {
        if (this._presenterInterval) {
            clearInterval(this._presenterInterval);
            this._presenterInterval = null;
        }
    }
};

// ─── Boot ───
document.addEventListener('DOMContentLoaded', () => App.init());
