// ============================================================
// app.js — Router, event delegation, initialization
// ============================================================

const App = {

    init() {
        AppState.init();
        AppState.subscribe(() => this.render());

        window.addEventListener('hashchange', () => this.parseRoute());
        document.addEventListener('click', (e) => this.handleClick(e));
        document.addEventListener('change', (e) => this.handleChange(e));
        document.addEventListener('keydown', (e) => this.handleKeydown(e));

        this.parseRoute();
        this._setupSseListener();
        AppState.notify(); // initial push
    },

    // ---- Routing ----
    parseRoute() {
        const hash = window.location.hash || '#/inbox';
        const parts = hash.replace('#/', '').split('/');
        const view = parts[0] || 'inbox';

        AppState.currentEmailId = null;
        AppState.selectedEmailIds = new Set();
        AppState.currentPage = 1;
        AppState.commandPaletteOpen = false;
        AppState.reminderPickerOpen = false;
        AppState.labelPickerOpen = false;
        AppState.movePickerOpen = false;
        AppState.snippetPickerOpen = false;

        if (view === 'email' && parts[1]) {
            AppState.currentView = 'email';
            AppState.currentEmailId = parseInt(parts[1]);
            const email = AppState.getEmail(AppState.currentEmailId);
            if (email && !email.isRead) {
                email.isRead = true;
                AppState._persist();
                AppState._pushStateToServer();
            }
        } else if (view === 'label' && parts[1]) {
            AppState.currentView = 'label';
            AppState.currentLabelId = parts[1];
        } else if (view === 'settings' && parts[1]) {
            AppState.currentView = parts[0];
            AppState.settingsOpen = true;
            AppState.settingsTab = parts[1] || 'general';
        } else {
            AppState.currentView = view;
            if (view === 'inbox') {
                AppState.searchResults = null;
                AppState.searchQuery = '';
            }
        }
        this.render();
    },

    navigate(route) {
        window.location.hash = '#/' + route;
    },

    // ---- Render ----
    render() {
        // Sidebar
        const sidebarNav = document.getElementById('sidebarNav');
        if (sidebarNav) sidebarNav.innerHTML = Views.renderSidebar();

        // Toolbar
        const toolbar = document.getElementById('toolbar');
        if (toolbar) toolbar.innerHTML = Views.renderToolbar();

        // Main content
        const content = document.getElementById('contentWrapper');
        if (content) {
            if (AppState.currentView === 'email' && AppState.currentEmailId) {
                content.innerHTML = Views.renderEmailDetail(AppState.currentEmailId);
            } else if (AppState.calendarView === 'week') {
                content.innerHTML = Views.renderCalendarWeek();
            } else {
                content.innerHTML = Views.renderEmailList();
            }
        }

        // Settings panel
        const settingsPanel = document.getElementById('settingsPanel');
        if (settingsPanel) {
            if (AppState.settingsOpen) {
                settingsPanel.innerHTML = Views.renderSettings();
                settingsPanel.style.display = 'block';
            } else {
                settingsPanel.style.display = 'none';
            }
        }

        // Calendar sidebar
        const calendarSidebar = document.getElementById('calendarSidebar');
        if (calendarSidebar) {
            if (AppState.calendarView === 'day') {
                calendarSidebar.innerHTML = Views.renderCalendarDay();
                calendarSidebar.style.display = 'block';
            } else {
                calendarSidebar.style.display = 'none';
            }
        }

        // Command palette
        const cmdPalette = document.getElementById('commandPaletteContainer');
        if (cmdPalette) {
            if (AppState.commandPaletteOpen) {
                cmdPalette.innerHTML = Views.renderCommandPalette();
                cmdPalette.style.display = 'block';
                setTimeout(() => {
                    const input = document.getElementById('commandInput');
                    if (input) input.focus();
                }, 50);
            } else {
                cmdPalette.style.display = 'none';
            }
        }

        // Reminder picker
        const reminderPicker = document.getElementById('reminderPickerContainer');
        if (reminderPicker) {
            if (AppState.reminderPickerOpen) {
                reminderPicker.innerHTML = Views.renderReminderPicker();
                reminderPicker.style.display = 'block';
            } else {
                reminderPicker.style.display = 'none';
            }
        }

        // Label picker
        const labelPicker = document.getElementById('labelPickerContainer');
        if (labelPicker) {
            if (AppState.labelPickerOpen) {
                labelPicker.innerHTML = Views.renderLabelPicker();
                labelPicker.style.display = 'block';
            } else {
                labelPicker.style.display = 'none';
            }
        }

        // Move picker
        const movePicker = document.getElementById('movePickerContainer');
        if (movePicker) {
            if (AppState.movePickerOpen) {
                movePicker.innerHTML = Views.renderMovePicker();
                movePicker.style.display = 'block';
            } else {
                movePicker.style.display = 'none';
            }
        }

        // Snippet picker
        const snippetPicker = document.getElementById('snippetPickerContainer');
        if (snippetPicker) {
            if (AppState.snippetPickerOpen) {
                snippetPicker.innerHTML = Views.renderSnippetPicker();
                snippetPicker.style.display = 'block';
            } else {
                snippetPicker.style.display = 'none';
            }
        }

        // Compose modal
        const composeModal = document.getElementById('composeModal');
        if (composeModal) {
            if (AppState.composeOpen) {
                const { title, draft } = Views.renderComposeContent();
                document.getElementById('composeTitle').textContent = title;
                const toInput = document.getElementById('composeTo');
                const subjectInput = document.getElementById('composeSubject');
                const bodyInput = document.getElementById('composeBody');
                // Only set values if they're empty (avoid overwriting user typing)
                if (toInput && !toInput.dataset.userEdited) {
                    toInput.value = (draft.to || []).map(t => t.email || t).join(', ');
                }
                if (subjectInput && !subjectInput.dataset.userEdited) {
                    subjectInput.value = draft.subject || '';
                }
                if (bodyInput && !bodyInput.dataset.userEdited) {
                    bodyInput.value = draft.body || '';
                }
                composeModal.style.display = 'flex';
            } else {
                composeModal.style.display = 'none';
                // Reset user-edited flags
                const inputs = composeModal.querySelectorAll('input, textarea');
                inputs.forEach(i => delete i.dataset.userEdited);
            }
        }

        // Search
        const searchInput = document.getElementById('searchInput');
        if (searchInput && AppState.searchQuery && searchInput.value !== AppState.searchQuery) {
            searchInput.value = AppState.searchQuery;
        }

        // Theme
        document.body.className = AppState.settings.theme === 'dark' ? 'theme-dark' : '';

        // Active sidebar highlighting
        document.querySelectorAll('.sidebar-item').forEach(el => {
            el.classList.toggle('active', el.dataset.route === AppState.currentView ||
                (AppState.currentView === 'label' && el.dataset.route === 'label/' + AppState.currentLabelId));
        });

        // User avatar
        const userInitials = document.getElementById('userInitials');
        if (userInitials && AppState.currentUser) {
            userInitials.textContent = AppState.currentUser.name.split(' ').map(w => w[0]).join('');
            userInitials.parentElement.style.background = AppState.currentUser.avatarColor;
        }
    },

    // ---- Event Delegation ----
    handleClick(e) {
        const actionEl = e.target.closest('[data-action]');
        if (!actionEl) {
            // Click outside dropdowns/pickers - close them
            if (!e.target.closest('.dropdown-menu') && !e.target.closest('.dropdown-trigger')) {
                document.querySelectorAll('.dropdown-menu').forEach(m => m.style.display = 'none');
            }
            if (e.target.closest('.command-palette-overlay') && !e.target.closest('.command-palette')) {
                AppState.commandPaletteOpen = false;
                this.render();
            }
            if (e.target.closest('.picker-overlay') && !e.target.closest('.picker-panel')) {
                AppState.reminderPickerOpen = false;
                AppState.labelPickerOpen = false;
                AppState.movePickerOpen = false;
                AppState.snippetPickerOpen = false;
                this.render();
            }
            return;
        }

        e.preventDefault();
        const action = actionEl.dataset.action;

        switch (action) {
            // Navigation
            case 'navigate':
                AppState.settingsOpen = false;
                AppState.calendarView = 'none';
                this.navigate(actionEl.dataset.route);
                break;

            // Email actions
            case 'open-email':
                this.navigate('email/' + actionEl.dataset.emailId);
                break;

            case 'toggle-select': {
                const id = parseInt(actionEl.dataset.emailId);
                if (AppState.selectedEmailIds.has(id)) {
                    AppState.selectedEmailIds.delete(id);
                } else {
                    AppState.selectedEmailIds.add(id);
                }
                this.render();
                break;
            }

            case 'toggle-star':
                AppState.toggleStar(parseInt(actionEl.dataset.emailId));
                break;

            case 'mark-done-single':
                AppState.markDone(parseInt(actionEl.dataset.emailId));
                Components.showToast('Marked as Done', 'success');
                if (AppState.currentView === 'email') this.navigate(AppState.currentView === 'email' ? 'inbox' : AppState.currentView);
                break;

            case 'mark-done-selected':
                AppState.markDone([...AppState.selectedEmailIds]);
                Components.showToast(`${AppState.selectedEmailIds.size || 'Emails'} marked as Done`, 'success');
                break;

            case 'remind-single':
                AppState.reminderPickerOpen = true;
                AppState.reminderPickerEmailId = parseInt(actionEl.dataset.emailId);
                this.render();
                break;

            case 'remind-selected':
                if (AppState.selectedEmailIds.size > 0) {
                    AppState.reminderPickerOpen = true;
                    AppState.reminderPickerEmailId = [...AppState.selectedEmailIds][0];
                    this.render();
                }
                break;

            case 'set-reminder-option': {
                const emailId = AppState.reminderPickerEmailId;
                if (emailId) {
                    // If multiple selected, apply to all
                    if (AppState.selectedEmailIds.size > 0) {
                        [...AppState.selectedEmailIds].forEach(id => AppState.setReminder(id, actionEl.dataset.value));
                    } else {
                        AppState.setReminder(emailId, actionEl.dataset.value);
                    }
                    Components.showToast('Reminder set', 'success');
                }
                AppState.reminderPickerOpen = false;
                if (AppState.currentView === 'email') this.navigate('inbox');
                else this.render();
                break;
            }

            case 'set-custom-reminder': {
                const dateVal = document.getElementById('customReminderDate')?.value;
                const timeVal = document.getElementById('customReminderTime')?.value || '09:00';
                if (dateVal) {
                    const remindAt = new Date(`${dateVal}T${timeVal}:00`).toISOString();
                    const emailId = AppState.reminderPickerEmailId;
                    if (emailId) AppState.setReminder(emailId, remindAt);
                    AppState.reminderPickerOpen = false;
                    Components.showToast('Reminder set', 'success');
                    if (AppState.currentView === 'email') this.navigate('inbox');
                    else this.render();
                }
                break;
            }

            case 'close-reminder-picker':
                AppState.reminderPickerOpen = false;
                this.render();
                break;

            case 'clear-reminder':
                AppState.clearReminder(parseInt(actionEl.dataset.emailId));
                Components.showToast('Reminder cleared', 'info');
                break;

            case 'trash-email':
            case 'trash-selected':
                if (action === 'trash-selected') {
                    AppState.moveToTrash([...AppState.selectedEmailIds]);
                } else {
                    AppState.moveToTrash(parseInt(actionEl.dataset.emailId));
                    if (AppState.currentView === 'email') this.navigate('inbox');
                }
                Components.showToast('Moved to Trash', 'info');
                break;

            case 'star-selected':
                [...AppState.selectedEmailIds].forEach(id => {
                    const email = AppState.getEmail(id);
                    if (email && !email.isStarred) AppState.toggleStar(id);
                });
                AppState.selectedEmailIds = new Set();
                this.render();
                break;

            case 'label-selected':
            case 'label-email':
                AppState.labelPickerOpen = true;
                AppState.labelPickerEmailId = action === 'label-email' ? parseInt(actionEl.dataset.emailId) : [...AppState.selectedEmailIds][0];
                this.render();
                break;

            case 'close-label-picker':
                AppState.labelPickerOpen = false;
                this.render();
                break;

            case 'toggle-email-label': {
                const emailId = parseInt(actionEl.dataset.emailId);
                const labelId = actionEl.dataset.labelId;
                const email = AppState.getEmail(emailId);
                if (email) {
                    if (email.labels.includes(labelId)) {
                        AppState.removeLabel(emailId, labelId);
                    } else {
                        AppState.addLabel(emailId, labelId);
                    }
                }
                break;
            }

            case 'remove-label-chip':
                if (AppState.currentEmailId) {
                    AppState.removeLabel(AppState.currentEmailId, actionEl.dataset.labelId);
                }
                break;

            case 'move-email':
                AppState.movePickerOpen = true;
                AppState.movePickerEmailId = parseInt(actionEl.dataset.emailId);
                this.render();
                break;

            case 'close-move-picker':
                AppState.movePickerOpen = false;
                this.render();
                break;

            case 'move-to-folder':
                if (AppState.movePickerEmailId) {
                    AppState.moveToFolder(AppState.movePickerEmailId, actionEl.dataset.folder);
                    Components.showToast('Moved', 'success');
                }
                AppState.movePickerOpen = false;
                if (AppState.currentView === 'email') this.navigate('inbox');
                else this.render();
                break;

            case 'unsubscribe-email':
                AppState.unsubscribe(parseInt(actionEl.dataset.emailId));
                Components.showToast('Unsubscribed', 'success');
                if (AppState.currentView === 'email') this.navigate('inbox');
                break;

            case 'mark-read-selected':
                AppState.markAsRead([...AppState.selectedEmailIds]);
                AppState.selectedEmailIds = new Set();
                this.render();
                break;

            case 'mark-unread-selected':
                AppState.markAsUnread([...AppState.selectedEmailIds]);
                AppState.selectedEmailIds = new Set();
                this.render();
                break;

            // Reply/Forward
            case 'reply-email':
                this._openReply(parseInt(actionEl.dataset.emailId), 'reply');
                break;
            case 'reply-all-email':
                this._openReply(parseInt(actionEl.dataset.emailId), 'reply-all');
                break;
            case 'forward-email':
                this._openReply(parseInt(actionEl.dataset.emailId), 'forward');
                break;

            case 'instant-reply': {
                const emailId = parseInt(actionEl.dataset.emailId);
                const replyType = actionEl.dataset.replyType;
                const replies = {
                    'thanks': 'Thanks for sending this over! I\'ll take a look.',
                    'sounds-good': 'Sounds good, let\'s do it.',
                    'will-review': 'I\'ll review and get back to you shortly.'
                };
                const email = AppState.getEmail(emailId);
                if (email) {
                    AppState.sendEmail({
                        to: [email.from],
                        subject: 'Re: ' + email.subject,
                        body: replies[replyType] + '\n\n' + (AppState.settings.signature || '')
                    });
                    Components.showToast('Reply sent', 'success');
                }
                break;
            }

            // Compose
            case 'compose':
                AppState.composeOpen = true;
                AppState.composeDraft = { to: [], cc: [], subject: '', body: '' };
                AppState.replyMode = null;
                this.render();
                break;

            case 'close-compose':
                AppState.composeOpen = false;
                AppState.composeDraft = null;
                AppState.replyMode = null;
                this.render();
                break;

            case 'minimize-compose':
                AppState.composeOpen = false;
                this.render();
                break;

            case 'send-email': {
                const to = document.getElementById('composeTo')?.value || '';
                const cc = document.getElementById('composeCc')?.value || '';
                const subject = document.getElementById('composeSubject')?.value || '';
                const body = document.getElementById('composeBody')?.value || '';
                if (!to.trim()) {
                    Components.showToast('Please add a recipient', 'error');
                    break;
                }
                const toList = to.split(',').map(e => e.trim()).filter(Boolean).map(e => {
                    const contact = AppState.contacts.find(c => c.email === e || c.name === e);
                    return contact ? { name: contact.name, email: contact.email } : { name: e, email: e };
                });
                const ccList = cc ? cc.split(',').map(e => e.trim()).filter(Boolean).map(e => {
                    const contact = AppState.contacts.find(c => c.email === e || c.name === e);
                    return contact ? { name: contact.name, email: contact.email } : { name: e, email: e };
                }) : [];
                AppState.sendEmail({ to: toList, cc: ccList, subject, body });
                AppState.composeOpen = false;
                AppState.composeDraft = null;
                AppState.replyMode = null;
                Components.showToast('Email sent', 'success');
                break;
            }

            case 'discard-draft':
                AppState.composeOpen = false;
                AppState.composeDraft = null;
                AppState.replyMode = null;
                Components.showToast('Draft discarded', 'info');
                this.render();
                break;

            case 'show-cc':
                document.getElementById('composeCcField').style.display = 'flex';
                break;
            case 'show-bcc':
                document.getElementById('composeBccField').style.display = 'flex';
                break;

            // Snippet picker
            case 'open-snippet-picker':
                AppState.snippetPickerOpen = true;
                this.render();
                break;
            case 'close-snippet-picker':
                AppState.snippetPickerOpen = false;
                this.render();
                break;
            case 'insert-snippet': {
                const snippet = AppState.snippets.find(s => s.id === actionEl.dataset.snippetId);
                if (snippet) {
                    const bodyInput = document.getElementById('composeBody');
                    if (bodyInput) {
                        bodyInput.value += snippet.body;
                        bodyInput.dataset.userEdited = 'true';
                    }
                }
                AppState.snippetPickerOpen = false;
                this.render();
                break;
            }

            // Snippets CRUD
            case 'create-snippet':
                Components.showModal('Create Snippet', `
                    <div class="modal-form">
                        ${Components.textInput('snippet-name', '', 'Snippet name', 'Name')}
                        <div class="input-wrapper">
                            <label class="input-label">Body</label>
                            <textarea id="snippet-body" class="text-input snippet-body-input" placeholder="Type your snippet..." rows="6"></textarea>
                        </div>
                        <label class="checkbox-row">
                            <input type="checkbox" id="snippet-shared">
                            <span>Share with team</span>
                        </label>
                    </div>
                `, [
                    { action: 'close-modal', label: 'Cancel' },
                    { action: 'save-new-snippet', label: 'Create', primary: true }
                ]);
                break;

            case 'save-new-snippet': {
                const name = document.getElementById('snippet-name')?.value;
                const body = document.getElementById('snippet-body')?.value;
                const isShared = document.getElementById('snippet-shared')?.checked;
                if (name && body) {
                    const vars = (body.match(/\{(\w+)\}/g) || []).map(v => v.slice(1, -1));
                    AppState.createSnippet({ name, body, variables: vars, isShared });
                    Components.closeModal();
                    Components.showToast('Snippet created', 'success');
                }
                break;
            }

            case 'edit-snippet': {
                const snippet = AppState.snippets.find(s => s.id === actionEl.dataset.snippetId);
                if (snippet) {
                    Components.showModal('Edit Snippet', `
                        <div class="modal-form">
                            ${Components.textInput('edit-snippet-name', snippet.name, 'Snippet name', 'Name')}
                            <div class="input-wrapper">
                                <label class="input-label">Body</label>
                                <textarea id="edit-snippet-body" class="text-input snippet-body-input" rows="6">${Components.escapeHtml(snippet.body)}</textarea>
                            </div>
                            <label class="checkbox-row">
                                <input type="checkbox" id="edit-snippet-shared" ${snippet.isShared ? 'checked' : ''}>
                                <span>Share with team</span>
                            </label>
                            <input type="hidden" id="edit-snippet-id" value="${snippet.id}">
                        </div>
                    `, [
                        { action: 'close-modal', label: 'Cancel' },
                        { action: 'save-edit-snippet', label: 'Save', primary: true }
                    ]);
                }
                break;
            }

            case 'save-edit-snippet': {
                const id = document.getElementById('edit-snippet-id')?.value;
                const name = document.getElementById('edit-snippet-name')?.value;
                const body = document.getElementById('edit-snippet-body')?.value;
                const isShared = document.getElementById('edit-snippet-shared')?.checked;
                if (id && name && body) {
                    const vars = (body.match(/\{(\w+)\}/g) || []).map(v => v.slice(1, -1));
                    AppState.updateSnippet(id, { name, body, variables: vars, isShared });
                    Components.closeModal();
                    Components.showToast('Snippet updated', 'success');
                }
                break;
            }

            case 'delete-snippet':
                AppState.deleteSnippet(actionEl.dataset.snippetId);
                Components.showToast('Snippet deleted', 'info');
                break;

            case 'toggle-snippet-share':
                AppState.toggleSnippetSharing(actionEl.dataset.snippetId);
                break;

            // Split tabs
            case 'switch-split':
                AppState.currentSplit = actionEl.dataset.splitId;
                AppState.currentPage = 1;
                AppState.selectedEmailIds = new Set();
                this.render();
                break;

            // Pagination
            case 'prev-page':
                if (AppState.currentPage > 1) { AppState.currentPage--; this.render(); }
                break;
            case 'next-page':
                AppState.currentPage++;
                this.render();
                break;

            case 'back-to-list':
                this.navigate(AppState.currentView === 'email' ? 'inbox' : AppState.currentView);
                break;

            // Settings
            case 'open-settings':
                AppState.settingsOpen = true;
                AppState.settingsTab = 'general';
                this.render();
                break;
            case 'close-settings':
                AppState.settingsOpen = false;
                this.render();
                break;
            case 'settings-tab':
                AppState.settingsTab = actionEl.dataset.tab;
                this.render();
                break;

            case 'save-signature': {
                const sigVal = document.getElementById('signature-input')?.value;
                AppState.updateSetting('signature', sigVal || '');
                Components.showToast('Signature saved', 'success');
                break;
            }

            // Calendar
            case 'toggle-calendar':
                AppState.calendarView = AppState.calendarView === 'day' ? 'none' : 'day';
                if (AppState.calendarView === 'day') {
                    AppState.calendarSelectedDate = new Date().toISOString().split('T')[0];
                }
                this.render();
                break;

            case 'calendar-prev-day':
            case 'calendar-next-day': {
                const current = new Date((AppState.calendarSelectedDate || new Date().toISOString().split('T')[0]) + 'T12:00:00');
                current.setDate(current.getDate() + (action === 'calendar-next-day' ? 1 : -1));
                AppState.calendarSelectedDate = current.toISOString().split('T')[0];
                this.render();
                break;
            }

            case 'calendar-prev-week':
            case 'calendar-next-week': {
                const curr = new Date((AppState.calendarSelectedDate || new Date().toISOString().split('T')[0]) + 'T12:00:00');
                curr.setDate(curr.getDate() + (action === 'calendar-next-week' ? 7 : -7));
                AppState.calendarSelectedDate = curr.toISOString().split('T')[0];
                this.render();
                break;
            }

            case 'calendar-today':
                AppState.calendarSelectedDate = new Date().toISOString().split('T')[0];
                this.render();
                break;

            case 'show-week-view':
                AppState.calendarView = 'week';
                AppState.calendarSelectedDate = AppState.calendarSelectedDate || new Date().toISOString().split('T')[0];
                this.render();
                break;

            case 'show-day-view':
                AppState.calendarView = 'day';
                this.render();
                break;

            // Create event
            case 'create-event':
                Components.showModal('Create Event', `
                    <div class="modal-form">
                        ${Components.textInput('event-title', '', 'Event title', 'Title')}
                        ${Components.textInput('event-date', AppState.calendarSelectedDate || new Date().toISOString().split('T')[0], 'YYYY-MM-DD', 'Date')}
                        ${Components.textInput('event-start', '09:00', 'HH:MM', 'Start Time')}
                        ${Components.textInput('event-end', '10:00', 'HH:MM', 'End Time')}
                        ${Components.textInput('event-location', '', 'Location or meeting link', 'Location')}
                        <div class="input-wrapper">
                            <label class="input-label">Description</label>
                            <textarea id="event-description" class="text-input" rows="3" placeholder="Add details..."></textarea>
                        </div>
                        ${Components.textInput('event-attendees', '', 'email1@example.com, email2@example.com', 'Attendees')}
                    </div>
                `, [
                    { action: 'close-modal', label: 'Cancel' },
                    { action: 'save-new-event', label: 'Create', primary: true }
                ]);
                break;

            case 'save-new-event': {
                const title = document.getElementById('event-title')?.value;
                const date = document.getElementById('event-date')?.value;
                const startTime = document.getElementById('event-start')?.value;
                const endTime = document.getElementById('event-end')?.value;
                const location = document.getElementById('event-location')?.value;
                const description = document.getElementById('event-description')?.value;
                const attendees = (document.getElementById('event-attendees')?.value || '').split(',').map(e => e.trim()).filter(Boolean);
                if (title && date) {
                    AppState.createEvent({ title, date, startTime, endTime, location, description, attendees });
                    Components.closeModal();
                    Components.showToast('Event created', 'success');
                }
                break;
            }

            // Labels CRUD
            case 'create-label':
                Components.showModal('Create Label', `
                    <div class="modal-form">
                        ${Components.textInput('label-name', '', 'Label name', 'Name')}
                        <div class="input-wrapper">
                            <label class="input-label">Color</label>
                            ${Components.colorPalette('#6C4FF7')}
                            <input type="hidden" id="label-color" value="#6C4FF7">
                        </div>
                    </div>
                `, [
                    { action: 'close-modal', label: 'Cancel' },
                    { action: 'save-new-label', label: 'Create', primary: true }
                ]);
                break;

            case 'save-new-label': {
                const name = document.getElementById('label-name')?.value;
                const color = document.getElementById('label-color')?.value;
                if (name) {
                    AppState.createLabel(name, color);
                    Components.closeModal();
                    Components.showToast('Label created', 'success');
                }
                break;
            }

            case 'select-color': {
                const color = actionEl.dataset.color;
                document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
                actionEl.classList.add('selected');
                const colorInput = document.getElementById('label-color') || document.getElementById('edit-label-color');
                if (colorInput) colorInput.value = color;
                break;
            }

            // Auto Labels
            case 'create-auto-label':
                Components.showModal('Create Auto Label', `
                    <div class="modal-form">
                        ${Components.textInput('al-name', '', 'Label name', 'Name')}
                        ${Components.textInput('al-from', '', 'e.g., @company.com', 'From (optional)')}
                        ${Components.textInput('al-subject', '', 'Keywords', 'Subject contains (optional)')}
                        <div class="input-wrapper">
                            <label class="input-label">AI description (optional)</label>
                            <textarea id="al-ai" class="text-input" rows="2" placeholder="Describe the type of emails..."></textarea>
                        </div>
                    </div>
                `, [
                    { action: 'close-modal', label: 'Cancel' },
                    { action: 'save-new-auto-label', label: 'Create', primary: true }
                ]);
                break;

            case 'save-new-auto-label': {
                const name = document.getElementById('al-name')?.value;
                const from = document.getElementById('al-from')?.value;
                const subject = document.getElementById('al-subject')?.value;
                const ai = document.getElementById('al-ai')?.value;
                if (name) {
                    const criteria = {};
                    if (from) criteria.from = from;
                    if (subject) criteria.subject = subject;
                    if (ai) criteria.ai = ai;
                    AppState.createAutoLabel(name, criteria, 'custom');
                    Components.closeModal();
                    Components.showToast('Auto Label created', 'success');
                }
                break;
            }

            case 'delete-auto-label':
                AppState.deleteAutoLabel(actionEl.dataset.autoLabelId);
                Components.showToast('Auto Label deleted', 'info');
                break;

            // Splits
            case 'create-split':
                Components.showModal('Create Split', `
                    <div class="modal-form">
                        ${Components.textInput('split-name', '', 'Split name', 'Name')}
                        ${Components.dropdown('split-criteria-type', [
                            { value: 'autoLabel', label: 'Based on Auto Label' },
                            { value: 'from', label: 'Based on sender' }
                        ], 'autoLabel', 'Criteria type')}
                        ${Components.textInput('split-criteria-value', '', 'Auto Label name or sender pattern', 'Value')}
                    </div>
                `, [
                    { action: 'close-modal', label: 'Cancel' },
                    { action: 'save-new-split', label: 'Create', primary: true }
                ]);
                break;

            case 'save-new-split': {
                const name = document.getElementById('split-name')?.value;
                const criteriaValue = document.getElementById('split-criteria-value')?.value;
                if (name) {
                    AppState.createSplit(name, { autoLabel: criteriaValue });
                    Components.closeModal();
                    Components.showToast('Split created', 'success');
                }
                break;
            }

            case 'delete-split':
                AppState.deleteSplit(actionEl.dataset.splitId);
                Components.showToast('Split removed', 'info');
                break;

            // Booking pages
            case 'create-booking-page':
                Components.showModal('Create Booking Page', `
                    <div class="modal-form">
                        ${Components.textInput('bp-title', '', 'e.g., Coffee Chat', 'Title')}
                        ${Components.dropdown('bp-duration', [
                            { value: '15', label: '15 minutes' },
                            { value: '30', label: '30 minutes' },
                            { value: '45', label: '45 minutes' },
                            { value: '60', label: '60 minutes' }
                        ], '30', 'Duration')}
                        ${Components.dropdown('bp-location', [
                            { value: 'Zoom', label: 'Zoom' },
                            { value: 'Google Meet', label: 'Google Meet' },
                            { value: 'Phone', label: 'Phone' },
                            { value: 'In-person', label: 'In-person' }
                        ], 'Zoom', 'Location')}
                        <div class="input-wrapper">
                            <label class="input-label">Description</label>
                            <textarea id="bp-description" class="text-input" rows="2" placeholder="What's this meeting about?"></textarea>
                        </div>
                    </div>
                `, [
                    { action: 'close-modal', label: 'Cancel' },
                    { action: 'save-new-booking-page', label: 'Create', primary: true }
                ]);
                break;

            case 'save-new-booking-page': {
                const title = document.getElementById('bp-title')?.value;
                const durationEl = document.getElementById('bp-duration');
                const locationEl = document.getElementById('bp-location');
                const description = document.getElementById('bp-description')?.value;
                if (title) {
                    AppState.createBookingPage({
                        title,
                        duration: parseInt(durationEl?.dataset?.value || '30'),
                        location: locationEl?.dataset?.value || 'Zoom',
                        description
                    });
                    Components.closeModal();
                    Components.showToast('Booking page created', 'success');
                }
                break;
            }

            case 'toggle-booking-page':
                AppState.toggleBookingPage(actionEl.dataset.bpId);
                break;

            case 'delete-booking-page':
                AppState.deleteBookingPage(actionEl.dataset.bpId);
                Components.showToast('Booking page deleted', 'info');
                break;

            // Command palette
            case 'open-command-palette':
                AppState.commandPaletteOpen = true;
                this.render();
                break;

            case 'cmd-compose':
                AppState.commandPaletteOpen = false;
                AppState.composeOpen = true;
                AppState.composeDraft = { to: [], cc: [], subject: '', body: '' };
                AppState.replyMode = null;
                this.render();
                break;

            case 'cmd-search':
                AppState.commandPaletteOpen = false;
                this.render();
                setTimeout(() => document.getElementById('searchInput')?.focus(), 50);
                break;

            case 'cmd-goto-inbox':
                AppState.commandPaletteOpen = false;
                AppState.settingsOpen = false;
                this.navigate('inbox');
                break;
            case 'cmd-goto-done':
                AppState.commandPaletteOpen = false;
                AppState.settingsOpen = false;
                this.navigate('done');
                break;
            case 'cmd-goto-reminders':
                AppState.commandPaletteOpen = false;
                AppState.settingsOpen = false;
                this.navigate('reminders');
                break;
            case 'cmd-goto-sent':
                AppState.commandPaletteOpen = false;
                AppState.settingsOpen = false;
                this.navigate('sent');
                break;
            case 'cmd-goto-snippets':
                AppState.commandPaletteOpen = false;
                AppState.settingsOpen = false;
                this.navigate('snippets');
                break;
            case 'cmd-goto-opens':
                AppState.commandPaletteOpen = false;
                AppState.settingsOpen = false;
                this.navigate('opens');
                break;
            case 'cmd-calendar-day':
                AppState.commandPaletteOpen = false;
                AppState.calendarView = 'day';
                AppState.calendarSelectedDate = new Date().toISOString().split('T')[0];
                this.render();
                break;
            case 'cmd-calendar-week':
                AppState.commandPaletteOpen = false;
                AppState.calendarView = 'week';
                AppState.calendarSelectedDate = new Date().toISOString().split('T')[0];
                this.render();
                break;
            case 'cmd-settings':
                AppState.commandPaletteOpen = false;
                AppState.settingsOpen = true;
                AppState.settingsTab = 'general';
                this.render();
                break;
            case 'cmd-create-event':
                AppState.commandPaletteOpen = false;
                // Trigger create event action
                this.handleClick({ target: document.createElement('div'), preventDefault: () => {} });
                document.querySelector('[data-action="create-event"]')?.click();
                break;
            case 'cmd-create-snippet':
                AppState.commandPaletteOpen = false;
                this.navigate('snippets');
                break;
            case 'cmd-get-me-to-zero': {
                AppState.commandPaletteOpen = false;
                const oldEmails = AppState.getInboxEmails().filter(e => {
                    const age = Date.now() - new Date(e.date).getTime();
                    return age > 7 * 86400000; // older than 7 days
                });
                if (oldEmails.length > 0) {
                    AppState.markDone(oldEmails.map(e => e.id));
                    Components.showToast(`Archived ${oldEmails.length} old emails`, 'success');
                } else {
                    Components.showToast('No old emails to archive', 'info');
                }
                break;
            }

            // Dropdown
            case 'toggle-dropdown': {
                const menu = document.getElementById(actionEl.dataset.dropdownId + '-menu');
                if (menu) {
                    const isVisible = menu.style.display !== 'none';
                    document.querySelectorAll('.dropdown-menu').forEach(m => m.style.display = 'none');
                    menu.style.display = isVisible ? 'none' : 'block';
                }
                break;
            }
            case 'select-dropdown': {
                const dropdownId = actionEl.dataset.dropdownId;
                const value = actionEl.dataset.value;
                const dropdown = document.getElementById(dropdownId);
                if (dropdown) {
                    dropdown.dataset.value = value;
                    const trigger = dropdown.querySelector('.dropdown-value');
                    if (trigger) trigger.textContent = actionEl.textContent;
                }
                const menu = document.getElementById(dropdownId + '-menu');
                if (menu) menu.style.display = 'none';
                // Handle specific dropdown changes
                this._handleDropdownChange(dropdownId, value);
                break;
            }

            // Modal
            case 'close-modal':
                Components.closeModal();
                break;

            default:
                console.warn('Unhandled action:', action);
        }
    },

    handleChange(e) {
        const el = e.target;

        // Toggle switches
        if (el.type === 'checkbox' && el.closest('.toggle-switch')) {
            const name = el.name || el.id;
            this._handleToggleChange(name, el.checked);
        }

        // Auto archive label checkboxes
        if (el.dataset.action === 'toggle-auto-archive-label') {
            const labelId = el.dataset.labelId;
            const aa = AppState.settings.autoArchive;
            if (el.checked) {
                if (!aa.labels.includes(labelId)) aa.labels.push(labelId);
            } else {
                aa.labels = aa.labels.filter(l => l !== labelId);
            }
            AppState.notify();
        }

        // Radio groups
        if (el.type === 'radio') {
            this._handleRadioChange(el.name, el.value);
        }

        // Mark compose inputs as user-edited
        if (el.closest('.compose-modal')) {
            el.dataset.userEdited = 'true';
        }
    },

    _handleToggleChange(name, checked) {
        const settingsMap = {
            'notifications-desktop': 'notifications.desktop',
            'notifications-sound': 'notifications.sound',
            'instant-reply': 'instantReply.enabled',
            'smart-send': 'smartSend.enabled',
            'ask-ai': 'askAi.enabled',
            'read-receipts-enabled': 'readReceipts.enabled',
            'read-receipts-team': 'readReceipts.teamSharing',
            'auto-reminders-enabled': 'autoReminders.enabled',
            'auto-drafts-enabled': 'autoDrafts.enabled',
            'auto-drafts-cc': 'autoDrafts.ccTeammate',
            'calendar-alerts': 'notifications.calendarAlerts',
            'meeting-auto-add': 'meetingLink.autoAdd',
            'shortcuts-enabled': 'keyboard.shortcuts',
            'auto-archive-enabled': 'autoArchive.enabled'
        };

        if (settingsMap[name]) {
            AppState.updateSetting(settingsMap[name], checked);
            return;
        }

        // Auto label toggles
        if (name.startsWith('al-')) {
            const alId = name.substring(3);
            AppState.toggleAutoLabel(alId);
        }
    },

    _handleRadioChange(name, value) {
        switch (name) {
            case 'auto-reminder-mode':
                AppState.updateSetting('autoReminders.mode', value);
                break;
            case 'auto-draft-type':
                AppState.updateSetting('autoDrafts.type', value);
                break;
        }
    },

    _handleDropdownChange(dropdownId, value) {
        const settingsMap = {
            'theme': 'theme',
            'swipe-left': 'swipeLeft',
            'swipe-right': 'swipeRight',
            'auto-reminder-time': 'autoReminders.defaultTime',
            'alert-minutes': 'notifications.alertMinutes',
            'meeting-provider': 'meetingLink.provider',
            'timezone': 'timezone',
            'secondary-timezone': 'secondaryTimezone'
        };

        if (settingsMap[dropdownId]) {
            let val = value;
            if (dropdownId === 'alert-minutes') val = parseInt(value);
            AppState.updateSetting(settingsMap[dropdownId], val);
        }
    },

    _openReply(emailId, mode) {
        const email = AppState.getEmail(emailId);
        if (!email) return;

        let to = [email.from];
        let cc = [];
        let subject = email.subject;
        let body = '';

        if (mode === 'reply-all') {
            to = [email.from, ...email.to.filter(t => t.email !== AppState.currentUser.email)];
            cc = email.cc || [];
        }
        if (mode === 'forward') {
            to = [];
            subject = 'Fwd: ' + email.subject;
            body = `\n\n---------- Forwarded message ----------\nFrom: ${email.from.name} <${email.from.email}>\nDate: ${Components.formatFullDate(email.date)}\nSubject: ${email.subject}\n\n${email.body || email.snippet}`;
        } else {
            subject = subject.startsWith('Re: ') ? subject : 'Re: ' + subject;
            body = '\n\n' + (AppState.settings.signature || '');
        }

        AppState.composeOpen = true;
        AppState.composeDraft = { to, cc, subject, body };
        AppState.replyMode = mode;
        this.render();
    },

    // ---- Keyboard Shortcuts ----
    handleKeydown(e) {
        if (!AppState.settings.keyboard?.shortcuts) return;

        // Don't handle shortcuts when typing in inputs
        const tag = e.target.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') {
            // Search submit on Enter
            if (tag === 'INPUT' && e.target.id === 'searchInput' && e.key === 'Enter') {
                e.preventDefault();
                AppState.searchQuery = e.target.value;
                AppState.searchEmails(e.target.value);
                AppState.currentView = 'search';
                this.render();
            }
            // Command palette search
            if (tag === 'INPUT' && e.target.id === 'commandInput') {
                if (e.key === 'Escape') {
                    AppState.commandPaletteOpen = false;
                    this.render();
                }
                // Filter commands on input
                const query = e.target.value.toLowerCase();
                setTimeout(() => {
                    const results = document.getElementById('commandResults');
                    if (results) {
                        const items = results.querySelectorAll('.command-item');
                        items.forEach(item => {
                            const label = item.querySelector('.command-label')?.textContent.toLowerCase() || '';
                            item.style.display = label.includes(query) ? 'flex' : 'none';
                        });
                    }
                }, 10);
            }
            // Send on Cmd+Enter
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter' && AppState.composeOpen) {
                e.preventDefault();
                document.querySelector('[data-action="send-email"]')?.click();
            }
            return;
        }

        // Escape closes overlays
        if (e.key === 'Escape') {
            if (AppState.commandPaletteOpen) { AppState.commandPaletteOpen = false; this.render(); return; }
            if (AppState.reminderPickerOpen) { AppState.reminderPickerOpen = false; this.render(); return; }
            if (AppState.labelPickerOpen) { AppState.labelPickerOpen = false; this.render(); return; }
            if (AppState.movePickerOpen) { AppState.movePickerOpen = false; this.render(); return; }
            if (AppState.composeOpen) { AppState.composeOpen = false; this.render(); return; }
            if (AppState.settingsOpen) { AppState.settingsOpen = false; this.render(); return; }
            if (AppState.currentView === 'email') { this.navigate('inbox'); return; }
        }

        // Cmd+K - Command palette
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            AppState.commandPaletteOpen = !AppState.commandPaletteOpen;
            this.render();
            return;
        }

        // Cmd+U - Unsubscribe
        if ((e.metaKey || e.ctrlKey) && e.key === 'u') {
            if (AppState.currentEmailId) {
                e.preventDefault();
                AppState.unsubscribe(AppState.currentEmailId);
                Components.showToast('Unsubscribed', 'success');
                this.navigate('inbox');
            }
            return;
        }

        // / - Search
        if (e.key === '/') {
            e.preventDefault();
            document.getElementById('searchInput')?.focus();
            return;
        }

        // c - Compose
        if (e.key === 'c') {
            AppState.composeOpen = true;
            AppState.composeDraft = { to: [], cc: [], subject: '', body: '' };
            AppState.replyMode = null;
            this.render();
            return;
        }

        // e - Mark Done
        if (e.key === 'e' || e.key === 'E') {
            if (AppState.currentEmailId) {
                AppState.markDone(AppState.currentEmailId);
                Components.showToast('Marked as Done', 'success');
                this.navigate('inbox');
            } else if (AppState.selectedEmailIds.size > 0) {
                AppState.markDone([...AppState.selectedEmailIds]);
                Components.showToast('Marked as Done', 'success');
            }
            return;
        }

        // h - Remind Me
        if (e.key === 'h' || e.key === 'H') {
            const emailId = AppState.currentEmailId || (AppState.selectedEmailIds.size > 0 ? [...AppState.selectedEmailIds][0] : null);
            if (emailId) {
                AppState.reminderPickerOpen = true;
                AppState.reminderPickerEmailId = emailId;
                this.render();
            }
            return;
        }

        // r - Reply
        if (e.key === 'r') {
            if (AppState.currentEmailId) {
                this._openReply(AppState.currentEmailId, 'reply');
            }
            return;
        }

        // Enter - Reply All
        if (e.key === 'Enter' && AppState.currentView === 'email') {
            if (AppState.currentEmailId) {
                this._openReply(AppState.currentEmailId, 'reply-all');
            }
            return;
        }

        // f - Forward
        if (e.key === 'f') {
            if (AppState.currentEmailId) {
                this._openReply(AppState.currentEmailId, 'forward');
            }
            return;
        }

        // v - Move
        if (e.key === 'v') {
            const emailId = AppState.currentEmailId || (AppState.selectedEmailIds.size > 0 ? [...AppState.selectedEmailIds][0] : null);
            if (emailId) {
                AppState.movePickerOpen = true;
                AppState.movePickerEmailId = emailId;
                this.render();
            }
            return;
        }

        // ; - Snippet picker
        if (e.key === ';' && AppState.composeOpen) {
            AppState.snippetPickerOpen = true;
            this.render();
            return;
        }

        // 0 - Calendar day view
        if (e.key === '0') {
            AppState.calendarView = AppState.calendarView === 'day' ? 'none' : 'day';
            AppState.calendarSelectedDate = new Date().toISOString().split('T')[0];
            this.render();
            return;
        }

        // 2 - Calendar week view
        if (e.key === '2') {
            AppState.calendarView = AppState.calendarView === 'week' ? 'none' : 'week';
            AppState.calendarSelectedDate = new Date().toISOString().split('T')[0];
            this.render();
            return;
        }

        // Tab / Shift+Tab - Navigate splits
        if (e.key === 'Tab' && AppState.currentView === 'inbox') {
            e.preventDefault();
            const splits = AppState.splits.sort((a, b) => a.position - b.position);
            const currentIdx = splits.findIndex(s => s.id === AppState.currentSplit);
            let nextIdx;
            if (e.shiftKey) {
                nextIdx = currentIdx <= 0 ? splits.length - 1 : currentIdx - 1;
            } else {
                nextIdx = currentIdx >= splits.length - 1 ? 0 : currentIdx + 1;
            }
            AppState.currentSplit = splits[nextIdx].id;
            AppState.currentPage = 1;
            this.render();
            return;
        }

        // b - Create event
        if (e.key === 'b') {
            document.querySelector('[data-action="create-event"]')?.click();
            return;
        }

        // ? - Ask AI (show command palette with AI focus)
        if (e.key === '?') {
            AppState.commandPaletteOpen = true;
            this.render();
            return;
        }

        // Cmd+A - Select all
        if ((e.metaKey || e.ctrlKey) && e.key === 'a') {
            e.preventDefault();
            const emails = Views._getEmailsForView();
            AppState.selectedEmailIds = new Set(emails.map(e => e.id));
            this.render();
            return;
        }
    },

    // ---- SSE ----
    _setupSseListener() {
        const es = new EventSource('/api/events');
        es.onmessage = (e) => {
            if (e.data === 'reset') {
                AppState.resetToSeedData();
                AppState.notify();
                this.navigate('inbox');
            }
        };
        es.onerror = () => {
            setTimeout(() => this._setupSseListener(), 5000);
            es.close();
        };
    }
};

// ---- Initialize on DOM ready ----
document.addEventListener('DOMContentLoaded', () => App.init());
