const Views = {
    // ============================================================
    // SIDEBAR
    // ============================================================
    renderSidebar() {
        const pages = [
            { id: 'feed', label: 'Feed', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="3" width="16" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="2" y="9" width="16" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="2" y="15" width="10" height="2" rx="1" stroke="currentColor" stroke-width="1.5"/></svg>' },
            { id: 'jobs', label: 'Jobs', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="3" y="6" width="14" height="11" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M7 6V4a2 2 0 012-2h2a2 2 0 012 2v2" stroke="currentColor" stroke-width="1.5"/></svg>' },
            { id: 'employers', label: 'Employers', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="4" width="16" height="13" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M7 10h6M10 7v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>' },
            { id: 'events', label: 'Events', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="3" width="16" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M2 7h16M6 1v4M14 1v4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>' },
            { id: 'messages', label: 'Messages', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 4h14a1 1 0 011 1v9a1 1 0 01-1 1H6l-3 3V5a1 1 0 011-1z" stroke="currentColor" stroke-width="1.5"/></svg>', badge: AppState.getUnreadMessageCount() },
            { id: 'career-center', label: 'Career Center', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="7" r="4" stroke="currentColor" stroke-width="1.5"/><path d="M3 18c0-3.87 3.13-7 7-7s7 3.13 7 7" stroke="currentColor" stroke-width="1.5"/></svg>' },
            { id: 'qa', label: 'Q&A', icon: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/><path d="M7 8a3 3 0 015.2 2c0 2-3 2-3 4M10 16v0" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>' }
        ];

        return `
            <div class="sidebar-header">
                <div class="sidebar-logo">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#E44D2E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <span class="sidebar-logo-text">Handshake</span>
                </div>
            </div>
            <nav class="sidebar-nav">
                ${pages.map(p => `
                    <button class="sidebar-item ${AppState.currentPage === p.id ? 'active' : ''}" data-action="navigate" data-page="${p.id}">
                        <span class="sidebar-icon">${p.icon}</span>
                        <span class="sidebar-text">${p.label}</span>
                        ${p.badge ? Components.notificationDot(p.badge) : ''}
                    </button>
                `).join('')}
            </nav>
            <div class="sidebar-footer">
                <div class="sidebar-user" data-action="navigate" data-page="profile">
                    ${Components.avatar(AppState.currentUser.fullName, AppState.currentUser.avatarColor, 'small')}
                    <div class="sidebar-user-info">
                        <div class="sidebar-user-name">${AppState.currentUser.fullName}</div>
                        <div class="sidebar-user-school">${AppState.currentUser.school}</div>
                    </div>
                </div>
            </div>
        `;
    },

    // ============================================================
    // MAIN CONTENT ROUTER
    // ============================================================
    renderContent() {
        switch (AppState.currentPage) {
            case 'feed': return this.renderFeed();
            case 'jobs': return this.renderJobs();
            case 'employers': return this.renderEmployers();
            case 'employer-detail': return this.renderEmployerDetail();
            case 'job-detail': return this.renderJobDetail();
            case 'events': return this.renderEvents();
            case 'event-detail': return this.renderEventDetail();
            case 'messages': return this.renderMessages();
            case 'message-detail': return this.renderMessageDetail();
            case 'career-center': return this.renderCareerCenter();
            case 'appointment-detail': return this.renderAppointmentDetail();
            case 'schedule-appointment': return this.renderScheduleAppointment();
            case 'qa': return this.renderQA();
            case 'question-detail': return this.renderQuestionDetail();
            case 'profile': return this.renderProfile();
            case 'career-interests': return this.renderCareerInterests();
            default: return this.renderFeed();
        }
    },

    // ============================================================
    // FEED
    // ============================================================
    renderFeed() {
        const tabs = [
            { id: 'feed', label: 'Feed' },
            { id: 'saved', label: 'Saved' }
        ];
        const isSaved = AppState.feedTab === 'saved';
        const posts = isSaved ? AppState.getSavedPosts() : AppState.getFilteredFeedPosts();

        return `
            <div class="page-feed">
                ${Components.sectionHeader('Feed', 'Stay connected with your career community')}
                ${Components.tabBar(tabs, AppState.feedTab, 'setFeedTab')}

                ${!isSaved ? `
                    ${(AppState.currentUser.profileVisibility === 'Community' || AppState.currentUser.profileVisibility === 'Public') ? `
                    <div class="create-post-box" data-action="openCreatePost">
                        ${Components.avatar(AppState.currentUser.fullName, AppState.currentUser.avatarColor, 'small')}
                        <span class="create-post-placeholder">Share something with the community...</span>
                    </div>
                    ` : ''}
                    ${Components.filterChips(FEED_FILTERS, AppState.feedFilter, 'setFeedFilter')}
                ` : ''}

                <div class="feed-posts">
                    ${posts.length === 0 ? Components.emptyState(
                        '<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect x="6" y="10" width="36" height="8" rx="2" stroke="#ccc" stroke-width="2"/><rect x="6" y="22" width="36" height="8" rx="2" stroke="#ccc" stroke-width="2"/><rect x="6" y="34" width="24" height="4" rx="2" stroke="#ccc" stroke-width="2"/></svg>',
                        isSaved ? 'No saved posts yet' : 'No posts match this filter',
                        isSaved ? 'Bookmark posts to save them here' : 'Try a different filter to see more posts'
                    ) : posts.map(p => this._renderFeedPost(p)).join('')}
                </div>
                ${posts.length > 0 ? Components.paginationInfo(posts.length, AppState.feedPosts.length) : ''}
            </div>
        `;
    },

    _renderFeedPost(post) {
        const isEmployer = post.authorType === 'employer';
        const isFollowed = isEmployer && AppState.currentUser.followedEmployerIds.includes(post.authorId);
        return `
            <div class="feed-post" data-post-id="${post.id}">
                <div class="feed-post-header">
                    ${Components.avatar(post.authorName, post.authorAvatarColor, 'medium')}
                    <div class="feed-post-author-info">
                        <div class="feed-post-author-row">
                            <span class="feed-post-author-name ${isEmployer ? 'employer-name' : ''}" ${isEmployer ? `data-action="viewEmployer" data-employer-id="${post.authorId}"` : ''}>${post.authorName}</span>
                            ${isEmployer && !isFollowed ? `<button class="btn-follow-small" data-action="followEmployer" data-employer-id="${post.authorId}">+ Follow</button>` : ''}
                        </div>
                        <div class="feed-post-meta">
                            ${post.authorSchool ? `${post.authorSchool} &middot; ` : ''}
                            ${Components.timeAgo(post.createdAt)}
                            ${post.audience === 'school' ? ' &middot; <span class="audience-badge">Your school</span>' : ''}
                        </div>
                    </div>
                    <div class="feed-post-menu">
                        <button class="icon-btn" data-action="togglePostMenu" data-post-id="${post.id}"><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="3" cy="8" r="1.5" fill="currentColor"/><circle cx="8" cy="8" r="1.5" fill="currentColor"/><circle cx="13" cy="8" r="1.5" fill="currentColor"/></svg></button>
                    </div>
                </div>
                <div class="feed-post-content">${this._formatPostContent(post.content)}</div>
                <div class="feed-post-actions">
                    <button class="post-action-btn ${post.likes > 0 ? 'liked' : ''}" data-action="likePost" data-post-id="${post.id}">
                        <svg width="18" height="18" viewBox="0 0 18 18" fill="${post.likes > 0 ? '#E44D2E' : 'none'}"><path d="M9 15.5s-6.5-4-6.5-8A3.5 3.5 0 019 4.5a3.5 3.5 0 016.5 3c0 4-6.5 8-6.5 8z" stroke="${post.likes > 0 ? '#E44D2E' : 'currentColor'}" stroke-width="1.5"/></svg>
                        <span>${post.likes || ''}</span>
                    </button>
                    <button class="post-action-btn" data-action="openComments" data-post-id="${post.id}">
                        <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2 4h14v9H5l-3 3V4z" stroke="currentColor" stroke-width="1.5"/></svg>
                        <span>${post.comments.length || ''}</span>
                    </button>
                    <button class="post-action-btn ${post.bookmarked ? 'bookmarked' : ''}" data-action="bookmarkPost" data-post-id="${post.id}">
                        <svg width="18" height="18" viewBox="0 0 18 18" fill="${post.bookmarked ? '#4A90D9' : 'none'}"><path d="M4 2h10v14l-5-3-5 3V2z" stroke="${post.bookmarked ? '#4A90D9' : 'currentColor'}" stroke-width="1.5"/></svg>
                    </button>
                </div>
                ${post.comments.length > 0 ? `
                    <div class="feed-post-comments">
                        ${post.comments.slice(-2).map(c => `
                            <div class="comment">
                                ${Components.avatar(c.authorName, c.authorAvatarColor, 'tiny')}
                                <div class="comment-body">
                                    <span class="comment-author">${c.authorName}</span>
                                    <span class="comment-text">${c.text}</span>
                                    <span class="comment-time">${Components.timeAgo(c.createdAt)}</span>
                                </div>
                            </div>
                        `).join('')}
                        ${post.comments.length > 2 ? `<button class="view-all-comments" data-action="openComments" data-post-id="${post.id}">View all ${post.comments.length} comments</button>` : ''}
                    </div>
                ` : ''}
            </div>
        `;
    },

    _formatPostContent(text) {
        if (!text) return '';
        return text.replace(/\n/g, '<br>').replace(/#(\w+)/g, '<span class="hashtag">#$1</span>');
    },

    // ============================================================
    // JOBS
    // ============================================================
    renderJobs() {
        const jobs = AppState.getFilteredJobs();
        const savedJobIds = AppState.currentUser.savedJobIds;

        return `
            <div class="page-jobs">
                ${Components.sectionHeader('Jobs', 'Find internships and full-time positions')}
                <div class="jobs-toolbar">
                    ${Components.searchInput('jobSearch', 'Search jobs, companies, keywords...', AppState.jobSearchQuery)}
                    <div class="jobs-filters">
                        ${Components.dropdown('jobTypeFilter', AppState.jobFilters.type, ['', 'Internship', 'Full-time', 'Part-time'], 'Job Type')}
                        ${Components.dropdown('jobLocationFilter', AppState.jobFilters.location, ['', ...LOCATION_OPTIONS.slice(0, 10)], 'Location')}
                        ${Components.dropdown('jobLabelFilter', AppState.jobFilters.label, ['', ...SCHOOL_LABELS], 'Label')}
                    </div>
                </div>
                ${Components.paginationInfo(jobs.length, AppState.jobs.length)}
                <div class="jobs-list">
                    ${jobs.length === 0 ? Components.emptyState(
                        '<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect x="8" y="14" width="32" height="24" rx="3" stroke="#ccc" stroke-width="2"/><path d="M16 14V10a4 4 0 014-4h8a4 4 0 014 4v4" stroke="#ccc" stroke-width="2"/></svg>',
                        'No jobs found',
                        'Try adjusting your search or filters'
                    ) : jobs.map(j => {
                        const emp = AppState.getEmployerById(j.employerId);
                        const isSaved = savedJobIds.includes(j.id);
                        return `
                            <div class="job-card" data-action="viewJob" data-job-id="${j.id}">
                                <div class="job-card-left">
                                    ${Components.avatar(emp ? emp.name : '?', emp ? emp.logoColor : '#ccc', 'medium')}
                                </div>
                                <div class="job-card-info">
                                    <div class="job-card-title">${j.title}</div>
                                    <div class="job-card-company">${emp ? emp.name : 'Unknown'}</div>
                                    <div class="job-card-meta">
                                        <span>${j.location}</span>
                                        <span class="meta-sep">&middot;</span>
                                        <span>${j.type}</span>
                                        <span class="meta-sep">&middot;</span>
                                        <span>${j.salary}</span>
                                    </div>
                                    <div class="job-card-tags">
                                        ${(j.labels || []).map(l => `<span class="job-label">${l}</span>`).join('')}
                                        ${j.status === 'closed' ? '<span class="job-label job-label-closed">Closed</span>' : ''}
                                    </div>
                                </div>
                                <div class="job-card-right">
                                    <button class="icon-btn bookmark-btn ${isSaved ? 'saved' : ''}" data-action="${isSaved ? 'unsaveJob' : 'saveJob'}" data-job-id="${j.id}">
                                        <svg width="20" height="20" viewBox="0 0 20 20" fill="${isSaved ? '#4A90D9' : 'none'}"><path d="M4 2h12v16l-6-3-6 3V2z" stroke="${isSaved ? '#4A90D9' : 'currentColor'}" stroke-width="1.5"/></svg>
                                    </button>
                                    <div class="job-card-posted">${Components.timeAgo(j.postedAt)}</div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    },

    // ============================================================
    // JOB DETAIL
    // ============================================================
    renderJobDetail() {
        const job = AppState.getJobById(AppState.selectedJobId);
        if (!job) return Components.emptyState('', 'Job not found', '');
        const emp = AppState.getEmployerById(job.employerId);
        const isSaved = AppState.currentUser.savedJobIds.includes(job.id);
        const isFollowed = emp && AppState.currentUser.followedEmployerIds.includes(emp.id);

        return `
            <div class="page-detail">
                <button class="back-btn" data-action="navigate" data-page="jobs"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Jobs</button>
                <div class="detail-header">
                    <div class="detail-header-left">
                        ${emp ? Components.avatar(emp.name, emp.logoColor, 'large') : ''}
                        <div>
                            <h1 class="detail-title">${job.title}</h1>
                            <div class="detail-subtitle" data-action="viewEmployer" data-employer-id="${job.employerId}">${emp ? emp.name : 'Unknown'}</div>
                        </div>
                    </div>
                    <div class="detail-header-right">
                        <button class="btn btn-outline ${isSaved ? 'saved' : ''}" data-action="${isSaved ? 'unsaveJob' : 'saveJob'}" data-job-id="${job.id}">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="${isSaved ? '#4A90D9' : 'none'}"><path d="M3 1h10v14l-5-3-5 3V1z" stroke="${isSaved ? '#4A90D9' : 'currentColor'}" stroke-width="1.5"/></svg>
                            ${isSaved ? 'Saved' : 'Save'}
                        </button>
                    </div>
                </div>

                <div class="detail-meta-row">
                    <span class="detail-meta-item"><strong>Location:</strong> ${job.location}</span>
                    <span class="detail-meta-item"><strong>Type:</strong> ${job.type}</span>
                    <span class="detail-meta-item"><strong>Salary:</strong> ${job.salary}</span>
                    <span class="detail-meta-item"><strong>Posted:</strong> ${Components.timeAgo(job.postedAt)}</span>
                    <span class="detail-meta-item"><strong>Deadline:</strong> ${Components.formatDate(job.deadline ? job.deadline.split('T')[0] : '')}</span>
                    <span class="detail-meta-item"><strong>Applicants:</strong> ${job.applicants ? job.applicants.toLocaleString() : 'N/A'}</span>
                </div>

                <div class="detail-tags">
                    ${(job.labels || []).map(l => `<span class="job-label">${l}</span>`).join('')}
                    ${(job.roles || []).map(r => `<span class="job-label role-label">${r}</span>`).join('')}
                    ${job.status === 'closed' ? '<span class="job-label job-label-closed">Applications Closed</span>' : ''}
                </div>

                <div class="detail-section">
                    <h3>Description</h3>
                    <p>${job.description}</p>
                </div>

                <div class="detail-section">
                    <h3>Qualifications</h3>
                    <p>${job.qualifications}</p>
                </div>

                ${emp ? `
                <div class="detail-section employer-about-section">
                    <h3>About ${emp.name}</h3>
                    <div class="employer-mini-card" data-action="viewEmployer" data-employer-id="${emp.id}">
                        ${Components.avatar(emp.name, emp.logoColor, 'medium')}
                        <div class="employer-mini-info">
                            <div class="employer-mini-name">${emp.name}</div>
                            <div class="employer-mini-meta">${emp.industry} &middot; ${emp.location} &middot; ${emp.size}</div>
                        </div>
                        <button class="btn btn-sm ${isFollowed ? 'btn-outline' : 'btn-primary'}" data-action="${isFollowed ? 'unfollowEmployer' : 'followEmployer'}" data-employer-id="${emp.id}">
                            ${isFollowed ? 'Following' : 'Follow'}
                        </button>
                    </div>
                </div>
                ` : ''}
            </div>
        `;
    },

    // ============================================================
    // EMPLOYERS
    // ============================================================
    renderEmployers() {
        const employers = AppState.getFilteredEmployers();

        return `
            <div class="page-employers">
                ${Components.sectionHeader('Employers', 'Explore companies and follow the ones you love')}
                ${Components.searchInput('employerSearch', 'Search employers by name, industry, or location...', AppState.employerSearchQuery)}
                ${Components.paginationInfo(employers.length, AppState.employers.length)}
                <div class="employers-grid">
                    ${employers.map(emp => {
                        const isFollowed = AppState.currentUser.followedEmployerIds.includes(emp.id);
                        return `
                            <div class="employer-card" data-action="viewEmployer" data-employer-id="${emp.id}">
                                <div class="employer-card-header">
                                    ${Components.avatar(emp.name, emp.logoColor, 'large')}
                                    <button class="btn btn-sm ${isFollowed ? 'btn-outline' : 'btn-primary'}" data-action="${isFollowed ? 'unfollowEmployer' : 'followEmployer'}" data-employer-id="${emp.id}">
                                        ${isFollowed ? 'Following' : 'Follow'}
                                    </button>
                                </div>
                                <div class="employer-card-name">${emp.name}</div>
                                <div class="employer-card-meta">${emp.industry} &middot; ${emp.location}</div>
                                <div class="employer-card-meta">${emp.size} &middot; ${emp.type}</div>
                                <div class="employer-card-followers">${emp.followCount.toLocaleString()} followers</div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    },

    // ============================================================
    // EMPLOYER DETAIL (Brand Page)
    // ============================================================
    renderEmployerDetail() {
        const emp = AppState.getEmployerById(AppState.selectedEmployerId);
        if (!emp) return Components.emptyState('', 'Employer not found', '');
        const isFollowed = AppState.currentUser.followedEmployerIds.includes(emp.id);
        const tabs = [
            { id: 'overview', label: 'Overview' },
            { id: 'jobs', label: 'Jobs' },
            { id: 'posts', label: 'Posts' }
        ];

        return `
            <div class="page-detail">
                <button class="back-btn" data-action="navigate" data-page="employers"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Employers</button>
                <div class="employer-brand-header">
                    <div class="employer-brand-banner" style="background-color: ${emp.logoColor}20">
                        ${Components.avatar(emp.name, emp.logoColor, 'xlarge')}
                    </div>
                    <div class="employer-brand-info">
                        <div class="employer-brand-row">
                            <div>
                                <h1 class="employer-brand-name">${emp.name}</h1>
                                <div class="employer-brand-meta">${emp.industry} &middot; ${emp.location} &middot; ${emp.size} &middot; ${emp.type}</div>
                                <div class="employer-brand-meta">${emp.followCount.toLocaleString()} followers &middot; <a href="#">${emp.website}</a></div>
                            </div>
                            <button class="btn ${isFollowed ? 'btn-outline' : 'btn-primary'}" data-action="${isFollowed ? 'unfollowEmployer' : 'followEmployer'}" data-employer-id="${emp.id}">
                                ${isFollowed ? 'Following' : 'Follow'}
                            </button>
                        </div>
                    </div>
                </div>

                ${Components.tabBar(tabs, AppState.selectedEmployerTab, 'setEmployerTab')}

                ${this._renderEmployerTabContent(emp)}
            </div>
        `;
    },

    _renderEmployerTabContent(emp) {
        switch (AppState.selectedEmployerTab) {
            case 'jobs': return this._renderEmployerJobs(emp);
            case 'posts': return this._renderEmployerPosts(emp);
            default: return this._renderEmployerOverview(emp);
        }
    },

    _renderEmployerOverview(emp) {
        const jobs = AppState.getJobsByEmployer(emp.id).slice(0, 3);
        const events = AppState.getEventsByEmployer(emp.id).slice(0, 3);
        const posts = AppState.getPostsByEmployer(emp.id).slice(0, 2);

        return `
            <div class="employer-overview">
                <div class="detail-section">
                    <h3>About</h3>
                    <p>${emp.about}</p>
                </div>

                ${emp.workLife ? `
                <div class="detail-section">
                    <h3>Work Life</h3>
                    <p>${emp.workLife}</p>
                </div>
                ` : ''}

                ${emp.testimonials && emp.testimonials.length > 0 ? `
                <div class="detail-section">
                    <h3>Testimonials</h3>
                    <div class="testimonials-list">
                        ${emp.testimonials.map(t => `
                            <div class="testimonial-card">
                                <p class="testimonial-text">"${t.text}"</p>
                                <div class="testimonial-author">
                                    <strong>${t.name}</strong> &middot; ${t.role} &middot; ${t.school} &middot; Class of ${t.gradYear}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}

                ${jobs.length > 0 ? `
                <div class="detail-section">
                    <h3>Jobs</h3>
                    ${jobs.map(j => `
                        <div class="mini-job-card" data-action="viewJob" data-job-id="${j.id}">
                            <div class="mini-job-title">${j.title}</div>
                            <div class="mini-job-meta">${j.location} &middot; ${j.type} &middot; ${j.salary}</div>
                        </div>
                    `).join('')}
                    ${AppState.getJobsByEmployer(emp.id).length > 3 ? `<button class="btn-link" data-action="setEmployerTab" data-tab="jobs">View all jobs</button>` : ''}
                </div>
                ` : ''}

                ${events.length > 0 ? `
                <div class="detail-section">
                    <h3>Events</h3>
                    ${events.map(e => `
                        <div class="mini-event-card" data-action="viewEvent" data-event-id="${e.id}">
                            <div class="mini-event-date">${Components.formatDateShort(e.date)}</div>
                            <div>
                                <div class="mini-event-title">${e.title}</div>
                                <div class="mini-event-meta">${e.time} &middot; ${e.location}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                ` : ''}

                ${posts.length > 0 ? `
                <div class="detail-section">
                    <h3>Posts</h3>
                    ${posts.map(p => this._renderFeedPost(p)).join('')}
                    ${AppState.getPostsByEmployer(emp.id).length > 2 ? `<button class="btn-link" data-action="setEmployerTab" data-tab="posts">View all posts</button>` : ''}
                </div>
                ` : ''}

                ${emp.affiliatedEmployers && emp.affiliatedEmployers.length > 0 ? `
                <div class="detail-section">
                    <h3>Affiliated Employers</h3>
                    <div class="affiliated-list">
                        ${emp.affiliatedEmployers.map(a => `<span class="affiliated-badge">${a}</span>`).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        `;
    },

    _renderEmployerJobs(emp) {
        const jobs = AppState.getJobsByEmployer(emp.id);
        return `
            <div class="employer-jobs-tab">
                ${jobs.length === 0 ? Components.emptyState('', 'No active jobs', 'Check back later for new opportunities') :
                    jobs.map(j => {
                        const isSaved = AppState.currentUser.savedJobIds.includes(j.id);
                        return `
                            <div class="job-card" data-action="viewJob" data-job-id="${j.id}">
                                <div class="job-card-info">
                                    <div class="job-card-title">${j.title}</div>
                                    <div class="job-card-meta">
                                        <span>${j.location}</span><span class="meta-sep">&middot;</span>
                                        <span>${j.type}</span><span class="meta-sep">&middot;</span>
                                        <span>${j.salary}</span>
                                    </div>
                                    <div class="job-card-tags">
                                        ${(j.labels || []).map(l => `<span class="job-label">${l}</span>`).join('')}
                                    </div>
                                </div>
                                <button class="icon-btn bookmark-btn ${isSaved ? 'saved' : ''}" data-action="${isSaved ? 'unsaveJob' : 'saveJob'}" data-job-id="${j.id}">
                                    <svg width="20" height="20" viewBox="0 0 20 20" fill="${isSaved ? '#4A90D9' : 'none'}"><path d="M4 2h12v16l-6-3-6 3V2z" stroke="${isSaved ? '#4A90D9' : 'currentColor'}" stroke-width="1.5"/></svg>
                                </button>
                            </div>
                        `;
                    }).join('')
                }
            </div>
        `;
    },

    _renderEmployerPosts(emp) {
        const posts = AppState.getPostsByEmployer(emp.id);
        return `
            <div class="employer-posts-tab">
                ${posts.length === 0 ? Components.emptyState('', 'No posts yet', '') : posts.map(p => this._renderFeedPost(p)).join('')}
            </div>
        `;
    },

    // ============================================================
    // EVENTS
    // ============================================================
    renderEvents() {
        const events = AppState.getFilteredEvents();
        const upcoming = events.filter(e => e.status === 'upcoming');
        const past = events.filter(e => e.status === 'past');

        return `
            <div class="page-events">
                ${Components.sectionHeader('Events', 'Discover career fairs, info sessions, and workshops')}
                <div class="events-toolbar">
                    ${Components.searchInput('eventSearch', 'Search events...', AppState.eventSearchQuery)}
                    <div class="events-filters">
                        ${Components.dropdown('eventTypeFilter', AppState.eventTypeFilter, EVENT_TYPE_OPTIONS, 'Event Type')}
                        <label class="checkbox-row inline-filter" data-checkbox-id="virtualOnly">
                            <div class="custom-checkbox ${AppState.eventShowVirtualOnly ? 'checked' : ''}" id="virtualOnly">
                                ${AppState.eventShowVirtualOnly ? '<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6L5 9L10 3" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>' : ''}
                            </div>
                            <span class="checkbox-label">Virtual only</span>
                        </label>
                    </div>
                </div>

                ${upcoming.length > 0 ? `
                    <h3 class="list-section-title">Upcoming Events</h3>
                    <div class="events-list">
                        ${upcoming.map(e => this._renderEventCard(e)).join('')}
                    </div>
                ` : ''}

                ${past.length > 0 ? `
                    <h3 class="list-section-title">Past Events</h3>
                    <div class="events-list">
                        ${past.map(e => this._renderEventCard(e)).join('')}
                    </div>
                ` : ''}

                ${events.length === 0 ? Components.emptyState(
                    '<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect x="6" y="8" width="36" height="32" rx="3" stroke="#ccc" stroke-width="2"/><path d="M6 16h36M14 4v8M34 4v8" stroke="#ccc" stroke-width="2"/></svg>',
                    'No events found',
                    'Try adjusting your search or filters'
                ) : ''}
            </div>
        `;
    },

    _renderEventCard(evt) {
        return `
            <div class="event-card" data-action="viewEvent" data-event-id="${evt.id}">
                <div class="event-card-date">
                    <div class="event-date-month">${new Date(evt.date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short' })}</div>
                    <div class="event-date-day">${new Date(evt.date + 'T00:00:00').getDate()}</div>
                </div>
                <div class="event-card-info">
                    <div class="event-card-title">${evt.title}</div>
                    <div class="event-card-meta">${evt.employerName} &middot; ${evt.type}</div>
                    <div class="event-card-meta">${evt.time} &middot; ${evt.location}</div>
                    <div class="event-card-tags">
                        ${(evt.labels || []).map(l => `<span class="event-label">${l}</span>`).join('')}
                        ${evt.isVirtual ? '<span class="event-label virtual-label">Virtual</span>' : ''}
                    </div>
                </div>
                <div class="event-card-right">
                    <div class="event-rsvp-count">${evt.rsvpCount} attending</div>
                    ${evt.status === 'upcoming' ? `
                        <button class="btn btn-sm ${evt.rsvped ? 'btn-outline' : 'btn-primary'}" data-action="${evt.rsvped ? 'cancelRsvp' : 'rsvpEvent'}" data-event-id="${evt.id}">
                            ${evt.rsvped ? 'Cancel RSVP' : 'RSVP'}
                        </button>
                    ` : '<span class="event-past-label">Past</span>'}
                </div>
            </div>
        `;
    },

    // ============================================================
    // EVENT DETAIL
    // ============================================================
    renderEventDetail() {
        const evt = AppState.events.find(e => e.id === AppState.selectedEventId);
        if (!evt) return Components.emptyState('', 'Event not found', '');

        return `
            <div class="page-detail">
                <button class="back-btn" data-action="navigate" data-page="events"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Events</button>
                <div class="detail-header">
                    <div>
                        <h1 class="detail-title">${evt.title}</h1>
                        <div class="detail-subtitle">${evt.employerName}</div>
                    </div>
                    ${evt.status === 'upcoming' ? `
                        <button class="btn ${evt.rsvped ? 'btn-outline' : 'btn-primary'}" data-action="${evt.rsvped ? 'cancelRsvp' : 'rsvpEvent'}" data-event-id="${evt.id}">
                            ${evt.rsvped ? 'Cancel RSVP' : 'RSVP'}
                        </button>
                    ` : ''}
                </div>
                <div class="detail-meta-row">
                    <span class="detail-meta-item"><strong>Date:</strong> ${Components.formatDate(evt.date)}</span>
                    <span class="detail-meta-item"><strong>Time:</strong> ${evt.time}</span>
                    <span class="detail-meta-item"><strong>Location:</strong> ${evt.location}</span>
                    <span class="detail-meta-item"><strong>Type:</strong> ${evt.type}</span>
                    <span class="detail-meta-item"><strong>Attending:</strong> ${evt.rsvpCount}</span>
                </div>
                <div class="detail-tags">
                    ${(evt.labels || []).map(l => `<span class="event-label">${l}</span>`).join('')}
                    ${evt.isVirtual ? '<span class="event-label virtual-label">Virtual</span>' : ''}
                </div>
                <div class="detail-section">
                    <h3>Description</h3>
                    <p>${evt.description}</p>
                </div>
                ${evt.employerId ? `
                <div class="detail-section">
                    <button class="btn btn-outline" data-action="viewEmployer" data-employer-id="${evt.employerId}">View ${evt.employerName} Profile</button>
                </div>
                ` : ''}
            </div>
        `;
    },

    // ============================================================
    // MESSAGES
    // ============================================================
    renderMessages() {
        const msgs = AppState.getFilteredMessages();
        const unread = AppState.getUnreadMessageCount();
        const filterTabs = [
            { id: 'all', label: 'All' },
            { id: 'unread', label: 'Unread', count: unread },
            { id: 'top-match', label: 'Top Match' }
        ];

        return `
            <div class="page-messages">
                <div class="messages-header">
                    ${Components.sectionHeader('Messages', 'Messages from employers')}
                    ${unread > 0 ? `<button class="btn btn-sm btn-outline" data-action="markAllRead">Mark all as read</button>` : ''}
                </div>
                ${Components.tabBar(filterTabs, AppState.messageFilter, 'setMessageFilter')}
                <div class="messages-list">
                    ${msgs.length === 0 ? Components.emptyState(
                        '<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><path d="M8 12h32v24H14l-6 6V12z" stroke="#ccc" stroke-width="2"/></svg>',
                        'No messages',
                        AppState.messageFilter === 'unread' ? 'All messages have been read' : 'No messages match this filter'
                    ) : msgs.map(m => `
                        <div class="message-row ${m.isRead ? '' : 'unread'}" data-action="viewMessage" data-message-id="${m.id}">
                            <div class="message-row-left">
                                ${Components.avatar(m.employerName, AppState.getEmployerById(m.employerId)?.logoColor || '#ccc', 'medium')}
                            </div>
                            <div class="message-row-content">
                                <div class="message-row-header">
                                    <span class="message-sender">${m.employerName}</span>
                                    ${m.isTopMatch ? '<span class="top-match-badge">Top Match</span>' : ''}
                                    <span class="message-time">${Components.timeAgo(m.createdAt)}</span>
                                </div>
                                <div class="message-subject">${m.subject}</div>
                                <div class="message-preview">${Components.truncate(m.body.replace(/\n/g, ' '), 100)}</div>
                            </div>
                            ${!m.isRead ? '<div class="unread-dot"></div>' : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    },

    // ============================================================
    // MESSAGE DETAIL
    // ============================================================
    renderMessageDetail() {
        const msg = AppState.messages.find(m => m.id === AppState.selectedMessageId);
        if (!msg) return Components.emptyState('', 'Message not found', '');
        const emp = AppState.getEmployerById(msg.employerId);

        return `
            <div class="page-detail">
                <button class="back-btn" data-action="navigate" data-page="messages"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Messages</button>
                <div class="message-detail-header">
                    ${Components.avatar(msg.employerName, emp?.logoColor || '#ccc', 'large')}
                    <div>
                        <h2 class="message-detail-subject">${msg.subject}</h2>
                        <div class="message-detail-from">
                            From: <strong>${msg.employerName}</strong>
                            ${msg.isTopMatch ? '<span class="top-match-badge">Top Match</span>' : ''}
                            &middot; ${Components.timeAgo(msg.createdAt)}
                        </div>
                    </div>
                </div>
                <div class="message-detail-body">${msg.body.replace(/\n/g, '<br>')}</div>
                ${emp ? `
                <div class="detail-section">
                    <button class="btn btn-outline" data-action="viewEmployer" data-employer-id="${emp.id}">View ${emp.name} Profile</button>
                </div>
                ` : ''}
            </div>
        `;
    },

    // ============================================================
    // CAREER CENTER (Appointments)
    // ============================================================
    renderCareerCenter() {
        const upcoming = AppState.getUpcomingAppointments();
        const past = AppState.getPastAppointments();

        return `
            <div class="page-career-center">
                ${Components.sectionHeader('Career Center', 'Appointments with your career services team')}
                <div class="career-center-actions">
                    <button class="btn btn-primary" data-action="navigate" data-page="schedule-appointment">Schedule a New Appointment</button>
                </div>

                ${upcoming.length > 0 ? `
                    <h3 class="list-section-title">Upcoming Appointments</h3>
                    <div class="appointments-list">
                        ${upcoming.map(a => this._renderAppointmentCard(a)).join('')}
                    </div>
                ` : ''}

                ${past.length > 0 ? `
                    <h3 class="list-section-title">Past Appointments</h3>
                    <div class="appointments-list">
                        ${past.map(a => this._renderAppointmentCard(a)).join('')}
                    </div>
                ` : ''}

                ${upcoming.length === 0 && past.length === 0 ? Components.emptyState('', 'No appointments', 'Schedule a new appointment to get started') : ''}
            </div>
        `;
    },

    _renderAppointmentCard(appt) {
        const statusColors = { requested: 'warning', approved: 'success', completed: 'info', declined: 'danger', cancelled: 'danger', started: 'info' };
        return `
            <div class="appointment-card" data-action="viewAppointment" data-appointment-id="${appt.id}">
                <div class="appointment-card-date">
                    <div class="appt-date-month">${Components.formatDateShort(appt.date)}</div>
                    <div class="appt-date-time">${appt.time}</div>
                </div>
                <div class="appointment-card-info">
                    <div class="appointment-card-type">${appt.type}</div>
                    <div class="appointment-card-meta">
                        ${appt.staffName} &middot; ${appt.duration} min &middot; ${appt.medium}
                    </div>
                    <div class="appointment-card-category">${appt.category}</div>
                </div>
                <div class="appointment-card-status">
                    ${Components.statusBadge(appt.status.charAt(0).toUpperCase() + appt.status.slice(1), statusColors[appt.status] || 'default')}
                </div>
            </div>
        `;
    },

    // ============================================================
    // APPOINTMENT DETAIL
    // ============================================================
    renderAppointmentDetail() {
        const appt = AppState.appointments.find(a => a.id === AppState.selectedAppointmentId);
        if (!appt) return Components.emptyState('', 'Appointment not found', '');
        const statusColors = { requested: 'warning', approved: 'success', completed: 'info', declined: 'danger', cancelled: 'danger', started: 'info' };
        const canCancel = appt.status === 'requested' || appt.status === 'approved';

        return `
            <div class="page-detail">
                <button class="back-btn" data-action="navigate" data-page="career-center"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Career Center</button>
                <div class="detail-header">
                    <div>
                        <h1 class="detail-title">${appt.type}</h1>
                        <div class="detail-subtitle">${appt.category}</div>
                    </div>
                    ${Components.statusBadge(appt.status.charAt(0).toUpperCase() + appt.status.slice(1), statusColors[appt.status])}
                </div>
                <div class="detail-meta-row">
                    <span class="detail-meta-item"><strong>Date:</strong> ${Components.formatDate(appt.date)}</span>
                    <span class="detail-meta-item"><strong>Time:</strong> ${appt.time}</span>
                    <span class="detail-meta-item"><strong>Duration:</strong> ${appt.duration} minutes</span>
                    <span class="detail-meta-item"><strong>Medium:</strong> ${appt.medium}</span>
                    ${appt.location ? `<span class="detail-meta-item"><strong>Location:</strong> ${appt.location}</span>` : ''}
                    <span class="detail-meta-item"><strong>Staff:</strong> ${appt.staffName}</span>
                </div>

                <div class="detail-section">
                    <h3>Details</h3>
                    <p>${appt.details || 'No details provided.'}</p>
                </div>

                ${appt.medium === 'Virtual on Handshake' && appt.status === 'approved' ? `
                <div class="detail-section">
                    <button class="btn btn-primary" disabled title="Available 5 minutes before appointment">Start Video Appointment</button>
                    <p class="help-text">The "Start Video Appointment" button will be available 5 minutes before your appointment time.</p>
                </div>
                ` : ''}

                ${appt.comments && appt.comments.length > 0 ? `
                <div class="detail-section">
                    <h3>Comments</h3>
                    <div class="comments-thread">
                        ${appt.comments.map(c => `
                            <div class="thread-comment">
                                <div class="thread-comment-author">${c.author}</div>
                                <div class="thread-comment-text">${c.text}</div>
                                <div class="thread-comment-time">${Components.timeAgo(c.createdAt)}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}

                <div class="detail-section">
                    <h3>Add a Comment</h3>
                    <textarea class="form-textarea" id="appointmentComment" placeholder="Post a follow-up comment or question..." rows="3"></textarea>
                    <button class="btn btn-primary" data-action="addAppointmentComment" data-appointment-id="${appt.id}" style="margin-top: 8px;">Post Comment</button>
                </div>

                ${canCancel ? `
                <div class="detail-section">
                    <button class="btn btn-danger" data-action="cancelAppointment" data-appointment-id="${appt.id}">Cancel Appointment</button>
                </div>
                ` : ''}
            </div>
        `;
    },

    // ============================================================
    // SCHEDULE APPOINTMENT
    // ============================================================
    renderScheduleAppointment() {
        const sched = AppState.appointmentScheduling;
        const selectedCategory = sched.category ? AppState.appointmentCategories.find(c => c.name === sched.category) : null;
        const typeOptions = selectedCategory ? selectedCategory.types : [];
        const staffOptions = AppState.appointmentStaff.map(s => s.name);

        const availableDates = AppState.availableSlots.filter(slot => {
            if (sched.staff) {
                const staffObj = AppState.appointmentStaff.find(s => s.name === sched.staff);
                if (staffObj && !slot.staffAvailable.includes(staffObj.id)) return false;
            }
            return true;
        });

        const selectedSlot = sched.date ? availableDates.find(s => s.date === sched.date) : null;
        const timeOptions = selectedSlot ? selectedSlot.times : [];

        const canSubmit = sched.category && sched.type && sched.date && sched.time && sched.medium;

        return `
            <div class="page-detail">
                <button class="back-btn" data-action="navigate" data-page="career-center"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Career Center</button>
                ${Components.sectionHeader('Schedule a New Appointment', 'Select a category, type, and available time slot')}

                <div class="schedule-form">
                    <div class="form-group">
                        <label class="form-label">Category <span class="required">*</span></label>
                        ${Components.dropdown('schedCategory', sched.category, AppState.appointmentCategories.map(c => c.name), 'Select category...')}
                    </div>

                    <div class="form-group">
                        <label class="form-label">Appointment Type <span class="required">*</span></label>
                        ${Components.dropdown('schedType', sched.type, typeOptions, 'Select type...')}
                    </div>

                    <div class="form-group">
                        <label class="form-label">Staff Member (optional)</label>
                        ${Components.dropdown('schedStaff', sched.staff, ['', ...staffOptions], 'Any available staff')}
                    </div>

                    <div class="form-group">
                        <label class="form-label">Date <span class="required">*</span></label>
                        <div class="date-grid">
                            ${availableDates.map(slot => `
                                <button class="date-slot ${sched.date === slot.date ? 'selected' : ''}" data-action="selectAppointmentDate" data-date="${slot.date}">
                                    ${Components.formatDateShort(slot.date)}
                                </button>
                            `).join('')}
                        </div>
                    </div>

                    ${sched.date ? `
                    <div class="form-group">
                        <label class="form-label">Time <span class="required">*</span></label>
                        <div class="time-grid">
                            ${timeOptions.map(t => `
                                <button class="time-slot ${sched.time === t ? 'selected' : ''}" data-action="selectAppointmentTime" data-time="${t}">
                                    ${t}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                    ` : ''}

                    <div class="form-group">
                        <label class="form-label">Appointment Medium <span class="required">*</span></label>
                        ${Components.dropdown('schedMedium', sched.medium, APPOINTMENT_MEDIUMS, 'Select medium...')}
                    </div>

                    <div class="form-group">
                        <label class="form-label">What can we help you with?</label>
                        <textarea class="form-textarea" id="schedDetails" placeholder="Describe what you'd like to discuss..." rows="4">${sched.details || ''}</textarea>
                    </div>

                    <button class="btn btn-primary btn-lg" data-action="submitAppointment" ${canSubmit ? '' : 'disabled'}>Request Appointment</button>
                </div>
            </div>
        `;
    },

    // ============================================================
    // Q&A
    // ============================================================
    renderQA() {
        const tabs = [
            { id: 'all', label: 'All Questions' },
            { id: 'my-questions', label: 'My Questions' },
            { id: 'my-answers', label: 'My Answers' }
        ];

        let questions = [...AppState.qaQuestions];
        if (AppState.qaTab === 'my-questions') {
            questions = questions.filter(q => q.authorName === AppState.currentUser.fullName);
        } else if (AppState.qaTab === 'my-answers') {
            questions = questions.filter(q => q.answers.some(a => a.authorName === AppState.currentUser.fullName || (a.visibility === 'semi-anonymous' && a.authorSchool === AppState.currentUser.school)));
        }
        if (AppState.qaSearchQuery) {
            const sq = AppState.qaSearchQuery.toLowerCase();
            questions = questions.filter(q => q.question.toLowerCase().includes(sq) || q.answers.some(a => a.text.toLowerCase().includes(sq)));
        }

        return `
            <div class="page-qa">
                ${Components.sectionHeader('Q&A Community', 'Ask questions and get advice from peers')}
                ${Components.tabBar(tabs, AppState.qaTab, 'setQATab')}
                ${Components.searchInput('qaSearch', 'Search questions, advice, companies...', AppState.qaSearchQuery)}

                <div class="qa-create-section">
                    <h4>Ask your own question</h4>
                    <textarea class="form-textarea" id="newQuestion" placeholder="Type your question here..." rows="3"></textarea>
                    <button class="btn btn-primary" data-action="submitQuestion" style="margin-top: 8px;">Submit Question</button>
                </div>

                <div class="qa-list">
                    ${questions.length === 0 ? Components.emptyState('', 'No questions found', AppState.qaTab === 'my-questions' ? 'Ask a question above' : 'Try a different search') :
                        questions.map(q => `
                            <div class="qa-card" data-action="viewQuestion" data-question-id="${q.id}">
                                <div class="qa-card-header">
                                    <span class="qa-author">${q.authorName}</span>
                                    <span class="qa-meta">${q.authorSchool} &middot; ${q.authorMajor} &middot; Class of ${q.authorGradYear}</span>
                                    ${q.status === 'pending' ? Components.statusBadge('Pending', 'warning') : ''}
                                </div>
                                <div class="qa-question-text">${q.question}</div>
                                <div class="qa-card-footer">
                                    <span>${q.answers.length} answer${q.answers.length !== 1 ? 's' : ''}</span>
                                    <span>${q.views} views</span>
                                    <span>${Components.timeAgo(q.createdAt)}</span>
                                </div>
                            </div>
                        `).join('')}
                </div>
            </div>
        `;
    },

    // ============================================================
    // QUESTION DETAIL
    // ============================================================
    renderQuestionDetail() {
        const q = AppState.qaQuestions.find(q => q.id === AppState.selectedQuestionId);
        if (!q) return Components.emptyState('', 'Question not found', '');

        return `
            <div class="page-detail">
                <button class="back-btn" data-action="navigate" data-page="qa"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Q&A</button>

                <div class="question-detail">
                    <div class="question-detail-header">
                        ${Components.avatar(q.authorName, q.authorAvatarColor, 'medium')}
                        <div>
                            <div class="question-author">${q.authorName}</div>
                            <div class="question-meta">${q.authorSchool} &middot; ${q.authorMajor} &middot; Class of ${q.authorGradYear} &middot; ${Components.timeAgo(q.createdAt)}</div>
                        </div>
                    </div>
                    <h2 class="question-text">${q.question}</h2>
                    <div class="question-stats">${q.views} views &middot; ${q.answers.length} answers</div>
                </div>

                <div class="answers-section">
                    <h3>Answers</h3>
                    ${q.answers.length === 0 ? '<p class="no-answers">No answers yet. Be the first to answer!</p>' :
                        q.answers.map(a => `
                            <div class="answer-card ${a.status === 'pending' ? 'answer-pending' : ''}">
                                <div class="answer-header">
                                    ${Components.avatar(a.authorName, a.authorAvatarColor, 'small')}
                                    <div>
                                        <div class="answer-author">${a.authorName}</div>
                                        <div class="answer-meta">${a.authorSchool} &middot; ${a.authorMajor} &middot; Class of ${a.authorGradYear} &middot; ${Components.timeAgo(a.createdAt)}</div>
                                    </div>
                                    ${a.status === 'pending' ? Components.statusBadge('Pending Review', 'warning') : ''}
                                </div>
                                <div class="answer-text">${a.text}</div>
                                <div class="answer-footer">
                                    <button class="helpful-btn" data-action="markHelpful" data-question-id="${q.id}" data-answer-id="${a.id}">
                                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1l2 4h4l-3 3 1 4-4-2-4 2 1-4-3-3h4z" stroke="currentColor" stroke-width="1.2"/></svg>
                                        Helpful (${a.helpful || 0})
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                </div>

                <div class="submit-answer-section">
                    <h3>Your Answer</h3>
                    <textarea class="form-textarea" id="answerText" placeholder="Type your answer here..." rows="4"></textarea>
                    <div class="answer-visibility">
                        <label class="form-label">Visibility</label>
                        <div class="visibility-options">
                            <label class="radio-option">
                                <input type="radio" name="answerVisibility" value="full" checked /> Fully visible (name, photo, school, year, major)
                            </label>
                            <label class="radio-option">
                                <input type="radio" name="answerVisibility" value="semi-anonymous" /> Semi-anonymous (hide name and photo, show school/year/major)
                            </label>
                        </div>
                    </div>
                    <button class="btn btn-primary" data-action="submitAnswer" data-question-id="${q.id}" style="margin-top: 8px;">Submit Answer</button>
                </div>
            </div>
        `;
    },

    // ============================================================
    // PROFILE
    // ============================================================
    renderProfile() {
        const u = AppState.currentUser;

        return `
            <div class="page-profile">
                ${Components.sectionHeader('My Profile', 'Manage your profile information')}
                <div class="profile-card">
                    <div class="profile-header">
                        ${Components.avatar(u.fullName, u.avatarColor, 'xlarge')}
                        <div class="profile-header-info">
                            <h2>${u.fullName}</h2>
                            <p>${u.school} &middot; ${u.major} &middot; Class of ${u.graduationYear}</p>
                            <p>${u.location}</p>
                        </div>
                    </div>
                </div>

                <div class="profile-section">
                    <h3>About</h3>
                    <div class="profile-field-row">
                        <label>Bio</label>
                        <div class="profile-field-value" id="field-bio">${u.bio}</div>
                        <button class="btn-edit" data-action="editProfileField" data-field="bio">Edit</button>
                    </div>
                    <div class="profile-field-row">
                        <label>Email</label>
                        <div class="profile-field-value">${u.email}</div>
                        <button class="btn-edit" data-action="editProfileField" data-field="email">Edit</button>
                    </div>
                    <div class="profile-field-row">
                        <label>Phone</label>
                        <div class="profile-field-value">${u.phone || 'Not set'}</div>
                        <button class="btn-edit" data-action="editProfileField" data-field="phone">Edit</button>
                    </div>
                    <div class="profile-field-row">
                        <label>LinkedIn</label>
                        <div class="profile-field-value">${u.linkedinUrl || 'Not set'}</div>
                        <button class="btn-edit" data-action="editProfileField" data-field="linkedinUrl">Edit</button>
                    </div>
                    <div class="profile-field-row">
                        <label>Website</label>
                        <div class="profile-field-value">${u.websiteUrl || 'Not set'}</div>
                        <button class="btn-edit" data-action="editProfileField" data-field="websiteUrl">Edit</button>
                    </div>
                </div>

                <div class="profile-section">
                    <h3>Looking For</h3>
                    <div class="profile-field-row">
                        <label>Current status</label>
                        <div class="profile-field-value">${u.lookingFor || 'Not set'}</div>
                    </div>
                    <div class="profile-field-row">
                        <label>Roles</label>
                        <div class="profile-field-tags">${(u.careerInterests.roles || []).map(r => `<span class="tag">${r}</span>`).join('')}</div>
                    </div>
                    <div class="profile-field-row">
                        <label>Industries</label>
                        <div class="profile-field-tags">${(u.careerInterests.industries || []).map(i => `<span class="tag">${i}</span>`).join('')}</div>
                    </div>
                    <div class="profile-field-row">
                        <label>Locations</label>
                        <div class="profile-field-tags">${(u.careerInterests.locations || []).map(l => `<span class="tag">${l}</span>`).join('')}</div>
                    </div>
                    <button class="btn btn-outline" data-action="navigate" data-page="career-interests">Edit Career Interests</button>
                </div>

                <div class="profile-section">
                    <h3>Profile Visibility</h3>
                    <div class="profile-field-row">
                        <label>Who can see your profile</label>
                        ${Components.dropdown('profileVisibility', u.profileVisibility, ['Public', 'Community', 'Employers', 'Private'], 'Select visibility')}
                    </div>
                    <p class="help-text">Public: visible to everyone. Community: visible to all Handshake users. Employers: visible to employers only. Private: visible only to you.</p>
                </div>

                <div class="profile-section">
                    <h3>Work Experience</h3>
                    ${(u.workExperience || []).map(exp => `
                        <div class="experience-card">
                            <div class="exp-title">${exp.title}</div>
                            <div class="exp-company">${exp.company}</div>
                            <div class="exp-dates">${exp.startDate} - ${exp.endDate || 'Present'}</div>
                            <div class="exp-desc">${exp.description}</div>
                        </div>
                    `).join('')}
                </div>

                <div class="profile-section">
                    <h3>Skills</h3>
                    <div class="profile-field-tags">${(u.skills || []).map(s => `<span class="tag">${s}</span>`).join('')}</div>
                </div>

                <div class="profile-section">
                    <h3>Organizations</h3>
                    <div class="profile-field-tags">${(u.organizations || []).map(o => `<span class="tag">${o}</span>`).join('')}</div>
                </div>
            </div>
        `;
    },

    // ============================================================
    // CAREER INTERESTS
    // ============================================================
    renderCareerInterests() {
        const ci = AppState.currentUser.careerInterests;

        return `
            <div class="page-career-interests">
                <button class="back-btn" data-action="navigate" data-page="profile"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg> Back to Profile</button>
                ${Components.sectionHeader('Career Interests', 'Help us match you with the right opportunities')}

                <div class="interests-form">
                    <div class="form-group">
                        <label class="form-label">What type of job are you looking for?</label>
                        <div class="checkbox-grid">
                            ${JOB_TYPE_OPTIONS.map(jt => Components.checkbox('jobType-' + jt.replace(/\s/g, '-'), (ci.jobTypes || []).includes(jt), jt)).join('')}
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">How can Handshake help you?</label>
                        <div class="checkbox-grid">
                            ${HELP_WITH_OPTIONS.map(h => Components.checkbox('helpWith-' + h.replace(/\s/g, '-'), (ci.helpWith || []).includes(h), h)).join('')}
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">What are you considering after graduation?</label>
                        <div class="checkbox-grid">
                            ${POST_GRADUATION_OPTIONS.map(p => Components.checkbox('postGrad-' + p.replace(/\s/g, '-'), (ci.postGraduation || []).includes(p), p)).join('')}
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Job Roles</label>
                        <div class="typeahead-tags">
                            ${(ci.roles || []).map(r => Components.tag(r, true, 'removeRole')).join('')}
                        </div>
                        ${Components.dropdown('addRoleDropdown', '', ROLE_OPTIONS.filter(r => !(ci.roles || []).includes(r)), 'Add a role...')}
                    </div>

                    <div class="form-group">
                        <label class="form-label">Where are you interested in living?</label>
                        <div class="typeahead-tags">
                            ${(ci.locations || []).map(l => Components.tag(l, true, 'removeLocation')).join('')}
                        </div>
                        ${Components.dropdown('addLocationDropdown', '', LOCATION_OPTIONS.filter(l => !(ci.locations || []).includes(l)), 'Add a location...')}
                    </div>

                    <div class="form-group">
                        <label class="form-label">Career Community</label>
                        ${Components.dropdown('careerCommunity', ci.careerCommunity, CAREER_COMMUNITY_OPTIONS, 'Select a community...')}
                    </div>

                    <div class="form-group">
                        <label class="form-label">Industries</label>
                        <div class="checkbox-grid industries-grid">
                            ${INDUSTRY_OPTIONS.map(ind => Components.checkbox('industry-' + ind.replace(/[\s&]/g, '-'), (ci.industries || []).includes(ind), ind)).join('')}
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Job Functions</label>
                        <div class="checkbox-grid">
                            ${JOB_FUNCTION_OPTIONS.map(fn => Components.checkbox('jobFunction-' + fn.replace(/[\s&]/g, '-'), (ci.jobFunctions || []).includes(fn), fn)).join('')}
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Expected Graduation Date</label>
                        ${Components.dropdown('expectedGradDate', ci.expectedGraduationDate, GRADUATION_DATE_OPTIONS, 'Select graduation date...')}
                    </div>

                    <button class="btn btn-primary btn-lg" data-action="saveCareerInterests">Save My Career Interests</button>
                </div>
            </div>
        `;
    },

    // ============================================================
    // MODAL RENDERING
    // ============================================================
    renderModal() {
        if (!AppState.activeModal) return '';

        switch (AppState.activeModal) {
            case 'createPost': return this._renderCreatePostModal();
            case 'editProfile': return this._renderEditProfileModal();
            case 'comments': return this._renderCommentsModal();
            default: return '';
        }
    },

    _renderCreatePostModal() {
        return Components.modal('createPostModal', 'Create a Post', `
            <div class="create-post-form">
                <div class="create-post-author">
                    ${Components.avatar(AppState.currentUser.fullName, AppState.currentUser.avatarColor, 'small')}
                    <div>
                        <div class="create-post-name">${AppState.currentUser.fullName}</div>
                        <div class="create-post-visibility">
                            ${Components.dropdown('postAudience', AppState.newPostAudience, ['Everyone on Handshake', 'People at your school'], 'Audience')}
                        </div>
                    </div>
                </div>
                <textarea class="form-textarea" id="newPostContent" placeholder="Share something with the community..." rows="6" maxlength="3000"></textarea>
                <div class="char-count"><span id="charCount">0</span> / 3,000</div>
            </div>
        `, `
            <button class="btn btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn btn-primary" data-action="confirmCreatePost" id="postSubmitBtn" disabled>Post</button>
        `);
    },

    _renderEditProfileModal() {
        const field = AppState.modalData?.field;
        const currentValue = AppState.currentUser[field] || '';
        const labels = { bio: 'Bio', email: 'Email', phone: 'Phone', linkedinUrl: 'LinkedIn URL', websiteUrl: 'Website URL' };
        const isTextarea = field === 'bio';

        return Components.modal('editProfileModal', `Edit ${labels[field] || field}`, `
            <div class="form-group">
                <label class="form-label">${labels[field] || field}</label>
                ${isTextarea ?
                    `<textarea class="form-textarea" id="editProfileInput" rows="4">${currentValue.replace(/</g, '&lt;')}</textarea>` :
                    `<input type="text" class="form-input" id="editProfileInput" value="${currentValue.replace(/"/g, '&quot;')}" />`
                }
            </div>
        `, `
            <button class="btn btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn btn-primary" data-action="confirmEditProfile" data-field="${field}">Save</button>
        `);
    },

    _renderCommentsModal() {
        const post = AppState.feedPosts.find(p => p.id === AppState.modalData?.postId);
        if (!post) return '';

        return Components.modal('commentsModal', 'Comments', `
            <div class="comments-modal-list">
                ${post.comments.length === 0 ? '<p class="no-comments">No comments yet. Be the first!</p>' :
                    post.comments.map(c => `
                        <div class="comment">
                            ${Components.avatar(c.authorName, c.authorAvatarColor, 'small')}
                            <div class="comment-body">
                                <div class="comment-header">
                                    <span class="comment-author">${c.authorName}</span>
                                    <span class="comment-time">${Components.timeAgo(c.createdAt)}</span>
                                </div>
                                <div class="comment-text">${c.text}</div>
                            </div>
                        </div>
                    `).join('')}
            </div>
            <div class="add-comment-form">
                <textarea class="form-textarea" id="newCommentText" placeholder="Write a comment..." rows="2"></textarea>
                <div class="comment-form-actions">
                    <label class="checkbox-row" data-checkbox-id="anonymousComment">
                        <div class="custom-checkbox" id="anonymousComment"></div>
                        <span class="checkbox-label">Post anonymously</span>
                    </label>
                </div>
            </div>
        `, `
            <button class="btn btn-secondary" data-action="closeModal">Close</button>
            <button class="btn btn-primary" data-action="confirmAddComment" data-post-id="${post.id}">Comment</button>
        `, 'modal-lg');
    },

    // ============================================================
    // TOAST
    // ============================================================
    renderToast() {
        if (!AppState.toastMessage) return '';
        return `<div class="toast-message">${AppState.toastMessage}</div>`;
    }
};
