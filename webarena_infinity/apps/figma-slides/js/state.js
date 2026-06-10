const AppState = {
    // Persistent state
    slides: [],
    deckSettings: {},
    templateStyles: [],
    comments: [],
    libraries: [],
    collaborators: [],
    currentUser: {},
    exportHistory: [],
    versionHistory: [],
    availableTemplates: [],
    _seedVersion: SEED_DATA_VERSION,
    _nextSlideOrder: 16,
    _nextCommentId: 7,
    _nextObjectId: 200,

    // UI state (not persisted)
    currentView: 'slides',
    selectedSlideId: null,
    selectedObjectId: null,
    activePanel: 'design',
    activeModal: null,
    modalData: null,
    toastMessage: null,
    searchQuery: '',
    gridView: false,
    designMode: false,
    presenterNotesVisible: true,
    sidebarCollapsed: false,
    contextMenuData: null,

    // Listeners
    _listeners: [],

    subscribe(fn) {
        this._listeners.push(fn);
    },

    notify() {
        this._persist();
        this._pushStateToServer();
        this._listeners.forEach(fn => fn());
    },

    _persist() {
        const state = this.getSerializableState();
        localStorage.setItem('figmaSlidesState', JSON.stringify(state));
    },

    _pushStateToServer() {
        const state = this.getSerializableState();
        fetch('/api/state', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(state)
        }).catch(() => {});
    },

    getSerializableState() {
        return {
            slides: this.slides,
            deckSettings: this.deckSettings,
            templateStyles: this.templateStyles,
            comments: this.comments,
            libraries: this.libraries,
            collaborators: this.collaborators,
            currentUser: this.currentUser,
            exportHistory: this.exportHistory,
            versionHistory: this.versionHistory,
            availableTemplates: this.availableTemplates,
            _seedVersion: this._seedVersion,
            _nextSlideOrder: this._nextSlideOrder,
            _nextCommentId: this._nextCommentId,
            _nextObjectId: this._nextObjectId
        };
    },

    init() {
        const saved = localStorage.getItem('figmaSlidesState');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                if (parsed._seedVersion === SEED_DATA_VERSION) {
                    Object.assign(this, parsed);
                    if (!this.selectedSlideId && this.slides.length > 0) {
                        this.selectedSlideId = this.slides[0].id;
                    }
                    return;
                }
            } catch (e) {}
            localStorage.removeItem('figmaSlidesState');
        }
        this._loadSeedData();
    },

    _loadSeedData() {
        this.slides = JSON.parse(JSON.stringify(SLIDES));
        this.deckSettings = JSON.parse(JSON.stringify(DECK_SETTINGS));
        this.templateStyles = JSON.parse(JSON.stringify(TEMPLATE_STYLES));
        this.comments = JSON.parse(JSON.stringify(COMMENTS));
        this.libraries = JSON.parse(JSON.stringify(LIBRARIES));
        this.collaborators = JSON.parse(JSON.stringify(COLLABORATORS));
        this.currentUser = JSON.parse(JSON.stringify(CURRENT_USER));
        this.exportHistory = JSON.parse(JSON.stringify(EXPORT_HISTORY));
        this.versionHistory = JSON.parse(JSON.stringify(VERSION_HISTORY));
        this.availableTemplates = JSON.parse(JSON.stringify(AVAILABLE_TEMPLATES));
        this._seedVersion = SEED_DATA_VERSION;
        this._nextSlideOrder = 16;
        this._nextCommentId = 7;
        this._nextObjectId = 200;
        if (this.slides.length > 0) {
            this.selectedSlideId = this.slides[0].id;
        }
    },

    resetToSeedData() {
        localStorage.removeItem('figmaSlidesState');
        this._loadSeedData();
        this.currentView = 'slides';
        this.selectedObjectId = null;
        this.activePanel = 'design';
        this.activeModal = null;
        this.modalData = null;
        this.toastMessage = null;
        this.searchQuery = '';
        this.gridView = false;
        this.designMode = false;
        this.presenterNotesVisible = true;
        this.sidebarCollapsed = false;
        this.contextMenuData = null;
        this.notify();
    },

    // Slide operations
    getSelectedSlide() {
        return this.slides.find(s => s.id === this.selectedSlideId) || null;
    },

    getOrderedSlides() {
        return [...this.slides].sort((a, b) => a.order - b.order);
    },

    getSlideGroups() {
        const ordered = this.getOrderedSlides();
        const groups = [];
        let currentGroup = null;
        ordered.forEach(slide => {
            if (slide.groupId) {
                if (!currentGroup || currentGroup.id !== slide.groupId) {
                    currentGroup = { id: slide.groupId, name: slide.groupName, slides: [] };
                    groups.push(currentGroup);
                }
                currentGroup.slides.push(slide);
            } else {
                currentGroup = null;
                groups.push({ id: null, name: null, slides: [slide] });
            }
        });
        return groups;
    },

    selectSlide(slideId) {
        this.selectedSlideId = slideId;
        this.selectedObjectId = null;
        this.notify();
    },

    addSlide(layout, afterSlideId) {
        const afterSlide = afterSlideId ? this.slides.find(s => s.id === afterSlideId) : this.getSelectedSlide();
        const afterOrder = afterSlide ? afterSlide.order : this.slides.length - 1;

        this.slides.forEach(s => {
            if (s.order > afterOrder) s.order++;
        });

        const newSlide = {
            id: 'slide_' + Date.now().toString(36),
            order: afterOrder + 1,
            title: 'Untitled Slide',
            layout: layout || 'layout_blank',
            templateStyle: this.deckSettings.defaultTemplateStyle,
            skipped: false,
            groupId: afterSlide ? afterSlide.groupId : null,
            groupName: afterSlide ? afterSlide.groupName : null,
            background: { type: 'solid', color: '#1E1E1E' },
            presenterNotes: '',
            transition: JSON.parse(JSON.stringify(this.deckSettings.defaultTransition)),
            slideNumberEnabled: this.deckSettings.slideNumbersEnabled,
            slideNumberCount: this.deckSettings.slideNumberCount,
            slideNumberFormat: this.deckSettings.slideNumberFormat,
            slideNumberIncludeTotal: this.deckSettings.slideNumberIncludeTotal,
            objects: []
        };

        this.slides.push(newSlide);
        this._nextSlideOrder++;
        this.selectedSlideId = newSlide.id;
        this.selectedObjectId = null;
        this.notify();
        return newSlide;
    },

    duplicateSlide(slideId) {
        const source = this.slides.find(s => s.id === slideId);
        if (!source) return;

        this.slides.forEach(s => {
            if (s.order > source.order) s.order++;
        });

        const dup = JSON.parse(JSON.stringify(source));
        dup.id = 'slide_' + Date.now().toString(36);
        dup.order = source.order + 1;
        dup.title = source.title + ' (copy)';
        dup.objects = dup.objects.map(obj => ({
            ...obj,
            id: 'obj_' + (this._nextObjectId++).toString()
        }));

        this.slides.push(dup);
        this._nextSlideOrder++;
        this.selectedSlideId = dup.id;
        this.selectedObjectId = null;
        this.notify();
        return dup;
    },

    deleteSlide(slideId) {
        const idx = this.slides.findIndex(s => s.id === slideId);
        if (idx === -1 || this.slides.length <= 1) return;

        const deletedOrder = this.slides[idx].order;
        this.slides.splice(idx, 1);

        this.slides.forEach(s => {
            if (s.order > deletedOrder) s.order--;
        });

        this.comments = this.comments.filter(c => c.slideId !== slideId);

        if (this.selectedSlideId === slideId) {
            const ordered = this.getOrderedSlides();
            this.selectedSlideId = ordered[Math.min(idx, ordered.length - 1)]?.id || ordered[0]?.id;
        }
        this.selectedObjectId = null;
        this.notify();
    },

    moveSlide(slideId, newOrder) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;

        const oldOrder = slide.order;
        if (oldOrder === newOrder) return;

        if (newOrder > oldOrder) {
            this.slides.forEach(s => {
                if (s.order > oldOrder && s.order <= newOrder) s.order--;
            });
        } else {
            this.slides.forEach(s => {
                if (s.order >= newOrder && s.order < oldOrder) s.order++;
            });
        }
        slide.order = newOrder;
        this.notify();
    },

    toggleSkipSlide(slideId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.skipped = !slide.skipped;
        this.notify();
    },

    groupSlides(slideIds, groupName) {
        const groupId = 'group_' + Date.now().toString(36);
        slideIds.forEach(id => {
            const slide = this.slides.find(s => s.id === id);
            if (slide) {
                slide.groupId = groupId;
                slide.groupName = groupName || 'Untitled Group';
            }
        });
        this.notify();
    },

    ungroupSlide(slideId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.groupId = null;
        slide.groupName = null;
        this.notify();
    },

    renameGroup(groupId, newName) {
        this.slides.forEach(s => {
            if (s.groupId === groupId) {
                s.groupName = newName;
            }
        });
        this.notify();
    },

    // Slide properties
    updateSlideTitle(slideId, title) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.title = title;
        this.notify();
    },

    updateSlideBackground(slideId, background) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.background = background;
        this.notify();
    },

    updateSlideTransition(slideId, transition) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        Object.assign(slide.transition, transition);
        this.notify();
    },

    applyTransitionToAll(transition) {
        this.slides.forEach(s => {
            s.transition = JSON.parse(JSON.stringify(transition));
        });
        this.notify();
    },

    updatePresenterNotes(slideId, notes) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.presenterNotes = notes;
        this.notify();
    },

    updateSlideTemplateStyle(slideId, templateStyleId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.templateStyle = templateStyleId;
        this.notify();
    },

    // Slide number settings
    updateSlideNumberEnabled(slideId, enabled) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.slideNumberEnabled = enabled;
        this.notify();
    },

    updateSlideNumberCount(slideId, count) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.slideNumberCount = count;
        this.notify();
    },

    updateSlideNumberFormat(slideId, format) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.slideNumberFormat = format;
        this.notify();
    },

    updateSlideNumberIncludeTotal(slideId, includeTotal) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.slideNumberIncludeTotal = includeTotal;
        this.notify();
    },

    addSlideNumbersToAll() {
        this.slides.forEach(s => {
            s.slideNumberEnabled = true;
        });
        this.notify();
    },

    // Deck-level slide number settings
    updateDeckSlideNumbers(settings) {
        Object.assign(this.deckSettings, settings);
        this.notify();
    },

    // Object operations
    getSelectedObject() {
        if (!this.selectedSlideId || !this.selectedObjectId) return null;
        const slide = this.getSelectedSlide();
        if (!slide) return null;
        return slide.objects.find(o => o.id === this.selectedObjectId) || null;
    },

    selectObject(objectId) {
        this.selectedObjectId = objectId;
        this.notify();
    },

    deselectObject() {
        this.selectedObjectId = null;
        this.notify();
    },

    addObject(slideId, objectData) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;

        const obj = {
            id: 'obj_' + (this._nextObjectId++).toString(),
            ...objectData,
            opacity: objectData.opacity || 100,
            rotation: objectData.rotation || 0,
            locked: false,
            visible: true,
            animation: null
        };

        slide.objects.push(obj);
        this.selectedObjectId = obj.id;
        this.notify();
        return obj;
    },

    updateObject(slideId, objectId, updates) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj) return;
        Object.assign(obj, updates);
        this.notify();
    },

    deleteObject(slideId, objectId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        slide.objects = slide.objects.filter(o => o.id !== objectId);
        if (this.selectedObjectId === objectId) {
            this.selectedObjectId = null;
        }
        this.notify();
    },

    reorderObject(slideId, objectId, newIndex) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const idx = slide.objects.findIndex(o => o.id === objectId);
        if (idx === -1) return;
        const [obj] = slide.objects.splice(idx, 1);
        slide.objects.splice(newIndex, 0, obj);
        this.notify();
    },

    toggleObjectLock(slideId, objectId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj) return;
        obj.locked = !obj.locked;
        this.notify();
    },

    toggleObjectVisibility(slideId, objectId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj) return;
        obj.visible = !obj.visible;
        this.notify();
    },

    // Animation operations
    addAnimation(slideId, objectId, animation) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj) return;
        obj.animation = animation;
        this.notify();
    },

    removeAnimation(slideId, objectId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj) return;
        obj.animation = null;
        this.notify();
    },

    updateAnimation(slideId, objectId, updates) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || !obj.animation) return;
        Object.assign(obj.animation, updates);
        this.notify();
    },

    // Comment operations
    addComment(slideId, text, position) {
        const comment = {
            id: 'comment_' + String(this._nextCommentId++).padStart(3, '0'),
            slideId: slideId,
            userId: this.currentUser.id,
            userName: this.currentUser.name,
            avatarColor: this.currentUser.avatarColor,
            text: text,
            createdAt: new Date().toISOString(),
            resolved: false,
            replies: [],
            position: position || { x: 400, y: 300 }
        };
        this.comments.push(comment);
        this.notify();
        return comment;
    },

    replyToComment(commentId, text) {
        const comment = this.comments.find(c => c.id === commentId);
        if (!comment) return;
        comment.replies.push({
            id: 'reply_' + Date.now().toString(36),
            userId: this.currentUser.id,
            userName: this.currentUser.name,
            avatarColor: this.currentUser.avatarColor,
            text: text,
            createdAt: new Date().toISOString()
        });
        this.notify();
    },

    resolveComment(commentId) {
        const comment = this.comments.find(c => c.id === commentId);
        if (!comment) return;
        comment.resolved = true;
        this.notify();
    },

    unresolveComment(commentId) {
        const comment = this.comments.find(c => c.id === commentId);
        if (!comment) return;
        comment.resolved = false;
        this.notify();
    },

    deleteComment(commentId) {
        this.comments = this.comments.filter(c => c.id !== commentId);
        this.notify();
    },

    // Template style operations
    addTemplateColor(styleId, color) {
        const style = this.templateStyles.find(s => s.id === styleId);
        if (!style) return;
        style.colors.push({
            id: 'tc_' + Date.now().toString(36),
            name: color.name || 'New Color',
            value: color.value || '#888888'
        });
        this.notify();
    },

    updateTemplateColor(styleId, colorId, updates) {
        const style = this.templateStyles.find(s => s.id === styleId);
        if (!style) return;
        const color = style.colors.find(c => c.id === colorId);
        if (!color) return;
        Object.assign(color, updates);
        this.notify();
    },

    removeTemplateColor(styleId, colorId) {
        const style = this.templateStyles.find(s => s.id === styleId);
        if (!style) return;
        style.colors = style.colors.filter(c => c.id !== colorId);
        this.notify();
    },

    addTemplateTextStyle(styleId, textStyle) {
        const style = this.templateStyles.find(s => s.id === styleId);
        if (!style) return;
        style.textStyles.push({
            id: 'txt_' + Date.now().toString(36),
            name: textStyle.name || 'New Style',
            fontFamily: textStyle.fontFamily || 'Inter',
            fontSize: textStyle.fontSize || 16,
            fontWeight: textStyle.fontWeight || 400,
            lineHeight: textStyle.lineHeight || 1.5,
            letterSpacing: textStyle.letterSpacing || 0
        });
        this.notify();
    },

    updateTemplateTextStyle(styleId, textStyleId, updates) {
        const style = this.templateStyles.find(s => s.id === styleId);
        if (!style) return;
        const ts = style.textStyles.find(t => t.id === textStyleId);
        if (!ts) return;
        Object.assign(ts, updates);
        this.notify();
    },

    removeTemplateTextStyle(styleId, textStyleId) {
        const style = this.templateStyles.find(s => s.id === styleId);
        if (!style) return;
        style.textStyles = style.textStyles.filter(t => t.id !== textStyleId);
        this.notify();
    },

    renameTemplateStyle(styleId, newName) {
        const style = this.templateStyles.find(s => s.id === styleId);
        if (!style) return;
        style.name = newName;
        this.notify();
    },

    // Library operations
    addLibrary(library) {
        this.libraries.push({
            id: 'lib_' + Date.now().toString(36),
            name: library.name,
            description: library.description || '',
            addedAt: new Date().toISOString(),
            lastUpdated: library.lastUpdated || new Date().toISOString(),
            hasUpdates: false,
            componentCount: library.componentCount || 0,
            styleCount: library.styleCount || 0,
            variableCount: library.variableCount || 0,
            enabled: true
        });
        this.notify();
    },

    removeLibrary(libraryId) {
        this.libraries = this.libraries.filter(l => l.id !== libraryId);
        this.notify();
    },

    toggleLibrary(libraryId) {
        const lib = this.libraries.find(l => l.id === libraryId);
        if (!lib) return;
        lib.enabled = !lib.enabled;
        this.notify();
    },

    updateLibrary(libraryId) {
        const lib = this.libraries.find(l => l.id === libraryId);
        if (!lib) return;
        lib.hasUpdates = false;
        lib.lastUpdated = new Date().toISOString();
        this.notify();
    },

    // Deck settings operations
    updateDeckName(name) {
        this.deckSettings.name = name;
        this.notify();
    },

    updateDeckAspectRatio(ratio) {
        this.deckSettings.aspectRatio = ratio;
        if (ratio === '16:9') {
            this.deckSettings.width = 1200;
            this.deckSettings.height = 675;
        } else if (ratio === '4:3') {
            this.deckSettings.width = 1024;
            this.deckSettings.height = 768;
        }
        this.notify();
    },

    updateDefaultTransition(transition) {
        this.deckSettings.defaultTransition = transition;
        this.notify();
    },

    updateShareSettings(settings) {
        Object.assign(this.deckSettings.shareSettings, settings);
        this.notify();
    },

    toggleAvailableOffline() {
        this.deckSettings.availableOffline = !this.deckSettings.availableOffline;
        this.notify();
    },

    updateDefaultTemplateStyle(styleId) {
        this.deckSettings.defaultTemplateStyle = styleId;
        this.notify();
    },

    // Collaborator operations
    updateCollaboratorRole(userId, role) {
        const collab = this.collaborators.find(c => c.id === userId);
        if (!collab) return;
        collab.role = role;
        this.notify();
    },

    removeCollaborator(userId) {
        this.collaborators = this.collaborators.filter(c => c.id !== userId);
        this.notify();
    },

    // Export operations
    addExport(exportData) {
        this.exportHistory.push({
            id: 'exp_' + Date.now().toString(36),
            format: exportData.format,
            fileName: exportData.fileName,
            exportedAt: new Date().toISOString(),
            exportedBy: this.currentUser.id,
            fileSize: exportData.fileSize || '0 KB',
            colorProfile: exportData.colorProfile || 'srgb',
            quality: exportData.quality || 'high',
            slidesIncluded: exportData.slidesIncluded || 'all'
        });
        this.notify();
    },

    // Live interaction operations
    addPollVote(slideId, objectId, optionId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'liveInteraction' || obj.interactionType !== 'poll') return;
        const option = obj.options.find(o => o.id === optionId);
        if (!option) return;
        option.votes++;
        this.notify();
    },

    togglePollResultsVisibility(slideId, objectId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'liveInteraction') return;
        obj.hideResults = !obj.hideResults;
        this.notify();
    },

    addAlignmentResponse(slideId, objectId, value) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'liveInteraction' || obj.interactionType !== 'alignment') return;
        const existing = obj.responses.findIndex(r => r.userId === this.currentUser.id);
        if (existing >= 0) {
            obj.responses[existing].value = value;
        } else {
            obj.responses.push({ userId: this.currentUser.id, value: value });
        }
        this.notify();
    },

    addStamp(slideId, objectId, stampType) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'liveInteraction' || obj.interactionType !== 'stamps') return;
        const existing = obj.stamps.findIndex(s => s.userId === this.currentUser.id);
        if (existing >= 0) {
            obj.stamps[existing].type = stampType;
        } else {
            obj.stamps.push({ userId: this.currentUser.id, type: stampType });
        }
        this.notify();
    },

    // Table operations
    updateTableCell(slideId, objectId, row, col, value) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'table') return;
        if (obj.cells[row] && obj.cells[row][col] !== undefined) {
            obj.cells[row][col] = value;
            this.notify();
        }
    },

    addTableRow(slideId, objectId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'table') return;
        const newRow = new Array(obj.columns).fill('');
        obj.cells.push(newRow);
        obj.rows++;
        this.notify();
    },

    addTableColumn(slideId, objectId) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'table') return;
        obj.cells.forEach(row => row.push(''));
        obj.columns++;
        this.notify();
    },

    deleteTableRow(slideId, objectId, rowIndex) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'table' || obj.rows <= 1) return;
        obj.cells.splice(rowIndex, 1);
        obj.rows--;
        this.notify();
    },

    deleteTableColumn(slideId, objectId, colIndex) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'table' || obj.columns <= 1) return;
        obj.cells.forEach(row => row.splice(colIndex, 1));
        obj.columns--;
        this.notify();
    },

    // Code block operations
    updateCodeBlock(slideId, objectId, updates) {
        const slide = this.slides.find(s => s.id === slideId);
        if (!slide) return;
        const obj = slide.objects.find(o => o.id === objectId);
        if (!obj || obj.type !== 'code') return;
        Object.assign(obj, updates);
        this.notify();
    },

    // UI state (these still call notify since they affect rendering)
    showToast(message, duration) {
        this.toastMessage = message;
        this._listeners.forEach(fn => fn());
        if (duration !== 0) {
            setTimeout(() => {
                this.toastMessage = null;
                this._listeners.forEach(fn => fn());
            }, duration || 3000);
        }
    },

    openModal(modalId, data) {
        this.activeModal = modalId;
        this.modalData = data || null;
        this._listeners.forEach(fn => fn());
    },

    closeModal() {
        this.activeModal = null;
        this.modalData = null;
        this._listeners.forEach(fn => fn());
    },

    setActivePanel(panel) {
        this.activePanel = panel;
        this._listeners.forEach(fn => fn());
    },

    toggleGridView() {
        this.gridView = !this.gridView;
        this._listeners.forEach(fn => fn());
    },

    toggleDesignMode() {
        this.designMode = !this.designMode;
        this._listeners.forEach(fn => fn());
    },

    togglePresenterNotes() {
        this.presenterNotesVisible = !this.presenterNotesVisible;
        this._listeners.forEach(fn => fn());
    },

    toggleSidebar() {
        this.sidebarCollapsed = !this.sidebarCollapsed;
        this._listeners.forEach(fn => fn());
    },

    setSearchQuery(query) {
        this.searchQuery = query;
        this._listeners.forEach(fn => fn());
    }
};
