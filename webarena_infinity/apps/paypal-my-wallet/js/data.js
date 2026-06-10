// ============================================================
// data.js — Rich, realistic seed data for PayPal My Wallet
// ============================================================
const SEED_DATA_VERSION = 1;

// ---- Current User ----
const CURRENT_USER = {
    id: 'usr_pp_29481',
    firstName: 'Jordan',
    lastName: 'Mitchell',
    email: 'jordan.mitchell@outlook.com',
    phone: '+1 (415) 555-0187',
    dateJoined: '2019-03-14T10:22:00Z',
    accountType: 'personal',
    accountStatus: 'verified',
    country: 'US',
    primaryCurrency: 'USD',
    preferredPaymentMethodId: 'card_001',
    backupPaymentMethodId: 'bank_001',
    avatarInitials: 'JM'
};

// ---- Cards (Credit & Debit) ----
const CARDS = [
    {
        id: 'card_001',
        type: 'credit',
        brand: 'Visa',
        lastFour: '4829',
        cardholderName: 'Jordan Mitchell',
        expirationMonth: 9,
        expirationYear: 2028,
        billingAddress: {
            street: '742 Evergreen Terrace',
            city: 'San Francisco',
            state: 'CA',
            zip: '94102',
            country: 'US'
        },
        status: 'confirmed',
        isPreferred: true,
        isExpired: false,
        addedAt: '2019-03-14T10:30:00Z',
        confirmedAt: '2019-03-14T11:45:00Z',
        lastUsed: '2026-03-05T14:22:00Z',
        isBackup: false
    },
    {
        id: 'card_002',
        type: 'debit',
        brand: 'Mastercard',
        lastFour: '7156',
        cardholderName: 'Jordan Mitchell',
        expirationMonth: 3,
        expirationYear: 2027,
        billingAddress: {
            street: '742 Evergreen Terrace',
            city: 'San Francisco',
            state: 'CA',
            zip: '94102',
            country: 'US'
        },
        status: 'confirmed',
        isPreferred: false,
        isExpired: false,
        addedAt: '2020-06-22T09:15:00Z',
        confirmedAt: '2020-06-22T10:30:00Z',
        lastUsed: '2026-02-28T11:03:00Z',
        isBackup: false,
        instantTransferEligible: true
    },
    {
        id: 'card_003',
        type: 'credit',
        brand: 'American Express',
        lastFour: '3001',
        cardholderName: 'Jordan Mitchell',
        expirationMonth: 12,
        expirationYear: 2026,
        billingAddress: {
            street: '742 Evergreen Terrace',
            city: 'San Francisco',
            state: 'CA',
            zip: '94102',
            country: 'US'
        },
        status: 'confirmed',
        isPreferred: false,
        isExpired: false,
        addedAt: '2021-01-10T16:45:00Z',
        confirmedAt: '2021-01-11T09:20:00Z',
        lastUsed: '2026-01-15T08:44:00Z',
        isBackup: false
    },
    {
        id: 'card_004',
        type: 'credit',
        brand: 'Discover',
        lastFour: '6221',
        cardholderName: 'Jordan Mitchell',
        expirationMonth: 6,
        expirationYear: 2025,
        billingAddress: {
            street: '742 Evergreen Terrace',
            city: 'San Francisco',
            state: 'CA',
            zip: '94102',
            country: 'US'
        },
        status: 'expired',
        isPreferred: false,
        isExpired: true,
        addedAt: '2020-11-03T14:20:00Z',
        confirmedAt: '2020-11-03T15:50:00Z',
        lastUsed: '2025-05-20T10:11:00Z',
        isBackup: false
    },
    {
        id: 'card_005',
        type: 'debit',
        brand: 'Visa',
        lastFour: '8834',
        cardholderName: 'Jordan Mitchell',
        expirationMonth: 11,
        expirationYear: 2029,
        billingAddress: {
            street: '1200 Pacific Ave',
            city: 'San Francisco',
            state: 'CA',
            zip: '94109',
            country: 'US'
        },
        status: 'pending_confirmation',
        isPreferred: false,
        isExpired: false,
        addedAt: '2026-03-01T10:00:00Z',
        confirmedAt: null,
        lastUsed: null,
        isBackup: false,
        confirmationCode: null,
        instantTransferEligible: true
    },
    {
        id: 'card_006',
        type: 'credit',
        brand: 'Mastercard',
        lastFour: '2290',
        cardholderName: 'Jordan Mitchell',
        expirationMonth: 8,
        expirationYear: 2028,
        billingAddress: {
            street: '742 Evergreen Terrace',
            city: 'San Francisco',
            state: 'CA',
            zip: '94102',
            country: 'US'
        },
        status: 'confirmed',
        isPreferred: false,
        isExpired: false,
        addedAt: '2022-09-15T11:30:00Z',
        confirmedAt: '2022-09-15T13:00:00Z',
        lastUsed: '2026-02-10T16:30:00Z',
        isBackup: true
    }
];

