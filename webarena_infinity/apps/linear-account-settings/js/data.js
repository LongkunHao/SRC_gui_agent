// ============================================================
// data.js — Rich, realistic seed data for Linear Account Settings
// ============================================================
const SEED_DATA_VERSION = 1;

// ---- Current User (profile) ----
const CURRENT_USER = {
    id: 'usr_a1b2c3d4',
    fullName: 'Alex Morgan',
    username: 'alexmorgan',
    email: 'alex.morgan@acmecorp.io',
    avatarUrl: null,
    avatarColor: '#5E6AD2',
    timezone: 'America/Los_Angeles',
    createdAt: '2024-06-15T08:30:00Z',
    updatedAt: '2026-02-28T14:22:00Z'
};

// ---- Workspaces ----
const WORKSPACES = [
    {
        id: 'ws_01',
        name: 'Acme Corp',
        slug: 'acme-corp',
        role: 'Admin',
        memberCount: 47,
        joinedAt: '2024-06-15T08:30:00Z',
        avatarColor: '#5E6AD2',
        urlKey: 'acme'
    },
    {
        id: 'ws_02',
        name: 'Side Project Labs',
        slug: 'side-project-labs',
        role: 'Member',
        memberCount: 8,
        joinedAt: '2025-03-10T12:00:00Z',
        avatarColor: '#26B5CE',
        urlKey: 'sideproject'
    },
    {
        id: 'ws_03',
        name: 'Open Source Collective',
        slug: 'open-source-collective',
        role: 'Member',
        memberCount: 124,
        joinedAt: '2025-09-22T09:15:00Z',
        avatarColor: '#F2994A',
        urlKey: 'osc'
    }
];

// ---- Connected Accounts ----
const CONNECTED_ACCOUNTS = [
    {
        id: 'ca_01',
        provider: 'GitHub',
        providerIcon: 'github',
        accountName: 'alexmorgan',
        accountEmail: 'alex.morgan@acmecorp.io',
        connectedAt: '2024-06-16T10:00:00Z',
        status: 'active',
        scopes: ['repo', 'read:org', 'read:user']
    },
    {
        id: 'ca_02',
        provider: 'GitLab',
        providerIcon: 'gitlab',
        accountName: 'alex.morgan',
        accountEmail: 'alex.morgan@acmecorp.io',
        connectedAt: '2024-08-22T15:30:00Z',
        status: 'active',
        scopes: ['api', 'read_user']
    },
    {
        id: 'ca_03',
        provider: 'Slack',
        providerIcon: 'slack',
        accountName: 'Alex Morgan',
        accountEmail: 'alex.morgan@acmecorp.io',
        connectedAt: '2024-06-18T09:00:00Z',
        status: 'active',
        scopes: ['chat:write', 'users:read']
    },
    {
        id: 'ca_04',
        provider: 'Figma',
        providerIcon: 'figma',
        accountName: 'alex.morgan@acmecorp.io',
        accountEmail: 'alex.morgan@acmecorp.io',
        connectedAt: '2025-01-12T11:45:00Z',
        status: 'active',
        scopes: ['file_read']
    },
    {
        id: 'ca_05',
        provider: 'Google',
        providerIcon: 'google',
        accountName: 'alex.morgan@gmail.com',
        accountEmail: 'alex.morgan@gmail.com',
        connectedAt: '2024-06-15T08:31:00Z',
        status: 'active',
        scopes: ['email', 'profile']
    }
];

// ---- Preferences ----
const PREFERENCES = {
    // General
    defaultHomeView: 'Active issues',
    displayFullNames: true,
    firstDayOfWeek: 'Monday',
    convertTextEmojis: true,

    // Interface and theme
    interfaceTheme: 'System',
    fontSize: 'Default',
    usePointerCursor: false,

    // Desktop application
    openInDesktopApp: true,
    desktopNotificationBadge: true,
    enableSpellCheck: true,

    // Automations and workflows
    autoAssignOnCreate: false,
    autoAssignOnStarted: false,
    gitAttachmentFormat: 'Title only',
    onGitBranchCopyMoveToStarted: true,
    onGitBranchCopyAutoAssign: true
};

// ---- Theme Options ----
const THEME_OPTIONS = [
    'Light',
    'Dark',
    'System',
    'Light - Contrast',
    'Dark - Contrast'
];

// ---- Notifications ----
const NOTIFICATION_SETTINGS = {
    // Channels
    desktop: {
        enabled: true,
        issueAssigned: true,
        issueStatusChanged: true,
        issueCommented: true,
        issueMentioned: true,
        projectUpdated: true,
        cycleUpdated: false
    },
    mobile: {
        enabled: true,
        issueAssigned: true,
        issueStatusChanged: true,
        issueCommented: true,
        issueMentioned: true,
        projectUpdated: false,
        cycleUpdated: false
    },
    email: {
        enabled: true,
        issueAssigned: true,
        issueStatusChanged: true,
        issueCommented: false,
        issueMentioned: true,
        projectUpdated: false,
        cycleUpdated: false,
        // Digest settings
        sendUrgentImmediately: true,
        delayLowPriorityOutsideHours: true
    },
    slack: {
        enabled: false,
        issueAssigned: false,
        issueStatusChanged: false,
        issueCommented: false,
        issueMentioned: false,
        projectUpdated: false,
        cycleUpdated: false
    },
    // Communications
    receiveChangelogs: true,
    receiveDpaUpdates: true,
    receiveProductUpdates: false
};

