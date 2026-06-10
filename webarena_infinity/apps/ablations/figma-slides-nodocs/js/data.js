/* ============================================================
   data.js — Seed data for Figma Slides app
   ============================================================ */

const SEED_DATA_VERSION = 1;

// ── Canvas dimensions (16:9) ──
const CANVAS_WIDTH = 960;
const CANVAS_HEIGHT = 540;

// ── Users ──
const USERS = [
    { id: 'user_001', name: 'Sarah Chen', email: 'sarah.chen@designco.io', initials: 'SC', color: '#7B61FF', role: 'owner' },
    { id: 'user_002', name: 'Marcus Rivera', email: 'marcus.r@designco.io', initials: 'MR', color: '#0D99FF', role: 'editor' },
    { id: 'user_003', name: 'Anika Patel', email: 'anika.patel@designco.io', initials: 'AP', color: '#14AE5C', role: 'editor' },
    { id: 'user_004', name: 'James O\'Brien', email: 'james.obrien@designco.io', initials: 'JO', color: '#F24822', role: 'editor' },
    { id: 'user_005', name: 'Yuki Tanaka', email: 'yuki.tanaka@designco.io', initials: 'YT', color: '#FF7262', role: 'viewer' },
    { id: 'user_006', name: 'Priya Sharma-Krishnamurthy', email: 'priya.sk@designco.io', initials: 'PS', color: '#9747FF', role: 'editor' },
    { id: 'user_007', name: 'David Kim', email: 'david.kim@designco.io', initials: 'DK', color: '#FFC700', role: 'viewer' },
    { id: 'user_008', name: 'Elena Voronova', email: 'elena.v@designco.io', initials: 'EV', color: '#FF8577', role: 'editor' }
];

// ── Color themes for presentations ──
const THEMES = {
    corporate: { primary: '#1a1a2e', secondary: '#16213e', accent: '#0f3460', text: '#ffffff', textDark: '#1a1a2e', bg: '#ffffff' },
    creative: { primary: '#7B61FF', secondary: '#9747FF', accent: '#FF7262', text: '#ffffff', textDark: '#2c2c2c', bg: '#faf8ff' },
    minimal: { primary: '#2c2c2c', secondary: '#555555', accent: '#0D99FF', text: '#ffffff', textDark: '#2c2c2c', bg: '#ffffff' },
    nature: { primary: '#1B4332', secondary: '#2D6A4F', accent: '#40916C', text: '#ffffff', textDark: '#1B4332', bg: '#f0faf4' },
    warm: { primary: '#BC4749', secondary: '#F26157', accent: '#FFC700', text: '#ffffff', textDark: '#3D0000', bg: '#fff8f0' },
    ocean: { primary: '#023E8A', secondary: '#0077B6', accent: '#00B4D8', text: '#ffffff', textDark: '#023E8A', bg: '#f0f8ff' },
    dark: { primary: '#0f0f0f', secondary: '#1a1a1a', accent: '#7B61FF', text: '#f0f0f0', textDark: '#f0f0f0', bg: '#1e1e1e' },
    sunset: { primary: '#E63946', secondary: '#F4845F', accent: '#F7B267', text: '#ffffff', textDark: '#2b0a0a', bg: '#fff5f0' }
};

// ── Transition types ──
const TRANSITION_TYPES = ['none', 'fade', 'slide', 'dissolve', 'push'];
const ANIMATION_TYPES = ['none', 'appear', 'fade-in', 'move-in-left', 'move-in-right', 'move-in-up', 'move-in-down', 'scale-in', 'bounce-in'];

// ── Layout types ──
const LAYOUT_TYPES = ['title', 'title-content', 'two-column', 'section-header', 'blank', 'image-focused'];

