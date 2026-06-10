/* ============================================================
   state.js — Centralized state management for Elation Clinical Records
   ============================================================ */

const AppState = {
    // ── Persistent State (synced to server) ──
    currentProvider: null,
    providers: [],
    patients: [],
    problems: [],
    vaccinations: [],
    vitals: [],
    visitNotes: [],
    carePlans: [],
    visitNoteCategories: [],
    visitNoteTemplates: [],
    appointmentTypes: [],
    documentTags: [],
    providerPreferences: null,

    // ID counters
    _nextProblemId: 100,
    _nextVaxId: 100,
    _nextVitalId: 100,
    _nextNoteId: 100,
    _nextCarePlanId: 100,
    _nextCategoryId: 100,
    _nextTemplateId: 100,

    // ── UI State (not persisted) ──
    currentSection: 'patients',
    selectedPatientId: null,
    patientTab: 'chart',
    activeModal: null,
    modalData: null,
    toastMessage: null,
    searchQuery: '',
    patientSearchQuery: '',
    noteSearchQuery: '',

    // ── Event subscription ──
    _listeners: [],

    subscribe(fn) {
        this._listeners.push(fn);
    },

    notify() {
        this._persist();
        this._pushStateToServer();
        this._listeners.forEach(fn => fn());
    },

    // ── Initialization ──
    init() {
        const persisted = this._loadPersistedData();
        if (persisted) {
            this.currentProvider = persisted.currentProvider;
            this.providers = persisted.providers;
            this.patients = persisted.patients;
            this.problems = persisted.problems;
            this.vaccinations = persisted.vaccinations;
            this.vitals = persisted.vitals;
            this.visitNotes = persisted.visitNotes;
            this.carePlans = persisted.carePlans;
            this.visitNoteCategories = persisted.visitNoteCategories;
            this.visitNoteTemplates = persisted.visitNoteTemplates;
            this.appointmentTypes = persisted.appointmentTypes;
            this.documentTags = persisted.documentTags;
            this.providerPreferences = persisted.providerPreferences;
            this._nextProblemId = persisted._nextProblemId || 100;
            this._nextVaxId = persisted._nextVaxId || 100;
            this._nextVitalId = persisted._nextVitalId || 100;
            this._nextNoteId = persisted._nextNoteId || 100;
            this._nextCarePlanId = persisted._nextCarePlanId || 100;
            this._nextCategoryId = persisted._nextCategoryId || 100;
            this._nextTemplateId = persisted._nextTemplateId || 100;
        } else {
            this._loadSeedData();
        }
    },

    _loadSeedData() {
        this.currentProvider = JSON.parse(JSON.stringify(CURRENT_PROVIDER));
        this.providers = JSON.parse(JSON.stringify(PROVIDERS));
        this.patients = JSON.parse(JSON.stringify(PATIENTS));
        this.problems = JSON.parse(JSON.stringify(PROBLEMS));
        this.vaccinations = JSON.parse(JSON.stringify(VACCINATIONS));
        this.vitals = JSON.parse(JSON.stringify(VITALS));
        this.visitNotes = JSON.parse(JSON.stringify(VISIT_NOTES));
        this.carePlans = JSON.parse(JSON.stringify(CARE_PLANS));
        this.visitNoteCategories = JSON.parse(JSON.stringify(VISIT_NOTE_CATEGORIES));
        this.visitNoteTemplates = JSON.parse(JSON.stringify(VISIT_NOTE_TEMPLATES));
        this.appointmentTypes = JSON.parse(JSON.stringify(APPOINTMENT_TYPES));
        this.documentTags = [...DOCUMENT_TAGS];
        this.providerPreferences = JSON.parse(JSON.stringify(PROVIDER_PREFERENCES));
        this._nextProblemId = 100;
        this._nextVaxId = 100;
        this._nextVitalId = 100;
        this._nextNoteId = 100;
        this._nextCarePlanId = 100;
        this._nextCategoryId = 100;
        this._nextTemplateId = 100;
    },

    resetToSeedData() {
        this._loadSeedData();
        this.currentSection = 'patients';
        this.selectedPatientId = null;
        this.patientTab = 'chart';
        this.activeModal = null;
        this.modalData = null;
        this.toastMessage = null;
        this.searchQuery = '';
        this.patientSearchQuery = '';
        this.noteSearchQuery = '';
        localStorage.removeItem('elationClinicalState');
        this.notify();
    },

    // ── Persistence ──
    _persist() {
        const data = {
            _seedVersion: SEED_DATA_VERSION,
            currentProvider: this.currentProvider,
            providers: this.providers,
            patients: this.patients,
            problems: this.problems,
            vaccinations: this.vaccinations,
            vitals: this.vitals,
            visitNotes: this.visitNotes,
            carePlans: this.carePlans,
            visitNoteCategories: this.visitNoteCategories,
            visitNoteTemplates: this.visitNoteTemplates,
            appointmentTypes: this.appointmentTypes,
            documentTags: this.documentTags,
            providerPreferences: this.providerPreferences,
            _nextProblemId: this._nextProblemId,
            _nextVaxId: this._nextVaxId,
            _nextVitalId: this._nextVitalId,
            _nextNoteId: this._nextNoteId,
            _nextCarePlanId: this._nextCarePlanId,
            _nextCategoryId: this._nextCategoryId,
            _nextTemplateId: this._nextTemplateId
        };
        localStorage.setItem('elationClinicalState', JSON.stringify(data));
    },

    _loadPersistedData() {
        const saved = localStorage.getItem('elationClinicalState');
        if (!saved) return null;
        try {
            const parsed = JSON.parse(saved);
            if (parsed._seedVersion !== SEED_DATA_VERSION) {
                localStorage.removeItem('elationClinicalState');
                return null;
            }
            return parsed;
        } catch (e) {
            localStorage.removeItem('elationClinicalState');
            return null;
        }
    },

    _pushStateToServer() {
        fetch('/api/state', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.getSerializableState())
        }).catch(() => {});
    },

    getSerializableState() {
        return {
            currentProvider: this.currentProvider,
            providers: this.providers,
            patients: this.patients,
            problems: this.problems,
            vaccinations: this.vaccinations,
            vitals: this.vitals,
            visitNotes: this.visitNotes,
            carePlans: this.carePlans,
            visitNoteCategories: this.visitNoteCategories,
            visitNoteTemplates: this.visitNoteTemplates,
            appointmentTypes: this.appointmentTypes,
            documentTags: this.documentTags,
            providerPreferences: this.providerPreferences,
            _nextProblemId: this._nextProblemId,
            _nextVaxId: this._nextVaxId,
            _nextVitalId: this._nextVitalId,
            _nextNoteId: this._nextNoteId,
            _nextCarePlanId: this._nextCarePlanId,
            _nextCategoryId: this._nextCategoryId,
            _nextTemplateId: this._nextTemplateId
        };
    },

    // ── Helpers ──
    getPatient(id) {
        return this.patients.find(p => p.id === id);
    },

    getProvider(id) {
        return this.providers.find(p => p.id === id);
    },

    getPatientProblems(patientId) {
        return this.problems
            .filter(p => p.patientId === patientId)
            .sort((a, b) => a.sortOrder - b.sortOrder);
    },

    getPatientVaccinations(patientId) {
        return this.vaccinations
            .filter(v => v.patientId === patientId)
            .sort((a, b) => new Date(b.givenOn) - new Date(a.givenOn));
    },

    getPatientVitals(patientId) {
        return this.vitals
            .filter(v => v.patientId === patientId)
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    getPatientNotes(patientId) {
        return this.visitNotes
            .filter(n => n.patientId === patientId)
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    getPatientCarePlans(patientId) {
        return this.carePlans
            .filter(cp => cp.patientId === patientId)
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    getCategoryName(catId) {
        const cat = this.visitNoteCategories.find(c => c.id === catId);
        return cat ? cat.name : 'Unknown';
    },

    getFormatName(formatId) {
        const fmt = VISIT_NOTE_FORMATS.find(f => f.id === formatId);
        return fmt ? fmt.name : 'Unknown';
    },

    getTemplateName(tmplId) {
        if (!tmplId) return 'None';
        const t = this.visitNoteTemplates.find(t => t.id === tmplId);
        return t ? t.name : 'Unknown';
    },

    // ── Problem Mutations ──
    addProblem(patientId, data) {
        const id = 'prob_' + String(this._nextProblemId++).padStart(3, '0');
        const existingProblems = this.getPatientProblems(patientId);
        const problem = {
            id,
            patientId,
            title: data.title,
            icd10: data.icd10 || '',
            icd9: data.icd9 || '',
            snomed: data.snomed || '',
            dxDate: data.dxDate || new Date().toISOString().split('T')[0],
            status: data.status || 'Active',
            synopsis: data.synopsis || '',
            resolvedDate: '',
            sortOrder: existingProblems.length
        };
        this.problems.push(problem);
        this.notify();
        return problem;
    },

    updateProblem(problemId, updates) {
        const prob = this.problems.find(p => p.id === problemId);
        if (prob) {
            Object.assign(prob, updates);
            if (updates.status === 'Resolved' && !prob.resolvedDate) {
                prob.resolvedDate = new Date().toISOString().split('T')[0];
            }
            this.notify();
        }
    },

    changeProblemStatus(problemId, newStatus) {
        const prob = this.problems.find(p => p.id === problemId);
        if (prob) {
            prob.status = newStatus;
            if (newStatus === 'Resolved' && !prob.resolvedDate) {
                prob.resolvedDate = new Date().toISOString().split('T')[0];
            }
            if (newStatus !== 'Resolved') {
                prob.resolvedDate = '';
            }
            this.notify();
        }
    },

    reorderProblems(patientId, orderedIds) {
        orderedIds.forEach((id, idx) => {
            const prob = this.problems.find(p => p.id === id);
            if (prob) prob.sortOrder = idx;
        });
        this.notify();
    },

    // ── Vaccination Mutations ──
    addVaccination(patientId, data) {
        const id = 'vax_' + String(this._nextVaxId++).padStart(3, '0');
        const vax = {
            id,
            patientId,
            vaccineName: data.vaccineName,
            cvx: data.cvx || '',
            ndc: data.ndc || '',
            manufacturer: data.manufacturer || '',
            lotNumber: data.lotNumber || '',
            expirationDate: data.expirationDate || '',
            doseAmount: data.doseAmount || '',
            doseUnits: data.doseUnits || '',
            seriesNumber: data.seriesNumber || '',
            method: data.method || '',
            site: data.site || '',
            givenOn: data.givenOn || new Date().toISOString(),
            orderedBy: data.orderedBy || this.currentProvider.id,
            givenBy: data.givenBy || this.currentProvider.id,
            recordType: data.recordType || 'New',
            visDate: data.visDate || '',
            recall: data.recall || '',
            reason: data.reason || '',
            notes: data.notes || '',
            program: data.program || 'Not VFC Eligible',
            fundedBy: data.fundedBy || 'Private',
            source: data.source || 'New Immunization',
            status: data.recordType === 'Declined' ? 'declined' : 'completed',
            isInjectable: data.isInjectable || false,
            notSendToRegistry: data.notSendToRegistry || false
        };
        this.vaccinations.push(vax);
        this.notify();
        return vax;
    },

    // ── Vitals Mutations ──
    addVitals(patientId, noteId, data) {
        const id = 'vit_' + String(this._nextVitalId++).padStart(3, '0');
        const vital = {
            id,
            patientId,
            noteId,
            date: data.date || new Date().toISOString(),
            bloodPressureSystolic: data.bloodPressureSystolic || null,
            bloodPressureDiastolic: data.bloodPressureDiastolic || null,
            heartRate: data.heartRate || null,
            respiratoryRate: data.respiratoryRate || null,
            temperature: data.temperature || null,
            temperatureUnit: data.temperatureUnit || 'F',
            oxygenSaturation: data.oxygenSaturation || null,
            weight: data.weight || null,
            weightUnit: data.weightUnit || 'lbs',
            height: data.height || null,
            heightUnit: data.heightUnit || 'in',
            bmi: data.bmi || null,
            painLevel: data.painLevel !== undefined ? data.painLevel : null
        };
        this.vitals.push(vital);
        this.notify();
        return vital;
    },

    // ── Visit Note Mutations ──
    addVisitNote(patientId, data) {
        const id = 'note_' + String(this._nextNoteId++).padStart(3, '0');
        const note = {
            id,
            patientId,
            providerId: data.providerId || this.currentProvider.id,
            format: data.format || this.currentProvider.defaultNoteFormat,
            category: data.category || this.currentProvider.defaultCategory,
            templateUsed: data.templateUsed || '',
            date: data.date || new Date().toISOString(),
            status: 'draft',
            signedAt: '',
            reason: data.reason || '',
            blocks: data.blocks || [],
            billingItems: data.billingItems || [],
            documentTags: data.documentTags || []
        };
        this.visitNotes.push(note);
        this.notify();
        return note;
    },

    updateVisitNote(noteId, updates) {
        const note = this.visitNotes.find(n => n.id === noteId);
        if (note) {
            Object.assign(note, updates);
            this.notify();
        }
    },

    signVisitNote(noteId) {
        const note = this.visitNotes.find(n => n.id === noteId);
        if (note) {
            note.status = 'signed';
            note.signedAt = new Date().toISOString();
            this.notify();
        }
    },

    addBlockToNote(noteId, block) {
        const note = this.visitNotes.find(n => n.id === noteId);
        if (note) {
            note.blocks.push(block);
            this.notify();
        }
    },

    updateNoteBlock(noteId, blockIndex, content) {
        const note = this.visitNotes.find(n => n.id === noteId);
        if (note && note.blocks[blockIndex]) {
            note.blocks[blockIndex].content = content;
            this.notify();
        }
    },

    removeBlockFromNote(noteId, blockIndex) {
        const note = this.visitNotes.find(n => n.id === noteId);
        if (note) {
            note.blocks.splice(blockIndex, 1);
            this.notify();
        }
    },

    addBillingItemToNote(noteId, item) {
        const note = this.visitNotes.find(n => n.id === noteId);
        if (note) {
            note.billingItems.push(item);
            this.notify();
        }
    },

    removeBillingItemFromNote(noteId, index) {
        const note = this.visitNotes.find(n => n.id === noteId);
        if (note) {
            note.billingItems.splice(index, 1);
            this.notify();
        }
    },

    // ── Care Plan Mutations ──
    addCarePlan(patientId, noteId, data) {
        const id = 'cp_' + String(this._nextCarePlanId++).padStart(3, '0');
        const cp = {
            id,
            patientId,
            noteId,
            providerId: data.providerId || this.currentProvider.id,
            date: data.date || new Date().toISOString(),
            content: data.content || '',
            diagnoses: data.diagnoses || [],
            status: 'active'
        };
        this.carePlans.push(cp);
        this.notify();
        return cp;
    },

    // ── Category Mutations ──
    addCategory(data) {
        const id = 'cat_' + String(this._nextCategoryId++).padStart(3, '0');
        const maxSort = Math.max(0, ...this.visitNoteCategories.map(c => c.sortOrder));
        const cat = {
            id,
            name: data.name,
            countForMIPS: data.countForMIPS || false,
            isDefault: false,
            sortOrder: maxSort + 1
        };
        this.visitNoteCategories.push(cat);
        this.notify();
        return cat;
    },

    updateCategory(catId, updates) {
        const cat = this.visitNoteCategories.find(c => c.id === catId);
        if (cat) {
            Object.assign(cat, updates);
            this.notify();
        }
    },

    removeCategory(catId) {
        this.visitNoteCategories = this.visitNoteCategories.filter(c => c.id !== catId);
        this.notify();
    },

    reorderCategories(orderedIds) {
        orderedIds.forEach((id, idx) => {
            const cat = this.visitNoteCategories.find(c => c.id === id);
            if (cat) {
                cat.sortOrder = idx;
                cat.isDefault = idx === 0;
            }
        });
        this.notify();
    },

    // ── Template Mutations ──
    addTemplate(data) {
        const id = 'tmpl_' + String(this._nextTemplateId++).padStart(3, '0');
        const tmpl = {
            id,
            name: data.name,
            createdBy: this.currentProvider.id,
            content: data.content || {},
            billingItems: data.billingItems || [],
            pos: data.pos || '',
            billingNotes: data.billingNotes || '',
            documentTags: data.documentTags || [],
            createdAt: new Date().toISOString()
        };
        this.visitNoteTemplates.push(tmpl);
        this.notify();
        return tmpl;
    },

    updateTemplate(tmplId, updates) {
        const tmpl = this.visitNoteTemplates.find(t => t.id === tmplId);
        if (tmpl) {
            Object.assign(tmpl, updates);
            this.notify();
        }
    },

    deleteTemplate(tmplId) {
        this.visitNoteTemplates = this.visitNoteTemplates.filter(t => t.id !== tmplId);
        this.notify();
    },

    duplicateTemplate(tmplId) {
        const orig = this.visitNoteTemplates.find(t => t.id === tmplId);
        if (orig) {
            const copy = JSON.parse(JSON.stringify(orig));
            copy.id = 'tmpl_' + String(this._nextTemplateId++).padStart(3, '0');
            copy.name = orig.name + ' (Copy)';
            copy.createdAt = new Date().toISOString();
            this.visitNoteTemplates.push(copy);
            this.notify();
            return copy;
        }
    },

    // ── Patient Tag Mutations ──
    addPatientTag(patientId, tag) {
        const patient = this.patients.find(p => p.id === patientId);
        if (patient && !patient.tags.includes(tag)) {
            patient.tags.push(tag);
            patient.tags.sort((a, b) => {
                const aStar = a.startsWith('*');
                const bStar = b.startsWith('*');
                if (aStar && !bStar) return -1;
                if (!aStar && bStar) return 1;
                return a.localeCompare(b);
            });
            this.notify();
        }
    },

    removePatientTag(patientId, tag) {
        const patient = this.patients.find(p => p.id === patientId);
        if (patient) {
            patient.tags = patient.tags.filter(t => t !== tag);
            this.notify();
        }
    },

    // ── Provider Preferences ──
    updatePreference(key, value) {
        if (this.providerPreferences) {
            this.providerPreferences[key] = value;
            this.notify();
        }
    },

    // ── Appointment Type Mutations ──
    updateAppointmentType(aptId, updates) {
        const apt = this.appointmentTypes.find(a => a.id === aptId);
        if (apt) {
            Object.assign(apt, updates);
            this.notify();
        }
    },

    // ── Toast ──
    showToast(message) {
        this.toastMessage = message;
        this._listeners.forEach(fn => fn());
        setTimeout(() => {
            this.toastMessage = null;
            this._listeners.forEach(fn => fn());
        }, 3000);
    }
};