// ---- Bank Accounts ----
const BANK_ACCOUNTS = [
    {
        id: 'bank_001',
        bankName: 'Chase',
        accountType: 'checking',
        lastFour: '6742',
        routingNumber: '021000021',
        status: 'confirmed',
        isPreferred: false,
        addedAt: '2019-03-14T10:35:00Z',
        confirmedAt: '2019-03-16T08:00:00Z',
        lastUsed: '2026-03-01T09:00:00Z',
        instantTransferEligible: true
    },
    {
        id: 'bank_002',
        bankName: 'Bank of America',
        accountType: 'savings',
        lastFour: '3891',
        routingNumber: '026009593',
        status: 'confirmed',
        isPreferred: false,
        addedAt: '2020-01-20T14:10:00Z',
        confirmedAt: '2020-01-22T11:00:00Z',
        lastUsed: '2026-01-05T15:30:00Z',
        instantTransferEligible: false
    },
    {
        id: 'bank_003',
        bankName: 'Wells Fargo',
        accountType: 'checking',
        lastFour: '5518',
        routingNumber: '121000248',
        status: 'pending_confirmation',
        isPreferred: false,
        addedAt: '2026-02-25T10:00:00Z',
        confirmedAt: null,
        lastUsed: null,
        confirmationDeposit1: null,
        confirmationDeposit2: null,
        instantTransferEligible: true
    },
    {
        id: 'bank_004',
        bankName: 'Citibank',
        accountType: 'checking',
        lastFour: '1104',
        routingNumber: '021000089',
        status: 'confirmed',
        isPreferred: false,
        addedAt: '2021-07-08T09:45:00Z',
        confirmedAt: '2021-07-10T10:15:00Z',
        lastUsed: '2025-11-20T12:00:00Z',
        instantTransferEligible: true
    },
    {
        id: 'bank_005',
        bankName: 'US Bank',
        accountType: 'savings',
        lastFour: '7823',
        routingNumber: '091000019',
        status: 'confirmed',
        isPreferred: false,
        addedAt: '2022-04-12T16:30:00Z',
        confirmedAt: '2022-04-14T09:00:00Z',
        lastUsed: '2025-08-15T14:20:00Z',
        instantTransferEligible: false
    }
];

// ---- PayPal Balance ----
const BALANCES = [
    { currency: 'USD', amount: 2847.63, isPrimary: true },
    { currency: 'EUR', amount: 523.18, isPrimary: false },
    { currency: 'GBP', amount: 189.42, isPrimary: false },
    { currency: 'CAD', amount: 0.00, isPrimary: false },
    { currency: 'JPY', amount: 45200, isPrimary: false },
    { currency: 'AUD', amount: 312.75, isPrimary: false }
];

// ---- Supported Currencies ----
const CURRENCIES = [
    { code: 'USD', name: 'U.S. Dollar', symbol: '$' },
    { code: 'EUR', name: 'Euro', symbol: '\u20AC' },
    { code: 'GBP', name: 'British Pound', symbol: '\u00A3' },
    { code: 'CAD', name: 'Canadian Dollar', symbol: 'CA$' },
    { code: 'AUD', name: 'Australian Dollar', symbol: 'A$' },
    { code: 'JPY', name: 'Japanese Yen', symbol: '\u00A5' },
    { code: 'CHF', name: 'Swiss Franc', symbol: 'CHF' },
    { code: 'SEK', name: 'Swedish Krona', symbol: 'kr' },
    { code: 'NOK', name: 'Norwegian Krone', symbol: 'kr' },
    { code: 'DKK', name: 'Danish Krone', symbol: 'kr' },
    { code: 'PLN', name: 'Polish Zloty', symbol: 'z\u0142' },
    { code: 'BRL', name: 'Brazilian Real', symbol: 'R$' },
    { code: 'MXN', name: 'Mexican Peso', symbol: 'MX$' },
    { code: 'SGD', name: 'Singapore Dollar', symbol: 'S$' },
    { code: 'HKD', name: 'Hong Kong Dollar', symbol: 'HK$' },
    { code: 'NZD', name: 'New Zealand Dollar', symbol: 'NZ$' },
    { code: 'CZK', name: 'Czech Koruna', symbol: 'K\u010D' },
    { code: 'ILS', name: 'Israeli Shekel', symbol: '\u20AA' },
    { code: 'HUF', name: 'Hungarian Forint', symbol: 'Ft' },
    { code: 'PHP', name: 'Philippine Peso', symbol: '\u20B1' },
    { code: 'TWD', name: 'Taiwan Dollar', symbol: 'NT$' },
    { code: 'THB', name: 'Thai Baht', symbol: '\u0E3F' },
    { code: 'INR', name: 'Indian Rupee', symbol: '\u20B9' },
    { code: 'RUB', name: 'Russian Ruble', symbol: '\u20BD' }
];

// ---- Exchange Rates (relative to USD) ----
const EXCHANGE_RATES = {
    USD: 1.0,
    EUR: 0.92,
    GBP: 0.79,
    CAD: 1.36,
    AUD: 1.54,
    JPY: 149.50,
    CHF: 0.88,
    SEK: 10.42,
    NOK: 10.68,
    DKK: 6.87,
    PLN: 3.98,
    BRL: 4.97,
    MXN: 17.15,
    SGD: 1.34,
    HKD: 7.82,
    NZD: 1.64,
    CZK: 22.85,
    ILS: 3.67,
    HUF: 356.20,
    PHP: 55.80,
    TWD: 31.45,
    THB: 35.20,
    INR: 83.10,
    RUB: 92.50
};

