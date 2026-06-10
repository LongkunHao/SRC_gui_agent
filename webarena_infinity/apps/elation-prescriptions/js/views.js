const Views = {

    renderTopBar() {
        const pt = AppState.currentPatient;
        let html = '<div class="topbar-left">';
        html += `<div class="topbar-logo" data-testid="app-logo">Elation</div>`;
        html += '<div class="topbar-patient-info">';
        html += `<span class="patient-name" data-testid="patient-name">${Components.escapeHtml(pt.lastName)}, ${Components.escapeHtml(pt.firstName)}</span>`;
        html += `<span class="patient-demo">${Components.escapeHtml(pt.sex)} | DOB: ${Components.formatDate(pt.dob)} (${pt.age}y) | MRN: ${Components.escapeHtml(pt.id)}</span>`;
        html += '</div></div>';
        html += '<div class="topbar-right">';
        html += `<div class="topbar-user" data-testid="current-user">${Components.icon('user')} ${Components.escapeHtml(AppState.currentUser.name)}</div>`;
        html += '</div>';
        return html;
    },

    renderNavBar() {
        const navItems = [
            { route: 'chart', label: 'Chart', icon: 'file' },
            { route: 'med-history', label: 'Meds Hx', icon: 'list' },
            { route: 'rx-requests', label: 'Rx Requests', icon: 'inbox', badge: AppState.getAllPendingRequests().length },
            { route: 'settings', label: 'Settings', icon: 'settings' }
        ];

        let html = '<div class="navbar-items">';
        for (const item of navItems) {
            const active = AppState.currentView === item.route ? ' active' : '';
            html += `<div class="navbar-item${active}" data-route="${item.route}" data-testid="nav-${item.route}">`;
            html += `<span class="navbar-icon">${Components.icon(item.icon)}</span>`;
            html += `<span class="navbar-label">${Components.escapeHtml(item.label)}</span>`;
            if (item.badge && item.badge > 0) {
                html += `<span class="navbar-badge">${item.badge}</span>`;
            }
            html += '</div>';
        }
        html += '</div>';

        html += '<div class="navbar-actions">';
        html += `<button class="btn btn-primary btn-sm" data-action="open-prescribe" data-testid="btn-prescribe">${Components.icon('rx')} Prescribe</button>`;
        html += `<button class="btn btn-outline btn-sm" data-action="open-document-med" data-testid="btn-document-med">${Components.icon('plus')} Document Med</button>`;
        html += '</div>';
        return html;
    },

    renderChartView() {
        let html = '<div class="chart-layout">';
        html += '<div class="clinical-profile" data-testid="clinical-profile">';
        html += Views._renderClinicalProfile();
        html += '</div>';
        html += '<div class="chart-main">';
        html += Views._renderChartMain();
        html += '</div>';
        html += '</div>';
        return html;
    },

    _renderClinicalProfile() {
        const pt = AppState.currentPatient;
        let html = '<div class="cp-section">';
        html += '<div class="cp-header">Patient Info</div>';
        html += `<div class="cp-field"><span class="cp-label">Name:</span> ${Components.escapeHtml(pt.firstName)} ${Components.escapeHtml(pt.lastName)}</div>`;
        html += `<div class="cp-field"><span class="cp-label">DOB:</span> ${Components.formatDate(pt.dob)} (${pt.age}y)</div>`;
        html += `<div class="cp-field"><span class="cp-label">Sex:</span> ${Components.escapeHtml(pt.sex)}</div>`;
        html += `<div class="cp-field"><span class="cp-label">Weight:</span> ${pt.weightKg} kg</div>`;
        html += `<div class="cp-field"><span class="cp-label">Phone:</span> ${Components.escapeHtml(pt.phone)}</div>`;
        html += '</div>';

        // Allergies
        html += '<div class="cp-section">';
        html += '<div class="cp-header">Allergies <button class="btn-icon" data-action="add-allergy" data-testid="btn-add-allergy">' + Components.icon('plus') + '</button></div>';
        if (pt.allergies.length === 0) {
            html += '<div class="cp-empty">No known allergies</div>';
        } else {
            for (const a of pt.allergies) {
                html += `<div class="allergy-item" data-testid="allergy-${Components.escapeAttr(a.id)}">`;
                html += `<span class="allergy-name">${Components.escapeHtml(a.allergen)}</span>`;
                html += ` <span class="allergy-reaction">${Components.escapeHtml(a.reaction)}</span>`;
                html += ` ${Components.severityBadge(a.severity)}`;
                html += `<button class="btn-icon btn-icon-sm" data-action="remove-allergy" data-allergy-id="${Components.escapeAttr(a.id)}" data-testid="remove-allergy-${Components.escapeAttr(a.id)}">${Components.icon('x')}</button>`;
                html += '</div>';
            }
        }
        html += '</div>';

        // Problems
        html += '<div class="cp-section">';
        html += '<div class="cp-header">Problem List</div>';
        for (const p of pt.problems) {
            html += `<div class="problem-item"><span class="problem-code">${Components.escapeHtml(p.icd10)}</span> ${Components.escapeHtml(p.description)}</div>`;
        }
        html += '</div>';

        // Insurance
        html += '<div class="cp-section">';
        html += '<div class="cp-header">Insurance</div>';
        html += `<div class="cp-field"><span class="cp-label">Plan:</span> ${Components.escapeHtml(pt.insurance.planName)}</div>`;
        html += `<div class="cp-field"><span class="cp-label">Member ID:</span> ${Components.escapeHtml(pt.insurance.memberId)}</div>`;
        html += `<div class="cp-field"><span class="cp-label">PBM:</span> ${Components.escapeHtml(pt.insurance.pbm)}</div>`;
        html += `<div class="cp-field"><span class="cp-label">Copay (Generic):</span> $${pt.insurance.copayGeneric}</div>`;
        html += `<div class="cp-field"><span class="cp-label">Copay (Preferred):</span> $${pt.insurance.copayPreferred}</div>`;
        html += '</div>';

        // Preferred Pharmacy
        const prefPharm = AppState.getPharmacyById(pt.preferredPharmacyId);
        if (prefPharm) {
            html += '<div class="cp-section">';
            html += '<div class="cp-header">Preferred Pharmacy</div>';
            html += `<div class="cp-field">${Components.escapeHtml(prefPharm.name)}</div>`;
            html += `<div class="cp-field">${Components.escapeHtml(prefPharm.address)}, ${Components.escapeHtml(prefPharm.city)}</div>`;
            html += `<div class="cp-field">${Components.escapeHtml(prefPharm.phone)}</div>`;
            html += '</div>';
        }

        return html;
    },

    _renderChartMain() {
        let html = '';

        // Permanent Rx Meds
        html += '<div class="med-list-section" data-testid="permanent-rx-section">';
        html += '<div class="med-list-header">';
        html += '<h3>Permanent Rx Meds</h3>';
        html += '<div class="med-list-actions">';
        html += `<button class="btn btn-sm btn-outline" data-action="reconcile-meds" data-testid="btn-reconcile-meds">${Components.icon('check')} Reconcile Meds</button>`;
        html += `<button class="btn btn-sm btn-outline" data-action="bulk-refill-rx" data-testid="btn-bulk-refill">${Components.icon('refresh')} Bulk Refill</button>`;
        html += '</div></div>';
        if (AppState.currentPatient.lastReconciledDate) {
            html += `<div class="last-reconciled">Last Reconciled: ${Components.formatDate(AppState.currentPatient.lastReconciledDate)}</div>`;
        }
        html += Views._renderMedList(AppState.permanentRxMeds, 'rx');
        html += '</div>';

        // Permanent OTC Meds
        html += '<div class="med-list-section" data-testid="permanent-otc-section">';
        html += '<div class="med-list-header"><h3>Permanent OTC Meds</h3></div>';
        html += Views._renderMedList(AppState.permanentOtcMeds, 'otc');
        html += '</div>';

        // Temporary Meds
        if (AppState.temporaryMeds.length > 0) {
            html += '<div class="med-list-section" data-testid="temporary-section">';
            html += '<div class="med-list-header"><h3>Temporary Medications</h3></div>';
            html += Views._renderMedList(AppState.temporaryMeds, 'tmp');
            html += '</div>';
        }

        return html;
    },

    _renderMedList(meds, type) {
        if (meds.length === 0) {
            return Components.emptyState('', 'No medications in this category');
        }
        let html = '<div class="med-list">';
        for (const med of meds) {
            html += Views._renderMedItem(med);
        }
        html += '</div>';
        return html;
    },

    _renderMedItem(med) {
        const isControlled = med.isControlled ? ' <span class="controlled-badge">C' + (med.scheduleClass || '') + '</span>' : '';
        let html = `<div class="med-item" data-med-id="${Components.escapeAttr(med.id)}" data-testid="med-item-${Components.escapeAttr(med.id)}">`;
        html += '<div class="med-item-main">';
        html += `<div class="med-item-name">${Components.escapeHtml(med.medicationName)}${isControlled}</div>`;
        html += `<div class="med-item-sig">${Components.escapeHtml(med.sig)}</div>`;
        html += '<div class="med-item-details">';
        html += `<span>Qty: ${med.qty} ${Components.escapeHtml(med.unit || '')}</span>`;
        if (med.refills != null) html += `<span>Refills: ${med.refillsRemaining != null ? med.refillsRemaining : med.refills}</span>`;
        if (med.daysSupply) html += `<span>Days: ${med.daysSupply}</span>`;
        if (med.pharmacyName) html += `<span>${Components.icon('pharmacy')} ${Components.escapeHtml(med.pharmacyName)}</span>`;
        html += '</div>';
        if (med.lastFilledDate) {
            html += `<div class="med-item-filled">Last filled: ${Components.formatDate(med.lastFilledDate)}</div>`;
        }
        html += '</div>';
        html += '<div class="med-item-actions">';
        html += `<div class="med-actions-dropdown" data-testid="med-actions-${Components.escapeAttr(med.id)}">`;
        html += `<button class="btn btn-sm btn-outline" data-dropdown="med-actions-${Components.escapeAttr(med.id)}">Actions ${Components.icon('chevronDown')}</button>`;
        html += `<div class="dropdown-menu" id="med-actions-${Components.escapeAttr(med.id)}-menu">`;
        if (med.status === 'active') {
            html += `<div class="dropdown-item" data-action="refill-med" data-med-id="${Components.escapeAttr(med.id)}" data-testid="action-refill-${Components.escapeAttr(med.id)}">Refill</div>`;
            html += `<div class="dropdown-item" data-action="discontinue-med" data-med-id="${Components.escapeAttr(med.id)}" data-testid="action-discontinue-${Components.escapeAttr(med.id)}">Discontinue</div>`;
            if (med.classification === 'permanent_rx') {
                html += `<div class="dropdown-item" data-action="set-temporary" data-med-id="${Components.escapeAttr(med.id)}" data-testid="action-set-temp-${Components.escapeAttr(med.id)}">Set as Temporary</div>`;
            } else if (med.classification === 'temporary') {
                html += `<div class="dropdown-item" data-action="set-permanent-rx" data-med-id="${Components.escapeAttr(med.id)}" data-testid="action-set-perm-${Components.escapeAttr(med.id)}">Set as Permanent</div>`;
            }
        }
        html += `<div class="dropdown-item" data-action="view-med-detail" data-med-id="${Components.escapeAttr(med.id)}" data-testid="action-view-${Components.escapeAttr(med.id)}">View Details</div>`;
        html += '</div></div>';
        html += '</div>';
        html += '</div>';
        return html;
    },

    renderMedHistoryView() {
        let html = '<div class="med-history-view" data-testid="med-history-view">';
        html += '<div class="med-history-toolbar">';
        html += '<h2>Medication History</h2>';
        html += '<div class="med-history-controls">';
        html += `<div class="search-box"><input type="text" class="form-input" id="medHistorySearch" data-testid="med-history-search" placeholder="Search medications..." value="${Components.escapeAttr(AppState.medHistorySearch)}">${Components.icon('search')}</div>`;
        const filterOptions = [
            { value: 'all', label: 'All Medications' },
            { value: 'permanent_rx', label: 'Permanent Rx' },
            { value: 'permanent_otc', label: 'Permanent OTC' },
            { value: 'temporary', label: 'Temporary' },
            { value: 'discontinued', label: 'Discontinued' },
            { value: 'canceled', label: 'Canceled Scripts' }
        ];
        html += Components.dropdown('medHistoryFilter', filterOptions, AppState.medHistoryFilter, 'Filter...');
        html += '</div>';
        html += '<div class="med-history-shortcuts">';
        html += `<button class="btn btn-sm btn-outline" data-action="reconcile-meds" data-testid="mh-reconcile">${Components.icon('check')} Reconcile</button>`;
        html += `<button class="btn btn-sm btn-outline" data-action="bulk-refill-rx" data-testid="mh-bulk-refill">${Components.icon('refresh')} Bulk Refill</button>`;
        html += '</div></div>';

        const meds = AppState.getMedHistoryFiltered();
        if (meds.length === 0) {
            html += Components.emptyState('', 'No medications match your search');
        } else {
            // Group by classification
            const groups = {};
            for (const med of meds) {
                const cls = med.classification || 'other';
                if (!groups[cls]) groups[cls] = [];
                groups[cls].push(med);
            }
            const order = ['permanent_rx', 'permanent_otc', 'temporary', 'discontinued', 'canceled'];
            const labels = {
                permanent_rx: 'Permanent Rx Meds',
                permanent_otc: 'Permanent OTC Meds',
                temporary: 'Temporary Medications',
                discontinued: 'Discontinued Medications',
                canceled: 'Scripts Canceled'
            };
            for (const cls of order) {
                if (!groups[cls] || groups[cls].length === 0) continue;
                html += `<div class="mh-group" data-testid="mh-group-${cls}">`;
                html += `<div class="mh-group-header">${Components.escapeHtml(labels[cls] || cls)} (${groups[cls].length})</div>`;
                for (const med of groups[cls]) {
                    html += Views._renderMedHistoryItem(med);
                }
                html += '</div>';
            }
        }
        html += '</div>';
        return html;
    },

    _renderMedHistoryItem(med) {
        let html = `<div class="mh-item" data-med-id="${Components.escapeAttr(med.id)}" data-testid="mh-item-${Components.escapeAttr(med.id)}">`;
        html += '<div class="mh-item-main">';
        html += `<div class="mh-item-name">${Components.escapeHtml(med.medicationName)} ${Components.statusBadge(med.status)}</div>`;
        html += `<div class="mh-item-sig">${Components.escapeHtml(med.sig)}</div>`;
        html += '<div class="mh-item-meta">';
        if (med.prescriberName) html += `<span>Prescribed by: ${Components.escapeHtml(med.prescriberName)}</span>`;
        if (med.startDate) html += `<span>Started: ${Components.formatDate(med.startDate)}</span>`;
        if (med.discontinuedDate) {
            html += `<span>Discontinued: ${Components.formatDate(med.discontinuedDate)}</span>`;
            html += `<span>Reason: ${Components.escapeHtml(med.discontinueReason || '')}</span>`;
        }
        if (med.canceledDate) {
            html += `<span>Canceled: ${Components.formatDate(med.canceledDate)}</span>`;
        }
        html += '</div>';
        html += '</div>';
        if (med.status === 'active') {
            html += '<div class="mh-item-actions">';
            html += `<button class="btn btn-sm btn-outline" data-action="refill-med" data-med-id="${Components.escapeAttr(med.id)}">Refill</button>`;
            html += `<button class="btn btn-sm btn-outline" data-action="discontinue-med" data-med-id="${Components.escapeAttr(med.id)}">Discontinue</button>`;
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    renderRxRequestsView() {
        let html = '<div class="rx-requests-view" data-testid="rx-requests-view">';
        html += '<h2>Rx Requests</h2>';

        const pendingRefills = AppState.getPendingRefillRequests();
        const pendingChanges = AppState.getPendingChangeRequests();

        // Pending section
        if (pendingRefills.length > 0 || pendingChanges.length > 0) {
            html += '<div class="rr-section">';
            html += `<div class="rr-section-header">Requiring Action (${pendingRefills.length + pendingChanges.length})</div>`;
            for (const req of pendingRefills) {
                html += Views._renderRefillRequest(req);
            }
            for (const req of pendingChanges) {
                html += Views._renderChangeRequest(req);
            }
            html += '</div>';
        } else {
            html += Components.emptyState(Components.icon('inbox'), 'No pending requests');
        }

        // Processed section
        const processed = [...AppState.refillRequests.filter(r => r.status !== 'pending'), ...AppState.changeRequests.filter(r => r.status !== 'pending')];
        if (processed.length > 0) {
            html += '<div class="rr-section">';
            html += `<div class="rr-section-header">Recently Processed (${processed.length})</div>`;
            for (const req of processed) {
                if (req.type === 'change') {
                    html += Views._renderChangeRequest(req);
                } else {
                    html += Views._renderRefillRequest(req);
                }
            }
            html += '</div>';
        }

        html += '</div>';
        return html;
    },

    _renderRefillRequest(req) {
        let html = `<div class="rr-item" data-request-id="${Components.escapeAttr(req.id)}" data-testid="rr-item-${Components.escapeAttr(req.id)}">`;
        html += '<div class="rr-item-header">';
        html += `<span class="rr-type-badge">${Components.badge('Refill Request', 'info')}</span>`;
        html += ` ${Components.statusBadge(req.status)}`;
        html += `<span class="rr-date">${Components.formatRelativeDate(req.requestDate)}</span>`;
        html += '</div>';
        html += `<div class="rr-item-med">${Components.escapeHtml(req.medicationName)}</div>`;
        html += '<div class="rr-item-details">';
        html += `<span>Pharmacy: ${Components.escapeHtml(req.pharmacyName)}</span>`;
        if (req.lastPrescription) {
            html += `<span>Last Rx: ${Components.escapeHtml(req.lastPrescription.sig)} | Qty: ${req.lastPrescription.qty} | Refills: ${req.lastPrescription.refills}</span>`;
        }
        if (req.lastDispensed) {
            html += `<span>Last Dispensed: ${Components.formatDate(req.lastDispensed.date)}</span>`;
        }
        if (req.notes) {
            html += `<span class="rr-notes">${Components.escapeHtml(req.notes)}</span>`;
        }
        html += '</div>';
        if (req.status === 'pending') {
            html += '<div class="rr-item-actions">';
            html += `<button class="btn btn-sm btn-success" data-action="approve-refill" data-request-id="${Components.escapeAttr(req.id)}" data-testid="approve-${Components.escapeAttr(req.id)}">Approve</button>`;
            html += `<button class="btn btn-sm btn-outline" data-action="approve-refill-modified" data-request-id="${Components.escapeAttr(req.id)}" data-testid="approve-modified-${Components.escapeAttr(req.id)}">Approve with Modifications</button>`;
            html += `<button class="btn btn-sm btn-danger" data-action="deny-refill" data-request-id="${Components.escapeAttr(req.id)}" data-testid="deny-${Components.escapeAttr(req.id)}">Deny</button>`;
            html += '</div>';
        }
        if (req.status === 'denied' && req.denyReason) {
            html += `<div class="rr-deny-reason">Denial reason: ${Components.escapeHtml(req.denyReason)}</div>`;
        }
        if (req.status === 'approved' && req.modifications) {
            html += `<div class="rr-modifications">Modified: ${Components.escapeHtml(JSON.stringify(req.modifications))}</div>`;
        }
        html += '</div>';
        return html;
    },

    _renderChangeRequest(req) {
        let html = `<div class="rr-item rr-change" data-request-id="${Components.escapeAttr(req.id)}" data-testid="cr-item-${Components.escapeAttr(req.id)}">`;
        html += '<div class="rr-item-header">';
        html += `<span class="rr-type-badge">${Components.badge('Change Request', 'warning')}</span>`;
        html += ` ${Components.statusBadge(req.status)}`;
        html += `<span class="rr-date">${Components.formatRelativeDate(req.requestDate)}</span>`;
        html += '</div>';
        html += `<div class="rr-item-med">${Components.escapeHtml(req.medicationName)}</div>`;
        html += '<div class="rr-item-details">';
        html += `<span>Pharmacy: ${Components.escapeHtml(req.pharmacyName)}</span>`;
        html += `<span>Reason: ${Components.escapeHtml(req.reason)}</span>`;
        if (req.requestedMedication && req.requestedMedication !== req.originalMedication) {
            html += `<span>Requested: ${Components.escapeHtml(req.originalMedication)} → ${Components.escapeHtml(req.requestedMedication)}</span>`;
        }
        html += '</div>';
        if (req.status === 'pending') {
            html += '<div class="rr-item-actions">';
            html += `<button class="btn btn-sm btn-success" data-action="approve-change" data-request-id="${Components.escapeAttr(req.id)}" data-testid="approve-change-${Components.escapeAttr(req.id)}">Approve</button>`;
            html += `<button class="btn btn-sm btn-danger" data-action="deny-change" data-request-id="${Components.escapeAttr(req.id)}" data-testid="deny-change-${Components.escapeAttr(req.id)}">Deny & Add Reason</button>`;
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    renderSettingsView() {
        const tabs = [
            { id: 'templates', label: 'Rx Templates' },
            { id: 'sigs', label: 'Custom Rx Sigs' },
            { id: 'drug-support', label: 'Drug Decision Support' },
            { id: 'preferences', label: 'Preferences' }
        ];

        let html = '<div class="settings-view" data-testid="settings-view">';
        html += '<h2>Prescription Settings</h2>';
        html += '<div class="settings-tabs">';
        for (const tab of tabs) {
            const active = AppState.settingsTab === tab.id ? ' active' : '';
            html += `<div class="settings-tab${active}" data-action="settings-tab" data-tab="${tab.id}" data-testid="settings-tab-${tab.id}">${Components.escapeHtml(tab.label)}</div>`;
        }
        html += '</div>';
        html += '<div class="settings-content">';

        switch (AppState.settingsTab) {
            case 'templates': html += Views._renderRxTemplatesSettings(); break;
            case 'sigs': html += Views._renderCustomSigsSettings(); break;
            case 'drug-support': html += Views._renderDrugSupportSettings(); break;
            case 'preferences': html += Views._renderPreferencesSettings(); break;
        }

        html += '</div></div>';
        return html;
    },

    _renderRxTemplatesSettings() {
        let html = '<div class="settings-section" data-testid="rx-templates-section">';
        html += '<div class="settings-section-header">';
        html += '<h3>Rx Templates</h3>';
        html += `<button class="btn btn-sm btn-primary" data-action="add-rx-template" data-testid="btn-add-template">${Components.icon('plus')} Add Rx Template</button>`;
        html += '</div>';
        if (AppState.rxTemplates.length === 0) {
            html += Components.emptyState('', 'No Rx templates saved');
        } else {
            html += '<div class="template-list">';
            for (const tpl of AppState.rxTemplates) {
                html += `<div class="template-item" data-testid="template-${Components.escapeAttr(tpl.id)}">`;
                html += '<div class="template-item-main">';
                html += `<div class="template-name">${Components.escapeHtml(tpl.medicationName)}</div>`;
                html += `<div class="template-sig">${Components.escapeHtml(tpl.sig)}</div>`;
                html += `<div class="template-details">Qty: ${tpl.qty} ${Components.escapeHtml(tpl.unit)} | Refills: ${tpl.refills} | Days: ${tpl.daysSupply}</div>`;
                html += '</div>';
                html += '<div class="template-actions">';
                html += `<button class="btn btn-sm btn-outline" data-action="edit-template" data-template-id="${Components.escapeAttr(tpl.id)}" data-testid="edit-template-${Components.escapeAttr(tpl.id)}">${Components.icon('edit')}</button>`;
                html += `<button class="btn btn-sm btn-outline btn-danger-outline" data-action="delete-template" data-template-id="${Components.escapeAttr(tpl.id)}" data-testid="delete-template-${Components.escapeAttr(tpl.id)}">${Components.icon('trash')}</button>`;
                html += '</div></div>';
            }
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    _renderCustomSigsSettings() {
        let html = '<div class="settings-section" data-testid="custom-sigs-section">';
        html += '<div class="settings-section-header">';
        html += '<h3>Custom Rx Sigs</h3>';
        html += `<button class="btn btn-sm btn-primary" data-action="add-custom-sig" data-testid="btn-add-sig">${Components.icon('plus')} Add Custom Sig</button>`;
        html += '</div>';

        const categories = [...new Set(AppState.customSigs.map(s => s.category))];
        for (const cat of categories) {
            const sigs = AppState.customSigs.filter(s => s.category === cat);
            html += `<div class="sig-category" data-testid="sig-category-${Components.escapeAttr(cat)}">`;
            html += `<div class="sig-category-header">${Components.escapeHtml(cat.charAt(0).toUpperCase() + cat.slice(1))} (${sigs.length})</div>`;
            for (const sig of sigs) {
                html += `<div class="sig-item" data-testid="sig-${Components.escapeAttr(sig.id)}">`;
                html += `<span class="sig-text">${Components.escapeHtml(sig.text)}</span>`;
                html += '<div class="sig-actions">';
                html += `<button class="btn-icon" data-action="edit-sig" data-sig-id="${Components.escapeAttr(sig.id)}" data-testid="edit-sig-${Components.escapeAttr(sig.id)}">${Components.icon('edit')}</button>`;
                html += `<button class="btn-icon" data-action="delete-sig" data-sig-id="${Components.escapeAttr(sig.id)}" data-testid="delete-sig-${Components.escapeAttr(sig.id)}">${Components.icon('trash')}</button>`;
                html += '</div></div>';
            }
            html += '</div>';
        }
        html += '</div>';
        return html;
    },

    _renderDrugSupportSettings() {
        const dds = AppState.settings.drugDecisionSupport;
        let html = '<div class="settings-section" data-testid="drug-support-section">';
        html += '<h3>Drug Decision Support</h3>';
        html += '<div class="settings-form">';

        // Drug-to-Drug alerts level
        html += '<div class="form-group">';
        html += '<label class="form-label">Drug-to-Drug Interaction Alerts</label>';
        const ddOptions = [
            { value: 'all', label: 'All alerts (Minor, Moderate, Major)' },
            { value: 'major_moderate', label: 'Major and Moderate only' },
            { value: 'major_only', label: 'Major only' }
        ];
        html += Components.dropdown('drugToDrugLevel', ddOptions, dds.drugToDrugLevel, 'Select level');
        html += '</div>';

        // Drug-to-Allergy toggle
        html += '<div class="form-group">';
        html += Components.toggle('drugToAllergyEnabled', dds.drugToAllergyEnabled, 'Drug-to-Allergy Alerts', 'Show alerts when prescribing medications that may interact with patient allergies');
        html += '</div>';

        html += '</div></div>';
        return html;
    },

    _renderPreferencesSettings() {
        let html = '<div class="settings-section" data-testid="preferences-section">';
        html += '<h3>Prescription Preferences</h3>';
        html += '<div class="settings-form">';

        // Default pharmacy
        const pharmOptions = AppState.pharmacies.map(p => ({ value: p.id, label: p.name }));
        html += '<div class="form-group">';
        html += '<label class="form-label">Default Pharmacy</label>';
        html += Components.dropdown('defaultPharmacy', pharmOptions, AppState.settings.defaultPharmacyId, 'Select pharmacy');
        html += '</div>';

        html += '<div class="form-group">';
        html += Components.toggle('autoPopulateLastPharmacy', AppState.settings.autoPopulateLastPharmacy, 'Auto-populate Last Used Pharmacy', 'Automatically use the most recently used pharmacy when prescribing');
        html += '</div>';

        html += '<div class="form-group">';
        html += Components.toggle('showCostEstimates', AppState.settings.showCostEstimates, 'Show Cost Estimates', 'Display medication cost estimates when prescribing');
        html += '</div>';

        html += '<div class="form-group">';
        html += Components.toggle('showFormularyData', AppState.settings.showFormularyData, 'Show Formulary Information', 'Display formulary status and copay information');
        html += '</div>';

        html += '</div></div>';
        return html;
    },

    // --- Prescribe Form ---

    renderPrescribeForm() {
        const fd = AppState.prescribeFormData || {};
        let html = '<div class="prescribe-overlay" data-testid="prescribe-form">';
        html += '<div class="prescribe-modal">';
        html += '<div class="prescribe-header">';
        html += '<h2>Prescription Form</h2>';
        html += `<button class="btn-icon" data-action="close-prescribe" data-testid="close-prescribe">${Components.icon('x')}</button>`;
        html += '</div>';

        html += '<div class="prescribe-body">';
        html += '<div class="prescribe-main">';

        // Medication search
        html += '<div class="form-group">';
        html += '<label class="form-label">Medication <span class="required">*</span></label>';
        html += `<div class="med-search-wrapper">`;
        html += `<input type="text" class="form-input" id="rxMedSearch" data-testid="rx-med-search" placeholder="Search medication name..." value="${Components.escapeAttr(fd.medicationName || '')}" autocomplete="off">`;
        html += '<div class="med-search-results" id="medSearchResults" style="display:none;"></div>';
        html += '</div></div>';

        if (fd.medicationName) {
            // Sig
            html += '<div class="form-group">';
            html += '<label class="form-label">Sig (Directions) <span class="required">*</span></label>';
            html += `<div class="sig-input-wrapper">`;
            html += `<input type="text" class="form-input" id="rxSig" data-testid="rx-sig" placeholder="e.g., Take 1 tablet by mouth once daily" value="${Components.escapeAttr(fd.sig || '')}">`;
            html += `<button class="btn btn-sm btn-outline" data-action="show-sig-list" data-testid="btn-sig-list">Saved Sigs</button>`;
            html += '</div></div>';

            // Qty, Unit, Refills, Days Supply in a row
            html += '<div class="form-row form-row-4">';
            html += '<div class="form-group">' + Components.numberInput('rxQty', fd.qty, 'Qty', true, 'Qty *', 1) + '</div>';
            html += '<div class="form-group">';
            html += '<label class="form-label">Unit</label>';
            const unitOpts = UNIT_OPTIONS.map(u => ({ value: u, label: u }));
            html += Components.dropdown('rxUnit', unitOpts, fd.unit || 'tablets', 'Unit');
            html += '</div>';
            html += '<div class="form-group">' + Components.numberInput('rxRefills', fd.refills != null ? fd.refills : '', 'Refills', true, 'Refills *', 0) + '</div>';
            html += '<div class="form-group">' + Components.numberInput('rxDaysSupply', fd.daysSupply || 30, 'Days', false, 'Days Supply', 1) + '</div>';
            html += '</div>';

            // Classification
            html += '<div class="form-group">';
            html += '<label class="form-label">Classification</label>';
            const classOpts = [
                { value: 'permanent_rx', label: 'Permanent' },
                { value: 'temporary', label: 'Temporary' }
            ];
            html += Components.radioGroup('rxClassification', classOpts, fd.classification || 'permanent_rx');
            html += '</div>';

            // Dispense as Written
            html += '<div class="form-group">';
            html += Components.checkbox('rxDAW', fd.dispenseAsWritten || false, 'Dispense as Written');
            html += '</div>';

            // Diagnosis
            html += '<div class="form-group">';
            html += '<label class="form-label">Diagnosis (ICD-10)</label>';
            html += `<input type="text" class="form-input" id="rxDiagnosis" data-testid="rx-diagnosis" placeholder="Search diagnosis code..." value="${Components.escapeAttr(fd.diagnosisSearch || '')}" autocomplete="off">`;
            html += '<div class="diagnosis-search-results" id="diagnosisSearchResults" style="display:none;"></div>';
            if (fd.diagnosis && fd.diagnosis.length > 0) {
                html += '<div class="selected-diagnoses">';
                for (const dx of fd.diagnosis) {
                    html += `<span class="diagnosis-tag">${Components.escapeHtml(dx.code)} - ${Components.escapeHtml(dx.description)} <button class="btn-icon btn-icon-sm" data-action="remove-diagnosis" data-code="${Components.escapeAttr(dx.code)}">${Components.icon('x')}</button></span>`;
                }
                html += '</div>';
            }
            html += '</div>';

            // Pharmacy
            html += '<div class="form-group">';
            html += '<label class="form-label">Pharmacy</label>';
            html += `<input type="text" class="form-input" id="rxPharmacySearch" data-testid="rx-pharmacy-search" placeholder="Search pharmacy..." value="${Components.escapeAttr(fd.pharmacySearch || fd.pharmacyName || '')}" autocomplete="off">`;
            html += '<div class="pharmacy-search-results" id="pharmacySearchResults" style="display:none;"></div>';
            if (fd.pharmacyName) {
                html += `<div class="selected-pharmacy">${Components.icon('pharmacy')} ${Components.escapeHtml(fd.pharmacyName)}`;
                if (fd.pharmacyEpcs) html += ' <span class="epcs-badge">EPCS</span>';
                html += '</div>';
            }
            html += '</div>';

            // Instructions to Pharmacy
            html += '<div class="form-group">';
            html += Components.textarea('rxInstructions', fd.instructionsToPharmacy, 'Instructions to pharmacy...', 2, 'Instructions to Pharmacy');
            html += '</div>';

            // Do not fill before date
            html += '<div class="form-group">';
            html += '<label class="form-label">Do Not Fill Before</label>';
            html += `<input type="date" class="form-input" id="rxDoNotFillBefore" data-testid="rx-do-not-fill-before" value="${Components.escapeAttr(fd.doNotFillBefore || '')}">`;
            html += '</div>';

            // Drug interaction alerts
            const interactions = AppState.getInteractionsForMed(fd.medicationName);
            const allergyAlerts = AppState.getAllergyAlertsForMed(fd.medicationName);
            if (interactions.length > 0 || allergyAlerts.length > 0) {
                html += '<div class="rx-alerts" data-testid="rx-alerts">';
                html += '<h4>Drug Alerts</h4>';
                for (const alert of allergyAlerts) {
                    html += Components.allergyAlert(alert);
                }
                for (const di of interactions) {
                    html += Components.drugInteractionAlert(di);
                }
                html += '</div>';
            }
        }

        html += '</div>'; // prescribe-main

        // Right panel - Coverage/Formulary
        if (fd.medicationName) {
            html += '<div class="prescribe-sidebar">';
            const formulary = AppState.getFormularyInfo(fd.medicationName);
            if (formulary && AppState.settings.showFormularyData) {
                html += '<div class="rx-panel" data-testid="formulary-panel">';
                html += '<div class="rx-panel-header">Coverage</div>';
                html += `<div class="rx-panel-row">${Components.formularyBadge(formulary.status)}</div>`;
                if (formulary.tier) html += `<div class="rx-panel-row"><span class="rx-panel-label">Tier:</span> ${formulary.tier}</div>`;
                if (formulary.copay != null) html += `<div class="rx-panel-row"><span class="rx-panel-label">Copay:</span> $${formulary.copay}</div>`;
                if (formulary.requiresPA) html += `<div class="rx-panel-row">${Components.badge('Prior Auth Required', 'warning')}</div>`;
                if (formulary.alternatives && formulary.alternatives.length > 0) {
                    html += '<div class="rx-panel-row"><span class="rx-panel-label">Alternatives:</span></div>';
                    for (const alt of formulary.alternatives) {
                        html += `<div class="rx-panel-alt">${Components.escapeHtml(alt)}</div>`;
                    }
                }
                html += '</div>';
            }
            html += '</div>';
        }

        html += '</div>'; // prescribe-body

        // Footer
        html += '<div class="prescribe-footer">';
        const canSubmit = fd.medicationName && fd.sig && fd.qty;
        html += `<button class="btn btn-outline" data-action="discard-prescribe" data-testid="btn-discard-rx">Discard</button>`;
        html += `<button class="btn btn-outline" data-action="save-as-template" data-testid="btn-save-template"${!canSubmit ? ' disabled' : ''}>Save as Rx Template</button>`;
        html += `<button class="btn btn-primary" data-action="submit-prescribe" data-testid="btn-prescribe-submit"${!canSubmit ? ' disabled' : ''}>Prescribe</button>`;
        html += '</div>';

        html += '</div></div>';
        return html;
    },

    // --- Document Med Form ---

    renderDocumentMedForm() {
        let html = '<div class="prescribe-overlay" data-testid="document-med-form">';
        html += '<div class="prescribe-modal prescribe-modal-sm">';
        html += '<div class="prescribe-header">';
        html += '<h2>Document Med Patient is On</h2>';
        html += `<button class="btn-icon" data-action="close-document-med" data-testid="close-document-med">${Components.icon('x')}</button>`;
        html += '</div>';
        html += '<div class="prescribe-body">';
        html += '<div class="prescribe-main">';

        // Med type
        html += '<div class="form-group">';
        html += '<label class="form-label">Medication Type</label>';
        const typeOpts = [{ value: 'rx', label: 'Rx' }, { value: 'otc', label: 'OTC' }];
        html += Components.radioGroup('docMedType', typeOpts, 'rx');
        html += '</div>';

        // Medication search
        html += '<div class="form-group">';
        html += '<label class="form-label">Medication <span class="required">*</span></label>';
        html += `<input type="text" class="form-input" id="docMedSearch" data-testid="doc-med-search" placeholder="Search medication name..." autocomplete="off">`;
        html += '<div class="med-search-results" id="docMedSearchResults" style="display:none;"></div>';
        html += '</div>';

        // Start date
        html += '<div class="form-group">';
        html += '<label class="form-label">Start Date</label>';
        html += `<input type="date" class="form-input" id="docMedStartDate" data-testid="doc-med-start-date">`;
        html += '</div>';

        // Sig
        html += '<div class="form-group">';
        html += Components.textInput('docMedSig', '', 'Directions...', false, 'Sig');
        html += '</div>';

        html += '</div></div>'; // prescribe-main, prescribe-body

        html += '<div class="prescribe-footer">';
        html += `<button class="btn btn-outline" data-action="close-document-med" data-testid="btn-cancel-doc-med">Cancel</button>`;
        html += `<button class="btn btn-primary" data-action="submit-document-med" data-testid="btn-submit-doc-med">Save</button>`;
        html += '</div>';

        html += '</div></div>';
        return html;
    },

    // --- Discontinue Modal ---

    renderDiscontinueModal() {
        const med = AppState.discontinueTarget;
        if (!med) return '';
        let html = '<div class="prescribe-overlay" data-testid="discontinue-modal">';
        html += '<div class="prescribe-modal prescribe-modal-sm">';
        html += '<div class="prescribe-header">';
        html += '<h2>Discontinue Medication</h2>';
        html += `<button class="btn-icon" data-action="close-discontinue" data-testid="close-discontinue">${Components.icon('x')}</button>`;
        html += '</div>';
        html += '<div class="prescribe-body"><div class="prescribe-main">';
        html += `<div class="disc-med-name">${Components.escapeHtml(med.medicationName)}</div>`;

        html += '<div class="form-group">';
        html += '<label class="form-label">Reason <span class="required">*</span></label>';
        const reasons = DISCONTINUE_REASONS.map(r => ({ value: r, label: r }));
        html += Components.dropdown('discReason', reasons, '', 'Select reason...');
        html += '</div>';

        html += '<div class="form-group">';
        html += '<label class="form-label">Discontinued By</label>';
        html += `<input type="text" class="form-input" id="discBy" data-testid="disc-by" value="${Components.escapeAttr(AppState.currentUser.name)}">`;
        html += '</div>';

        html += '<div class="form-group">';
        html += Components.textarea('discDetails', '', 'Additional details...', 3, 'Additional Details');
        html += '</div>';

        if (med.pharmacyId) {
            const pharmacy = AppState.getPharmacyById(med.pharmacyId);
            if (pharmacy && pharmacy.acceptsECancel) {
                html += '<div class="form-group">';
                html += Components.checkbox('discSendCancel', false, `Send a cancellation request to ${pharmacy.name}`);
                html += '</div>';
            }
        }

        html += '</div></div>';
        html += '<div class="prescribe-footer">';
        html += `<button class="btn btn-outline" data-action="close-discontinue">Cancel</button>`;
        html += `<button class="btn btn-danger" data-action="submit-discontinue" data-testid="btn-submit-discontinue">Discontinue</button>`;
        html += '</div>';
        html += '</div></div>';
        return html;
    },

    // --- Reconcile Modal ---

    renderReconcileModal() {
        const allActive = AppState.getAllActiveMeds();
        let html = '<div class="prescribe-overlay" data-testid="reconcile-modal">';
        html += '<div class="prescribe-modal prescribe-modal-lg">';
        html += '<div class="prescribe-header">';
        html += '<h2>Medication Reconciliation</h2>';
        html += `<button class="btn-icon" data-action="close-reconcile" data-testid="close-reconcile">${Components.icon('x')}</button>`;
        html += '</div>';
        html += '<div class="prescribe-body"><div class="prescribe-main" style="max-width:100%">';

        if (allActive.length === 0) {
            html += Components.emptyState('', 'No active medications to reconcile');
        } else {
            html += '<table class="reconcile-table">';
            html += '<thead><tr>';
            html += '<th>Medication</th><th>Sig</th><th>Last Filled</th><th>Adherence Note</th><th>Doc D/C</th>';
            html += '</tr></thead><tbody>';
            for (const med of allActive) {
                html += `<tr data-med-id="${Components.escapeAttr(med.id)}" data-testid="reconcile-row-${Components.escapeAttr(med.id)}">`;
                html += `<td class="reconcile-med-name">${Components.escapeHtml(med.medicationName)}</td>`;
                html += `<td>${Components.escapeHtml(med.sig)}</td>`;
                html += `<td>${Components.formatDate(med.lastFilledDate)}</td>`;
                html += `<td><input type="text" class="form-input form-input-sm reconcile-note" data-med-id="${Components.escapeAttr(med.id)}" placeholder="Note..." data-testid="reconcile-note-${Components.escapeAttr(med.id)}"></td>`;
                html += `<td><input type="checkbox" class="reconcile-dc" data-med-id="${Components.escapeAttr(med.id)}" data-testid="reconcile-dc-${Components.escapeAttr(med.id)}"></td>`;
                html += '</tr>';
            }
            html += '</tbody></table>';
        }

        html += '</div></div>';
        html += '<div class="prescribe-footer">';
        html += `<button class="btn btn-outline" data-action="close-reconcile">Cancel</button>`;
        html += `<button class="btn btn-outline" data-action="complete-reconcile-no-changes" data-testid="btn-reconcile-no-changes">Complete Without Changes</button>`;
        html += `<button class="btn btn-primary" data-action="complete-reconcile" data-testid="btn-complete-reconcile">Complete Med Rec</button>`;
        html += '</div>';
        html += '</div></div>';
        return html;
    },

    // --- Bulk Refill Modal ---

    renderBulkRefillModal() {
        const rxMeds = AppState.permanentRxMeds.filter(m => m.status === 'active');
        let html = '<div class="prescribe-overlay" data-testid="bulk-refill-modal">';
        html += '<div class="prescribe-modal prescribe-modal-lg">';
        html += '<div class="prescribe-header">';
        html += '<h2>Bulk Refill</h2>';
        html += `<button class="btn-icon" data-action="close-bulk-refill" data-testid="close-bulk-refill">${Components.icon('x')}</button>`;
        html += '</div>';
        html += '<div class="prescribe-body"><div class="prescribe-main" style="max-width:100%">';

        if (rxMeds.length === 0) {
            html += Components.emptyState('', 'No active prescriptions to refill');
        } else {
            html += '<table class="reconcile-table">';
            html += '<thead><tr>';
            html += '<th><input type="checkbox" id="bulkSelectAll" data-testid="bulk-select-all"></th>';
            html += '<th>Medication</th><th>Sig</th><th>Qty</th><th>Refills Left</th><th>Pharmacy</th>';
            html += '</tr></thead><tbody>';
            for (const med of rxMeds) {
                const checked = AppState.selectedRefillIds.has(med.id) ? ' checked' : '';
                html += `<tr data-testid="bulk-row-${Components.escapeAttr(med.id)}">`;
                html += `<td><input type="checkbox" class="bulk-refill-check" data-med-id="${Components.escapeAttr(med.id)}"${checked} data-testid="bulk-check-${Components.escapeAttr(med.id)}"></td>`;
                html += `<td>${Components.escapeHtml(med.medicationName)}</td>`;
                html += `<td>${Components.escapeHtml(med.sig)}</td>`;
                html += `<td>${med.qty} ${Components.escapeHtml(med.unit || '')}</td>`;
                html += `<td>${med.refillsRemaining != null ? med.refillsRemaining : med.refills}</td>`;
                html += `<td>${Components.escapeHtml(med.pharmacyName || 'N/A')}</td>`;
                html += '</tr>';
            }
            html += '</tbody></table>';
        }

        html += '</div></div>';
        html += '<div class="prescribe-footer">';
        html += `<button class="btn btn-outline" data-action="close-bulk-refill">Cancel</button>`;
        html += `<button class="btn btn-primary" data-action="submit-bulk-refill" data-testid="btn-submit-bulk-refill">Refill Selected</button>`;
        html += '</div>';
        html += '</div></div>';
        return html;
    },

    // --- Med Detail Modal ---

    renderMedDetailModal(med) {
        if (!med) return '';
        let html = '<div class="prescribe-overlay" data-testid="med-detail-modal">';
        html += '<div class="prescribe-modal prescribe-modal-sm">';
        html += '<div class="prescribe-header">';
        html += `<h2>Medication Details</h2>`;
        html += `<button class="btn-icon" data-action="close-med-detail" data-testid="close-med-detail">${Components.icon('x')}</button>`;
        html += '</div>';
        html += '<div class="prescribe-body"><div class="prescribe-main">';

        html += `<div class="detail-field"><span class="detail-label">Medication:</span> ${Components.escapeHtml(med.medicationName)}</div>`;
        html += `<div class="detail-field"><span class="detail-label">Status:</span> ${Components.statusBadge(med.status)}</div>`;
        html += `<div class="detail-field"><span class="detail-label">Sig:</span> ${Components.escapeHtml(med.sig)}</div>`;
        html += `<div class="detail-field"><span class="detail-label">Qty:</span> ${med.qty} ${Components.escapeHtml(med.unit || '')}</div>`;
        if (med.refills != null) html += `<div class="detail-field"><span class="detail-label">Refills:</span> ${med.refillsRemaining != null ? med.refillsRemaining + '/' + med.refills : med.refills}</div>`;
        html += `<div class="detail-field"><span class="detail-label">Days Supply:</span> ${med.daysSupply || 'N/A'}</div>`;
        if (med.ndc) html += `<div class="detail-field"><span class="detail-label">NDC:</span> ${Components.escapeHtml(med.ndc)}</div>`;
        html += `<div class="detail-field"><span class="detail-label">Classification:</span> ${Components.escapeHtml(med.classification)}</div>`;
        if (med.dispenseAsWritten) html += `<div class="detail-field"><span class="detail-label">DAW:</span> Yes</div>`;
        if (med.prescriberName) html += `<div class="detail-field"><span class="detail-label">Prescriber:</span> ${Components.escapeHtml(med.prescriberName)}</div>`;
        if (med.pharmacyName) html += `<div class="detail-field"><span class="detail-label">Pharmacy:</span> ${Components.escapeHtml(med.pharmacyName)}</div>`;
        html += `<div class="detail-field"><span class="detail-label">Start Date:</span> ${Components.formatDate(med.startDate)}</div>`;
        if (med.lastPrescribedDate) html += `<div class="detail-field"><span class="detail-label">Last Prescribed:</span> ${Components.formatDate(med.lastPrescribedDate)}</div>`;
        if (med.lastFilledDate) html += `<div class="detail-field"><span class="detail-label">Last Filled:</span> ${Components.formatDate(med.lastFilledDate)}</div>`;
        if (med.discontinuedDate) {
            html += `<div class="detail-field"><span class="detail-label">Discontinued:</span> ${Components.formatDate(med.discontinuedDate)}</div>`;
            html += `<div class="detail-field"><span class="detail-label">Discontinued By:</span> ${Components.escapeHtml(med.discontinuedBy || '')}</div>`;
            html += `<div class="detail-field"><span class="detail-label">Reason:</span> ${Components.escapeHtml(med.discontinueReason || '')}</div>`;
            if (med.discontinueDetails) html += `<div class="detail-field"><span class="detail-label">Details:</span> ${Components.escapeHtml(med.discontinueDetails)}</div>`;
        }
        if (med.diagnosis && med.diagnosis.length > 0) {
            html += '<div class="detail-field"><span class="detail-label">Diagnosis:</span>';
            for (const dx of med.diagnosis) {
                html += ` <span class="diagnosis-tag">${Components.escapeHtml(dx.code)} - ${Components.escapeHtml(dx.description)}</span>`;
            }
            html += '</div>';
        }
        if (med.isControlled) {
            html += `<div class="detail-field"><span class="detail-label">Controlled:</span> Schedule ${Components.escapeHtml(med.scheduleClass || '')}</div>`;
        }

        html += '</div></div>';
        html += '<div class="prescribe-footer">';
        html += `<button class="btn btn-outline" data-action="close-med-detail">Close</button>`;
        html += '</div>';
        html += '</div></div>';
        return html;
    }
};
