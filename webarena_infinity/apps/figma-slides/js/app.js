const App = {
    init() {
        AppState.init();
        AppState.subscribe(() => this.render());

        document.addEventListener('click', (e) => this.handleClick(e));
        document.addEventListener('change', (e) => this.handleChange(e));
        document.addEventListener('input', (e) => this.handleInput(e));
        document.addEventListener('keydown', (e) => this.handleKeydown(e));
        document.addEventListener('contextmenu', (e) => this.handleContextMenu(e));

        this._connectSSE();
        this.render();
        AppState._pushStateToServer();
    },

    render() {
        const toolbar = document.getElementById('toolbar');
        const leftSidebar = document.getElementById('left-sidebar');
        const canvas = document.getElementById('canvas');
        const rightSidebar = document.getElementById('right-sidebar');
        const modalContainer = document.getElementById('modal-container');
        const toastContainer = document.getElementById('toast-container');
        const contextMenuContainer = document.getElementById('context-menu-container');

        if (toolbar) toolbar.innerHTML = Views.renderToolbar();
        if (leftSidebar) leftSidebar.innerHTML = Views.renderLeftSidebar();
        if (canvas) canvas.innerHTML = Views.renderCanvas();
        if (rightSidebar) rightSidebar.innerHTML = Views.renderRightSidebar();
        if (modalContainer) modalContainer.innerHTML = Views.renderModals();
        if (toastContainer) toastContainer.innerHTML = Views.renderToast();
        if (contextMenuContainer) contextMenuContainer.innerHTML = Views.renderContextMenu();

        this._restoreFocus();
    },

    _restoreFocus() {
        if (AppState.activeModal === 'editTableCell') {
            const input = document.getElementById('tableCellValue');
            if (input) setTimeout(() => input.focus(), 0);
        } else if (AppState.activeModal === 'editText') {
            const ta = document.getElementById('editTextValue');
            if (ta) setTimeout(() => ta.focus(), 0);
        }
    },

    handleClick(e) {
        // Close context menu on any click
        if (AppState.contextMenuData) {
            AppState.contextMenuData = null;
            AppState._listeners.forEach(fn => fn());
        }

        // Close open dropdowns if clicking outside
        if (!e.target.closest('.custom-dropdown')) {
            document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
        }

        // Close color picker panels if clicking outside
        if (!e.target.closest('.color-picker')) {
            document.querySelectorAll('.color-picker-panel.open').forEach(p => p.classList.remove('open'));
        }

        const action = e.target.closest('[data-action]');
        if (!action) {
            // Click on canvas area but not on an object = deselect
            if (e.target.closest('.canvas-slide') && !e.target.closest('.slide-object')) {
                AppState.deselectObject();
            }
            return;
        }

        const actionName = action.dataset.action;
        e.preventDefault();

        switch (actionName) {
            // Navigation
            case 'setView':
                AppState.currentView = action.dataset.view;
                AppState._listeners.forEach(fn => fn());
                break;

            case 'setGridView':
                AppState.gridView = action.dataset.grid === 'true';
                AppState._listeners.forEach(fn => fn());
                break;

            // Slide operations
            case 'selectSlide':
                AppState.selectSlide(action.dataset.slideId);
                break;

            case 'addSlide':
                AppState.openModal('addSlide');
                break;

            case 'confirmAddSlide':
                AppState.closeModal();
                AppState.addSlide(action.dataset.layout);
                AppState.showToast('Slide added');
                break;

            case 'duplicateSlide':
                AppState.duplicateSlide(action.dataset.slideId || AppState.selectedSlideId);
                AppState.showToast('Slide duplicated');
                break;

            case 'deleteSlideConfirm': {
                const slide = AppState.getSelectedSlide();
                AppState.openModal('confirmDelete', { slideId: action.dataset.slideId || AppState.selectedSlideId, title: slide?.title });
                break;
            }

            case 'confirmModal':
                if (action.dataset.modalId === 'confirmDelete' && AppState.modalData) {
                    AppState.deleteSlide(AppState.modalData.slideId);
                    AppState.closeModal();
                    AppState.showToast('Slide deleted');
                }
                break;

            case 'skipSlide':
                AppState.toggleSkipSlide(action.dataset.slideId || AppState.selectedSlideId);
                AppState.showToast(AppState.slides.find(s => s.id === (action.dataset.slideId || AppState.selectedSlideId))?.skipped ? 'Slide skipped' : 'Slide unskipped');
                break;

            // Object operations
            case 'selectObject':
                AppState.selectedSlideId = action.dataset.slideId;
                AppState.selectObject(action.dataset.objectId);
                break;

            case 'deleteObject':
                AppState.deleteObject(action.dataset.slideId, action.dataset.objectId);
                AppState.showToast('Object deleted');
                break;

            case 'toggleObjectLock':
                AppState.toggleObjectLock(action.dataset.slideId, action.dataset.objectId);
                break;

            case 'toggleObjectVisibility':
                AppState.toggleObjectVisibility(action.dataset.slideId, action.dataset.objectId);
                break;

            // Text editing
            case 'addText':
                if (AppState.selectedSlideId) {
                    AppState.addObject(AppState.selectedSlideId, {
                        type: 'text', name: 'Text', x: 200, y: 200, width: 400, height: 60,
                        text: 'Double-click to edit', fontSize: 20, fontWeight: 400, fontFamily: 'Inter',
                        color: '#FFFFFF', textAlign: 'left'
                    });
                    AppState.showToast('Text added');
                }
                break;

            // Shapes
            case 'openShapes':
                AppState.openModal('shapes');
                break;

            case 'insertShape':
                if (AppState.selectedSlideId) {
                    AppState.closeModal();
                    AppState.addObject(AppState.selectedSlideId, {
                        type: 'shape', name: action.dataset.shapeType, shapeType: action.dataset.shapeType,
                        x: 200, y: 200, width: 200, height: 150,
                        fill: '#2C2C2C', stroke: null, cornerRadius: action.dataset.shapeType === 'rounded_rect' ? 12 : 0,
                        text: '', fontSize: 14, fontWeight: 400, fontFamily: 'Inter', color: '#FFFFFF', textAlign: 'center'
                    });
                    AppState.showToast('Shape added');
                }
                break;

            // Images
            case 'addImage':
                if (AppState.selectedSlideId) {
                    AppState.addObject(AppState.selectedSlideId, {
                        type: 'image', name: 'Image', x: 200, y: 150, width: 400, height: 300,
                        src: '', fillMode: 'fill', cornerRadius: 0
                    });
                    AppState.showToast('Image placeholder added');
                }
                break;

            // Assets
            case 'openAssets':
                AppState.openModal('assets', { tab: 'components' });
                break;

            case 'switchTab':
                if (action.dataset.tabGroup === 'rightPanelTabs') {
                    AppState.setActivePanel(action.dataset.tabId);
                } else if (action.dataset.tabGroup === 'assetsTabs') {
                    AppState.modalData = { ...AppState.modalData, tab: action.dataset.tabId };
                    AppState._listeners.forEach(fn => fn());
                } else if (action.dataset.tabGroup === 'commentsTabs') {
                    AppState.modalData = { ...AppState.modalData, tab: action.dataset.tabId };
                    AppState._listeners.forEach(fn => fn());
                }
                break;

            // Tables
            case 'insertTable':
                if (AppState.selectedSlideId) {
                    AppState.closeModal();
                    AppState.addObject(AppState.selectedSlideId, {
                        type: 'table', name: 'Table', x: 80, y: 150, width: 600, height: 200,
                        rows: 4, columns: 4,
                        cells: [['Header 1', 'Header 2', 'Header 3', 'Header 4'], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']],
                        headerRow: true,
                        headerStyle: { background: '#2C2C2C', color: '#FFFFFF', fontWeight: 700 },
                        cellStyle: { background: 'transparent', color: '#E0E0E0', fontWeight: 400 },
                        borderColor: '#404040', fontSize: 14
                    });
                    AppState.showToast('Table added');
                }
                break;

            case 'editTableCell':
                AppState.openModal('editTableCell', {
                    slideId: action.dataset.slideId,
                    objectId: action.dataset.objectId,
                    row: parseInt(action.dataset.row),
                    col: parseInt(action.dataset.col)
                });
                break;

            case 'confirmTableCellEdit': {
                const input = document.getElementById('tableCellValue');
                if (input && AppState.modalData) {
                    AppState.updateTableCell(AppState.modalData.slideId, AppState.modalData.objectId, AppState.modalData.row, AppState.modalData.col, input.value);
                    AppState.closeModal();
                }
                break;
            }

            case 'addTableRow':
                AppState.addTableRow(action.dataset.slideId, action.dataset.objectId);
                break;

            case 'addTableColumn':
                AppState.addTableColumn(action.dataset.slideId, action.dataset.objectId);
                break;

            // Code blocks
            case 'insertCodeBlock':
                if (AppState.selectedSlideId) {
                    AppState.closeModal();
                    AppState.addObject(AppState.selectedSlideId, {
                        type: 'code', name: 'Code Block', x: 80, y: 150, width: 600, height: 200,
                        code: '// Your code here\n', language: 'JavaScript', theme: 'dark', fontSize: 14
                    });
                    AppState.showToast('Code block added');
                }
                break;

            // Slide numbers
            case 'insertSlideNumber':
                if (AppState.selectedSlideId) {
                    AppState.updateSlideNumberEnabled(AppState.selectedSlideId, true);
                    AppState.closeModal();
                    AppState.showToast('Slide number added');
                }
                break;

            case 'addSlideNumbersToAll':
                AppState.addSlideNumbersToAll();
                AppState.showToast('Slide numbers added to all slides');
                break;

            // Interactions
            case 'openInteractions':
                AppState.openModal('interactions');
                break;

            case 'insertInteraction':
                if (AppState.selectedSlideId) {
                    AppState.closeModal();
                    const type = action.dataset.interactionType;
                    let obj = {
                        type: 'liveInteraction', interactionType: type,
                        name: type.charAt(0).toUpperCase() + type.slice(1),
                        x: 200, y: 200, width: 400, height: 280
                    };
                    if (type === 'poll') {
                        obj.question = 'Your question here?';
                        obj.options = [
                            { id: 'opt_new_1', text: 'Option 1', votes: 0 },
                            { id: 'opt_new_2', text: 'Option 2', votes: 0 },
                            { id: 'opt_new_3', text: 'Option 3', votes: 0 }
                        ];
                        obj.hideResults = false;
                    } else if (type === 'alignment') {
                        obj.question = 'How do you feel about this?';
                        obj.scaleMin = 1;
                        obj.scaleMax = 5;
                        obj.scaleLabels = { min: 'Disagree', max: 'Agree' };
                        obj.responses = [];
                        obj.hideResults = false;
                    } else if (type === 'stamps') {
                        obj.stampTypes = ['thumbsUp', 'heart', 'fire', 'clap', 'rocket'];
                        obj.stamps = [];
                    }
                    AppState.addObject(AppState.selectedSlideId, obj);
                    AppState.showToast(`${type} interaction added`);
                }
                break;

            // Live interaction actions
            case 'votePoll':
                AppState.addPollVote(action.dataset.slideId, action.dataset.objectId, action.dataset.optionId);
                break;

            case 'togglePollResults':
                AppState.togglePollResultsVisibility(action.dataset.slideId, action.dataset.objectId);
                break;

            case 'submitAlignment':
                AppState.addAlignmentResponse(action.dataset.slideId, action.dataset.objectId, parseInt(action.dataset.value));
                break;

            case 'addStamp':
                AppState.addStamp(action.dataset.slideId, action.dataset.objectId, action.dataset.stampType);
                break;

            // Transitions
            case 'setTransitionDirection':
                if (AppState.selectedSlideId) {
                    AppState.updateSlideTransition(AppState.selectedSlideId, { direction: action.dataset.direction });
                }
                break;

            case 'applyTransitionToAll': {
                const slide = AppState.getSelectedSlide();
                if (slide) {
                    AppState.applyTransitionToAll(slide.transition);
                    AppState.showToast('Transition applied to all slides');
                }
                break;
            }

            // Animation
            case 'addAnimation':
                AppState.addAnimation(action.dataset.slideId, action.dataset.objectId, {
                    style: 'fade', duration: 400, timing: 'on_click', direction: 'in', order: 0
                });
                break;

            case 'removeAnimation':
                AppState.removeAnimation(action.dataset.slideId, action.dataset.objectId);
                break;

            // Background type
            case 'setBgType':
                if (AppState.selectedSlideId) {
                    const bgType = action.dataset.type;
                    let bg;
                    if (bgType === 'solid') bg = { type: 'solid', color: '#1E1E1E' };
                    else if (bgType === 'gradient') bg = { type: 'gradient', gradient: { type: 'linear', angle: 135, stops: [{ color: '#1E1E1E', position: 0 }, { color: '#2D1B69', position: 100 }] } };
                    else bg = { type: 'image', imageUrl: '' };
                    AppState.updateSlideBackground(AppState.selectedSlideId, bg);
                }
                break;

            // Template styles
            case 'remixColors':
                AppState.showToast('Colors remixed');
                break;

            case 'openTemplateStyles':
                AppState.openModal('templateStyles', { styleId: AppState.deckSettings.defaultTemplateStyle });
                break;

            case 'addTemplateColor':
                AppState.addTemplateColor(action.dataset.styleId, { name: 'New Color', value: '#888888' });
                break;

            case 'removeTemplateColor':
                AppState.removeTemplateColor(action.dataset.styleId, action.dataset.colorId);
                break;

            case 'addTemplateTextStyle':
                AppState.addTemplateTextStyle(action.dataset.styleId, { name: 'New Style' });
                break;

            case 'removeTemplateTextStyle':
                AppState.removeTemplateTextStyle(action.dataset.styleId, action.dataset.textStyleId);
                break;

            // Libraries
            case 'openLibraries':
                AppState.openModal('libraries');
                break;

            case 'removeLibrary':
                AppState.removeLibrary(action.dataset.libraryId);
                AppState.showToast('Library removed');
                break;

            case 'updateLibrary':
                AppState.updateLibrary(action.dataset.libraryId);
                AppState.showToast('Library updated');
                break;

            // Comments
            case 'openComments':
                AppState.openModal('comments', { tab: 'slide' });
                break;

            case 'submitComment': {
                const input = document.getElementById('newCommentInput');
                if (input && input.value.trim()) {
                    AppState.addComment(AppState.selectedSlideId, input.value.trim());
                    AppState.showToast('Comment added');
                }
                break;
            }

            case 'addCommentFromModal': {
                const newInput = document.getElementById('newCommentInput');
                if (newInput) newInput.focus();
                break;
            }

            case 'submitReply': {
                const replyInput = document.querySelector(`[data-input-id="commentReply"][data-comment-id="${action.dataset.commentId}"]`);
                if (replyInput && replyInput.value.trim()) {
                    AppState.replyToComment(action.dataset.commentId, replyInput.value.trim());
                }
                break;
            }

            case 'resolveComment':
                AppState.resolveComment(action.dataset.commentId);
                break;

            case 'unresolveComment':
                AppState.unresolveComment(action.dataset.commentId);
                break;

            case 'deleteComment':
                AppState.deleteComment(action.dataset.commentId);
                AppState.showToast('Comment deleted');
                break;

            // Share
            case 'openShare':
                AppState.openModal('share');
                break;

            case 'copyPresentationLink':
                AppState.showToast('Presentation link copied');
                break;

            case 'removeCollaborator':
                AppState.removeCollaborator(action.dataset.userId);
                AppState.showToast('Collaborator removed');
                break;

            // Present
            case 'openPresent':
                AppState.openModal('present');
                break;

            case 'startPresent':
                AppState.closeModal();
                AppState.showToast(`Presenting in ${action.dataset.mode === 'present_notes' ? 'presenter + notes' : 'fullscreen'} mode`);
                break;

            // Export
            case 'openExportModal':
                AppState.openModal('export', { format: 'pdf', colorProfile: 'srgb', quality: 'high', slidesIncluded: 'all' });
                break;

            case 'confirmExport': {
                const data = AppState.modalData || {};
                const ext = data.format === 'pptx' ? '.pptx' : '.pdf';
                AppState.addExport({
                    format: data.format || 'pdf',
                    fileName: AppState.deckSettings.name.replace(/\s+/g, '-') + ext,
                    fileSize: data.format === 'pptx' ? '8.2 MB' : '4.5 MB',
                    colorProfile: data.colorProfile,
                    quality: data.quality,
                    slidesIncluded: data.slidesIncluded
                });
                AppState.closeModal();
                AppState.showToast('Export started');
                break;
            }

            // Design mode
            case 'toggleDesignMode':
                AppState.toggleDesignMode();
                break;

            // Presenter notes
            case 'togglePresenterNotes':
                AppState.togglePresenterNotes();
                break;

            // Deck settings
            case 'openDeckSettings':
                AppState.openModal('deckSettings');
                break;

            case 'saveDeckSettings': {
                const nameInput = document.querySelector('[data-input-id="settingsDeckName"]');
                if (nameInput) AppState.updateDeckName(nameInput.value);
                AppState.closeModal();
                AppState.showToast('Settings saved');
                break;
            }

            // Dropdown
            case 'toggleDropdown': {
                const menu = action.closest('.custom-dropdown')?.querySelector('.dropdown-menu');
                if (menu) {
                    const wasOpen = menu.classList.contains('open');
                    document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
                    if (!wasOpen) menu.classList.add('open');
                }
                break;
            }

            case 'selectDropdownItem': {
                const dropdownId = action.dataset.dropdownId;
                const value = action.dataset.value;
                this._handleDropdownChange(dropdownId, value);
                const menu = action.closest('.dropdown-menu');
                if (menu) menu.classList.remove('open');
                break;
            }

            // Color picker
            case 'toggleColorPicker': {
                const panel = action.closest('.color-picker')?.querySelector('.color-picker-panel');
                if (panel) {
                    panel.classList.toggle('open');
                }
                break;
            }

            case 'selectColor': {
                const pickerId = action.dataset.pickerId;
                const color = action.dataset.color;
                this._handleColorChange(pickerId, color);
                const panel = action.closest('.color-picker-panel');
                if (panel) panel.classList.remove('open');
                break;
            }

            // Modal
            case 'closeModal':
                AppState.closeModal();
                break;

            // Misc
            case 'goHome':
                AppState.openModal('deckSettings');
                break;

            case 'clearSearch':
                AppState.setSearchQuery('');
                break;
        }
    },

    handleChange(e) {
        const target = e.target;

        // Toggle switches
        if (target.dataset.action === 'toggle') {
            const toggleId = target.dataset.toggleId;
            const checked = target.checked;
            this._handleToggleChange(toggleId, checked);
        }
    },

    handleInput(e) {
        const target = e.target;
        const inputId = target.dataset.inputId;
        if (!inputId) {
            // Slider
            const sliderId = target.dataset.sliderId;
            if (sliderId) {
                this._handleSliderChange(sliderId, parseFloat(target.value));
                const valueSpan = target.nextElementSibling;
                if (valueSpan) valueSpan.textContent = target.value;
            }
            return;
        }

        switch (inputId) {
            case 'deckName':
                AppState.updateDeckName(target.value);
                break;
            case 'presenterNotes':
                AppState.updatePresenterNotes(target.dataset.slideId, target.value);
                break;
            case 'objectName':
                AppState.updateObject(target.dataset.slideId, target.dataset.objectId, { name: target.value });
                break;
            case 'searchInput':
                AppState.setSearchQuery(target.value);
                break;
        }
    },

    handleKeydown(e) {
        // Close modal on Escape
        if (e.key === 'Escape') {
            if (AppState.activeModal) {
                AppState.closeModal();
                e.preventDefault();
            } else if (AppState.selectedObjectId) {
                AppState.deselectObject();
                e.preventDefault();
            }
        }

        // Delete selected object
        if ((e.key === 'Delete' || e.key === 'Backspace') && AppState.selectedObjectId && !e.target.closest('input, textarea')) {
            const slide = AppState.getSelectedSlide();
            const obj = AppState.getSelectedObject();
            if (slide && obj && !obj.locked) {
                AppState.deleteObject(slide.id, obj.id);
                e.preventDefault();
            }
        }

        // Duplicate slide: Cmd+D
        if ((e.metaKey || e.ctrlKey) && e.key === 'd' && !e.target.closest('input, textarea')) {
            e.preventDefault();
            if (AppState.selectedSlideId) {
                AppState.duplicateSlide(AppState.selectedSlideId);
                AppState.showToast('Slide duplicated');
            }
        }

        // Toggle design mode: Shift+D
        if (e.shiftKey && e.key === 'D' && !e.target.closest('input, textarea')) {
            AppState.toggleDesignMode();
        }

        // Enter on modal inputs
        if (e.key === 'Enter' && AppState.activeModal) {
            if (AppState.activeModal === 'editTableCell') {
                const input = document.getElementById('tableCellValue');
                if (input && AppState.modalData) {
                    AppState.updateTableCell(AppState.modalData.slideId, AppState.modalData.objectId, AppState.modalData.row, AppState.modalData.col, input.value);
                    AppState.closeModal();
                }
            }
        }
    },

    handleContextMenu(e) {
        const slideThumbnail = e.target.closest('[data-context-menu="slide"]');
        if (slideThumbnail) {
            e.preventDefault();
            const slideId = slideThumbnail.dataset.slideId;
            const slide = AppState.slides.find(s => s.id === slideId);
            if (!slide) return;

            AppState.contextMenuData = {
                x: e.clientX,
                y: e.clientY,
                items: [
                    { label: 'Duplicate', action: 'duplicateSlide', data: { 'slide-id': slideId } },
                    { label: slide.skipped ? 'Unskip slide' : 'Skip slide', action: 'skipSlide', data: { 'slide-id': slideId } },
                    { separator: true },
                    { label: 'Delete', action: 'deleteSlideConfirm', data: { 'slide-id': slideId }, disabled: AppState.slides.length <= 1 }
                ]
            };
            AppState._listeners.forEach(fn => fn());
        }
    },

    _handleDropdownChange(dropdownId, value) {
        const slide = AppState.getSelectedSlide();
        const obj = AppState.getSelectedObject();

        switch (dropdownId) {
            // Slide properties
            case 'slideTemplateStyle':
                if (slide) AppState.updateSlideTemplateStyle(slide.id, value);
                break;
            case 'slideNumberCount':
                if (slide) AppState.updateSlideNumberCount(slide.id, value);
                break;
            case 'slideNumberFormat':
                if (slide) AppState.updateSlideNumberFormat(slide.id, value);
                break;

            // Object text properties
            case 'objFont':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { fontFamily: value });
                break;
            case 'objFontWeight':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { fontWeight: parseInt(value) });
                break;
            case 'objTextAlign':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { textAlign: value });
                break;

            // Shape properties
            case 'objShapeType':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { shapeType: value });
                break;

            // Code properties
            case 'objCodeLang':
                if (slide && obj) AppState.updateCodeBlock(slide.id, obj.id, { language: value });
                break;
            case 'objCodeTheme':
                if (slide && obj) AppState.updateCodeBlock(slide.id, obj.id, { theme: value });
                break;

            // Transition properties
            case 'transitionType':
                if (slide) {
                    const transType = TRANSITION_TYPES.find(t => t.id === value);
                    const updates = { type: value };
                    if (transType && transType.hasDirection) {
                        updates.direction = transType.directions[0];
                    } else {
                        updates.direction = null;
                    }
                    AppState.updateSlideTransition(slide.id, updates);
                }
                break;
            case 'transitionEasing':
                if (slide) AppState.updateSlideTransition(slide.id, { easing: value });
                break;
            case 'transitionTiming':
                if (slide) AppState.updateSlideTransition(slide.id, { timing: value });
                break;

            // Animation properties
            case 'animStyle':
                if (slide && obj) AppState.updateAnimation(slide.id, obj.id, { style: value });
                break;
            case 'animTiming':
                if (slide && obj) AppState.updateAnimation(slide.id, obj.id, { timing: value });
                break;
            case 'animDirection':
                if (slide && obj) AppState.updateAnimation(slide.id, obj.id, { direction: value });
                break;

            // Share settings
            case 'shareLinkAccess':
                AppState.updateShareSettings({ linkAccess: value });
                break;
            case 'shareLinkRole':
                AppState.updateShareSettings({ linkRole: value });
                break;

            // Export
            case 'exportFormat':
                if (AppState.modalData) {
                    AppState.modalData.format = value;
                    AppState._listeners.forEach(fn => fn());
                }
                break;
            case 'exportColorProfile':
                if (AppState.modalData) {
                    AppState.modalData.colorProfile = value;
                    AppState._listeners.forEach(fn => fn());
                }
                break;
            case 'exportQuality':
                if (AppState.modalData) {
                    AppState.modalData.quality = value;
                    AppState._listeners.forEach(fn => fn());
                }
                break;
            case 'exportSlides':
                if (AppState.modalData) {
                    AppState.modalData.slidesIncluded = value;
                    AppState._listeners.forEach(fn => fn());
                }
                break;

            // Deck settings
            case 'settingsAspectRatio':
                AppState.updateDeckAspectRatio(value);
                break;
            case 'settingsDefaultTransType':
                AppState.updateDefaultTransition({ ...AppState.deckSettings.defaultTransition, type: value });
                break;
            case 'settingsSlideNumFormat':
                AppState.updateDeckSlideNumbers({ slideNumberFormat: value });
                break;
            case 'settingsDefaultTemplate':
                AppState.updateDefaultTemplateStyle(value);
                break;

            // Collaborator role
            default:
                if (dropdownId.startsWith('collabRole_')) {
                    const userId = dropdownId.replace('collabRole_', '');
                    AppState.updateCollaboratorRole(userId, value);
                }
                break;
        }
    },

    _handleToggleChange(toggleId, checked) {
        const slide = AppState.getSelectedSlide();

        switch (toggleId) {
            case 'slideNumberEnabled':
                if (slide) AppState.updateSlideNumberEnabled(slide.id, checked);
                break;
            case 'slideNumberIncludeTotal':
                if (slide) AppState.updateSlideNumberIncludeTotal(slide.id, checked);
                break;
            case 'tableHeaderRow':
                if (slide && AppState.selectedObjectId) {
                    AppState.updateObject(slide.id, AppState.selectedObjectId, { headerRow: checked });
                }
                break;
            case 'pollHideResults':
                if (slide && AppState.selectedObjectId) {
                    AppState.togglePollResultsVisibility(slide.id, AppState.selectedObjectId);
                }
                break;
            case 'shareAllowCopy':
                AppState.updateShareSettings({ allowCopy: checked });
                break;
            case 'shareAllowDownload':
                AppState.updateShareSettings({ allowDownload: checked });
                break;
            case 'availableOffline':
                AppState.toggleAvailableOffline();
                break;
            case 'settingsSlideNumbers':
                AppState.updateDeckSlideNumbers({ slideNumbersEnabled: checked });
                break;
            case 'settingsSlideNumTotal':
                AppState.updateDeckSlideNumbers({ slideNumberIncludeTotal: checked });
                break;
        }
    },

    _handleSliderChange(sliderId, value) {
        const slide = AppState.getSelectedSlide();
        const obj = AppState.getSelectedObject();

        switch (sliderId) {
            case 'objOpacity':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { opacity: value });
                break;
        }
    },

    _handleColorChange(pickerId, color) {
        const slide = AppState.getSelectedSlide();
        const obj = AppState.getSelectedObject();

        switch (pickerId) {
            case 'slideBgColor':
                if (slide) AppState.updateSlideBackground(slide.id, { type: 'solid', color: color });
                break;
            case 'gradientStart':
                if (slide && slide.background.type === 'gradient') {
                    const grad = { ...slide.background.gradient };
                    grad.stops = [...grad.stops];
                    grad.stops[0] = { ...grad.stops[0], color: color };
                    AppState.updateSlideBackground(slide.id, { type: 'gradient', gradient: grad });
                }
                break;
            case 'gradientEnd':
                if (slide && slide.background.type === 'gradient') {
                    const grad = { ...slide.background.gradient };
                    grad.stops = [...grad.stops];
                    grad.stops[1] = { ...grad.stops[1], color: color };
                    AppState.updateSlideBackground(slide.id, { type: 'gradient', gradient: grad });
                }
                break;
            case 'objTextColor':
            case 'objShapeTextColor':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { color: color });
                break;
            case 'objFill':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { fill: color });
                break;
            case 'objStrokeColor':
                if (slide && obj && obj.stroke) {
                    AppState.updateObject(slide.id, obj.id, { stroke: { ...obj.stroke, color: color } });
                }
                break;
            case 'tableBorderColor':
                if (slide && obj) AppState.updateObject(slide.id, obj.id, { borderColor: color });
                break;
            case 'tableHeaderBg':
                if (slide && obj) {
                    AppState.updateObject(slide.id, obj.id, { headerStyle: { ...obj.headerStyle, background: color } });
                }
                break;
        }
    },

    _connectSSE() {
        const eventSource = new EventSource('/api/events');
        eventSource.onmessage = (e) => {
            if (e.data === 'reset') {
                AppState.resetToSeedData();
            }
        };
        eventSource.onerror = () => {
            setTimeout(() => this._connectSSE(), 5000);
        };
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