// ---- Cryptocurrency Holdings ----
const CRYPTO_HOLDINGS = [
    {
        id: 'crypto_001',
        symbol: 'BTC',
        name: 'Bitcoin',
        quantity: 0.04521,
        averagePurchasePrice: 42350.00,
        currentPrice: 67842.15,
        totalCost: 1914.27,
        currentValue: 3066.89,
        totalReturn: 1152.62,
        totalReturnPercent: 60.22,
        lastUpdated: '2026-03-07T08:00:00Z',
        transactions: [
            { id: 'ctx_001', type: 'buy', quantity: 0.02000, pricePerUnit: 38500.00, total: 770.00, fee: 7.70, date: '2023-11-15T10:30:00Z' },
            { id: 'ctx_002', type: 'buy', quantity: 0.01500, pricePerUnit: 44200.00, total: 663.00, fee: 6.63, date: '2024-03-20T14:15:00Z' },
            { id: 'ctx_003', type: 'buy', quantity: 0.01021, pricePerUnit: 47125.00, total: 481.27, fee: 4.81, date: '2024-09-05T09:00:00Z' }
        ]
    },
    {
        id: 'crypto_002',
        symbol: 'ETH',
        name: 'Ethereum',
        quantity: 0.85200,
        averagePurchasePrice: 2280.00,
        currentPrice: 3542.80,
        totalCost: 1942.56,
        currentValue: 3018.47,
        totalReturn: 1075.91,
        totalReturnPercent: 55.39,
        lastUpdated: '2026-03-07T08:00:00Z',
        transactions: [
            { id: 'ctx_004', type: 'buy', quantity: 0.50000, pricePerUnit: 2100.00, total: 1050.00, fee: 10.50, date: '2023-12-01T11:00:00Z' },
            { id: 'ctx_005', type: 'buy', quantity: 0.25000, pricePerUnit: 2450.00, total: 612.50, fee: 6.13, date: '2024-05-10T16:30:00Z' },
            { id: 'ctx_006', type: 'sell', quantity: 0.10000, pricePerUnit: 3200.00, total: 320.00, fee: 3.20, date: '2025-01-15T13:45:00Z' },
            { id: 'ctx_007', type: 'buy', quantity: 0.20200, pricePerUnit: 2800.00, total: 565.60, fee: 5.66, date: '2025-06-20T10:20:00Z' }
        ]
    },
    {
        id: 'crypto_003',
        symbol: 'LTC',
        name: 'Litecoin',
        quantity: 5.23400,
        averagePurchasePrice: 72.50,
        currentPrice: 98.45,
        totalCost: 379.47,
        currentValue: 515.28,
        totalReturn: 135.81,
        totalReturnPercent: 35.79,
        lastUpdated: '2026-03-07T08:00:00Z',
        transactions: [
            { id: 'ctx_008', type: 'buy', quantity: 3.00000, pricePerUnit: 68.00, total: 204.00, fee: 2.04, date: '2024-02-14T12:00:00Z' },
            { id: 'ctx_009', type: 'buy', quantity: 2.23400, pricePerUnit: 78.50, total: 175.37, fee: 1.75, date: '2024-08-30T09:30:00Z' }
        ]
    },
    {
        id: 'crypto_004',
        symbol: 'BCH',
        name: 'Bitcoin Cash',
        quantity: 1.10000,
        averagePurchasePrice: 245.00,
        currentPrice: 312.70,
        totalCost: 269.50,
        currentValue: 343.97,
        totalReturn: 74.47,
        totalReturnPercent: 27.64,
        lastUpdated: '2026-03-07T08:00:00Z',
        transactions: [
            { id: 'ctx_010', type: 'buy', quantity: 1.10000, pricePerUnit: 245.00, total: 269.50, fee: 2.70, date: '2024-06-12T15:00:00Z' }
        ]
    },
    {
        id: 'crypto_005',
        symbol: 'SOL',
        name: 'Solana',
        quantity: 0,
        averagePurchasePrice: 0,
        currentPrice: 142.30,
        totalCost: 0,
        currentValue: 0,
        totalReturn: 0,
        totalReturnPercent: 0,
        lastUpdated: '2026-03-07T08:00:00Z',
        transactions: []
    },
    {
        id: 'crypto_006',
        symbol: 'LINK',
        name: 'Chainlink',
        quantity: 12.50000,
        averagePurchasePrice: 14.20,
        currentPrice: 18.75,
        totalCost: 177.50,
        currentValue: 234.38,
        totalReturn: 56.88,
        totalReturnPercent: 32.04,
        lastUpdated: '2026-03-07T08:00:00Z',
        transactions: [
            { id: 'ctx_011', type: 'buy', quantity: 12.50000, pricePerUnit: 14.20, total: 177.50, fee: 1.78, date: '2025-04-10T11:00:00Z' }
        ]
    },
    {
        id: 'crypto_007',
        symbol: 'PYUSD',
        name: 'PayPal USD',
        quantity: 250.00000,
        averagePurchasePrice: 1.00,
        currentPrice: 1.00,
        totalCost: 250.00,
        currentValue: 250.00,
        totalReturn: 0,
        totalReturnPercent: 0,
        lastUpdated: '2026-03-07T08:00:00Z',
        transactions: [
            { id: 'ctx_012', type: 'buy', quantity: 250.00000, pricePerUnit: 1.00, total: 250.00, fee: 0, date: '2025-09-20T14:30:00Z' }
        ]
    }
];

// ---- PayPal Debit Card ----
const PAYPAL_DEBIT_CARD = {
    id: 'ppdc_001',
    lastFour: '9012',
    status: 'active',
    brand: 'Mastercard',
    cardholderName: 'Jordan Mitchell',
    activatedAt: '2020-08-15T10:00:00Z',
    pinSet: true,
    dailySpendingLimit: 3000,
    dailyATMLimit: 400,
    cashBackEnabled: true,
    cashBackPercent: 5,
    cashBackCategory: 'Restaurants',
    cashBackCategories: ['Fuel', 'Groceries', 'Apparel', 'Restaurants'],
    maxCashBackMonthlySpend: 1000,
    directDeposit: {
        enabled: true,
        routingNumber: '031101279',
        accountNumber: '4024007129012',
        employer: 'TechNova Solutions'
    }
};

