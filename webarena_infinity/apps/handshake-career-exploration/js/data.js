const SEED_DATA_VERSION = 1;

// ============================================================
// Current User (Student)
// ============================================================
const CURRENT_USER = {
    id: 'stu_8f3a2c81',
    firstName: 'Maya',
    lastName: 'Chen',
    fullName: 'Maya Chen',
    email: 'maya.chen@stanford.edu',
    school: 'Stanford University',
    major: 'Computer Science',
    minor: 'Business Administration',
    graduationYear: 2027,
    expectedGraduation: 'May 2027',
    gpa: 3.82,
    profileVisibility: 'Community',
    avatarColor: '#4A90D9',
    bio: 'CS student passionate about AI/ML and product design. Looking for summer 2026 internship opportunities in tech.',
    phone: '(650) 555-0142',
    location: 'Stanford, CA',
    linkedinUrl: 'linkedin.com/in/mayachen',
    websiteUrl: 'mayachen.dev',
    createdAt: '2024-09-01T08:00:00Z',
    updatedAt: '2026-03-05T14:30:00Z',
    careerInterests: {
        jobTypes: ['Internship', 'Part-time'],
        helpWith: ['Internship', 'Events', 'Network'],
        postGraduation: ['Working', 'Grad school'],
        roles: ['Software Engineer', 'Product Manager', 'Data Scientist', 'UX Designer'],
        locations: ['San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX', 'Remote'],
        careerCommunity: 'Technology',
        industries: ['Technology', 'Artificial Intelligence', 'Finance', 'Healthcare Technology'],
        jobFunctions: ['Engineering', 'Product Management', 'Data Analytics', 'Design'],
        expectedGraduationDate: 'May 2027'
    },
    lookingFor: 'Internship',
    skills: ['Python', 'JavaScript', 'React', 'Machine Learning', 'SQL', 'Figma', 'Product Strategy'],
    workExperience: [
        { id: 'exp_01', title: 'Software Engineering Intern', company: 'Meta', startDate: '2025-06-01', endDate: '2025-08-31', description: 'Built ML pipeline for content recommendations' },
        { id: 'exp_02', title: 'Research Assistant', company: 'Stanford AI Lab', startDate: '2025-01-15', endDate: null, description: 'NLP research under Prof. Manning' },
        { id: 'exp_03', title: 'Product Design Intern', company: 'Figma', startDate: '2024-06-15', endDate: '2024-08-30', description: 'Redesigned plugin marketplace UX' }
    ],
    education: [
        { id: 'edu_01', school: 'Stanford University', degree: 'B.S.', major: 'Computer Science', minor: 'Business Administration', startYear: 2023, endYear: 2027 }
    ],
    organizations: ['Stanford Women in Tech', 'ACM Student Chapter', 'Entrepreneurship Club'],
    followedEmployerIds: ['emp_01', 'emp_03', 'emp_05', 'emp_07', 'emp_10', 'emp_12', 'emp_15'],
    savedPostIds: ['post_02', 'post_08', 'post_14'],
    savedJobIds: ['job_03', 'job_07', 'job_12', 'job_18', 'job_24']
};

// ============================================================
// Career Interest Options
// ============================================================
const JOB_TYPE_OPTIONS = ['Full-time', 'Internship', 'Part-time', 'On-campus'];
const HELP_WITH_OPTIONS = ['Job', 'Internship', 'Grad school', 'Events', 'Network', 'Exploring'];
const POST_GRADUATION_OPTIONS = ['Working', 'Grad school', 'Gap year', 'Military', 'Volunteering', 'Fellowship', 'Not sure'];
const CAREER_COMMUNITY_OPTIONS = ['Technology', 'Business & Finance', 'Healthcare', 'Education', 'Creative Arts', 'Government & Policy', 'Science & Research', 'Nonprofit & Social Impact', 'Law', 'Engineering'];

const INDUSTRY_OPTIONS = [
    'Technology', 'Artificial Intelligence', 'Finance', 'Healthcare Technology',
    'Consulting', 'Education', 'E-Commerce', 'Cybersecurity', 'Biotechnology',
    'Media & Entertainment', 'Real Estate', 'Energy', 'Manufacturing',
    'Telecommunications', 'Automotive', 'Aerospace', 'Insurance',
    'Government', 'Nonprofit', 'Legal Services', 'Retail',
    'Agriculture', 'Transportation', 'Hospitality'
];

const JOB_FUNCTION_OPTIONS = [
    'Engineering', 'Product Management', 'Data Analytics', 'Design',
    'Marketing', 'Sales', 'Finance & Accounting', 'Human Resources',
    'Operations', 'Research', 'Legal', 'Customer Success',
    'Business Development', 'Content & Communications', 'IT & Infrastructure',
    'Quality Assurance', 'Supply Chain', 'Administrative'
];

const ROLE_OPTIONS = [
    'Software Engineer', 'Product Manager', 'Data Scientist', 'UX Designer',
    'Frontend Developer', 'Backend Developer', 'Full-Stack Developer',
    'Machine Learning Engineer', 'DevOps Engineer', 'Mobile Developer',
    'UI Designer', 'UX Researcher', 'Business Analyst', 'Financial Analyst',
    'Marketing Coordinator', 'Sales Associate', 'Account Manager',
    'Project Manager', 'Consultant', 'Data Engineer', 'Cloud Engineer',
    'Security Engineer', 'Technical Writer', 'QA Engineer',
    'Solutions Architect', 'Research Scientist'
];

const LOCATION_OPTIONS = [
    'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
    'Los Angeles, CA', 'Chicago, IL', 'Boston, MA', 'Denver, CO',
    'Atlanta, GA', 'Miami, FL', 'Portland, OR', 'Washington, DC',
    'San Jose, CA', 'Raleigh, NC', 'Minneapolis, MN', 'Remote',
    'Nashville, TN', 'Salt Lake City, UT', 'Phoenix, AZ', 'Philadelphia, PA'
];

const GRADUATION_DATE_OPTIONS = [
    'December 2025', 'May 2026', 'August 2026', 'December 2026',
    'May 2027', 'August 2027', 'December 2027', 'May 2028'
];

