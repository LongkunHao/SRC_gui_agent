const SEED_DATA_VERSION = 1;

const CURRENT_USER = {
    id: 'user_001',
    name: 'Sarah Chen',
    email: 'sarah.chen@designcraft.io',
    avatarColor: '#7B61FF',
    initials: 'SC',
    role: 'Editor',
    plan: 'Professional',
    teamName: 'DesignCraft',
    teamId: 'team_001'
};

const COLLABORATORS = [
    { id: 'user_002', name: 'Marcus Rivera', email: 'marcus.r@designcraft.io', avatarColor: '#F24E1E', initials: 'MR', role: 'Editor', online: true },
    { id: 'user_003', name: 'Aiko Tanaka', email: 'aiko.t@designcraft.io', avatarColor: '#0ACF83', initials: 'AT', role: 'Editor', online: true },
    { id: 'user_004', name: 'James O\'Brien', email: 'james.ob@designcraft.io', avatarColor: '#1ABCFE', initials: 'JO', role: 'Viewer', online: false },
    { id: 'user_005', name: 'Priya Sharma', email: 'priya.s@designcraft.io', avatarColor: '#FF7262', initials: 'PS', role: 'Editor', online: false },
    { id: 'user_006', name: 'Tom Nguyen', email: 'tom.n@designcraft.io', avatarColor: '#A259FF', initials: 'TN', role: 'Viewer', online: true },
    { id: 'user_007', name: 'Elena Kowalski', email: 'elena.k@designcraft.io', avatarColor: '#FF6B6B', initials: 'EK', role: 'Editor', online: false },
    { id: 'user_008', name: 'David Park', email: 'david.p@designcraft.io', avatarColor: '#4ECDC4', initials: 'DP', role: 'Editor', online: true }
];

const TEMPLATE_STYLES = [
    {
        id: 'ts_001',
        name: 'Minimal Dark',
        colors: [
            { id: 'tc_001', name: 'Background', value: '#1E1E1E' },
            { id: 'tc_002', name: 'Surface', value: '#2C2C2C' },
            { id: 'tc_003', name: 'Primary', value: '#7B61FF' },
            { id: 'tc_004', name: 'Accent', value: '#0ACF83' },
            { id: 'tc_005', name: 'Text Primary', value: '#FFFFFF' },
            { id: 'tc_006', name: 'Text Secondary', value: '#B3B3B3' }
        ],
        textStyles: [
            { id: 'txt_001', name: 'Heading 1', fontFamily: 'Inter', fontSize: 48, fontWeight: 700, lineHeight: 1.2, letterSpacing: -0.02 },
            { id: 'txt_002', name: 'Heading 2', fontFamily: 'Inter', fontSize: 36, fontWeight: 600, lineHeight: 1.3, letterSpacing: -0.01 },
            { id: 'txt_003', name: 'Heading 3', fontFamily: 'Inter', fontSize: 24, fontWeight: 600, lineHeight: 1.4, letterSpacing: 0 },
            { id: 'txt_004', name: 'Body', fontFamily: 'Inter', fontSize: 16, fontWeight: 400, lineHeight: 1.6, letterSpacing: 0 },
            { id: 'txt_005', name: 'Caption', fontFamily: 'Inter', fontSize: 12, fontWeight: 400, lineHeight: 1.5, letterSpacing: 0.01 }
        ]
    },
    {
        id: 'ts_002',
        name: 'Corporate Blue',
        colors: [
            { id: 'tc_011', name: 'Background', value: '#FFFFFF' },
            { id: 'tc_012', name: 'Surface', value: '#F5F7FA' },
            { id: 'tc_013', name: 'Primary', value: '#0052CC' },
            { id: 'tc_014', name: 'Accent', value: '#00B8D9' },
            { id: 'tc_015', name: 'Text Primary', value: '#172B4D' },
            { id: 'tc_016', name: 'Text Secondary', value: '#6B778C' }
        ],
        textStyles: [
            { id: 'txt_011', name: 'Heading 1', fontFamily: 'Plus Jakarta Sans', fontSize: 44, fontWeight: 700, lineHeight: 1.2, letterSpacing: -0.02 },
            { id: 'txt_012', name: 'Heading 2', fontFamily: 'Plus Jakarta Sans', fontSize: 32, fontWeight: 600, lineHeight: 1.3, letterSpacing: -0.01 },
            { id: 'txt_013', name: 'Heading 3', fontFamily: 'Plus Jakarta Sans', fontSize: 22, fontWeight: 600, lineHeight: 1.4, letterSpacing: 0 },
            { id: 'txt_014', name: 'Body', fontFamily: 'Inter', fontSize: 16, fontWeight: 400, lineHeight: 1.6, letterSpacing: 0 },
            { id: 'txt_015', name: 'Caption', fontFamily: 'Inter', fontSize: 11, fontWeight: 400, lineHeight: 1.5, letterSpacing: 0.02 }
        ]
    },
    {
        id: 'ts_003',
        name: 'Warm Sunset',
        colors: [
            { id: 'tc_021', name: 'Background', value: '#FFF8F0' },
            { id: 'tc_022', name: 'Surface', value: '#FFECD2' },
            { id: 'tc_023', name: 'Primary', value: '#FF6B35' },
            { id: 'tc_024', name: 'Accent', value: '#F7C948' },
            { id: 'tc_025', name: 'Text Primary', value: '#2D1B00' },
            { id: 'tc_026', name: 'Text Secondary', value: '#8B6914' }
        ],
        textStyles: [
            { id: 'txt_021', name: 'Heading 1', fontFamily: 'DM Sans', fontSize: 48, fontWeight: 700, lineHeight: 1.15, letterSpacing: -0.03 },
            { id: 'txt_022', name: 'Heading 2', fontFamily: 'DM Sans', fontSize: 34, fontWeight: 600, lineHeight: 1.25, letterSpacing: -0.01 },
            { id: 'txt_023', name: 'Heading 3', fontFamily: 'DM Sans', fontSize: 24, fontWeight: 600, lineHeight: 1.35, letterSpacing: 0 },
            { id: 'txt_024', name: 'Body', fontFamily: 'DM Sans', fontSize: 16, fontWeight: 400, lineHeight: 1.6, letterSpacing: 0 },
            { id: 'txt_025', name: 'Caption', fontFamily: 'DM Sans', fontSize: 12, fontWeight: 400, lineHeight: 1.5, letterSpacing: 0.01 }
        ]
    }
];