// ── Font families ──
const FONT_FAMILIES = ['Inter', 'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'Poppins', 'Source Sans Pro', 'Playfair Display', 'Merriweather', 'Fira Code'];

// ── Shape types ──
const SHAPE_TYPES = ['rectangle', 'circle', 'line', 'arrow', 'triangle', 'diamond', 'star', 'polygon'];

// ── Element ID counter ──
let _elemCounter = 1;
function nextElemId() { return 'elem_' + String(_elemCounter++).padStart(5, '0'); }

// ── Slide builder helpers ──
function makeTextElement(overrides) {
    return Object.assign({
        id: nextElemId(), type: 'text', x: 80, y: 60, width: 800, height: 60,
        rotation: 0, opacity: 1, locked: false,
        content: '', shapeType: null, fill: null, stroke: null, strokeWidth: 0, cornerRadius: 0,
        imageUrl: null, imagePlaceholder: null,
        style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' },
        animation: { type: 'none', duration: 300, delay: 0, order: 0 }
    }, overrides);
}

function makeShapeElement(overrides) {
    return Object.assign({
        id: nextElemId(), type: 'shape', x: 100, y: 100, width: 200, height: 200,
        rotation: 0, opacity: 1, locked: false,
        content: null, shapeType: 'rectangle', fill: '#4A90D9', stroke: '#333333', strokeWidth: 2, cornerRadius: 0,
        imageUrl: null, imagePlaceholder: null,
        style: null,
        animation: { type: 'none', duration: 300, delay: 0, order: 0 }
    }, overrides);
}

function makeImageElement(overrides) {
    return Object.assign({
        id: nextElemId(), type: 'image', x: 100, y: 100, width: 400, height: 300,
        rotation: 0, opacity: 1, locked: false,
        content: null, shapeType: null, fill: null, stroke: null, strokeWidth: 0, cornerRadius: 0,
        imageUrl: null, imagePlaceholder: '#e0e0e0',
        style: null,
        animation: { type: 'none', duration: 300, delay: 0, order: 0 }
    }, overrides);
}

function makeSlide(id, presId, order, layout, bgColor, transition, notes, elements) {
    return {
        id: id,
        presentationId: presId,
        order: order,
        layout: layout,
        backgroundColor: bgColor || '#ffffff',
        transition: transition || { type: 'none', duration: 500 },
        speakerNotes: notes || '',
        elements: elements || []
    };
}

// ============================================================
// PRESENTATION 1: Q1 2026 Product Roadmap (15 slides)
// ============================================================
const PRES_001_SLIDES = [
    makeSlide('slide_001_00', 'pres_001', 0, 'title', '#1a1a2e', { type: 'fade', duration: 500 },
        'Welcome everyone. Today we will review our Q1 progress and plan ahead for Q2.',
        [
            makeTextElement({ x: 80, y: 140, width: 800, height: 80, content: 'Q1 2026 Product Roadmap', style: { fontFamily: 'Inter', fontSize: 48, fontWeight: 'bold', color: '#ffffff', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -1, listType: 'none' }, animation: { type: 'fade-in', duration: 500, delay: 0, order: 1 } }),
            makeTextElement({ x: 180, y: 250, width: 600, height: 40, content: 'DesignCo Product Team — March 2026', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#a0a0cc', textAlign: 'center', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' }, animation: { type: 'fade-in', duration: 500, delay: 200, order: 2 } }),
            makeShapeElement({ x: 380, y: 330, width: 200, height: 4, shapeType: 'line', fill: '#7B61FF', stroke: '#7B61FF', strokeWidth: 2 })
        ]),
    makeSlide('slide_001_01', 'pres_001', 1, 'section-header', '#ffffff', { type: 'slide', duration: 400 },
        'Brief overview of what we shipped this quarter.',
        [
            makeTextElement({ x: 60, y: 80, width: 840, height: 60, content: 'What We Shipped in Q1', style: { fontFamily: 'Inter', fontSize: 40, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -0.5, listType: 'none' } }),
            makeShapeElement({ x: 60, y: 150, width: 100, height: 4, shapeType: 'line', fill: '#7B61FF', stroke: '#7B61FF', strokeWidth: 2 })
        ]),
    makeSlide('slide_001_02', 'pres_001', 2, 'title-content', '#ffffff', { type: 'fade', duration: 400 },
        'Highlight the three major launches and their impact metrics.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Major Launches', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 840, height: 200, content: 'Real-time collaboration engine v2.0\nAdvanced prototyping with conditional logic\nFigma-to-code export plugin (beta)\nPerformance overhaul: 40% faster canvas rendering\nNew component library with 200+ primitives', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.6, letterSpacing: 0, listType: 'bullet' } }),
            makeShapeElement({ x: 60, y: 380, width: 840, height: 100, shapeType: 'rectangle', fill: '#f0edff', stroke: 'none', strokeWidth: 0, cornerRadius: 8 }),
            makeTextElement({ x: 80, y: 395, width: 800, height: 60, content: 'Impact: 2.3M monthly active users (+18% QoQ), NPS score 72 (+5 pts)', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: '600', color: '#7B61FF', textAlign: 'left', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' } })
        ]),
    makeSlide('slide_001_03', 'pres_001', 3, 'two-column', '#ffffff', { type: 'dissolve', duration: 500 },
        'Show DAU and revenue side by side. Emphasize the growth trend.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Key Metrics Overview', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 60, y: 110, width: 400, height: 280, shapeType: 'rectangle', fill: '#f8f8ff', stroke: '#e0e0e0', strokeWidth: 1, cornerRadius: 12 }),
            makeTextElement({ x: 80, y: 125, width: 360, height: 30, content: 'Daily Active Users', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: '600', color: '#666666', textAlign: 'left', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 80, y: 160, width: 360, height: 50, content: '847,293', style: { fontFamily: 'Inter', fontSize: 42, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.1, letterSpacing: -1, listType: 'none' } }),
            makeTextElement({ x: 80, y: 220, width: 360, height: 30, content: '+23.4% vs Q4 2025', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#14AE5C', textAlign: 'left', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 500, y: 110, width: 400, height: 280, shapeType: 'rectangle', fill: '#f8f8ff', stroke: '#e0e0e0', strokeWidth: 1, cornerRadius: 12 }),
            makeTextElement({ x: 520, y: 125, width: 360, height: 30, content: 'Monthly Recurring Revenue', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: '600', color: '#666666', textAlign: 'left', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 520, y: 160, width: 360, height: 50, content: '$4.2M', style: { fontFamily: 'Inter', fontSize: 42, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.1, letterSpacing: -1, listType: 'none' } }),
            makeTextElement({ x: 520, y: 220, width: 360, height: 30, content: '+31.2% vs Q4 2025', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#14AE5C', textAlign: 'left', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } })
        ]),
    makeSlide('slide_001_04', 'pres_001', 4, 'title-content', '#ffffff', { type: 'fade', duration: 400 },
        'Walk through the collaboration engine improvements. Demo available if time permits.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Collaboration Engine v2.0', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 840, height: 250, content: 'Conflict-free replicated data types (CRDTs) for real-time sync\nUp to 50 simultaneous editors per file (was 15)\nLatency reduced from 120ms to 35ms average\nOffline editing with automatic merge on reconnect\nGranular undo/redo per collaborator', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }),
            makeShapeElement({ x: 700, y: 380, width: 200, height: 120, shapeType: 'rectangle', fill: '#7B61FF', stroke: 'none', strokeWidth: 0, cornerRadius: 8, opacity: 0.15 })
        ]),
    makeSlide('slide_001_05', 'pres_001', 5, 'title-content', '#ffffff', { type: 'slide', duration: 400 },
        'This is where things get exciting. Conditional logic in prototyping opens up new use cases.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Advanced Prototyping', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 500, height: 250, content: 'Conditional logic: if/else branching\nVariable support for dynamic content\nMath expressions in prototypes\nState management across frames\nAdvanced micro-interactions library', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }),
            makeImageElement({ x: 580, y: 120, width: 340, height: 240, imagePlaceholder: '#e8e0ff' })
        ]),
    makeSlide('slide_001_06', 'pres_001', 6, 'title-content', '#ffffff', { type: 'fade', duration: 400 },
        'Beta results have been very positive. Mention the waitlist numbers.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Figma-to-Code Export (Beta)', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 840, height: 200, content: 'React, Vue, and Swift code generation\n94% accuracy on component mapping\n12,400 beta users, 4.6/5 satisfaction\nCode quality comparable to hand-written output\nIntegration with VS Code and JetBrains IDEs', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }),
            makeShapeElement({ x: 60, y: 350, width: 840, height: 2, shapeType: 'line', fill: '#e0e0e0', stroke: '#e0e0e0', strokeWidth: 1 }),
            makeTextElement({ x: 60, y: 370, width: 840, height: 40, content: 'Target GA: April 15, 2026 — Waitlist: 34,200 teams', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: '600', color: '#7B61FF', textAlign: 'left', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' } })
        ]),
    makeSlide('slide_001_07', 'pres_001', 7, 'section-header', '#1a1a2e', { type: 'dissolve', duration: 600 },
        'Transition to Q2 planning. Keep energy high.',
        [
            makeTextElement({ x: 60, y: 160, width: 840, height: 70, content: 'Q2 2026 Roadmap', style: { fontFamily: 'Inter', fontSize: 44, fontWeight: 'bold', color: '#ffffff', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -0.5, listType: 'none' } }),
            makeTextElement({ x: 60, y: 250, width: 600, height: 40, content: 'Where we\'re heading next', style: { fontFamily: 'Inter', fontSize: 22, fontWeight: 'normal', color: '#a0a0cc', textAlign: 'left', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 60, y: 310, width: 100, height: 4, shapeType: 'line', fill: '#7B61FF', stroke: '#7B61FF', strokeWidth: 2 })
        ]),
    makeSlide('slide_001_08', 'pres_001', 8, 'title-content', '#ffffff', { type: 'fade', duration: 400 },
        'Three major initiatives. Each has its own deep-dive slide.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Q2 Priority Initiatives', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 60, y: 110, width: 260, height: 300, shapeType: 'rectangle', fill: '#f0edff', stroke: '#d4ccff', strokeWidth: 1, cornerRadius: 12 }),
            makeTextElement({ x: 80, y: 130, width: 220, height: 30, content: 'AI Design Assistant', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'bold', color: '#7B61FF', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 80, y: 170, width: 220, height: 200, content: 'Auto-layout suggestions\nContent generation\nStyle transfer\nAccessibility fixes', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: 'normal', color: '#555555', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }),
            makeShapeElement({ x: 350, y: 110, width: 260, height: 300, shapeType: 'rectangle', fill: '#e8f7ee', stroke: '#b8e6c8', strokeWidth: 1, cornerRadius: 12 }),
            makeTextElement({ x: 370, y: 130, width: 220, height: 30, content: 'Design Systems 2.0', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'bold', color: '#14AE5C', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 370, y: 170, width: 220, height: 200, content: 'Multi-brand theming\nToken management\nVersion control\nUsage analytics', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: 'normal', color: '#555555', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }),
            makeShapeElement({ x: 640, y: 110, width: 260, height: 300, shapeType: 'rectangle', fill: '#fff0e6', stroke: '#ffd4b8', strokeWidth: 1, cornerRadius: 12 }),
            makeTextElement({ x: 660, y: 130, width: 220, height: 30, content: 'Enterprise Platform', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'bold', color: '#F24822', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 660, y: 170, width: 220, height: 200, content: 'SSO & SCIM\nAudit logging\nAdvanced permissions\nData residency', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: 'normal', color: '#555555', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } })
        ]),
    makeSlide('slide_001_09', 'pres_001', 9, 'title-content', '#ffffff', { type: 'slide', duration: 400 },
        'AI Assistant is the biggest bet. Emphasize responsible AI approach.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Deep Dive: AI Design Assistant', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 840, height: 300, content: 'Layout Intelligence: Suggest optimal arrangements based on content type and hierarchy\nContent Generation: Create placeholder text, icons, and images contextually\nStyle Transfer: Apply design patterns from one component to another\nAccessibility Checker: Real-time WCAG compliance suggestions with one-click fixes\nDesign Critique: AI-powered feedback on visual hierarchy, spacing, and consistency\nTimeline: Alpha in April, Beta in June, GA in August', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 2.0, letterSpacing: 0, listType: 'numbered' } })
        ]),
    makeSlide('slide_001_10', 'pres_001', 10, 'two-column', '#ffffff', { type: 'fade', duration: 400 },
        'Show timeline on one side, team allocation on the other.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Q2 Timeline & Resources', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 420, height: 30, content: 'Timeline', style: { fontFamily: 'Inter', fontSize: 22, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 150, width: 420, height: 250, content: 'April: AI Assistant alpha, Enterprise SSO\nMay: Design Systems 2.0 beta, Code export GA\nJune: AI Assistant beta, Token management\nJuly: Enterprise audit logging, Usage analytics\nAugust: AI Assistant GA, Multi-brand theming', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 2.0, letterSpacing: 0, listType: 'bullet' } }),
            makeTextElement({ x: 520, y: 110, width: 380, height: 30, content: 'Team Allocation', style: { fontFamily: 'Inter', fontSize: 22, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 520, y: 150, width: 380, height: 250, content: 'AI Team: 8 engineers, 2 designers\nPlatform: 12 engineers, 3 designers\nEnterprise: 6 engineers, 1 designer\nDesign Systems: 5 engineers, 4 designers\nInfra/DevOps: 4 engineers', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 2.0, letterSpacing: 0, listType: 'bullet' } })
        ]),
    makeSlide('slide_001_11', 'pres_001', 11, 'title-content', '#ffffff', { type: 'fade', duration: 400 },
        'Acknowledge the challenges openly. Show we have mitigation plans.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Risks & Mitigations', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 840, height: 300, content: 'AI model latency at scale — Mitigation: Edge deployment + caching layer\nEnterprise security certifications — Mitigation: SOC2 audit in progress, target June\nDesign systems migration complexity — Mitigation: Phased rollout, backwards compatibility\nCompetitive pressure from Canva AI — Mitigation: Focus on professional/enterprise segment\nEngineering hiring timeline — Mitigation: Contractor bridge, internal mobility program', style: { fontFamily: 'Inter', fontSize: 17, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 2.0, letterSpacing: 0, listType: 'bullet' } })
        ]),
    makeSlide('slide_001_12', 'pres_001', 12, 'title-content', '#ffffff', { type: 'dissolve', duration: 400 },
        'Three clear success metrics. Keep it simple.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Success Metrics for Q2', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 60, y: 120, width: 270, height: 180, shapeType: 'rectangle', fill: '#f0edff', stroke: 'none', strokeWidth: 0, cornerRadius: 12 }),
            makeTextElement({ x: 80, y: 140, width: 230, height: 30, content: 'DAU Target', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#666666', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 80, y: 175, width: 230, height: 50, content: '1.1M', style: { fontFamily: 'Inter', fontSize: 42, fontWeight: 'bold', color: '#7B61FF', textAlign: 'center', italic: false, underline: false, lineHeight: 1.1, letterSpacing: -1, listType: 'none' } }),
            makeTextElement({ x: 80, y: 230, width: 230, height: 30, content: '+30% growth target', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: 'normal', color: '#888888', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 345, y: 120, width: 270, height: 180, shapeType: 'rectangle', fill: '#e8f7ee', stroke: 'none', strokeWidth: 0, cornerRadius: 12 }),
            makeTextElement({ x: 365, y: 140, width: 230, height: 30, content: 'MRR Target', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#666666', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 365, y: 175, width: 230, height: 50, content: '$5.8M', style: { fontFamily: 'Inter', fontSize: 42, fontWeight: 'bold', color: '#14AE5C', textAlign: 'center', italic: false, underline: false, lineHeight: 1.1, letterSpacing: -1, listType: 'none' } }),
            makeTextElement({ x: 365, y: 230, width: 230, height: 30, content: '+38% revenue growth', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: 'normal', color: '#888888', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 630, y: 120, width: 270, height: 180, shapeType: 'rectangle', fill: '#fff0e6', stroke: 'none', strokeWidth: 0, cornerRadius: 12 }),
            makeTextElement({ x: 650, y: 140, width: 230, height: 30, content: 'Enterprise Deals', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#666666', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 650, y: 175, width: 230, height: 50, content: '45', style: { fontFamily: 'Inter', fontSize: 42, fontWeight: 'bold', color: '#F24822', textAlign: 'center', italic: false, underline: false, lineHeight: 1.1, letterSpacing: -1, listType: 'none' } }),
            makeTextElement({ x: 650, y: 230, width: 230, height: 30, content: 'signed this quarter', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: 'normal', color: '#888888', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } })
        ]),
    makeSlide('slide_001_13', 'pres_001', 13, 'title-content', '#ffffff', { type: 'fade', duration: 400 },
        'Quick summary before opening for questions.',
        [
            makeTextElement({ x: 60, y: 40, width: 840, height: 50, content: 'Key Takeaways', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } }),
            makeTextElement({ x: 60, y: 110, width: 840, height: 250, content: 'Q1 exceeded targets across all key metrics\nAI Design Assistant is our biggest bet for Q2\nEnterprise expansion is accelerating\nDesign Systems 2.0 unlocks new pricing tiers\nTeam is well-resourced but hiring remains a priority', style: { fontFamily: 'Inter', fontSize: 22, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 2.0, letterSpacing: 0, listType: 'numbered' } })
        ]),
    makeSlide('slide_001_14', 'pres_001', 14, 'title', '#1a1a2e', { type: 'fade', duration: 600 },
        'End on a strong note. Open for questions.',
        [
            makeTextElement({ x: 80, y: 160, width: 800, height: 70, content: 'Questions & Discussion', style: { fontFamily: 'Inter', fontSize: 48, fontWeight: 'bold', color: '#ffffff', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -1, listType: 'none' } }),
            makeTextElement({ x: 180, y: 260, width: 600, height: 40, content: 'sarah.chen@designco.io · #product-roadmap', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: '#a0a0cc', textAlign: 'center', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' } }),
            makeShapeElement({ x: 430, y: 330, width: 100, height: 4, shapeType: 'line', fill: '#7B61FF', stroke: '#7B61FF', strokeWidth: 2 })
        ])
];

// ============================================================
// PRESENTATION 2: Brand Identity Guidelines v2.0 (18 slides)
// ============================================================
function generateBrandSlides() {
    const pid = 'pres_002';
    const titles = [
        'Brand Identity Guidelines v2.0', 'Introduction & Purpose', 'Brand Mission & Vision', 'Logo Usage',
        'Logo Clear Space & Minimum Size', 'Color Palette — Primary', 'Color Palette — Secondary & Neutral',
        'Typography System', 'Type Scale & Hierarchy', 'Iconography Style', 'Photography Guidelines',
        'Illustration Style', 'Layout Principles', 'Grid System', 'Component Patterns', 'Tone of Voice',
        'Social Media Templates', 'Contact & Resources'
    ];
    return titles.map((title, i) => {
        const isFirst = i === 0;
        const isLast = i === titles.length - 1;
        const isSectionBreak = [0, 3, 5, 7, 9, 12, 15].includes(i);
        const bg = isSectionBreak ? '#7B61FF' : '#ffffff';
        const textColor = isSectionBreak ? '#ffffff' : '#2c2c2c';
        const layout = isFirst || isLast ? 'title' : isSectionBreak ? 'section-header' : 'title-content';
        const elements = [
            makeTextElement({ x: 60, y: isSectionBreak ? 180 : 40, width: 840, height: 60, content: title, style: { fontFamily: 'Montserrat', fontSize: isSectionBreak ? 42 : 32, fontWeight: 'bold', color: textColor, textAlign: isSectionBreak ? 'center' : 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -0.5, listType: 'none' } })
        ];
        if (!isSectionBreak) {
            elements.push(makeTextElement({ x: 60, y: 120, width: 840, height: 300, content: getBrandContent(i), style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: '#555555', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: i % 3 === 0 ? 'bullet' : 'none' } }));
        }
        if (i >= 5 && i <= 6) {
            elements.push(makeShapeElement({ x: 60, y: 350, width: 120, height: 80, shapeType: 'rectangle', fill: '#7B61FF', stroke: 'none', strokeWidth: 0, cornerRadius: 8 }));
            elements.push(makeShapeElement({ x: 200, y: 350, width: 120, height: 80, shapeType: 'rectangle', fill: '#0D99FF', stroke: 'none', strokeWidth: 0, cornerRadius: 8 }));
            elements.push(makeShapeElement({ x: 340, y: 350, width: 120, height: 80, shapeType: 'rectangle', fill: '#14AE5C', stroke: 'none', strokeWidth: 0, cornerRadius: 8 }));
            elements.push(makeShapeElement({ x: 480, y: 350, width: 120, height: 80, shapeType: 'rectangle', fill: '#F24822', stroke: 'none', strokeWidth: 0, cornerRadius: 8 }));
            elements.push(makeShapeElement({ x: 620, y: 350, width: 120, height: 80, shapeType: 'rectangle', fill: '#FFC700', stroke: 'none', strokeWidth: 0, cornerRadius: 8 }));
        }
        return makeSlide(`slide_002_${String(i).padStart(2,'0')}`, pid, i, layout, bg,
            { type: i % 2 === 0 ? 'fade' : 'dissolve', duration: 400 + (i % 3) * 100 },
            getBrandNotes(i), elements);
    });
}

function getBrandContent(i) {
    const contents = {
        1: 'This document defines the visual and verbal identity of DesignCo. It provides comprehensive guidelines for maintaining brand consistency across all touchpoints, from digital products to print materials and communications.',
        2: 'Mission: Empower every team to design collaboratively at the speed of thought.\nVision: A world where great design is accessible to everyone, not just designers.\nValues: Craft, Collaboration, Courage, Curiosity.',
        4: 'Minimum clear space: 2x the height of the logomark\nMinimum size: 24px height for digital, 10mm for print\nNever distort, rotate, or add effects to the logo\nAlways use approved logo files from the brand portal',
        6: 'Secondary palette supports the primary colors for backgrounds, borders, and subtle accents.\nNeutrals: Gray-50 (#F9FAFB) through Gray-900 (#111827)\nAlways maintain WCAG AA contrast ratios (4.5:1 for body text, 3:1 for large text)',
        8: 'Display: Montserrat Bold — Headlines and hero text\nBody: Inter Regular/Medium — All body copy and UI text\nMono: Fira Code — Code blocks and technical content\nBase size: 16px, Scale ratio: 1.250 (Major Third)',
        10: 'Photography should feel authentic, warm, and inclusive.\nPrefer candid moments over staged shots.\nColor treatment: Slight warm tone (+5 warmth, -10 contrast)\nNever use stock photos with watermarks or obviously staged compositions.',
        11: 'Illustrations use a flat, geometric style with rounded edges.\nColor palette limited to brand primary and secondary colors.\nLine weight: 2px consistent across all illustrations.\nCharacters follow our inclusive representation guidelines.',
        13: 'Base grid: 8px unit grid for spacing and sizing\n12-column layout for web (max-width: 1200px)\n4-column layout for mobile (max-width: 375px)\nGutter: 24px desktop, 16px mobile',
        14: 'Buttons, inputs, cards, and modals follow consistent patterns.\nBorder radius: 8px for cards, 6px for buttons, 4px for inputs.\nShadow levels: sm (subtle), md (standard), lg (prominent), xl (dramatic).',
        16: 'Avatar templates for profile images (circle, square, rounded)\nStory templates with brand overlay\nPost templates: Quote, Product, Team, Event\nStory highlight covers using brand iconography'
    };
    return contents[i] || 'Detailed guidelines and specifications for this section are available in the complete brand book. Refer to the Figma component library for implementation-ready assets.';
}

function getBrandNotes(i) {
    const notes = {
        0: 'This is the updated v2.0 brand guidelines. Major changes from v1: new secondary palette, updated typography scale, new illustration style.',
        3: 'Emphasize that the logo should never be used below minimum size. Common mistake.',
        5: 'Walk through each color swatch. Mention the accessibility requirements.',
        7: 'Note: We switched from Helvetica to Inter last quarter. Some legacy materials still use the old font.',
        12: 'Layout principles are the most commonly violated guidelines. Stress the importance of whitespace.',
        17: 'All resources are available on the internal wiki and Figma community page.'
    };
    return notes[i] || '';
}

const PRES_002_SLIDES = generateBrandSlides();

// ============================================================
// PRESENTATION 3: Series B Fundraising Pitch (12 slides)
// ============================================================
function generatePitchSlides() {
    const pid = 'pres_003';
    const slides = [
        { title: 'DesignCo', subtitle: 'Series B Fundraising Deck — Confidential', layout: 'title', bg: '#0f0f0f', notes: 'Do NOT share this deck externally without CEO approval.' },
        { title: 'The Problem', body: 'Design collaboration remains fragmented across tools\n78% of design teams use 4+ tools in their workflow\nAverage designer spends 3.2 hours/week on tool-switching overhead\nEnterprise design teams lack governance and version control\nBridge between design and development is still manual', layout: 'title-content', bg: '#ffffff', notes: 'Cite the Forrester report for the statistics.' },
        { title: 'Our Solution', body: 'Unified design platform: design, prototype, present, and hand off in one tool\nReal-time collaboration with CRDT-based sync engine\nAI-powered design assistance reducing repetitive tasks by 60%\nEnterprise-grade security, SSO, and audit logging\nNative code export eliminating design-to-dev handoff friction', layout: 'title-content', bg: '#ffffff', notes: '' },
        { title: 'Market Opportunity', body: 'Total Addressable Market: $28.4B (design tools + collaboration)\nServiceable Market: $8.2B (professional design tools)\nCurrent penetration: 3.4% of SAM\nGrowing at 42% CAGR (vs market 18%)', layout: 'title-content', bg: '#ffffff', notes: 'Updated TAM numbers from McKinsey Q4 2025 report.' },
        { title: 'Traction & Growth', body: '2.3M monthly active users (+180% YoY)\n$4.2M MRR ($50.4M ARR run rate)\n847K daily active users\n12,400 enterprise accounts\nNet revenue retention: 142%', layout: 'title-content', bg: '#ffffff', notes: 'These are Q1 2026 actuals. Verified by finance team.' },
        { title: 'Business Model', body: 'Freemium: Free for up to 3 editors\nProfessional: $15/editor/month (billed annually)\nOrganization: $45/editor/month + admin features\nEnterprise: Custom pricing, dedicated support, SLA\nAverage deal size: $32K ARR (enterprise), growing 28% QoQ', layout: 'title-content', bg: '#ffffff', notes: '' },
        { title: 'Competitive Landscape', body: 'vs Canva: We focus on professional design teams, not consumers\nvs Adobe XD: Our collaboration is 10x better, real-time by default\nvs Sketch: We\'re web-native, no Mac dependency\nvs InVision: We combine design + prototyping, no tool-switching\nMoat: Network effects, switching costs, AI training data from 50M+ files', layout: 'title-content', bg: '#ffffff', notes: 'Do not disparage competitors. Focus on our differentiation.' },
        { title: 'Team', body: '127 employees across San Francisco, London, and Tokyo\nFounders: ex-Google Design, ex-Stripe Engineering\n42% of engineering team from FAANG\nDesign advisory board includes John Maeda, Julie Zhuo', layout: 'title-content', bg: '#ffffff', notes: 'Mention the recent VP of Engineering hire from Figma (the real one).' },
        { title: 'Go-to-Market Strategy', body: 'Product-led growth: 85% of revenue from self-serve\nEnterprise sales team: 12 AEs, targeting Fortune 500\nPartner program: Agency and consultancy channel\nCommunity: 450K members, 8,200 community plugins\nContent marketing: 2.1M monthly blog visitors', layout: 'title-content', bg: '#ffffff', notes: '' },
        { title: 'Financial Projections', body: '2026 Revenue: $72M (projected)\n2027 Revenue: $128M (projected)\n2028 Revenue: $210M (projected)\nGross margin: 82% (improving)\nPath to profitability: Q3 2027', layout: 'title-content', bg: '#ffffff', notes: 'Conservative estimates. Upside case is 15-20% higher.' },
        { title: 'The Ask', body: 'Raising $80M Series B at $600M pre-money valuation\nUse of funds:\n- 50% Engineering (AI + Enterprise)\n- 25% Sales & Marketing\n- 15% International expansion\n- 10% Infrastructure & security certifications', layout: 'title-content', bg: '#ffffff', notes: 'The board approved this valuation range. Floor is $550M.' },
        { title: 'Thank You', subtitle: 'sarah.chen@designco.io\ndesignco.io/investors', layout: 'title', bg: '#0f0f0f', notes: 'Follow up with the data room link within 24 hours.' }
    ];
    return slides.map((s, i) => {
        const textColor = s.bg === '#0f0f0f' ? '#ffffff' : '#1a1a2e';
        const subColor = s.bg === '#0f0f0f' ? '#888888' : '#666666';
        const elements = [
            makeTextElement({ x: 60, y: s.layout === 'title' ? 180 : 40, width: 840, height: 60, content: s.title, style: { fontFamily: 'Inter', fontSize: s.layout === 'title' ? 48 : 32, fontWeight: 'bold', color: textColor, textAlign: s.layout === 'title' ? 'center' : 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -0.5, listType: 'none' } })
        ];
        if (s.subtitle) {
            elements.push(makeTextElement({ x: 160, y: 260, width: 640, height: 60, content: s.subtitle, style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: subColor, textAlign: 'center', italic: false, underline: false, lineHeight: 1.6, letterSpacing: 0, listType: 'none' } }));
        }
        if (s.body) {
            elements.push(makeTextElement({ x: 60, y: 120, width: 840, height: 300, content: s.body, style: { fontFamily: 'Inter', fontSize: 19, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.9, letterSpacing: 0, listType: 'bullet' } }));
        }
        return makeSlide(`slide_003_${String(i).padStart(2,'0')}`, pid, i, s.layout, s.bg,
            { type: 'fade', duration: 500 }, s.notes, elements);
    });
}

const PRES_003_SLIDES = generatePitchSlides();

// ============================================================
// PRESENTATION 4: User Research Findings (16 slides)
// ============================================================
function generateResearchSlides() {
    const pid = 'pres_004';
    const slides = [
        { t: 'User Research Findings: Mobile App Redesign', sub: 'Research Phase 2 — February 2026', sec: true },
        { t: 'Research Overview', b: 'Study period: January 8 – February 14, 2026\n24 participants across 4 user segments\nMethods: In-depth interviews (60 min), usability testing (45 min), diary study (2 weeks)\n3 rounds of prototype testing with iterative improvements' },
        { t: 'Participant Demographics', b: 'Ages: 22–58 (median 34)\nGender: 13 women, 9 men, 2 non-binary\nExperience level: 8 beginners, 10 intermediate, 6 advanced\nGeography: US (12), UK (5), Germany (4), Japan (3)\nDevice usage: iOS 58%, Android 42%' },
        { t: 'Key Finding #1: Navigation Confusion', b: 'Task completion rate: 47% for navigation-dependent tasks\nAverage time to find settings: 23 seconds (target: 8 seconds)\n18/24 participants expected bottom navigation\n"I keep getting lost in the hamburger menu" — P07\n"Why is search hidden behind two taps?" — P15' },
        { t: 'Key Finding #2: Onboarding Drop-off', b: '62% of new users abandon onboarding at step 3 (account setup)\nAverage onboarding time: 4m 32s (target: 2m)\nPain points: too many required fields, unclear value proposition\nUsers who complete onboarding have 3.2x higher 30-day retention\nRecommendation: progressive disclosure, reduce required fields to 3' },
        { t: 'Key Finding #3: Performance Perception', b: 'Average perceived load time: "slow" (3.2/5 rating)\nActual load time: 1.8s (within technical target)\nSkeleton screens improved perception by 40%\nAnimations during loading reduced frustration scores by 25%\nRecommendation: focus on perceived performance, not just technical metrics' },
        { t: 'Usability Test Results', sec: true },
        { t: 'Task Success Rates', b: 'Create new project: 92% success (easy baseline)\nShare with team member: 71% success (share button hard to find)\nExport as PDF: 54% success (buried in overflow menu)\nApply template: 83% success (template gallery well-received)\nCollaborate real-time: 67% success (cursor presence confusing)\nAdjust permissions: 38% success (permission model too complex)' },
        { t: 'System Usability Scale (SUS)', b: 'Overall SUS score: 68.4 (industry avg: 68, target: 75)\nBeginner users: 58.2 (below acceptable)\nIntermediate users: 72.1 (good)\nAdvanced users: 78.8 (excellent)\nBiggest gap: "I found the system unnecessarily complex" — scored 3.8/5' },
        { t: 'Affinity Map: Pain Points', b: 'Cluster 1: Navigation & Information Architecture (42 sticky notes)\nCluster 2: Collaboration & Sharing (31 sticky notes)\nCluster 3: Performance & Loading (24 sticky notes)\nCluster 4: Visual Design & Aesthetics (18 sticky notes)\nCluster 5: Feature Discoverability (15 sticky notes)' },
        { t: 'Recommendations', sec: true },
        { t: 'Priority Recommendations', b: 'P0 — Redesign navigation to bottom tab bar (impact: high, effort: medium)\nP0 — Simplify onboarding to 3 steps (impact: high, effort: low)\nP1 — Add skeleton screens for all loading states (impact: medium, effort: low)\nP1 — Redesign share flow with autocomplete (impact: medium, effort: medium)\nP2 — Simplify permission model to 3 tiers (impact: medium, effort: high)\nP2 — Add contextual tooltips for advanced features (impact: low, effort: low)' },
        { t: 'Design Principles (Updated)', b: 'Clarity over cleverness: every action should be self-explanatory\nProgress over perfection: show partial results, let users iterate\nCollaboration by default: sharing should be 1 tap, not 3\nPerformance is a feature: speed is a competitive advantage\nAccessibility is non-negotiable: WCAG AA minimum across all flows' },
        { t: 'Next Steps & Timeline', b: 'March 1–14: Wireframe navigation redesign\nMarch 15–28: Prototype onboarding v2\nApril 1–14: Usability test round 3 (12 participants)\nApril 15–30: Iterate based on test results\nMay 1: Handoff to engineering, begin implementation sprint' },
        { t: 'Appendix: Methodology Notes', b: 'Recruiting: UserTesting.com + internal panel\nCompensation: $100 Amazon gift card per session\nFacilitator: Anika Patel (lead researcher)\nNote-taker: Marcus Rivera (product designer)\nRecording consent: 100% opted in for video recording\nData storage: Anonymized on DesignCo Research Drive' },
        { t: 'Thank You', sub: 'Questions? → anika.patel@designco.io\nFull report: designco.notion.so/research-q1-2026', sec: true }
    ];
    return slides.map((s, i) => {
        const isSec = s.sec && !s.b;
        const bg = isSec ? '#14AE5C' : '#ffffff';
        const textColor = isSec ? '#ffffff' : '#2c2c2c';
        const layout = isSec ? (i === 0 || i === slides.length - 1 ? 'title' : 'section-header') : 'title-content';
        const elems = [makeTextElement({ x: 60, y: isSec ? 180 : 40, width: 840, height: 60, content: s.t, style: { fontFamily: 'Inter', fontSize: isSec ? 42 : 30, fontWeight: 'bold', color: textColor, textAlign: isSec ? 'center' : 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -0.5, listType: 'none' } })];
        if (s.sub) elems.push(makeTextElement({ x: 160, y: 260, width: 640, height: 50, content: s.sub, style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: isSec ? '#c8f0d4' : '#888888', textAlign: 'center', italic: false, underline: false, lineHeight: 1.5, letterSpacing: 0, listType: 'none' } }));
        if (s.b) elems.push(makeTextElement({ x: 60, y: 120, width: 840, height: 300, content: s.b, style: { fontFamily: 'Inter', fontSize: 17, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.9, letterSpacing: 0, listType: 'bullet' } }));
        return makeSlide(`slide_004_${String(i).padStart(2,'0')}`, pid, i, layout, bg,
            { type: i % 3 === 0 ? 'slide' : 'fade', duration: 400 }, '', elems);
    });
}

