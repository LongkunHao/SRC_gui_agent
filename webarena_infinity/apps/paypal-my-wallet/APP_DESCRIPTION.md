# PayPal My Wallet - App Description

## Summary

A faithful functional replica of PayPal's "My Wallet" section, implementing the core financial management features documented in PayPal's user-facing help articles. The app allows users to manage payment methods (cards and bank accounts), view and manage multi-currency balances, buy/sell cryptocurrency, manage a PayPal Debit Card, interact with Pay in 4 installment plans, manage PayPal Credit, earn and redeem rewards, save merchant offers, purchase digital gift cards, and configure payment preferences.

## Main Sections/Pages

1. **Overview (My Wallet)** - Dashboard with balance summary, crypto portfolio value, rewards points, payment methods preview, active Pay in 4 plans, and recent transactions
2. **Cards** - View, add, update, remove, and confirm credit/debit cards; set preferred/backup payment method
3. **Bank Accounts** - Link, confirm (via micro-deposits), and remove bank accounts
4. **Balance** - Multi-currency balance management, add/withdraw money, currency conversion, exchange rates
5. **Savings** - PayPal Savings account with APY, deposit/withdraw, interest tracking
6. **Cryptocurrency** - Buy/sell Bitcoin, Ethereum, Litecoin, Bitcoin Cash, Solana; portfolio tracking with gains/losses
7. **PayPal Debit Card** - Card settings, PIN management, spending/ATM limits, cash back toggle, direct deposit
8. **PayPal Credit** - Credit line management, make payments, autopay settings
9. **Pay in 4** - View active and completed installment plans with payment schedules
10. **Rewards** - Points balance, earn/redeem history, tier status
11. **Offers** - Browse, save, and manage merchant cashback offers
12. **Gift Cards** - Purchase digital gift cards from 15 merchants with custom messages
13. **Transactions** - Full transaction history with search, filtering, pagination
14. **Preferences** - Payment method preferences, currency conversion settings, notification toggles

## Implemented Features and UI Interactions

### Cards
- Link a new credit or debit card (Visa, Mastercard, Amex, Discover) with full billing address
- Update card expiration date and billing address
- Confirm a pending card via 4-digit confirmation code (simulating the $1.95 PayPal charge)
- Set a card as preferred payment method
- Remove a card (with confirmation dialog)
- Visual card representation showing brand, last 4 digits, expiration, preferred/backup badges
- Status tracking: confirmed, pending_confirmation, expired
- Instant Transfer eligibility indicator for debit cards

### Bank Accounts
- Link a bank account (checking or savings) with routing/account numbers
- Confirm bank via two micro-deposit amounts
- Remove bank account (with confirmation dialog)
- Status tracking: confirmed, pending_confirmation
- Instant Transfer eligibility indicator

### Balance & Currency
- View total balance across all currencies (USD equivalent)
- Add money from a confirmed bank account
- Withdraw money to a confirmed bank account
- Add new currency to wallet (24 currencies supported)
- Remove zero-balance non-primary currencies
- Set primary currency
- Convert between currencies (with 3% fee)
- Exchange rate display for major currencies

### Cryptocurrency
- Buy crypto using PayPal balance (with real-time fee calculation)
- Sell crypto back to PayPal balance
- Portfolio overview with total value, cost basis, and returns
- Per-asset view: quantity, current price, total value, percentage return
- Transaction history per asset
- Fee schedule display (tiered by purchase amount)
- Supported: Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC), Bitcoin Cash (BCH), Solana (SOL), Chainlink (LINK), PayPal USD (PYUSD)

### PayPal Debit Card
- View card details and status
- Change PIN (4-digit, with confirmation)
- Set daily spending limit ($0-$10,000)
- Set daily ATM withdrawal limit ($0-$3,000)
- Toggle monthly cash back (5%)
- Direct deposit toggle with routing/account numbers
- Edit employer name for direct deposit