const SLIDE_LAYOUTS = [
    { id: 'layout_title', name: 'Title Slide', category: 'Title', description: 'Large centered title with subtitle' },
    { id: 'layout_title_content', name: 'Title and Content', category: 'Content', description: 'Title at top with content area below' },
    { id: 'layout_two_column', name: 'Two Columns', category: 'Content', description: 'Title with two equal content columns' },
    { id: 'layout_image_left', name: 'Image Left', category: 'Media', description: 'Image on left, content on right' },
    { id: 'layout_image_right', name: 'Image Right', category: 'Media', description: 'Content on left, image on right' },
    { id: 'layout_full_image', name: 'Full Image', category: 'Media', description: 'Full-bleed background image with text overlay' },
    { id: 'layout_section', name: 'Section Divider', category: 'Title', description: 'Section break with large text' },
    { id: 'layout_quote', name: 'Quote', category: 'Content', description: 'Large quote with attribution' },
    { id: 'layout_blank', name: 'Blank', category: 'Blank', description: 'Empty slide with no predefined layout' },
    { id: 'layout_three_column', name: 'Three Columns', category: 'Content', description: 'Title with three content columns' },
    { id: 'layout_comparison', name: 'Comparison', category: 'Content', description: 'Side-by-side comparison layout' },
    { id: 'layout_closing', name: 'Closing', category: 'Title', description: 'Thank you / closing slide' }
];

const TRANSITION_TYPES = [
    { id: 'none', name: 'None', description: 'No transition', hasDirection: false },
    { id: 'dissolve', name: 'Dissolve', description: 'Fade in next slide on top of previous', hasDirection: false },
    { id: 'smart_animate', name: 'Smart Animate', description: 'Matches objects between slides to create motion', hasDirection: false },
    { id: 'push', name: 'Push', description: 'Push out previous slide as next enters', hasDirection: true, directions: ['left', 'right', 'top', 'bottom'] },
    { id: 'slide_in', name: 'Slide In', description: 'Move next slide in while dissolving previous', hasDirection: true, directions: ['left', 'right', 'top', 'bottom'] },
    { id: 'slide_out', name: 'Slide Out', description: 'Move previous slide out to reveal next behind', hasDirection: true, directions: ['left', 'right', 'top', 'bottom'] },
    { id: 'move_in', name: 'Move In', description: 'Move next slide into view above previous', hasDirection: true, directions: ['left', 'right', 'top', 'bottom'] },
    { id: 'move_out', name: 'Move Out', description: 'Move previous slide out of view', hasDirection: true, directions: ['left', 'right', 'top', 'bottom'] }
];

const ANIMATION_STYLES = [
    { id: 'fade', name: 'Fade', description: 'Fade in or out' },
    { id: 'scale', name: 'Scale', description: 'Scale up from small or down to small' },
    { id: 'slide_up', name: 'Slide Up', description: 'Slide in from below' },
    { id: 'slide_down', name: 'Slide Down', description: 'Slide in from above' },
    { id: 'slide_left', name: 'Slide Left', description: 'Slide in from right' },
    { id: 'slide_right', name: 'Slide Right', description: 'Slide in from left' },
    { id: 'bounce', name: 'Bounce', description: 'Bounce effect' },
    { id: 'pop', name: 'Pop', description: 'Quick pop-in effect' }
];

const EASING_PRESETS = [
    { id: 'ease', name: 'Ease' },
    { id: 'ease_in', name: 'Ease In' },
    { id: 'ease_out', name: 'Ease Out' },
    { id: 'ease_in_out', name: 'Ease In Out' },
    { id: 'linear', name: 'Linear' },
    { id: 'spring', name: 'Spring' },
    { id: 'bounce', name: 'Bounce' }
];

const CODE_LANGUAGES = [
    'JavaScript', 'TypeScript', 'Python', 'HTML', 'CSS', 'Java', 'C++', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin', 'PHP', 'SQL', 'Shell', 'JSON', 'YAML', 'Markdown', 'Plain Text'
];

const CODE_THEMES = [
    { id: 'dark', name: 'Dark' },
    { id: 'light', name: 'Light' },
    { id: 'monokai', name: 'Monokai' },
    { id: 'github', name: 'GitHub' },
    { id: 'dracula', name: 'Dracula' },
    { id: 'solarized', name: 'Solarized' }
];

const SHAPE_TYPES = [
    { id: 'rectangle', name: 'Rectangle', icon: 'rect' },
    { id: 'ellipse', name: 'Ellipse', icon: 'circle' },
    { id: 'triangle', name: 'Triangle', icon: 'triangle' },
    { id: 'diamond', name: 'Diamond', icon: 'diamond' },
    { id: 'arrow_right', name: 'Arrow Right', icon: 'arrow' },
    { id: 'star', name: 'Star', icon: 'star' },
    { id: 'rounded_rect', name: 'Rounded Rectangle', icon: 'rounded' },
    { id: 'hexagon', name: 'Hexagon', icon: 'hexagon' },
    { id: 'callout', name: 'Callout', icon: 'callout' },
    { id: 'pill', name: 'Pill', icon: 'pill' }
];

