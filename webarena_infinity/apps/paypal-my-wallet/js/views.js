// ============================================================
// views.js — View rendering functions for PayPal My Wallet
// ============================================================

const Views = {

    render() {
        const app = document.getElementById('app-content');
        if (!app) return;

        switch (AppState.currentView) {
            case 'overview': app.innerHTML = this.renderOverview(); break;
            case 'cards': app.innerHTML = this.renderCards(); break;
            case 'banks': app.innerHTML = this.renderBanks(); break;
            case 'balance': app.innerHTML = this.renderBalance(); break;
            case 'crypto': app.innerHTML = this.renderCrypto(); break;
            case 'debit-card': app.innerHTML = this.renderDebitCard(); break;
            case 'savings': app.innerHTML = this.renderSavings(); break;
            case 'pay-later': app.innerHTML = this.renderPayLater(); break;
            case 'credit': app.innerHTML = this.renderCredit(); break;
            case 'rewards': app.innerHTML = this.renderRewards(); break;
            case 'offers': app.innerHTML = this.renderOffers(); break;
            case 'gift-cards': app.innerHTML = this.renderGiftCards(); break;
            case 'transactions': app.innerHTML = this.renderTransactions(); break;
            case 'preferences': app.innerHTML = this.renderPreferences(); break;
            default: app.innerHTML = this.renderOverview();
        }
        this.updateSidebar();
    },

    updateSidebar() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.view === AppState.currentView);
        });
    },

    // ================================================================
    // OVERVIEW
    // ================================================================
    renderOverview() {
        const primary = AppState.getPrimaryBalance();
        const totalCrypto = AppState.cryptoHoldings.reduce((sum, c) => sum + c.currentValue, 0);
        const activeCards = AppState.cards.filter(c => c.status !== 'expired').length;
        const activeBanks = AppState.bankAccounts.filter(b => b.status === 'confirmed').length;
        const activePlans = AppState.payLaterPlans.filter(p => p.status === 'active').length;

        return `
            <div class="page-header">
                <h1>My Wallet</h1>
                <p class="page-subtitle">Welcome back, ${AppState.currentUser.firstName}</p>
            </div>

            <div class="overview-cards-grid">
                <div class="overview-card balance-card" data-action="navigate" data-view="balance">
                    <div class="overview-card-header">
                        <span class="material-icons">account_balance_wallet</span>
                        <span>PayPal Balance</span>
                    </div>
                    <div class="overview-card-value">${Components.formatCurrency(primary ? primary.amount : 0)}</div>
                    <div class="overview-card-footer">${AppState.balances.length} currencies</div>
                </div>

                <div class="overview-card savings-card" data-action="navigate" data-view="savings">
                    <div class="overview-card-header">
                        <span class="material-icons">savings</span>
                        <span>Savings</span>
                    </div>
                    <div class="overview-card-value">${Components.formatCurrency(AppState.savingsAccount ? AppState.savingsAccount.balance : 0)}</div>
                    <div class="overview-card-footer">${AppState.savingsAccount ? AppState.savingsAccount.apy : 0}% APY</div>
                </div>

                <div class="overview-card crypto-card" data-action="navigate" data-view="crypto">
                    <div class="overview-card-header">
                        <span class="material-icons">currency_bitcoin</span>
                        <span>Crypto</span>
                    </div>
                    <div class="overview-card-value">${Components.formatCurrency(totalCrypto)}</div>
                    <div class="overview-card-footer">${AppState.cryptoHoldings.filter(c => c.quantity > 0).length} assets</div>
                </div>

                <div class="overview-card rewards-card" data-action="navigate" data-view="rewards">
                    <div class="overview-card-header">
                        <span class="material-icons">star</span>
                        <span>Rewards</span>
                    </div>
                    <div class="overview-card-value">${AppState.rewards ? AppState.rewards.totalPoints.toLocaleString() : 0} pts</div>
                    <div class="overview-card-footer">Worth ${Components.formatCurrency(AppState.rewards ? AppState.rewards.pointsValue : 0)}</div>
                </div>
            </div>

            ${Components.renderSectionHeader('Payment Methods', `<button class="btn btn-sm btn-outline" data-action="navigate" data-view="cards">View All</button>`)}
            <div class="payment-methods-list">
                ${AppState.cards.filter(c => c.status !== 'expired').slice(0, 3).map(card => `
                    <div class="payment-method-item" data-action="navigate" data-view="cards" data-id="${card.id}">
                        ${Components.renderCardVisual(card, true)}
                        ${Components.renderStatusBadge(card.status)}
                    </div>
                `).join('')}
                ${AppState.bankAccounts.filter(b => b.status === 'confirmed').slice(0, 2).map(bank => `
                    <div class="payment-method-item" data-action="navigate" data-view="banks" data-id="${bank.id}">
                        <div class="card-visual-compact bank">
                            <span class="material-icons">account_balance</span>
                            <span class="card-last-four">${bank.bankName} &bull;&bull;&bull;&bull; ${bank.lastFour}</span>
                            <span class="card-type-label">${bank.accountType}</span>
                        </div>
                        ${Components.renderStatusBadge(bank.status)}
                    </div>
                `).join('')}
            </div>

            ${activePlans > 0 ? `
                ${Components.renderSectionHeader('Active Pay Later Plans', `<button class="btn btn-sm btn-outline" data-action="navigate" data-view="pay-later">View All</button>`)}
                <div class="plans-summary">
                    ${AppState.payLaterPlans.filter(p => p.status === 'active').map(plan => {
                        const paidCount = plan.payments.filter(p => p.status === 'paid').length;
                        return `
                            <div class="plan-summary-item" data-action="navigate" data-view="pay-later" data-id="${plan.id}">
                                <div class="plan-merchant">${plan.merchantName}</div>
                                <div class="plan-amount">${Components.formatCurrency(plan.totalAmount)}</div>
                                ${Components.renderProgressBar(paidCount, 4, `${paidCount}/4 payments`)}
                            </div>
                        `;
                    }).join('')}
                </div>
            ` : ''}

            ${Components.renderSectionHeader('Recent Activity', `<button class="btn btn-sm btn-outline" data-action="navigate" data-view="transactions">View All</button>`)}
            <div class="transactions-list">
                ${AppState.transactions.slice(0, 5).map(txn => this._renderTransactionRow(txn)).join('')}
            </div>
        `;
    },

    // ================================================================
    // CARDS
    // ================================================================
    renderCards() {
        const activeCards = AppState.cards.filter(c => c.status !== 'expired');
        const expiredCards = AppState.cards.filter(c => c.status === 'expired');

        return `
            <div class="page-header">
                <h1>Cards</h1>
                <button class="btn btn-primary" data-action="open-add-card-modal">
                    <span class="material-icons">add</span> Link a Card
                </button>
            </div>

            <div class="cards-grid">
                ${activeCards.map(card => `
                    <div class="card-item" data-card-id="${card.id}">
                        ${Components.renderCardVisual(card)}
                        <div class="card-item-details">
                            <div class="card-item-status">
                                ${Components.renderStatusBadge(card.status)}
                                ${card.type === 'debit' && card.instantTransferEligible ? '<span class="status-badge badge-info">Instant Transfer</span>' : ''}
                            </div>
                            <div class="card-item-info">
                                <span>Added ${Components.formatDate(card.addedAt)}</span>
                                ${card.lastUsed ? `<span>Last used ${Components.formatRelativeDate(card.lastUsed)}</span>` : ''}
                            </div>
                            <div class="card-item-actions">
                                ${card.status === 'pending_confirmation' ? `<button class="btn btn-sm btn-primary" data-action="confirm-card" data-id="${card.id}">Confirm Card</button>` : ''}
                                <button class="btn btn-sm btn-outline" data-action="open-edit-card-modal" data-id="${card.id}">Update</button>
                                ${card.status === 'confirmed' && !card.isPreferred ? `<button class="btn btn-sm btn-outline" data-action="set-preferred-card" data-id="${card.id}">Set as Preferred</button>` : ''}
                                <button class="btn btn-sm btn-danger-outline" data-action="remove-card" data-id="${card.id}">Remove</button>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>

            ${expiredCards.length > 0 ? `
                ${Components.renderSectionHeader('Expired Cards')}
                <div class="cards-grid">
                    ${expiredCards.map(card => `
                        <div class="card-item expired">
                            ${Components.renderCardVisual(card)}
                            <div class="card-item-details">
                                <div class="card-item-status">${Components.renderStatusBadge('expired')}</div>
                                <div class="card-item-info">
                                    <span>Expired ${String(card.expirationMonth).padStart(2, '0')}/${card.expirationYear}</span>
                                </div>
                                <div class="card-item-actions">
                                    <button class="btn btn-sm btn-outline" data-action="open-edit-card-modal" data-id="${card.id}">Update Expiration</button>
                                    <button class="btn btn-sm btn-danger-outline" data-action="remove-card" data-id="${card.id}">Remove</button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        `;
    },

    // ================================================================
    // BANK ACCOUNTS
    // ================================================================
    renderBanks() {
        return `
            <div class="page-header">
                <h1>Bank Accounts</h1>
                <button class="btn btn-primary" data-action="open-add-bank-modal">
                    <span class="material-icons">add</span> Link a Bank
                </button>
            </div>

            <div class="bank-list">
                ${AppState.bankAccounts.map(bank => `
                    <div class="bank-item" data-bank-id="${bank.id}">
                        <div class="bank-item-left">
                            <div class="bank-icon">
                                <span class="material-icons">account_balance</span>
                            </div>
                            <div class="bank-item-info">
                                <div class="bank-item-name">${bank.bankName}</div>
                                <div class="bank-item-detail">${bank.accountType.charAt(0).toUpperCase() + bank.accountType.slice(1)} &bull;&bull;&bull;&bull; ${bank.lastFour}</div>
                                <div class="bank-item-meta">
                                    Added ${Components.formatDate(bank.addedAt)}
                                    ${bank.lastUsed ? ` &middot; Last used ${Components.formatRelativeDate(bank.lastUsed)}` : ''}
                                </div>
                            </div>
                        </div>
                        <div class="bank-item-right">
                            <div class="bank-item-badges">
                                ${Components.renderStatusBadge(bank.status)}
                                ${bank.instantTransferEligible ? '<span class="status-badge badge-info">Instant Transfer</span>' : ''}
                            </div>
                            <div class="bank-item-actions">
                                ${bank.status === 'pending_confirmation' ? `<button class="btn btn-sm btn-primary" data-action="open-confirm-bank-modal" data-id="${bank.id}">Confirm</button>` : ''}
                                <button class="btn btn-sm btn-danger-outline" data-action="remove-bank" data-id="${bank.id}">Remove</button>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>

            ${AppState.bankAccounts.length === 0 ? Components.renderEmptyState('account_balance', 'No Bank Accounts', 'Link a bank account to transfer money to and from PayPal.') : ''}
        `;
    },

    // ================================================================
    // BALANCE
    // ================================================================
    renderBalance() {
        const totalUSD = AppState.getTotalBalanceUSD();
        const activeCurrencies = AppState.balances;

        return `
            <div class="page-header">
                <h1>PayPal Balance</h1>
                <div class="page-header-actions">
                    <button class="btn btn-primary" data-action="open-add-money-modal">
                        <span class="material-icons">add</span> Add Money
                    </button>
                    <button class="btn btn-outline" data-action="open-withdraw-modal">
                        <span class="material-icons">arrow_upward</span> Withdraw
                    </button>
                </div>
            </div>

            <div class="balance-summary-card">
                <div class="balance-total-label">Total Balance (USD equivalent)</div>
                <div class="balance-total-amount">${Components.formatCurrency(totalUSD)}</div>
            </div>

            ${Components.renderSectionHeader('Currencies', `
                <button class="btn btn-sm btn-outline" data-action="open-add-currency-modal">
                    <span class="material-icons">add</span> Add Currency
                </button>
                <button class="btn btn-sm btn-outline" data-action="open-convert-currency-modal">
                    <span class="material-icons">currency_exchange</span> Convert
                </button>
            `)}

            <div class="currency-list">
                ${activeCurrencies.map(bal => {
                    const curr = CURRENCIES.find(c => c.code === bal.currency);
                    return `
                        <div class="currency-item">
                            <div class="currency-item-left">
                                <div class="currency-code">${bal.currency}</div>
                                <div class="currency-name">${curr ? curr.name : bal.currency}</div>
                                ${bal.isPrimary ? '<span class="status-badge badge-primary">Primary</span>' : ''}
                            </div>
                            <div class="currency-item-right">
                                <div class="currency-amount">${Components.formatCurrency(bal.amount, bal.currency)}</div>
                                <div class="currency-actions">
                                    ${!bal.isPrimary ? `<button class="btn btn-xs btn-outline" data-action="set-primary-currency" data-currency="${bal.currency}">Set Primary</button>` : ''}
                                    ${!bal.isPrimary && bal.amount === 0 ? `<button class="btn btn-xs btn-danger-outline" data-action="remove-currency" data-currency="${bal.currency}">Remove</button>` : ''}
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>

            ${Components.renderSectionHeader('Exchange Rates')}
            <div class="exchange-rates-grid">
                ${['EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF'].map(code => {
                    const curr = CURRENCIES.find(c => c.code === code);
                    const rate = EXCHANGE_RATES[code];
                    return `
                        <div class="exchange-rate-card">
                            <div class="exchange-rate-pair">USD / ${code}</div>
                            <div class="exchange-rate-value">${rate.toFixed(code === 'JPY' ? 2 : 4)}</div>
                            <div class="exchange-rate-name">${curr ? curr.name : code}</div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    },

    // ================================================================
    // CRYPTO
    // ================================================================
    renderCrypto() {
        const totalValue = AppState.cryptoHoldings.reduce((sum, c) => sum + c.currentValue, 0);
        const totalCost = AppState.cryptoHoldings.reduce((sum, c) => sum + c.totalCost, 0);
        const totalReturn = totalValue - totalCost;
        const totalReturnPct = totalCost > 0 ? (totalReturn / totalCost) * 100 : 0;

        return `
            <div class="page-header">
                <h1>Cryptocurrency</h1>
            </div>

            <div class="crypto-summary-card">
                <div class="crypto-summary-left">
                    <div class="crypto-total-label">Total Portfolio Value</div>
                    <div class="crypto-total-value">${Components.formatCurrency(totalValue)}</div>
                    <div class="crypto-total-return">
                        ${Components.renderCryptoChange(totalReturnPct)}
                        <span class="crypto-return-amount">(${Components.formatCurrency(totalReturn)})</span>
                    </div>
                </div>
            </div>

            ${Components.renderSectionHeader('Your Assets')}
            <div class="crypto-list">
                ${AppState.cryptoHoldings.map(crypto => `
                    <div class="crypto-item ${crypto.quantity === 0 ? 'zero-balance' : ''}" data-crypto-id="${crypto.id}">
                        <div class="crypto-item-left">
                            <div class="crypto-symbol-badge">${crypto.symbol}</div>
                            <div class="crypto-item-info">
                                <div class="crypto-item-name">${crypto.name}</div>
                                <div class="crypto-item-qty">${crypto.quantity > 0 ? `${crypto.quantity.toFixed(5)} ${crypto.symbol}` : 'No holdings'}</div>
                            </div>
                        </div>
                        <div class="crypto-item-center">
                            <div class="crypto-item-price">${Components.formatCurrency(crypto.currentPrice)}</div>
                            <div class="crypto-item-price-label">Current Price</div>
                        </div>
                        <div class="crypto-item-right">
                            ${crypto.quantity > 0 ? `
                                <div class="crypto-item-value">${Components.formatCurrency(crypto.currentValue)}</div>
                                ${Components.renderCryptoChange(crypto.totalReturnPercent)}
                            ` : `
                                <div class="crypto-item-value">$0.00</div>
                            `}
                        </div>
                        <div class="crypto-item-actions">
                            <button class="btn btn-sm btn-primary" data-action="open-buy-crypto-modal" data-symbol="${crypto.symbol}">Buy</button>
                            ${crypto.quantity > 0 ? `<button class="btn btn-sm btn-outline" data-action="open-sell-crypto-modal" data-symbol="${crypto.symbol}">Sell</button>` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>

            ${Components.renderSectionHeader('Fee Schedule')}
            <div class="fee-schedule">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Purchase Amount</th>
                            <th>Fee</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${CRYPTO_FEE_SCHEDULE.map(tier => `
                            <tr>
                                <td>${Components.formatCurrency(tier.minAmount)} - ${tier.maxAmount ? Components.formatCurrency(tier.maxAmount) : 'Above'}</td>
                                <td>${tier.feePercent ? `${tier.feePercent}%` : Components.formatCurrency(tier.fee)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    },

    // ================================================================
    // DEBIT CARD
    // ================================================================
    renderDebitCard() {
        const dc = AppState.paypalDebitCard;
        if (!dc) return Components.renderEmptyState('credit_card', 'No PayPal Debit Card', 'Apply for a PayPal Debit Card to access your balance anywhere.');

        return `
            <div class="page-header">
                <h1>PayPal Debit Card</h1>
            </div>

            <div class="debit-card-visual">
                <div class="card-visual mastercard debit-main-card">
                    <div class="card-visual-top">
                        <span class="card-brand mastercard">PayPal Debit</span>
                        ${Components.renderStatusBadge(dc.status)}
                    </div>
                    <div class="card-visual-number">&bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; ${dc.lastFour}</div>
                    <div class="card-visual-bottom">
                        <div class="card-visual-name">${dc.cardholderName}</div>
                        <div class="card-visual-exp">${dc.brand}</div>
                    </div>
                </div>
            </div>

            ${Components.renderSectionHeader('Card Settings')}
            <div class="settings-card">
                ${Components.renderToggle('debit-cashback-toggle', dc.cashBackEnabled, `Cash Back (${dc.cashBackPercent}%)`, 'debit-cashback')}
                ${dc.cashBackEnabled ? `
                    <div class="divider"></div>
                    ${Components.renderInfoRow('Cash Back Category',
                        Components.renderDropdown('cashback-category-dropdown',
                            dc.cashBackCategories.map(c => ({ value: c, label: c })),
                            dc.cashBackCategory,
                            'Select category'
                        )
                    )}
                ` : ''}
                <div class="divider"></div>

                ${Components.renderInfoRow('PIN Status', dc.pinSet ? 'Set' : 'Not Set',
                    `<button class="btn btn-sm btn-outline" data-action="open-change-pin-modal">Change PIN</button>`
                )}
                <div class="divider"></div>

                ${Components.renderInfoRow('Daily Spending Limit', Components.formatCurrency(dc.dailySpendingLimit),
                    `<button class="btn btn-sm btn-outline" data-action="open-spending-limit-modal">Change</button>`
                )}
                <div class="divider"></div>

                ${Components.renderInfoRow('Daily ATM Limit', Components.formatCurrency(dc.dailyATMLimit),
                    `<button class="btn btn-sm btn-outline" data-action="open-atm-limit-modal">Change</button>`
                )}
                <div class="divider"></div>

                ${Components.renderInfoRow('Activated', Components.formatDate(dc.activatedAt))}
            </div>

            ${Components.renderSectionHeader('Direct Deposit')}
            <div class="settings-card">
                ${Components.renderToggle('direct-deposit-toggle', dc.directDeposit.enabled, 'Direct Deposit', 'direct-deposit')}
                ${dc.directDeposit.enabled ? `
                    <div class="divider"></div>
                    ${Components.renderInfoRow('Routing Number', dc.directDeposit.routingNumber)}
                    <div class="divider"></div>
                    ${Components.renderInfoRow('Account Number', dc.directDeposit.accountNumber)}
                    <div class="divider"></div>
                    ${Components.renderInfoRow('Employer', dc.directDeposit.employer || 'Not set',
                        `<button class="btn btn-sm btn-outline" data-action="open-edit-employer-modal">Edit</button>`
                    )}
                ` : ''}
            </div>
        `;
    },

    // ================================================================
    // SAVINGS
    // ================================================================
    renderSavings() {
        const sav = AppState.savingsAccount;
        if (!sav) return Components.renderEmptyState('savings', 'No Savings Account', 'Open a PayPal Savings account to earn interest on your money.');

        return `
            <div class="page-header">
                <h1>PayPal Savings</h1>
                <div class="page-header-actions">
                    <button class="btn btn-primary" data-action="open-savings-deposit-modal">
                        <span class="material-icons">add</span> Deposit
                    </button>
                    <button class="btn btn-outline" data-action="open-savings-withdraw-modal">
                        <span class="material-icons">arrow_upward</span> Withdraw
                    </button>
                </div>
            </div>

            <div class="savings-summary-card">
                <div class="savings-balance-label">Savings Balance</div>
                <div class="savings-balance-amount">${Components.formatCurrency(sav.balance)}</div>
                <div class="savings-apy">${sav.apy}% APY</div>
            </div>

            <div class="savings-stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Interest This Month</div>
                    <div class="stat-value">${Components.formatCurrency(sav.interestEarnedThisMonth)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Interest YTD</div>
                    <div class="stat-value">${Components.formatCurrency(sav.interestEarnedYTD)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Interest All Time</div>
                    <div class="stat-value">${Components.formatCurrency(sav.interestEarnedAllTime)}</div>
                </div>
            </div>

            ${Components.renderSectionHeader('Transfer History')}
            <div class="savings-history">
                ${sav.transferHistory.slice().reverse().map(tx => `
                    <div class="savings-tx-row">
                        <div class="savings-tx-left">
                            <span class="material-icons">${tx.type === 'deposit' ? 'arrow_downward' : 'arrow_upward'}</span>
                            <div>
                                <div class="savings-tx-type">${tx.type === 'deposit' ? 'Deposit' : 'Withdrawal'}</div>
                                <div class="savings-tx-detail">${tx.type === 'deposit' ? `From ${tx.from}` : `To ${tx.to}`}</div>
                            </div>
                        </div>
                        <div class="savings-tx-right">
                            <div class="savings-tx-amount ${tx.type === 'deposit' ? 'positive' : 'negative'}">
                                ${tx.type === 'deposit' ? '+' : '-'}${Components.formatCurrency(tx.amount)}
                            </div>
                            <div class="savings-tx-date">${Components.formatDate(tx.date)}</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    },

    // ================================================================
    // PAY LATER
    // ================================================================
    renderPayLater() {
        const activePlans = AppState.payLaterPlans.filter(p => p.status === 'active');
        const completedPlans = AppState.payLaterPlans.filter(p => p.status === 'completed');

        return `
            <div class="page-header">
                <h1>Pay in 4</h1>
            </div>

            <div class="pay-later-info-card">
                <span class="material-icons">info</span>
                <div>
                    <strong>Pay in 4 interest-free payments</strong>
                    <p>Split your purchase into 4 payments, every 2 weeks. No interest, no fees when you pay on time.</p>
                </div>
            </div>

            ${activePlans.length > 0 ? `
                ${Components.renderSectionHeader('Active Plans')}
                <div class="plans-list">
                    ${activePlans.map(plan => this._renderPlanCard(plan)).join('')}
                </div>
            ` : Components.renderEmptyState('credit_score', 'No Active Plans', 'Your Pay in 4 plans will appear here.')}

            ${completedPlans.length > 0 ? `
                ${Components.renderSectionHeader('Completed Plans')}
                <div class="plans-list">
                    ${completedPlans.map(plan => this._renderPlanCard(plan)).join('')}
                </div>
            ` : ''}
        `;
    },

    _renderPlanCard(plan) {
        const paidCount = plan.payments.filter(p => p.status === 'paid').length;
        const nextPayment = plan.payments.find(p => p.status === 'upcoming');
        const paymentMethod = AppState.getCardById(plan.paymentMethodId);

        return `
            <div class="plan-card" data-plan-id="${plan.id}">
                <div class="plan-card-header">
                    <div>
                        <div class="plan-merchant-name">${plan.merchantName}</div>
                        <div class="plan-order-date">Ordered ${Components.formatDate(plan.orderDate)}</div>
                    </div>
                    <div class="plan-total">${Components.formatCurrency(plan.totalAmount)}</div>
                </div>
                ${Components.renderProgressBar(paidCount, 4, `${paidCount} of 4 payments completed`)}
                <div class="plan-payments-grid">
                    ${plan.payments.map(p => `
                        <div class="plan-payment ${p.status}">
                            <div class="plan-payment-num">Payment ${p.number}</div>
                            <div class="plan-payment-amount">${Components.formatCurrency(p.amount)}</div>
                            <div class="plan-payment-date">${p.status === 'paid' ? `Paid ${Components.formatDate(p.paidDate)}` : `Due ${Components.formatDate(p.dueDate)}`}</div>
                            ${Components.renderStatusBadge(p.status)}
                        </div>
                    `).join('')}
                </div>
                ${paymentMethod ? `
                    <div class="plan-payment-method">
                        Payment method: ${paymentMethod.brand} &bull;&bull;&bull;&bull; ${paymentMethod.lastFour}
                    </div>
                ` : ''}
            </div>
        `;
    },

    // ================================================================
    // CREDIT
    // ================================================================
    renderCredit() {
        const credit = AppState.paypalCredit;
        if (!credit) return Components.renderEmptyState('credit_card', 'No PayPal Credit', 'Apply for PayPal Credit to get a line of credit.');

        const usedPct = (credit.currentBalance / credit.creditLimit) * 100;

        return `
            <div class="page-header">
                <h1>PayPal Credit</h1>
            </div>

            <div class="credit-summary-card">
                <div class="credit-summary-top">
                    <div>
                        <div class="credit-label">Available Credit</div>
                        <div class="credit-available">${Components.formatCurrency(credit.availableCredit)}</div>
                    </div>
                    <div>
                        <div class="credit-label">Credit Limit</div>
                        <div class="credit-limit-val">${Components.formatCurrency(credit.creditLimit)}</div>
                    </div>
                </div>
                ${Components.renderProgressBar(credit.currentBalance, credit.creditLimit, `${Components.formatCurrency(credit.currentBalance)} used of ${Components.formatCurrency(credit.creditLimit)}`)}
            </div>

            <div class="credit-details-grid">
                <div class="stat-card">
                    <div class="stat-label">Current Balance</div>
                    <div class="stat-value">${Components.formatCurrency(credit.currentBalance)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Minimum Payment Due</div>
                    <div class="stat-value">${Components.formatCurrency(credit.minimumPaymentDue)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Payment Due Date</div>
                    <div class="stat-value">${Components.formatDate(credit.paymentDueDate)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">APR</div>
                    <div class="stat-value">${credit.apr}%</div>
                </div>
            </div>

            ${Components.renderSectionHeader('Make a Payment')}
            <div class="settings-card">
                <button class="btn btn-primary" data-action="open-credit-payment-modal" style="width:100%">
                    Make a Payment
                </button>
            </div>

            ${Components.renderSectionHeader('AutoPay Settings')}
            <div class="settings-card">
                ${Components.renderToggle('autopay-toggle', credit.autopayEnabled, 'AutoPay', 'autopay')}
                ${credit.autopayEnabled ? `
                    <div class="divider"></div>
                    <div class="autopay-options">
                        <label class="radio-option ${credit.autopayAmount === 'minimum' ? 'selected' : ''}">
                            <input type="radio" name="autopay-amount" value="minimum" ${credit.autopayAmount === 'minimum' ? 'checked' : ''} data-action="set-autopay-amount">
                            <span>Minimum Payment Due</span>
                        </label>
                        <label class="radio-option ${credit.autopayAmount === 'statement' ? 'selected' : ''}">
                            <input type="radio" name="autopay-amount" value="statement" ${credit.autopayAmount === 'statement' ? 'checked' : ''} data-action="set-autopay-amount">
                            <span>Statement Balance</span>
                        </label>
                        <label class="radio-option ${credit.autopayAmount === 'full' ? 'selected' : ''}">
                            <input type="radio" name="autopay-amount" value="full" ${credit.autopayAmount === 'full' ? 'checked' : ''} data-action="set-autopay-amount">
                            <span>Full Balance</span>
                        </label>
                    </div>
                ` : ''}
            </div>

            ${Components.renderSectionHeader('Account Details')}
            <div class="settings-card">
                ${Components.renderInfoRow('Last Statement Date', Components.formatDate(credit.lastStatementDate))}
                <div class="divider"></div>
                ${Components.renderInfoRow('Last Statement Balance', Components.formatCurrency(credit.lastStatementBalance))}
                <div class="divider"></div>
                ${Components.renderInfoRow('Last Payment', `${Components.formatCurrency(credit.lastPaymentAmount)} on ${Components.formatDate(credit.lastPaymentDate)}`)}
            </div>
        `;
    },

    // ================================================================
    // REWARDS
    // ================================================================
    renderRewards() {
        const rwd = AppState.rewards;
        if (!rwd) return Components.renderEmptyState('star', 'No Rewards', 'Earn rewards points on qualifying purchases.');

        return `
            <div class="page-header">
                <h1>Rewards</h1>
                <button class="btn btn-primary" data-action="open-redeem-rewards-modal">
                    <span class="material-icons">redeem</span> Redeem Points
                </button>
            </div>

            <div class="rewards-summary-card">
                <div class="rewards-points-display">
                    <div class="rewards-points-number">${rwd.totalPoints.toLocaleString()}</div>
                    <div class="rewards-points-label">Points Available</div>
                </div>
                <div class="rewards-value">Worth ${Components.formatCurrency(rwd.pointsValue)}</div>
                <div class="rewards-tier">
                    <span class="material-icons">workspace_premium</span> ${rwd.tier} Member
                </div>
            </div>

            <div class="rewards-stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Earned This Month</div>
                    <div class="stat-value">${rwd.earnedThisMonth.toLocaleString()} pts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Earned This Year</div>
                    <div class="stat-value">${rwd.earnedThisYear.toLocaleString()} pts</div>
                </div>
            </div>

            ${Components.renderSectionHeader('History')}
            <div class="rewards-history">
                ${rwd.history.map(item => `
                    <div class="reward-history-row">
                        <div class="reward-history-left">
                            <span class="material-icons">${item.type === 'earned' ? 'add_circle' : item.type === 'redeemed' ? 'remove_circle' : 'star'}</span>
                            <div>
                                <div class="reward-desc">${item.description}</div>
                                <div class="reward-date">${Components.formatDate(item.date)}</div>
                            </div>
                        </div>
                        <div class="reward-history-right ${item.points >= 0 ? 'positive' : 'negative'}">
                            ${item.points >= 0 ? '+' : ''}${item.points.toLocaleString()} pts
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    },

    // ================================================================
    // OFFERS
    // ================================================================
    renderOffers() {
        const savedOffers = AppState.offers.filter(o => o.status === 'saved');
        const availableOffers = AppState.offers.filter(o => o.status === 'available');
        const usedOffers = AppState.offers.filter(o => o.status === 'used');
        const expiredOffers = AppState.offers.filter(o => o.status === 'expired');

        const tabs = [
            { id: 'all', label: 'All', count: AppState.offers.length },
            { id: 'saved', label: 'Saved', count: savedOffers.length },
            { id: 'available', label: 'Available', count: availableOffers.length }
        ];

        const filter = AppState.offerFilter || 'all';
        let displayOffers;
        switch (filter) {
            case 'saved': displayOffers = savedOffers; break;
            case 'available': displayOffers = availableOffers; break;
            default: displayOffers = AppState.offers;
        }

        return `
            <div class="page-header">
                <h1>Offers</h1>
            </div>

            ${Components.renderTabs(tabs, filter)}

            <div class="offers-grid">
                ${displayOffers.map(offer => `
                    <div class="offer-card ${offer.status}">
                        <div class="offer-card-header">
                            <div class="offer-merchant-icon">${offer.merchantName.charAt(0)}</div>
                            <div>
                                <div class="offer-merchant-name">${offer.merchantName}</div>
                                <div class="offer-category">${offer.category}</div>
                            </div>
                            ${Components.renderStatusBadge(offer.status)}
                        </div>
                        <div class="offer-description">${offer.description}</div>
                        <div class="offer-details">
                            ${offer.minPurchase > 0 ? `<span>Min. purchase: ${Components.formatCurrency(offer.minPurchase)}</span>` : ''}
                            <span>Max cashback: ${Components.formatCurrency(offer.maxCashback)}</span>
                        </div>
                        <div class="offer-expires">Expires ${Components.formatDate(offer.expiresAt)}</div>
                        <div class="offer-actions">
                            ${offer.status === 'available' ? `<button class="btn btn-sm btn-primary" data-action="save-offer" data-id="${offer.id}">Save Offer</button>` : ''}
                            ${offer.status === 'saved' ? `<button class="btn btn-sm btn-danger-outline" data-action="unsave-offer" data-id="${offer.id}">Remove</button>` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>

            ${displayOffers.length === 0 ? Components.renderEmptyState('local_offer', 'No Offers', 'Check back later for new offers.') : ''}
        `;
    },

    // ================================================================
    // GIFT CARDS
    // ================================================================
    renderGiftCards() {
        return `
            <div class="page-header">
                <h1>Gift Cards</h1>
                <button class="btn btn-primary" data-action="open-buy-gift-card-modal">
                    <span class="material-icons">card_giftcard</span> Buy Gift Card
                </button>
            </div>

            ${AppState.giftCards.length > 0 ? `
                ${Components.renderSectionHeader('Your Gift Cards')}
                <div class="gift-cards-list">
                    ${AppState.giftCards.map(gc => `
                        <div class="gift-card-item">
                            <div class="gift-card-icon">${gc.merchantName.charAt(0)}</div>
                            <div class="gift-card-info">
                                <div class="gift-card-merchant">${gc.merchantName}</div>
                                <div class="gift-card-recipient">To: ${gc.recipientName} (${gc.recipientEmail})</div>
                                <div class="gift-card-date">Purchased ${Components.formatDate(gc.purchasedAt)}</div>
                                ${gc.message ? `<div class="gift-card-message">"${gc.message}"</div>` : ''}
                            </div>
                            <div class="gift-card-right">
                                <div class="gift-card-amount">${Components.formatCurrency(gc.amount)}</div>
                                ${gc.remainingBalance !== gc.amount ? `<div class="gift-card-remaining">Remaining: ${Components.formatCurrency(gc.remainingBalance)}</div>` : ''}
                                ${Components.renderStatusBadge(gc.status)}
                            </div>
                        </div>
                    `).join('')}
                </div>
            ` : Components.renderEmptyState('card_giftcard', 'No Gift Cards', 'Buy and send digital gift cards to friends and family.')}
        `;
    },

    // ================================================================
    // TRANSACTIONS
    // ================================================================
    renderTransactions() {
        const { transactions, totalCount, totalPages, currentPage } = AppState.getPaginatedTransactions();

        const filterTabs = [
            { id: 'all', label: 'All' },
            { id: 'payments', label: 'Payments' },
            { id: 'received', label: 'Received' },
            { id: 'transfers', label: 'Transfers' },
            { id: 'crypto', label: 'Crypto' },
            { id: 'pending', label: 'Pending' }
        ];

        return `
            <div class="page-header">
                <h1>Transactions</h1>
            </div>

            <div class="transactions-filters">
                <div class="search-bar">
                    <span class="material-icons">search</span>
                    <input type="text" id="transaction-search" placeholder="Search transactions..."
                        value="${AppState.searchQuery}" data-action="search-transactions">
                </div>
                <div class="date-filter">
                    ${Components.renderDropdown('date-filter-dropdown',
                        [
                            { value: 'all', label: 'All Time' },
                            { value: '7days', label: 'Last 7 Days' },
                            { value: '30days', label: 'Last 30 Days' },
                            { value: '90days', label: 'Last 90 Days' }
                        ],
                        AppState.transactionDateFilter,
                        'Filter by date'
                    )}
                </div>
            </div>

            ${Components.renderTabs(filterTabs, AppState.transactionFilter)}

            <div class="transactions-list detailed">
                ${transactions.length > 0 ? transactions.map(txn => this._renderTransactionRow(txn, true)).join('') :
                    Components.renderEmptyState('receipt_long', 'No Transactions', 'No transactions match your filters.')}
            </div>

            ${Components.renderPagination(currentPage, totalPages, totalCount)}
        `;
    },

    _renderTransactionRow(txn, detailed = false) {
        const isPositive = txn.amount >= 0;
        const paymentMethodLabel = this._getPaymentMethodLabel(txn.paymentMethod);

        return `
            <div class="transaction-row ${txn.status === 'pending' ? 'pending' : ''}">
                <div class="transaction-icon ${isPositive ? 'positive' : 'negative'}">
                    <span class="material-icons">${Components.getTransactionIcon(txn.type)}</span>
                </div>
                <div class="transaction-info">
                    <div class="transaction-desc">${txn.description}</div>
                    <div class="transaction-meta">
                        ${Components.formatRelativeDate(txn.date)}
                        ${detailed && paymentMethodLabel ? ` &middot; ${paymentMethodLabel}` : ''}
                        ${txn.status === 'pending' ? ' &middot; Pending' : ''}
                    </div>
                </div>
                ${detailed ? `<div class="transaction-category">${txn.category}</div>` : ''}
                <div class="transaction-amount ${isPositive ? 'positive' : 'negative'}">
                    ${isPositive ? '+' : ''}${Components.formatCurrency(txn.amount, txn.currency)}
                </div>
            </div>
        `;
    },

    _getPaymentMethodLabel(pmId) {
        if (pmId === 'balance') return 'PayPal Balance';
        const card = AppState.getCardById(pmId);
        if (card) return `${card.brand} ****${card.lastFour}`;
        const bank = AppState.getBankById(pmId);
        if (bank) return `${bank.bankName} ****${bank.lastFour}`;
        return '';
    },

    // ================================================================
    // PREFERENCES
    // ================================================================
    renderPreferences() {
        const prefs = AppState.walletPreferences;
        if (!prefs) return '';

        const paymentMethods = [
            ...AppState.cards.filter(c => c.status === 'confirmed').map(c => ({
                value: c.id,
                label: `${c.brand} ****${c.lastFour} (${c.type})`
            })),
            ...AppState.bankAccounts.filter(b => b.status === 'confirmed').map(b => ({
                value: b.id,
                label: `${b.bankName} ****${b.lastFour} (${b.accountType})`
            }))
        ];

        return `
            <div class="page-header">
                <h1>Payment Preferences</h1>
            </div>

            ${Components.renderSectionHeader('Default Payment Methods')}
            <div class="settings-card">
                <div class="form-group">
                    <label class="form-label">Preferred Payment Method</label>
                    ${Components.renderDropdown('preferred-payment-dropdown', paymentMethods, prefs.preferredPaymentMethod, 'Select preferred method')}
                </div>
                <div class="divider"></div>
                <div class="form-group">
                    <label class="form-label">Backup Payment Method</label>
                    ${Components.renderDropdown('backup-payment-dropdown', paymentMethods, prefs.backupPaymentMethod, 'Select backup method')}
                </div>
            </div>

            ${Components.renderSectionHeader('Currency Conversion')}
            <div class="settings-card">
                <div class="radio-group">
                    <label class="radio-option ${prefs.currencyConversionOption === 'paypal' ? 'selected' : ''}">
                        <input type="radio" name="currency-conversion" value="paypal"
                            ${prefs.currencyConversionOption === 'paypal' ? 'checked' : ''}
                            data-action="set-currency-conversion">
                        <div>
                            <strong>Convert with PayPal</strong>
                            <p>PayPal will handle the currency conversion at the time of purchase</p>
                        </div>
                    </label>
                    <label class="radio-option ${prefs.currencyConversionOption === 'card_issuer' ? 'selected' : ''}">
                        <input type="radio" name="currency-conversion" value="card_issuer"
                            ${prefs.currencyConversionOption === 'card_issuer' ? 'checked' : ''}
                            data-action="set-currency-conversion">
                        <div>
                            <strong>Convert with Card Issuer</strong>
                            <p>Your card issuer will handle the currency conversion</p>
                        </div>
                    </label>
                </div>
            </div>

            ${Components.renderSectionHeader('Transfer Preferences')}
            <div class="settings-card">
                ${Components.renderToggle('instant-transfer-toggle', prefs.instantTransferPreference, 'Prefer Instant Transfer', 'instant-transfer')}
                <div class="divider"></div>
                ${Components.renderToggle('auto-accept-toggle', prefs.autoAcceptPayments, 'Auto-accept Payments', 'auto-accept')}
            </div>

            ${Components.renderSectionHeader('Email Notifications')}
            <div class="settings-card">
                ${Components.renderToggle('notif-payments', prefs.emailNotifications.payments, 'Payment Notifications', 'emailNotifications.payments')}
                <div class="divider"></div>
                ${Components.renderToggle('notif-transfers', prefs.emailNotifications.transfers, 'Transfer Notifications', 'emailNotifications.transfers')}
                <div class="divider"></div>
                ${Components.renderToggle('notif-security', prefs.emailNotifications.securityAlerts, 'Security Alerts', 'emailNotifications.securityAlerts')}
                <div class="divider"></div>
                ${Components.renderToggle('notif-promotions', prefs.emailNotifications.promotions, 'Promotional Emails', 'emailNotifications.promotions')}
                <div class="divider"></div>
                ${Components.renderToggle('notif-crypto', prefs.emailNotifications.cryptoAlerts, 'Crypto Alerts', 'emailNotifications.cryptoAlerts')}
                <div class="divider"></div>
                ${Components.renderToggle('notif-rewards', prefs.emailNotifications.rewardsUpdates, 'Rewards Updates', 'emailNotifications.rewardsUpdates')}
                <div class="divider"></div>
                ${Components.renderToggle('notif-weekly', prefs.emailNotifications.weeklyDigest, 'Weekly Digest', 'emailNotifications.weeklyDigest')}
            </div>
        `;
    }
};
