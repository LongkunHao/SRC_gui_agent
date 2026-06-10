const App = {
    _sseConnection: null,
    _openDropdownId: null,
    _medSearchTimeout: null,

    init() {
        AppState.subscribe(() => App.render());
        App._setupSSE();
        document.addEventListener('click', (e) => App.handleClick(e));
        document.addEventListener('input', (e) => App.handleInput(e));
        document.addEventListener('change', (e) => App.handleChange(e));
        document.addEventListener('keydown', (e) => App.handleKeydown(e));
        window.addEventListener('hashchange', () => {
            App.parseRoute();
            App.render();
        });
        AppState.init();
        App.parseRoute();
        App.render();
    },

    _setupSSE() {
        const eventSource = new EventSource('/api/events');
        App._sseConnection = eventSource;
        eventSource.onmessage = (e) => {
            if (e.data === 'reset') {
                AppState.resetToSeedData();
                window.location.hash = '#/chart';
            }
        };
    },

    parseRoute() {
        const hash = window.location.hash || '#/chart';
        const parts = hash.replace('#/', '').split('/');
        const view = parts[0] || 'chart';
        const validViews = ['chart', 'med-history', 'rx-requests', 'settings'];
        AppState.currentView = validViews.includes(view) ? view : 'chart';
        if (view === 'settings' && parts[1]) {
            AppState.settingsTab = parts[1];
        }
    },

    navigate(route) {
        window.location.hash = '#/' + route;
    },

    render() {
        // Top bar
        const topBar = document.getElementById('topBar');
        if (topBar) topBar.innerHTML = Views.renderTopBar();

        // Nav bar
        const navBar = document.getElementById('navBar');
        if (navBar) navBar.innerHTML = Views.renderNavBar();

        // Main content
        const mainContent = document.getElementById('mainContent');
        if (mainContent) {
            switch (AppState.currentView) {
                case 'chart':
                    mainContent.innerHTML = Views.renderChartView();
                    break;
                case 'med-history':
                    mainContent.innerHTML = Views.renderMedHistoryView();
                    break;
                case 'rx-requests':
                    mainContent.innerHTML = Views.renderRxRequestsView();
                    break;
                case 'settings':
                    mainContent.innerHTML = Views.renderSettingsView();
                    break;
                default:
                    mainContent.innerHTML = Views.renderChartView();
            }
        }

        // Modals
        const modalContainer = document.getElementById('modalContainer');
        if (modalContainer) {
            let modalHtml = '';
            if (AppState.prescribeFormOpen) {
                modalHtml += Views.renderPrescribeForm();
            }
            if (AppState.documentMedFormOpen) {
                modalHtml += Views.renderDocumentMedForm();
            }
            if (AppState.discontinueModalOpen && AppState.discontinueTarget) {
                modalHtml += Views.renderDiscontinueModal();
            }
            if (AppState.reconcileOpen) {
                modalHtml += Views.renderReconcileModal();
            }
            if (AppState.bulkRefillOpen) {
                modalHtml += Views.renderBulkRefillModal();
            }
            if (AppState.selectedMedId) {
                const med = AppState.getMedById(AppState.selectedMedId);
                if (med) modalHtml += Views.renderMedDetailModal(med);
            }
            modalContainer.innerHTML = modalHtml;
        }
    },

    handleClick(e) {
        const target = e.target;

        // Close open dropdowns when clicking outside
        if (App._openDropdownId) {
            const ddMenu = document.getElementById(App._openDropdownId + '-menu');
            if (ddMenu && !ddMenu.contains(target) && !target.closest(`[data-dropdown="${App._openDropdownId}"]`)) {
                ddMenu.classList.remove('open');
                App._openDropdownId = null;
            }
        }

        // Close search results
        if (!target.closest('.med-search-wrapper') && !target.closest('.med-search-results')) {
            const sr = document.getElementById('medSearchResults');
            if (sr) sr.style.display = 'none';
        }
        if (!target.closest('.pharmacy-search-results') && !target.closest('#rxPharmacySearch')) {
            const pr = document.getElementById('pharmacySearchResults');
            if (pr) pr.style.display = 'none';
        }
        if (!target.closest('.diagnosis-search-results') && !target.closest('#rxDiagnosis')) {
            const dr = document.getElementById('diagnosisSearchResults');
            if (dr) dr.style.display = 'none';
        }
        if (!target.closest('#docMedSearchResults') && !target.closest('#docMedSearch')) {
            const dr = document.getElementById('docMedSearchResults');
            if (dr) dr.style.display = 'none';
        }

        // Route navigation
        const routeEl = target.closest('[data-route]');
        if (routeEl) {
            e.preventDefault();
            App.navigate(routeEl.dataset.route);
            return;
        }

        // Dropdown toggle
        const dropdownEl = target.closest('[data-dropdown]');
        if (dropdownEl) {
            e.preventDefault();
            App.toggleDropdown(dropdownEl.dataset.dropdown);
            return;
        }

        // Dropdown item select
        const ddItem = target.closest('.dropdown-item[data-value][data-dropdown-id]');
        if (ddItem) {
            e.preventDefault();
            App.handleDropdownSelect(ddItem.dataset.dropdownId, ddItem.dataset.value);
            return;
        }

        // Med search result click
        const medResult = target.closest('.med-search-item');
        if (medResult) {
            e.preventDefault();
            App.handleMedSearchSelect(medResult);
            return;
        }

        // Pharmacy search result click
        const pharmResult = target.closest('.pharmacy-search-item');
        if (pharmResult) {
            e.preventDefault();
            App.handlePharmacySearchSelect(pharmResult);
            return;
        }

        // Diagnosis search result click
        const dxResult = target.closest('.diagnosis-search-item');
        if (dxResult) {
            e.preventDefault();
            App.handleDiagnosisSearchSelect(dxResult);
            return;
        }

        // Doc med search result click
        const docMedResult = target.closest('.doc-med-search-item');
        if (docMedResult) {
            e.preventDefault();
            App.handleDocMedSearchSelect(docMedResult);
            return;
        }

        // Actions
        const actionEl = target.closest('[data-action]');
        if (actionEl) {
            e.preventDefault();
            App.handleAction(actionEl.dataset.action, actionEl);
            return;
        }

        // Bulk refill checkbox
        const bulkCheck = target.closest('.bulk-refill-check');
        if (bulkCheck) {
            const medId = bulkCheck.dataset.medId;
            if (bulkCheck.checked) {
                AppState.selectedRefillIds.add(medId);
            } else {
                AppState.selectedRefillIds.delete(medId);
            }
            return;
        }

        // Bulk select all
        if (target.id === 'bulkSelectAll') {
            const rxMeds = AppState.permanentRxMeds.filter(m => m.status === 'active');
            if (target.checked) {
                for (const med of rxMeds) AppState.selectedRefillIds.add(med.id);
            } else {
                AppState.selectedRefillIds.clear();
            }
            App.render();
            return;
        }
    },

    handleAction(action, el) {
        switch (action) {
            case 'open-prescribe': {
                AppState.prescribeFormOpen = true;
                AppState.prescribeFormData = {
                    medicationName: '',
                    sig: '',
                    qty: '',
                    unit: 'tablets',
                    refills: '',
                    daysSupply: 30,
                    classification: 'permanent_rx',
                    dispenseAsWritten: false,
                    diagnosis: [],
                    diagnosisSearch: '',
                    pharmacyId: AppState.settings.defaultPharmacyId || '',
                    pharmacyName: '',
                    pharmacyEpcs: false,
                    pharmacySearch: '',
                    instructionsToPharmacy: '',
                    doNotFillBefore: '',
                    isControlled: false,
                    scheduleClass: null,
                    ndc: null
                };
                // Pre-populate pharmacy
                if (AppState.settings.defaultPharmacyId) {
                    const p = AppState.getPharmacyById(AppState.settings.defaultPharmacyId);
                    if (p) {
                        AppState.prescribeFormData.pharmacyName = p.name;
                        AppState.prescribeFormData.pharmacyEpcs = p.epcs;
                        AppState.prescribeFormData.pharmacySearch = p.name;
                    }
                }
                App.render();
                break;
            }
            case 'close-prescribe':
            case 'discard-prescribe': {
                AppState.prescribeFormOpen = false;
                AppState.prescribeFormData = null;
                App.render();
                break;
            }
            case 'submit-prescribe': {
                const fd = AppState.prescribeFormData;
                if (!fd || !fd.medicationName || !fd.sig || !fd.qty) {
                    Components.showToast('Please fill in all required fields');
                    return;
                }
                AppState.addPrescription(fd);
                AppState.prescribeFormOpen = false;
                AppState.prescribeFormData = null;
                Components.showToast('Prescription sent successfully');
                App.render();
                break;
            }
            case 'save-as-template': {
                const fd = AppState.prescribeFormData;
                if (!fd || !fd.medicationName) return;
                AppState.addRxTemplate({
                    medicationName: fd.medicationName,
                    sig: fd.sig || '',
                    qty: fd.qty || 30,
                    unit: fd.unit || 'tablets',
                    refills: fd.refills || 0,
                    daysSupply: fd.daysSupply || 30,
                    ndc: fd.ndc
                });
                Components.showToast('Rx template saved');
                break;
            }
            case 'open-document-med': {
                AppState.documentMedFormOpen = true;
                App.render();
                break;
            }
            case 'close-document-med': {
                AppState.documentMedFormOpen = false;
                App.render();
                break;
            }
            case 'submit-document-med': {
                const medName = document.getElementById('docMedSearch');
                const medType = document.querySelector('input[name="docMedType"]:checked');
                const startDate = document.getElementById('docMedStartDate');
                const sig = document.getElementById('docMedSig');
                if (!medName || !medName.value) {
                    Components.showToast('Please select a medication');
                    return;
                }
                AppState.documentMedication({
                    medicationName: medName.value,
                    type: medType ? medType.value : 'rx',
                    startDate: startDate ? startDate.value : '',
                    sig: sig ? sig.value : ''
                });
                AppState.documentMedFormOpen = false;
                Components.showToast('Medication documented');
                App.render();
                break;
            }
            case 'discontinue-med': {
                const medId = el.dataset.medId;
                const med = AppState.getMedById(medId);
                if (med) {
                    AppState.discontinueTarget = med;
                    AppState.discontinueModalOpen = true;
                    App.render();
                }
                break;
            }
            case 'close-discontinue': {
                AppState.discontinueModalOpen = false;
                AppState.discontinueTarget = null;
                App.render();
                break;
            }
            case 'submit-discontinue': {
                const med = AppState.discontinueTarget;
                if (!med) return;
                // Get reason from dropdown
                const reasonMenu = document.getElementById('discReason-menu');
                const selectedReason = reasonMenu ? reasonMenu.querySelector('.dropdown-item.selected') : null;
                const reason = selectedReason ? selectedReason.dataset.value : '';
                if (!reason) {
                    Components.showToast('Please select a reason');
                    return;
                }
                const byEl = document.getElementById('discBy');
                const detailsEl = document.getElementById('discDetails');
                const cancelEl = document.getElementById('discSendCancel');
                AppState.discontinueMed(
                    med.id,
                    reason,
                    detailsEl ? detailsEl.value : '',
                    byEl ? byEl.value : AppState.currentUser.name,
                    cancelEl ? cancelEl.checked : false
                );
                AppState.discontinueModalOpen = false;
                AppState.discontinueTarget = null;
                Components.showToast(`${med.medicationName} discontinued`);
                App.render();
                break;
            }
            case 'refill-med': {
                const medId = el.dataset.medId;
                const med = AppState.getMedById(medId);
                if (med) {
                    AppState.prescribeFormOpen = true;
                    AppState.prescribeFormData = {
                        medicationName: med.medicationName,
                        ndc: med.ndc,
                        sig: med.sig,
                        qty: med.qty,
                        unit: med.unit,
                        refills: med.refills,
                        daysSupply: med.daysSupply,
                        classification: med.classification === 'temporary' ? 'temporary' : 'permanent_rx',
                        dispenseAsWritten: med.dispenseAsWritten,
                        diagnosis: med.diagnosis || [],
                        diagnosisSearch: '',
                        pharmacyId: med.pharmacyId || '',
                        pharmacyName: med.pharmacyName || '',
                        pharmacyEpcs: false,
                        pharmacySearch: med.pharmacyName || '',
                        instructionsToPharmacy: '',
                        doNotFillBefore: '',
                        isControlled: med.isControlled,
                        scheduleClass: med.scheduleClass
                    };
                    App.render();
                }
                break;
            }
            case 'set-temporary': {
                const medId = el.dataset.medId;
                AppState.setMedClassification(medId, 'temporary');
                Components.showToast('Medication set as temporary');
                break;
            }
            case 'set-permanent-rx': {
                const medId = el.dataset.medId;
                AppState.setMedClassification(medId, 'permanent_rx');
                Components.showToast('Medication set as permanent');
                break;
            }
            case 'view-med-detail': {
                AppState.selectedMedId = el.dataset.medId;
                App.render();
                break;
            }
            case 'close-med-detail': {
                AppState.selectedMedId = null;
                App.render();
                break;
            }
            case 'reconcile-meds': {
                AppState.reconcileOpen = true;
                App.render();
                break;
            }
            case 'close-reconcile': {
                AppState.reconcileOpen = false;
                App.render();
                break;
            }
            case 'complete-reconcile': {
                // Process discontinuations
                const dcCheckboxes = document.querySelectorAll('.reconcile-dc:checked');
                let dcCount = 0;
                for (const cb of dcCheckboxes) {
                    const medId = cb.dataset.medId;
                    AppState.discontinueMed(medId, 'Patient is not taking the medication', '', AppState.currentUser.name, false);
                    dcCount++;
                }
                AppState.updateLastReconciled();
                AppState.reconcileOpen = false;
                Components.showToast(`Medication reconciliation complete${dcCount > 0 ? '. ' + dcCount + ' medication(s) discontinued.' : ''}`);
                App.render();
                break;
            }
            case 'complete-reconcile-no-changes': {
                AppState.updateLastReconciled();
                AppState.reconcileOpen = false;
                Components.showToast('Medication reconciliation complete (no changes)');
                App.render();
                break;
            }
            case 'bulk-refill-rx': {
                AppState.bulkRefillOpen = true;
                AppState.selectedRefillIds = new Set();
                App.render();
                break;
            }
            case 'close-bulk-refill': {
                AppState.bulkRefillOpen = false;
                AppState.selectedRefillIds = new Set();
                App.render();
                break;
            }
            case 'submit-bulk-refill': {
                const ids = Array.from(AppState.selectedRefillIds);
                if (ids.length === 0) {
                    Components.showToast('Please select at least one medication');
                    return;
                }
                for (const medId of ids) {
                    const med = AppState.getMedById(medId);
                    if (med) {
                        AppState.addPrescription({
                            medicationName: med.medicationName,
                            ndc: med.ndc,
                            sig: med.sig,
                            qty: med.qty,
                            unit: med.unit,
                            refills: med.refills,
                            daysSupply: med.daysSupply,
                            classification: med.classification,
                            dispenseAsWritten: med.dispenseAsWritten,
                            diagnosis: med.diagnosis,
                            pharmacyId: med.pharmacyId,
                            pharmacyName: med.pharmacyName,
                            isControlled: med.isControlled,
                            scheduleClass: med.scheduleClass
                        });
                    }
                }
                AppState.bulkRefillOpen = false;
                AppState.selectedRefillIds = new Set();
                Components.showToast(`${ids.length} prescription(s) refilled`);
                App.render();
                break;
            }
            case 'approve-refill': {
                const reqId = el.dataset.requestId;
                AppState.approveRefillRequest(reqId);
                Components.showToast('Refill request approved');
                break;
            }
            case 'approve-refill-modified': {
                const reqId = el.dataset.requestId;
                const req = AppState.refillRequests.find(r => r.id === reqId);
                if (!req) return;
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Updated Sig</label>
                        <input type="text" class="form-input" id="modSig" value="${Components.escapeAttr(req.lastPrescription ? req.lastPrescription.sig : '')}">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Number of Refills</label>
                        <input type="number" class="form-input" id="modRefills" value="${req.lastPrescription ? req.lastPrescription.refills : 0}" min="0">
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-primary" id="submitModApproval">Approve with Modifications</button>
                `;
                Components.showModal('Approve with Modifications', bodyHtml, footerHtml);
                document.getElementById('submitModApproval').onclick = () => {
                    const sig = document.getElementById('modSig').value;
                    const refills = parseInt(document.getElementById('modRefills').value, 10);
                    AppState.approveRefillRequest(reqId, { sig, refills });
                    Components.closeModal();
                    Components.showToast('Refill request approved with modifications');
                };
                break;
            }
            case 'deny-refill': {
                const reqId = el.dataset.requestId;
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Reason for Denial</label>
                        <textarea class="form-input form-textarea" id="denyReason" rows="3" placeholder="Enter reason..."></textarea>
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-danger" id="submitDeny">Deny Request</button>
                `;
                Components.showModal('Deny Refill Request', bodyHtml, footerHtml);
                document.getElementById('submitDeny').onclick = () => {
                    const reason = document.getElementById('denyReason').value;
                    AppState.denyRefillRequest(reqId, reason);
                    Components.closeModal();
                    Components.showToast('Refill request denied');
                };
                break;
            }
            case 'approve-change': {
                const reqId = el.dataset.requestId;
                AppState.approveChangeRequest(reqId);
                Components.showToast('Change request approved');
                break;
            }
            case 'deny-change': {
                const reqId = el.dataset.requestId;
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Reason for Denial</label>
                        <textarea class="form-input form-textarea" id="denyChangeReason" rows="3" placeholder="Enter reason..."></textarea>
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-danger" id="submitDenyChange">Deny & Add Reason</button>
                `;
                Components.showModal('Deny Change Request', bodyHtml, footerHtml);
                document.getElementById('submitDenyChange').onclick = () => {
                    const reason = document.getElementById('denyChangeReason').value;
                    AppState.denyChangeRequest(reqId, reason);
                    Components.closeModal();
                    Components.showToast('Change request denied');
                };
                break;
            }
            case 'close-modal-overlay': {
                Components.closeModal();
                break;
            }
            case 'settings-tab': {
                AppState.settingsTab = el.dataset.tab;
                App.navigate('settings/' + el.dataset.tab);
                break;
            }
            case 'add-rx-template': {
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Medication Name *</label>
                        <input type="text" class="form-input" id="tplMedName" placeholder="e.g., Lisinopril 10mg tablet">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Sig *</label>
                        <input type="text" class="form-input" id="tplSig" placeholder="e.g., Take 1 tablet by mouth once daily">
                    </div>
                    <div class="form-row form-row-4">
                        <div class="form-group"><label class="form-label">Qty</label><input type="number" class="form-input" id="tplQty" value="30" min="1"></div>
                        <div class="form-group"><label class="form-label">Unit</label><input type="text" class="form-input" id="tplUnit" value="tablets"></div>
                        <div class="form-group"><label class="form-label">Refills</label><input type="number" class="form-input" id="tplRefills" value="0" min="0"></div>
                        <div class="form-group"><label class="form-label">Days Supply</label><input type="number" class="form-input" id="tplDays" value="30" min="1"></div>
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-primary" id="submitTemplate">Save Template</button>
                `;
                Components.showModal('Add Rx Template', bodyHtml, footerHtml);
                document.getElementById('submitTemplate').onclick = () => {
                    const name = document.getElementById('tplMedName').value;
                    const sig = document.getElementById('tplSig').value;
                    if (!name || !sig) { Components.showToast('Please fill in required fields'); return; }
                    AppState.addRxTemplate({
                        medicationName: name,
                        sig: sig,
                        qty: document.getElementById('tplQty').value,
                        unit: document.getElementById('tplUnit').value,
                        refills: document.getElementById('tplRefills').value,
                        daysSupply: document.getElementById('tplDays').value
                    });
                    Components.closeModal();
                    Components.showToast('Template added');
                };
                break;
            }
            case 'edit-template': {
                const tplId = el.dataset.templateId;
                const tpl = AppState.rxTemplates.find(t => t.id === tplId);
                if (!tpl) return;
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Medication Name</label>
                        <input type="text" class="form-input" id="editTplMedName" value="${Components.escapeAttr(tpl.medicationName)}">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Sig</label>
                        <input type="text" class="form-input" id="editTplSig" value="${Components.escapeAttr(tpl.sig)}">
                    </div>
                    <div class="form-row form-row-4">
                        <div class="form-group"><label class="form-label">Qty</label><input type="number" class="form-input" id="editTplQty" value="${tpl.qty}" min="1"></div>
                        <div class="form-group"><label class="form-label">Unit</label><input type="text" class="form-input" id="editTplUnit" value="${Components.escapeAttr(tpl.unit)}"></div>
                        <div class="form-group"><label class="form-label">Refills</label><input type="number" class="form-input" id="editTplRefills" value="${tpl.refills}" min="0"></div>
                        <div class="form-group"><label class="form-label">Days Supply</label><input type="number" class="form-input" id="editTplDays" value="${tpl.daysSupply}" min="1"></div>
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-primary" id="submitEditTemplate">Save Changes</button>
                `;
                Components.showModal('Edit Rx Template', bodyHtml, footerHtml);
                document.getElementById('submitEditTemplate').onclick = () => {
                    AppState.updateRxTemplate(tplId, {
                        medicationName: document.getElementById('editTplMedName').value,
                        sig: document.getElementById('editTplSig').value,
                        qty: parseInt(document.getElementById('editTplQty').value, 10),
                        unit: document.getElementById('editTplUnit').value,
                        refills: parseInt(document.getElementById('editTplRefills').value, 10),
                        daysSupply: parseInt(document.getElementById('editTplDays').value, 10)
                    });
                    Components.closeModal();
                    Components.showToast('Template updated');
                };
                break;
            }
            case 'delete-template': {
                const tplId = el.dataset.templateId;
                const tpl = AppState.rxTemplates.find(t => t.id === tplId);
                if (!tpl) return;
                const bodyHtml = `<p>Are you sure you want to delete the template for "${Components.escapeHtml(tpl.medicationName)}"?</p>`;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-danger" id="confirmDeleteTemplate">Delete</button>
                `;
                Components.showModal('Delete Template', bodyHtml, footerHtml);
                document.getElementById('confirmDeleteTemplate').onclick = () => {
                    AppState.deleteRxTemplate(tplId);
                    Components.closeModal();
                    Components.showToast('Template deleted');
                };
                break;
            }
            case 'add-custom-sig': {
                const categories = ['oral', 'prn', 'topical', 'ophthalmic', 'inhalation', 'injectable', 'sublingual'];
                let catOptions = '';
                for (const c of categories) {
                    catOptions += `<option value="${c}">${c.charAt(0).toUpperCase() + c.slice(1)}</option>`;
                }
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Sig Text *</label>
                        <input type="text" class="form-input" id="newSigText" placeholder="e.g., Take 1 tablet by mouth once daily">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Category</label>
                        <select class="form-input" id="newSigCategory">${catOptions}</select>
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-primary" id="submitNewSig">Add Sig</button>
                `;
                Components.showModal('Add Custom Sig', bodyHtml, footerHtml);
                document.getElementById('submitNewSig').onclick = () => {
                    const text = document.getElementById('newSigText').value;
                    const cat = document.getElementById('newSigCategory').value;
                    if (!text) { Components.showToast('Please enter sig text'); return; }
                    AppState.addCustomSig(text, cat);
                    Components.closeModal();
                    Components.showToast('Custom sig added');
                };
                break;
            }
            case 'edit-sig': {
                const sigId = el.dataset.sigId;
                const sig = AppState.customSigs.find(s => s.id === sigId);
                if (!sig) return;
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Sig Text</label>
                        <input type="text" class="form-input" id="editSigText" value="${Components.escapeAttr(sig.text)}">
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-primary" id="submitEditSig">Save</button>
                `;
                Components.showModal('Edit Custom Sig', bodyHtml, footerHtml);
                document.getElementById('submitEditSig').onclick = () => {
                    const text = document.getElementById('editSigText').value;
                    if (!text) return;
                    AppState.updateCustomSig(sigId, text);
                    Components.closeModal();
                    Components.showToast('Sig updated');
                };
                break;
            }
            case 'delete-sig': {
                const sigId = el.dataset.sigId;
                AppState.deleteCustomSig(sigId);
                Components.showToast('Custom sig deleted');
                break;
            }
            case 'add-allergy': {
                const bodyHtml = `
                    <div class="form-group">
                        <label class="form-label">Allergen *</label>
                        <input type="text" class="form-input" id="newAllergen" placeholder="e.g., Penicillin">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Reaction</label>
                        <input type="text" class="form-input" id="newAllergyReaction" placeholder="e.g., Rash, hives">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Severity</label>
                        <select class="form-input" id="newAllergySeverity">
                            <option value="Mild">Mild</option>
                            <option value="Moderate">Moderate</option>
                            <option value="Severe">Severe</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Type</label>
                        <select class="form-input" id="newAllergyType">
                            <option value="drug">Drug</option>
                            <option value="food">Food</option>
                            <option value="environmental">Environmental</option>
                        </select>
                    </div>
                `;
                const footerHtml = `
                    <button class="btn btn-outline" data-action="close-modal-overlay">Cancel</button>
                    <button class="btn btn-primary" id="submitAllergy">Add Allergy</button>
                `;
                Components.showModal('Add Allergy', bodyHtml, footerHtml);
                document.getElementById('submitAllergy').onclick = () => {
                    const allergen = document.getElementById('newAllergen').value;
                    if (!allergen) { Components.showToast('Please enter allergen'); return; }
                    const reaction = document.getElementById('newAllergyReaction').value;
                    const severity = document.getElementById('newAllergySeverity').value;
                    const type = document.getElementById('newAllergyType').value;
                    AppState.addAllergy(allergen, reaction, severity, type);
                    Components.closeModal();
                    Components.showToast('Allergy added');
                };
                break;
            }
            case 'remove-allergy': {
                const allergyId = el.dataset.allergyId;
                AppState.removeAllergy(allergyId);
                Components.showToast('Allergy removed');
                break;
            }
            case 'show-sig-list': {
                let sigListHtml = '<div class="sig-list-dropdown">';
                for (const sig of AppState.customSigs) {
                    sigListHtml += `<div class="sig-list-item" data-sig-text="${Components.escapeAttr(sig.text)}">${Components.escapeHtml(sig.text)}</div>`;
                }
                sigListHtml += '</div>';
                const sigSearch = document.getElementById('rxSig');
                if (sigSearch) {
                    const wrapper = sigSearch.closest('.sig-input-wrapper');
                    let existing = wrapper.querySelector('.sig-list-dropdown');
                    if (existing) { existing.remove(); return; }
                    wrapper.insertAdjacentHTML('beforeend', sigListHtml);
                    wrapper.querySelector('.sig-list-dropdown').addEventListener('click', (ev) => {
                        const item = ev.target.closest('.sig-list-item');
                        if (item) {
                            sigSearch.value = item.dataset.sigText;
                            if (AppState.prescribeFormData) {
                                AppState.prescribeFormData.sig = item.dataset.sigText;
                            }
                            wrapper.querySelector('.sig-list-dropdown').remove();
                        }
                    });
                }
                break;
            }
            case 'remove-diagnosis': {
                const code = el.dataset.code;
                if (AppState.prescribeFormData && AppState.prescribeFormData.diagnosis) {
                    AppState.prescribeFormData.diagnosis = AppState.prescribeFormData.diagnosis.filter(d => d.code !== code);
                    App.render();
                }
                break;
            }
        }
    },

    toggleDropdown(ddId) {
        const menu = document.getElementById(ddId + '-menu');
        if (!menu) return;
        if (App._openDropdownId && App._openDropdownId !== ddId) {
            const prev = document.getElementById(App._openDropdownId + '-menu');
            if (prev) prev.classList.remove('open');
        }
        menu.classList.toggle('open');
        App._openDropdownId = menu.classList.contains('open') ? ddId : null;
    },

    handleDropdownSelect(ddId, value) {
        const menu = document.getElementById(ddId + '-menu');
        if (menu) {
            menu.querySelectorAll('.dropdown-item').forEach(item => {
                item.classList.toggle('selected', item.dataset.value === value);
                item.querySelector('.check').innerHTML = item.dataset.value === value ? '&#10003;' : '';
            });
            menu.classList.remove('open');
        }
        App._openDropdownId = null;

        // Handle specific dropdowns
        switch (ddId) {
            case 'medHistoryFilter':
                AppState.medHistoryFilter = value;
                App.render();
                break;
            case 'drugToDrugLevel':
                AppState.updateSettings('drugDecisionSupport.drugToDrugLevel', value);
                break;
            case 'defaultPharmacy':
                AppState.updateSettings('defaultPharmacyId', value);
                break;
            case 'rxUnit':
                if (AppState.prescribeFormData) {
                    AppState.prescribeFormData.unit = value;
                }
                break;
            case 'discReason':
                // Just update the visual selection - submit reads it
                break;
        }
    },

    handleMedSearchSelect(el) {
        const name = el.dataset.medName;
        const isTemplate = el.dataset.isTemplate === 'true';
        if (AppState.prescribeFormData) {
            AppState.prescribeFormData.medicationName = name;
            if (isTemplate) {
                const tpl = AppState.rxTemplates.find(t => t.medicationName === name);
                if (tpl) {
                    AppState.prescribeFormData.sig = tpl.sig;
                    AppState.prescribeFormData.qty = tpl.qty;
                    AppState.prescribeFormData.unit = tpl.unit;
                    AppState.prescribeFormData.refills = tpl.refills;
                    AppState.prescribeFormData.daysSupply = tpl.daysSupply;
                    AppState.prescribeFormData.ndc = tpl.ndc;
                }
            }
            if (el.dataset.controlled === 'true') {
                AppState.prescribeFormData.isControlled = true;
                AppState.prescribeFormData.scheduleClass = el.dataset.schedule || null;
                if (el.dataset.schedule === 'II') {
                    AppState.prescribeFormData.refills = 0;
                }
            }
        }
        const sr = document.getElementById('medSearchResults');
        if (sr) sr.style.display = 'none';
        App.render();
    },

    handlePharmacySearchSelect(el) {
        const pharmId = el.dataset.pharmId;
        const pharm = AppState.getPharmacyById(pharmId);
        if (pharm && AppState.prescribeFormData) {
            AppState.prescribeFormData.pharmacyId = pharm.id;
            AppState.prescribeFormData.pharmacyName = pharm.name;
            AppState.prescribeFormData.pharmacyEpcs = pharm.epcs;
            AppState.prescribeFormData.pharmacySearch = pharm.name;
        }
        const pr = document.getElementById('pharmacySearchResults');
        if (pr) pr.style.display = 'none';
        App.render();
    },

    handleDiagnosisSearchSelect(el) {
        const code = el.dataset.code;
        const desc = el.dataset.desc;
        if (AppState.prescribeFormData) {
            if (!AppState.prescribeFormData.diagnosis) AppState.prescribeFormData.diagnosis = [];
            if (AppState.prescribeFormData.diagnosis.length < 2 && !AppState.prescribeFormData.diagnosis.find(d => d.code === code)) {
                AppState.prescribeFormData.diagnosis.push({ code, description: desc });
            }
            AppState.prescribeFormData.diagnosisSearch = '';
        }
        const dr = document.getElementById('diagnosisSearchResults');
        if (dr) dr.style.display = 'none';
        App.render();
    },

    handleDocMedSearchSelect(el) {
        const name = el.dataset.medName;
        const searchInput = document.getElementById('docMedSearch');
        if (searchInput) searchInput.value = name;
        const sr = document.getElementById('docMedSearchResults');
        if (sr) sr.style.display = 'none';
    },

    handleInput(e) {
        const target = e.target;

        // Medication search in prescribe form
        if (target.id === 'rxMedSearch') {
            clearTimeout(App._medSearchTimeout);
            App._medSearchTimeout = setTimeout(() => {
                const q = target.value;
                const results = AppState.searchMedications(q);
                const container = document.getElementById('medSearchResults');
                if (!container) return;
                if (results.length === 0) {
                    container.style.display = 'none';
                    return;
                }
                let html = '';
                for (const r of results) {
                    const tplLabel = r.isTemplate ? '<span class="template-label">Rx Template</span>' : '';
                    const ctrlLabel = r.controlled ? `<span class="controlled-label">C${r.schedule || ''}</span>` : '';
                    html += `<div class="med-search-item" data-med-name="${Components.escapeAttr(r.medicationName)}" data-is-template="${r.isTemplate}" data-controlled="${r.controlled || false}" data-schedule="${r.schedule || ''}" data-testid="med-result-${Components.escapeAttr(r.id)}">`;
                    html += `<span class="med-result-name">${Components.escapeHtml(r.medicationName)}</span>`;
                    html += tplLabel + ctrlLabel;
                    if (r.drugClass) html += `<span class="med-result-class">${Components.escapeHtml(r.drugClass)}</span>`;
                    html += '</div>';
                }
                container.innerHTML = html;
                container.style.display = 'block';
            }, 200);
        }

        // Pharmacy search
        if (target.id === 'rxPharmacySearch') {
            const q = target.value;
            if (AppState.prescribeFormData) AppState.prescribeFormData.pharmacySearch = q;
            const results = AppState.searchPharmacies(q);
            const container = document.getElementById('pharmacySearchResults');
            if (!container) return;
            if (results.length === 0) {
                container.style.display = 'none';
                return;
            }
            let html = '';
            for (const p of results) {
                const epcsLabel = p.epcs ? '<span class="epcs-badge">EPCS</span>' : '';
                html += `<div class="pharmacy-search-item" data-pharm-id="${Components.escapeAttr(p.id)}" data-testid="pharm-result-${Components.escapeAttr(p.id)}">`;
                html += `<span class="pharm-result-name">${Components.escapeHtml(p.name)}</span>${epcsLabel}`;
                html += `<span class="pharm-result-addr">${Components.escapeHtml(p.address)}, ${Components.escapeHtml(p.city)}, ${Components.escapeHtml(p.state)} ${Components.escapeHtml(p.zip)}</span>`;
                html += `<span class="pharm-result-phone">${Components.escapeHtml(p.phone)}</span>`;
                html += '</div>';
            }
            container.innerHTML = html;
            container.style.display = 'block';
        }

        // Diagnosis search
        if (target.id === 'rxDiagnosis') {
            const q = target.value.toLowerCase();
            if (AppState.prescribeFormData) AppState.prescribeFormData.diagnosisSearch = target.value;
            const container = document.getElementById('diagnosisSearchResults');
            if (!container) return;
            if (q.length < 2) { container.style.display = 'none'; return; }
            const matches = AppState.diagnosisCodes.filter(d =>
                d.code.toLowerCase().includes(q) || d.description.toLowerCase().includes(q)
            ).slice(0, 15);
            if (matches.length === 0) { container.style.display = 'none'; return; }
            let html = '';
            for (const dx of matches) {
                html += `<div class="diagnosis-search-item" data-code="${Components.escapeAttr(dx.code)}" data-desc="${Components.escapeAttr(dx.description)}" data-testid="dx-result-${Components.escapeAttr(dx.code)}">`;
                html += `<span class="dx-code">${Components.escapeHtml(dx.code)}</span> ${Components.escapeHtml(dx.description)}`;
                html += '</div>';
            }
            container.innerHTML = html;
            container.style.display = 'block';
        }

        // Doc med search
        if (target.id === 'docMedSearch') {
            clearTimeout(App._medSearchTimeout);
            App._medSearchTimeout = setTimeout(() => {
                const q = target.value;
                const results = AppState.searchMedications(q);
                const container = document.getElementById('docMedSearchResults');
                if (!container) return;
                if (results.length === 0) { container.style.display = 'none'; return; }
                let html = '';
                for (const r of results) {
                    html += `<div class="doc-med-search-item" data-med-name="${Components.escapeAttr(r.medicationName)}" data-testid="doc-med-result-${Components.escapeAttr(r.id)}">`;
                    html += `${Components.escapeHtml(r.medicationName)}`;
                    html += '</div>';
                }
                container.innerHTML = html;
                container.style.display = 'block';
            }, 200);
        }

        // Med history search
        if (target.id === 'medHistorySearch') {
            AppState.medHistorySearch = target.value;
            App.render();
        }

        // Prescribe form field updates
        if (AppState.prescribeFormData) {
            if (target.id === 'rxSig') AppState.prescribeFormData.sig = target.value;
            if (target.id === 'rxQty') AppState.prescribeFormData.qty = target.value;
            if (target.id === 'rxRefills') AppState.prescribeFormData.refills = target.value;
            if (target.id === 'rxDaysSupply') AppState.prescribeFormData.daysSupply = target.value;
            if (target.id === 'rxInstructions') AppState.prescribeFormData.instructionsToPharmacy = target.value;

            // Update submit/template button disabled state without full re-render
            const fd = AppState.prescribeFormData;
            const canSubmit = fd.medicationName && fd.sig && fd.qty;
            const submitBtn = document.querySelector('[data-action="submit-prescribe"]');
            const templateBtn = document.querySelector('[data-action="save-as-template"]');
            if (submitBtn) submitBtn.disabled = !canSubmit;
            if (templateBtn) templateBtn.disabled = !canSubmit;
        }
    },

    handleChange(e) {
        const target = e.target;

        // Classification radio
        if (target.name === 'rxClassification' && AppState.prescribeFormData) {
            AppState.prescribeFormData.classification = target.value;
        }

        // DAW checkbox
        if (target.id === 'rxDAW' && AppState.prescribeFormData) {
            AppState.prescribeFormData.dispenseAsWritten = target.checked;
        }

        // Do not fill before
        if (target.id === 'rxDoNotFillBefore' && AppState.prescribeFormData) {
            AppState.prescribeFormData.doNotFillBefore = target.value;
        }

        // Drug-to-allergy toggle
        if (target.id === 'drugToAllergyEnabled') {
            AppState.updateSettings('drugDecisionSupport.drugToAllergyEnabled', target.checked);
        }

        // Preference toggles
        if (target.id === 'autoPopulateLastPharmacy') {
            AppState.updateSettings('autoPopulateLastPharmacy', target.checked);
        }
        if (target.id === 'showCostEstimates') {
            AppState.updateSettings('showCostEstimates', target.checked);
        }
        if (target.id === 'showFormularyData') {
            AppState.updateSettings('showFormularyData', target.checked);
        }
    },

    handleKeydown(e) {
        // Close modals on Escape
        if (e.key === 'Escape') {
            if (AppState.prescribeFormOpen) {
                AppState.prescribeFormOpen = false;
                AppState.prescribeFormData = null;
                App.render();
            } else if (AppState.documentMedFormOpen) {
                AppState.documentMedFormOpen = false;
                App.render();
            } else if (AppState.discontinueModalOpen) {
                AppState.discontinueModalOpen = false;
                AppState.discontinueTarget = null;
                App.render();
            } else if (AppState.reconcileOpen) {
                AppState.reconcileOpen = false;
                App.render();
            } else if (AppState.bulkRefillOpen) {
                AppState.bulkRefillOpen = false;
                App.render();
            } else if (AppState.selectedMedId) {
                AppState.selectedMedId = null;
                App.render();
            } else {
                Components.closeModal();
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