// ---- Sessions ----
const SESSIONS = [
    {
        id: 'sess_01',
        deviceName: 'Chrome on macOS',
        deviceType: 'desktop',
        browser: 'Chrome 122',
        os: 'macOS Sonoma 14.3',
        ipAddress: '203.0.113.42',
        location: 'San Francisco, CA, US',
        lastSeenAt: '2026-03-06T09:30:00Z',
        signedInAt: '2026-02-01T08:00:00Z',
        isCurrent: true
    },
    {
        id: 'sess_02',
        deviceName: 'Safari on iPhone',
        deviceType: 'mobile',
        browser: 'Safari 17',
        os: 'iOS 17.3',
        ipAddress: '203.0.113.42',
        location: 'San Francisco, CA, US',
        lastSeenAt: '2026-03-05T22:15:00Z',
        signedInAt: '2026-01-15T12:30:00Z',
        isCurrent: false
    },
    {
        id: 'sess_03',
        deviceName: 'Linear Desktop on macOS',
        deviceType: 'desktop',
        browser: 'Linear Desktop 2.5',
        os: 'macOS Sonoma 14.3',
        ipAddress: '203.0.113.42',
        location: 'San Francisco, CA, US',
        lastSeenAt: '2026-03-06T08:45:00Z',
        signedInAt: '2025-12-10T09:00:00Z',
        isCurrent: false
    },
    {
        id: 'sess_04',
        deviceName: 'Firefox on Windows',
        deviceType: 'desktop',
        browser: 'Firefox 123',
        os: 'Windows 11',
        ipAddress: '198.51.100.73',
        location: 'New York, NY, US',
        lastSeenAt: '2026-02-28T16:00:00Z',
        signedInAt: '2026-02-20T14:00:00Z',
        isCurrent: false
    },
    {
        id: 'sess_05',
        deviceName: 'Chrome on Linux',
        deviceType: 'desktop',
        browser: 'Chrome 121',
        os: 'Ubuntu 22.04',
        ipAddress: '192.0.2.156',
        location: 'Austin, TX, US',
        lastSeenAt: '2026-02-15T11:30:00Z',
        signedInAt: '2026-01-05T10:00:00Z',
        isCurrent: false
    },
    {
        id: 'sess_06',
        deviceName: 'Safari on iPad',
        deviceType: 'tablet',
        browser: 'Safari 17',
        os: 'iPadOS 17.3',
        ipAddress: '203.0.113.42',
        location: 'San Francisco, CA, US',
        lastSeenAt: '2026-02-10T19:00:00Z',
        signedInAt: '2025-11-28T15:00:00Z',
        isCurrent: false
    },
    {
        id: 'sess_07',
        deviceName: 'Chrome on Android',
        deviceType: 'mobile',
        browser: 'Chrome 122',
        os: 'Android 14',
        ipAddress: '172.16.0.88',
        location: 'Los Angeles, CA, US',
        lastSeenAt: '2026-02-05T08:00:00Z',
        signedInAt: '2025-12-20T11:00:00Z',
        isCurrent: false
    },
    {
        id: 'sess_08',
        deviceName: 'Edge on Windows',
        deviceType: 'desktop',
        browser: 'Edge 122',
        os: 'Windows 10',
        ipAddress: '10.0.0.55',
        location: 'Seattle, WA, US',
        lastSeenAt: '2026-01-20T14:30:00Z',
        signedInAt: '2025-10-15T08:00:00Z',
        isCurrent: false
    }
];

// ---- Passkeys ----
const PASSKEYS = [
    {
        id: 'pk_01',
        name: 'MacBook Pro Touch ID',
        createdAt: '2025-08-15T10:30:00Z',
        lastUsedAt: '2026-03-05T09:00:00Z',
        credentialType: 'platform'
    },
    {
        id: 'pk_02',
        name: 'YubiKey 5C NFC',
        createdAt: '2025-09-01T14:00:00Z',
        lastUsedAt: '2026-02-20T11:00:00Z',
        credentialType: 'cross-platform'
    },
    {
        id: 'pk_03',
        name: 'iPhone Face ID',
        createdAt: '2025-11-10T16:45:00Z',
        lastUsedAt: '2026-03-04T22:00:00Z',
        credentialType: 'platform'
    }
];