// ---- PayPal Savings ----
const SAVINGS_ACCOUNT = {
    id: 'sav_001',
    balance: 12450.82,
    apy: 4.30,
    status: 'active',
    openedAt: '2023-06-01T10:00:00Z',
    lastInterestPaid: '2026-03-01T00:00:00Z',
    interestEarnedThisMonth: 43.62,
    interestEarnedYTD: 127.85,
    interestEarnedAllTime: 1389.20,
    transferHistory: [
        { id: 'stx_001', type: 'deposit', amount: 5000.00, date: '2023-06-01T10:00:00Z', from: 'PayPal Balance' },
        { id: 'stx_002', type: 'deposit', amount: 2000.00, date: '2023-09-15T14:30:00Z', from: 'PayPal Balance' },
        { id: 'stx_003', type: 'withdrawal', amount: 500.00, date: '2024-01-10T11:00:00Z', to: 'PayPal Balance' },
        { id: 'stx_004', type: 'deposit', amount: 3000.00, date: '2024-04-22T09:15:00Z', from: 'PayPal Balance' },
        { id: 'stx_005', type: 'deposit', amount: 1500.00, date: '2024-08-05T16:45:00Z', from: 'PayPal Balance' },
        { id: 'stx_006', type: 'withdrawal', amount: 1000.00, date: '2025-02-18T13:20:00Z', to: 'PayPal Balance' },
        { id: 'stx_007', type: 'deposit', amount: 2000.00, date: '2025-07-30T10:00:00Z', from: 'PayPal Balance' },
        { id: 'stx_008', type: 'deposit', amount: 450.82, date: '2026-01-15T08:30:00Z', from: 'PayPal Balance' }
    ]
};

// ---- Pay Later (Pay in 4) Plans ----
const PAY_LATER_PLANS = [
    {
        id: 'pi4_001',
        merchantName: 'Nordstrom',
        totalAmount: 284.50,
        orderDate: '2026-02-10T14:30:00Z',
        status: 'active',
        payments: [
            { number: 1, amount: 71.13, dueDate: '2026-02-10T00:00:00Z', status: 'paid', paidDate: '2026-02-10T14:30:00Z' },
            { number: 2, amount: 71.13, dueDate: '2026-02-24T00:00:00Z', status: 'paid', paidDate: '2026-02-24T10:00:00Z' },
            { number: 3, amount: 71.12, dueDate: '2026-03-10T00:00:00Z', status: 'upcoming', paidDate: null },
            { number: 4, amount: 71.12, dueDate: '2026-03-24T00:00:00Z', status: 'upcoming', paidDate: null }
        ],
        paymentMethodId: 'card_001'
    },
    {
        id: 'pi4_002',
        merchantName: 'Best Buy',
        totalAmount: 649.99,
        orderDate: '2026-01-15T11:00:00Z',
        status: 'active',
        payments: [
            { number: 1, amount: 162.50, dueDate: '2026-01-15T00:00:00Z', status: 'paid', paidDate: '2026-01-15T11:00:00Z' },
            { number: 2, amount: 162.50, dueDate: '2026-01-29T00:00:00Z', status: 'paid', paidDate: '2026-01-29T09:15:00Z' },
            { number: 3, amount: 162.50, dueDate: '2026-02-12T00:00:00Z', status: 'paid', paidDate: '2026-02-12T10:30:00Z' },
            { number: 4, amount: 162.49, dueDate: '2026-02-26T00:00:00Z', status: 'paid', paidDate: '2026-02-26T08:00:00Z' }
        ],
        paymentMethodId: 'card_002'
    },
    {
        id: 'pi4_003',
        merchantName: 'Nike',
        totalAmount: 189.00,
        orderDate: '2026-03-01T09:45:00Z',
        status: 'active',
        payments: [
            { number: 1, amount: 47.25, dueDate: '2026-03-01T00:00:00Z', status: 'paid', paidDate: '2026-03-01T09:45:00Z' },
            { number: 2, amount: 47.25, dueDate: '2026-03-15T00:00:00Z', status: 'upcoming', paidDate: null },
            { number: 3, amount: 47.25, dueDate: '2026-03-29T00:00:00Z', status: 'upcoming', paidDate: null },
            { number: 4, amount: 47.25, dueDate: '2026-04-12T00:00:00Z', status: 'upcoming', paidDate: null }
        ],
        paymentMethodId: 'card_001'
    },
    {
        id: 'pi4_004',
        merchantName: 'Wayfair',
        totalAmount: 412.00,
        orderDate: '2025-11-20T16:00:00Z',
        status: 'completed',
        payments: [
            { number: 1, amount: 103.00, dueDate: '2025-11-20T00:00:00Z', status: 'paid', paidDate: '2025-11-20T16:00:00Z' },
            { number: 2, amount: 103.00, dueDate: '2025-12-04T00:00:00Z', status: 'paid', paidDate: '2025-12-04T10:00:00Z' },
            { number: 3, amount: 103.00, dueDate: '2025-12-18T00:00:00Z', status: 'paid', paidDate: '2025-12-18T09:30:00Z' },
            { number: 4, amount: 103.00, dueDate: '2026-01-01T00:00:00Z', status: 'paid', paidDate: '2025-12-30T14:15:00Z' }
        ],
        paymentMethodId: 'card_003'
    }
];