const FILL_MODES = [
    { id: 'fill', name: 'Fill', description: 'Scales visual to fill entire area' },
    { id: 'fit', name: 'Fit', description: 'Entire visual visible in area' },
    { id: 'crop', name: 'Crop', description: 'Adjust boundary to clip image' },
    { id: 'tile', name: 'Tile', description: 'Repeat pattern to fill area' }
];

const EXPORT_FORMATS = [
    { id: 'pptx', name: 'PowerPoint (.pptx)' },
    { id: 'pdf', name: 'PDF (.pdf)' }
];

const PDF_COLOR_PROFILES = [
    { id: 'srgb', name: 'sRGB' },
    { id: 'display_p3', name: 'Display P3' }
];

const PDF_QUALITY_OPTIONS = [
    { id: 'low', name: 'Low' },
    { id: 'medium', name: 'Medium' },
    { id: 'high', name: 'High' },
    { id: 'best', name: 'Best' }
];

const SLIDE_NUMBER_FORMATS = [
    { id: 'number_only', name: 'Number only', example: '3' },
    { id: 'with_total', name: 'With total', example: '3/24' },
    { id: 'padded', name: 'Padded', example: '03' },
    { id: 'dot_separated', name: 'Dot separated', example: '3.24' }
];

function generateSlideId() {
    return 'slide_' + Math.random().toString(36).substring(2, 10);
}

function generateObjectId() {
    return 'obj_' + Math.random().toString(36).substring(2, 10);
}

