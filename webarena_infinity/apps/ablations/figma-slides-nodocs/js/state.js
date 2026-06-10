/* ============================================================
   state.js — Centralized state management for Figma Slides
   ============================================================ */

const AppState = {
    // ─── Persistent data (saved to localStorage + pushed to server) ───
    presentations: [],
    slides: [],
    templates: [],
    comments: [],
    users: [],
    currentUserId: 'user_001',
    _nextPresentationId: 19,
    _nextSlideId: 500,
    _nextElementId: 2000,
    _nextCommentId: 41,
    _nextReplyId: 25,
    _nextTemplateId: 13,
    _seedVersion: SEED_DATA_VERSION,

    // ─── UI state (not persisted) ───
    currentView: 'dashboard',       // dashboard, editor, presenter
    currentPresentationId: null,
    currentSlideIndex: 0,
    selectedElementId: null,
    selectedElementIds: [],
    searchQuery: '',
    filterTag: '',
    filterStatus: '',
    sortBy: 'updatedAt',
    sortOrder: 'desc',

    // Editor UI
    activeTool: 'select',           // select, text, rectangle, circle, line, arrow, image
    showGrid: false,
    showRulers: false,
    zoom: 100,
    showSpeakerNotes: true,
    propertiesPanelOpen: true,
    showComments: false,

    // Presenter
    presenterSlideIndex: 0,
    presenterTimerStart: null,

    // Modal
    activeModal: null,

    // Clipboard
    clipboard: null,

    // ─── Listeners ───
    _listeners: [],

    // ═══════════════════════════════════════════════════════════
    // Initialization
    // ═══════════════════════════════════════════════════════════
    init() {
        const persisted = this._loadPersistedData();
        if (persisted) {
            this._applyPersisted(persisted);
        } else {
            this._loadSeedData();
        }
        this._pushStateToServer();
    },

    _loadSeedData() {
        const seed = getSeedData();
        this.presentations = seed.presentations;
        this.slides = seed.slides;
        this.templates = seed.templates;
        this.comments = seed.comments;
        this.users = seed.users;
        this.currentUserId = seed.currentUserId;
        this._nextPresentationId = seed._nextPresentationId;
        this._nextSlideId = seed._nextSlideId;
        this._nextElementId = seed._nextElementId;
        this._nextCommentId = seed._nextCommentId;
        this._nextReplyId = seed._nextReplyId;
        this._nextTemplateId = seed._nextTemplateId;
        this._seedVersion = seed._seedVersion;
    },

    _loadPersistedData() {
        try {
            const saved = localStorage.getItem('figmaSlidesState');
            if (!saved) return null;
            const parsed = JSON.parse(saved);
            if (parsed._seedVersion !== SEED_DATA_VERSION) {
                localStorage.removeItem('figmaSlidesState');
                return null;
            }
            return parsed;
        } catch (e) {
            localStorage.removeItem('figmaSlidesState');
            return null;
        }
    },

    _applyPersisted(data) {
        this.presentations = data.presentations || [];
        this.slides = data.slides || [];
        this.templates = data.templates || [];
        this.comments = data.comments || [];
        this.users = data.users || [];
        this.currentUserId = data.currentUserId || 'user_001';
        this._nextPresentationId = data._nextPresentationId || 19;
        this._nextSlideId = data._nextSlideId || 500;
        this._nextElementId = data._nextElementId || 2000;
        this._nextCommentId = data._nextCommentId || 41;
        this._nextReplyId = data._nextReplyId || 25;
        this._nextTemplateId = data._nextTemplateId || 13;
        this._seedVersion = data._seedVersion || SEED_DATA_VERSION;
    },

    resetToSeedData() {
        localStorage.removeItem('figmaSlidesState');
        this._loadSeedData();
        this.currentView = 'dashboard';
        this.currentPresentationId = null;
        this.currentSlideIndex = 0;
        this.selectedElementId = null;
        this.selectedElementIds = [];
        this.searchQuery = '';
        this.filterTag = '';
        this.filterStatus = '';
        this.activeModal = null;
        this._pushStateToServer();
        this._notifyListeners();
    },

    // ═══════════════════════════════════════════════════════════
    // Persistence & sync
    // ═══════════════════════════════════════════════════════════
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
            presentations: this.presentations,
            slides: this.slides,
            templates: this.templates,
            comments: this.comments,
            users: this.users,
            currentUserId: this.currentUserId,
            _nextPresentationId: this._nextPresentationId,
            _nextSlideId: this._nextSlideId,
            _nextElementId: this._nextElementId,
            _nextCommentId: this._nextCommentId,
            _nextReplyId: this._nextReplyId,
            _nextTemplateId: this._nextTemplateId,
            _seedVersion: this._seedVersion
        };
    },

    notify() {
        this._persist();
        this._pushStateToServer();
        this._notifyListeners();
    },

    subscribe(fn) {
        this._listeners.push(fn);
    },

    _notifyListeners() {
        this._listeners.forEach(fn => fn());
    },

    // ═══════════════════════════════════════════════════════════
    // Query helpers
    // ═══════════════════════════════════════════════════════════
    getUserById(id) {
        return this.users.find(u => u.id === id);
    },

    getCurrentUser() {
        return this.getUserById(this.currentUserId);
    },

    getPresentationById(id) {
        return this.presentations.find(p => p.id === id);
    },

    getSlidesForPresentation(presId) {
        return this.slides.filter(s => s.presentationId === presId).sort((a, b) => a.order - b.order);
    },

    getSlideById(id) {
        return this.slides.find(s => s.id === id);
    },

    getCurrentSlide() {
        if (!this.currentPresentationId) return null;
        const slides = this.getSlidesForPresentation(this.currentPresentationId);
        return slides[this.currentSlideIndex] || slides[0] || null;
    },

    getCommentsForSlide(slideId) {
        return this.comments.filter(c => c.slideId === slideId);
    },

    getCommentsForPresentation(presId) {
        return this.comments.filter(c => c.presentationId === presId);
    },

    getTemplateById(id) {
        return this.templates.find(t => t.id === id);
    },

    getTemplatesByCategory(cat) {
        if (!cat || cat === 'all') return this.templates;
        return this.templates.filter(t => t.category === cat);
    },

    getAllTags() {
        const tagSet = new Set();
        this.presentations.forEach(p => (p.tags || []).forEach(t => tagSet.add(t)));
        return Array.from(tagSet).sort();
    },

    // ═══════════════════════════════════════════════════════════
    // Filtered/sorted presentation list
    // ═══════════════════════════════════════════════════════════
    getFilteredPresentations() {
        let list = [...this.presentations];

        if (this.searchQuery) {
            const q = this.searchQuery.toLowerCase();
            list = list.filter(p =>
                p.title.toLowerCase().includes(q) ||
                p.description.toLowerCase().includes(q) ||
                (p.tags || []).some(t => t.toLowerCase().includes(q))
            );
        }

        if (this.filterTag) {
            list = list.filter(p => (p.tags || []).includes(this.filterTag));
        }

        if (this.filterStatus) {
            list = list.filter(p => p.status === this.filterStatus);
        }

        const dir = this.sortOrder === 'asc' ? 1 : -1;
        list.sort((a, b) => {
            if (this.sortBy === 'title') return dir * a.title.localeCompare(b.title);
            if (this.sortBy === 'createdAt') return dir * (new Date(a.createdAt) - new Date(b.createdAt));
            return dir * (new Date(a.updatedAt) - new Date(b.updatedAt));
        });

        return list;
    },

    // ═══════════════════════════════════════════════════════════
    // Presentation mutations
    // ═══════════════════════════════════════════════════════════
    createPresentation(data) {
        const id = 'pres_' + String(this._nextPresentationId++).padStart(3, '0');
        const now = new Date().toISOString();
        const pres = {
            id,
            title: data.title || 'Untitled Presentation',
            description: data.description || '',
            createdAt: now,
            updatedAt: now,
            createdBy: this.currentUserId,
            theme: data.theme || 'minimal',
            tags: data.tags || [],
            starred: false,
            status: 'draft',
            slideCount: 1,
            shareSettings: {
                visibility: 'private',
                allowComments: true,
                allowEditing: false,
                shareLink: '',
                embedLink: '',
                sharedWith: [this.currentUserId]
            }
        };
        this.presentations.push(pres);

        // Create first slide
        const slideId = 'slide_' + String(this._nextSlideId++).padStart(5, '0');
        this.slides.push({
            id: slideId,
            presentationId: id,
            order: 0,
            layout: 'title',
            backgroundColor: '#ffffff',
            transition: { type: 'none', duration: 500 },
            speakerNotes: '',
            elements: [
                { id: 'elem_' + String(this._nextElementId++).padStart(5, '0'), type: 'text', x: 80, y: 180, width: 800, height: 70, rotation: 0, opacity: 1, locked: false, content: data.title || 'Untitled Presentation', shapeType: null, fill: null, stroke: null, strokeWidth: 0, cornerRadius: 0, imageUrl: null, imagePlaceholder: null, style: { fontFamily: 'Inter', fontSize: 48, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -1, listType: 'none' }, animation: { type: 'none', duration: 300, delay: 0, order: 0 } }
            ]
        });

        this.notify();
        return id;
    },

    updatePresentation(id, updates) {
        const pres = this.getPresentationById(id);
        if (!pres) return;
        Object.assign(pres, updates, { updatedAt: new Date().toISOString() });
        this.notify();
    },

    deletePresentation(id) {
        this.presentations = this.presentations.filter(p => p.id !== id);
        this.slides = this.slides.filter(s => s.presentationId !== id);
        this.comments = this.comments.filter(c => c.presentationId !== id);
        this.notify();
    },

    duplicatePresentation(id) {
        const src = this.getPresentationById(id);
        if (!src) return null;
        const newId = 'pres_' + String(this._nextPresentationId++).padStart(3, '0');
        const now = new Date().toISOString();
        const copy = JSON.parse(JSON.stringify(src));
        copy.id = newId;
        copy.title = src.title + ' (Copy)';
        copy.createdAt = now;
        copy.updatedAt = now;
        copy.status = 'draft';
        copy.starred = false;
        this.presentations.push(copy);

        const srcSlides = this.getSlidesForPresentation(id);
        srcSlides.forEach(slide => {
            const newSlide = JSON.parse(JSON.stringify(slide));
            newSlide.id = 'slide_' + String(this._nextSlideId++).padStart(5, '0');
            newSlide.presentationId = newId;
            newSlide.elements = newSlide.elements.map(el => {
                el.id = 'elem_' + String(this._nextElementId++).padStart(5, '0');
                return el;
            });
            this.slides.push(newSlide);
        });

        this.notify();
        return newId;
    },

    toggleStar(id) {
        const pres = this.getPresentationById(id);
        if (pres) {
            pres.starred = !pres.starred;
            pres.updatedAt = new Date().toISOString();
            this.notify();
        }
    },

    updateShareSettings(presId, settings) {
        const pres = this.getPresentationById(presId);
        if (!pres) return;
        Object.assign(pres.shareSettings, settings);
        pres.updatedAt = new Date().toISOString();
        this.notify();
    },

    // ═══════════════════════════════════════════════════════════
    // Slide mutations
    // ═══════════════════════════════════════════════════════════
    addSlide(presId, afterIndex, templateId) {
        const slides = this.getSlidesForPresentation(presId);
        const insertOrder = (afterIndex !== undefined && afterIndex !== null) ? afterIndex + 1 : slides.length;

        // Shift existing slides
        slides.forEach(s => { if (s.order >= insertOrder) s.order++; });

        const slideId = 'slide_' + String(this._nextSlideId++).padStart(5, '0');
        let elements = [];
        let layout = 'blank';
        let bg = '#ffffff';

        if (templateId) {
            const tmpl = this.getTemplateById(templateId);
            if (tmpl) {
                layout = tmpl.layout;
                if (tmpl.layout === 'title' || tmpl.layout === 'section-header') bg = '#1a1a2e';
                elements = (tmpl.elements || []).map(te => {
                    const el = JSON.parse(JSON.stringify(te));
                    el.id = 'elem_' + String(this._nextElementId++).padStart(5, '0');
                    el.rotation = el.rotation || 0;
                    el.opacity = el.opacity !== undefined ? el.opacity : 1;
                    el.locked = el.locked || false;
                    el.animation = el.animation || { type: 'none', duration: 300, delay: 0, order: 0 };
                    if (!el.shapeType) el.shapeType = null;
                    if (!el.fill) el.fill = null;
                    if (el.stroke === undefined) el.stroke = null;
                    if (!el.strokeWidth) el.strokeWidth = 0;
                    if (!el.cornerRadius) el.cornerRadius = 0;
                    if (!el.imageUrl) el.imageUrl = null;
                    if (!el.imagePlaceholder) el.imagePlaceholder = null;
                    if (!el.content) el.content = null;
                    if (!el.style) el.style = null;
                    return el;
                });
            }
        }

        this.slides.push({
            id: slideId,
            presentationId: presId,
            order: insertOrder,
            layout: layout,
            backgroundColor: bg,
            transition: { type: 'none', duration: 500 },
            speakerNotes: '',
            elements: elements
        });

        // Update presentation slide count
        const pres = this.getPresentationById(presId);
        if (pres) {
            pres.slideCount = this.getSlidesForPresentation(presId).length;
            pres.updatedAt = new Date().toISOString();
        }

        this.notify();
        return slideId;
    },

    deleteSlide(slideId) {
        const slide = this.getSlideById(slideId);
        if (!slide) return;
        const presId = slide.presentationId;
        const order = slide.order;

        this.slides = this.slides.filter(s => s.id !== slideId);
        this.comments = this.comments.filter(c => c.slideId !== slideId);

        // Re-order
        this.getSlidesForPresentation(presId).forEach(s => {
            if (s.order > order) s.order--;
        });

        const pres = this.getPresentationById(presId);
        if (pres) {
            pres.slideCount = this.getSlidesForPresentation(presId).length;
            pres.updatedAt = new Date().toISOString();
        }

        this.notify();
    },

    duplicateSlide(slideId) {
        const slide = this.getSlideById(slideId);
        if (!slide) return null;
        const presId = slide.presentationId;
        const slides = this.getSlidesForPresentation(presId);

        // Shift slides after current
        slides.forEach(s => { if (s.order > slide.order) s.order++; });

        const newSlide = JSON.parse(JSON.stringify(slide));
        newSlide.id = 'slide_' + String(this._nextSlideId++).padStart(5, '0');
        newSlide.order = slide.order + 1;
        newSlide.elements = newSlide.elements.map(el => {
            el.id = 'elem_' + String(this._nextElementId++).padStart(5, '0');
            return el;
        });
        this.slides.push(newSlide);

        const pres = this.getPresentationById(presId);
        if (pres) {
            pres.slideCount = this.getSlidesForPresentation(presId).length;
            pres.updatedAt = new Date().toISOString();
        }

        this.notify();
        return newSlide.id;
    },

    moveSlide(slideId, newOrder) {
        const slide = this.getSlideById(slideId);
        if (!slide) return;
        const presId = slide.presentationId;
        const oldOrder = slide.order;
        if (oldOrder === newOrder) return;

        const slides = this.getSlidesForPresentation(presId);
        if (newOrder > oldOrder) {
            slides.forEach(s => { if (s.order > oldOrder && s.order <= newOrder) s.order--; });
        } else {
            slides.forEach(s => { if (s.order >= newOrder && s.order < oldOrder) s.order++; });
        }
        slide.order = newOrder;

        const pres = this.getPresentationById(presId);
        if (pres) pres.updatedAt = new Date().toISOString();

        this.notify();
    },

    updateSlide(slideId, updates) {
        const slide = this.getSlideById(slideId);
        if (!slide) return;
        if (updates.backgroundColor !== undefined) slide.backgroundColor = updates.backgroundColor;
        if (updates.transition !== undefined) slide.transition = updates.transition;
        if (updates.speakerNotes !== undefined) slide.speakerNotes = updates.speakerNotes;
        if (updates.layout !== undefined) slide.layout = updates.layout;

        const pres = this.getPresentationById(slide.presentationId);
        if (pres) pres.updatedAt = new Date().toISOString();

        this.notify();
    },

    applyTemplateToSlide(slideId, templateId) {
        const slide = this.getSlideById(slideId);
        const tmpl = this.getTemplateById(templateId);
        if (!slide || !tmpl) return;

        slide.layout = tmpl.layout;
        slide.elements = (tmpl.elements || []).map(te => {
            const el = JSON.parse(JSON.stringify(te));
            el.id = 'elem_' + String(this._nextElementId++).padStart(5, '0');
            el.rotation = el.rotation || 0;
            el.opacity = el.opacity !== undefined ? el.opacity : 1;
            el.locked = el.locked || false;
            el.animation = el.animation || { type: 'none', duration: 300, delay: 0, order: 0 };
            if (!el.shapeType) el.shapeType = null;
            if (!el.fill) el.fill = null;
            if (el.stroke === undefined) el.stroke = null;
            if (!el.strokeWidth) el.strokeWidth = 0;
            if (!el.cornerRadius) el.cornerRadius = 0;
            if (!el.imageUrl) el.imageUrl = null;
            if (!el.imagePlaceholder) el.imagePlaceholder = null;
            if (!el.content) el.content = null;
            if (!el.style) el.style = null;
            return el;
        });

        const pres = this.getPresentationById(slide.presentationId);
        if (pres) pres.updatedAt = new Date().toISOString();

        this.notify();
    },

    // ═══════════════════════════════════════════════════════════
    // Element mutations
    // ═══════════════════════════════════════════════════════════
    addElement(slideId, elementData) {
        const slide = this.getSlideById(slideId);
        if (!slide) return null;
        const id = 'elem_' + String(this._nextElementId++).padStart(5, '0');
        const el = Object.assign({
            id, type: 'text', x: 100, y: 100, width: 200, height: 60,
            rotation: 0, opacity: 1, locked: false,
            content: null, shapeType: null, fill: null, stroke: null, strokeWidth: 0, cornerRadius: 0,
            imageUrl: null, imagePlaceholder: null, style: null,
            animation: { type: 'none', duration: 300, delay: 0, order: 0 }
        }, elementData, { id });

        if (el.type === 'text' && !el.style) {
            el.style = { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#2c2c2c', textAlign: 'left', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' };
            el.content = el.content || 'Text';
        }
        if (el.type === 'shape') {
            el.shapeType = el.shapeType || 'rectangle';
            el.fill = el.fill || '#4A90D9';
            el.stroke = el.stroke || '#333333';
            el.strokeWidth = el.strokeWidth || 2;
        }
        if (el.type === 'image') {
            el.imagePlaceholder = el.imagePlaceholder || '#e0e0e0';
        }

        slide.elements.push(el);

        const pres = this.getPresentationById(slide.presentationId);
        if (pres) pres.updatedAt = new Date().toISOString();

        this.notify();
        return id;
    },

    updateElement(slideId, elementId, updates) {
        const slide = this.getSlideById(slideId);
        if (!slide) return;
        const el = slide.elements.find(e => e.id === elementId);
        if (!el) return;

        Object.keys(updates).forEach(key => {
            if (key === 'style' && el.style) {
                Object.assign(el.style, updates.style);
            } else if (key === 'animation' && el.animation) {
                Object.assign(el.animation, updates.animation);
            } else {
                el[key] = updates[key];
            }
        });

        const pres = this.getPresentationById(slide.presentationId);
        if (pres) pres.updatedAt = new Date().toISOString();

        this.notify();
    },

    deleteElement(slideId, elementId) {
        const slide = this.getSlideById(slideId);
        if (!slide) return;
        slide.elements = slide.elements.filter(e => e.id !== elementId);

        const pres = this.getPresentationById(slide.presentationId);
        if (pres) pres.updatedAt = new Date().toISOString();

        this.notify();
    },

    moveElement(slideId, elementId, x, y) {
        const slide = this.getSlideById(slideId);
        if (!slide) return;
        const el = slide.elements.find(e => e.id === elementId);
        if (!el || el.locked) return;
        el.x = Math.round(x);
        el.y = Math.round(y);
        this.notify();
    },

    resizeElement(slideId, elementId, width, height) {
        const slide = this.getSlideById(slideId);
        if (!slide) return;
        const el = slide.elements.find(e => e.id === elementId);
        if (!el || el.locked) return;
        el.width = Math.max(20, Math.round(width));
        el.height = Math.max(20, Math.round(height));
        this.notify();
    },

    // ═══════════════════════════════════════════════════════════
    // Comment mutations
    // ═══════════════════════════════════════════════════════════
    addComment(presId, slideId, content, elementId) {
        const id = 'cmt_' + String(this._nextCommentId++).padStart(3, '0');
        this.comments.push({
            id,
            presentationId: presId,
            slideId: slideId,
            elementId: elementId || null,
            authorId: this.currentUserId,
            content: content,
            createdAt: new Date().toISOString(),
            resolved: false,
            replies: []
        });
        this.notify();
        return id;
    },

    addReply(commentId, content) {
        const comment = this.comments.find(c => c.id === commentId);
        if (!comment) return;
        const id = 'reply_' + String(this._nextReplyId++).padStart(3, '0');
        comment.replies.push({
            id,
            authorId: this.currentUserId,
            content: content,
            createdAt: new Date().toISOString()
        });
        this.notify();
        return id;
    },

    toggleResolveComment(commentId) {
        const comment = this.comments.find(c => c.id === commentId);
        if (!comment) return;
        comment.resolved = !comment.resolved;
        this.notify();
    },

    deleteComment(commentId) {
        this.comments = this.comments.filter(c => c.id !== commentId);
        this.notify();
    },

    // ═══════════════════════════════════════════════════════════
    // Template mutations
    // ═══════════════════════════════════════════════════════════
    saveAsTemplate(slideId, name, category) {
        const slide = this.getSlideById(slideId);
        if (!slide) return null;
        const id = 'tmpl_' + String(this._nextTemplateId++).padStart(3, '0');
        const tmpl = {
            id,
            name: name || 'Custom Template',
            category: category || 'custom',
            layout: slide.layout,
            description: 'Custom template saved from slide',
            previewColor: slide.backgroundColor !== '#ffffff' ? slide.backgroundColor : '#7B61FF',
            elements: JSON.parse(JSON.stringify(slide.elements)).map(el => {
                delete el.id;
                return el;
            })
        };
        this.templates.push(tmpl);
        this.notify();
        return id;
    }
};