// ============================================================
// Employers
// ============================================================
const EMPLOYERS = [
    {
        id: 'emp_01', name: 'Google', industry: 'Technology', location: 'Mountain View, CA',
        size: '10,000+ employees', type: 'Public', website: 'google.com', isPremium: true,
        logoColor: '#4285F4', followCount: 45200,
        about: 'Google LLC is an American multinational technology company focusing on artificial intelligence, online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, and consumer electronics.',
        workLife: 'Flexible work arrangements, comprehensive health benefits, free meals, on-site fitness centers, generous PTO, 401(k) matching, parental leave, education reimbursement.',
        testimonials: [
            { name: 'Sarah Kim', role: 'Software Engineer', school: 'MIT', major: 'Computer Science', gradYear: 2024, text: 'The mentorship and learning opportunities at Google are unmatched. I grew more in my first year than I expected.' },
            { name: 'James Park', role: 'Product Manager', school: 'Stanford University', major: 'Management Science', gradYear: 2023, text: 'Amazing culture of innovation. Every day brings new challenges and the team support is incredible.' }
        ],
        gallery: ['office-campus.jpg', 'team-event.jpg', 'hackathon.jpg'],
        affiliatedEmployers: ['Alphabet Inc.', 'YouTube', 'DeepMind', 'Waymo']
    },
    {
        id: 'emp_02', name: 'JPMorgan Chase', industry: 'Finance', location: 'New York, NY',
        size: '10,000+ employees', type: 'Public', website: 'jpmorgan.com', isPremium: true,
        logoColor: '#003A70', followCount: 32100,
        about: 'JPMorgan Chase & Co. is an American multinational investment bank and financial services holding company. It is the largest bank in the US and the world\'s most valuable bank by market cap.',
        workLife: 'Competitive compensation, comprehensive benefits, career development programs, diverse and inclusive workplace, hybrid work model.',
        testimonials: [
            { name: 'Priya Sharma', role: 'Analyst', school: 'Wharton School', major: 'Finance', gradYear: 2025, text: 'Incredible learning curve in investment banking. The training program is world-class.' }
        ],
        gallery: ['nyc-office.jpg', 'trading-floor.jpg'],
        affiliatedEmployers: ['Chase Bank', 'J.P. Morgan Asset Management']
    },
    {
        id: 'emp_03', name: 'Microsoft', industry: 'Technology', location: 'Redmond, WA',
        size: '10,000+ employees', type: 'Public', website: 'microsoft.com', isPremium: true,
        logoColor: '#00A4EF', followCount: 41800,
        about: 'Microsoft Corporation is an American multinational technology corporation which produces computer software, consumer electronics, personal computers, and related services.',
        workLife: 'Hybrid work flexibility, health & wellness programs, stock purchase plan, tuition reimbursement, family benefits.',
        testimonials: [
            { name: 'Alex Rivera', role: 'Software Engineer', school: 'Carnegie Mellon', major: 'Computer Science', gradYear: 2024, text: 'Working on Azure has been transformative for my cloud engineering career.' }
        ],
        gallery: ['redmond-campus.jpg', 'team-collab.jpg'],
        affiliatedEmployers: ['LinkedIn', 'GitHub', 'Xbox']
    },
    {
        id: 'emp_04', name: 'McKinsey & Company', industry: 'Consulting', location: 'New York, NY',
        size: '5,001-10,000 employees', type: 'Private', website: 'mckinsey.com', isPremium: true,
        logoColor: '#003C71', followCount: 28700,
        about: 'McKinsey & Company is a global management consulting firm that serves as a trusted advisor to the world\'s leading businesses, governments, and institutions.',
        workLife: 'Competitive pay, extensive travel, accelerated career growth, knowledge-sharing culture, professional development.',
        testimonials: [],
        gallery: ['office-modern.jpg'],
        affiliatedEmployers: ['McKinsey Digital', 'McKinsey Solutions']
    },
    {
        id: 'emp_05', name: 'Apple', industry: 'Technology', location: 'Cupertino, CA',
        size: '10,000+ employees', type: 'Public', website: 'apple.com', isPremium: true,
        logoColor: '#000000', followCount: 52300,
        about: 'Apple Inc. is an American multinational technology company that designs, develops, and sells consumer electronics, computer software, and online services.',
        workLife: 'Product discounts, health benefits, onsite wellness center, stock purchase plan, education reimbursement.',
        testimonials: [
            { name: 'Emily Zhang', role: 'Hardware Engineer', school: 'Stanford University', major: 'Electrical Engineering', gradYear: 2025, text: 'Being part of the team that designs products used by billions is incredibly fulfilling.' }
        ],
        gallery: ['apple-park.jpg', 'product-lab.jpg'],
        affiliatedEmployers: ['Apple Services', 'Apple Retail']
    },
    {
        id: 'emp_06', name: 'Goldman Sachs', industry: 'Finance', location: 'New York, NY',
        size: '10,000+ employees', type: 'Public', website: 'goldmansachs.com', isPremium: true,
        logoColor: '#7399C6', followCount: 29500,
        about: 'The Goldman Sachs Group, Inc. is an American multinational investment banking company providing financial services.',
        workLife: 'Competitive compensation, wellness programs, professional development, networking events.',
        testimonials: [],
        gallery: ['gs-hq.jpg'],
        affiliatedEmployers: ['Marcus by Goldman Sachs', 'Goldman Sachs Asset Management']
    },
    {
        id: 'emp_07', name: 'Meta', industry: 'Technology', location: 'Menlo Park, CA',
        size: '10,000+ employees', type: 'Public', website: 'meta.com', isPremium: true,
        logoColor: '#0668E1', followCount: 38900,
        about: 'Meta Platforms, Inc. builds technologies that help people connect, find communities, and grow businesses.',
        workLife: 'Open office culture, free meals, fitness centers, generous PTO, remote work options, family benefits.',
        testimonials: [
            { name: 'David Lee', role: 'ML Engineer', school: 'UC Berkeley', major: 'EECS', gradYear: 2024, text: 'The scale of problems we solve here in AI is unparalleled. Great peer group too.' }
        ],
        gallery: ['menlo-campus.jpg', 'vr-lab.jpg'],
        affiliatedEmployers: ['Instagram', 'WhatsApp', 'Oculus']
    },
    {
        id: 'emp_08', name: 'Deloitte', industry: 'Consulting', location: 'New York, NY',
        size: '10,000+ employees', type: 'Private', website: 'deloitte.com', isPremium: false,
        logoColor: '#86BC25', followCount: 25400,
        about: 'Deloitte provides audit & assurance, consulting, financial advisory, risk advisory, tax, and related services.',
        workLife: 'Flexible work, professional development, diverse project exposure, mentoring programs.',
        testimonials: [],
        gallery: [],
        affiliatedEmployers: ['Deloitte Digital', 'Deloitte Consulting']
    },
    {
        id: 'emp_09', name: 'Amazon', industry: 'Technology', location: 'Seattle, WA',
        size: '10,000+ employees', type: 'Public', website: 'amazon.com', isPremium: true,
        logoColor: '#FF9900', followCount: 47600,
        about: 'Amazon.com, Inc. is an American multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence.',
        workLife: 'Day-one benefits, career growth paths, employee resource groups, relocation support.',
        testimonials: [
            { name: 'Rachel Torres', role: 'SDE', school: 'Georgia Tech', major: 'Computer Science', gradYear: 2025, text: 'Ownership culture is real here. As an intern I shipped features to millions of users.' }
        ],
        gallery: ['seattle-spheres.jpg', 'fulfillment.jpg'],
        affiliatedEmployers: ['AWS', 'Twitch', 'Whole Foods']
    },
    {
        id: 'emp_10', name: 'Stripe', industry: 'Technology', location: 'San Francisco, CA',
        size: '1,001-5,000 employees', type: 'Private', website: 'stripe.com', isPremium: false,
        logoColor: '#635BFF', followCount: 18200,
        about: 'Stripe is a financial infrastructure platform for businesses. Millions of companies use Stripe to accept payments, grow their revenue, and accelerate new business opportunities.',
        workLife: 'Remote-first, competitive equity, health benefits, learning & development budget.',
        testimonials: [
            { name: 'Marcus Johnson', role: 'Backend Engineer', school: 'University of Michigan', major: 'Computer Science', gradYear: 2024, text: 'The code quality bar here is extremely high. I learned more about distributed systems in 6 months than in 4 years of school.' }
        ],
        gallery: ['sf-office.jpg'],
        affiliatedEmployers: ['Stripe Atlas', 'Stripe Press']
    },
    {
        id: 'emp_11', name: 'Bain & Company', industry: 'Consulting', location: 'Boston, MA',
        size: '5,001-10,000 employees', type: 'Private', website: 'bain.com', isPremium: true,
        logoColor: '#CC0000', followCount: 22300,
        about: 'Bain & Company is one of the world\'s leading management consulting firms, advising leaders who want to transform industries and create lasting results.',
        workLife: 'Strong culture, social events, international transfer opportunities, externship program.',
        testimonials: [],
        gallery: ['boston-office.jpg'],
        affiliatedEmployers: ['Bain Capital']
    },
    {
        id: 'emp_12', name: 'Tesla', industry: 'Automotive', location: 'Austin, TX',
        size: '10,000+ employees', type: 'Public', website: 'tesla.com', isPremium: false,
        logoColor: '#CC0000', followCount: 35100,
        about: 'Tesla, Inc. is an American multinational automotive and clean energy company that designs, manufactures, and sells electric vehicles, stationary battery energy storage, solar panels, and related products and services.',
        workLife: 'Mission-driven culture, fast-paced environment, stock options, health benefits.',
        testimonials: [],
        gallery: ['gigafactory.jpg'],
        affiliatedEmployers: ['Tesla Energy', 'Tesla AI']
    },
    {
        id: 'emp_13', name: 'Spotify', industry: 'Media & Entertainment', location: 'New York, NY',
        size: '5,001-10,000 employees', type: 'Public', website: 'spotify.com', isPremium: false,
        logoColor: '#1DB954', followCount: 19800,
        about: 'Spotify is a digital music, podcast, and video service that gives you access to millions of songs and other content from creators all over the world.',
        workLife: 'Work from anywhere program, free Spotify Premium, health & wellness benefits, hack days.',
        testimonials: [],
        gallery: ['nyc-office-spotify.jpg'],
        affiliatedEmployers: ['Spotify for Artists', 'Anchor']
    },
    {
        id: 'emp_14', name: 'Epic Systems', industry: 'Healthcare Technology', location: 'Verona, WI',
        size: '5,001-10,000 employees', type: 'Private', website: 'epic.com', isPremium: false,
        logoColor: '#E44D2E', followCount: 12400,
        about: 'Epic develops software for mid-size and large medical groups, hospitals, and integrated healthcare organizations.',
        workLife: 'Campus with themed buildings, subsidized meals, sabbatical after 5 years, comprehensive training.',
        testimonials: [
            { name: 'Jenna Patel', role: 'Technical Solutions Engineer', school: 'Northwestern', major: 'Biomedical Engineering', gradYear: 2025, text: 'Meaningful work that directly impacts patient care. The campus is also amazing.' }
        ],
        gallery: ['epic-campus.jpg'],
        affiliatedEmployers: []
    },
    {
        id: 'emp_15', name: 'Anthropic', industry: 'Artificial Intelligence', location: 'San Francisco, CA',
        size: '501-1,000 employees', type: 'Private', website: 'anthropic.com', isPremium: true,
        logoColor: '#D4A574', followCount: 15600,
        about: 'Anthropic is an AI safety company building reliable, interpretable, and steerable AI systems.',
        workLife: 'Mission-driven work, competitive compensation, equity, learning-oriented culture, health benefits.',
        testimonials: [
            { name: 'Chris Wu', role: 'Research Engineer', school: 'Stanford University', major: 'Computer Science', gradYear: 2025, text: 'Working on AI safety is the most important problem of our generation. Brilliant colleagues.' }
        ],
        gallery: ['sf-anthropic.jpg'],
        affiliatedEmployers: []
    },
    {
        id: 'emp_16', name: 'Nike', industry: 'Retail', location: 'Beaverton, OR',
        size: '10,000+ employees', type: 'Public', website: 'nike.com', isPremium: false,
        logoColor: '#111111', followCount: 31200,
        about: 'NIKE, Inc. is the world\'s largest supplier of athletic shoes and apparel and a major manufacturer of sports equipment.',
        workLife: 'Product discounts, fitness centers, creative campus environment, diverse culture.',
        testimonials: [],
        gallery: ['nike-campus.jpg'],
        affiliatedEmployers: ['Jordan Brand', 'Converse']
    },
    {
        id: 'emp_17', name: 'Palantir Technologies', industry: 'Technology', location: 'Denver, CO',
        size: '1,001-5,000 employees', type: 'Public', website: 'palantir.com', isPremium: false,
        logoColor: '#101820', followCount: 14300,
        about: 'Palantir Technologies builds the world\'s leading software for data-driven decisions and operations.',
        workLife: 'High-impact projects, competitive compensation, collaborative environment.',
        testimonials: [],
        gallery: [],
        affiliatedEmployers: []
    },
    {
        id: 'emp_18', name: 'Teach For America', industry: 'Nonprofit', location: 'New York, NY',
        size: '1,001-5,000 employees', type: 'Nonprofit', website: 'teachforamerica.org', isPremium: false,
        logoColor: '#E31937', followCount: 8900,
        about: 'Teach For America works to provide an excellent education for all children. Corps members commit to teaching in underserved communities.',
        workLife: 'Mission-driven, transitional living stipend, AmeriCorps education award, alumni network.',
        testimonials: [],
        gallery: [],
        affiliatedEmployers: []
    },
    {
        id: 'emp_19', name: 'Salesforce', industry: 'Technology', location: 'San Francisco, CA',
        size: '10,000+ employees', type: 'Public', website: 'salesforce.com', isPremium: true,
        logoColor: '#00A1E0', followCount: 27600,
        about: 'Salesforce is the #1 CRM, bringing companies and customers together in the digital age.',
        workLife: 'Ohana culture, volunteer time off, wellness reimbursement, equality groups.',
        testimonials: [],
        gallery: ['salesforce-tower.jpg'],
        affiliatedEmployers: ['Slack', 'Tableau', 'MuleSoft']
    },
    {
        id: 'emp_20', name: 'Startup Grind Labs', industry: 'Technology', location: 'Austin, TX',
        size: '11-50 employees', type: 'Private', website: 'startupgrindlabs.com', isPremium: false,
        logoColor: '#FF6B35', followCount: 420,
        about: 'Early-stage startup building AI-powered developer tools. We are a small team with big ambitions.',
        workLife: 'Equity-heavy compensation, fully remote, unlimited PTO, weekly team game nights.',
        testimonials: [],
        gallery: [],
        affiliatedEmployers: []
    }
];