// ---- Rewards & Offers ----
const REWARDS = {
    totalPoints: 4825,
    pointsValue: 48.25,
    tier: 'Gold',
    earnedThisMonth: 312,
    earnedThisYear: 2150,
    history: [
        { id: 'rwd_001', description: 'Purchase at Amazon', points: 125, date: '2026-03-05T14:22:00Z', type: 'earned' },
        { id: 'rwd_002', description: 'Purchase at Target', points: 87, date: '2026-03-02T11:30:00Z', type: 'earned' },
        { id: 'rwd_003', description: 'Redeemed for PayPal Balance', points: -500, date: '2026-02-28T09:00:00Z', type: 'redeemed', redemptionValue: 5.00 },
        { id: 'rwd_004', description: 'Purchase at Uber Eats', points: 45, date: '2026-02-25T19:15:00Z', type: 'earned' },
        { id: 'rwd_005', description: 'Bonus: Monthly Spend Goal', points: 200, date: '2026-02-01T00:00:00Z', type: 'bonus' },
        { id: 'rwd_006', description: 'Purchase at Walmart', points: 63, date: '2026-01-28T10:45:00Z', type: 'earned' },
        { id: 'rwd_007', description: 'Purchase at Spotify', points: 15, date: '2026-01-15T00:00:00Z', type: 'earned' },
        { id: 'rwd_008', description: 'Redeemed for Gift Card', points: -1000, date: '2026-01-10T14:00:00Z', type: 'redeemed', redemptionValue: 10.00 },
        { id: 'rwd_009', description: 'Purchase at Etsy', points: 92, date: '2026-01-05T16:30:00Z', type: 'earned' },
        { id: 'rwd_010', description: 'Holiday Bonus', points: 500, date: '2025-12-25T00:00:00Z', type: 'bonus' },
        { id: 'rwd_011', description: 'Purchase at Apple', points: 340, date: '2025-12-20T13:00:00Z', type: 'earned' },
        { id: 'rwd_012', description: 'Purchase at Home Depot', points: 156, date: '2025-12-15T09:20:00Z', type: 'earned' }
    ]
};

const OFFERS = [
    {
        id: 'offer_001',
        merchantName: 'Starbucks',
        merchantLogo: null,
        description: 'Get 10% cashback on your next purchase',
        cashbackPercent: 10,
        cashbackType: 'percent',
        minPurchase: 5.00,
        maxCashback: 10.00,
        expiresAt: '2026-04-15T23:59:59Z',
        status: 'saved',
        savedAt: '2026-03-01T10:00:00Z',
        category: 'Food & Drink',
        usedAt: null
    },
    {
        id: 'offer_002',
        merchantName: 'Uber',
        merchantLogo: null,
        description: '$5 off your next ride of $20 or more',
        cashbackAmount: 5.00,
        cashbackType: 'fixed',
        minPurchase: 20.00,
        maxCashback: 5.00,
        expiresAt: '2026-03-31T23:59:59Z',
        status: 'saved',
        savedAt: '2026-02-20T08:30:00Z',
        category: 'Travel',
        usedAt: null
    },
    {
        id: 'offer_003',
        merchantName: 'DoorDash',
        merchantLogo: null,
        description: '15% cashback on orders over $25',
        cashbackPercent: 15,
        cashbackType: 'percent',
        minPurchase: 25.00,
        maxCashback: 15.00,
        expiresAt: '2026-04-01T23:59:59Z',
        status: 'available',
        savedAt: null,
        category: 'Food & Drink',
        usedAt: null
    },
    {
        id: 'offer_004',
        merchantName: 'Nike',
        merchantLogo: null,
        description: '8% cashback on all purchases',
        cashbackPercent: 8,
        cashbackType: 'percent',
        minPurchase: 0,
        maxCashback: 50.00,
        expiresAt: '2026-05-01T23:59:59Z',
        status: 'available',
        savedAt: null,
        category: 'Shopping',
        usedAt: null
    },
    {
        id: 'offer_005',
        merchantName: 'Grubhub',
        merchantLogo: null,
        description: '$3 off orders of $15+',
        cashbackAmount: 3.00,
        cashbackType: 'fixed',
        minPurchase: 15.00,
        maxCashback: 3.00,
        expiresAt: '2026-03-20T23:59:59Z',
        status: 'used',
        savedAt: '2026-02-10T12:00:00Z',
        category: 'Food & Drink',
        usedAt: '2026-03-02T18:30:00Z'
    },
    {
        id: 'offer_006',
        merchantName: 'Target',
        merchantLogo: null,
        description: '5% cashback on purchases over $50',
        cashbackPercent: 5,
        cashbackType: 'percent',
        minPurchase: 50.00,
        maxCashback: 25.00,
        expiresAt: '2026-04-30T23:59:59Z',
        status: 'available',
        savedAt: null,
        category: 'Shopping',
        usedAt: null
    },
    {
        id: 'offer_007',
        merchantName: 'Spotify',
        merchantLogo: null,
        description: '$2 cashback on monthly subscription',
        cashbackAmount: 2.00,
        cashbackType: 'fixed',
        minPurchase: 0,
        maxCashback: 2.00,
        expiresAt: '2026-06-30T23:59:59Z',
        status: 'saved',
        savedAt: '2026-01-15T09:00:00Z',
        category: 'Entertainment',
        usedAt: null
    },
    {
        id: 'offer_008',
        merchantName: 'Walmart',
        merchantLogo: null,
        description: '3% cashback on groceries',
        cashbackPercent: 3,
        cashbackType: 'percent',
        minPurchase: 30.00,
        maxCashback: 20.00,
        expiresAt: '2026-03-25T23:59:59Z',
        status: 'available',
        savedAt: null,
        category: 'Shopping',
        usedAt: null
    },
    {
        id: 'offer_009',
        merchantName: 'Lyft',
        merchantLogo: null,
        description: '12% cashback on 3 rides',
        cashbackPercent: 12,
        cashbackType: 'percent',
        minPurchase: 10.00,
        maxCashback: 15.00,
        expiresAt: '2026-04-10T23:59:59Z',
        status: 'available',
        savedAt: null,
        category: 'Travel',
        usedAt: null
    },
    {
        id: 'offer_010',
        merchantName: 'Best Buy',
        merchantLogo: null,
        description: '6% cashback on electronics',
        cashbackPercent: 6,
        cashbackType: 'percent',
        minPurchase: 100.00,
        maxCashback: 60.00,
        expiresAt: '2026-05-15T23:59:59Z',
        status: 'expired',
        savedAt: '2025-12-01T10:00:00Z',
        category: 'Shopping',
        usedAt: null
    },
    {
        id: 'offer_011',
        merchantName: 'Amazon',
        merchantLogo: null,
        description: '4% cashback on Prime purchases',
        cashbackPercent: 4,
        cashbackType: 'percent',
        minPurchase: 25.00,
        maxCashback: 40.00,
        expiresAt: '2026-04-20T23:59:59Z',
        status: 'available',
        savedAt: null,
        category: 'Shopping',
        usedAt: null
    },
    {
        id: 'offer_012',
        merchantName: 'Chipotle',
        merchantLogo: null,
        description: '$2 off any order over $10',
        cashbackAmount: 2.00,
        cashbackType: 'fixed',
        minPurchase: 10.00,
        maxCashback: 2.00,
        expiresAt: '2026-04-05T23:59:59Z',
        status: 'available',
        savedAt: null,
        category: 'Food & Drink',
        usedAt: null
    }
];