// ---- Personal API Keys ----
const API_KEYS = [
    {
        id: 'apikey_01',
        label: 'CI/CD Pipeline',
        keyPrefix: 'lin_api_7f3a',
        createdAt: '2025-06-20T09:00:00Z',
        lastUsedAt: '2026-03-06T07:15:00Z',
        expiresAt: null
    },
    {
        id: 'apikey_02',
        label: 'Slack Bot Integration',
        keyPrefix: 'lin_api_9b2e',
        createdAt: '2025-08-10T13:30:00Z',
        lastUsedAt: '2026-03-05T18:00:00Z',
        expiresAt: '2026-08-10T13:30:00Z'
    },
    {
        id: 'apikey_03',
        label: 'Data Export Script',
        keyPrefix: 'lin_api_4d1c',
        createdAt: '2025-10-05T11:00:00Z',
        lastUsedAt: '2026-02-28T06:00:00Z',
        expiresAt: null
    },
    {
        id: 'apikey_04',
        label: 'Mobile App Testing',
        keyPrefix: 'lin_api_8e5f',
        createdAt: '2026-01-15T16:00:00Z',
        lastUsedAt: '2026-01-20T10:00:00Z',
        expiresAt: '2026-07-15T16:00:00Z'
    },
    {
        id: 'apikey_05',
        label: 'Monitoring Dashboard',
        keyPrefix: 'lin_api_2a7g',
        createdAt: '2025-04-02T08:00:00Z',
        lastUsedAt: '2026-03-06T06:45:00Z',
        expiresAt: null
    }
];

// ---- Authorized OAuth Applications ----
const AUTHORIZED_APPS = [
    {
        id: 'oauth_01',
        name: 'Raycast',
        description: 'Productivity launcher for macOS',
        icon: 'raycast',
        authorizedAt: '2025-07-10T09:00:00Z',
        lastAccessedAt: '2026-03-06T08:30:00Z',
        permissions: ['read:issues', 'write:issues', 'read:projects']
    },
    {
        id: 'oauth_02',
        name: 'Notion Integration',
        description: 'Sync Linear issues with Notion databases',
        icon: 'notion',
        authorizedAt: '2025-09-15T14:00:00Z',
        lastAccessedAt: '2026-03-05T12:00:00Z',
        permissions: ['read:issues', 'read:projects', 'read:teams']
    },
    {
        id: 'oauth_03',
        name: 'Zapier',
        description: 'Automation platform connecting Linear to 5000+ apps',
        icon: 'zapier',
        authorizedAt: '2025-05-20T11:30:00Z',
        lastAccessedAt: '2026-03-04T15:00:00Z',
        permissions: ['read:issues', 'write:issues', 'read:projects', 'write:projects', 'read:teams']
    },
    {
        id: 'oauth_04',
        name: 'Linear Exporter',
        description: 'Export Linear data to CSV and Excel formats',
        icon: 'generic',
        authorizedAt: '2025-11-01T10:00:00Z',
        lastAccessedAt: '2026-02-15T09:00:00Z',
        permissions: ['read:issues', 'read:projects', 'read:teams', 'read:users']
    },
    {
        id: 'oauth_05',
        name: 'Screenful',
        description: 'Analytics and insights for Linear projects',
        icon: 'generic',
        authorizedAt: '2026-01-08T16:00:00Z',
        lastAccessedAt: '2026-03-06T07:00:00Z',
        permissions: ['read:issues', 'read:projects', 'read:cycles', 'read:teams']
    },
    {
        id: 'oauth_06',
        name: 'Marker.io',
        description: 'Visual bug reporting tool with Linear integration',
        icon: 'generic',
        authorizedAt: '2025-12-15T13:00:00Z',
        lastAccessedAt: '2026-02-28T17:00:00Z',
        permissions: ['read:issues', 'write:issues', 'read:teams']
    }
];

// ---- Dropdown Options ----
const HOME_VIEW_OPTIONS = [
    'All issues',
    'Active issues',
    'Current cycle',
    'Inbox',
    'My Issues',
    'Favorited Views',
    'Favorited Projects'
];

const FIRST_DAY_OPTIONS = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday'
];

const FONT_SIZE_OPTIONS = [
    'Small',
    'Default',
    'Large'
];

const GIT_ATTACHMENT_FORMAT_OPTIONS = [
    'Title only',
    'Title and repository'
];

// ---- Timezone Options ----
const TIMEZONE_OPTIONS = [
    'America/New_York',
    'America/Chicago',
    'America/Denver',
    'America/Los_Angeles',
    'America/Anchorage',
    'Pacific/Honolulu',
    'America/Toronto',
    'America/Vancouver',
    'America/Sao_Paulo',
    'America/Mexico_City',
    'Europe/London',
    'Europe/Paris',
    'Europe/Berlin',
    'Europe/Amsterdam',
    'Europe/Stockholm',
    'Europe/Helsinki',
    'Europe/Moscow',
    'Asia/Dubai',
    'Asia/Kolkata',
    'Asia/Shanghai',
    'Asia/Tokyo',
    'Asia/Seoul',
    'Asia/Singapore',
    'Australia/Sydney',
    'Australia/Melbourne',
    'Pacific/Auckland'
];