### Savings
- View savings balance with APY (4.30%)
- Deposit from PayPal Balance
- Withdraw to PayPal Balance
- Interest tracking: this month, year-to-date, all-time
- Transfer history (deposits and withdrawals)

### PayPal Credit
- View available credit, current balance, credit limit
- Usage progress bar
- Make payments (minimum or full balance quick buttons)
- Toggle autopay (minimum, statement balance, or full balance options)
- Account details: APR, statement dates, last payment info

### Pay in 4
- View active installment plans with payment schedules
- Progress bar showing completed payments
- Per-payment detail: amount, due date, paid date, status
- Completed plans history
- Payment method association

### Rewards
- Points balance display with dollar value
- Tier status (Gold member)
- Earned this month / this year stats
- Redeem points for PayPal Balance or Gift Card (100 pts = $1.00)
- Full earn/redeem/bonus history

### Offers
- Browse available merchant offers (cashback percent or fixed amount)
- Save/unsave offers
- Filter by: All, Saved, Available
- Offer details: merchant, category, description, min purchase, max cashback, expiration
- Status tracking: available, saved, used, expired

### Gift Cards
- Purchase digital gift cards from 15 merchants
- Select merchant, denomination, recipient details
- Custom message support
- Gift card history with status (active, partially_used, used)
- Remaining balance tracking
- Auto-generated redemption codes

### Transactions
- Full transaction history (40 seed transactions)
- Search by description or category
- Filter by type: All, Payments, Received, Transfers, Crypto, Pending
- Filter by date: All Time, Last 7 Days, Last 30 Days, Last 90 Days
- Pagination (10 per page)
- Transaction types: payment, received, transfer_in, transfer_out, crypto_buy, crypto_sell, refund, savings_deposit, currency_convert, gift_card, pending

### Preferences
- Set preferred payment method (dropdown of confirmed cards and banks)
- Set backup payment method
- Currency conversion preference (PayPal vs card issuer)
- Instant Transfer preference toggle
- Auto-accept payments toggle
- Email notification toggles (7 categories): payments, transfers, security alerts, promotions, crypto alerts, rewards updates, weekly digest

## Data Model

### Entities and Fields

**CurrentUser**
- id, firstName, lastName, email, phone, dateJoined, accountType, accountStatus, country, primaryCurrency, preferredPaymentMethodId, backupPaymentMethodId, avatarInitials

**Card**
- id, type (credit/debit), brand (Visa/Mastercard/American Express/Discover), lastFour, cardholderName, expirationMonth, expirationYear, billingAddress {street, city, state, zip, country}, status (confirmed/pending_confirmation/expired), isPreferred, isExpired, addedAt, confirmedAt, lastUsed, isBackup, confirmationCode, instantTransferEligible

**BankAccount**
- id, bankName, accountType (checking/savings), lastFour, routingNumber, status (confirmed/pending_confirmation), isPreferred, addedAt, confirmedAt, lastUsed, confirmationDeposit1, confirmationDeposit2, instantTransferEligible

**Balance**
- currency (3-letter code), amount, isPrimary

**CryptoHolding**
- id, symbol, name, quantity, averagePurchasePrice, currentPrice, totalCost, currentValue, totalReturn, totalReturnPercent, lastUpdated, transactions[] {id, type (buy/sell), quantity, pricePerUnit, total, fee, date}

**PayPalDebitCard**
- id, lastFour, status, brand, cardholderName, activatedAt, pinSet, dailySpendingLimit, dailyATMLimit, cashBackEnabled, cashBackPercent, directDeposit {enabled, routingNumber, accountNumber, employer}

**SavingsAccount**
- id, balance, apy, status, openedAt, lastInterestPaid, interestEarnedThisMonth, interestEarnedYTD, interestEarnedAllTime, transferHistory[] {id, type, amount, date, from/to}

