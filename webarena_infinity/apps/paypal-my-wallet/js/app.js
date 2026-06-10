// ============================================================
// app.js — Event handlers and initialization for PayPal My Wallet
// ============================================================

const App = {

    init() {
        AppState.init();
        AppState.subscribe(() => Views.render());
        this._setupEventListeners();
        this._setupSSE();
        Views.render();
        AppState._pushStateToServer();
    },

    // ---- Event Delegation ----
    _setupEventListeners() {
        document.addEventListener('click', (e) => {
            const target = e.target.closest('[data-action]');
            if (target) {
                e.preventDefault();
                this._handleAction(target.dataset.action, target);
            }
            // Close dropdowns on outside click
            if (!e.target.closest('.custom-dropdown')) {
                document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
            }
        });

        document.addEventListener('input', (e) => {
            if (e.target.id === 'transaction-search') {
                AppState.searchQuery = e.target.value;
                AppState.currentPage = 1;
                AppState.notify();
            }
        });

        document.addEventListener('change', (e) => {
            if (e.target.dataset.action === 'set-autopay-amount') {
                AppState.setAutopayAmount(e.target.value);
            }
            if (e.target.dataset.action === 'set-currency-conversion') {
                AppState.updatePreference('currencyConversionOption', e.target.value);
            }
        });
    },

    _handleAction(action, target) {
        switch (action) {
            // Navigation
            case 'navigate':
                AppState.currentView = target.dataset.view;
                AppState.currentSubView = null;
                AppState.currentPage = 1;
                AppState.searchQuery = '';
                Views.render();
                window.scrollTo(0, 0);
                break;

            // Tab switching
            case 'switch-tab':
                const tab = target.dataset.tab;
                if (AppState.currentView === 'transactions') {
                    AppState.transactionFilter = tab;
                    AppState.currentPage = 1;
                } else if (AppState.currentView === 'offers') {
                    AppState.offerFilter = tab;
                }
                Views.render();
                break;

            // Pagination
            case 'go-to-page':
                AppState.currentPage = parseInt(target.dataset.page);
                Views.render();
                window.scrollTo(0, 0);
                break;

            // Dropdown
            case 'toggle-dropdown':
                Components.toggleDropdown(target.dataset.dropdownId);
                break;
            case 'select-dropdown-item':
                this._handleDropdownSelect(target.dataset.dropdownId, target.dataset.value);
                document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
                break;

            // Toggle Switch
            case 'toggle-switch':
                this._handleToggle(target.dataset.toggleName);
                break;

            // Modal
            case 'close-modal':
                Components.closeModal();
                break;
            case 'confirm-dialog':
                if (AppState._confirmCallback) {
                    AppState._confirmCallback();
                    AppState._confirmCallback = null;
                }
                Components.closeModal();
                break;

            // Cards
            case 'open-add-card-modal':
                this._openAddCardModal();
                break;
            case 'open-edit-card-modal':
                this._openEditCardModal(target.dataset.id);
                break;
            case 'confirm-card':
                this._confirmCard(target.dataset.id);
                break;
            case 'set-preferred-card':
                AppState.setPreferredCard(target.dataset.id);
                Components.showToast('Card set as preferred payment method');
                break;
            case 'remove-card':
                this._removeCard(target.dataset.id);
                break;
            case 'submit-add-card':
                this._submitAddCard();
                break;
            case 'submit-edit-card':
                this._submitEditCard();
                break;
            case 'submit-confirm-card':
                this._submitConfirmCard();
                break;

            // Banks
            case 'open-add-bank-modal':
                this._openAddBankModal();
                break;
            case 'open-confirm-bank-modal':
                this._openConfirmBankModal(target.dataset.id);
                break;
            case 'remove-bank':
                this._removeBank(target.dataset.id);
                break;
            case 'submit-add-bank':
                this._submitAddBank();
                break;
            case 'submit-confirm-bank':
                this._submitConfirmBank();
                break;

            // Balance
            case 'open-add-money-modal':
                this._openAddMoneyModal();
                break;
            case 'open-withdraw-modal':
                this._openWithdrawModal();
                break;
            case 'open-convert-currency-modal':
                this._openConvertCurrencyModal();
                break;
            case 'open-add-currency-modal':
                this._openAddCurrencyModal();
                break;
            case 'set-primary-currency':
                AppState.setPrimaryCurrency(target.dataset.currency);
                Components.showToast(`${target.dataset.currency} set as primary currency`);
                break;
            case 'remove-currency':
                AppState.removeCurrency(target.dataset.currency);
                Components.showToast(`${target.dataset.currency} removed`);
                break;
            case 'submit-add-money':
                this._submitAddMoney();
                break;
            case 'submit-withdraw':
                this._submitWithdraw();
                break;
            case 'submit-convert-currency':
                this._submitConvertCurrency();
                break;
            case 'submit-add-currency':
                this._submitAddCurrency();
                break;

            // Crypto
            case 'open-buy-crypto-modal':
                this._openBuyCryptoModal(target.dataset.symbol);
                break;
            case 'open-sell-crypto-modal':
                this._openSellCryptoModal(target.dataset.symbol);
                break;
            case 'submit-buy-crypto':
                this._submitBuyCrypto();
                break;
            case 'submit-sell-crypto':
                this._submitSellCrypto();
                break;

            // Debit Card
            case 'open-change-pin-modal':
                this._openChangePinModal();
                break;
            case 'open-spending-limit-modal':
                this._openSpendingLimitModal();
                break;
            case 'open-atm-limit-modal':
                this._openATMLimitModal();
                break;
            case 'open-edit-employer-modal':
                this._openEditEmployerModal();
                break;
            case 'submit-change-pin':
                this._submitChangePin();
                break;
            case 'submit-spending-limit':
                this._submitSpendingLimit();
                break;
            case 'submit-atm-limit':
                this._submitATMLimit();
                break;
            case 'submit-edit-employer':
                this._submitEditEmployer();
                break;

            // Savings
            case 'open-savings-deposit-modal':
                this._openSavingsDepositModal();
                break;
            case 'open-savings-withdraw-modal':
                this._openSavingsWithdrawModal();
                break;
            case 'submit-savings-deposit':
                this._submitSavingsDeposit();
                break;
            case 'submit-savings-withdraw':
                this._submitSavingsWithdraw();
                break;

            // Credit
            case 'open-credit-payment-modal':
                this._openCreditPaymentModal();
                break;
            case 'submit-credit-payment':
                this._submitCreditPayment();
                break;

            // Rewards
            case 'open-redeem-rewards-modal':
                this._openRedeemRewardsModal();
                break;
            case 'submit-redeem-rewards':
                this._submitRedeemRewards();
                break;

            // Offers
            case 'save-offer':
                AppState.saveOffer(target.dataset.id);
                Components.showToast('Offer saved');
                break;
            case 'unsave-offer':
                AppState.unsaveOffer(target.dataset.id);
                Components.showToast('Offer removed');
                break;

            // Gift Cards
            case 'open-buy-gift-card-modal':
                this._openBuyGiftCardModal();
                break;
            case 'submit-buy-gift-card':
                this._submitBuyGiftCard();
                break;
            case 'select-gift-card-merchant':
                this._selectGiftCardMerchant(target.dataset.id);
                break;
            case 'select-gift-card-amount':
                this._selectGiftCardAmount(target.dataset.amount);
                break;

            // Preferences
            // handled by dropdown select

            // Mobile menu
            case 'toggle-sidebar':
                document.querySelector('.sidebar').classList.toggle('open');
                break;
        }
    },

    _handleDropdownSelect(dropdownId, value) {
        switch (dropdownId) {
            case 'date-filter-dropdown':
                AppState.transactionDateFilter = value;
                AppState.currentPage = 1;
                AppState.notify();
                break;
            case 'preferred-payment-dropdown':
                AppState.setPreferredPaymentMethod(value);
                Components.showToast('Preferred payment method updated');
                break;
            case 'backup-payment-dropdown':
                AppState.setBackupPaymentMethod(value);
                Components.showToast('Backup payment method updated');
                break;
            case 'cashback-category-dropdown':
                AppState.setCashBackCategory(value);
                Components.showToast(`Cash back category changed to ${value}`);
                break;
            case 'add-money-bank':
            case 'withdraw-bank':
            case 'convert-from-currency':
            case 'convert-to-currency':
            case 'add-currency-select':
                // These are form dropdowns, update the displayed value
                const trigger = document.querySelector(`#${dropdownId} .dropdown-value`);
                const items = document.querySelectorAll(`#${dropdownId}-menu .dropdown-item`);
                items.forEach(item => {
                    item.classList.toggle('selected', item.dataset.value === value);
                    if (item.dataset.value === value && trigger) {
                        trigger.textContent = item.textContent.trim();
                    }
                });
                document.querySelector(`#${dropdownId}`).dataset.selectedValue = value;
                break;
        }
    },

    _handleToggle(name) {
        switch (name) {
            case 'debit-cashback':
                AppState.toggleCashBack();
                Components.showToast(`Cash back ${AppState.paypalDebitCard.cashBackEnabled ? 'enabled' : 'disabled'}`);
                break;
            case 'direct-deposit':
                AppState.paypalDebitCard.directDeposit.enabled = !AppState.paypalDebitCard.directDeposit.enabled;
                AppState.notify();
                break;
            case 'autopay':
                AppState.toggleAutopay();
                Components.showToast(`AutoPay ${AppState.paypalCredit.autopayEnabled ? 'enabled' : 'disabled'}`);
                break;
            case 'instant-transfer':
                AppState.updatePreference('instantTransferPreference', !AppState.walletPreferences.instantTransferPreference);
                break;
            case 'auto-accept':
                AppState.updatePreference('autoAcceptPayments', !AppState.walletPreferences.autoAcceptPayments);
                break;
            default:
                if (name.startsWith('emailNotifications.')) {
                    const key = name;
                    const parts = key.split('.');
                    const current = AppState.walletPreferences.emailNotifications[parts[1]];
                    AppState.updatePreference(key, !current);
                }
                break;
        }
    },

    // ================================================================
    // MODAL IMPLEMENTATIONS
    // ================================================================

    // ---- Add Card ----
    _openAddCardModal() {
        const body = `
            <form id="add-card-form">
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Card Type <span class="required">*</span></label>
                        <div class="radio-inline">
                            <label class="radio-option selected"><input type="radio" name="card-type" value="credit" checked> Credit</label>
                            <label class="radio-option"><input type="radio" name="card-type" value="debit"> Debit</label>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Card Brand <span class="required">*</span></label>
                        <div class="radio-inline">
                            <label class="radio-option selected"><input type="radio" name="card-brand" value="Visa" checked> Visa</label>
                            <label class="radio-option"><input type="radio" name="card-brand" value="Mastercard"> Mastercard</label>
                            <label class="radio-option"><input type="radio" name="card-brand" value="American Express"> Amex</label>
                            <label class="radio-option"><input type="radio" name="card-brand" value="Discover"> Discover</label>
                        </div>
                    </div>
                </div>
                ${Components.renderInput('card-number', 'Card Number', '', 'text', { placeholder: '1234 5678 9012 3456', required: true, maxlength: '19' })}
                ${Components.renderInput('card-name', 'Name on Card', AppState.currentUser ? `${AppState.currentUser.firstName} ${AppState.currentUser.lastName}` : '', 'text', { required: true })}
                <div class="form-row two-col">
                    ${Components.renderInput('card-exp-month', 'Exp. Month', '', 'text', { placeholder: 'MM', required: true, maxlength: '2' })}
                    ${Components.renderInput('card-exp-year', 'Exp. Year', '', 'text', { placeholder: 'YYYY', required: true, maxlength: '4' })}
                </div>
                ${Components.renderInput('card-street', 'Billing Address', '', 'text', { placeholder: 'Street address', required: true })}
                <div class="form-row two-col">
                    ${Components.renderInput('card-city', 'City', '', 'text', { required: true })}
                    ${Components.renderInput('card-state', 'State', '', 'text', { required: true, maxlength: '2', placeholder: 'CA' })}
                </div>
                <div class="form-row two-col">
                    ${Components.renderInput('card-zip', 'ZIP Code', '', 'text', { required: true, maxlength: '10' })}
                    ${Components.renderInput('card-country', 'Country', 'US', 'text', { required: true, maxlength: '2' })}
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-add-card">Link Card</button>
        `;
        Components.openModal('add-card', 'Link a Card', body, footer);
    },

    _submitAddCard() {
        const cardNumber = document.getElementById('card-number')?.value?.trim();
        const name = document.getElementById('card-name')?.value?.trim();
        const month = parseInt(document.getElementById('card-exp-month')?.value?.trim());
        const year = parseInt(document.getElementById('card-exp-year')?.value?.trim());
        const street = document.getElementById('card-street')?.value?.trim();
        const city = document.getElementById('card-city')?.value?.trim();
        const state = document.getElementById('card-state')?.value?.trim();
        const zip = document.getElementById('card-zip')?.value?.trim();
        const country = document.getElementById('card-country')?.value?.trim();
        const type = document.querySelector('input[name="card-type"]:checked')?.value;
        const brand = document.querySelector('input[name="card-brand"]:checked')?.value;

        if (!cardNumber || cardNumber.replace(/\s/g, '').length < 13) {
            Components.showToast('Please enter a valid card number', 'error');
            return;
        }
        if (!name || !month || !year || !street || !city || !state || !zip) {
            Components.showToast('Please fill in all required fields', 'error');
            return;
        }
        if (month < 1 || month > 12) {
            Components.showToast('Invalid expiration month', 'error');
            return;
        }
        if (year < 2026) {
            Components.showToast('Card appears to be expired', 'error');
            return;
        }

        const lastFour = cardNumber.replace(/\s/g, '').slice(-4);
        AppState.addCard({
            type,
            brand,
            lastFour,
            cardholderName: name,
            expirationMonth: month,
            expirationYear: year,
            billingAddress: { street, city, state, zip, country: country || 'US' }
        });
        Components.closeModal();
        Components.showToast('Card linked successfully. Please confirm your card.');
    },

    // ---- Edit Card ----
    _openEditCardModal(cardId) {
        const card = AppState.getCardById(cardId);
        if (!card) return;
        AppState.modalData = { cardId };

        const body = `
            <form id="edit-card-form">
                <div class="card-edit-preview">
                    ${Components.renderCardVisual(card, true)}
                </div>
                <div class="form-row two-col">
                    ${Components.renderInput('edit-exp-month', 'Exp. Month', String(card.expirationMonth).padStart(2, '0'), 'text', { required: true, maxlength: '2' })}
                    ${Components.renderInput('edit-exp-year', 'Exp. Year', card.expirationYear, 'text', { required: true, maxlength: '4' })}
                </div>
                ${Components.renderInput('edit-street', 'Billing Address', card.billingAddress.street, 'text', { required: true })}
                <div class="form-row two-col">
                    ${Components.renderInput('edit-city', 'City', card.billingAddress.city, 'text', { required: true })}
                    ${Components.renderInput('edit-state', 'State', card.billingAddress.state, 'text', { required: true, maxlength: '2' })}
                </div>
                <div class="form-row two-col">
                    ${Components.renderInput('edit-zip', 'ZIP Code', card.billingAddress.zip, 'text', { required: true })}
                    ${Components.renderInput('edit-country', 'Country', card.billingAddress.country, 'text', { required: true, maxlength: '2' })}
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-edit-card">Update Card</button>
        `;
        Components.openModal('edit-card', 'Update Card', body, footer);
    },

    _submitEditCard() {
        const cardId = AppState.modalData?.cardId;
        if (!cardId) return;
        const month = parseInt(document.getElementById('edit-exp-month')?.value?.trim());
        const year = parseInt(document.getElementById('edit-exp-year')?.value?.trim());
        const street = document.getElementById('edit-street')?.value?.trim();
        const city = document.getElementById('edit-city')?.value?.trim();
        const state = document.getElementById('edit-state')?.value?.trim();
        const zip = document.getElementById('edit-zip')?.value?.trim();
        const country = document.getElementById('edit-country')?.value?.trim();

        if (!month || !year || !street || !city || !state || !zip) {
            Components.showToast('Please fill in all required fields', 'error');
            return;
        }

        const updates = {
            expirationMonth: month,
            expirationYear: year,
            billingAddress: { street, city, state, zip, country: country || 'US' }
        };
        if (year > 2026 || (year === 2026 && month >= new Date().getMonth() + 1)) {
            updates.isExpired = false;
            updates.status = 'confirmed';
        }
        AppState.updateCard(cardId, updates);
        Components.closeModal();
        Components.showToast('Card updated successfully');
    },

    // ---- Confirm Card ----
    _confirmCard(cardId) {
        AppState.modalData = { cardId };
        const card = AppState.getCardById(cardId);
        const body = `
            <p>PayPal has charged a small amount (approximately $1.95) to your ${card.brand} ending in ${card.lastFour}.</p>
            <p>Check your card statement for a 4-digit PayPal code and enter it below:</p>
            ${Components.renderInput('confirm-code', 'Confirmation Code', '', 'text', { placeholder: '4-digit code from your statement', required: true, maxlength: '4' })}
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-confirm-card">Confirm</button>
        `;
        Components.openModal('confirm-card', 'Confirm Your Card', body, footer);
    },

    _submitConfirmCard() {
        const cardId = AppState.modalData?.cardId;
        const code = document.getElementById('confirm-code')?.value?.trim();
        if (!code || code.length !== 4) {
            Components.showToast('Please enter a 4-digit code', 'error');
            return;
        }
        AppState.confirmCard(cardId);
        Components.closeModal();
        Components.showToast('Card confirmed successfully');
    },

    // ---- Remove Card ----
    _removeCard(cardId) {
        const card = AppState.getCardById(cardId);
        if (!card) return;
        Components.confirmDialog(
            'Remove Card',
            `Are you sure you want to remove your ${card.brand} card ending in ${card.lastFour}?`,
            () => {
                AppState.removeCard(cardId);
                Components.showToast('Card removed');
            },
            'Remove',
            true
        );
    },

    // ---- Add Bank ----
    _openAddBankModal() {
        const body = `
            <form id="add-bank-form">
                ${Components.renderInput('bank-name', 'Bank Name', '', 'text', { required: true, placeholder: 'e.g., Chase, Wells Fargo' })}
                <div class="form-group">
                    <label class="form-label">Account Type <span class="required">*</span></label>
                    <div class="radio-inline">
                        <label class="radio-option selected"><input type="radio" name="bank-type" value="checking" checked> Checking</label>
                        <label class="radio-option"><input type="radio" name="bank-type" value="savings"> Savings</label>
                    </div>
                </div>
                ${Components.renderInput('bank-routing', 'Routing Number', '', 'text', { required: true, placeholder: '9-digit routing number', maxlength: '9' })}
                ${Components.renderInput('bank-account', 'Account Number', '', 'text', { required: true, placeholder: 'Your account number' })}
                ${Components.renderInput('bank-account-confirm', 'Confirm Account Number', '', 'text', { required: true, placeholder: 'Re-enter account number' })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-add-bank">Link Bank Account</button>
        `;
        Components.openModal('add-bank', 'Link a Bank Account', body, footer);
    },

    _submitAddBank() {
        const bankName = document.getElementById('bank-name')?.value?.trim();
        const type = document.querySelector('input[name="bank-type"]:checked')?.value;
        const routing = document.getElementById('bank-routing')?.value?.trim();
        const account = document.getElementById('bank-account')?.value?.trim();
        const confirm = document.getElementById('bank-account-confirm')?.value?.trim();

        if (!bankName || !routing || !account || !confirm) {
            Components.showToast('Please fill in all required fields', 'error');
            return;
        }
        if (routing.length !== 9) {
            Components.showToast('Routing number must be 9 digits', 'error');
            return;
        }
        if (account !== confirm) {
            Components.showToast('Account numbers do not match', 'error');
            return;
        }

        const lastFour = account.slice(-4);
        AppState.addBankAccount({
            bankName,
            accountType: type,
            lastFour,
            routingNumber: routing,
            instantTransferEligible: type === 'checking'
        });
        Components.closeModal();
        Components.showToast('Bank account linked. Two small deposits will be sent for confirmation.');
    },

    // ---- Confirm Bank ----
    _openConfirmBankModal(bankId) {
        AppState.modalData = { bankId };
        const bank = AppState.getBankById(bankId);
        const body = `
            <p>Two small deposits were sent to your ${bank.bankName} account ending in ${bank.lastFour}.</p>
            <p>Enter the exact amounts below to confirm your bank account:</p>
            <div class="form-row two-col">
                ${Components.renderInput('deposit-1', 'Deposit 1', '', 'text', { placeholder: '0.XX', required: true })}
                ${Components.renderInput('deposit-2', 'Deposit 2', '', 'text', { placeholder: '0.XX', required: true })}
            </div>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-confirm-bank">Confirm</button>
        `;
        Components.openModal('confirm-bank', 'Confirm Bank Account', body, footer);
    },

    _submitConfirmBank() {
        const bankId = AppState.modalData?.bankId;
        const d1 = parseFloat(document.getElementById('deposit-1')?.value?.trim());
        const d2 = parseFloat(document.getElementById('deposit-2')?.value?.trim());
        if (isNaN(d1) || isNaN(d2) || d1 <= 0 || d2 <= 0) {
            Components.showToast('Please enter valid deposit amounts', 'error');
            return;
        }
        AppState.confirmBankAccount(bankId, d1, d2);
        Components.closeModal();
        Components.showToast('Bank account confirmed');
    },

    // ---- Remove Bank ----
    _removeBank(bankId) {
        const bank = AppState.getBankById(bankId);
        if (!bank) return;
        Components.confirmDialog(
            'Remove Bank Account',
            `Are you sure you want to remove your ${bank.bankName} account ending in ${bank.lastFour}?`,
            () => {
                AppState.removeBankAccount(bankId);
                Components.showToast('Bank account removed');
            },
            'Remove',
            true
        );
    },

    // ---- Add Money ----
    _openAddMoneyModal() {
        const confirmedBanks = AppState.bankAccounts.filter(b => b.status === 'confirmed');
        const bankOptions = confirmedBanks.map(b => ({
            value: b.id,
            label: `${b.bankName} ****${b.lastFour} (${b.accountType})`
        }));
        const body = `
            <form id="add-money-form">
                ${Components.renderInput('add-money-amount', 'Amount', '', 'text', { placeholder: '0.00', required: true })}
                <div class="form-group">
                    <label class="form-label">From Bank Account <span class="required">*</span></label>
                    ${Components.renderDropdown('add-money-bank', bankOptions, confirmedBanks[0]?.id, 'Select bank account')}
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-add-money">Add Money</button>
        `;
        Components.openModal('add-money', 'Add Money to Balance', body, footer);
    },

    _submitAddMoney() {
        const amount = parseFloat(document.getElementById('add-money-amount')?.value?.trim());
        const bankId = document.querySelector('#add-money-bank')?.dataset.selectedValue ||
                       AppState.bankAccounts.find(b => b.status === 'confirmed')?.id;
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (!bankId) {
            Components.showToast('Please select a bank account', 'error');
            return;
        }
        AppState.addMoney(amount, bankId);
        Components.closeModal();
        Components.showToast(`${Components.formatCurrency(amount)} added to your balance`);
    },

    // ---- Withdraw ----
    _openWithdrawModal() {
        const confirmedBanks = AppState.bankAccounts.filter(b => b.status === 'confirmed');
        const bankOptions = confirmedBanks.map(b => ({
            value: b.id,
            label: `${b.bankName} ****${b.lastFour} (${b.accountType})`
        }));
        const primary = AppState.getPrimaryBalance();
        const body = `
            <form id="withdraw-form">
                <p class="form-help-text">Available balance: ${Components.formatCurrency(primary ? primary.amount : 0)}</p>
                ${Components.renderInput('withdraw-amount', 'Amount', '', 'text', { placeholder: '0.00', required: true })}
                <div class="form-group">
                    <label class="form-label">To Bank Account <span class="required">*</span></label>
                    ${Components.renderDropdown('withdraw-bank', bankOptions, confirmedBanks[0]?.id, 'Select bank account')}
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-withdraw">Withdraw</button>
        `;
        Components.openModal('withdraw', 'Withdraw to Bank', body, footer);
    },

    _submitWithdraw() {
        const amount = parseFloat(document.getElementById('withdraw-amount')?.value?.trim());
        const bankId = document.querySelector('#withdraw-bank')?.dataset.selectedValue ||
                       AppState.bankAccounts.find(b => b.status === 'confirmed')?.id;
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (!bankId) {
            Components.showToast('Please select a bank account', 'error');
            return;
        }
        if (!AppState.withdrawMoney(amount, bankId)) {
            Components.showToast('Insufficient balance', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`${Components.formatCurrency(amount)} withdrawn to bank`);
    },

    // ---- Convert Currency ----
    _openConvertCurrencyModal() {
        const currencyOptions = AppState.balances.map(b => ({
            value: b.currency,
            label: `${b.currency} (${Components.formatCurrency(b.amount, b.currency)})`
        }));
        const allCurrencyOptions = CURRENCIES.map(c => ({ value: c.code, label: `${c.code} - ${c.name}` }));
        const body = `
            <form id="convert-form">
                <div class="form-group">
                    <label class="form-label">From Currency <span class="required">*</span></label>
                    ${Components.renderDropdown('convert-from-currency', currencyOptions, 'USD', 'Select currency')}
                </div>
                <div class="form-group">
                    <label class="form-label">To Currency <span class="required">*</span></label>
                    ${Components.renderDropdown('convert-to-currency', allCurrencyOptions, 'EUR', 'Select currency')}
                </div>
                ${Components.renderInput('convert-amount', 'Amount to Convert', '', 'text', { placeholder: '0.00', required: true })}
                <p class="form-help-text">A 3% conversion fee applies.</p>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-convert-currency">Convert</button>
        `;
        Components.openModal('convert-currency', 'Convert Currency', body, footer);
    },

    _submitConvertCurrency() {
        const from = document.querySelector('#convert-from-currency')?.dataset.selectedValue || 'USD';
        const to = document.querySelector('#convert-to-currency')?.dataset.selectedValue || 'EUR';
        const amount = parseFloat(document.getElementById('convert-amount')?.value?.trim());
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (from === to) {
            Components.showToast('Please select different currencies', 'error');
            return;
        }
        if (!AppState.convertCurrency(from, to, amount)) {
            Components.showToast('Insufficient balance in source currency', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`Converted ${Components.formatCurrency(amount, from)} to ${to}`);
    },

    // ---- Add Currency ----
    _openAddCurrencyModal() {
        const existingCodes = AppState.balances.map(b => b.currency);
        const availableCurrencies = CURRENCIES.filter(c => !existingCodes.includes(c.code));
        const options = availableCurrencies.map(c => ({ value: c.code, label: `${c.code} - ${c.name}` }));

        if (options.length === 0) {
            Components.showToast('All available currencies have been added', 'info');
            return;
        }

        const body = `
            <form id="add-currency-form">
                <div class="form-group">
                    <label class="form-label">Currency <span class="required">*</span></label>
                    ${Components.renderDropdown('add-currency-select', options, options[0]?.value, 'Select currency')}
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-add-currency">Add Currency</button>
        `;
        Components.openModal('add-currency', 'Add Currency', body, footer);
    },

    _submitAddCurrency() {
        const code = document.querySelector('#add-currency-select')?.dataset.selectedValue;
        if (!code) {
            Components.showToast('Please select a currency', 'error');
            return;
        }
        AppState.addCurrency(code);
        Components.closeModal();
        Components.showToast(`${code} added to your wallet`);
    },

    // ---- Buy Crypto ----
    _openBuyCryptoModal(symbol) {
        const crypto = AppState.getCryptoBySymbol(symbol);
        if (!crypto) return;
        const primary = AppState.getPrimaryBalance();
        AppState.modalData = { symbol };

        const body = `
            <form id="buy-crypto-form">
                <div class="crypto-modal-header">
                    <div class="crypto-symbol-badge large">${crypto.symbol}</div>
                    <div>
                        <div class="crypto-modal-name">${crypto.name}</div>
                        <div class="crypto-modal-price">Current Price: ${Components.formatCurrency(crypto.currentPrice)}</div>
                    </div>
                </div>
                <p class="form-help-text">Available balance: ${Components.formatCurrency(primary ? primary.amount : 0)}</p>
                ${Components.renderInput('buy-crypto-amount', 'Amount (USD)', '', 'text', { placeholder: '0.00', required: true })}
                <div class="crypto-estimate" id="buy-crypto-estimate"></div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-buy-crypto">Buy ${crypto.name}</button>
        `;
        Components.openModal('buy-crypto', `Buy ${crypto.name}`, body, footer);

        setTimeout(() => {
            const input = document.getElementById('buy-crypto-amount');
            if (input) {
                input.addEventListener('input', () => {
                    const amount = parseFloat(input.value);
                    const est = document.getElementById('buy-crypto-estimate');
                    if (!isNaN(amount) && amount > 0 && est) {
                        const fee = AppState._calculateCryptoFee(amount);
                        const qty = (amount - fee) / crypto.currentPrice;
                        est.innerHTML = `
                            <div>Estimated: ${qty.toFixed(6)} ${crypto.symbol}</div>
                            <div>Fee: ${Components.formatCurrency(fee)}</div>
                        `;
                    } else if (est) {
                        est.innerHTML = '';
                    }
                });
            }
        }, 100);
    },

    _submitBuyCrypto() {
        const symbol = AppState.modalData?.symbol;
        const amount = parseFloat(document.getElementById('buy-crypto-amount')?.value?.trim());
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (amount < 1) {
            Components.showToast('Minimum purchase is $1.00', 'error');
            return;
        }
        if (!AppState.buyCrypto(symbol, amount)) {
            Components.showToast('Insufficient balance', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`Successfully purchased ${symbol}`);
    },

    // ---- Sell Crypto ----
    _openSellCryptoModal(symbol) {
        const crypto = AppState.getCryptoBySymbol(symbol);
        if (!crypto) return;
        AppState.modalData = { symbol };

        const body = `
            <form id="sell-crypto-form">
                <div class="crypto-modal-header">
                    <div class="crypto-symbol-badge large">${crypto.symbol}</div>
                    <div>
                        <div class="crypto-modal-name">${crypto.name}</div>
                        <div class="crypto-modal-price">Current Price: ${Components.formatCurrency(crypto.currentPrice)}</div>
                    </div>
                </div>
                <p class="form-help-text">Available: ${crypto.quantity.toFixed(5)} ${crypto.symbol} (${Components.formatCurrency(crypto.currentValue)})</p>
                ${Components.renderInput('sell-crypto-amount', 'Amount to Sell (USD)', '', 'text', { placeholder: '0.00', required: true })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-sell-crypto">Sell ${crypto.name}</button>
        `;
        Components.openModal('sell-crypto', `Sell ${crypto.name}`, body, footer);
    },

    _submitSellCrypto() {
        const symbol = AppState.modalData?.symbol;
        const amount = parseFloat(document.getElementById('sell-crypto-amount')?.value?.trim());
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (!AppState.sellCrypto(symbol, amount)) {
            Components.showToast('Insufficient crypto balance or invalid amount', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`Successfully sold ${symbol}`);
    },

    // ---- Change PIN ----
    _openChangePinModal() {
        const body = `
            <form id="change-pin-form">
                ${Components.renderInput('new-pin', 'New PIN', '', 'password', { placeholder: '4-digit PIN', required: true, maxlength: '4' })}
                ${Components.renderInput('confirm-pin', 'Confirm PIN', '', 'password', { placeholder: 'Confirm PIN', required: true, maxlength: '4' })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-change-pin">Change PIN</button>
        `;
        Components.openModal('change-pin', 'Change Debit Card PIN', body, footer);
    },

    _submitChangePin() {
        const pin = document.getElementById('new-pin')?.value?.trim();
        const confirm = document.getElementById('confirm-pin')?.value?.trim();
        if (!pin || pin.length !== 4 || !/^\d{4}$/.test(pin)) {
            Components.showToast('PIN must be exactly 4 digits', 'error');
            return;
        }
        if (pin !== confirm) {
            Components.showToast('PINs do not match', 'error');
            return;
        }
        AppState.updateDebitCardPin();
        Components.closeModal();
        Components.showToast('PIN changed successfully');
    },

    // ---- Spending Limit ----
    _openSpendingLimitModal() {
        const dc = AppState.paypalDebitCard;
        const body = `
            <form id="spending-limit-form">
                <p class="form-help-text">Set your daily spending limit (max $10,000).</p>
                ${Components.renderInput('spending-limit', 'Daily Spending Limit ($)', dc ? dc.dailySpendingLimit : 3000, 'text', { required: true })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-spending-limit">Update</button>
        `;
        Components.openModal('spending-limit', 'Daily Spending Limit', body, footer);
    },

    _submitSpendingLimit() {
        const limit = parseFloat(document.getElementById('spending-limit')?.value?.trim());
        if (isNaN(limit) || limit < 0 || limit > 10000) {
            Components.showToast('Limit must be between $0 and $10,000', 'error');
            return;
        }
        AppState.setDailySpendingLimit(limit);
        Components.closeModal();
        Components.showToast('Spending limit updated');
    },

    // ---- ATM Limit ----
    _openATMLimitModal() {
        const dc = AppState.paypalDebitCard;
        const body = `
            <form id="atm-limit-form">
                <p class="form-help-text">Set your daily ATM withdrawal limit (max $3,000).</p>
                ${Components.renderInput('atm-limit', 'Daily ATM Limit ($)', dc ? dc.dailyATMLimit : 400, 'text', { required: true })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-atm-limit">Update</button>
        `;
        Components.openModal('atm-limit', 'Daily ATM Limit', body, footer);
    },

    _submitATMLimit() {
        const limit = parseFloat(document.getElementById('atm-limit')?.value?.trim());
        if (isNaN(limit) || limit < 0 || limit > 3000) {
            Components.showToast('Limit must be between $0 and $3,000', 'error');
            return;
        }
        AppState.setDailyATMLimit(limit);
        Components.closeModal();
        Components.showToast('ATM limit updated');
    },

    // ---- Edit Employer ----
    _openEditEmployerModal() {
        const dc = AppState.paypalDebitCard;
        const body = `
            <form id="edit-employer-form">
                ${Components.renderInput('employer-name', 'Employer Name', dc?.directDeposit?.employer || '', 'text', { required: true })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-edit-employer">Save</button>
        `;
        Components.openModal('edit-employer', 'Edit Employer', body, footer);
    },

    _submitEditEmployer() {
        const name = document.getElementById('employer-name')?.value?.trim();
        if (!name) {
            Components.showToast('Please enter an employer name', 'error');
            return;
        }
        AppState.updateDirectDeposit({ employer: name });
        Components.closeModal();
        Components.showToast('Employer updated');
    },

    // ---- Savings Deposit ----
    _openSavingsDepositModal() {
        const primary = AppState.getPrimaryBalance();
        const body = `
            <form id="savings-deposit-form">
                <p class="form-help-text">Available balance: ${Components.formatCurrency(primary ? primary.amount : 0)}</p>
                ${Components.renderInput('savings-deposit-amount', 'Deposit Amount', '', 'text', { placeholder: '0.00', required: true })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-savings-deposit">Deposit</button>
        `;
        Components.openModal('savings-deposit', 'Deposit to Savings', body, footer);
    },

    _submitSavingsDeposit() {
        const amount = parseFloat(document.getElementById('savings-deposit-amount')?.value?.trim());
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (!AppState.depositToSavings(amount)) {
            Components.showToast('Insufficient balance', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`${Components.formatCurrency(amount)} deposited to savings`);
    },

    // ---- Savings Withdraw ----
    _openSavingsWithdrawModal() {
        const sav = AppState.savingsAccount;
        const body = `
            <form id="savings-withdraw-form">
                <p class="form-help-text">Savings balance: ${Components.formatCurrency(sav ? sav.balance : 0)}</p>
                ${Components.renderInput('savings-withdraw-amount', 'Withdrawal Amount', '', 'text', { placeholder: '0.00', required: true })}
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-savings-withdraw">Withdraw</button>
        `;
        Components.openModal('savings-withdraw', 'Withdraw from Savings', body, footer);
    },

    _submitSavingsWithdraw() {
        const amount = parseFloat(document.getElementById('savings-withdraw-amount')?.value?.trim());
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (!AppState.withdrawFromSavings(amount)) {
            Components.showToast('Insufficient savings balance', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`${Components.formatCurrency(amount)} withdrawn from savings`);
    },

    // ---- Credit Payment ----
    _openCreditPaymentModal() {
        const credit = AppState.paypalCredit;
        const primary = AppState.getPrimaryBalance();
        const body = `
            <form id="credit-payment-form">
                <p class="form-help-text">Current balance: ${Components.formatCurrency(credit.currentBalance)}</p>
                <p class="form-help-text">Available PayPal balance: ${Components.formatCurrency(primary ? primary.amount : 0)}</p>
                <p class="form-help-text">Minimum payment: ${Components.formatCurrency(credit.minimumPaymentDue)}</p>
                ${Components.renderInput('credit-payment-amount', 'Payment Amount', '', 'text', { placeholder: '0.00', required: true })}
                <div class="quick-amount-btns">
                    <button type="button" class="btn btn-xs btn-outline" onclick="document.getElementById('credit-payment-amount').value='${credit.minimumPaymentDue}'">Minimum (${Components.formatCurrency(credit.minimumPaymentDue)})</button>
                    <button type="button" class="btn btn-xs btn-outline" onclick="document.getElementById('credit-payment-amount').value='${credit.currentBalance}'">Full Balance (${Components.formatCurrency(credit.currentBalance)})</button>
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-credit-payment">Make Payment</button>
        `;
        Components.openModal('credit-payment', 'Make a Payment', body, footer);
    },

    _submitCreditPayment() {
        const amount = parseFloat(document.getElementById('credit-payment-amount')?.value?.trim());
        if (isNaN(amount) || amount <= 0) {
            Components.showToast('Please enter a valid amount', 'error');
            return;
        }
        if (!AppState.makePaypalCreditPayment(amount)) {
            Components.showToast('Insufficient PayPal balance', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`Payment of ${Components.formatCurrency(amount)} applied`);
    },

    // ---- Redeem Rewards ----
    _openRedeemRewardsModal() {
        const rwd = AppState.rewards;
        const body = `
            <form id="redeem-rewards-form">
                <p class="form-help-text">Available: ${rwd.totalPoints.toLocaleString()} points (worth ${Components.formatCurrency(rwd.pointsValue)})</p>
                ${Components.renderInput('redeem-points', 'Points to Redeem', '', 'text', { placeholder: 'e.g., 500', required: true, helpText: '100 points = $1.00' })}
                <div class="form-group">
                    <label class="form-label">Redeem For</label>
                    <div class="radio-inline">
                        <label class="radio-option selected"><input type="radio" name="redeem-type" value="balance" checked> PayPal Balance</label>
                        <label class="radio-option"><input type="radio" name="redeem-type" value="gift_card"> Gift Card</label>
                    </div>
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-redeem-rewards">Redeem</button>
        `;
        Components.openModal('redeem-rewards', 'Redeem Rewards', body, footer);
    },

    _submitRedeemRewards() {
        const points = parseInt(document.getElementById('redeem-points')?.value?.trim());
        const type = document.querySelector('input[name="redeem-type"]:checked')?.value;
        if (isNaN(points) || points <= 0) {
            Components.showToast('Please enter a valid number of points', 'error');
            return;
        }
        if (points < 100) {
            Components.showToast('Minimum redemption is 100 points', 'error');
            return;
        }
        if (!AppState.redeemRewards(points, type)) {
            Components.showToast('Insufficient points', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`Redeemed ${points.toLocaleString()} points`);
    },

    // ---- Buy Gift Card ----
    _openBuyGiftCardModal() {
        AppState.modalData = { selectedMerchant: null, selectedAmount: null };
        const categories = [...new Set(AppState.giftCardMerchants.map(m => m.category))];
        const body = `
            <form id="buy-gift-card-form">
                <div class="gift-card-merchant-grid" id="gift-card-merchants">
                    ${AppState.giftCardMerchants.map(m => `
                        <div class="gift-card-merchant-option" data-action="select-gift-card-merchant" data-id="${m.id}">
                            <div class="merchant-icon">${m.name.charAt(0)}</div>
                            <div class="merchant-name">${m.name}</div>
                        </div>
                    `).join('')}
                </div>
                <div id="gift-card-amount-section" style="display:none">
                    <div class="form-group">
                        <label class="form-label">Amount</label>
                        <div class="amount-options" id="gift-card-amounts"></div>
                    </div>
                </div>
                <div id="gift-card-details-section" style="display:none">
                    ${Components.renderInput('gc-recipient-name', 'Recipient Name', '', 'text', { required: true, placeholder: 'Name' })}
                    ${Components.renderInput('gc-recipient-email', 'Recipient Email', '', 'text', { required: true, placeholder: 'email@example.com' })}
                    ${Components.renderInput('gc-message', 'Message (optional)', '', 'text', { placeholder: 'Add a personal message' })}
                </div>
            </form>
        `;
        const footer = `
            <button class="btn btn-secondary" data-action="close-modal">Cancel</button>
            <button class="btn btn-primary" data-action="submit-buy-gift-card" id="buy-gc-btn" disabled>Buy Gift Card</button>
        `;
        Components.openModal('buy-gift-card', 'Buy a Gift Card', body, footer, { width: '600px' });
    },

    _selectGiftCardMerchant(merchantId) {
        const merchant = AppState.giftCardMerchants.find(m => m.id === merchantId);
        if (!merchant) return;
        AppState.modalData.selectedMerchant = merchant;
        AppState.modalData.selectedAmount = null;

        document.querySelectorAll('.gift-card-merchant-option').forEach(el => {
            el.classList.toggle('selected', el.dataset.id === merchantId);
        });

        const amountSection = document.getElementById('gift-card-amount-section');
        const amountsContainer = document.getElementById('gift-card-amounts');
        if (amountSection && amountsContainer) {
            amountSection.style.display = 'block';
            amountsContainer.innerHTML = merchant.denominations.map(d => `
                <button type="button" class="amount-btn" data-action="select-gift-card-amount" data-amount="${d}">
                    ${Components.formatCurrency(d)}
                </button>
            `).join('');
        }
        document.getElementById('gift-card-details-section').style.display = 'none';
        document.getElementById('buy-gc-btn').disabled = true;
    },

    _selectGiftCardAmount(amount) {
        AppState.modalData.selectedAmount = parseFloat(amount);
        document.querySelectorAll('.amount-btn').forEach(btn => {
            btn.classList.toggle('selected', btn.dataset.amount === amount);
        });
        document.getElementById('gift-card-details-section').style.display = 'block';
        document.getElementById('buy-gc-btn').disabled = false;
    },

    _submitBuyGiftCard() {
        const merchant = AppState.modalData?.selectedMerchant;
        const amount = AppState.modalData?.selectedAmount;
        const name = document.getElementById('gc-recipient-name')?.value?.trim();
        const email = document.getElementById('gc-recipient-email')?.value?.trim();
        const message = document.getElementById('gc-message')?.value?.trim() || '';

        if (!merchant || !amount) {
            Components.showToast('Please select a merchant and amount', 'error');
            return;
        }
        if (!name || !email) {
            Components.showToast('Please enter recipient name and email', 'error');
            return;
        }
        if (!email.includes('@')) {
            Components.showToast('Please enter a valid email address', 'error');
            return;
        }

        const gc = AppState.purchaseGiftCard(merchant.name, amount, email, name, message);
        if (!gc) {
            Components.showToast('Insufficient balance', 'error');
            return;
        }
        Components.closeModal();
        Components.showToast(`${Components.formatCurrency(amount)} ${merchant.name} gift card purchased!`);
    },

    // ---- SSE ----
    _setupSSE() {
        const eventSource = new EventSource('/api/events');
        eventSource.onmessage = (e) => {
            if (e.data === 'reset') {
                AppState.resetToSeedData();
            }
        };
    }
};

// ---- Initialize on DOM ready ----
document.addEventListener('DOMContentLoaded', () => App.init());