// ---- Gift Cards ----
const GIFT_CARDS = [
    {
        id: 'gc_001',
        merchantName: 'Amazon',
        amount: 50.00,
        remainingBalance: 50.00,
        status: 'active',
        purchasedAt: '2026-02-14T10:00:00Z',
        recipientEmail: 'sarah.chen@email.com',
        recipientName: 'Sarah Chen',
        senderName: 'Jordan Mitchell',
        message: 'Happy Valentine\'s Day!',
        redemptionCode: 'AMZ-K9R2-HTLP-QW81',
        redeemed: false
    },
    {
        id: 'gc_002',
        merchantName: 'Starbucks',
        amount: 25.00,
        remainingBalance: 12.50,
        status: 'partially_used',
        purchasedAt: '2025-12-20T15:30:00Z',
        recipientEmail: 'jordan.mitchell@outlook.com',
        recipientName: 'Jordan Mitchell',
        senderName: 'Jordan Mitchell',
        message: '',
        redemptionCode: 'SBX-M4TN-VPCR-2F67',
        redeemed: true
    },
    {
        id: 'gc_003',
        merchantName: 'Target',
        amount: 100.00,
        remainingBalance: 0,
        status: 'used',
        purchasedAt: '2025-11-28T09:00:00Z',
        recipientEmail: 'marcus.williams@email.com',
        recipientName: 'Marcus Williams',
        senderName: 'Jordan Mitchell',
        message: 'Thanks for everything!',
        redemptionCode: 'TGT-LP8W-BNDS-KR43',
        redeemed: true
    },
    {
        id: 'gc_004',
        merchantName: 'Netflix',
        amount: 30.00,
        remainingBalance: 30.00,
        status: 'active',
        purchasedAt: '2026-03-05T12:00:00Z',
        recipientEmail: 'emily.r@email.com',
        recipientName: 'Emily Rodriguez',
        senderName: 'Jordan Mitchell',
        message: 'Enjoy!',
        redemptionCode: 'NFX-R2DQ-HWNP-8V45',
        redeemed: false
    },
    {
        id: 'gc_005',
        merchantName: 'Home Depot',
        amount: 75.00,
        remainingBalance: 75.00,
        status: 'active',
        purchasedAt: '2026-01-20T08:15:00Z',
        recipientEmail: 'jordan.mitchell@outlook.com',
        recipientName: 'Jordan Mitchell',
        senderName: 'Jordan Mitchell',
        message: '',
        redemptionCode: 'HDT-QW7X-FCNS-3B91',
        redeemed: false
    }
];