**PayLaterPlan**
- id, merchantName, totalAmount, orderDate, status (active/completed), payments[] {number, amount, dueDate, status (paid/upcoming), paidDate}, paymentMethodId

**Rewards**
- totalPoints, pointsValue, tier, earnedThisMonth, earnedThisYear, history[] {id, description, points, date, type (earned/redeemed/bonus), redemptionValue}

**Offer**
- id, merchantName, description, cashbackPercent/cashbackAmount, cashbackType (percent/fixed), minPurchase, maxCashback, expiresAt, status (available/saved/used/expired), savedAt, category, usedAt

**GiftCard**
- id, merchantName, amount, remainingBalance, status (active/partially_used/used), purchasedAt, recipientEmail, recipientName, senderName, message, redemptionCode, redeemed

**Transaction**
- id, type (payment/received/transfer_in/transfer_out/crypto_buy/crypto_sell/refund/savings_deposit/savings_withdrawal/currency_convert/gift_card/pending), description, amount, currency, date, status (completed/pending), paymentMethod, category

**PayPalCredit**
- id, status, creditLimit, currentBalance, availableCredit, minimumPaymentDue, paymentDueDate, apr, lastStatementDate, lastStatementBalance, lastPaymentAmount, lastPaymentDate, autopayEnabled, autopayAmount

**WalletPreferences**
- preferredPaymentMethod, backupPaymentMethod, onlinePaymentPreference, inStorePaymentPreference, autoAcceptPayments, instantTransferPreference, currencyConversionOption (paypal/card_issuer), emailNotifications {payments, transfers, securityAlerts, promotions, cryptoAlerts, rewardsUpdates, weeklyDigest}

**GiftCardMerchant**
- id, name, denominations[], category

### Relationships
- Card.id referenced by WalletPreferences.preferredPaymentMethod, PayLaterPlan.paymentMethodId
- BankAccount.id referenced by WalletPreferences.backupPaymentMethod
- Transaction.paymentMethod references Card.id, BankAccount.id, or 'balance'
- CryptoHolding contains nested transactions[]
- SavingsAccount contains nested transferHistory[]

## Navigation Structure

Sidebar navigation with sections:
- **Overview**: My Wallet, Transactions
- **Payment Methods**: Cards, Bank Accounts, PayPal Debit Card
- **Money**: Balance, Savings, Cryptocurrency
- **Credit & Pay Later**: PayPal Credit, Pay in 4
- **Rewards & More**: Rewards, Offers, Gift Cards
- **Settings**: Preferences

All views accessible via sidebar click. Overview cards link to their respective detail pages.

## Available Form Controls, Dropdowns, Toggles, and Their Options

### Dropdowns
- **Preferred Payment Method**: All confirmed cards and banks (dynamic)
- **Backup Payment Method**: All confirmed cards and banks (dynamic)
- **Date Filter (Transactions)**: All Time, Last 7 Days, Last 30 Days, Last 90 Days
- **Bank Account Selection (Add/Withdraw Money)**: All confirmed bank accounts
- **From Currency (Convert)**: Currencies with balance
- **To Currency (Convert)**: All 24 supported currencies
- **Add Currency**: Currencies not yet in wallet

### Toggle Switches
- Debit Card Cash Back (5% on rotating categories: Fuel, Groceries, Apparel, Restaurants)
- Direct Deposit enabled/disabled
- AutoPay enabled/disabled
- Instant Transfer preference
- Auto-accept Payments
- Email Notification toggles (7): Payments, Transfers, Security Alerts, Promotions, Crypto Alerts, Rewards Updates, Weekly Digest

### Radio Buttons
- Card Type: Credit / Debit
- Card Brand: Visa / Mastercard / American Express / Discover
- Bank Account Type: Checking / Savings
- AutoPay Amount: Minimum Payment Due / Statement Balance / Full Balance
- Currency Conversion: Convert with PayPal / Convert with Card Issuer
- Rewards Redemption Type: PayPal Balance / Gift Card

