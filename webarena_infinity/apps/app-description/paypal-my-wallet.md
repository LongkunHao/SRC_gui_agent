# PayPal — My Wallet

PayPal is a digital payments platform. This environment covers the **My Wallet** section where users manage their payment methods, balances, and financial instruments.

## Components to Implement

### Wallet Overview
- PayPal balance display (with currency)
- List of linked payment methods (cards, bank accounts) with card type icons, last 4 digits, expiration
- Default/preferred payment method indicator
- Quick actions: add money, withdraw to bank, send money

### Credit/Debit Cards
- List of linked cards: card brand (Visa, Mastercard, Amex, Discover), card name, last 4 digits, expiration date, status (active, expired)
- Add new card form (card number, expiration, CVV, billing address)
- Edit card details (billing address, expiration)
- Remove card (with confirmation)
- Set as preferred payment method

### Bank Accounts
- List of linked bank accounts: bank name, account type (checking, savings), last 4 digits, status (confirmed, pending verification)
- Add bank account (routing number, account number, account type)
- Verify bank account (micro-deposit confirmation)
- Remove bank account
- Set as preferred for withdrawals

### PayPal Balance
- Current balance amount
- Balance history / recent transactions list
- Add money from bank account (amount input, source selection)
- Withdraw to bank account (amount, destination selection)
- Currency management (multiple currency balances if applicable)

### Payment Preferences
- Default payment method selection (for online purchases)
- Backup payment method configuration
- Preferred currency setting
- Pre-approved payments / automatic payments list
  - Merchant name, amount/frequency, status (active, suspended)
  - Cancel or suspend pre-approved payment

### Rewards & Cashback
- Cashback balance or rewards points display
- Rewards history list
- Redeem options (apply to balance, use at checkout)

### Settings
- Wallet notifications (payment received, card expiring, etc.)
- Security preferences (require confirmation for payments over threshold)
- Auto-reload balance settings