// ---- Recent Transactions ----
const TRANSACTIONS = [
    { id: 'txn_001', type: 'payment', description: 'Amazon.com', amount: -89.47, currency: 'USD', date: '2026-03-06T16:22:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_002', type: 'received', description: 'From Marcus Williams', amount: 150.00, currency: 'USD', date: '2026-03-06T10:15:00Z', status: 'completed', paymentMethod: 'balance', category: 'Personal' },
    { id: 'txn_003', type: 'payment', description: 'Spotify Premium', amount: -11.99, currency: 'USD', date: '2026-03-05T00:00:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Entertainment' },
    { id: 'txn_004', type: 'payment', description: 'Uber Trip', amount: -24.50, currency: 'USD', date: '2026-03-04T19:30:00Z', status: 'completed', paymentMethod: 'card_002', category: 'Travel' },
    { id: 'txn_005', type: 'transfer_out', description: 'To Chase ***6742', amount: -500.00, currency: 'USD', date: '2026-03-03T14:00:00Z', status: 'completed', paymentMethod: 'bank_001', category: 'Transfer' },
    { id: 'txn_006', type: 'payment', description: 'Target', amount: -67.23, currency: 'USD', date: '2026-03-02T11:30:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_007', type: 'received', description: 'From Emily Rodriguez', amount: 42.00, currency: 'USD', date: '2026-03-01T20:45:00Z', status: 'completed', paymentMethod: 'balance', category: 'Personal' },
    { id: 'txn_008', type: 'payment', description: 'Nike.com', amount: -189.00, currency: 'USD', date: '2026-03-01T09:45:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_009', type: 'crypto_buy', description: 'Bought Bitcoin', amount: -200.00, currency: 'USD', date: '2026-02-28T15:00:00Z', status: 'completed', paymentMethod: 'balance', category: 'Crypto' },
    { id: 'txn_010', type: 'transfer_in', description: 'From Chase ***6742', amount: 1000.00, currency: 'USD', date: '2026-02-27T09:00:00Z', status: 'completed', paymentMethod: 'bank_001', category: 'Transfer' },
    { id: 'txn_011', type: 'payment', description: 'Nordstrom', amount: -284.50, currency: 'USD', date: '2026-02-25T14:30:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_012', type: 'payment', description: 'DoorDash', amount: -32.15, currency: 'USD', date: '2026-02-24T19:00:00Z', status: 'completed', paymentMethod: 'card_002', category: 'Food & Drink' },
    { id: 'txn_013', type: 'received', description: 'From David Kim', amount: 75.00, currency: 'USD', date: '2026-02-23T12:30:00Z', status: 'completed', paymentMethod: 'balance', category: 'Personal' },
    { id: 'txn_014', type: 'refund', description: 'Refund from Wayfair', amount: 45.99, currency: 'USD', date: '2026-02-22T10:00:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Refund' },
    { id: 'txn_015', type: 'payment', description: 'Uber Eats', amount: -18.75, currency: 'USD', date: '2026-02-21T20:15:00Z', status: 'completed', paymentMethod: 'card_002', category: 'Food & Drink' },
    { id: 'txn_016', type: 'payment', description: 'Apple.com', amount: -1299.00, currency: 'USD', date: '2026-02-20T13:00:00Z', status: 'completed', paymentMethod: 'card_003', category: 'Shopping' },
    { id: 'txn_017', type: 'savings_deposit', description: 'Transfer to Savings', amount: -450.82, currency: 'USD', date: '2026-02-18T08:30:00Z', status: 'completed', paymentMethod: 'balance', category: 'Savings' },
    { id: 'txn_018', type: 'currency_convert', description: 'Converted USD to EUR', amount: -500.00, currency: 'USD', date: '2026-02-15T11:00:00Z', status: 'completed', paymentMethod: 'balance', category: 'Currency' },
    { id: 'txn_019', type: 'payment', description: 'Best Buy', amount: -649.99, currency: 'USD', date: '2026-02-10T11:00:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_020', type: 'received', description: 'From Priya Sharma', amount: 200.00, currency: 'USD', date: '2026-02-08T16:00:00Z', status: 'completed', paymentMethod: 'balance', category: 'Personal' },
    { id: 'txn_021', type: 'payment', description: 'Netflix', amount: -15.49, currency: 'USD', date: '2026-02-05T00:00:00Z', status: 'completed', paymentMethod: 'card_002', category: 'Entertainment' },
    { id: 'txn_022', type: 'payment', description: 'Costco', amount: -312.87, currency: 'USD', date: '2026-02-03T10:20:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_023', type: 'transfer_out', description: 'To Bank of America ***3891', amount: -250.00, currency: 'USD', date: '2026-02-01T14:30:00Z', status: 'completed', paymentMethod: 'bank_002', category: 'Transfer' },
    { id: 'txn_024', type: 'crypto_sell', description: 'Sold Ethereum', amount: 320.00, currency: 'USD', date: '2026-01-28T13:45:00Z', status: 'completed', paymentMethod: 'balance', category: 'Crypto' },
    { id: 'txn_025', type: 'payment', description: 'Walmart', amount: -156.32, currency: 'USD', date: '2026-01-25T11:15:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_026', type: 'payment', description: 'Steam', amount: -59.99, currency: 'USD', date: '2026-01-22T21:00:00Z', status: 'completed', paymentMethod: 'card_002', category: 'Entertainment' },
    { id: 'txn_027', type: 'received', description: 'Tax Refund - IRS', amount: 2847.00, currency: 'USD', date: '2026-01-20T06:00:00Z', status: 'completed', paymentMethod: 'balance', category: 'Government' },
    { id: 'txn_028', type: 'payment', description: 'Grubhub', amount: -28.90, currency: 'USD', date: '2026-01-18T19:30:00Z', status: 'completed', paymentMethod: 'card_002', category: 'Food & Drink' },
    { id: 'txn_029', type: 'gift_card', description: 'Gift Card - Amazon', amount: -50.00, currency: 'USD', date: '2026-01-15T10:00:00Z', status: 'completed', paymentMethod: 'balance', category: 'Gift Cards' },
    { id: 'txn_030', type: 'payment', description: 'Lyft', amount: -16.50, currency: 'USD', date: '2026-01-12T18:45:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Travel' },
    { id: 'txn_031', type: 'payment', description: 'Hulu', amount: -7.99, currency: 'USD', date: '2026-01-10T00:00:00Z', status: 'completed', paymentMethod: 'card_002', category: 'Entertainment' },
    { id: 'txn_032', type: 'payment', description: 'Etsy - Handmade Goods', amount: -92.00, currency: 'USD', date: '2026-01-05T16:30:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_033', type: 'received', description: 'From Ana Gutierrez', amount: 35.00, currency: 'USD', date: '2026-01-03T14:20:00Z', status: 'completed', paymentMethod: 'balance', category: 'Personal' },
    { id: 'txn_034', type: 'payment', description: 'Instacart', amount: -78.43, currency: 'USD', date: '2025-12-30T12:00:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Food & Drink' },
    { id: 'txn_035', type: 'payment', description: 'REI', amount: -234.95, currency: 'USD', date: '2025-12-28T10:30:00Z', status: 'completed', paymentMethod: 'card_003', category: 'Shopping' },
    { id: 'txn_036', type: 'transfer_in', description: 'From Bank of America ***3891', amount: 500.00, currency: 'USD', date: '2025-12-22T09:00:00Z', status: 'completed', paymentMethod: 'bank_002', category: 'Transfer' },
    { id: 'txn_037', type: 'payment', description: 'Airbnb', amount: -425.00, currency: 'EUR', date: '2025-12-18T14:00:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Travel' },
    { id: 'txn_038', type: 'payment', description: 'British Airways', amount: -312.00, currency: 'GBP', date: '2025-12-15T08:30:00Z', status: 'completed', paymentMethod: 'card_001', category: 'Travel' },
    { id: 'txn_039', type: 'pending', description: 'Pending - eBay', amount: -45.00, currency: 'USD', date: '2026-03-07T06:00:00Z', status: 'pending', paymentMethod: 'card_001', category: 'Shopping' },
    { id: 'txn_040', type: 'pending', description: 'Pending - Google Cloud', amount: -12.34, currency: 'USD', date: '2026-03-07T02:00:00Z', status: 'pending', paymentMethod: 'card_002', category: 'Services' }
];