const SLIDES = [
    {
        id: 'slide_001',
        order: 0,
        title: 'Q4 2025 Product Strategy',
        layout: 'layout_title',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: null,
        groupName: null,
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: '**Welcome everyone!** Thanks for joining the Q4 strategy review.\n\n- Cover product roadmap\n- Key metrics from Q3\n- Team assignments for Q4\n\nRemember to mention the new *design system* launch.',
        transition: { type: 'none', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_001',
                type: 'text',
                name: 'Title',
                x: 120, y: 200, width: 960, height: 120,
                text: 'Q4 2025 Product Strategy',
                fontSize: 52, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100,
                rotation: 0,
                locked: false,
                visible: true,
                animation: { style: 'fade', duration: 600, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_002',
                type: 'text',
                name: 'Subtitle',
                x: 240, y: 340, width: 720, height: 60,
                text: 'DesignCraft - Building the Future of Design Collaboration',
                fontSize: 20, fontWeight: 400, fontFamily: 'Inter',
                color: '#B3B3B3',
                textAlign: 'center',
                opacity: 100,
                rotation: 0,
                locked: false,
                visible: true,
                animation: { style: 'fade', duration: 400, timing: 'after_previous', direction: 'in', order: 1 }
            },
            {
                id: 'obj_003',
                type: 'text',
                name: 'Date',
                x: 440, y: 420, width: 320, height: 40,
                text: 'October 15, 2025',
                fontSize: 14, fontWeight: 400, fontFamily: 'Inter',
                color: '#666666',
                textAlign: 'center',
                opacity: 100,
                rotation: 0,
                locked: false,
                visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_002',
        order: 1,
        title: 'Agenda',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: null,
        groupName: null,
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Walk through the agenda items quickly. Each section has its own presenter.\n\n1. Product recap - Sarah (5 min)\n2. Metrics review - Marcus (10 min)\n3. Roadmap deep dive - Aiko (15 min)\n4. Q&A - Everyone (10 min)',
        transition: { type: 'dissolve', direction: null, easing: 'ease_out', duration: 500, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_010',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Agenda',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_011',
                type: 'text',
                name: 'Agenda List',
                x: 80, y: 150, width: 600, height: 280,
                text: '1. Q3 Product Recap & Highlights\n2. Key Metrics & Growth Analysis\n3. Q4 Roadmap Deep Dive\n4. Design System 2.0 Launch Plan\n5. Resource Allocation & Team Updates\n6. Open Discussion & Q&A',
                fontSize: 20, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'slide_up', duration: 500, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_012',
                type: 'shape',
                name: 'Accent Line',
                shapeType: 'rectangle',
                x: 80, y: 130, width: 60, height: 4,
                fill: '#7B61FF',
                stroke: null,
                text: '',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_003',
        order: 2,
        title: 'Q3 Highlights',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_001',
        groupName: 'Q3 Review',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Focus on the **3 main wins** this quarter. User growth was exceptional.',
        transition: { type: 'push', direction: 'left', easing: 'ease_in_out', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_020',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Q3 Highlights',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_021',
                type: 'shape',
                name: 'Metric Card 1',
                shapeType: 'rounded_rect',
                x: 80, y: 150, width: 260, height: 160,
                fill: '#2C2C2C',
                stroke: null,
                cornerRadius: 12,
                text: '2.4M\nActive Users\n+32% YoY',
                fontSize: 16, fontWeight: 600, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'scale', duration: 400, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_022',
                type: 'shape',
                name: 'Metric Card 2',
                shapeType: 'rounded_rect',
                x: 370, y: 150, width: 260, height: 160,
                fill: '#2C2C2C',
                stroke: null,
                cornerRadius: 12,
                text: '$18.7M\nARR\n+28% YoY',
                fontSize: 16, fontWeight: 600, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'scale', duration: 400, timing: 'after_previous', direction: 'in', order: 1 }
            },
            {
                id: 'obj_023',
                type: 'shape',
                name: 'Metric Card 3',
                shapeType: 'rounded_rect',
                x: 660, y: 150, width: 260, height: 160,
                fill: '#2C2C2C',
                stroke: null,
                cornerRadius: 12,
                text: '98.2%\nUptime\nSLA Target: 99%',
                fontSize: 16, fontWeight: 600, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'scale', duration: 400, timing: 'after_previous', direction: 'in', order: 2 }
            }
        ]
    },
    {
        id: 'slide_004',
        order: 3,
        title: 'Growth Metrics',
        layout: 'layout_two_column',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_001',
        groupName: 'Q3 Review',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Growth is driven by our freemium model. Conversion rate improved after the onboarding redesign.\n\n*Key insight:* Enterprise segment grew 45% - our biggest growth area.',
        transition: { type: 'slide_in', direction: 'right', easing: 'ease', duration: 350, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_030',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 800, height: 60,
                text: 'Growth Metrics Deep Dive',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_031',
                type: 'text',
                name: 'Left Column',
                x: 80, y: 150, width: 400, height: 300,
                text: 'User Acquisition\n\nOrganic: 45%\nPaid Search: 22%\nReferrals: 18%\nSocial: 10%\nDirect: 5%',
                fontSize: 16, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_032',
                type: 'text',
                name: 'Right Column',
                x: 540, y: 150, width: 400, height: 300,
                text: 'Revenue Breakdown\n\nEnterprise: $9.4M (+45%)\nProfessional: $6.2M (+22%)\nStarter: $2.1M (+15%)\nFree-to-Paid: $1.0M (+38%)',
                fontSize: 16, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_005',
        order: 4,
        title: 'Customer Feedback',
        layout: 'layout_quote',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_001',
        groupName: 'Q3 Review',
        background: { type: 'gradient', gradient: { type: 'linear', angle: 135, stops: [{ color: '#1E1E1E', position: 0 }, { color: '#2D1B69', position: 100 }] } },
        presenterNotes: 'This quote is from our biggest enterprise customer. They renewed for 3 years!',
        transition: { type: 'dissolve', direction: null, easing: 'ease', duration: 500, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_040',
                type: 'text',
                name: 'Quote',
                x: 120, y: 160, width: 760, height: 160,
                text: '"DesignCraft has transformed how our entire product team collaborates. The real-time features alone saved us 200+ hours per quarter."',
                fontSize: 28, fontWeight: 400, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                fontStyle: 'italic',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'fade', duration: 600, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_041',
                type: 'text',
                name: 'Attribution',
                x: 300, y: 360, width: 400, height: 40,
                text: '-- Jennifer Wu, VP of Product, TechGlobal Inc.',
                fontSize: 16, fontWeight: 400, fontFamily: 'Inter',
                color: '#A78BFA',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'fade', duration: 300, timing: 'after_previous', direction: 'in', order: 1 }
            }
        ]
    },
    {
        id: 'slide_006',
        order: 5,
        title: 'Q4 Roadmap',
        layout: 'layout_section',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_002',
        groupName: 'Q4 Planning',
        background: { type: 'solid', color: '#7B61FF' },
        presenterNotes: 'Transition to the roadmap section. Let Aiko take over here.',
        transition: { type: 'push', direction: 'left', easing: 'spring', duration: 500, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_050',
                type: 'text',
                name: 'Section Title',
                x: 120, y: 200, width: 800, height: 100,
                text: 'Q4 Roadmap',
                fontSize: 64, fontWeight: 800, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'pop', duration: 300, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_051',
                type: 'text',
                name: 'Section Subtitle',
                x: 200, y: 310, width: 600, height: 40,
                text: 'What we\'re building next',
                fontSize: 20, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0D4FF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_007',
        order: 6,
        title: 'Design System 2.0',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_002',
        groupName: 'Q4 Planning',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'DS 2.0 is our highest priority. Beta in November, GA in January.\n\nKey improvements:\n- Token-based architecture\n- Better dark mode support\n- Accessibility audit complete',
        transition: { type: 'smart_animate', direction: null, easing: 'ease_in_out', duration: 500, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_060',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Design System 2.0',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_061',
                type: 'text',
                name: 'Content',
                x: 80, y: 150, width: 500, height: 280,
                text: 'Key Features:\n\nToken-based theming architecture\nAdvanced dark mode with auto-detection\nFull WCAG 2.1 AA compliance\n14 new component primitives\nFigma plugin for design-to-code sync\nReact, Vue, and Svelte bindings',
                fontSize: 16, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'slide_up', duration: 400, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_062',
                type: 'shape',
                name: 'Timeline Badge',
                shapeType: 'pill',
                x: 660, y: 170, width: 240, height: 44,
                fill: '#0ACF83',
                stroke: null,
                text: 'Beta: Nov 2025',
                fontSize: 14, fontWeight: 600, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'pop', duration: 300, timing: 'after_previous', direction: 'in', order: 1 }
            },
            {
                id: 'obj_063',
                type: 'shape',
                name: 'GA Badge',
                shapeType: 'pill',
                x: 660, y: 230, width: 240, height: 44,
                fill: '#7B61FF',
                stroke: null,
                text: 'GA: Jan 2026',
                fontSize: 14, fontWeight: 600, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'pop', duration: 300, timing: 'after_previous', direction: 'in', order: 2 }
            }
        ]
    },
    {
        id: 'slide_008',
        order: 7,
        title: 'API Reference',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_002',
        groupName: 'Q4 Planning',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Show the code example briefly. Emphasize the simplicity of our new SDK.',
        transition: { type: 'dissolve', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_070',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'New SDK Preview',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_071',
                type: 'code',
                name: 'Code Example',
                x: 80, y: 150, width: 840, height: 240,
                code: 'import { DesignCraft } from \'@designcraft/sdk\';\n\nconst client = new DesignCraft({\n  apiKey: process.env.DC_API_KEY,\n  workspace: \'designcraft-team\'\n});\n\nconst components = await client.library.list({\n  filter: { type: \'component\', status: \'published\' }\n});\n\nconsole.log(`Found ${components.length} components`);',
                language: 'JavaScript',
                theme: 'monokai',
                fontSize: 14,
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'fade', duration: 400, timing: 'on_click', direction: 'in', order: 0 }
            }
        ]
    },
    {
        id: 'slide_009',
        order: 8,
        title: 'Team Survey Results',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_002',
        groupName: 'Q4 Planning',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Results from our last team alignment survey. Good sentiment overall but some concerns about timeline.',
        transition: { type: 'dissolve', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_080',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Team Survey Results',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_081',
                type: 'liveInteraction',
                interactionType: 'poll',
                name: 'Priority Poll',
                x: 80, y: 150, width: 400, height: 280,
                question: 'What should we prioritize in Q4?',
                options: [
                    { id: 'opt_01', text: 'Design System 2.0', votes: 12 },
                    { id: 'opt_02', text: 'Performance improvements', votes: 8 },
                    { id: 'opt_03', text: 'Mobile app', votes: 5 },
                    { id: 'opt_04', text: 'AI features', votes: 15 },
                    { id: 'opt_05', text: 'Developer API', votes: 6 }
                ],
                hideResults: false,
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_082',
                type: 'liveInteraction',
                interactionType: 'alignment',
                name: 'Timeline Confidence',
                x: 540, y: 150, width: 380, height: 200,
                question: 'How confident are you in the Q4 timeline?',
                scaleMin: 1,
                scaleMax: 5,
                scaleLabels: { min: 'Not confident', max: 'Very confident' },
                responses: [
                    { userId: 'user_002', value: 4 },
                    { userId: 'user_003', value: 3 },
                    { userId: 'user_005', value: 2 },
                    { userId: 'user_007', value: 4 },
                    { userId: 'user_008', value: 5 }
                ],
                hideResults: false,
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_010',
        order: 9,
        title: 'Data Comparison',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_002',
        groupName: 'Q4 Planning',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Compare feature adoption across quarters. Focus on the trajectory, not absolute numbers.',
        transition: { type: 'dissolve', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_090',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Feature Adoption by Quarter',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_091',
                type: 'table',
                name: 'Adoption Table',
                x: 80, y: 150, width: 840, height: 280,
                rows: 6,
                columns: 5,
                cells: [
                    ['Feature', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Target Q4'],
                    ['Real-time Collab', '68%', '72%', '81%', '90%'],
                    ['Design Tokens', '12%', '25%', '41%', '60%'],
                    ['Auto Layout', '45%', '52%', '58%', '70%'],
                    ['AI Assist', '--', '8%', '22%', '40%'],
                    ['Dev Handoff', '55%', '60%', '67%', '80%']
                ],
                headerRow: true,
                headerStyle: { background: '#2C2C2C', color: '#FFFFFF', fontWeight: 700 },
                cellStyle: { background: 'transparent', color: '#E0E0E0', fontWeight: 400 },
                borderColor: '#404040',
                fontSize: 14,
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'fade', duration: 500, timing: 'on_click', direction: 'in', order: 0 }
            }
        ]
    },
    {
        id: 'slide_011',
        order: 10,
        title: 'Resource Allocation',
        layout: 'layout_three_column',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: 'group_003',
        groupName: 'Team Updates',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Three streams running in parallel. Design System has the most headcount.\n\nNote: Mobile team is borrowing 2 engineers from Platform.',
        transition: { type: 'move_in', direction: 'bottom', easing: 'ease_out', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_100',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 800, height: 60,
                text: 'Team Resource Allocation',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_101',
                type: 'shape',
                name: 'Team A Card',
                shapeType: 'rounded_rect',
                x: 60, y: 150, width: 280, height: 260,
                fill: '#2C2C2C',
                stroke: { color: '#7B61FF', width: 2 },
                cornerRadius: 12,
                text: 'Design System\n\n8 Engineers\n3 Designers\n1 PM\n\nLead: Aiko Tanaka\nStatus: On Track',
                fontSize: 14, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'slide_up', duration: 400, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_102',
                type: 'shape',
                name: 'Team B Card',
                shapeType: 'rounded_rect',
                x: 370, y: 150, width: 280, height: 260,
                fill: '#2C2C2C',
                stroke: { color: '#0ACF83', width: 2 },
                cornerRadius: 12,
                text: 'Platform & API\n\n5 Engineers\n1 Designer\n1 PM\n\nLead: Marcus Rivera\nStatus: At Risk',
                fontSize: 14, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'slide_up', duration: 400, timing: 'after_previous', direction: 'in', order: 1 }
            },
            {
                id: 'obj_103',
                type: 'shape',
                name: 'Team C Card',
                shapeType: 'rounded_rect',
                x: 680, y: 150, width: 280, height: 260,
                fill: '#2C2C2C',
                stroke: { color: '#F24E1E', width: 2 },
                cornerRadius: 12,
                text: 'Mobile App\n\n4 Engineers\n2 Designers\n1 PM\n\nLead: Elena Kowalski\nStatus: Planning',
                fontSize: 14, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'slide_up', duration: 400, timing: 'after_previous', direction: 'in', order: 2 }
            }
        ]
    },
    {
        id: 'slide_012',
        order: 11,
        title: 'Sprint Timeline',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: true,
        groupId: 'group_003',
        groupName: 'Team Updates',
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: '*SKIPPED* - This slide has outdated timeline info. Keep for reference but don\'t present.',
        transition: { type: 'none', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
        slideNumberEnabled: false,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_110',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Sprint Timeline (DRAFT)',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_111',
                type: 'text',
                name: 'Timeline Content',
                x: 80, y: 150, width: 800, height: 200,
                text: 'Sprint 1 (Oct 1-14): Foundation & Setup\nSprint 2 (Oct 15-28): Core Components\nSprint 3 (Oct 29 - Nov 11): Integration Testing\nSprint 4 (Nov 12-25): Beta Release\nSprint 5 (Nov 26 - Dec 9): Feedback & Iteration\nSprint 6 (Dec 10-23): Final Polish',
                fontSize: 16, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_013',
        order: 12,
        title: 'Competitive Landscape',
        layout: 'layout_comparison',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: null,
        groupName: null,
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Sensitive slide - do not share externally. For internal discussion only.\n\nOur key differentiator is the integrated design-to-code pipeline.',
        transition: { type: 'dissolve', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_120',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 800, height: 60,
                text: 'Competitive Landscape',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_121',
                type: 'table',
                name: 'Comparison Table',
                x: 80, y: 140, width: 840, height: 300,
                rows: 7,
                columns: 4,
                cells: [
                    ['Capability', 'DesignCraft', 'Competitor A', 'Competitor B'],
                    ['Real-time Collab', 'Full', 'Limited', 'Full'],
                    ['Design Tokens', 'Native', 'Plugin', 'None'],
                    ['Dev Handoff', 'Integrated', 'Separate tool', 'Basic'],
                    ['AI Features', 'Built-in', 'Beta', 'Planned'],
                    ['Pricing (Team)', '$15/user/mo', '$20/user/mo', '$12/user/mo'],
                    ['API Access', 'Full REST + SDK', 'REST only', 'Webhooks only']
                ],
                headerRow: true,
                headerStyle: { background: '#7B61FF', color: '#FFFFFF', fontWeight: 700 },
                cellStyle: { background: 'transparent', color: '#E0E0E0', fontWeight: 400 },
                borderColor: '#404040',
                fontSize: 13,
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_014',
        order: 13,
        title: 'Key Risks & Mitigations',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: null,
        groupName: null,
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Be transparent about risks. The team appreciates honesty.\n\nMost critical risk is the hiring timeline for mobile engineers.',
        transition: { type: 'slide_in', direction: 'left', easing: 'ease_in_out', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_130',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Key Risks & Mitigations',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_131',
                type: 'shape',
                name: 'Risk 1',
                shapeType: 'rounded_rect',
                x: 80, y: 150, width: 400, height: 80,
                fill: '#3D1010',
                stroke: { color: '#F24E1E', width: 1 },
                cornerRadius: 8,
                text: 'HIGH: Mobile team understaffed\nMitigation: Contractor augmentation',
                fontSize: 13, fontWeight: 400, fontFamily: 'Inter',
                color: '#FF9B9B',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_132',
                type: 'shape',
                name: 'Risk 2',
                shapeType: 'rounded_rect',
                x: 80, y: 250, width: 400, height: 80,
                fill: '#3D2E10',
                stroke: { color: '#FFAC33', width: 1 },
                cornerRadius: 8,
                text: 'MED: Design token migration complexity\nMitigation: Phased rollout approach',
                fontSize: 13, fontWeight: 400, fontFamily: 'Inter',
                color: '#FFD699',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_133',
                type: 'shape',
                name: 'Risk 3',
                shapeType: 'rounded_rect',
                x: 80, y: 350, width: 400, height: 80,
                fill: '#0D3D1A',
                stroke: { color: '#0ACF83', width: 1 },
                cornerRadius: 8,
                text: 'LOW: Third-party API deprecation\nMitigation: Abstraction layer ready',
                fontSize: 13, fontWeight: 400, fontFamily: 'Inter',
                color: '#80E6B4',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_015',
        order: 14,
        title: 'Next Steps',
        layout: 'layout_title_content',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: null,
        groupName: null,
        background: { type: 'solid', color: '#1E1E1E' },
        presenterNotes: 'Action items - make sure each owner acknowledges their items.\n\nFollow up on Slack in #q4-planning channel.',
        transition: { type: 'dissolve', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
        slideNumberEnabled: true,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_140',
                type: 'text',
                name: 'Title',
                x: 80, y: 60, width: 600, height: 60,
                text: 'Next Steps & Action Items',
                fontSize: 36, fontWeight: 700, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            },
            {
                id: 'obj_141',
                type: 'text',
                name: 'Action Items',
                x: 80, y: 150, width: 800, height: 280,
                text: 'Immediate (This Week):\n  Finalize Q4 sprint planning - Sarah\n  Complete mobile team hiring plan - Elena\n  Set up Design System beta environment - Aiko\n\nShort Term (2 Weeks):\n  Review API documentation draft - Marcus\n  Security audit for new auth flow - David\n  User research for mobile MVP - Priya\n\nOngoing:\n  Weekly sync: Tuesdays 10am PT\n  Bi-weekly demos: Every other Friday\n  Monthly stakeholder update: Last Wednesday',
                fontSize: 15, fontWeight: 400, fontFamily: 'Inter',
                color: '#E0E0E0',
                textAlign: 'left',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    },
    {
        id: 'slide_016',
        order: 15,
        title: 'Thank You',
        layout: 'layout_closing',
        templateStyle: 'ts_001',
        skipped: false,
        groupId: null,
        groupName: null,
        background: { type: 'gradient', gradient: { type: 'linear', angle: 180, stops: [{ color: '#7B61FF', position: 0 }, { color: '#1E1E1E', position: 100 }] } },
        presenterNotes: 'Open the floor for questions. Keep it under 10 minutes if possible.',
        transition: { type: 'dissolve', direction: null, easing: 'ease_out', duration: 600, timing: 'immediately' },
        slideNumberEnabled: false,
        slideNumberCount: 'all',
        slideNumberFormat: 'number_only',
        slideNumberIncludeTotal: false,
        objects: [
            {
                id: 'obj_150',
                type: 'text',
                name: 'Closing Title',
                x: 200, y: 180, width: 600, height: 100,
                text: 'Thank You!',
                fontSize: 56, fontWeight: 800, fontFamily: 'Inter',
                color: '#FFFFFF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'scale', duration: 500, timing: 'on_click', direction: 'in', order: 0 }
            },
            {
                id: 'obj_151',
                type: 'text',
                name: 'Contact Info',
                x: 300, y: 310, width: 400, height: 80,
                text: 'Questions? Reach out on #q4-planning\nsarah.chen@designcraft.io',
                fontSize: 16, fontWeight: 400, fontFamily: 'Inter',
                color: '#D4C4FF',
                textAlign: 'center',
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: { style: 'fade', duration: 400, timing: 'after_previous', direction: 'in', order: 1 }
            },
            {
                id: 'obj_152',
                type: 'liveInteraction',
                interactionType: 'stamps',
                name: 'Reaction Stamps',
                x: 340, y: 410, width: 320, height: 80,
                stampTypes: ['thumbsUp', 'heart', 'fire', 'clap', 'rocket'],
                stamps: [
                    { userId: 'user_003', type: 'rocket' },
                    { userId: 'user_006', type: 'thumbsUp' },
                    { userId: 'user_002', type: 'fire' },
                    { userId: 'user_008', type: 'heart' }
                ],
                opacity: 100, rotation: 0, locked: false, visible: true,
                animation: null
            }
        ]
    }
];

const DECK_SETTINGS = {
    id: 'deck_001',
    name: 'Q4 2025 Product Strategy',
    createdAt: '2025-09-28T14:30:00Z',
    updatedAt: '2025-10-14T09:15:22Z',
    createdBy: 'user_001',
    width: 1200,
    height: 675,
    aspectRatio: '16:9',
    defaultTemplateStyle: 'ts_001',
    slideNumbersEnabled: true,
    slideNumberCount: 'all',
    slideNumberFormat: 'number_only',
    slideNumberIncludeTotal: false,
    slideNumberPosition: { x: 1120, y: 640 },
    defaultTransition: { type: 'dissolve', direction: null, easing: 'ease', duration: 400, timing: 'immediately' },
    presentationMode: 'present',
    availableOffline: false,
    location: 'team',
    projectName: 'Q4 Planning',
    teamName: 'DesignCraft',
    shareSettings: {
        linkAccess: 'team',
        linkRole: 'can_view',
        allowCopy: true,
        allowDownload: true
    }
};

const COMMENTS = [
    {
        id: 'comment_001',
        slideId: 'slide_003',
        userId: 'user_002',
        userName: 'Marcus Rivera',
        avatarColor: '#F24E1E',
        text: 'The uptime number seems low. Should we address this?',
        createdAt: '2025-10-12T15:30:00Z',
        resolved: false,
        replies: [
            {
                id: 'reply_001',
                userId: 'user_001',
                userName: 'Sarah Chen',
                avatarColor: '#7B61FF',
                text: 'Good catch - the 98.2% was due to the August incident. We\'re back to 99.5% now. I\'ll update.',
                createdAt: '2025-10-12T15:45:00Z'
            }
        ],
        position: { x: 780, y: 200 }
    },
    {
        id: 'comment_002',
        slideId: 'slide_007',
        userId: 'user_003',
        userName: 'Aiko Tanaka',
        avatarColor: '#0ACF83',
        text: 'I think we should add more detail about the token architecture. Can we add a technical deep-dive slide?',
        createdAt: '2025-10-13T09:20:00Z',
        resolved: false,
        replies: [],
        position: { x: 600, y: 180 }
    },
    {
        id: 'comment_003',
        slideId: 'slide_004',
        userId: 'user_005',
        userName: 'Priya Sharma',
        avatarColor: '#FF7262',
        text: 'Enterprise growth numbers are impressive! Should we break this down by region?',
        createdAt: '2025-10-11T11:00:00Z',
        resolved: true,
        replies: [
            {
                id: 'reply_002',
                userId: 'user_001',
                userName: 'Sarah Chen',
                avatarColor: '#7B61FF',
                text: 'Added a regional breakdown in the appendix. Thanks!',
                createdAt: '2025-10-11T14:30:00Z'
            }
        ],
        position: { x: 500, y: 250 }
    },
    {
        id: 'comment_004',
        slideId: 'slide_013',
        userId: 'user_004',
        userName: 'James O\'Brien',
        avatarColor: '#1ABCFE',
        text: 'This competitive comparison might be outdated. Competitor A launched AI features last week.',
        createdAt: '2025-10-14T08:00:00Z',
        resolved: false,
        replies: [],
        position: { x: 400, y: 300 }
    },
    {
        id: 'comment_005',
        slideId: 'slide_011',
        userId: 'user_007',
        userName: 'Elena Kowalski',
        avatarColor: '#FF6B6B',
        text: 'Mobile team status should be "Hiring" not "Planning". We\'ve already started architecture work.',
        createdAt: '2025-10-13T16:45:00Z',
        resolved: false,
        replies: [
            {
                id: 'reply_003',
                userId: 'user_001',
                userName: 'Sarah Chen',
                avatarColor: '#7B61FF',
                text: 'Updated! Thanks Elena.',
                createdAt: '2025-10-13T17:00:00Z'
            },
            {
                id: 'reply_004',
                userId: 'user_007',
                userName: 'Elena Kowalski',
                avatarColor: '#FF6B6B',
                text: 'Perfect, looks good now.',
                createdAt: '2025-10-13T17:05:00Z'
            }
        ],
        position: { x: 700, y: 280 }
    },
    {
        id: 'comment_006',
        slideId: 'slide_001',
        userId: 'user_008',
        userName: 'David Park',
        avatarColor: '#4ECDC4',
        text: 'Love the new slide design! Clean and professional.',
        createdAt: '2025-10-10T10:00:00Z',
        resolved: true,
        replies: [],
        position: { x: 300, y: 150 }
    }
];

const LIBRARIES = [
    {
        id: 'lib_001',
        name: 'DesignCraft Component Library',
        description: 'Core UI components for all DesignCraft products',
        addedAt: '2025-09-28T14:35:00Z',
        lastUpdated: '2025-10-10T12:00:00Z',
        hasUpdates: true,
        componentCount: 142,
        styleCount: 38,
        variableCount: 24,
        enabled: true
    },
    {
        id: 'lib_002',
        name: 'Brand Assets 2025',
        description: 'Logos, icons, and brand color palette',
        addedAt: '2025-09-29T09:00:00Z',
        lastUpdated: '2025-10-05T16:30:00Z',
        hasUpdates: false,
        componentCount: 56,
        styleCount: 12,
        variableCount: 8,
        enabled: true
    },
    {
        id: 'lib_003',
        name: 'Presentation Icons Pack',
        description: 'Icon set optimized for slide presentations',
        addedAt: '2025-10-01T11:20:00Z',
        lastUpdated: '2025-09-20T08:00:00Z',
        hasUpdates: false,
        componentCount: 320,
        styleCount: 0,
        variableCount: 0,
        enabled: true
    }
];

const VERSION_HISTORY = [
    { id: 'ver_001', name: 'Initial draft', createdAt: '2025-09-28T14:30:00Z', createdBy: 'user_001', slideCount: 8 },
    { id: 'ver_002', name: 'Added metrics slides', createdAt: '2025-10-02T16:45:00Z', createdBy: 'user_001', slideCount: 10 },
    { id: 'ver_003', name: 'Team review feedback', createdAt: '2025-10-08T11:30:00Z', createdBy: 'user_003', slideCount: 13 },
    { id: 'ver_004', name: 'Added competitive analysis', createdAt: '2025-10-10T14:00:00Z', createdBy: 'user_001', slideCount: 15 },
    { id: 'ver_005', name: 'Final review edits', createdAt: '2025-10-14T09:15:00Z', createdBy: 'user_001', slideCount: 16 }
];

const AVAILABLE_TEMPLATES = [
    { id: 'tmpl_001', name: 'Minimal Dark', category: 'Business', author: 'Figma', thumbnailColor: '#1E1E1E', slideCount: 24, published: true },
    { id: 'tmpl_002', name: 'Corporate Blue', category: 'Business', author: 'Figma', thumbnailColor: '#0052CC', slideCount: 20, published: true },
    { id: 'tmpl_003', name: 'Warm Sunset', category: 'Creative', author: 'Figma', thumbnailColor: '#FF6B35', slideCount: 18, published: true },
    { id: 'tmpl_004', name: 'Pitch Deck Pro', category: 'Startup', author: 'Community', thumbnailColor: '#6C5CE7', slideCount: 16, published: true },
    { id: 'tmpl_005', name: 'Tech Conference', category: 'Conference', author: 'Community', thumbnailColor: '#00B894', slideCount: 22, published: true },
    { id: 'tmpl_006', name: 'Annual Report', category: 'Business', author: 'DesignCraft Team', thumbnailColor: '#2D3436', slideCount: 30, published: true },
    { id: 'tmpl_007', name: 'Product Launch', category: 'Marketing', author: 'DesignCraft Team', thumbnailColor: '#E17055', slideCount: 14, published: true },
    { id: 'tmpl_008', name: 'Education Series', category: 'Education', author: 'Community', thumbnailColor: '#74B9FF', slideCount: 20, published: true },
    { id: 'tmpl_009', name: 'Portfolio Showcase', category: 'Creative', author: 'Community', thumbnailColor: '#FD79A8', slideCount: 12, published: true },
    { id: 'tmpl_010', name: 'Sprint Review', category: 'Agile', author: 'DesignCraft Team', thumbnailColor: '#636E72', slideCount: 10, published: false },
    { id: 'tmpl_011', name: 'Investor Update', category: 'Startup', author: 'Community', thumbnailColor: '#0984E3', slideCount: 15, published: true },
    { id: 'tmpl_012', name: 'Workshop Materials', category: 'Education', author: 'Community', thumbnailColor: '#FDCB6E', slideCount: 25, published: true }
];

const EXPORT_HISTORY = [
    { id: 'exp_001', format: 'pdf', fileName: 'Q4-Strategy-Draft-v1.pdf', exportedAt: '2025-10-08T15:00:00Z', exportedBy: 'user_001', fileSize: '4.2 MB', colorProfile: 'srgb', quality: 'high', slidesIncluded: 'all' },
    { id: 'exp_002', format: 'pptx', fileName: 'Q4-Strategy-for-Stakeholders.pptx', exportedAt: '2025-10-10T10:30:00Z', exportedBy: 'user_001', fileSize: '8.7 MB', slidesIncluded: 'all' },
    { id: 'exp_003', format: 'pdf', fileName: 'Q4-Strategy-Metrics-Only.pdf', exportedAt: '2025-10-12T14:00:00Z', exportedBy: 'user_002', fileSize: '1.8 MB', colorProfile: 'display_p3', quality: 'best', slidesIncluded: 'selected' }
];
