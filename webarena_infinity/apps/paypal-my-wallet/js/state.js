// ============================================================
// state.js — Centralized state management for PayPal My Wallet
// ============================================================

const AppState = {
    // ---- Persistent State ----
    currentUser: null,
    cards: [],
    bankAccounts: [],
    balances: [],
    cryptoHoldings: [],
    paypalDebitCard: null,
    savingsAccount: null,
    payLaterPlans: [],
    rewards: null,
    offers: [],
    giftCards: [],
    transactions: [],
    paypalCredit: null,
    walletPreferences: null,
    giftCardMerchants: [],

    // ---- ID Counters ----
    _nextCardId: 100,
    _nextBankId: 100,
    _nextTransactionId: 200,
    _nextGiftCardId: 100,
    _nextOfferId: 100,
    _nextRewardId: 100,
    _nextCryptoTxId: 200,
    _nextSavingsTxId: 100,
    _nextPlanId: 100,

    // ---- UI State (not persisted) ----
    currentView: 'overview',
    currentSubView: null,
    selectedCardId: null,
    selectedBankId: null,
    selectedCryptoId: null,
    selectedGiftCardId: null,
    selectedPlanId: null,
    selectedTransactionId: null,
    modalOpen: null,
    modalData: null,
    toastMessage: null,
    toastType: null,
    searchQuery: '',
    transactionFilter: 'all',
    transactionDateFilter: 'all',
    offerFilter: 'all',
    cryptoSortBy: 'value',
    currentPage: 1,
    itemsPerPage: 10,

    // ---- Listeners ----
    _listeners: [],

    subscribe(fn) {
        this._listeners.push(fn);
    },

    notify() {
        this._persist();
        this._pushStateToServer();
        for (const fn of this._listeners) {
            try { fn(); } catch (e) { console.error('Listener error:', e); }
        }
    },

    // ---- Initialization ----

    init() {
        const persisted = this._loadPersistedData();
        if (persisted) {
            this.currentUser = persisted.currentUser || null;
            this.cards = persisted.cards || [];
            this.bankAccounts = persisted.bankAccounts || [];
            this.balances = persisted.balances || [];
            this.cryptoHoldings = persisted.cryptoHoldings || [];
            this.paypalDebitCard = persisted.paypalDebitCard || null;
            this.savingsAccount = persisted.savingsAccount || null;
            this.payLaterPlans = persisted.payLaterPlans || [];
            this.rewards = persisted.rewards || null;
            this.offers = persisted.offers || [];
            this.giftCards = persisted.giftCards || [];
            this.transactions = persisted.transactions || [];
            this.paypalCredit = persisted.paypalCredit || null;
            this.walletPreferences = persisted.walletPreferences || null;
            this.giftCardMerchants = persisted.giftCardMerchants || [];
            this._nextCardId = persisted._nextCardId || 100;
            this._nextBankId = persisted._nextBankId || 100;
            this._nextTransactionId = persisted._nextTransactionId || 200;
            this._nextGiftCardId = persisted._nextGiftCardId || 100;
            this._nextOfferId = persisted._nextOfferId || 100;
            this._nextRewardId = persisted._nextRewardId || 100;
            this._nextCryptoTxId = persisted._nextCryptoTxId || 200;
            this._nextSavingsTxId = persisted._nextSavingsTxId || 100;
            this._nextPlanId = persisted._nextPlanId || 100;
        } else {
            this._loadSeedData();
        }
    },

    _loadSeedData() {
        this.currentUser = JSON.parse(JSON.stringify(CURRENT_USER));
        this.cards = JSON.parse(JSON.stringify(CARDS));
        this.bankAccounts = JSON.parse(JSON.stringify(BANK_ACCOUNTS));
        this.balances = JSON.parse(JSON.stringify(BALANCES));
        this.cryptoHoldings = JSON.parse(JSON.stringify(CRYPTO_HOLDINGS));
        this.paypalDebitCard = JSON.parse(JSON.stringify(PAYPAL_DEBIT_CARD));
        this.savingsAccount = JSON.parse(JSON.stringify(SAVINGS_ACCOUNT));
        this.payLaterPlans = JSON.parse(JSON.stringify(PAY_LATER_PLANS));
        this.rewards = JSON.parse(JSON.stringify(REWARDS));
        this.offers = JSON.parse(JSON.stringify(OFFERS));
        this.giftCards = JSON.parse(JSON.stringify(GIFT_CARDS));
        this.transactions = JSON.parse(JSON.stringify(TRANSACTIONS));
        this.paypalCredit = JSON.parse(JSON.stringify(PAYPAL_CREDIT));
        this.walletPreferences = JSON.parse(JSON.stringify(WALLET_PREFERENCES));
        this.giftCardMerchants = JSON.parse(JSON.stringify(GIFT_CARD_MERCHANTS));
    },

    _loadPersistedData() {
        try {
            const saved = localStorage.getItem('paypalWalletState');
            if (!saved) return null;
            const parsed = JSON.parse(saved);
            if (parsed._seedVersion !== SEED_DATA_VERSION) {
                localStorage.removeItem('paypalWalletState');
                return null;
            }
            return parsed;
        } catch (e) {
            return null;
        }
    },

    // ---- Persistence ----

    _persist() {
        const state = this.getSerializableState();
        localStorage.setItem('paypalWalletState', JSON.stringify(state));
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
            _seedVersion: SEED_DATA_VERSION,
            currentUser: this.currentUser,
            cards: this.cards,
            bankAccounts: this.bankAccounts,
            balances: this.balances,
            cryptoHoldings: this.cryptoHoldings,
            paypalDebitCard: this.paypalDebitCard,
            savingsAccount: this.savingsAccount,
            payLaterPlans: this.payLaterPlans,
            rewards: this.rewards,
            offers: this.offers,
            giftCards: this.giftCards,
            transactions: this.transactions,
            paypalCredit: this.paypalCredit,
            walletPreferences: this.walletPreferences,
            giftCardMerchants: this.giftCardMerchants,
            _nextCardId: this._nextCardId,
            _nextBankId: this._nextBankId,
            _nextTransactionId: this._nextTransactionId,
            _nextGiftCardId: this._nextGiftCardId,
            _nextOfferId: this._nextOfferId,
            _nextRewardId: this._nextRewardId,
            _nextCryptoTxId: this._nextCryptoTxId,
            _nextSavingsTxId: this._nextSavingsTxId,
            _nextPlanId: this._nextPlanId,
        };
    },

    resetToSeedData() {
        localStorage.removeItem('paypalWalletState');
        this._loadSeedData();
        this.currentView = 'overview';
        this.currentSubView = null;
        this.selectedCardId = null;
        this.selectedBankId = null;
        this.selectedCryptoId = null;
        this.modalOpen = null;
        this.modalData = null;
        this.searchQuery = '';
        this.transactionFilter = 'all';
        this.transactionDateFilter = 'all';
        this.currentPage = 1;
        this.notify();
    },

    // ---- Card Operations ----

    getCardById(id) {
        return this.cards.find(c => c.id === id);
    },

    addCard(cardData) {
        const card = {
            id: `card_${String(this._nextCardId++).padStart(3, '0')}`,
            ...cardData,
            status: 'pending_confirmation',
            isPreferred: false,
            isExpired: false,
            addedAt: new Date().toISOString(),
            confirmedAt: null,
            lastUsed: null,
            isBackup: false,
            confirmationCode: null
        };
        this.cards.push(card);
        this.notify();
        return card;
    },

    updateCard(id, updates) {
        const card = this.getCardById(id);
        if (card) {
            Object.assign(card, updates);
            this.notify();
        }
        return card;
    },

    removeCard(id) {
        const idx = this.cards.findIndex(c => c.id === id);
        if (idx !== -1) {
            const card = this.cards[idx];
            if (card.isPreferred) {
                this.walletPreferences.preferredPaymentMethod = null;
            }
            if (card.isBackup) {
                this.walletPreferences.backupPaymentMethod = null;
            }
            this.cards.splice(idx, 1);
            this.notify();
            return true;
        }
        return false;
    },

    confirmCard(id) {
        const card = this.getCardById(id);
        if (card && card.status === 'pending_confirmation') {
            card.status = 'confirmed';
            card.confirmedAt = new Date().toISOString();
            this.notify();
            return true;
        }
        return false;
    },

    setPreferredCard(id) {
        this.cards.forEach(c => c.isPreferred = false);
        const card = this.getCardById(id);
        if (card) {
            card.isPreferred = true;
            this.walletPreferences.preferredPaymentMethod = id;
            this.currentUser.preferredPaymentMethodId = id;
            this.notify();
        }
    },

    setBackupCard(id) {
        this.cards.forEach(c => c.isBackup = false);
        this.bankAccounts.forEach(b => { if (b.id === this.walletPreferences.backupPaymentMethod) { /* keep */ } });
        const card = this.getCardById(id);
        if (card) {
            card.isBackup = true;
            this.walletPreferences.backupPaymentMethod = id;
            this.currentUser.backupPaymentMethodId = id;
            this.notify();
        }
    },

    // ---- Bank Account Operations ----

    getBankById(id) {
        return this.bankAccounts.find(b => b.id === id);
    },

    addBankAccount(bankData) {
        const bank = {
            id: `bank_${String(this._nextBankId++).padStart(3, '0')}`,
            ...bankData,
            status: 'pending_confirmation',
            isPreferred: false,
            addedAt: new Date().toISOString(),
            confirmedAt: null,
            lastUsed: null,
            confirmationDeposit1: null,
            confirmationDeposit2: null
        };
        this.bankAccounts.push(bank);
        this.notify();
        return bank;
    },

    removeBankAccount(id) {
        const idx = this.bankAccounts.findIndex(b => b.id === id);
        if (idx !== -1) {
            if (this.walletPreferences.backupPaymentMethod === id) {
                this.walletPreferences.backupPaymentMethod = null;
            }
            this.bankAccounts.splice(idx, 1);
            this.notify();
            return true;
        }
        return false;
    },

    confirmBankAccount(id, deposit1, deposit2) {
        const bank = this.getBankById(id);
        if (bank && bank.status === 'pending_confirmation') {
            bank.status = 'confirmed';
            bank.confirmedAt = new Date().toISOString();
            bank.confirmationDeposit1 = deposit1;
            bank.confirmationDeposit2 = deposit2;
            this.notify();
            return true;
        }
        return false;
    },

    // ---- Balance Operations ----

    getBalance(currency) {
        return this.balances.find(b => b.currency === currency);
    },

    getPrimaryBalance() {
        return this.balances.find(b => b.isPrimary);
    },

    getTotalBalanceUSD() {
        let total = 0;
        for (const bal of this.balances) {
            if (bal.currency === 'USD') {
                total += bal.amount;
            } else {
                total += bal.amount / (EXCHANGE_RATES[bal.currency] || 1);
            }
        }
        return total;
    },

    addCurrency(currencyCode) {
        if (!this.balances.find(b => b.currency === currencyCode)) {
            this.balances.push({
                currency: currencyCode,
                amount: 0,
                isPrimary: false
            });
            this.notify();
        }
    },

    removeCurrency(currencyCode) {
        const bal = this.getBalance(currencyCode);
        if (bal && !bal.isPrimary && bal.amount === 0) {
            this.balances = this.balances.filter(b => b.currency !== currencyCode);
            this.notify();
            return true;
        }
        return false;
    },

    setPrimaryCurrency(currencyCode) {
        this.balances.forEach(b => b.isPrimary = false);
        const bal = this.getBalance(currencyCode);
        if (bal) {
            bal.isPrimary = true;
            this.currentUser.primaryCurrency = currencyCode;
            this.notify();
        }
    },

    convertCurrency(fromCurrency, toCurrency, amount) {
        const fromBal = this.getBalance(fromCurrency);
        let toBal = this.getBalance(toCurrency);
        if (!fromBal || fromBal.amount < amount) return false;
        if (!toBal) {
            this.addCurrency(toCurrency);
            toBal = this.getBalance(toCurrency);
        }
        const fromRate = EXCHANGE_RATES[fromCurrency] || 1;
        const toRate = EXCHANGE_RATES[toCurrency] || 1;
        const usdAmount = amount / fromRate;
        const convertedAmount = usdAmount * toRate;
        const fee = usdAmount * 0.03;
        fromBal.amount = Math.round((fromBal.amount - amount) * 100) / 100;
        toBal.amount = Math.round((toBal.amount + convertedAmount - (fee * toRate)) * 100) / 100;

        this.transactions.unshift({
            id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
            type: 'currency_convert',
            description: `Converted ${fromCurrency} to ${toCurrency}`,
            amount: -amount,
            currency: fromCurrency,
            date: new Date().toISOString(),
            status: 'completed',
            paymentMethod: 'balance',
            category: 'Currency'
        });
        this.notify();
        return true;
    },

    addMoney(amount, fromBankId) {
        const primary = this.getPrimaryBalance();
        if (primary) {
            primary.amount = Math.round((primary.amount + amount) * 100) / 100;
            this.transactions.unshift({
                id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
                type: 'transfer_in',
                description: `From ${this.getBankById(fromBankId)?.bankName || 'Bank'} ***${this.getBankById(fromBankId)?.lastFour || '****'}`,
                amount: amount,
                currency: primary.currency,
                date: new Date().toISOString(),
                status: 'completed',
                paymentMethod: fromBankId,
                category: 'Transfer'
            });
            this.notify();
            return true;
        }
        return false;
    },

    withdrawMoney(amount, toBankId) {
        const primary = this.getPrimaryBalance();
        if (primary && primary.amount >= amount) {
            primary.amount = Math.round((primary.amount - amount) * 100) / 100;
            this.transactions.unshift({
                id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
                type: 'transfer_out',
                description: `To ${this.getBankById(toBankId)?.bankName || 'Bank'} ***${this.getBankById(toBankId)?.lastFour || '****'}`,
                amount: -amount,
                currency: primary.currency,
                date: new Date().toISOString(),
                status: 'completed',
                paymentMethod: toBankId,
                category: 'Transfer'
            });
            this.notify();
            return true;
        }
        return false;
    },

    // ---- Crypto Operations ----

    getCryptoById(id) {
        return this.cryptoHoldings.find(c => c.id === id);
    },

    getCryptoBySymbol(symbol) {
        return this.cryptoHoldings.find(c => c.symbol === symbol);
    },

    buyCrypto(symbol, usdAmount) {
        const crypto = this.getCryptoBySymbol(symbol);
        const primary = this.getPrimaryBalance();
        if (!crypto || !primary || primary.amount < usdAmount) return false;
        const fee = this._calculateCryptoFee(usdAmount);
        const netAmount = usdAmount - fee;
        const quantity = netAmount / crypto.currentPrice;
        primary.amount = Math.round((primary.amount - usdAmount) * 100) / 100;
        crypto.quantity = Math.round((crypto.quantity + quantity) * 100000) / 100000;
        crypto.totalCost = Math.round((crypto.totalCost + netAmount) * 100) / 100;
        crypto.currentValue = Math.round(crypto.quantity * crypto.currentPrice * 100) / 100;
        crypto.totalReturn = Math.round((crypto.currentValue - crypto.totalCost) * 100) / 100;
        crypto.totalReturnPercent = crypto.totalCost > 0 ? Math.round((crypto.totalReturn / crypto.totalCost) * 10000) / 100 : 0;
        crypto.averagePurchasePrice = crypto.quantity > 0 ? Math.round((crypto.totalCost / crypto.quantity) * 100) / 100 : 0;
        crypto.transactions.push({
            id: `ctx_${String(this._nextCryptoTxId++).padStart(3, '0')}`,
            type: 'buy',
            quantity,
            pricePerUnit: crypto.currentPrice,
            total: netAmount,
            fee,
            date: new Date().toISOString()
        });
        this.transactions.unshift({
            id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
            type: 'crypto_buy',
            description: `Bought ${crypto.name}`,
            amount: -usdAmount,
            currency: 'USD',
            date: new Date().toISOString(),
            status: 'completed',
            paymentMethod: 'balance',
            category: 'Crypto'
        });
        this.notify();
        return true;
    },

    sellCrypto(symbol, usdAmount) {
        const crypto = this.getCryptoBySymbol(symbol);
        const primary = this.getPrimaryBalance();
        if (!crypto || !primary) return false;
        const quantity = usdAmount / crypto.currentPrice;
        if (crypto.quantity < quantity) return false;
        const fee = this._calculateCryptoFee(usdAmount);
        const netProceeds = usdAmount - fee;
        crypto.quantity = Math.round((crypto.quantity - quantity) * 100000) / 100000;
        const costBasis = quantity * crypto.averagePurchasePrice;
        crypto.totalCost = Math.max(0, Math.round((crypto.totalCost - costBasis) * 100) / 100);
        crypto.currentValue = Math.round(crypto.quantity * crypto.currentPrice * 100) / 100;
        crypto.totalReturn = Math.round((crypto.currentValue - crypto.totalCost) * 100) / 100;
        crypto.totalReturnPercent = crypto.totalCost > 0 ? Math.round((crypto.totalReturn / crypto.totalCost) * 10000) / 100 : 0;
        primary.amount = Math.round((primary.amount + netProceeds) * 100) / 100;
        crypto.transactions.push({
            id: `ctx_${String(this._nextCryptoTxId++).padStart(3, '0')}`,
            type: 'sell',
            quantity,
            pricePerUnit: crypto.currentPrice,
            total: netProceeds,
            fee,
            date: new Date().toISOString()
        });
        this.transactions.unshift({
            id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
            type: 'crypto_sell',
            description: `Sold ${crypto.name}`,
            amount: netProceeds,
            currency: 'USD',
            date: new Date().toISOString(),
            status: 'completed',
            paymentMethod: 'balance',
            category: 'Crypto'
        });
        this.notify();
        return true;
    },

    _calculateCryptoFee(amount) {
        for (const tier of CRYPTO_FEE_SCHEDULE) {
            if (amount >= tier.minAmount && (tier.maxAmount === null || amount <= tier.maxAmount)) {
                return tier.feePercent ? Math.round(amount * tier.feePercent) / 100 : tier.fee;
            }
        }
        return 0;
    },

    // ---- Savings Operations ----

    depositToSavings(amount) {
        const primary = this.getPrimaryBalance();
        if (!primary || primary.amount < amount || !this.savingsAccount) return false;
        primary.amount = Math.round((primary.amount - amount) * 100) / 100;
        this.savingsAccount.balance = Math.round((this.savingsAccount.balance + amount) * 100) / 100;
        this.savingsAccount.transferHistory.push({
            id: `stx_${String(this._nextSavingsTxId++).padStart(3, '0')}`,
            type: 'deposit',
            amount,
            date: new Date().toISOString(),
            from: 'PayPal Balance'
        });
        this.transactions.unshift({
            id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
            type: 'savings_deposit',
            description: 'Transfer to Savings',
            amount: -amount,
            currency: 'USD',
            date: new Date().toISOString(),
            status: 'completed',
            paymentMethod: 'balance',
            category: 'Savings'
        });
        this.notify();
        return true;
    },

    withdrawFromSavings(amount) {
        if (!this.savingsAccount || this.savingsAccount.balance < amount) return false;
        const primary = this.getPrimaryBalance();
        if (!primary) return false;
        this.savingsAccount.balance = Math.round((this.savingsAccount.balance - amount) * 100) / 100;
        primary.amount = Math.round((primary.amount + amount) * 100) / 100;
        this.savingsAccount.transferHistory.push({
            id: `stx_${String(this._nextSavingsTxId++).padStart(3, '0')}`,
            type: 'withdrawal',
            amount,
            date: new Date().toISOString(),
            to: 'PayPal Balance'
        });
        this.transactions.unshift({
            id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
            type: 'savings_withdrawal',
            description: 'Transfer from Savings',
            amount: amount,
            currency: 'USD',
            date: new Date().toISOString(),
            status: 'completed',
            paymentMethod: 'balance',
            category: 'Savings'
        });
        this.notify();
        return true;
    },

    // ---- Offers Operations ----

    saveOffer(offerId) {
        const offer = this.offers.find(o => o.id === offerId);
        if (offer && offer.status === 'available') {
            offer.status = 'saved';
            offer.savedAt = new Date().toISOString();
            this.notify();
            return true;
        }
        return false;
    },

    unsaveOffer(offerId) {
        const offer = this.offers.find(o => o.id === offerId);
        if (offer && offer.status === 'saved') {
            offer.status = 'available';
            offer.savedAt = null;
            this.notify();
            return true;
        }
        return false;
    },

    // ---- Rewards Operations ----

    redeemRewards(points, type) {
        if (!this.rewards || this.rewards.totalPoints < points) return false;
        const value = points / 100;
        this.rewards.totalPoints -= points;
        this.rewards.pointsValue = Math.round(this.rewards.totalPoints) / 100;
        this.rewards.history.unshift({
            id: `rwd_${String(this._nextRewardId++).padStart(3, '0')}`,
            description: type === 'balance' ? 'Redeemed for PayPal Balance' : 'Redeemed for Gift Card',
            points: -points,
            date: new Date().toISOString(),
            type: 'redeemed',
            redemptionValue: value
        });
        if (type === 'balance') {
            const primary = this.getPrimaryBalance();
            if (primary) {
                primary.amount = Math.round((primary.amount + value) * 100) / 100;
            }
        }
        this.notify();
        return true;
    },

    // ---- Gift Card Operations ----

    purchaseGiftCard(merchantName, amount, recipientEmail, recipientName, message) {
        const primary = this.getPrimaryBalance();
        if (!primary || primary.amount < amount) return false;
        primary.amount = Math.round((primary.amount - amount) * 100) / 100;
        const code = `${merchantName.substring(0, 3).toUpperCase()}-${this._randomCode()}-${this._randomCode()}-${this._randomCode()}`;
        const gc = {
            id: `gc_${String(this._nextGiftCardId++).padStart(3, '0')}`,
            merchantName,
            amount,
            remainingBalance: amount,
            status: 'active',
            purchasedAt: new Date().toISOString(),
            recipientEmail,
            recipientName,
            senderName: `${this.currentUser.firstName} ${this.currentUser.lastName}`,
            message,
            redemptionCode: code,
            redeemed: false
        };
        this.giftCards.unshift(gc);
        this.transactions.unshift({
            id: `txn_${String(this._nextTransactionId++).padStart(3, '0')}`,
            type: 'gift_card',
            description: `Gift Card - ${merchantName}`,
            amount: -amount,
            currency: 'USD',
            date: new Date().toISOString(),
            status: 'completed',
            paymentMethod: 'balance',
            category: 'Gift Cards'
        });
        this.notify();
        return gc;
    },

    _randomCode() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let result = '';
        for (let i = 0; i < 4; i++) result += chars[Math.floor(Math.random() * chars.length)];
        return result;
    },

    // ---- PayPal Credit Operations ----

    makePaypalCreditPayment(amount) {
        if (!this.paypalCredit) return false;
        const primary = this.getPrimaryBalance();
        if (!primary || primary.amount < amount) return false;
        primary.amount = Math.round((primary.amount - amount) * 100) / 100;
        this.paypalCredit.currentBalance = Math.max(0, Math.round((this.paypalCredit.currentBalance - amount) * 100) / 100);
        this.paypalCredit.availableCredit = Math.round((this.paypalCredit.creditLimit - this.paypalCredit.currentBalance) * 100) / 100;
        this.paypalCredit.lastPaymentAmount = amount;
        this.paypalCredit.lastPaymentDate = new Date().toISOString();
        if (this.paypalCredit.currentBalance <= 0) {
            this.paypalCredit.minimumPaymentDue = 0;
        }
        this.notify();
        return true;
    },

    toggleAutopay() {
        if (!this.paypalCredit) return;
        this.paypalCredit.autopayEnabled = !this.paypalCredit.autopayEnabled;
        this.notify();
    },

    setAutopayAmount(type) {
        if (!this.paypalCredit) return;
        this.paypalCredit.autopayAmount = type;
        this.notify();
    },

    // ---- Debit Card Operations ----

    updateDebitCardPin() {
        if (this.paypalDebitCard) {
            this.paypalDebitCard.pinSet = true;
            this.notify();
        }
    },

    setDailySpendingLimit(amount) {
        if (this.paypalDebitCard) {
            this.paypalDebitCard.dailySpendingLimit = amount;
            this.notify();
        }
    },

    setDailyATMLimit(amount) {
        if (this.paypalDebitCard) {
            this.paypalDebitCard.dailyATMLimit = amount;
            this.notify();
        }
    },

    toggleCashBack() {
        if (this.paypalDebitCard) {
            this.paypalDebitCard.cashBackEnabled = !this.paypalDebitCard.cashBackEnabled;
            this.notify();
        }
    },

    setCashBackCategory(category) {
        if (this.paypalDebitCard && this.paypalDebitCard.cashBackCategories.includes(category)) {
            this.paypalDebitCard.cashBackCategory = category;
            this.notify();
        }
    },

    updateDirectDeposit(data) {
        if (this.paypalDebitCard) {
            Object.assign(this.paypalDebitCard.directDeposit, data);
            this.notify();
        }
    },

    // ---- Preferences Operations ----

    updatePreference(key, value) {
        if (this.walletPreferences) {
            if (key.includes('.')) {
                const parts = key.split('.');
                let obj = this.walletPreferences;
                for (let i = 0; i < parts.length - 1; i++) {
                    obj = obj[parts[i]];
                }
                obj[parts[parts.length - 1]] = value;
            } else {
                this.walletPreferences[key] = value;
            }
            this.notify();
        }
    },

    setPreferredPaymentMethod(id) {
        this.cards.forEach(c => c.isPreferred = false);
        const card = this.getCardById(id);
        if (card) {
            card.isPreferred = true;
        }
        this.walletPreferences.preferredPaymentMethod = id;
        this.currentUser.preferredPaymentMethodId = id;
        this.notify();
    },

    setBackupPaymentMethod(id) {
        this.cards.forEach(c => c.isBackup = false);
        const card = this.getCardById(id);
        const bank = this.getBankById(id);
        if (card) card.isBackup = true;
        this.walletPreferences.backupPaymentMethod = id;
        this.currentUser.backupPaymentMethodId = id;
        this.notify();
    },

    // ---- Transaction Queries ----

    getFilteredTransactions() {
        let txns = [...this.transactions];
        if (this.transactionFilter !== 'all') {
            txns = txns.filter(t => {
                switch (this.transactionFilter) {
                    case 'payments': return t.type === 'payment';
                    case 'received': return t.type === 'received' || t.type === 'refund';
                    case 'transfers': return t.type === 'transfer_in' || t.type === 'transfer_out';
                    case 'crypto': return t.type === 'crypto_buy' || t.type === 'crypto_sell';
                    case 'pending': return t.status === 'pending';
                    default: return true;
                }
            });
        }
        if (this.searchQuery) {
            const q = this.searchQuery.toLowerCase();
            txns = txns.filter(t =>
                t.description.toLowerCase().includes(q) ||
                t.category.toLowerCase().includes(q)
            );
        }
        if (this.transactionDateFilter !== 'all') {
            const now = new Date();
            let cutoff;
            switch (this.transactionDateFilter) {
                case '7days': cutoff = new Date(now - 7 * 86400000); break;
                case '30days': cutoff = new Date(now - 30 * 86400000); break;
                case '90days': cutoff = new Date(now - 90 * 86400000); break;
                default: cutoff = null;
            }
            if (cutoff) {
                txns = txns.filter(t => new Date(t.date) >= cutoff);
            }
        }
        return txns.sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    getPaginatedTransactions() {
        const filtered = this.getFilteredTransactions();
        const start = (this.currentPage - 1) * this.itemsPerPage;
        return {
            transactions: filtered.slice(start, start + this.itemsPerPage),
            totalCount: filtered.length,
            totalPages: Math.ceil(filtered.length / this.itemsPerPage),
            currentPage: this.currentPage
        };
    }
};