// ---- PayPal Credit Line ----
const PAYPAL_CREDIT = {
    id: 'ppc_001',
    status: 'active',
    creditLimit: 5000.00,
    currentBalance: 1245.67,
    availableCredit: 3754.33,
    minimumPaymentDue: 35.00,
    paymentDueDate: '2026-03-22T00:00:00Z',
    apr: 25.99,
    lastStatementDate: '2026-02-22T00:00:00Z',
    lastStatementBalance: 1580.23,
    lastPaymentAmount: 334.56,
    lastPaymentDate: '2026-03-01T10:00:00Z',
    autopayEnabled: true,
    autopayAmount: 'minimum'
};

// ---- Preferences/Settings ----
const WALLET_PREFERENCES = {
    preferredPaymentMethod: 'card_001',
    backupPaymentMethod: 'bank_001',
    onlinePaymentPreference: 'preferred',
    inStorePaymentPreference: 'paypal_balance',
    autoAcceptPayments: true,
    instantTransferPreference: true,
    currencyConversionOption: 'paypal',
    emailNotifications: {
        payments: true,
        transfers: true,
        securityAlerts: true,
        promotions: false,
        cryptoAlerts: true,
        rewardsUpdates: true,
        weeklyDigest: true
    }
};

// ---- Available Gift Card Merchants ----
const GIFT_CARD_MERCHANTS = [
    { id: 'gcm_001', name: 'Amazon', denominations: [10, 25, 50, 100, 150, 200, 500], category: 'Shopping' },
    { id: 'gcm_002', name: 'Starbucks', denominations: [10, 15, 25, 50, 75], category: 'Food & Drink' },
    { id: 'gcm_003', name: 'Target', denominations: [10, 25, 50, 100, 200], category: 'Shopping' },
    { id: 'gcm_004', name: 'Netflix', denominations: [15, 30, 50, 100], category: 'Entertainment' },
    { id: 'gcm_005', name: 'Apple', denominations: [15, 25, 50, 100, 200], category: 'Tech' },
    { id: 'gcm_006', name: 'Google Play', denominations: [10, 15, 25, 50, 100], category: 'Tech' },
    { id: 'gcm_007', name: 'Home Depot', denominations: [25, 50, 75, 100, 200, 500], category: 'Home & Garden' },
    { id: 'gcm_008', name: 'Uber', denominations: [15, 25, 50, 100], category: 'Travel' },
    { id: 'gcm_009', name: 'Nike', denominations: [25, 50, 75, 100, 150, 200], category: 'Shopping' },
    { id: 'gcm_010', name: 'Spotify', denominations: [10, 30, 60], category: 'Entertainment' },
    { id: 'gcm_011', name: 'DoorDash', denominations: [15, 25, 50, 100], category: 'Food & Drink' },
    { id: 'gcm_012', name: 'Best Buy', denominations: [25, 50, 100, 150, 200, 500], category: 'Tech' },
    { id: 'gcm_013', name: 'Walmart', denominations: [10, 25, 50, 100, 200], category: 'Shopping' },
    { id: 'gcm_014', name: 'Sephora', denominations: [25, 50, 100, 150], category: 'Beauty' },
    { id: 'gcm_015', name: 'GameStop', denominations: [10, 25, 50, 100], category: 'Entertainment' }
];

// ---- Crypto Fee Schedule ----
const CRYPTO_FEE_SCHEDULE = [
    { minAmount: 1, maxAmount: 4.99, fee: 0.49 },
    { minAmount: 5, maxAmount: 24.99, fee: 0.99 },
    { minAmount: 25, maxAmount: 74.99, fee: 1.99 },
    { minAmount: 75, maxAmount: 200, fee: 2.49 },
    { minAmount: 200.01, maxAmount: null, feePercent: 1.50 }
];