### Tabs
- Transaction filter: All, Payments, Received, Transfers, Crypto, Pending
- Offers filter: All, Saved, Available

## Seed Data Summary

### User
- Jordan Mitchell, jordan.mitchell@outlook.com, personal verified US account, member since Mar 2019

### Cards (6)
- Visa ****4829 (credit, confirmed, preferred) - added 2019
- Mastercard ****7156 (debit, confirmed, instant transfer eligible) - added 2020
- American Express ****3001 (credit, confirmed) - added 2021
- Discover ****6221 (credit, expired Jun 2025) - added 2020
- Visa ****8834 (debit, pending confirmation, instant transfer) - added Mar 2026
- Mastercard ****2290 (credit, confirmed, backup) - added 2022

### Bank Accounts (5)
- Chase Checking ****6742 (confirmed, instant transfer) - added 2019
- Bank of America Savings ****3891 (confirmed) - added 2020
- Wells Fargo Checking ****5518 (pending confirmation, instant transfer) - added Feb 2026
- Citibank Checking ****1104 (confirmed, instant transfer) - added 2021
- US Bank Savings ****7823 (confirmed) - added 2022

### Balances (6 currencies)
- USD $2,847.63 (primary)
- EUR 523.18
- GBP 189.42
- CAD 0.00
- JPY 45,200
- AUD 312.75

### Crypto Holdings (5)
- Bitcoin: 0.04521 BTC (~$3,067, +60.2%)
- Ethereum: 0.85200 ETH (~$3,018, +55.4%)
- Litecoin: 5.23400 LTC (~$515, +35.8%)
- Bitcoin Cash: 1.10000 BCH (~$344, +27.6%)
- Solana: 0 SOL (available to buy)
- Chainlink: 12.50000 LINK (~$234, +32.0%)
- PayPal USD: 250.00000 PYUSD ($250, stablecoin, no fees)

### PayPal Debit Card
- Mastercard ****9012, active, PIN set, $3,000 daily spending limit, $400 ATM limit, 5% cash back enabled (current category: Restaurants; rotates through Fuel, Groceries, Apparel, Restaurants), max $1,000 spend/month for cash back, direct deposit with TechNova Solutions

### Savings
- $12,450.82 at 4.30% APY, $1,389.20 total interest earned, 8 transfer history entries

### Pay in 4 Plans (4)
- Nordstrom $284.50 (active, 2/4 paid)
- Best Buy $649.99 (active, fully paid / completed)
- Nike $189.00 (active, 1/4 paid)
- Wayfair $412.00 (completed)

### PayPal Credit
- $5,000 limit, $1,245.67 balance, $3,754.33 available, 25.99% APR, autopay enabled (minimum)

### Rewards
- 4,825 points (worth $48.25), Gold tier, 12 history entries (earned/redeemed/bonus)

### Offers (12)
- 3 saved (Starbucks, Uber, Spotify)
- 7 available (DoorDash, Nike, Target, Walmart, Lyft, Amazon, Chipotle)
- 1 used (Grubhub)
- 1 expired (Best Buy)

### Gift Cards (5)
- Amazon $50 (active, to Sarah Chen)
- Starbucks $25 (partially used, $12.50 remaining, self)
- Target $100 (used, to Marcus Williams)
- Netflix $30 (active, to Emily Rodriguez)
- Home Depot $75 (active, self)

### Transactions (40)
- Mix of payments, received, transfers, crypto, refund, savings, currency conversion, gift card, pending
- Spanning Dec 2025 to Mar 2026
- 2 pending transactions
- Multiple currencies (USD, EUR, GBP)
- Various merchants and categories

### Gift Card Merchants (15)
- Amazon, Starbucks, Target, Netflix, Apple, Google Play, Home Depot, Uber, Nike, Spotify, DoorDash, Best Buy, Walmart, Sephora, GameStop
- Each with multiple denomination options