// ============================================================
// Jobs
// ============================================================
const JOBS = [
    { id: 'job_01', employerId: 'emp_01', title: 'Software Engineering Intern, Summer 2026', type: 'Internship', location: 'Mountain View, CA', salary: '$55/hr', postedAt: '2026-02-15T10:00:00Z', deadline: '2026-03-31T23:59:59Z', roles: ['Software Engineer'], labels: ['STEM', 'Top Employer'], status: 'active', description: 'Join Google as a Software Engineering Intern and work on large-scale distributed systems. You\'ll collaborate with a team on a specific project over the 12-week internship.', qualifications: 'Currently pursuing BS/MS in CS or related field. Strong coding skills in one or more of: C++, Java, Python.', applicants: 1842 },
    { id: 'job_02', employerId: 'emp_01', title: 'Associate Product Manager Intern', type: 'Internship', location: 'San Francisco, CA', salary: '$52/hr', postedAt: '2026-02-20T14:00:00Z', deadline: '2026-04-15T23:59:59Z', roles: ['Product Manager'], labels: ['Top Employer'], status: 'active', description: 'Google\'s APM program is a two-year rotational program for new graduates. Interns get a preview of this experience.', qualifications: 'Pursuing BS/MS. Strong analytical and communication skills.', applicants: 2456 },
    { id: 'job_03', employerId: 'emp_02', title: 'Investment Banking Summer Analyst', type: 'Internship', location: 'New York, NY', salary: '$95,000/yr prorated', postedAt: '2026-01-10T09:00:00Z', deadline: '2026-02-28T23:59:59Z', roles: ['Financial Analyst'], labels: ['Finance', 'Top Employer'], status: 'closed', description: 'Join JPMorgan Chase\'s Investment Banking Division for a 10-week summer program in M&A or Capital Markets.', qualifications: 'Expected graduation 2027. Strong academic record. Interest in finance.', applicants: 5210 },
    { id: 'job_04', employerId: 'emp_03', title: 'Software Engineer Intern', type: 'Internship', location: 'Redmond, WA', salary: '$50/hr', postedAt: '2026-02-01T12:00:00Z', deadline: '2026-04-01T23:59:59Z', roles: ['Software Engineer'], labels: ['STEM', 'Top Employer'], status: 'active', description: 'Work on real products used by millions as a Software Engineer Intern at Microsoft. Teams include Azure, Office, Windows, and more.', qualifications: 'Pursuing BS/MS/PhD in CS, CE, or related. Proficient in C++, C#, or Java.', applicants: 1567 },
    { id: 'job_05', employerId: 'emp_04', title: 'Business Analyst Intern', type: 'Internship', location: 'Multiple Locations', salary: 'Competitive', postedAt: '2026-01-20T08:00:00Z', deadline: '2026-03-15T23:59:59Z', roles: ['Business Analyst', 'Consultant'], labels: ['Consulting'], status: 'active', description: 'As a Business Analyst Intern at McKinsey, you\'ll work alongside consultants to solve complex business problems.', qualifications: 'Outstanding academic record. Strong problem-solving skills.', applicants: 3890 },
    { id: 'job_06', employerId: 'emp_05', title: 'Hardware Engineering Intern', type: 'Internship', location: 'Cupertino, CA', salary: '$48/hr', postedAt: '2026-02-10T11:00:00Z', deadline: '2026-03-30T23:59:59Z', roles: ['Hardware Engineer'], labels: ['STEM', 'Top Employer'], status: 'active', description: 'Join Apple\'s hardware team to work on next-generation devices.', qualifications: 'Pursuing BS/MS in EE, CE, or ME. Lab experience preferred.', applicants: 987 },
    { id: 'job_07', employerId: 'emp_07', title: 'Machine Learning Engineer Intern', type: 'Internship', location: 'Menlo Park, CA', salary: '$56/hr', postedAt: '2026-02-18T09:30:00Z', deadline: '2026-04-10T23:59:59Z', roles: ['Machine Learning Engineer', 'Software Engineer'], labels: ['STEM', 'AI/ML'], status: 'active', description: 'Work on cutting-edge ML systems powering Meta\'s family of apps.', qualifications: 'Pursuing MS/PhD in CS, ML, Statistics. Experience with PyTorch.', applicants: 1234 },
    { id: 'job_08', employerId: 'emp_09', title: 'SDE Intern, AWS', type: 'Internship', location: 'Seattle, WA', salary: '$51/hr', postedAt: '2026-02-05T08:00:00Z', deadline: '2026-04-05T23:59:59Z', roles: ['Software Engineer', 'Cloud Engineer'], labels: ['STEM', 'Top Employer'], status: 'active', description: 'Join Amazon Web Services as an SDE Intern. Build and operate large-scale cloud services.', qualifications: 'Pursuing BS/MS in CS or related. Experience with distributed systems preferred.', applicants: 2103 },
    { id: 'job_09', employerId: 'emp_10', title: 'Backend Engineer Intern', type: 'Internship', location: 'San Francisco, CA', salary: '$50/hr', postedAt: '2026-02-22T10:00:00Z', deadline: '2026-04-15T23:59:59Z', roles: ['Backend Developer', 'Software Engineer'], labels: ['STEM', 'Startup'], status: 'active', description: 'Help build the future of internet payments at Stripe. Work on distributed systems and API design.', qualifications: 'Pursuing BS/MS in CS. Strong fundamentals in algorithms and systems.', applicants: 876 },
    { id: 'job_10', employerId: 'emp_06', title: 'Summer Analyst, Securities Division', type: 'Internship', location: 'New York, NY', salary: '$90,000/yr prorated', postedAt: '2026-01-15T09:00:00Z', deadline: '2026-03-01T23:59:59Z', roles: ['Financial Analyst'], labels: ['Finance', 'Top Employer'], status: 'closed', description: 'Join Goldman Sachs\' Securities Division for a 10-week summer program.', qualifications: 'Expected graduation 2027. Quantitative background preferred.', applicants: 4100 },
    { id: 'job_11', employerId: 'emp_08', title: 'Technology Consulting Intern', type: 'Internship', location: 'Chicago, IL', salary: '$40/hr', postedAt: '2026-02-12T14:00:00Z', deadline: '2026-04-01T23:59:59Z', roles: ['Consultant'], labels: ['Consulting', 'Technology'], status: 'active', description: 'Join Deloitte\'s Technology Consulting practice and help clients solve complex business challenges.', qualifications: 'Pursuing BS/MS in CS, IS, or Business. Strong communication skills.', applicants: 1654 },
    { id: 'job_12', employerId: 'emp_15', title: 'Research Engineer Intern', type: 'Internship', location: 'San Francisco, CA', salary: '$60/hr', postedAt: '2026-02-25T09:00:00Z', deadline: '2026-04-20T23:59:59Z', roles: ['Research Scientist', 'Machine Learning Engineer'], labels: ['AI/ML', 'Research'], status: 'active', description: 'Work on alignment research and build AI systems that are safe, beneficial, and interpretable.', qualifications: 'Pursuing MS/PhD in CS, ML, or related. Experience with large language models preferred.', applicants: 567 },
    { id: 'job_13', employerId: 'emp_12', title: 'Mechanical Engineering Intern', type: 'Internship', location: 'Austin, TX', salary: '$42/hr', postedAt: '2026-02-08T10:00:00Z', deadline: '2026-03-25T23:59:59Z', roles: ['Mechanical Engineer'], labels: ['STEM', 'Manufacturing'], status: 'active', description: 'Join Tesla\'s manufacturing team and help design next-gen EV components.', qualifications: 'Pursuing BS/MS in ME. CAD experience required.', applicants: 743 },
    { id: 'job_14', employerId: 'emp_11', title: 'Associate Consultant Intern', type: 'Internship', location: 'Boston, MA', salary: 'Competitive', postedAt: '2026-01-25T08:00:00Z', deadline: '2026-03-10T23:59:59Z', roles: ['Consultant', 'Business Analyst'], labels: ['Consulting'], status: 'closed', description: 'Experience Bain\'s case-based approach to consulting during this summer program.', qualifications: 'Outstanding academic record. Analytical and interpersonal skills.', applicants: 2890 },
    { id: 'job_15', employerId: 'emp_13', title: 'Data Science Intern', type: 'Internship', location: 'New York, NY', salary: '$47/hr', postedAt: '2026-02-28T11:00:00Z', deadline: '2026-04-18T23:59:59Z', roles: ['Data Scientist', 'Data Engineer'], labels: ['STEM', 'Media'], status: 'active', description: 'Use data to drive decision-making across Spotify\'s products and content teams.', qualifications: 'Pursuing MS in Statistics, CS, or related. SQL and Python required.', applicants: 921 },
    { id: 'job_16', employerId: 'emp_14', title: 'Technical Solutions Engineer', type: 'Full-time', location: 'Verona, WI', salary: '$95,000-$115,000/yr', postedAt: '2026-02-14T08:00:00Z', deadline: '2026-05-01T23:59:59Z', roles: ['Software Engineer', 'Solutions Architect'], labels: ['Healthcare', 'STEM'], status: 'active', description: 'Configure and implement Epic\'s healthcare software for hospitals and clinics nationwide.', qualifications: 'BS in CS, Engineering, Math, or related. Willingness to relocate to Madison, WI area.', applicants: 445 },
    { id: 'job_17', employerId: 'emp_19', title: 'Software Engineer, New Grad', type: 'Full-time', location: 'San Francisco, CA', salary: '$130,000-$160,000/yr', postedAt: '2026-02-17T10:00:00Z', deadline: '2026-04-30T23:59:59Z', roles: ['Software Engineer', 'Full-Stack Developer'], labels: ['STEM', 'Top Employer'], status: 'active', description: 'Join Salesforce as a new graduate software engineer. Work on the world\'s #1 CRM platform.', qualifications: 'BS/MS in CS or related. Graduating in 2026.', applicants: 1890 },
    { id: 'job_18', employerId: 'emp_16', title: 'Product Management Intern', type: 'Internship', location: 'Beaverton, OR', salary: '$40/hr', postedAt: '2026-02-20T09:00:00Z', deadline: '2026-04-10T23:59:59Z', roles: ['Product Manager'], labels: ['Retail', 'Consumer'], status: 'active', description: 'Shape the future of Nike\'s digital products as a PM intern.', qualifications: 'Pursuing BS/MBA. Passion for sports and consumer products.', applicants: 1342 },
    { id: 'job_19', employerId: 'emp_17', title: 'Forward Deployed Engineer Intern', type: 'Internship', location: 'Denver, CO', salary: '$55/hr', postedAt: '2026-02-19T11:00:00Z', deadline: '2026-04-12T23:59:59Z', roles: ['Software Engineer'], labels: ['STEM', 'Government'], status: 'active', description: 'Work directly with Palantir\'s customers to solve real-world problems using Palantir platforms.', qualifications: 'Pursuing BS/MS in CS. Strong programming skills and adaptability.', applicants: 654 },
    { id: 'job_20', employerId: 'emp_18', title: 'Corps Member 2026', type: 'Full-time', location: 'Multiple Locations', salary: '$33,000-$58,000/yr', postedAt: '2026-01-05T08:00:00Z', deadline: '2026-04-01T23:59:59Z', roles: ['Teacher', 'Educator'], labels: ['Education', 'Nonprofit'], status: 'active', description: 'Make a difference as a TFA corps member. Teach in an underserved community for two years.', qualifications: 'Bachelor\'s degree by start date. All majors welcome. US citizenship or permanent residency.', applicants: 3200 },
    { id: 'job_21', employerId: 'emp_20', title: 'Full-Stack Engineer (Early Stage)', type: 'Full-time', location: 'Austin, TX (Remote OK)', salary: '$110,000-$140,000 + equity', postedAt: '2026-03-01T08:00:00Z', deadline: '2026-04-30T23:59:59Z', roles: ['Full-Stack Developer', 'Software Engineer'], labels: ['Startup', 'Remote-Friendly'], status: 'active', description: 'Join our founding engineering team. Build AI-powered developer tools from the ground up.', qualifications: '2+ years experience with React and Node.js. Comfortable with ambiguity.', applicants: 89 },
    { id: 'job_22', employerId: 'emp_01', title: 'UX Design Intern', type: 'Internship', location: 'San Francisco, CA', salary: '$50/hr', postedAt: '2026-02-23T10:00:00Z', deadline: '2026-04-08T23:59:59Z', roles: ['UX Designer', 'UI Designer'], labels: ['Design', 'Top Employer'], status: 'active', description: 'Design user experiences for Google products used by billions of people worldwide.', qualifications: 'Pursuing BS/MFA in Design, HCI, or related. Portfolio required.', applicants: 1123 },
    { id: 'job_23', employerId: 'emp_03', title: 'Program Manager Intern', type: 'Internship', location: 'Redmond, WA', salary: '$48/hr', postedAt: '2026-02-16T08:00:00Z', deadline: '2026-04-03T23:59:59Z', roles: ['Project Manager', 'Product Manager'], labels: ['STEM', 'Top Employer'], status: 'active', description: 'Drive engineering projects forward as a Program Manager Intern at Microsoft.', qualifications: 'Pursuing BS/MS in CS, Engineering, or Business. Strong organizational skills.', applicants: 932 },
    { id: 'job_24', employerId: 'emp_09', title: 'Product Manager Intern', type: 'Internship', location: 'Seattle, WA', salary: '$53/hr', postedAt: '2026-02-24T14:00:00Z', deadline: '2026-04-14T23:59:59Z', roles: ['Product Manager'], labels: ['Top Employer'], status: 'active', description: 'Own and drive product features end-to-end at Amazon.', qualifications: 'Pursuing MBA or BS/MS. Data-driven decision-making experience.', applicants: 1678 },
    { id: 'job_25', employerId: 'emp_05', title: 'Machine Learning / AI Intern', type: 'Internship', location: 'Cupertino, CA', salary: '$55/hr', postedAt: '2026-03-01T09:00:00Z', deadline: '2026-04-25T23:59:59Z', roles: ['Machine Learning Engineer', 'Research Scientist'], labels: ['AI/ML', 'Top Employer'], status: 'active', description: 'Work on Siri, Core ML, or Apple Intelligence as an ML/AI intern.', qualifications: 'Pursuing MS/PhD in CS, ML, or Statistics. Published research preferred.', applicants: 782 },
    { id: 'job_26', employerId: 'emp_07', title: 'Product Design Intern', type: 'Internship', location: 'Menlo Park, CA', salary: '$52/hr', postedAt: '2026-02-26T10:00:00Z', deadline: '2026-04-16T23:59:59Z', roles: ['UX Designer', 'Product Manager'], labels: ['Design'], status: 'active', description: 'Design experiences for 3+ billion people across Meta\'s family of apps.', qualifications: 'Pursuing BS/MFA in Design or HCI. Portfolio with mobile/web work.', applicants: 1456 },
    { id: 'job_27', employerId: 'emp_02', title: 'Quantitative Research Analyst', type: 'Full-time', location: 'New York, NY', salary: '$120,000-$150,000/yr', postedAt: '2026-02-11T09:00:00Z', deadline: '2026-04-20T23:59:59Z', roles: ['Data Scientist', 'Financial Analyst'], labels: ['Finance', 'Quantitative'], status: 'active', description: 'Apply advanced quantitative methods to solve complex financial problems at JPMorgan.', qualifications: 'MS/PhD in Math, Physics, CS, or related. Strong programming skills.', applicants: 1230 },
    { id: 'job_28', employerId: 'emp_06', title: 'Engineering Analyst, New Grad', type: 'Full-time', location: 'New York, NY', salary: '$110,000-$135,000/yr', postedAt: '2026-02-13T14:00:00Z', deadline: '2026-04-22T23:59:59Z', roles: ['Software Engineer'], labels: ['Finance', 'STEM'], status: 'active', description: 'Build trading systems and risk platforms at Goldman Sachs Engineering.', qualifications: 'BS/MS in CS or Engineering. Graduating 2026. Strong programming fundamentals.', applicants: 2340 },
    { id: 'job_29', employerId: 'emp_15', title: 'Policy Research Intern', type: 'Internship', location: 'San Francisco, CA', salary: '$45/hr', postedAt: '2026-03-02T08:00:00Z', deadline: '2026-04-28T23:59:59Z', roles: ['Research Scientist'], labels: ['AI/ML', 'Policy'], status: 'active', description: 'Research AI policy and governance at Anthropic. Help shape responsible AI development.', qualifications: 'Pursuing MS/PhD in public policy, law, philosophy, or CS. Interest in AI governance.', applicants: 234 },
    { id: 'job_30', employerId: 'emp_19', title: 'Marketing Analyst Intern', type: 'Internship', location: 'San Francisco, CA', salary: '$38/hr', postedAt: '2026-02-27T10:00:00Z', deadline: '2026-04-15T23:59:59Z', roles: ['Marketing Coordinator', 'Business Analyst'], labels: ['Marketing'], status: 'active', description: 'Drive data-informed marketing strategies at Salesforce.', qualifications: 'Pursuing BS/MS in Marketing, Business, or Analytics. SQL knowledge preferred.', applicants: 678 }
];