const PRES_004_SLIDES = generateResearchSlides();

// ============================================================
// PRESENTATIONS 5–18: Generated with realistic variety
// ============================================================
function generatePresentation(pid, config) {
    return config.slideTitles.map((title, i) => {
        const isFirst = i === 0;
        const isLast = i === config.slideTitles.length - 1;
        const isSec = config.sectionBreaks && config.sectionBreaks.includes(i);
        const layout = isFirst || isLast ? 'title' : isSec ? 'section-header' : ['title-content', 'two-column', 'title-content', 'image-focused'][i % 4];
        const bg = isFirst || isLast || isSec ? config.accentBg : '#ffffff';
        const textColor = bg !== '#ffffff' ? '#ffffff' : '#2c2c2c';
        const elems = [
            makeTextElement({ x: 60, y: (isFirst || isLast || isSec) ? 180 : 40, width: 840, height: 60, content: title, style: { fontFamily: config.font || 'Inter', fontSize: (isFirst || isLast) ? 44 : isSec ? 38 : 30, fontWeight: 'bold', color: textColor, textAlign: (isFirst || isLast || isSec) ? 'center' : 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -0.5, listType: 'none' } })
        ];
        if ((isFirst || isLast) && config.subtitle) {
            elems.push(makeTextElement({ x: 160, y: 260, width: 640, height: 50, content: isFirst ? config.subtitle : config.endSubtitle || 'Thank you!', style: { fontFamily: config.font || 'Inter', fontSize: 18, fontWeight: 'normal', color: bg !== '#ffffff' ? '#bbbbbb' : '#888888', textAlign: 'center', italic: false, underline: false, lineHeight: 1.5, letterSpacing: 0, listType: 'none' } }));
        }
        if (!isFirst && !isLast && !isSec && config.bodies && config.bodies[i]) {
            elems.push(makeTextElement({ x: 60, y: 120, width: layout === 'two-column' ? 400 : 840, height: 300, content: config.bodies[i], style: { fontFamily: config.font || 'Inter', fontSize: 17, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }));
            if (layout === 'two-column' && config.rightBodies && config.rightBodies[i]) {
                elems.push(makeTextElement({ x: 500, y: 120, width: 400, height: 300, content: config.rightBodies[i], style: { fontFamily: config.font || 'Inter', fontSize: 17, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }));
            }
            if (layout === 'image-focused') {
                elems.push(makeImageElement({ x: 520, y: 100, width: 380, height: 280, imagePlaceholder: config.imagePlaceholder || '#e8e8e8' }));
            }
        }
        if (!isFirst && !isLast && !isSec) {
            elems.push(makeShapeElement({ x: 60, y: 480, width: 840, height: 2, shapeType: 'line', fill: '#e8e8e8', stroke: '#e8e8e8', strokeWidth: 1 }));
        }
        return makeSlide(`slide_${pid.split('_')[1]}_${String(i).padStart(2,'0')}`, pid, i, layout, bg,
            { type: TRANSITION_TYPES[i % TRANSITION_TYPES.length], duration: 400 + (i % 4) * 100 },
            config.notes && config.notes[i] ? config.notes[i] : '', elems);
    });
}

const PRES_005_SLIDES = generatePresentation('pres_005', {
    accentBg: '#023E8A', font: 'Inter',
    subtitle: 'Engineering Architecture — Q1 2026',
    endSubtitle: 'architecture@designco.io',
    sectionBreaks: [4, 7],
    slideTitles: ['Engineering Architecture Overview', 'System Architecture', 'Frontend Stack', 'Backend Services',
        'Data Layer', 'Database Architecture', 'Caching Strategy', 'Infrastructure', 'CI/CD Pipeline', 'Monitoring & Observability', 'Thank You'],
    bodies: { 1: 'React 18 with Server Components\nNext.js for SSR and routing\nTypeScript throughout the stack\nMicro-frontend architecture for team autonomy\nWebSocket layer for real-time features',
        2: 'Node.js + Express API gateway\nGo microservices for performance-critical paths\nGraphQL federation for API composition\nEvent-driven architecture with Kafka\ngRPC for inter-service communication',
        3: 'PostgreSQL 15 as primary datastore\nRedis for caching and pub/sub\nElasticsearch for full-text search\nS3 for file storage (4.2 PB total)\nClickHouse for analytics pipeline',
        5: 'Read replicas across 3 regions\nPartitioning by organization ID\n99.99% uptime SLA\nAutomated failover in < 30 seconds\nPoint-in-time recovery with 5-minute RPO',
        6: 'Multi-tier caching: Browser → CDN → Redis → DB\nCache hit rate: 94.2% (target: 95%)\nCache invalidation via event-driven approach\nEdge caching for static assets (CloudFront)',
        8: 'GitHub Actions for CI\nArgoCD for Kubernetes deployments\nCanary releases with 1% → 10% → 50% → 100%\nRollback in < 2 minutes\n850+ automated tests per pipeline',
        9: 'Datadog for metrics and APM\nPagerDuty for incident management\nCustom dashboards per team\nP99 latency target: < 200ms\nError budget: 0.01% (99.99% reliability)' },
    notes: { 0: 'High-level overview for new engineers and cross-functional partners.' }
});

const PRES_006_SLIDES = generatePresentation('pres_006', {
    accentBg: '#BC4749', font: 'Poppins',
    subtitle: 'DesignCo — March 2026 All-Hands',
    endSubtitle: 'Let\'s make Q2 amazing! 🚀',
    sectionBreaks: [5, 10, 15],
    slideTitles: ['Annual Company All-Hands 2026', 'CEO Welcome', 'Company Highlights', 'Headcount & Growth', 'Culture & Engagement',
        'Product Update', 'What We Built', 'Customer Success Stories', 'Product Roadmap Preview', 'Design System Evolution',
        'Business & Finance', 'Revenue Performance', 'Market Position', 'Fundraising Update', 'Customer Acquisition',
        'People & Culture', 'New Hires & Promotions', 'DEI Progress', 'Learning & Development', 'Looking Ahead', 'Thank You & Q&A'],
    bodies: { 1: 'Welcome to our annual all-hands meeting.\nIncredible year of growth and innovation.\nI want to recognize every team member\'s contribution.\nWe grew from 85 to 127 employees.\nOur product is now used by 2.3M people monthly.',
        2: '180% YoY user growth\nExpanded to 3 offices globally\nLaunched 4 major product features\nAchieved $50M ARR run rate\nWon "Best Design Tool" at Product Hunt Golden Kitty Awards',
        3: 'Engineering: 52 → 68 people\nDesign: 18 → 24 people\nSales & Marketing: 12 → 22 people\nOperations: 8 → 13 people\nTotal headcount: 127 (+49% YoY)',
        4: 'Employee NPS: 72 (excellent)\nRetention rate: 94%\nAverage tenure: 2.1 years\nDiversity index: 0.78 (target: 0.80)\nRemote/hybrid: 65% of workforce',
        6: 'Collaboration Engine v2.0 — shipped January\nAdvanced Prototyping — shipped February\nFigma-to-Code Beta — launched March\nPerformance Overhaul — 40% faster rendering\n200+ new component library primitives',
        7: 'Spotify: Reduced design iteration time by 60%\nAirbnb: Unified 12 design teams on our platform\nStripe: Cut design-to-dev handoff time from 2 weeks to 2 days\nShopify: 200+ merchants using our templates',
        8: 'Q2: AI Design Assistant (biggest initiative)\nQ3: Design Systems 2.0 with multi-brand theming\nQ4: Enterprise platform with advanced security\nOngoing: Performance improvements and accessibility',
        11: 'Revenue: $50.4M ARR (run rate)\nGrowth: +180% YoY\nGross Margin: 82%\nBurn rate: $2.1M/month\nRunway: 28 months',
        12: '#3 in design tools market share\n#1 in collaboration features satisfaction\nFastest growing in enterprise segment\nStrongest developer community engagement\nHighest NPS in category (72)',
        13: 'Series A: $25M (2024)\nSeries B: $80M (in progress, 2026)\nTotal raised to date: $30M\nValuation: $600M pre-money (Series B)\nInvestor interest: oversubscribed',
        16: '42 new hires in the past year\n6 internal promotions\nNotable: VP Engineering (ex-Figma), Head of AI (ex-Google)\nIntern program: 8 interns, 5 converted to full-time',
        17: 'Gender parity in leadership: 48% women\nEthnicity diversity: 12 nationalities represented\nPay equity audit: completed, 0.98 ratio\nERG groups: 4 active groups\nInclusive hiring: blind resume screening',
        18: 'LinkedIn Learning partnership for all employees\n$3,000 annual learning budget per person\n24 internal tech talks this year\nDesign critique sessions: monthly\nHackathon: Q2 (theme: AI + Design)' },
    notes: {}
});

const PRES_007_SLIDES = generatePresentation('pres_007', {
    accentBg: '#1B4332', font: 'Inter',
    subtitle: 'Client: TechVentures Inc. — Website Redesign',
    endSubtitle: 'Next steps: Review → Approve → Kickoff',
    sectionBreaks: [4, 8],
    slideTitles: ['Client Proposal: TechVentures Redesign', 'Project Understanding', 'Our Approach', 'Team & Timeline',
        'Discovery Phase', 'User Research Plan', 'Competitive Analysis', 'Content Strategy',
        'Design Phase', 'Visual Direction Options', 'Responsive Strategy', 'Deliverables & Milestones',
        'Investment & Terms', 'Thank You'],
    bodies: { 1: 'TechVentures needs a modern web presence that reflects their innovation\nCurrent site: 4 years old, not mobile-optimized, high bounce rate (72%)\nGoals: Increase leads by 40%, reduce bounce rate to < 45%, mobile-first\nTarget audience: CTOs, VPs of Engineering at Series B+ startups',
        2: 'Phase 1: Discovery & Research (2 weeks)\nPhase 2: Strategy & Architecture (1 week)\nPhase 3: Visual Design (3 weeks)\nPhase 4: Prototyping & Testing (2 weeks)\nPhase 5: Development Handoff (1 week)',
        3: 'Lead Designer: Sarah Chen\nUX Researcher: Anika Patel\nVisual Designer: Elena Voronova\nProject Manager: David Kim\nTimeline: 9 weeks total (April 1 – June 2, 2026)',
        5: '8 stakeholder interviews\n12 user interviews (current customers + prospects)\nAnalytics deep-dive (Google Analytics + Hotjar)\nSurvey to 500 existing users\nPersona development (3 primary, 2 secondary)',
        6: 'Direct competitors: 5 companies analyzed\nIndirect competitors: 3 adjacent industries\nBenchmarking: Performance, UX patterns, content strategy\nGap analysis: Where TechVentures can differentiate',
        7: 'Content audit of 240 existing pages\nSEO analysis and keyword mapping\nContent hierarchy and IA redesign\nBlog and resource center strategy\nCTA optimization framework',
        9: '3 visual direction options presented as mood boards\nFull homepage design in chosen direction\n5 key page templates\nComponent library design\nAnimation and interaction guidelines',
        10: 'Mobile-first design approach\nBreakpoints: 375px, 768px, 1024px, 1440px\nTouch-friendly interactions\nPerformance budget: < 2s LCP on 3G\nAccessibility: WCAG AA compliance',
        11: 'Week 2: Research report & personas\nWeek 3: Site map & wireframes\nWeek 6: Visual design (3 directions)\nWeek 7: Chosen direction refined\nWeek 9: Final prototype & dev handoff package',
        12: 'Project fee: $84,000 (fixed price)\nPayment: 30% upfront, 40% at design approval, 30% at handoff\nIncludes: 2 rounds of revisions per deliverable\nOptional: Development support at $175/hour\nMaintenance retainer: $3,500/month (optional)' },
    notes: { 0: 'Customize the intro slide with TechVentures branding before the meeting.' }
});

const PRES_008_SLIDES = generatePresentation('pres_008', {
    accentBg: '#555555', font: 'Inter',
    subtitle: 'Sprint Review — Week ending March 14, 2026',
    endSubtitle: 'Next sprint starts Monday!',
    sectionBreaks: [],
    slideTitles: ['Design Sprint Week 12 Recap', 'Sprint Goals', 'What We Completed', 'Key Decisions',
        'Design Explorations', 'Feedback Summary', 'Blockers & Risks', 'Next Sprint Plan'],
    bodies: { 1: 'Finalize mobile navigation redesign\nComplete accessibility audit for checkout flow\nPrototype AI suggestion overlay\nReview brand guidelines v2 draft',
        2: 'Mobile navigation: Shipped bottom tab bar design (3 iterations)\nAccessibility: 14 of 18 issues resolved\nAI overlay: First prototype ready for testing\nBrand guidelines: v2 draft reviewed, pending color palette finalization',
        3: 'Bottom navigation beats hamburger menu (A/B test: +34% task completion)\nAI suggestions: overlay > sidebar (user preference from 8/10 testers)\nAccessibility: Will exceed WCAG AA, targeting AAA for critical paths\nBrand color: Keeping purple (#7B61FF) as primary, updating secondary palette',
        4: 'Explored 4 variations of the AI suggestion overlay\nTested micro-interactions for slide transitions\nWireframed new onboarding flow (3-step vs 5-step)\nMocked up dark mode for the editor',
        5: 'PM team: Positive on navigation redesign, wants to fast-track\nEngineering: AI overlay needs performance profiling before commit\nStakeholders: Brand guidelines need CEO sign-off by March 22\nUsers (beta): "The new navigation is so much better" — 7/8 positive',
        6: 'Engineering bandwidth for AI features (3 engineers instead of 5)\nCEO travel may delay brand guidelines sign-off\nAccessibility testing tools licensing expires March 30\nRisk: Scope creep on the onboarding redesign',
        7: 'Ship mobile navigation to beta (March 18)\nComplete remaining 4 accessibility issues\nAI overlay: Performance profiling + iteration\nOnboarding redesign: Wireframes + user flow\nBrand guidelines: Final review meeting (March 20)' },
    notes: {}
});

const PRES_009_SLIDES = generatePresentation('pres_009', {
    accentBg: '#0077B6', font: 'Open Sans',
    subtitle: 'New Employee Orientation — DesignCo 2026',
    endSubtitle: 'Welcome to the team! HR: hr@designco.io',
    sectionBreaks: [5, 10],
    slideTitles: ['Welcome to DesignCo!', 'About DesignCo', 'Our Mission & Values', 'Meet the Leadership Team', 'Your First 30 Days',
        'Tools & Environment', 'Development Setup', 'Communication Tools', 'Design Tools Access', 'HR & Benefits Overview',
        'Policies & Culture', 'Work From Home Policy', 'PTO & Leave', 'Code of Conduct', 'Growth & Development',
        'FAQ & Resources'],
    bodies: { 1: 'Founded in 2022 in San Francisco\nNow 127 employees across SF, London, Tokyo\n2.3M monthly active users\nDesign collaboration platform used by Spotify, Airbnb, Stripe\nBacked by Sequoia, a16z, and Craft Ventures',
        2: 'Mission: Empower every team to design collaboratively\nValues: Craft, Collaboration, Courage, Curiosity\nWe believe great design should be accessible to everyone\nWe build tools that remove friction from the creative process',
        3: 'CEO: Alex Morgan (ex-Google Design Director)\nCTO: Jordan Reeves (ex-Stripe Engineering)\nVP Design: Sarah Chen (our very own!)\nVP Engineering: Recently hired from Figma\nHead of AI: Former Google Brain researcher',
        4: 'Week 1: Orientation, tool setup, meet your team\nWeek 2: Shadow sessions with key team members\nWeek 3: First small project or contribution\nWeek 4: 30-day check-in with manager\nBuddy system: Paired with a tenured team member',
        6: 'MacBook Pro 16" (M3 Max) for all engineering & design\nGitHub Enterprise for source code\nFigma Organization account (obviously!)\nLinear for project management\nVercel for frontend deployments',
        7: 'Slack: Primary communication (channels by team + topic)\nNotion: Documentation and wikis\nZoom: Meetings and calls\nLoom: Async video updates\nLinear: Task tracking and sprint management',
        8: 'Full Figma Organization license\nAdobe Creative Cloud (if needed)\nProtoPie for advanced prototyping\nMaze for usability testing\nContentful for design system documentation',
        9: 'Health insurance: Fully covered for employee + 80% for dependents\n401(k): 4% company match\nStock options: Refresh grants annually\nHome office stipend: $2,000 one-time\nWellness benefit: $100/month',
        11: 'Hybrid-first: 2 days in office (Tue/Thu), 3 remote\nFully remote option for roles that support it\nCo-working space stipend for remote employees: $200/month\nCore hours: 10am–4pm local time\nNo-meeting Wednesdays',
        12: 'Unlimited PTO (minimum 15 days encouraged)\nSick leave: 10 days/year\nParental leave: 16 weeks (all parents)\nBereavement: 5 days\nVolunteer days: 2 days/year',
        13: 'Respect and inclusion are non-negotiable\nZero tolerance for harassment\nSpeak up: Anonymous reporting through Ethics Hotline\nData security: Handle customer data with care\nOpen source: Contribute with manager approval',
        14: '$3,000/year professional development budget\nConference attendance: 2 conferences/year\nInternal mobility: Apply for any role after 1 year\nMentorship program: Formal 6-month tracks\nDesign critique: Weekly sessions open to all' },
    notes: { 0: 'Make new hires feel welcomed. This is their first impression of the company.' }
});

const PRES_010_SLIDES = generatePresentation('pres_010', {
    accentBg: '#E63946', font: 'Montserrat',
    subtitle: 'Q2 2026 — "Design Without Limits" Campaign',
    endSubtitle: 'Let\'s launch this! marketing@designco.io',
    sectionBreaks: [3, 7],
    slideTitles: ['Marketing Campaign Launch Plan', 'Campaign Objectives', 'Target Audience',
        'Creative Strategy', 'Key Messages', 'Visual Identity', 'Content Calendar',
        'Distribution Channels', 'Paid Media Plan', 'Organic & Social Strategy', 'KPIs & Measurement', 'Thank You'],
    bodies: { 1: 'Launch the AI Design Assistant feature to market\nDrive 50,000 feature activations in first month\nIncrease brand awareness by 25% (measured by branded search)\nGenerate 3,000 enterprise leads\nPosition DesignCo as the AI-first design platform',
        2: 'Primary: Design leads and managers at companies with 50+ employees\nSecondary: Individual designers exploring AI tools\nTertiary: Developers who collaborate with design teams\nGeo focus: US, UK, Germany, Japan\nBehavior: Active in design communities, early adopters',
        4: '"Design Without Limits" — AI amplifies human creativity, doesn\'t replace it\n"From Idea to Design in Seconds" — Speed messaging\n"Your Design Co-pilot" — AI as assistant, not replacement\n"Enterprise-Ready AI" — Security and compliance messaging\nCTA: "Try AI Design Assistant Free"',
        5: 'Hero visual: Human hand + AI hand creating together\nColor palette: Gradient from brand purple to electric blue\nMotion design: Fluid animations showing AI in action\nPhotography: Real designers using the product (not stock)\nTypography: Bold Montserrat headlines, clean Inter body',
        6: 'Pre-launch (March 15–31): Teaser campaign, waitlist\nLaunch week (April 1–7): Full campaign blitz\nSustain (April 8–30): Content drip, testimonials\nOptimize (May 1–15): Double down on top performers\nWrapping (May 16–31): Case study phase',
        8: 'Google Ads: $120K budget, search + display\nLinkedIn: $80K budget, sponsored content + InMail\nTwitter/X: $30K budget, promoted tweets\nYouTube: $50K budget, pre-roll + bumper ads\nProduct Hunt: Featured launch (April 1)\nTotal paid budget: $280K',
        9: 'Blog: 8 articles (tutorials, thought leadership, case studies)\nSocial: Daily posts across LinkedIn, Twitter, Instagram\nEmail: 6-part nurture sequence to 150K subscribers\nCommunity: 3 webinars, AMA with product team\nPartner co-marketing: 5 agency partners',
        10: 'Feature activations: 50K target (month 1)\nWebsite traffic: +40% vs baseline\nLead generation: 3,000 MQLs\nSocial engagement: 2x current rates\nBrand awareness: +25% branded search volume\nPipeline influence: $2M in enterprise pipeline' },
    notes: {}
});

const PRES_011_SLIDES = generatePresentation('pres_011', {
    accentBg: '#2D6A4F', font: 'Inter',
    subtitle: 'Conducted February 2026 — WCAG 2.1 AA/AAA',
    endSubtitle: 'Full report: notion.so/a11y-audit-2026',
    sectionBreaks: [3, 6],
    slideTitles: ['Accessibility Audit Results', 'Audit Scope', 'Methodology',
        'Findings Overview', 'Critical Issues (WCAG A)', 'Serious Issues (WCAG AA)', 'Minor Issues',
        'Remediation Plan', 'Thank You'],
    bodies: { 1: 'Pages tested: 24 core user flows\nAssistive technologies: NVDA, VoiceOver, JAWS\nDevices: Desktop (Chrome, Firefox, Safari), iOS, Android\nStandard: WCAG 2.1 Level AA (with AAA targets for critical flows)',
        2: 'Automated scanning: axe-core, Lighthouse\nManual testing: Keyboard navigation, screen reader\nUser testing: 6 participants with disabilities\nColor contrast analysis: All UI elements\nForm and interaction testing: All input types',
        4: 'Missing alt text on 23 images in the editor\nFocus trap in modal dialogs not implemented\n4 custom dropdowns not keyboard-accessible\nColor contrast ratio < 3:1 on 8 secondary buttons\nARIA labels missing on 12 interactive elements',
        5: 'Heading hierarchy skips H2 in 3 pages\nForm error messages not associated with inputs\nToast notifications not announced to screen readers\nDrag-and-drop has no keyboard alternative\nFocus order incorrect in slide panel',
        7: 'Sprint 1 (March 1–14): Fix all critical WCAG A issues\nSprint 2 (March 15–28): Fix serious WCAG AA issues\nSprint 3 (April 1–14): Address minor issues\nOngoing: Accessibility testing in CI pipeline\nTarget: Full WCAG AA compliance by April 30' },
    notes: {}
});

const PRES_012_SLIDES = generatePresentation('pres_012', {
    accentBg: '#16213e', font: 'Inter',
    subtitle: 'Finance Team — Revenue & Growth Analysis',
    endSubtitle: 'finance@designco.io — Next review: April 15',
    sectionBreaks: [4, 8],
    slideTitles: ['Q4 2025 Revenue Analysis', 'Executive Summary', 'Revenue Breakdown', 'Subscription Metrics',
        'Growth Analysis', 'MRR Trends', 'Customer Acquisition Cost', 'Churn Analysis', 'Segment Performance',
        'Enterprise Revenue', 'SMB Revenue', 'Self-Serve Revenue', 'Outlook & Forecast'],
    bodies: { 1: 'Total Q4 revenue: $11.8M (+32% QoQ)\nMRR at end of Q4: $4.2M\nNet revenue retention: 142%\nGross margin: 82% (up from 79%)\nCustomers: 12,400 paid accounts',
        2: 'Subscriptions: $10.2M (86%)\nProfessional services: $0.9M (8%)\nMarketplace/plugins: $0.7M (6%)\nEnterprise: 45% of subscription revenue\nSMB: 35% of subscription revenue',
        3: 'Monthly active subscribers: 34,200\nAverage revenue per user: $28.40/month\nTrial-to-paid conversion: 14.2%\nAnnual contract value: $342/year avg\nEnterprise ACV: $32,000/year avg',
        5: 'January: $3.8M → February: $4.0M → March: $4.2M\nGrowth rate: 5.2% month-over-month\nExpansion revenue: $620K/month\nContraction: $180K/month\nNet new MRR: $440K/month',
        6: 'Blended CAC: $142 (target: < $150)\nEnterprise CAC: $4,200 (LTV/CAC ratio: 8.2x)\nSelf-serve CAC: $28 (LTV/CAC ratio: 12.4x)\nPayback period: 4.8 months\nMarketing spend efficiency improving QoQ',
        7: 'Gross churn: 2.8% monthly\nNet churn: -3.2% (negative = expansion > churn)\nEnterprise churn: 0.4% (excellent)\nSMB churn: 3.8% (needs attention)\nTop churn reason: Budget constraints (34%)',
        9: 'Enterprise revenue: $4.6M (39% of total)\n34 new enterprise customers in Q4\nAverage deal cycle: 45 days (down from 62)\nTop verticals: Technology, Financial Services, Healthcare\nPipeline: $8.2M for Q1 2026',
        10: 'SMB revenue: $4.1M (35% of total)\n2,800 active SMB accounts\nGrowth: +28% QoQ\nSelf-serve dominates acquisition\nUpsell rate: 18% to Organization tier',
        11: 'Self-serve revenue: $3.1M (26% of total)\n8,200 individual accounts\nFastest growing segment: +45% QoQ\nPrimarily Professional tier\nHigh expansion potential to team tiers',
        12: 'Q1 2026 projection: $13.2M revenue\nFull year 2026: $72M (conservative)\nKey drivers: Enterprise expansion, AI feature monetization\nRisks: Macro slowdown, competitive pressure\nOpportunity: International expansion (EU launch Q3)' },
    notes: {}
});

const PRES_013_SLIDES = generatePresentation('pres_013', {
    accentBg: '#9747FF', font: 'Inter',
    subtitle: 'DesignCo Mobile Design System — v3.2',
    endSubtitle: 'Component library: figma.com/designco-ds',
    sectionBreaks: [4, 10, 16, 20],
    slideTitles: ['Mobile Design System Components', 'System Overview', 'Design Tokens', 'Color Tokens',
        'Typography', 'Type Scale', 'Font Weights & Styles', 'Line Heights & Spacing',
        'Buttons & Actions', 'Button Variants', 'Icon Buttons', 'Input Fields', 'Dropdowns & Selects',
        'Toggle & Checkbox', 'Radio & Switch', 'Navigation', 'Tab Bars', 'Cards & Lists',
        'List Items', 'Modals & Sheets', 'Bottom Sheets', 'Status & Feedback', 'Toasts & Snackbars',
        'Loading States', 'Thank You'],
    bodies: { 1: '148 components across 12 categories\nBuilt for iOS and Android platforms\nFigma auto-layout for responsive behavior\nDark mode variants for all components\nAccessibility: WCAG AA compliant',
        2: 'Color tokens: 48 semantic colors\nSpacing tokens: 4px base unit (4, 8, 12, 16, 24, 32, 48, 64)\nBorder radius: 4px, 8px, 12px, 16px, 24px (pill)\nShadow tokens: sm, md, lg, xl\nMotion tokens: 150ms, 250ms, 350ms, 500ms',
        3: 'Primary: #7B61FF (Purple-500)\nSecondary: #0D99FF (Blue-500)\nSuccess: #14AE5C (Green-500)\nWarning: #FFC700 (Yellow-500)\nError: #F24822 (Red-500)\nNeutral: Gray-50 through Gray-900',
        5: 'Display: 34/40 — Hero headlines\nH1: 28/34 — Page titles\nH2: 24/30 — Section headers\nH3: 20/26 — Card titles\nBody Large: 17/24 — Primary content\nBody: 15/22 — Standard text\nCaption: 13/18 — Secondary text\nOverline: 11/16 — Labels and overlines',
        6: 'Regular (400): Body text, descriptions\nMedium (500): Buttons, links, emphasis\nSemibold (600): Subheadings, labels\nBold (700): Headlines, titles',
        9: 'Primary: Filled, high emphasis\nSecondary: Outlined, medium emphasis\nTertiary: Text only, low emphasis\nDestructive: Red filled, dangerous actions\nSizes: Small (32px), Medium (40px), Large (48px)',
        11: 'Text input, password, email, number, search\nStates: Default, focused, filled, error, disabled\nWith/without labels, helper text, icons\nCharacter counter for limited fields\nMulti-line textarea variant',
        13: 'Toggle: On/off binary states\nCheckbox: Multi-select options\nStates: Default, checked, indeterminate, disabled\nWith/without labels\nGrouped variants for forms',
        17: 'Basic card: Image + title + description\nCompact card: Thumbnail + text\nAction card: With CTA button\nStats card: Metric + trend indicator\nMedia card: Full-bleed image + overlay text',
        19: 'Center modal: Alerts and confirmations\nBottom sheet: Actions and selections\nFull screen modal: Complex forms\nOverlay: Semi-transparent backdrop\nSheet sizes: Small (30%), Medium (50%), Large (80%)',
        22: 'Success toast: Green accent\nError toast: Red accent\nInfo toast: Blue accent\nWarning toast: Yellow accent\nWith/without action button\nAuto-dismiss: 4 seconds default',
        23: 'Skeleton screens for content loading\nSpinner for indeterminate progress\nProgress bar for determinate progress\nShimmer effect for placeholder content\nPull-to-refresh indicator' },
    notes: {}
});

const PRES_014_SLIDES = generatePresentation('pres_014', {
    accentBg: '#444444', font: 'Inter',
    subtitle: 'Sprint 47 — March 4–14, 2026',
    endSubtitle: 'Action items tracked in Linear',
    sectionBreaks: [],
    slideTitles: ['Team Retrospective: Sprint 47', 'What Went Well', 'What Could Improve', 'Action Items',
        'Shout-outs', 'Next Sprint Focus'],
    bodies: { 1: 'Shipped mobile navigation redesign on time\nGreat collaboration between design and engineering\nAutomated testing caught 3 bugs before release\nNew hire (Elena) onboarded smoothly and contributed by day 3\nStakeholder demo went really well',
        2: 'Scope creep on the AI overlay feature (added 2 days)\nLate feedback from legal on privacy implications\nCI pipeline was flaky (3 false-negative failures)\nDocumentation fell behind — need to catch up\nToo many context switches between projects',
        3: 'Scope: Lock scope by Sprint Planning, changes go to next sprint [Owner: PM]\nLegal: Loop in legal during design phase, not after [Owner: Design Lead]\nCI: Dedicate 1 day to fix flaky tests [Owner: Engineering]\nDocs: Allocate 2 hours/week for documentation [Owner: Everyone]\nFocus: Max 2 projects per person per sprint [Owner: PM]',
        4: 'Elena: Amazing first sprint contribution — fixed 4 accessibility issues!\nMarcus: Went above and beyond on the stakeholder demo preparation\nAnika: User research report was incredibly thorough\nEngineering team: Zero production incidents this sprint!',
        5: 'AI overlay: Performance profiling and optimization\nAccessibility: Complete remaining WCAG AA fixes\nOnboarding: Start wireframing new 3-step flow\nBrand guidelines: Finalize after CEO review\nTech debt: Address 3 highest-priority items from backlog' },
    notes: {}
});

const PRES_015_SLIDES = generatePresentation('pres_015', {
    accentBg: '#0f3460', font: 'Inter',
    subtitle: 'Enterprise Features — Live Demo Walk-through',
    endSubtitle: 'Sales: sales@designco.io — Schedule a demo',
    sectionBreaks: [3, 7],
    slideTitles: ['Product Demo: Enterprise Features', 'Enterprise Overview', 'SSO & Authentication',
        'Admin Dashboard', 'User Management', 'Permission Tiers', 'Audit Logging',
        'Security & Compliance', 'Data Residency', 'SOC2 Certification', 'Thank You'],
    bodies: { 1: 'DesignCo Enterprise is built for large organizations\nCurrently serving 34 enterprise customers\nAverage deal size: $32K ARR\nDesigned for security, compliance, and governance\nDedicated support with < 4 hour response time SLA',
        2: 'SAML 2.0 and OpenID Connect support\nOkta, Azure AD, OneLogin integrations\nMFA enforcement for all users\nSession management with configurable timeout\nJIT (Just-in-Time) provisioning for new users',
        4: 'Manage users individually or via SCIM provisioning\nBulk user operations: invite, deactivate, reassign\nUser groups with cascading permissions\nExternal collaborator management\nLicense usage tracking and optimization',
        5: 'Viewer: View-only access to files and projects\nEditor: Full design capabilities within assigned projects\nAdmin: Team management, billing, and settings\nOwner: Full organization control, SSO configuration\nCustom roles available on Enterprise Plus',
        6: 'Complete audit trail for all user actions\nRetention: 1 year standard, unlimited on Enterprise Plus\nExport: CSV, JSON, or SIEM integration\nFilters: By user, action type, date range, resource\nReal-time alerts for sensitive operations',
        8: 'Choose data storage region: US, EU, APAC\nData isolation per organization\nEncryption at rest (AES-256) and in transit (TLS 1.3)\nRegular penetration testing by third-party\nGDPR, CCPA, and HIPAA compliance ready',
        9: 'SOC2 Type II certification (in progress, target June 2026)\nISO 27001 certification planned for Q4\nAnnual security audits by Deloitte\nBug bounty program: 47 valid reports resolved\nZero data breaches since founding' },
    notes: {}
});

const PRES_016_SLIDES = generatePresentation('pres_016', {
    accentBg: '#4A90D9', font: 'Inter',
    subtitle: 'Proposal for TechStartup.io — March 2026',
    endSubtitle: 'Proposal valid until April 30, 2026',
    sectionBreaks: [4, 9],
    slideTitles: ['Website Redesign Proposal', 'Current State Analysis', 'Competitive Benchmarking', 'Objectives & KPIs',
        'Proposed Solution', 'Information Architecture', 'Visual Design Direction', 'Technical Stack',
        'Responsive Framework', 'Project Management', 'Timeline & Phases', 'Team Composition',
        'Budget Breakdown', 'Thank You'],
    bodies: { 1: 'Current site is 3 years old with dated visual design\nMobile traffic: 62% of visitors, but mobile conversion is 40% below desktop\nPage speed: 4.2s average (target: < 2s)\nSEO: Ranking on page 2 for 80% of target keywords\nBounce rate: 68% (industry avg: 45%)',
        2: 'Analyzed 8 competitors in the B2B SaaS space\nTop performers: Modern design, sub-2s load times, strong CTAs\nGap: Most competitors lack interactive product demos\nOpportunity: Interactive demo + strong social proof = differentiation\nBenchmark: Top quartile conversion rate is 4.2% (current: 1.8%)',
        3: 'Increase organic traffic by 50% within 6 months\nReduce bounce rate to < 45%\nImprove page speed to < 2s (LCP)\nIncrease conversion rate from 1.8% to 3.5%\nAchieve WCAG AA accessibility compliance',
        5: 'Restructure from 240 pages to ~80 focused pages\nNew navigation: Mega-menu with product, solutions, resources\nBlog: Redesigned with category filtering and search\nResource center: Gated content for lead generation\nKnowledge base: Integrated help documentation',
        6: 'Clean, modern aesthetic with bold typography\nGradient accents (brand blue to teal)\nWhitespace-forward layout\nCustom illustrations (flat geometric style)\nDark mode option for developer audience',
        7: 'Next.js 14 with App Router\nTailwind CSS for styling\nContentful CMS for marketing pages\nVercel for hosting and edge functions\nPlausible for privacy-friendly analytics',
        10: 'Phase 1 (Weeks 1–2): Discovery, research, IA\nPhase 2 (Weeks 3–4): Wireframes, content strategy\nPhase 3 (Weeks 5–7): Visual design, 2 rounds of feedback\nPhase 4 (Weeks 8–10): Development sprint\nPhase 5 (Weeks 11–12): QA, launch, and optimization',
        11: 'Project Lead: James O\'Brien\nUX Designer: Anika Patel\nVisual Designer: Priya Sharma-Krishnamurthy\n2 Frontend Developers\nContent Strategist (part-time)',
        12: 'Discovery & Strategy: $12,000\nUX/UI Design: $28,000\nFrontend Development: $35,000\nContent & SEO: $8,000\nQA & Launch: $5,000\nTotal: $88,000' },
    notes: {}
});

const PRES_017_SLIDES = generatePresentation('pres_017', {
    accentBg: '#333333', font: 'Inter',
    subtitle: 'Market Intelligence — Updated March 2026',
    endSubtitle: 'Updated monthly by Strategy team',
    sectionBreaks: [2, 5],
    slideTitles: ['Competitor Analysis Dashboard', 'Market Overview',
        'Direct Competitors', 'Figma (Real)', 'Adobe Creative Suite', 'Canva',
        'Feature Comparison', 'Strategic Implications'],
    bodies: { 1: 'Design tools market growing at 18% CAGR\nTotal market: $28.4B by 2028\nKey trends: AI integration, real-time collaboration, design-to-code\nConsolidation: Adobe acquired Figma (reversed), Canva IPO rumors\nNew entrants: AI-native design tools emerging',
        3: 'Market leader in UI design\n4M+ paying users, est. $600M+ ARR\nStrengths: Brand, network effects, developer ecosystem\nWeaknesses: Pricing pressure, slow AI adoption\nOur advantage: AI-first, faster iteration, better enterprise features',
        4: 'Dominant in creative professional market\nPhotoshop, Illustrator, XD, After Effects\nStrengths: Brand legacy, feature depth, Creative Cloud bundle\nWeaknesses: Complexity, slow collaboration, subscription fatigue\nOur advantage: Modern UX, real-time collaboration, web-native',
        5: 'Strong in consumer/prosumer segment\nEst. 150M+ MAU, approaching IPO\nStrengths: Ease of use, template library, AI features\nWeaknesses: Not professional-grade, limited prototyping\nOur advantage: Professional features, developer handoff, enterprise security',
        6: 'Real-time Collaboration: DesignCo ★★★★★ vs Figma ★★★★ vs Adobe ★★ vs Canva ★★★\nAI Features: DesignCo ★★★★ vs Figma ★★★ vs Adobe ★★★ vs Canva ★★★★\nEnterprise: DesignCo ★★★★ vs Figma ★★★★★ vs Adobe ★★★★ vs Canva ★★\nPrototyping: DesignCo ★★★★★ vs Figma ★★★★ vs Adobe ★★★ vs Canva ★★\nPricing: DesignCo ★★★★ vs Figma ★★★ vs Adobe ★★ vs Canva ★★★★★',
        7: 'Double down on AI as primary differentiator\nEnterprise is our best growth vector (less competition)\nAvoid Canva\'s consumer market — focus on professional/enterprise\nBuild switching tools for Adobe and Figma migration\nInvest in developer community and plugin ecosystem' },
    notes: {}
});

const PRES_018_SLIDES = generatePresentation('pres_018', {
    accentBg: '#F4845F', font: 'Poppins',
    subtitle: 'Creative Thinking Workshop — March 2026',
    endSubtitle: 'Workshop materials: notion.so/workshop-q1',
    sectionBreaks: [],
    slideTitles: ['Design Workshop Materials', 'Workshop Agenda', 'Warm-Up Exercise', 'Group Activity', 'Wrap-Up & Next Steps'],
    bodies: { 1: '9:00 AM — Welcome and introductions (15 min)\n9:15 AM — Warm-up: Crazy 8s sketching exercise (20 min)\n9:35 AM — Design challenge briefing (10 min)\n9:45 AM — Group brainstorming session (45 min)\n10:30 AM — Break (15 min)\n10:45 AM — Prototype and present (60 min)\n11:45 AM — Feedback and voting (15 min)\n12:00 PM — Wrap-up and next steps',
        2: 'Crazy 8s: 8 ideas in 8 minutes\nRules: One idea per panel, no erasing, quantity over quality\nMaterials: Paper template (provided), markers\nTip: Start with the obvious ideas to clear your mind, then push for novelty',
        3: 'Design Challenge: "How might we make the onboarding experience delightful?"\nTeams of 3–4 people\nStep 1: Individual ideation (10 min)\nStep 2: Share and discuss (15 min)\nStep 3: Converge on top 3 ideas (10 min)\nStep 4: Prototype the best idea (30 min)',
        4: 'Each team presents their prototype (5 min each)\nDot voting: 3 votes per person\nWinning idea gets fast-tracked to design sprint\nAll ideas documented in Notion workspace\nFollow-up meeting: Thursday 2pm to review action items' },
    notes: {}
});

// ============================================================
// Assemble all slides
// ============================================================
const ALL_SLIDES = [
    ...PRES_001_SLIDES,
    ...PRES_002_SLIDES,
    ...PRES_003_SLIDES,
    ...PRES_004_SLIDES,
    ...PRES_005_SLIDES,
    ...PRES_006_SLIDES,
    ...PRES_007_SLIDES,
    ...PRES_008_SLIDES,
    ...PRES_009_SLIDES,
    ...PRES_010_SLIDES,
    ...PRES_011_SLIDES,
    ...PRES_012_SLIDES,
    ...PRES_013_SLIDES,
    ...PRES_014_SLIDES,
    ...PRES_015_SLIDES,
    ...PRES_016_SLIDES,
    ...PRES_017_SLIDES,
    ...PRES_018_SLIDES
];

// ============================================================
// Presentations metadata
// ============================================================
const PRESENTATIONS = [
    { id: 'pres_001', title: 'Q1 2026 Product Roadmap', description: 'Quarterly planning presentation covering Q1 achievements and Q2 roadmap for the product team.', createdAt: '2026-02-10T09:00:00Z', updatedAt: '2026-03-15T14:30:00Z', createdBy: 'user_001', theme: 'corporate', tags: ['product', 'roadmap', 'quarterly'], starred: true, status: 'published', slideCount: 15, shareSettings: { visibility: 'team', allowComments: true, allowEditing: false, shareLink: 'https://slides.designco.io/s/prd-q1-2026', embedLink: 'https://slides.designco.io/embed/prd-q1-2026', sharedWith: ['user_002', 'user_003', 'user_004'] } },
    { id: 'pres_002', title: 'Brand Identity Guidelines v2.0', description: 'Comprehensive brand guidelines covering logo, color, typography, iconography, illustration, and layout standards.', createdAt: '2026-01-20T11:00:00Z', updatedAt: '2026-03-12T16:45:00Z', createdBy: 'user_006', theme: 'creative', tags: ['brand', 'design-system', 'guidelines'], starred: true, status: 'published', slideCount: 18, shareSettings: { visibility: 'organization', allowComments: true, allowEditing: true, shareLink: 'https://slides.designco.io/s/brand-v2', embedLink: 'https://slides.designco.io/embed/brand-v2', sharedWith: ['user_001', 'user_002', 'user_003', 'user_004', 'user_005', 'user_006', 'user_007', 'user_008'] } },
    { id: 'pres_003', title: 'Series B Fundraising Pitch', description: 'Confidential investor pitch deck for $80M Series B round at $600M valuation.', createdAt: '2026-02-28T08:00:00Z', updatedAt: '2026-03-16T19:20:00Z', createdBy: 'user_001', theme: 'dark', tags: ['fundraising', 'confidential', 'investors'], starred: true, status: 'published', slideCount: 12, shareSettings: { visibility: 'private', allowComments: false, allowEditing: false, shareLink: '', embedLink: '', sharedWith: ['user_001'] } },
    { id: 'pres_004', title: 'User Research Findings — Mobile App', description: 'Phase 2 research findings covering 24 participants, usability testing, and design recommendations.', createdAt: '2026-02-15T10:00:00Z', updatedAt: '2026-03-08T11:30:00Z', createdBy: 'user_003', theme: 'nature', tags: ['research', 'ux', 'mobile', 'usability'], starred: false, status: 'published', slideCount: 16, shareSettings: { visibility: 'team', allowComments: true, allowEditing: false, shareLink: 'https://slides.designco.io/s/research-mobile-q1', embedLink: '', sharedWith: ['user_001', 'user_002', 'user_004', 'user_006'] } },
    { id: 'pres_005', title: 'Engineering Architecture Overview', description: 'Technical overview of system architecture, infrastructure, and CI/CD pipeline for cross-functional partners.', createdAt: '2026-01-05T14:00:00Z', updatedAt: '2026-03-01T09:15:00Z', createdBy: 'user_004', theme: 'ocean', tags: ['engineering', 'architecture', 'technical'], starred: false, status: 'published', slideCount: 11, shareSettings: { visibility: 'team', allowComments: true, allowEditing: true, shareLink: 'https://slides.designco.io/s/eng-architecture', embedLink: '', sharedWith: ['user_001', 'user_004', 'user_008'] } },
    { id: 'pres_006', title: 'Annual Company All-Hands 2026', description: 'Company-wide all-hands presentation covering all departments, financials, and company culture.', createdAt: '2026-02-20T08:00:00Z', updatedAt: '2026-03-14T22:00:00Z', createdBy: 'user_001', theme: 'warm', tags: ['all-hands', 'company', 'culture'], starred: true, status: 'published', slideCount: 21, shareSettings: { visibility: 'organization', allowComments: true, allowEditing: false, shareLink: 'https://slides.designco.io/s/allhands-2026', embedLink: 'https://slides.designco.io/embed/allhands-2026', sharedWith: ['user_001', 'user_002', 'user_003', 'user_004', 'user_005', 'user_006', 'user_007', 'user_008'] } },
    { id: 'pres_007', title: 'Client Proposal — TechVentures Redesign', description: 'Website redesign proposal for TechVentures Inc. covering discovery, design, and development phases.', createdAt: '2026-03-01T10:00:00Z', updatedAt: '2026-03-13T17:00:00Z', createdBy: 'user_001', theme: 'nature', tags: ['client', 'proposal', 'web-design'], starred: false, status: 'published', slideCount: 14, shareSettings: { visibility: 'private', allowComments: true, allowEditing: true, shareLink: 'https://slides.designco.io/s/tv-proposal', embedLink: '', sharedWith: ['user_001', 'user_003', 'user_007', 'user_008'] } },
    { id: 'pres_008', title: 'Design Sprint Week 12 Recap', description: 'Weekly design sprint review covering completed work, decisions, feedback, and next sprint planning.', createdAt: '2026-03-14T16:00:00Z', updatedAt: '2026-03-14T18:30:00Z', createdBy: 'user_002', theme: 'minimal', tags: ['sprint', 'recap', 'weekly'], starred: false, status: 'published', slideCount: 8, shareSettings: { visibility: 'team', allowComments: true, allowEditing: true, shareLink: '', embedLink: '', sharedWith: ['user_001', 'user_002', 'user_003', 'user_004'] } },
    { id: 'pres_009', title: 'Onboarding Training Module', description: 'New employee orientation covering company overview, tools, benefits, and policies.', createdAt: '2025-11-15T09:00:00Z', updatedAt: '2026-03-10T10:00:00Z', createdBy: 'user_007', theme: 'ocean', tags: ['onboarding', 'hr', 'training'], starred: false, status: 'published', slideCount: 16, shareSettings: { visibility: 'organization', allowComments: false, allowEditing: false, shareLink: 'https://slides.designco.io/s/onboarding-2026', embedLink: 'https://slides.designco.io/embed/onboarding-2026', sharedWith: ['user_007'] } },
    { id: 'pres_010', title: 'Marketing Campaign: Design Without Limits', description: 'Q2 2026 campaign launch plan for the AI Design Assistant feature.', createdAt: '2026-03-05T13:00:00Z', updatedAt: '2026-03-17T11:45:00Z', createdBy: 'user_008', theme: 'sunset', tags: ['marketing', 'campaign', 'ai', 'launch'], starred: true, status: 'published', slideCount: 12, shareSettings: { visibility: 'team', allowComments: true, allowEditing: true, shareLink: 'https://slides.designco.io/s/campaign-q2', embedLink: '', sharedWith: ['user_001', 'user_002', 'user_008'] } },
    { id: 'pres_011', title: 'Accessibility Audit Results', description: 'WCAG 2.1 AA/AAA accessibility audit findings and remediation plan.', createdAt: '2026-02-25T09:30:00Z', updatedAt: '2026-03-05T14:00:00Z', createdBy: 'user_003', theme: 'nature', tags: ['accessibility', 'audit', 'wcag'], starred: false, status: 'published', slideCount: 9, shareSettings: { visibility: 'team', allowComments: true, allowEditing: false, shareLink: '', embedLink: '', sharedWith: ['user_001', 'user_003', 'user_004'] } },
    { id: 'pres_012', title: 'Q4 2025 Revenue Analysis', description: 'Quarterly revenue analysis covering subscriptions, enterprise, SMB, and self-serve segments.', createdAt: '2026-01-10T08:00:00Z', updatedAt: '2026-01-25T16:30:00Z', createdBy: 'user_005', theme: 'corporate', tags: ['finance', 'revenue', 'quarterly', 'analysis'], starred: false, status: 'published', slideCount: 13, shareSettings: { visibility: 'private', allowComments: true, allowEditing: false, shareLink: '', embedLink: '', sharedWith: ['user_001', 'user_005'] } },
    { id: 'pres_013', title: 'Mobile Design System Components', description: 'Comprehensive mobile design system documentation with 148 components across 12 categories.', createdAt: '2025-10-01T10:00:00Z', updatedAt: '2026-03-11T15:20:00Z', createdBy: 'user_006', theme: 'creative', tags: ['design-system', 'mobile', 'components', 'documentation'], starred: true, status: 'published', slideCount: 25, shareSettings: { visibility: 'organization', allowComments: true, allowEditing: true, shareLink: 'https://slides.designco.io/s/mobile-ds-v3', embedLink: 'https://slides.designco.io/embed/mobile-ds-v3', sharedWith: ['user_001', 'user_002', 'user_003', 'user_004', 'user_006', 'user_008'] } },
    { id: 'pres_014', title: 'Team Retrospective — Sprint 47', description: 'Sprint 47 retrospective covering wins, improvements, and action items.', createdAt: '2026-03-14T15:00:00Z', updatedAt: '2026-03-14T16:45:00Z', createdBy: 'user_002', theme: 'minimal', tags: ['retro', 'sprint', 'agile'], starred: false, status: 'published', slideCount: 6, shareSettings: { visibility: 'team', allowComments: true, allowEditing: true, shareLink: '', embedLink: '', sharedWith: ['user_001', 'user_002', 'user_003', 'user_004', 'user_008'] } },
    { id: 'pres_015', title: 'Product Demo — Enterprise Features', description: 'Live demo walk-through of enterprise features including SSO, admin dashboard, and audit logging.', createdAt: '2026-03-10T11:00:00Z', updatedAt: '2026-03-16T09:30:00Z', createdBy: 'user_004', theme: 'ocean', tags: ['demo', 'enterprise', 'product', 'sales'], starred: false, status: 'published', slideCount: 11, shareSettings: { visibility: 'team', allowComments: false, allowEditing: false, shareLink: 'https://slides.designco.io/s/enterprise-demo', embedLink: '', sharedWith: ['user_001', 'user_004'] } },
    { id: 'pres_016', title: 'Website Redesign Proposal — TechStartup.io', description: 'Website redesign proposal with technical analysis, design direction, and budget breakdown.', createdAt: '2026-03-08T14:00:00Z', updatedAt: '2026-03-15T10:00:00Z', createdBy: 'user_004', theme: 'ocean', tags: ['proposal', 'web-design', 'client'], starred: false, status: 'draft', slideCount: 14, shareSettings: { visibility: 'private', allowComments: true, allowEditing: true, shareLink: '', embedLink: '', sharedWith: ['user_003', 'user_004', 'user_006'] } },
    { id: 'pres_017', title: 'Competitor Analysis Dashboard', description: 'Monthly updated competitive intelligence covering Figma, Adobe, and Canva.', createdAt: '2025-12-01T09:00:00Z', updatedAt: '2026-03-02T11:00:00Z', createdBy: 'user_005', theme: 'minimal', tags: ['strategy', 'competitors', 'market', 'analysis'], starred: false, status: 'archived', slideCount: 8, shareSettings: { visibility: 'private', allowComments: true, allowEditing: false, shareLink: '', embedLink: '', sharedWith: ['user_001', 'user_005'] } },
    { id: 'pres_018', title: 'Design Workshop Materials', description: 'Creative thinking workshop materials including warm-up exercises and group activities.', createdAt: '2026-03-12T08:00:00Z', updatedAt: '2026-03-12T12:00:00Z', createdBy: 'user_003', theme: 'sunset', tags: ['workshop', 'creative', 'exercise'], starred: false, status: 'draft', slideCount: 5, shareSettings: { visibility: 'team', allowComments: true, allowEditing: true, shareLink: '', embedLink: '', sharedWith: ['user_002', 'user_003'] } }
];

// ============================================================
// Templates
// ============================================================
const TEMPLATES = [
    { id: 'tmpl_001', name: 'Title Slide', category: 'basic', layout: 'title', description: 'Large centered title with subtitle', previewColor: '#7B61FF',
        elements: [
            { type: 'text', x: 80, y: 180, width: 800, height: 70, content: 'Presentation Title', style: { fontFamily: 'Inter', fontSize: 48, fontWeight: 'bold', color: '#ffffff', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -1, listType: 'none' } },
            { type: 'text', x: 180, y: 270, width: 600, height: 40, content: 'Subtitle or author name', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#cccccc', textAlign: 'center', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_002', name: 'Title + Content', category: 'basic', layout: 'title-content', description: 'Header with bullet point content area', previewColor: '#0D99FF',
        elements: [
            { type: 'text', x: 60, y: 40, width: 840, height: 50, content: 'Slide Title', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } },
            { type: 'text', x: 60, y: 120, width: 840, height: 300, content: 'Add your content here\nSecond point\nThird point', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.8, letterSpacing: 0, listType: 'bullet' } }
        ] },
    { id: 'tmpl_003', name: 'Two Column', category: 'basic', layout: 'two-column', description: 'Side-by-side content columns', previewColor: '#14AE5C',
        elements: [
            { type: 'text', x: 60, y: 40, width: 840, height: 50, content: 'Slide Title', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } },
            { type: 'text', x: 60, y: 120, width: 400, height: 300, content: 'Left column content', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.6, letterSpacing: 0, listType: 'none' } },
            { type: 'text', x: 500, y: 120, width: 400, height: 300, content: 'Right column content', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.6, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_004', name: 'Section Header', category: 'basic', layout: 'section-header', description: 'Bold section divider with accent background', previewColor: '#F24822',
        elements: [
            { type: 'text', x: 60, y: 200, width: 840, height: 60, content: 'Section Title', style: { fontFamily: 'Inter', fontSize: 44, fontWeight: 'bold', color: '#ffffff', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: -0.5, listType: 'none' } }
        ] },
    { id: 'tmpl_005', name: 'Blank', category: 'basic', layout: 'blank', description: 'Empty slide for custom content', previewColor: '#ffffff', elements: [] },
    { id: 'tmpl_006', name: 'Image + Text', category: 'basic', layout: 'image-focused', description: 'Large image area with text overlay', previewColor: '#FFC700',
        elements: [
            { type: 'image', x: 0, y: 0, width: 480, height: 540, imagePlaceholder: '#e0e0e0' },
            { type: 'text', x: 520, y: 40, width: 400, height: 50, content: 'Image Title', style: { fontFamily: 'Inter', fontSize: 28, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } },
            { type: 'text', x: 520, y: 110, width: 400, height: 300, content: 'Describe the image or add context here.', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: '#444444', textAlign: 'left', italic: false, underline: false, lineHeight: 1.6, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_007', name: 'Big Number', category: 'business', layout: 'title-content', description: 'Highlight a key metric or statistic', previewColor: '#9747FF',
        elements: [
            { type: 'text', x: 60, y: 60, width: 840, height: 30, content: 'KEY METRIC', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#888888', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 2, listType: 'none' } },
            { type: 'text', x: 60, y: 140, width: 840, height: 100, content: '42%', style: { fontFamily: 'Inter', fontSize: 96, fontWeight: 'bold', color: '#7B61FF', textAlign: 'center', italic: false, underline: false, lineHeight: 1.0, letterSpacing: -2, listType: 'none' } },
            { type: 'text', x: 160, y: 280, width: 640, height: 40, content: 'Description of what this number means', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'normal', color: '#666666', textAlign: 'center', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_008', name: 'Comparison', category: 'business', layout: 'two-column', description: 'Side-by-side comparison layout', previewColor: '#FF7262',
        elements: [
            { type: 'text', x: 60, y: 40, width: 840, height: 50, content: 'Before vs After', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 60, y: 110, width: 400, height: 350, shapeType: 'rectangle', fill: '#fff0f0', stroke: '#ffcccc', strokeWidth: 1, cornerRadius: 12 },
            { type: 'text', x: 80, y: 125, width: 360, height: 30, content: 'Before', style: { fontFamily: 'Inter', fontSize: 22, fontWeight: 'bold', color: '#F24822', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 500, y: 110, width: 400, height: 350, shapeType: 'rectangle', fill: '#f0fff4', stroke: '#b8e6c8', strokeWidth: 1, cornerRadius: 12 },
            { type: 'text', x: 520, y: 125, width: 360, height: 30, content: 'After', style: { fontFamily: 'Inter', fontSize: 22, fontWeight: 'bold', color: '#14AE5C', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_009', name: 'Three Cards', category: 'business', layout: 'title-content', description: 'Three cards in a row for features or highlights', previewColor: '#0D99FF',
        elements: [
            { type: 'text', x: 60, y: 40, width: 840, height: 50, content: 'Three Key Points', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 60, y: 120, width: 260, height: 300, shapeType: 'rectangle', fill: '#f5f5ff', stroke: '#e0e0f0', strokeWidth: 1, cornerRadius: 12 },
            { type: 'text', x: 80, y: 140, width: 220, height: 30, content: 'Point One', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 350, y: 120, width: 260, height: 300, shapeType: 'rectangle', fill: '#f5f5ff', stroke: '#e0e0f0', strokeWidth: 1, cornerRadius: 12 },
            { type: 'text', x: 370, y: 140, width: 220, height: 30, content: 'Point Two', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 640, y: 120, width: 260, height: 300, shapeType: 'rectangle', fill: '#f5f5ff', stroke: '#e0e0f0', strokeWidth: 1, cornerRadius: 12 },
            { type: 'text', x: 660, y: 140, width: 220, height: 30, content: 'Point Three', style: { fontFamily: 'Inter', fontSize: 20, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_010', name: 'Quote', category: 'creative', layout: 'title', description: 'Large quote with attribution', previewColor: '#1a1a2e',
        elements: [
            { type: 'text', x: 100, y: 120, width: 760, height: 200, content: '"Design is not just what it looks like and feels like. Design is how it works."', style: { fontFamily: 'Playfair Display', fontSize: 36, fontWeight: 'normal', color: '#ffffff', textAlign: 'center', italic: true, underline: false, lineHeight: 1.5, letterSpacing: 0, listType: 'none' } },
            { type: 'text', x: 200, y: 360, width: 560, height: 30, content: '— Steve Jobs', style: { fontFamily: 'Inter', fontSize: 18, fontWeight: 'normal', color: '#aaaaaa', textAlign: 'center', italic: false, underline: false, lineHeight: 1.4, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_011', name: 'Timeline', category: 'business', layout: 'title-content', description: 'Horizontal timeline for milestones', previewColor: '#40916C',
        elements: [
            { type: 'text', x: 60, y: 40, width: 840, height: 50, content: 'Project Timeline', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'left', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 60, y: 250, width: 840, height: 4, shapeType: 'line', fill: '#7B61FF', stroke: '#7B61FF', strokeWidth: 3 },
            { type: 'shape', x: 120, y: 238, width: 24, height: 24, shapeType: 'circle', fill: '#7B61FF', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 80, y: 270, width: 100, height: 20, content: 'Phase 1', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: '600', color: '#7B61FF', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 360, y: 238, width: 24, height: 24, shapeType: 'circle', fill: '#7B61FF', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 320, y: 270, width: 100, height: 20, content: 'Phase 2', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: '600', color: '#7B61FF', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 600, y: 238, width: 24, height: 24, shapeType: 'circle', fill: '#7B61FF', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 560, y: 270, width: 100, height: 20, content: 'Phase 3', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: '600', color: '#7B61FF', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 840, y: 238, width: 24, height: 24, shapeType: 'circle', fill: '#cccccc', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 800, y: 270, width: 100, height: 20, content: 'Launch', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: '600', color: '#999999', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }
        ] },
    { id: 'tmpl_012', name: 'Team Intro', category: 'creative', layout: 'title-content', description: 'Team member grid with avatars', previewColor: '#FF8577',
        elements: [
            { type: 'text', x: 60, y: 40, width: 840, height: 50, content: 'Meet the Team', style: { fontFamily: 'Inter', fontSize: 32, fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.2, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 120, y: 130, width: 80, height: 80, shapeType: 'circle', fill: '#7B61FF', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 80, y: 220, width: 160, height: 20, content: 'Name', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'text', x: 80, y: 245, width: 160, height: 20, content: 'Role', style: { fontFamily: 'Inter', fontSize: 14, fontWeight: 'normal', color: '#888888', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 360, y: 130, width: 80, height: 80, shapeType: 'circle', fill: '#0D99FF', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 320, y: 220, width: 160, height: 20, content: 'Name', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 600, y: 130, width: 80, height: 80, shapeType: 'circle', fill: '#14AE5C', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 560, y: 220, width: 160, height: 20, content: 'Name', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } },
            { type: 'shape', x: 840, y: 130, width: 80, height: 80, shapeType: 'circle', fill: '#FFC700', stroke: 'none', strokeWidth: 0 },
            { type: 'text', x: 800, y: 220, width: 160, height: 20, content: 'Name', style: { fontFamily: 'Inter', fontSize: 16, fontWeight: '600', color: '#1a1a2e', textAlign: 'center', italic: false, underline: false, lineHeight: 1.3, letterSpacing: 0, listType: 'none' } }
        ] }
];

// ============================================================
// Comments
// ============================================================
const COMMENTS = [
    { id: 'cmt_001', presentationId: 'pres_001', slideId: 'slide_001_02', elementId: null, authorId: 'user_002', content: 'Should we add a chart visualization for the launch impact metrics?', createdAt: '2026-03-15T10:30:00Z', resolved: false, replies: [
        { id: 'reply_001', authorId: 'user_001', content: 'Good idea! Let me add a bar chart for the user growth.', createdAt: '2026-03-15T10:45:00Z' },
        { id: 'reply_002', authorId: 'user_002', content: 'Maybe a line chart would better show the trend over time.', createdAt: '2026-03-15T11:00:00Z' }
    ]},
    { id: 'cmt_002', presentationId: 'pres_001', slideId: 'slide_001_03', elementId: null, authorId: 'user_003', content: 'The DAU number is slightly outdated. Latest from analytics is 852K.', createdAt: '2026-03-15T14:00:00Z', resolved: false, replies: [
        { id: 'reply_003', authorId: 'user_001', content: 'Updated! Thanks for catching that.', createdAt: '2026-03-15T14:15:00Z' }
    ]},
    { id: 'cmt_003', presentationId: 'pres_001', slideId: 'slide_001_08', elementId: null, authorId: 'user_004', content: 'Can we add estimated timelines for each initiative card?', createdAt: '2026-03-14T16:20:00Z', resolved: true, replies: [
        { id: 'reply_004', authorId: 'user_001', content: 'Added in slide 11 (Timeline & Resources). Let me know if you want them on this slide too.', createdAt: '2026-03-14T16:40:00Z' }
    ]},
    { id: 'cmt_004', presentationId: 'pres_001', slideId: 'slide_001_11', elementId: null, authorId: 'user_006', content: 'The competitive risk section could be more specific about Canva\'s AI features.', createdAt: '2026-03-13T09:00:00Z', resolved: false, replies: []},
    { id: 'cmt_005', presentationId: 'pres_001', slideId: 'slide_001_14', elementId: null, authorId: 'user_005', content: 'Love the design! Very clean and professional.', createdAt: '2026-03-15T15:00:00Z', resolved: false, replies: []},
    { id: 'cmt_006', presentationId: 'pres_002', slideId: 'slide_002_03', elementId: null, authorId: 'user_001', content: 'The logo clear space guidelines need to match the updated logo dimensions from the rebrand.', createdAt: '2026-03-10T11:00:00Z', resolved: false, replies: [
        { id: 'reply_005', authorId: 'user_006', content: 'Will update. The new logo is 15% wider so clear space needs adjustment.', createdAt: '2026-03-10T11:30:00Z' }
    ]},
    { id: 'cmt_007', presentationId: 'pres_002', slideId: 'slide_002_05', elementId: null, authorId: 'user_008', content: 'The secondary color palette swatches look off on my screen. Can we add hex codes below each swatch?', createdAt: '2026-03-11T14:00:00Z', resolved: true, replies: [
        { id: 'reply_006', authorId: 'user_006', content: 'Done! Added hex and RGB values below each color swatch.', createdAt: '2026-03-11T15:00:00Z' }
    ]},
    { id: 'cmt_008', presentationId: 'pres_002', slideId: 'slide_002_07', elementId: null, authorId: 'user_003', content: 'We should mention the fallback fonts for web and email contexts.', createdAt: '2026-03-08T09:30:00Z', resolved: false, replies: []},
    { id: 'cmt_009', presentationId: 'pres_003', slideId: 'slide_003_04', elementId: null, authorId: 'user_001', content: 'Finance team confirmed these are the final Q1 numbers. Good to go.', createdAt: '2026-03-16T18:00:00Z', resolved: true, replies: []},
    { id: 'cmt_010', presentationId: 'pres_003', slideId: 'slide_003_10', elementId: null, authorId: 'user_001', content: 'Board wants to see more detail on the use of funds breakdown. Can we add a pie chart?', createdAt: '2026-03-16T19:00:00Z', resolved: false, replies: []},
    { id: 'cmt_011', presentationId: 'pres_004', slideId: 'slide_004_03', elementId: null, authorId: 'user_001', content: 'The navigation finding is really compelling. Can we include a short video clip from the session?', createdAt: '2026-03-08T10:00:00Z', resolved: false, replies: [
        { id: 'reply_007', authorId: 'user_003', content: 'I have clips from P07 and P15. Will add the most impactful one.', createdAt: '2026-03-08T10:20:00Z' }
    ]},
    { id: 'cmt_012', presentationId: 'pres_004', slideId: 'slide_004_07', elementId: null, authorId: 'user_002', content: 'The task success rates for "Adjust permissions" (38%) is alarming. We should prioritize this.', createdAt: '2026-03-07T14:00:00Z', resolved: false, replies: [
        { id: 'reply_008', authorId: 'user_003', content: 'Agreed. It\'s in the P2 recommendations. Should we bump it to P1?', createdAt: '2026-03-07T14:30:00Z' },
        { id: 'reply_009', authorId: 'user_002', content: 'Yes, let\'s discuss in the next sprint planning.', createdAt: '2026-03-07T14:45:00Z' }
    ]},
    { id: 'cmt_013', presentationId: 'pres_004', slideId: 'slide_004_11', elementId: null, authorId: 'user_006', content: 'The priority recommendations look solid. Agree with the effort/impact assessment.', createdAt: '2026-03-08T16:00:00Z', resolved: false, replies: []},
    { id: 'cmt_014', presentationId: 'pres_006', slideId: 'slide_006_01', elementId: null, authorId: 'user_008', content: 'The CEO welcome slide should mention the recent product awards.', createdAt: '2026-03-14T20:00:00Z', resolved: false, replies: []},
    { id: 'cmt_015', presentationId: 'pres_006', slideId: 'slide_006_03', elementId: null, authorId: 'user_007', content: 'Headcount numbers are correct. I verified with the HR system this morning.', createdAt: '2026-03-14T21:00:00Z', resolved: true, replies: []},
    { id: 'cmt_016', presentationId: 'pres_006', slideId: 'slide_006_17', elementId: null, authorId: 'user_003', content: 'The DEI numbers are great progress! Can we add a year-over-year comparison?', createdAt: '2026-03-14T21:30:00Z', resolved: false, replies: [
        { id: 'reply_010', authorId: 'user_007', content: 'Good idea. I\'ll pull the 2025 numbers for comparison.', createdAt: '2026-03-14T22:00:00Z' }
    ]},
    { id: 'cmt_017', presentationId: 'pres_007', slideId: 'slide_007_12', elementId: null, authorId: 'user_003', content: 'The $84K budget seems low for a 9-week project. Should we pad for contingency?', createdAt: '2026-03-13T15:00:00Z', resolved: false, replies: [
        { id: 'reply_011', authorId: 'user_001', content: 'It includes our standard 10% contingency buffer. We can discuss if more is needed.', createdAt: '2026-03-13T15:30:00Z' }
    ]},
    { id: 'cmt_018', presentationId: 'pres_008', slideId: 'slide_008_02', elementId: null, authorId: 'user_004', content: 'Great sprint! The mobile nav redesign is looking really polished.', createdAt: '2026-03-14T17:00:00Z', resolved: false, replies: []},
    { id: 'cmt_019', presentationId: 'pres_010', slideId: 'slide_010_08', elementId: null, authorId: 'user_001', content: 'The $280K paid budget needs CFO approval. Have we submitted the request?', createdAt: '2026-03-17T10:00:00Z', resolved: false, replies: [
        { id: 'reply_012', authorId: 'user_008', content: 'Submitted yesterday. Expecting approval by end of week.', createdAt: '2026-03-17T10:30:00Z' }
    ]},
    { id: 'cmt_020', presentationId: 'pres_010', slideId: 'slide_010_04', elementId: null, authorId: 'user_002', content: 'The hero visual concept sounds great. Can we see some initial sketches?', createdAt: '2026-03-17T11:00:00Z', resolved: false, replies: []},
    { id: 'cmt_021', presentationId: 'pres_011', slideId: 'slide_011_04', elementId: null, authorId: 'user_004', content: 'I\'ll take ownership of fixing the focus trap issue in modals. Should be a quick fix.', createdAt: '2026-03-05T10:00:00Z', resolved: true, replies: [
        { id: 'reply_013', authorId: 'user_003', content: 'Thanks James! That\'s one of the critical WCAG A issues.', createdAt: '2026-03-05T10:15:00Z' }
    ]},
    { id: 'cmt_022', presentationId: 'pres_012', slideId: 'slide_012_07', elementId: null, authorId: 'user_001', content: 'SMB churn at 3.8% is concerning. Do we have a retention initiative planned?', createdAt: '2026-01-25T15:00:00Z', resolved: false, replies: [
        { id: 'reply_014', authorId: 'user_005', content: 'Yes, the product team is working on better onboarding for SMB accounts. Should help.', createdAt: '2026-01-25T15:30:00Z' }
    ]},
    { id: 'cmt_023', presentationId: 'pres_013', slideId: 'slide_013_02', elementId: null, authorId: 'user_002', content: 'Should we add dark mode token examples alongside each color token?', createdAt: '2026-03-11T14:00:00Z', resolved: false, replies: [
        { id: 'reply_015', authorId: 'user_006', content: 'Great idea. I\'ll add a dark mode column to each token table.', createdAt: '2026-03-11T14:30:00Z' }
    ]},
    { id: 'cmt_024', presentationId: 'pres_014', slideId: 'slide_014_03', elementId: null, authorId: 'user_008', content: 'Can we assign owners to each action item and add a due date?', createdAt: '2026-03-14T16:00:00Z', resolved: true, replies: [
        { id: 'reply_016', authorId: 'user_002', content: 'Updated with owners. Due dates tracked in Linear.', createdAt: '2026-03-14T16:20:00Z' }
    ]},
    { id: 'cmt_025', presentationId: 'pres_015', slideId: 'slide_015_02', elementId: null, authorId: 'user_001', content: 'Make sure the SSO demo uses a test Okta environment, not production.', createdAt: '2026-03-16T09:00:00Z', resolved: true, replies: [
        { id: 'reply_017', authorId: 'user_004', content: 'Using the demo.okta.designco.io environment. All set.', createdAt: '2026-03-16T09:15:00Z' }
    ]},
    { id: 'cmt_026', presentationId: 'pres_016', slideId: 'slide_016_12', elementId: null, authorId: 'user_006', content: 'Budget breakdown looks good. The design allocation might be tight for 3 visual directions though.', createdAt: '2026-03-15T09:00:00Z', resolved: false, replies: []},
    { id: 'cmt_027', presentationId: 'pres_016', slideId: 'slide_016_06', elementId: null, authorId: 'user_003', content: 'I like the gradient direction. Can we mock up a few hero section options?', createdAt: '2026-03-15T09:30:00Z', resolved: false, replies: [
        { id: 'reply_018', authorId: 'user_004', content: 'Will have 3 hero concepts ready by Monday.', createdAt: '2026-03-15T10:00:00Z' }
    ]},
    { id: 'cmt_028', presentationId: 'pres_018', slideId: 'slide_018_01', elementId: null, authorId: 'user_002', content: 'Should we add an icebreaker before the Crazy 8s exercise?', createdAt: '2026-03-12T10:00:00Z', resolved: false, replies: [
        { id: 'reply_019', authorId: 'user_003', content: 'Good call. Maybe a quick "Two truths and a lie" to warm up the group.', createdAt: '2026-03-12T10:15:00Z' }
    ]},
    { id: 'cmt_029', presentationId: 'pres_001', slideId: 'slide_001_09', elementId: null, authorId: 'user_008', content: 'The AI design assistant timeline seems aggressive. Can we add a contingency buffer?', createdAt: '2026-03-14T12:00:00Z', resolved: false, replies: [
        { id: 'reply_020', authorId: 'user_001', content: 'Good point. I\'ll add a note about the alpha being internal-only to reduce scope pressure.', createdAt: '2026-03-14T12:30:00Z' }
    ]},
    { id: 'cmt_030', presentationId: 'pres_002', slideId: 'slide_002_11', elementId: null, authorId: 'user_002', content: 'The illustration style guide needs examples of our character set in different contexts.', createdAt: '2026-03-12T13:00:00Z', resolved: false, replies: []},
    { id: 'cmt_031', presentationId: 'pres_006', slideId: 'slide_006_12', elementId: null, authorId: 'user_005', content: 'Revenue numbers confirmed accurate. Finance team signed off.', createdAt: '2026-03-14T18:00:00Z', resolved: true, replies: []},
    { id: 'cmt_032', presentationId: 'pres_006', slideId: 'slide_006_08', elementId: null, authorId: 'user_004', content: 'The product roadmap slide should reference the separate deep-dive deck (pres_001).', createdAt: '2026-03-14T19:00:00Z', resolved: false, replies: [
        { id: 'reply_021', authorId: 'user_001', content: 'Will add a "See detailed roadmap deck" link.', createdAt: '2026-03-14T19:20:00Z' }
    ]},
    { id: 'cmt_033', presentationId: 'pres_009', slideId: 'slide_009_04', elementId: null, authorId: 'user_008', content: 'The "30 days" plan should mention the buddy program more explicitly.', createdAt: '2026-03-10T09:00:00Z', resolved: false, replies: []},
    { id: 'cmt_034', presentationId: 'pres_013', slideId: 'slide_013_09', elementId: null, authorId: 'user_001', content: 'The button variants look great. Can we add a "ghost" button variant?', createdAt: '2026-03-11T15:00:00Z', resolved: false, replies: [
        { id: 'reply_022', authorId: 'user_006', content: 'Added to the backlog. Will include in v3.3 update.', createdAt: '2026-03-11T15:20:00Z' }
    ]},
    { id: 'cmt_035', presentationId: 'pres_003', slideId: 'slide_003_06', elementId: null, authorId: 'user_001', content: 'Legal reviewed the competitive landscape claims. All good. No defamation risks.', createdAt: '2026-03-16T17:00:00Z', resolved: true, replies: []},
    { id: 'cmt_036', presentationId: 'pres_007', slideId: 'slide_007_03', elementId: null, authorId: 'user_008', content: 'Should we include Elena on the team slide? She could handle the animation work.', createdAt: '2026-03-13T16:00:00Z', resolved: false, replies: [
        { id: 'reply_023', authorId: 'user_001', content: 'Let me check her availability with PM. Will update by tomorrow.', createdAt: '2026-03-13T16:15:00Z' }
    ]},
    { id: 'cmt_037', presentationId: 'pres_004', slideId: 'slide_004_12', elementId: null, authorId: 'user_004', content: 'The design principles update is excellent. "Performance is a feature" resonates.', createdAt: '2026-03-08T11:00:00Z', resolved: false, replies: []},
    { id: 'cmt_038', presentationId: 'pres_010', slideId: 'slide_010_10', elementId: null, authorId: 'user_001', content: 'KPIs look right. Make sure we have dashboards set up before launch.', createdAt: '2026-03-17T12:00:00Z', resolved: false, replies: [
        { id: 'reply_024', authorId: 'user_008', content: 'Analytics dashboards are ready. Shared access with the team.', createdAt: '2026-03-17T12:30:00Z' }
    ]},
    { id: 'cmt_039', presentationId: 'pres_012', slideId: 'slide_012_01', elementId: null, authorId: 'user_005', content: 'Updated revenue number from $11.6M to $11.8M after final audit adjustments.', createdAt: '2026-01-24T16:00:00Z', resolved: true, replies: []},
    { id: 'cmt_040', presentationId: 'pres_005', slideId: 'slide_005_05', elementId: null, authorId: 'user_004', content: 'The database architecture diagram should be updated to show the new read replica in APAC.', createdAt: '2026-03-01T08:00:00Z', resolved: false, replies: []}
];

// ============================================================
// Aggregate seed data
// ============================================================
function getSeedData() {
    return {
        presentations: JSON.parse(JSON.stringify(PRESENTATIONS)),
        slides: JSON.parse(JSON.stringify(ALL_SLIDES)),
        templates: JSON.parse(JSON.stringify(TEMPLATES)),
        comments: JSON.parse(JSON.stringify(COMMENTS)),
        users: JSON.parse(JSON.stringify(USERS)),
        currentUserId: 'user_001',
        _nextPresentationId: 19,
        _nextSlideId: 500,
        _nextElementId: _elemCounter + 1,
        _nextCommentId: 41,
        _nextReplyId: 25,
        _nextTemplateId: 13,
        _seedVersion: SEED_DATA_VERSION
    };
}