// ============================================================
// Feed Posts
// ============================================================
const FEED_POSTS = [
    { id: 'post_01', authorType: 'employer', authorId: 'emp_01', authorName: 'Google', authorAvatarColor: '#4285F4', content: 'Exciting news! We\'re expanding our Summer 2026 internship program with 500 new positions across engineering, product, and design. Apply now on Handshake!', audience: 'everyone', likes: 342, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-03-05T14:00:00Z', bookmarked: false },
    { id: 'post_02', authorType: 'student', authorId: 'stu_f2a1b3c4', authorName: 'Jessica Park', authorSchool: 'Stanford University', authorAvatarColor: '#E74C3C', content: 'Just got my return offer from Meta after an amazing summer internship! Happy to share tips about the interview process and what to expect. DM me or comment below! #internship #meta #tech', audience: 'everyone', likes: 187, comments: [
        { id: 'cmt_01', authorName: 'Tyler Wong', authorSchool: 'UC Berkeley', authorAvatarColor: '#3498DB', text: 'Congrats! Would love to hear about the coding interview format.', createdAt: '2026-03-05T15:10:00Z', isAnonymous: false },
        { id: 'cmt_02', authorName: 'Anonymous Student', authorSchool: 'Stanford University', authorAvatarColor: '#95A5A6', text: 'How many rounds were there?', createdAt: '2026-03-05T16:22:00Z', isAnonymous: true }
    ], hasImage: false, hasVideo: false, createdAt: '2026-03-05T12:30:00Z', bookmarked: true },
    { id: 'post_03', authorType: 'employer', authorId: 'emp_07', authorName: 'Meta', authorAvatarColor: '#0668E1', content: 'We\'re hosting a virtual info session on AI/ML careers at Meta next Thursday at 5pm PT. Sign up through Events on Handshake! We\'ll cover team overviews, project highlights, and Q&A with current engineers.', audience: 'everyone', likes: 256, comments: [
        { id: 'cmt_03', authorName: 'Rahul Gupta', authorSchool: 'Georgia Tech', authorAvatarColor: '#2ECC71', text: 'Is this open to all schools?', createdAt: '2026-03-04T11:45:00Z', isAnonymous: false }
    ], hasImage: false, hasVideo: false, createdAt: '2026-03-04T10:00:00Z', bookmarked: false },
    { id: 'post_04', authorType: 'student', authorId: 'stu_a4c2d5e6', authorName: 'Marcus Johnson', authorSchool: 'University of Michigan', authorAvatarColor: '#F39C12', content: 'Just wrapped up my first week at Stripe as a backend engineer. The code review culture here is incredible - I\'ve already learned so much about distributed systems. If anyone is considering Stripe, happy to share my experience!', audience: 'everyone', likes: 143, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-03-04T08:15:00Z', bookmarked: false },
    { id: 'post_05', authorType: 'employer', authorId: 'emp_15', authorName: 'Anthropic', authorAvatarColor: '#D4A574', content: 'We believe in building AI that is safe, beneficial, and understandable. Our 2026 internship applications are now open for Research Engineering and Policy Research roles. Help us shape the future of AI safety.', audience: 'everyone', likes: 198, comments: [
        { id: 'cmt_04', authorName: 'Maya Chen', authorSchool: 'Stanford University', authorAvatarColor: '#4A90D9', text: 'So excited about this! Just submitted my application for the Research Engineering role.', createdAt: '2026-03-03T16:30:00Z', isAnonymous: false }
    ], hasImage: false, hasVideo: false, createdAt: '2026-03-03T14:00:00Z', bookmarked: false },
    { id: 'post_06', authorType: 'student', authorId: 'stu_b5d3e7f8', authorName: 'Aisha Mohammed', authorSchool: 'Howard University', authorAvatarColor: '#9B59B6', content: 'Attending the National Society of Black Engineers conference next week! Who else will be there? Let\'s connect! I\'m especially interested in meeting recruiters from tech companies. #NSBE #engineering #diversity', audience: 'everyone', likes: 231, comments: [
        { id: 'cmt_05', authorName: 'Derek Williams', authorSchool: 'Morehouse College', authorAvatarColor: '#1ABC9C', text: 'See you there! I\'ll be at the Google and Microsoft booths.', createdAt: '2026-03-03T10:50:00Z', isAnonymous: false },
        { id: 'cmt_06', authorName: 'Jasmine Lewis', authorSchool: 'Spelman College', authorAvatarColor: '#E67E22', text: 'Can\'t wait! This will be my first NSBE conference.', createdAt: '2026-03-03T11:30:00Z', isAnonymous: false }
    ], hasImage: false, hasVideo: false, createdAt: '2026-03-03T09:00:00Z', bookmarked: false },
    { id: 'post_07', authorType: 'employer', authorId: 'emp_09', authorName: 'Amazon', authorAvatarColor: '#FF9900', content: 'AWS re:Invent was incredible this year! Missed it? Check out our recap and highlights. We\'re also hiring across all AWS teams - SDE, Solutions Architect, PM, and more. 200+ new grad and intern positions available.', audience: 'everyone', likes: 178, comments: [], hasImage: true, hasVideo: false, createdAt: '2026-03-02T16:00:00Z', bookmarked: false },
    { id: 'post_08', authorType: 'student', authorId: 'stu_c6e4f8a9', authorName: 'Kevin O\'Brien', authorSchool: 'MIT', authorAvatarColor: '#34495E', content: 'After 6 months of preparation, I finally passed all my FAANG interviews! Here\'s my study plan:\n\n1. LeetCode: 200 problems (focus on patterns, not quantity)\n2. System Design: Grokking + YouTube\n3. Behavioral: STAR method with real examples\n4. Mock interviews: Pramp + friends\n\nDon\'t give up. The process is tough but worth it.', audience: 'everyone', likes: 534, comments: [
        { id: 'cmt_07', authorName: 'Sarah Kim', authorSchool: 'MIT', authorAvatarColor: '#2C3E50', text: 'This is so helpful! Did you use any specific LeetCode lists?', createdAt: '2026-03-02T12:45:00Z', isAnonymous: false },
        { id: 'cmt_08', authorName: 'Anonymous Student', authorSchool: 'Purdue University', authorAvatarColor: '#95A5A6', text: 'How long did you study each day?', createdAt: '2026-03-02T13:20:00Z', isAnonymous: true },
        { id: 'cmt_09', authorName: 'Priya Sharma', authorSchool: 'Columbia University', authorAvatarColor: '#8E44AD', text: 'Congrats Kevin! Which companies did you end up getting offers from?', createdAt: '2026-03-02T14:00:00Z', isAnonymous: false }
    ], hasImage: false, hasVideo: false, createdAt: '2026-03-02T11:00:00Z', bookmarked: true },
    { id: 'post_09', authorType: 'employer', authorId: 'emp_04', authorName: 'McKinsey & Company', authorAvatarColor: '#003C71', content: 'Thinking about a career in consulting? Join our campus presentation at Stanford on March 15th. We\'ll cover what it\'s like to work at McKinsey, the types of projects you\'ll be on, and tips for the case interview.', audience: 'everyone', likes: 167, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-03-02T09:00:00Z', bookmarked: false },
    { id: 'post_10', authorType: 'student', authorId: 'stu_d7f5a9b0', authorName: 'Emma Rodriguez', authorSchool: 'Stanford University', authorAvatarColor: '#27AE60', content: 'Hi everyone! I\'m a junior studying HCI and I just launched my portfolio website. Would love feedback from fellow designers and anyone in UX. Link in my profile bio. Also open to coffee chats about UX careers!', audience: 'school', likes: 89, comments: [
        { id: 'cmt_10', authorName: 'Maya Chen', authorSchool: 'Stanford University', authorAvatarColor: '#4A90D9', text: 'Love your case studies, Emma! The Spotify redesign is really thoughtful.', createdAt: '2026-03-01T15:30:00Z', isAnonymous: false }
    ], hasImage: false, hasVideo: false, createdAt: '2026-03-01T14:00:00Z', bookmarked: false },
    { id: 'post_11', authorType: 'employer', authorId: 'emp_05', authorName: 'Apple', authorAvatarColor: '#000000', content: 'Our Apple Pathways intern program is designed for students from underrepresented backgrounds in tech. Applications are open for Summer 2026 across engineering, design, and marketing. We\'re committed to building a workforce as diverse as our user base.', audience: 'everyone', likes: 289, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-03-01T10:00:00Z', bookmarked: false },
    { id: 'post_12', authorType: 'student', authorId: 'stu_e8a6b0c1', authorName: 'Jordan Taylor', authorSchool: 'Northwestern University', authorAvatarColor: '#C0392B', content: 'Hot take: You don\'t need to work at a FAANG company to have a great career in tech. I turned down a Big Tech offer to join a Series B startup and it was the best decision I ever made. Ownership, speed, and impact are unmatched.', audience: 'everyone', likes: 412, comments: [
        { id: 'cmt_11', authorName: 'Alex Rivera', authorSchool: 'Carnegie Mellon', authorAvatarColor: '#16A085', text: 'Totally agree! I started at a startup and learned more in 6 months than some learn in 2 years at big companies.', createdAt: '2026-02-28T17:00:00Z', isAnonymous: false },
        { id: 'cmt_12', authorName: 'Anonymous Student', authorSchool: 'Columbia University', authorAvatarColor: '#95A5A6', text: 'Counter-point: Big Tech gives you brand name recognition and structured mentorship that startups often lack.', createdAt: '2026-02-28T18:15:00Z', isAnonymous: true }
    ], hasImage: false, hasVideo: false, createdAt: '2026-02-28T15:30:00Z', bookmarked: false },
    { id: 'post_13', authorType: 'employer', authorId: 'emp_10', authorName: 'Stripe', authorAvatarColor: '#635BFF', content: 'Engineering at Stripe: We process hundreds of billions of dollars in payments every year. Behind every transaction is elegant code. Our engineering blog just published a deep dive on our distributed systems architecture. Come build with us!', audience: 'everyone', likes: 156, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-02-28T12:00:00Z', bookmarked: false },
    { id: 'post_14', authorType: 'student', authorId: 'stu_f9b7c1d2', authorName: 'David Lee', authorSchool: 'UC Berkeley', authorAvatarColor: '#2980B9', content: 'I created a study group for anyone preparing for PM interviews this spring. We meet virtually every Tuesday and Thursday at 7pm PT. Topics include product sense, analytical, and execution questions. Comment or DM to join!', audience: 'everyone', likes: 276, comments: [
        { id: 'cmt_13', authorName: 'Lisa Chang', authorSchool: 'UCLA', authorAvatarColor: '#F1C40F', text: 'I\'d love to join! Just sent you a DM.', createdAt: '2026-02-27T20:00:00Z', isAnonymous: false },
        { id: 'cmt_14', authorName: 'Sam Patel', authorSchool: 'UC Berkeley', authorAvatarColor: '#D35400', text: 'This is exactly what I needed. Signing up!', createdAt: '2026-02-27T21:30:00Z', isAnonymous: false },
        { id: 'cmt_15', authorName: 'Mia Thompson', authorSchool: 'University of Washington', authorAvatarColor: '#7F8C8D', text: 'Is this open to people from other schools?', createdAt: '2026-02-28T08:00:00Z', isAnonymous: false }
    ], hasImage: false, hasVideo: false, createdAt: '2026-02-27T18:00:00Z', bookmarked: true },
    { id: 'post_15', authorType: 'employer', authorId: 'emp_02', authorName: 'JPMorgan Chase', authorAvatarColor: '#003A70', content: 'Our Technology Analyst program is one of the largest in financial services. Over 1,500 new technologists join us each year. This summer, interns will have the opportunity to work on real projects in AI, cloud, and cybersecurity.', audience: 'everyone', likes: 134, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-02-27T10:00:00Z', bookmarked: false },
    { id: 'post_16', authorType: 'student', authorId: 'stu_a0c8d2e3', authorName: 'Nathan Brooks', authorSchool: 'Rice University', authorAvatarColor: '#6C3483', content: 'Career fair tips from someone who\'s been to 12 of them:\n\n- Research companies beforehand\n- Prepare your 30-second pitch\n- Ask thoughtful questions (NOT \"what does your company do?\")\n- Follow up within 24 hours\n- Wear comfortable shoes\n\nGood luck to everyone attending the Stanford Career Fair next week!', audience: 'everyone', likes: 325, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-02-26T13:00:00Z', bookmarked: false },
    { id: 'post_17', authorType: 'employer', authorId: 'emp_18', authorName: 'Teach For America', authorAvatarColor: '#E31937', content: 'Every child deserves access to an excellent education. Our 2026 corps applications are still open. All majors welcome. Make an impact that lasts a lifetime. Learn more about the corps member experience on our brand page.', audience: 'everyone', likes: 98, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-02-26T09:00:00Z', bookmarked: false },
    { id: 'post_18', authorType: 'student', authorId: 'stu_b1d9e3f4', authorName: 'Sophia Williams', authorSchool: 'Harvard University', authorAvatarColor: '#A93226', content: 'Just finished reading \"Cracking the PM Interview\" - here are my top 5 takeaways for anyone preparing for PM roles:\n\n1. Structure your answers (always)\n2. Quantify impact wherever possible\n3. Practice out loud, not just in your head\n4. Know your \"why\" for each company\n5. Build side projects to demonstrate product thinking', audience: 'everyone', likes: 267, comments: [
        { id: 'cmt_16', authorName: 'David Lee', authorSchool: 'UC Berkeley', authorAvatarColor: '#2980B9', text: 'Great list! I\'d add: always tie your answers back to user impact.', createdAt: '2026-02-25T16:45:00Z', isAnonymous: false }
    ], hasImage: false, hasVideo: false, createdAt: '2026-02-25T14:30:00Z', bookmarked: false },
    { id: 'post_19', authorType: 'employer', authorId: 'emp_03', authorName: 'Microsoft', authorAvatarColor: '#00A4EF', content: 'Microsoft Imagine Cup 2026 is here! Form your team and build a solution using Microsoft technology. Grand prize: $100K, mentorship from Microsoft leaders, and Azure credits. Registration closes March 31st.', audience: 'everyone', likes: 312, comments: [
        { id: 'cmt_17', authorName: 'Omar Hassan', authorSchool: 'University of Texas', authorAvatarColor: '#E67E22', text: 'Looking for teammates! I\'m a CS junior with experience in Azure and React. DM me!', createdAt: '2026-02-24T19:00:00Z', isAnonymous: false }
    ], hasImage: true, hasVideo: false, createdAt: '2026-02-24T12:00:00Z', bookmarked: false },
    { id: 'post_20', authorType: 'student', authorId: 'stu_c2e0f4a5', authorName: 'Rachel Kim', authorSchool: 'Yale University', authorAvatarColor: '#148F77', content: 'Intro post! I\'m Rachel, a sophomore at Yale studying Cognitive Science and CS. I\'m interested in the intersection of psychology and technology, especially in UX research and human-AI interaction. Looking to connect with others in this space!', audience: 'everyone', likes: 145, comments: [], hasImage: false, hasVideo: false, createdAt: '2026-02-23T11:00:00Z', bookmarked: false }
];

// ============================================================
// Events
// ============================================================
const EVENTS = [
    { id: 'evt_01', employerId: 'emp_04', employerName: 'McKinsey & Company', title: 'McKinsey Campus Presentation - Stanford', type: 'Info Session', date: '2026-03-15', time: '5:00 PM - 6:30 PM', location: 'Huang Engineering Center, Room 100', isVirtual: false, description: 'Learn about career opportunities at McKinsey. Hear from consultants about their day-to-day work and get tips for the case interview.', rsvpCount: 87, status: 'upcoming', labels: ['Consulting', 'Presentation'] },
    { id: 'evt_02', employerId: 'emp_07', employerName: 'Meta', title: 'AI/ML Careers at Meta - Virtual Info Session', type: 'Virtual Session', date: '2026-03-13', time: '5:00 PM - 6:00 PM PT', location: 'Virtual on Handshake', isVirtual: true, description: 'Discover AI/ML career paths at Meta. Our engineers will share project highlights and answer your questions live.', rsvpCount: 234, status: 'upcoming', labels: ['Technology', 'AI/ML', 'Virtual'] },
    { id: 'evt_03', employerId: null, employerName: 'Stanford Career Center', title: 'Stanford Spring Career Fair 2026', type: 'Career Fair', date: '2026-03-20', time: '10:00 AM - 4:00 PM', location: 'Arrillaga Alumni Center', isVirtual: false, description: 'Meet 200+ employers across technology, finance, consulting, healthcare, and more. Bring your resume and dress professionally.', rsvpCount: 1256, status: 'upcoming', labels: ['Career Fair', 'All Industries'] },
    { id: 'evt_04', employerId: 'emp_01', employerName: 'Google', title: 'Google Tech Talk: Building Scalable ML Systems', type: 'Tech Talk', date: '2026-03-18', time: '4:00 PM - 5:30 PM', location: 'Gates Computer Science Building, Room B03', isVirtual: false, description: 'Join Google engineers as they discuss how ML systems are built and deployed at Google scale. Includes networking and refreshments.', rsvpCount: 156, status: 'upcoming', labels: ['Technology', 'AI/ML', 'Tech Talk'] },
    { id: 'evt_05', employerId: null, employerName: 'Stanford Career Center', title: 'Resume Workshop: Making Your Resume Stand Out', type: 'Workshop', date: '2026-03-10', time: '2:00 PM - 3:30 PM', location: 'Career Center, Room 201', isVirtual: false, description: 'Learn how to craft a compelling resume that gets noticed by recruiters. Bring a printed copy of your current resume for live feedback.', rsvpCount: 45, status: 'upcoming', labels: ['Workshop', 'Career Development'] },
    { id: 'evt_06', employerId: 'emp_15', employerName: 'Anthropic', title: 'Anthropic Research Talk: AI Alignment', type: 'Tech Talk', date: '2026-03-22', time: '3:00 PM - 4:30 PM PT', location: 'Virtual on Handshake', isVirtual: true, description: 'Anthropic researchers discuss the latest developments in AI alignment and constitutional AI. Q&A session included.', rsvpCount: 198, status: 'upcoming', labels: ['Technology', 'AI/ML', 'Research', 'Virtual'] },
    { id: 'evt_07', employerId: null, employerName: 'Stanford Career Center', title: 'Virtual Career Fair - Technology Focus', type: 'Career Fair', date: '2026-03-25', time: '11:00 AM - 3:00 PM PT', location: 'Virtual on Handshake', isVirtual: true, description: 'Connect with 50+ technology employers in 1:1 and group sessions. Create your schedule in advance to secure time slots.', rsvpCount: 567, status: 'upcoming', labels: ['Career Fair', 'Technology', 'Virtual'] },
    { id: 'evt_08', employerId: 'emp_02', employerName: 'JPMorgan Chase', title: 'JPM Markets & Trading Panel', type: 'Panel', date: '2026-03-12', time: '6:00 PM - 7:30 PM', location: 'GSB Knight Management Center', isVirtual: false, description: 'Hear from JPMorgan traders about career paths in global markets. Networking reception to follow.', rsvpCount: 92, status: 'upcoming', labels: ['Finance', 'Panel'] },
    { id: 'evt_09', employerId: null, employerName: 'Stanford Career Center', title: 'Interview Prep: Behavioral Questions Masterclass', type: 'Workshop', date: '2026-03-08', time: '1:00 PM - 2:30 PM', location: 'Career Center, Room 105', isVirtual: false, description: 'Master the STAR method and prepare for behavioral interviews. Practice with peers and get real-time feedback.', rsvpCount: 38, status: 'upcoming', labels: ['Workshop', 'Interview Prep'] },
    { id: 'evt_10', employerId: 'emp_19', employerName: 'Salesforce', title: 'Salesforce Futureforce: Building Your Career in Cloud', type: 'Info Session', date: '2026-03-17', time: '12:00 PM - 1:00 PM PT', location: 'Virtual on Handshake', isVirtual: true, description: 'Learn about Salesforce\'s Futureforce intern and new grad program. Hear from recent hires about their experiences.', rsvpCount: 123, status: 'upcoming', labels: ['Technology', 'Virtual'] },
    { id: 'evt_11', employerId: null, employerName: 'Stanford Career Center', title: 'Networking 101: Building Professional Relationships', type: 'Workshop', date: '2026-02-28', time: '3:00 PM - 4:00 PM', location: 'Career Center, Room 201', isVirtual: false, description: 'Learn strategies for building and maintaining professional relationships. Includes networking practice exercises.', rsvpCount: 52, status: 'past', labels: ['Workshop', 'Career Development'] },
    { id: 'evt_12', employerId: 'emp_05', employerName: 'Apple', title: 'Apple Design Speaker Series', type: 'Speaker Event', date: '2026-02-25', time: '4:00 PM - 5:30 PM', location: 'd.school, Building 550', isVirtual: false, description: 'Apple designers share how they approach human-centered design. Learn about the intersection of technology and liberal arts at Apple.', rsvpCount: 178, status: 'past', labels: ['Design', 'Technology'] }
];

// ============================================================
// Appointments
// ============================================================
const APPOINTMENT_CATEGORIES = [
    { id: 'cat_01', name: 'Career Counseling', types: ['General Career Advising', 'Career Change Guidance', 'Major Exploration'] },
    { id: 'cat_02', name: 'Job & Internship Search', types: ['Job Search Strategy', 'Internship Planning', 'Application Review'] },
    { id: 'cat_03', name: 'Resume & Cover Letter', types: ['Resume Review', 'Cover Letter Review', 'LinkedIn Profile Review'] },
    { id: 'cat_04', name: 'Interview Preparation', types: ['Mock Interview - Technical', 'Mock Interview - Behavioral', 'Case Interview Prep'] },
    { id: 'cat_05', name: 'Graduate School', types: ['Grad School Advising', 'Personal Statement Review', 'School Selection'] },
    { id: 'cat_06', name: 'Networking & Professional Development', types: ['Networking Strategy', 'Professional Branding', 'Salary Negotiation'] }
];

const APPOINTMENT_STAFF = [
    { id: 'staff_01', name: 'Dr. Patricia Williams', title: 'Senior Career Counselor', specialties: ['Technology', 'Engineering'] },
    { id: 'staff_02', name: 'James Chen', title: 'Career Advisor', specialties: ['Finance', 'Consulting'] },
    { id: 'staff_03', name: 'Maria Rodriguez', title: 'Career Advisor', specialties: ['Healthcare', 'Graduate School'] },
    { id: 'staff_04', name: 'David Kim', title: 'Interview Coach', specialties: ['Technical Interviews', 'Case Interviews'] },
    { id: 'staff_05', name: 'Sarah Thompson', title: 'Career Counselor', specialties: ['Creative Industries', 'Nonprofit'] },
    { id: 'staff_06', name: 'Michael Okafor', title: 'Career Advisor', specialties: ['Resume Writing', 'Professional Branding'] }
];

const APPOINTMENT_MEDIUMS = ['In Person', 'Virtual on Handshake', 'Phone'];

const APPOINTMENTS = [
    { id: 'appt_01', category: 'Resume & Cover Letter', type: 'Resume Review', staffId: 'staff_06', staffName: 'Michael Okafor', date: '2026-03-14', time: '10:00 AM', duration: 30, medium: 'In Person', location: 'Career Center, Office 204', status: 'approved', details: 'I\'d like feedback on my resume before the Spring Career Fair. Targeting tech PM roles.', comments: [
        { author: 'Michael Okafor', text: 'Looking forward to it, Maya! Please bring a printed copy and any job descriptions you\'re targeting.', createdAt: '2026-03-06T09:00:00Z' }
    ], createdAt: '2026-03-05T14:00:00Z' },
    { id: 'appt_02', category: 'Interview Preparation', type: 'Mock Interview - Technical', staffId: 'staff_04', staffName: 'David Kim', date: '2026-03-21', time: '2:00 PM', duration: 60, medium: 'Virtual on Handshake', location: null, status: 'requested', details: 'Preparing for Google SWE internship interview. Would like to practice coding problems and system design.', comments: [], createdAt: '2026-03-06T10:30:00Z' },
    { id: 'appt_03', category: 'Career Counseling', type: 'General Career Advising', staffId: 'staff_01', staffName: 'Dr. Patricia Williams', date: '2026-02-20', time: '11:00 AM', duration: 45, medium: 'In Person', location: 'Career Center, Office 101', status: 'completed', details: 'Want to discuss career options in AI/ML vs product management. Not sure which path to focus on.', comments: [
        { author: 'Dr. Patricia Williams', text: 'Great session today, Maya! As we discussed, both paths are viable with your background. I\'d recommend exploring PM internships this summer to complement your engineering experience. Here are the resources I mentioned: [Career Path Comparison Guide], [PM Interview Handbook].', createdAt: '2026-02-20T12:00:00Z' },
        { author: 'Maya Chen', text: 'Thank you! The PM path comparison was really helpful. I\'ll schedule a follow-up after the career fair.', createdAt: '2026-02-20T18:30:00Z' }
    ], createdAt: '2026-02-15T09:00:00Z' },
    { id: 'appt_04', category: 'Job & Internship Search', type: 'Internship Planning', staffId: 'staff_01', staffName: 'Dr. Patricia Williams', date: '2026-01-15', time: '3:00 PM', duration: 30, medium: 'Virtual on Handshake', location: null, status: 'completed', details: 'Looking for help planning my summer 2026 internship search strategy.', comments: [
        { author: 'Dr. Patricia Williams', text: 'Maya, great meeting! Key takeaways: 1) Apply broadly to 15-20 companies 2) Leverage your Meta experience 3) Attend career fair for networking 4) Consider reaching out to Stanford alumni at target companies.', createdAt: '2026-01-15T16:00:00Z' }
    ], createdAt: '2026-01-10T11:00:00Z' },
    { id: 'appt_05', category: 'Resume & Cover Letter', type: 'LinkedIn Profile Review', staffId: 'staff_06', staffName: 'Michael Okafor', date: '2026-01-08', time: '9:00 AM', duration: 30, medium: 'Phone', location: null, status: 'completed', details: 'Want help optimizing my LinkedIn profile for recruiter visibility.', comments: [], createdAt: '2025-12-20T14:00:00Z' },
    { id: 'appt_06', category: 'Interview Preparation', type: 'Mock Interview - Behavioral', staffId: 'staff_04', staffName: 'David Kim', date: '2025-11-10', time: '1:00 PM', duration: 45, medium: 'In Person', location: 'Career Center, Office 302', status: 'completed', details: 'Preparing for McKinsey final round.', comments: [
        { author: 'David Kim', text: 'Strong performance! Focus on being more concise in your STAR responses and quantifying impact more.', createdAt: '2025-11-10T14:00:00Z' }
    ], createdAt: '2025-11-05T10:00:00Z' },
    { id: 'appt_07', category: 'Career Counseling', type: 'Major Exploration', staffId: 'staff_03', staffName: 'Maria Rodriguez', date: '2025-09-20', time: '10:00 AM', duration: 30, medium: 'In Person', location: 'Career Center, Office 108', status: 'completed', details: 'Considering adding a minor in business. Want to understand how it helps in tech careers.', comments: [], createdAt: '2025-09-15T08:00:00Z' },
    { id: 'appt_08', category: 'Interview Preparation', type: 'Case Interview Prep', staffId: 'staff_02', staffName: 'James Chen', date: '2026-03-28', time: '11:00 AM', duration: 60, medium: 'Virtual on Handshake', location: null, status: 'requested', details: 'Bain second round coming up. Need to practice market sizing and profitability frameworks.', comments: [], createdAt: '2026-03-06T16:00:00Z' }
];

// ============================================================
// Q&A Community
// ============================================================
const QA_QUESTIONS = [
    {
        id: 'qa_01', authorName: 'Anonymous', authorSchool: 'Stanford University', authorMajor: 'Computer Science', authorGradYear: 2026, authorAvatarColor: '#95A5A6',
        question: 'What is the Google SWE internship interview process like?',
        status: 'approved', createdAt: '2026-02-20T10:00:00Z', views: 1245,
        answers: [
            { id: 'ans_01', authorName: 'Tyler Wong', authorSchool: 'UC Berkeley', authorMajor: 'EECS', authorGradYear: 2025, authorAvatarColor: '#3498DB', text: 'I went through it last year. There are 2 coding interviews (45 min each) on Google Meet. Questions are medium-hard LeetCode level, focusing on arrays, strings, trees, and graphs. The interviewers are friendly and give hints if you\'re stuck. I\'d recommend practicing 100+ LeetCode problems focusing on patterns.', visibility: 'full', status: 'approved', createdAt: '2026-02-20T14:00:00Z', helpful: 67 },
            { id: 'ans_02', authorName: 'Anonymous', authorSchool: 'Carnegie Mellon', authorMajor: 'Computer Science', authorGradYear: 2026, authorAvatarColor: '#95A5A6', text: 'For me it was: online assessment first (2 problems, 90 min), then 2 phone interviews. The OA was harder than the phone rounds tbh. Make sure you can explain your thought process clearly.', visibility: 'semi-anonymous', status: 'approved', createdAt: '2026-02-21T09:30:00Z', helpful: 43 }
        ]
    },
    {
        id: 'qa_02', authorName: 'Priya Sharma', authorSchool: 'Columbia University', authorMajor: 'Economics', authorGradYear: 2026, authorAvatarColor: '#8E44AD',
        question: 'How competitive is the JPMorgan Investment Banking Summer Analyst program?',
        status: 'approved', createdAt: '2026-02-18T11:00:00Z', views: 892,
        answers: [
            { id: 'ans_03', authorName: 'Michael Torres', authorSchool: 'Wharton School', authorMajor: 'Finance', authorGradYear: 2025, authorAvatarColor: '#E74C3C', text: 'Extremely competitive. They receive 10,000+ applications for around 500 positions. Having a strong GPA (3.7+), relevant experience, and networking with JPM employees are crucial. I\'d recommend attending their info sessions and getting coffee chats with analysts/associates.', visibility: 'full', status: 'approved', createdAt: '2026-02-18T15:30:00Z', helpful: 55 },
            { id: 'ans_04', authorName: 'Jessica Lee', authorSchool: 'NYU Stern', authorMajor: 'Finance & Accounting', authorGradYear: 2026, authorAvatarColor: '#2ECC71', text: 'I interned there last summer. The application process: online app -> HireVue video -> Superday (3 back-to-back interviews). Prep your behavioral stories and know DCF, LBO basics. Networking really makes a difference.', visibility: 'full', status: 'approved', createdAt: '2026-02-19T08:00:00Z', helpful: 41 }
        ]
    },
    {
        id: 'qa_03', authorName: 'Kevin O\'Brien', authorSchool: 'MIT', authorMajor: 'Computer Science', authorGradYear: 2026, authorAvatarColor: '#34495E',
        question: 'Is it worth doing a consulting internship before going into tech?',
        status: 'approved', createdAt: '2026-02-15T14:00:00Z', views: 634,
        answers: [
            { id: 'ans_05', authorName: 'Sarah Kim', authorSchool: 'Harvard University', authorMajor: 'Applied Math', authorGradYear: 2025, authorAvatarColor: '#F39C12', text: 'I did MBB consulting for 2 years before switching to tech PM. The analytical and communication skills you build in consulting are incredibly transferable. Many top tech companies value consulting experience for PM roles. However, if you\'re certain about engineering, a tech internship is more directly relevant.', visibility: 'full', status: 'approved', createdAt: '2026-02-15T18:00:00Z', helpful: 38 }
        ]
    },
    {
        id: 'qa_04', authorName: 'Anonymous', authorSchool: 'University of Michigan', authorMajor: 'Information Science', authorGradYear: 2027, authorAvatarColor: '#95A5A6',
        question: 'What should I wear to a virtual career fair on Handshake?',
        status: 'approved', createdAt: '2026-02-12T09:00:00Z', views: 423,
        answers: [
            { id: 'ans_06', authorName: 'Emma Rodriguez', authorSchool: 'Stanford University', authorMajor: 'Human-Computer Interaction', authorGradYear: 2027, authorAvatarColor: '#27AE60', text: 'Business casual is perfectly fine for virtual fairs. A nice top/blouse with a clean background works great. Make sure your lighting is good and test your camera/mic beforehand. Also, have your resume open and ready to reference!', visibility: 'full', status: 'approved', createdAt: '2026-02-12T12:00:00Z', helpful: 29 }
        ]
    },
    {
        id: 'qa_05', authorName: 'Lisa Chang', authorSchool: 'UCLA', authorMajor: 'Psychology', authorGradYear: 2026, authorAvatarColor: '#F1C40F',
        question: 'How do you negotiate salary for a new grad offer?',
        status: 'approved', createdAt: '2026-02-10T16:00:00Z', views: 1567,
        answers: [
            { id: 'ans_07', authorName: 'Jordan Taylor', authorSchool: 'Northwestern University', authorMajor: 'Industrial Engineering', authorGradYear: 2025, authorAvatarColor: '#C0392B', text: 'Key tips: 1) Always negotiate - most companies expect it. 2) Have competing offers if possible. 3) Research salary ranges on Levels.fyi and Glassdoor. 4) Negotiate total comp, not just base (signing bonus, equity, relocation). 5) Be respectful but firm. 6) Get the final offer in writing.', visibility: 'full', status: 'approved', createdAt: '2026-02-10T20:00:00Z', helpful: 89 },
            { id: 'ans_08', authorName: 'Anonymous', authorSchool: 'Stanford University', authorMajor: 'Computer Science', authorGradYear: 2025, authorAvatarColor: '#95A5A6', text: 'I negotiated my new grad offer from $180k to $210k total comp by having a competing offer. The recruiter was understanding and it didn\'t affect our relationship at all. Always negotiate.', visibility: 'semi-anonymous', status: 'approved', createdAt: '2026-02-11T10:00:00Z', helpful: 72 }
        ]
    },
    {
        id: 'qa_06', authorName: 'Aisha Mohammed', authorSchool: 'Howard University', authorMajor: 'Computer Engineering', authorGradYear: 2027, authorAvatarColor: '#9B59B6',
        question: 'What are the best resources for learning system design for interviews?',
        status: 'approved', createdAt: '2026-02-08T13:00:00Z', views: 987,
        answers: [
            { id: 'ans_09', authorName: 'Kevin O\'Brien', authorSchool: 'MIT', authorMajor: 'Computer Science', authorGradYear: 2026, authorAvatarColor: '#34495E', text: 'My top picks: 1) \"Designing Data-Intensive Applications\" by Martin Kleppmann 2) System Design Primer on GitHub 3) Grokking the System Design Interview on Educative 4) YouTube channels: Tech Dummies, Gaurav Sen. Start with the basics (load balancing, caching, databases) and work up to distributed systems.', visibility: 'full', status: 'approved', createdAt: '2026-02-08T17:00:00Z', helpful: 56 }
        ]
    },
    {
        id: 'qa_07', authorName: 'Maya Chen', authorSchool: 'Stanford University', authorMajor: 'Computer Science', authorGradYear: 2027, authorAvatarColor: '#4A90D9',
        question: 'What\'s the work-life balance like at Meta as a new grad engineer?',
        status: 'approved', createdAt: '2026-02-05T10:00:00Z', views: 756,
        answers: [
            { id: 'ans_10', authorName: 'David Lee', authorSchool: 'UC Berkeley', authorMajor: 'EECS', authorGradYear: 2024, authorAvatarColor: '#2980B9', text: 'I\'m a first-year engineer at Meta. WLB is team-dependent but generally good. My team does ~40-45 hours/week with flexibility to WFH 2-3 days. There are crunch periods around launches but managers are understanding. The free food and campus amenities are a nice perk too!', visibility: 'full', status: 'approved', createdAt: '2026-02-05T14:00:00Z', helpful: 44 }
        ]
    },
    {
        id: 'qa_08', authorName: 'Sam Patel', authorSchool: 'UC Berkeley', authorMajor: 'Business Administration', authorGradYear: 2027, authorAvatarColor: '#D35400',
        question: 'How important is GPA for consulting recruiting at MBB firms?',
        status: 'approved', createdAt: '2026-02-01T11:00:00Z', views: 1123,
        answers: [
            { id: 'ans_11', authorName: 'Anonymous', authorSchool: 'Harvard University', authorMajor: 'Economics', authorGradYear: 2025, authorAvatarColor: '#95A5A6', text: 'Very important for getting past the resume screen. 3.5+ is the general cutoff, 3.7+ is ideal. However, strong extracurriculars, leadership, and networking can sometimes compensate. Once you\'re in the interview, GPA barely matters - it\'s all about case performance and fit.', visibility: 'semi-anonymous', status: 'approved', createdAt: '2026-02-01T15:00:00Z', helpful: 63 }
        ]
    },
    {
        id: 'qa_09', authorName: 'Rachel Torres', authorSchool: 'Georgia Tech', authorMajor: 'Computer Science', authorGradYear: 2026, authorAvatarColor: '#1ABC9C',
        question: 'Should I accept a return offer or keep interviewing?',
        status: 'approved', createdAt: '2026-01-28T09:00:00Z', views: 534,
        answers: [
            { id: 'ans_12', authorName: 'Marcus Johnson', authorSchool: 'University of Michigan', authorMajor: 'Computer Science', authorGradYear: 2024, authorAvatarColor: '#F39C12', text: 'Depends on your situation. Return offers are great because you already know the team and culture. But if you\'re not excited about the role/team, keep interviewing. Ask for a deadline extension on the return offer (most companies give 2-4 weeks). Having a return offer as a safety net is a great position to interview from.', visibility: 'full', status: 'approved', createdAt: '2026-01-28T13:00:00Z', helpful: 35 }
        ]
    },
    {
        id: 'qa_10', authorName: 'Anonymous', authorSchool: 'University of Pennsylvania', authorMajor: 'Finance', authorGradYear: 2027, authorAvatarColor: '#95A5A6',
        question: 'What is the timeline for summer 2027 internship recruiting in finance?',
        status: 'approved', createdAt: '2026-01-25T14:00:00Z', views: 678,
        answers: []
    },
    {
        id: 'qa_11', authorName: 'Derek Williams', authorSchool: 'Morehouse College', authorMajor: 'Computer Science', authorGradYear: 2027, authorAvatarColor: '#1ABC9C',
        question: 'What diversity programs do big tech companies offer for underrepresented students?',
        status: 'approved', createdAt: '2026-01-20T10:00:00Z', views: 890,
        answers: [
            { id: 'ans_13', authorName: 'Aisha Mohammed', authorSchool: 'Howard University', authorMajor: 'Computer Engineering', authorGradYear: 2027, authorAvatarColor: '#9B59B6', text: 'Here are some I know of: Google STEP, Microsoft Explore, Meta University, Apple Pathways, Amazon Propel, Goldman Sachs Possibilities Summit. Also look into NSBE, SWE, and SHPE conferences - companies recruit heavily there. Handshake also surfaces diversity-focused programs if you update your profile.', visibility: 'full', status: 'approved', createdAt: '2026-01-20T16:00:00Z', helpful: 78 }
        ]
    },
    {
        id: 'qa_12', authorName: 'Sophia Williams', authorSchool: 'Harvard University', authorMajor: 'Government', authorGradYear: 2026, authorAvatarColor: '#A93226',
        question: 'How do you transition from a liberal arts background to a tech career?',
        status: 'approved', createdAt: '2026-01-15T11:00:00Z', views: 567,
        answers: [
            { id: 'ans_14', authorName: 'Nathan Brooks', authorSchool: 'Rice University', authorMajor: 'English', authorGradYear: 2025, authorAvatarColor: '#6C3483', text: 'I did this! Studied English, now work in tech PM. Key steps: 1) Take online CS courses (CS50, freeCodeCamp) 2) Build side projects 3) Target roles that value communication: PM, UX Research, Technical Writing, Sales Engineering 4) Leverage your unique perspective - liberal arts grads bring critical thinking that STEM grads sometimes lack.', visibility: 'full', status: 'approved', createdAt: '2026-01-15T16:00:00Z', helpful: 45 }
        ]
    }
];

// Current user's own questions
const MY_QUESTIONS = [
    { id: 'qa_07', status: 'approved' }
];

const MY_ANSWERS = [
    { questionId: 'qa_01', answerId: null }
];

// ============================================================
// Messages (from employers)
// ============================================================
const MESSAGES = [
    { id: 'msg_01', employerId: 'emp_01', employerName: 'Google', subject: 'You\'re a top match for Software Engineering Intern!', body: 'Hi Maya,\n\nBased on your profile, you\'re in the top 15% of candidates for our Software Engineering Intern position. We\'d love to see your application!\n\nThe role involves working on large-scale distributed systems with a team of experienced engineers. Applications close March 31st.\n\nBest,\nGoogle University Recruiting', isTopMatch: true, isRead: false, createdAt: '2026-03-06T08:00:00Z', type: 'recruiting' },
    { id: 'msg_02', employerId: 'emp_15', employerName: 'Anthropic', subject: 'Research Engineering Intern - Application Update', body: 'Hi Maya,\n\nThank you for your application to our Research Engineering Intern position. We were impressed by your background in ML and your research experience at Stanford AI Lab.\n\nWe\'d like to invite you to a phone screen. Please use the following link to schedule a time that works for you.\n\nBest regards,\nAnthropic Recruiting Team', isTopMatch: false, isRead: true, createdAt: '2026-03-05T10:00:00Z', type: 'recruiting' },
    { id: 'msg_03', employerId: 'emp_07', employerName: 'Meta', subject: 'Exclusive: ML Engineer Intern positions now open', body: 'Hi Maya,\n\nAs a student who has expressed interest in machine learning, we wanted to let you know about our ML Engineer Intern positions for Summer 2026. These roles are at the forefront of AI research and development.\n\nApply through Handshake by April 10th.\n\nMeta University Recruiting', isTopMatch: true, isRead: false, createdAt: '2026-03-04T14:00:00Z', type: 'promotional' },
    { id: 'msg_04', employerId: 'emp_04', employerName: 'McKinsey & Company', subject: 'McKinsey campus presentation - See you there?', body: 'Hi Maya,\n\nMcKinsey & Company is hosting a campus presentation at Stanford on March 15th. We\'ll discuss what it\'s like to work at McKinsey, share project examples, and provide tips for the case interview.\n\nRSVP through the Events page on Handshake.\n\nBest,\nMcKinsey Stanford Recruiting Team', isTopMatch: false, isRead: true, createdAt: '2026-03-03T09:00:00Z', type: 'event' },
    { id: 'msg_05', employerId: 'emp_03', employerName: 'Microsoft', subject: 'Your profile caught our attention!', body: 'Hi Maya,\n\nYour Handshake profile stood out to our recruiting team. With your experience in software engineering and product design, we think you\'d be a great fit for several roles at Microsoft.\n\nCheck out our open positions and consider applying to our Software Engineer Intern or Program Manager Intern roles.\n\nBest,\nMicrosoft University Recruiting', isTopMatch: false, isRead: true, createdAt: '2026-03-01T11:00:00Z', type: 'recruiting' },
    { id: 'msg_06', employerId: 'emp_10', employerName: 'Stripe', subject: 'Backend Engineer Intern - We think you\'d be great', body: 'Hi Maya,\n\nWe noticed your strong background in systems and algorithms. Our Backend Engineer Intern role might be a perfect fit for you.\n\nAt Stripe, interns work on real infrastructure powering millions of businesses. Apply by April 15th.\n\nCheers,\nStripe Recruiting', isTopMatch: false, isRead: false, createdAt: '2026-02-28T15:00:00Z', type: 'recruiting' },
    { id: 'msg_07', employerId: 'emp_09', employerName: 'Amazon', subject: 'Amazon SDE Intern - Apply Now', body: 'Dear Maya,\n\nAmazon is actively recruiting for SDE Intern positions across AWS, Alexa, and Amazon.com teams. With your CS background and prior internship experience, we encourage you to apply.\n\nThe application deadline is April 5th.\n\nAmazon University Programs', isTopMatch: false, isRead: true, createdAt: '2026-02-25T10:00:00Z', type: 'promotional' },
    { id: 'msg_08', employerId: 'emp_05', employerName: 'Apple', subject: 'Apple Pathways - Exclusive invitation', body: 'Hi Maya,\n\nYou\'ve been identified as a strong candidate for Apple\'s Pathways program, designed for exceptional students. This program offers unique mentorship and project opportunities.\n\nLearn more and apply through Handshake.\n\nApple University Recruiting', isTopMatch: true, isRead: false, createdAt: '2026-02-22T08:00:00Z', type: 'recruiting' },
    { id: 'msg_09', employerId: 'emp_02', employerName: 'JPMorgan Chase', subject: 'Tech Analyst Program - Applications Still Open', body: 'Hi Maya,\n\nOur Technology Analyst program combines finance and engineering. If you\'re interested in fintech, this is a unique opportunity to work at the intersection of banking and technology.\n\nApplications close April 20th.\n\nJPMorgan Chase Campus Recruiting', isTopMatch: false, isRead: true, createdAt: '2026-02-18T09:00:00Z', type: 'promotional' },
    { id: 'msg_10', employerId: 'emp_19', employerName: 'Salesforce', subject: 'Futureforce Internship Program', body: 'Hi Maya,\n\nJoin Salesforce\'s Futureforce program and help build the future of CRM and enterprise software. We offer software engineering, product management, and UX design internships.\n\nApply by April 30th.\n\nSalesforce University Recruiting', isTopMatch: false, isRead: true, createdAt: '2026-02-15T14:00:00Z', type: 'promotional' },
    { id: 'msg_11', employerId: 'emp_11', employerName: 'Bain & Company', subject: 'Bain Associate Consultant Intern - Application Reminder', body: 'Hi Maya,\n\nThis is a friendly reminder that applications for our Associate Consultant Intern position close on March 10th. Don\'t miss this opportunity to experience world-class consulting.\n\nBain & Company Recruiting', isTopMatch: false, isRead: true, createdAt: '2026-02-10T08:00:00Z', type: 'recruiting' },
    { id: 'msg_12', employerId: 'emp_12', employerName: 'Tesla', subject: 'Tesla Summer Internships - Engineering', body: 'Hello Maya,\n\nTesla is looking for passionate engineers to join us this summer. While our focus includes mechanical and electrical engineering, we also have software roles in AI, robotics, and embedded systems.\n\nExplore open positions on Handshake.\n\nTesla Recruiting', isTopMatch: false, isRead: true, createdAt: '2026-02-05T11:00:00Z', type: 'promotional' }
];

// ============================================================
// Labels (school-defined)
// ============================================================
const SCHOOL_LABELS = [
    'STEM', 'Top Employer', 'Finance', 'Consulting', 'AI/ML', 'Design',
    'Healthcare', 'Startup', 'Remote-Friendly', 'Research', 'Nonprofit',
    'Government', 'Media', 'Manufacturing', 'Marketing', 'Education',
    'Consumer', 'Quantitative', 'Policy', 'Retail', 'Technology'
];

// ============================================================
// Feed Filter Options
// ============================================================
const FEED_FILTERS = ['All', 'Employers', 'Top Posts', 'Intros'];

// ============================================================
// Appointment Available Dates (for scheduling)
// ============================================================
const AVAILABLE_APPOINTMENT_SLOTS = [
    { date: '2026-03-10', times: ['9:00 AM', '10:00 AM', '2:00 PM', '3:00 PM'], staffAvailable: ['staff_01', 'staff_02', 'staff_06'] },
    { date: '2026-03-11', times: ['10:00 AM', '11:00 AM', '1:00 PM'], staffAvailable: ['staff_03', 'staff_04', 'staff_05'] },
    { date: '2026-03-12', times: ['9:00 AM', '11:00 AM', '2:00 PM', '4:00 PM'], staffAvailable: ['staff_01', 'staff_04', 'staff_06'] },
    { date: '2026-03-13', times: ['10:00 AM', '1:00 PM', '3:00 PM'], staffAvailable: ['staff_02', 'staff_03', 'staff_05'] },
    { date: '2026-03-14', times: ['9:00 AM', '11:00 AM', '2:00 PM'], staffAvailable: ['staff_01', 'staff_06'] },
    { date: '2026-03-17', times: ['9:00 AM', '10:00 AM', '1:00 PM', '3:00 PM'], staffAvailable: ['staff_01', 'staff_02', 'staff_04'] },
    { date: '2026-03-18', times: ['10:00 AM', '11:00 AM', '2:00 PM'], staffAvailable: ['staff_03', 'staff_05', 'staff_06'] },
    { date: '2026-03-19', times: ['9:00 AM', '1:00 PM', '3:00 PM', '4:00 PM'], staffAvailable: ['staff_01', 'staff_04'] },
    { date: '2026-03-20', times: ['10:00 AM', '2:00 PM'], staffAvailable: ['staff_02', 'staff_03'] },
    { date: '2026-03-21', times: ['9:00 AM', '11:00 AM', '1:00 PM', '3:00 PM'], staffAvailable: ['staff_04', 'staff_05', 'staff_06'] },
    { date: '2026-03-24', times: ['9:00 AM', '10:00 AM', '2:00 PM'], staffAvailable: ['staff_01', 'staff_02'] },
    { date: '2026-03-25', times: ['11:00 AM', '1:00 PM', '3:00 PM'], staffAvailable: ['staff_03', 'staff_04', 'staff_06'] },
    { date: '2026-03-26', times: ['9:00 AM', '10:00 AM', '1:00 PM', '4:00 PM'], staffAvailable: ['staff_01', 'staff_05'] },
    { date: '2026-03-27', times: ['10:00 AM', '2:00 PM', '3:00 PM'], staffAvailable: ['staff_02', 'staff_04', 'staff_06'] },
    { date: '2026-03-28', times: ['9:00 AM', '11:00 AM', '1:00 PM'], staffAvailable: ['staff_03', 'staff_05'] }
];

// ============================================================
// Event Type Filter Options
// ============================================================
const EVENT_TYPE_OPTIONS = ['All Types', 'Info Session', 'Career Fair', 'Tech Talk', 'Workshop', 'Panel', 'Speaker Event', 'Virtual Session'];
