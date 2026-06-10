const Views = {
    renderToolbar() {
        const slide = AppState.getSelectedSlide();
        return `<div class="toolbar">
            <div class="toolbar-left">
                <div class="toolbar-logo" data-action="goHome" title="Figma Slides">
                    <span class="logo-icon">&#9670;</span>
                </div>
                <div class="deck-name-area">
                    <input type="text" class="deck-name-input" value="${Components._esc(AppState.deckSettings.name)}" data-input-id="deckName" title="Rename deck">
                    <span class="deck-location">${Components._esc(AppState.deckSettings.teamName)} / ${Components._esc(AppState.deckSettings.projectName)}</span>
                </div>
            </div>
            <div class="toolbar-center">
                <button class="toolbar-btn${AppState.currentView === 'slides' ? ' active' : ''}" data-action="setView" data-view="slides" title="Slides">
                    <span class="toolbar-icon">&#9639;</span>
                    <span class="toolbar-btn-label">Slides</span>
                </button>
                <div class="toolbar-separator"></div>
                <button class="toolbar-btn" data-action="addText" title="Text (T)">
                    <span class="toolbar-icon">T</span>
                </button>
                <button class="toolbar-btn" data-action="openShapes" title="Shapes">
                    <span class="toolbar-icon">&#9632;</span>
                </button>
                <button class="toolbar-btn" data-action="addImage" title="Image/Video">
                    <span class="toolbar-icon">&#128247;</span>
                </button>
                <div class="toolbar-separator"></div>
                <button class="toolbar-btn" data-action="openAssets" title="Assets">
                    <span class="toolbar-icon">&#9830;</span>
                    <span class="toolbar-btn-label">Assets</span>
                </button>
                <button class="toolbar-btn" data-action="openInteractions" title="Live interactions">
                    <span class="toolbar-icon">&#9889;</span>
                    <span class="toolbar-btn-label">Interactions</span>
                </button>
                <div class="toolbar-separator"></div>
                <button class="toolbar-btn${AppState.designMode ? ' active' : ''}" data-action="toggleDesignMode" title="Design mode (Shift+D)">
                    <span class="toolbar-icon">&#9998;</span>
                    <span class="toolbar-btn-label">Design</span>
                </button>
            </div>
            <div class="toolbar-right">
                ${Components.avatarStack(AppState.collaborators.filter(c => c.online), 4)}
                <button class="btn btn-primary btn-present" data-action="openPresent" title="Present">
                    <span>&#9654;</span> Present
                </button>
                <button class="btn btn-secondary" data-action="openShare" title="Share">Share</button>
            </div>
        </div>`;
    },

    renderLeftSidebar() {
        const ordered = AppState.getOrderedSlides();
        const groups = AppState.getSlideGroups();

        let html = `<div class="left-sidebar${AppState.sidebarCollapsed ? ' collapsed' : ''}">
            <div class="sidebar-header">
                <div class="sidebar-view-toggle">
                    <button class="view-toggle-btn${!AppState.gridView ? ' active' : ''}" data-action="setGridView" data-grid="false" title="Slide view">&#9776;</button>
                    <button class="view-toggle-btn${AppState.gridView ? ' active' : ''}" data-action="setGridView" data-grid="true" title="Grid view">&#9638;</button>
                </div>
            </div>
            <div class="slide-list${AppState.gridView ? ' grid-mode' : ''}">`;

        if (AppState.gridView) {
            html += this._renderGridView(groups);
        } else {
            html += this._renderSlideList(groups);
        }

        html += `</div>
            <div class="sidebar-footer">
                <button class="btn btn-add-slide" data-action="addSlide" title="New slide">
                    <span>+</span> New slide
                </button>
            </div>
        </div>`;
        return html;
    },

    _renderSlideList(groups) {
        let html = '';
        let slideNum = 0;
        groups.forEach(group => {
            if (group.id) {
                html += `<div class="slide-group" data-group-id="${group.id}">
                    <div class="slide-group-header" data-action="toggleGroup" data-group-id="${group.id}">
                        <span class="group-arrow">&#9662;</span>
                        <span class="group-name">${Components._esc(group.name)}</span>
                        <span class="group-count">${group.slides.length}</span>
                    </div>`;
            }
            group.slides.forEach(slide => {
                if (!slide.skipped) slideNum++;
                const isSelected = slide.id === AppState.selectedSlideId;
                const displayNum = slide.skipped ? '--' : slideNum;
                html += `<div class="slide-thumbnail${isSelected ? ' selected' : ''}${slide.skipped ? ' skipped' : ''}"
                    data-action="selectSlide" data-slide-id="${slide.id}"
                    data-context-menu="slide">
                    <div class="slide-number">${displayNum}</div>
                    <div class="slide-preview" style="background:${this._getSlideBackground(slide)}">
                        <div class="slide-preview-title">${Components._esc(slide.title)}</div>
                        ${slide.skipped ? '<div class="skipped-badge">&#128065;&#8212;</div>' : ''}
                    </div>
                </div>`;
            });
            if (group.id) html += '</div>';
        });
        return html;
    },

    _renderGridView(groups) {
        let html = '<div class="grid-container">';
        let slideNum = 0;
        groups.forEach(group => {
            if (group.id) {
                html += `<div class="grid-group" data-group-id="${group.id}">
                    <div class="grid-group-label">${Components._esc(group.name)}</div>
                    <div class="grid-group-slides">`;
            }
            group.slides.forEach(slide => {
                if (!slide.skipped) slideNum++;
                const isSelected = slide.id === AppState.selectedSlideId;
                html += `<div class="grid-slide${isSelected ? ' selected' : ''}${slide.skipped ? ' skipped' : ''}"
                    data-action="selectSlide" data-slide-id="${slide.id}">
                    <div class="grid-slide-preview" style="background:${this._getSlideBackground(slide)}">
                        <div class="slide-preview-title">${Components._esc(slide.title)}</div>
                        ${slide.skipped ? '<div class="skipped-badge">&#128065;&#8212;</div>' : ''}
                    </div>
                    <div class="grid-slide-number">${slide.skipped ? '--' : slideNum}</div>
                </div>`;
            });
            if (group.id) html += '</div></div>';
        });
        html += '</div>';
        return html;
    },

    renderCanvas() {
        const slide = AppState.getSelectedSlide();
        if (!slide) {
            return '<div class="canvas-area"><div class="canvas-empty">No slide selected</div></div>';
        }

        const deckW = AppState.deckSettings.width || 1200;
        const deckH = AppState.deckSettings.height || 675;
        const canvasW = 960;
        const scale = canvasW / deckW;
        const canvasH = Math.round(deckH * scale);

        let html = `<div class="canvas-area">
            <div class="canvas-slide" style="background:${this._getSlideBackground(slide)};width:${canvasW}px;height:${canvasH}px;" data-slide-id="${slide.id}">
            <div class="canvas-slide-inner" style="width:${deckW}px;height:${deckH}px;transform:scale(${scale});transform-origin:0 0;">`;

        slide.objects.forEach(obj => {
            if (!obj.visible) return;
            html += this._renderObject(obj, slide.id);
        });

        html += '</div></div>';

        // Presenter notes
        if (AppState.presenterNotesVisible) {
            html += this._renderPresenterNotes(slide);
        }

        html += '</div>';
        return html;
    },

    _renderObject(obj, slideId) {
        const isSelected = obj.id === AppState.selectedObjectId;
        const baseStyle = `left:${obj.x}px;top:${obj.y}px;width:${obj.width}px;height:${obj.height}px;opacity:${(obj.opacity || 100) / 100};transform:rotate(${obj.rotation || 0}deg);`;

        switch (obj.type) {
            case 'text':
                return this._renderTextObject(obj, slideId, isSelected, baseStyle);
            case 'shape':
                return this._renderShapeObject(obj, slideId, isSelected, baseStyle);
            case 'code':
                return this._renderCodeObject(obj, slideId, isSelected, baseStyle);
            case 'table':
                return this._renderTableObject(obj, slideId, isSelected, baseStyle);
            case 'liveInteraction':
                return this._renderLiveInteraction(obj, slideId, isSelected, baseStyle);
            case 'image':
                return this._renderImageObject(obj, slideId, isSelected, baseStyle);
            default:
                return '';
        }
    },

    _renderTextObject(obj, slideId, isSelected, baseStyle) {
        const fontStyle = obj.fontStyle === 'italic' ? 'font-style:italic;' : '';
        return `<div class="slide-object text-object${isSelected ? ' selected' : ''}${obj.locked ? ' locked' : ''}"
            style="${baseStyle}font-size:${obj.fontSize}px;font-weight:${obj.fontWeight};font-family:${obj.fontFamily};color:${obj.color};text-align:${obj.textAlign};${fontStyle}"
            data-action="selectObject" data-object-id="${obj.id}" data-slide-id="${slideId}">
            <div class="object-content">${this._formatText(obj.text)}</div>
            ${isSelected ? '<div class="selection-handles"><div class="handle nw"></div><div class="handle ne"></div><div class="handle sw"></div><div class="handle se"></div></div>' : ''}
        </div>`;
    },

    _renderShapeObject(obj, slideId, isSelected, baseStyle) {
        const borderStyle = obj.stroke ? `border:${obj.stroke.width || 1}px solid ${obj.stroke.color};` : '';
        const radiusStyle = obj.cornerRadius ? `border-radius:${obj.cornerRadius}px;` : '';
        return `<div class="slide-object shape-object${isSelected ? ' selected' : ''}${obj.locked ? ' locked' : ''} shape-${obj.shapeType}"
            style="${baseStyle}background:${obj.fill || 'transparent'};${borderStyle}${radiusStyle}color:${obj.color || '#FFFFFF'};font-size:${obj.fontSize || 14}px;font-weight:${obj.fontWeight || 400};text-align:${obj.textAlign || 'center'};"
            data-action="selectObject" data-object-id="${obj.id}" data-slide-id="${slideId}">
            <div class="shape-text">${this._formatText(obj.text || '')}</div>
            ${isSelected ? '<div class="selection-handles"><div class="handle nw"></div><div class="handle ne"></div><div class="handle sw"></div><div class="handle se"></div></div>' : ''}
        </div>`;
    },

    _renderCodeObject(obj, slideId, isSelected, baseStyle) {
        const themeClass = `code-theme-${obj.theme || 'dark'}`;
        return `<div class="slide-object code-object${isSelected ? ' selected' : ''} ${themeClass}"
            style="${baseStyle}font-size:${obj.fontSize || 14}px;"
            data-action="selectObject" data-object-id="${obj.id}" data-slide-id="${slideId}">
            <div class="code-header">
                <span class="code-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></span>
                <span class="code-language">${Components._esc(obj.language || 'Plain Text')}</span>
            </div>
            <pre class="code-content"><code>${Components._esc(obj.code || '')}</code></pre>
            ${isSelected ? '<div class="selection-handles"><div class="handle nw"></div><div class="handle ne"></div><div class="handle sw"></div><div class="handle se"></div></div>' : ''}
        </div>`;
    },

    _renderTableObject(obj, slideId, isSelected, baseStyle) {
        let tableHtml = '<table class="slide-table">';
        obj.cells.forEach((row, ri) => {
            const isHeader = obj.headerRow && ri === 0;
            const tag = isHeader ? 'th' : 'td';
            const rowStyle = isHeader ? `background:${obj.headerStyle?.background || '#2C2C2C'};color:${obj.headerStyle?.color || '#FFF'};font-weight:${obj.headerStyle?.fontWeight || 700};` : `color:${obj.cellStyle?.color || '#E0E0E0'};`;
            tableHtml += '<tr>';
            row.forEach((cell, ci) => {
                tableHtml += `<${tag} style="${rowStyle}border:1px solid ${obj.borderColor || '#404040'};font-size:${obj.fontSize || 14}px;padding:8px 12px;" data-action="editTableCell" data-slide-id="${slideId}" data-object-id="${obj.id}" data-row="${ri}" data-col="${ci}">${Components._esc(cell)}</${tag}>`;
            });
            tableHtml += '</tr>';
        });
        tableHtml += '</table>';

        return `<div class="slide-object table-object${isSelected ? ' selected' : ''}"
            style="${baseStyle}"
            data-action="selectObject" data-object-id="${obj.id}" data-slide-id="${slideId}">
            ${tableHtml}
            ${isSelected ? '<div class="selection-handles"><div class="handle nw"></div><div class="handle ne"></div><div class="handle sw"></div><div class="handle se"></div></div>' : ''}
        </div>`;
    },

    _renderLiveInteraction(obj, slideId, isSelected, baseStyle) {
        let content = '';
        switch (obj.interactionType) {
            case 'poll':
                content = this._renderPoll(obj, slideId);
                break;
            case 'alignment':
                content = this._renderAlignment(obj, slideId);
                break;
            case 'stamps':
                content = this._renderStamps(obj, slideId);
                break;
        }
        return `<div class="slide-object interaction-object${isSelected ? ' selected' : ''}"
            style="${baseStyle}"
            data-action="selectObject" data-object-id="${obj.id}" data-slide-id="${slideId}">
            ${content}
            ${isSelected ? '<div class="selection-handles"><div class="handle nw"></div><div class="handle ne"></div><div class="handle sw"></div><div class="handle se"></div></div>' : ''}
        </div>`;
    },

    _renderPoll(obj, slideId) {
        const totalVotes = obj.options.reduce((sum, o) => sum + o.votes, 0);
        let html = `<div class="poll-widget">
            <div class="poll-header">
                <span class="interaction-icon">&#128202;</span>
                <span class="poll-question">${Components._esc(obj.question)}</span>
            </div>
            <div class="poll-options">`;
        obj.options.forEach(opt => {
            const pct = totalVotes > 0 ? Math.round((opt.votes / totalVotes) * 100) : 0;
            html += `<div class="poll-option" data-action="votePoll" data-slide-id="${slideId}" data-object-id="${obj.id}" data-option-id="${opt.id}">
                <div class="poll-option-bar" style="width:${obj.hideResults ? 0 : pct}%"></div>
                <span class="poll-option-text">${Components._esc(opt.text)}</span>
                ${!obj.hideResults ? `<span class="poll-option-count">${opt.votes} (${pct}%)</span>` : ''}
            </div>`;
        });
        html += `</div>
            <div class="poll-footer">
                <span class="poll-total">${totalVotes} votes</span>
                <button class="btn btn-sm" data-action="togglePollResults" data-slide-id="${slideId}" data-object-id="${obj.id}">${obj.hideResults ? 'Show results' : 'Hide results'}</button>
            </div>
        </div>`;
        return html;
    },

    _renderAlignment(obj, slideId) {
        const avg = obj.responses.length > 0 ? (obj.responses.reduce((s, r) => s + r.value, 0) / obj.responses.length).toFixed(1) : '--';
        let html = `<div class="alignment-widget">
            <div class="alignment-header">
                <span class="interaction-icon">&#9878;</span>
                <span class="alignment-question">${Components._esc(obj.question)}</span>
            </div>
            <div class="alignment-scale">
                <span class="scale-label">${Components._esc(obj.scaleLabels.min)}</span>
                <div class="scale-track">`;
        for (let i = obj.scaleMin; i <= obj.scaleMax; i++) {
            const isSelected = obj.responses.some(r => r.userId === AppState.currentUser.id && r.value === i);
            html += `<button class="scale-point${isSelected ? ' selected' : ''}" data-action="submitAlignment" data-slide-id="${slideId}" data-object-id="${obj.id}" data-value="${i}">${i}</button>`;
        }
        html += `</div>
                <span class="scale-label">${Components._esc(obj.scaleLabels.max)}</span>
            </div>
            <div class="alignment-footer">
                <span>${obj.responses.length} responses</span>
                ${!obj.hideResults ? `<span class="alignment-avg">Avg: ${avg}</span>` : ''}
            </div>
        </div>`;
        return html;
    },

    _renderStamps(obj, slideId) {
        const stampEmojis = { thumbsUp: '&#128077;', heart: '&#10084;', fire: '&#128293;', clap: '&#128079;', rocket: '&#128640;' };
        let html = `<div class="stamps-widget">
            <div class="stamp-buttons">`;
        obj.stampTypes.forEach(type => {
            const count = obj.stamps.filter(s => s.type === type).length;
            const userStamped = obj.stamps.some(s => s.userId === AppState.currentUser.id && s.type === type);
            html += `<button class="stamp-btn${userStamped ? ' stamped' : ''}" data-action="addStamp" data-slide-id="${slideId}" data-object-id="${obj.id}" data-stamp-type="${type}">
                <span class="stamp-emoji">${stampEmojis[type] || type}</span>
                ${count > 0 ? `<span class="stamp-count">${count}</span>` : ''}
            </button>`;
        });
        html += '</div></div>';
        return html;
    },

    _renderImageObject(obj, slideId, isSelected, baseStyle) {
        const fillMode = obj.fillMode || 'fill';
        return `<div class="slide-object image-object${isSelected ? ' selected' : ''}"
            style="${baseStyle}background-image:url(${obj.src});background-size:${fillMode === 'fill' ? 'cover' : 'contain'};background-position:center;background-repeat:${fillMode === 'tile' ? 'repeat' : 'no-repeat'};border-radius:${obj.cornerRadius || 0}px;"
            data-action="selectObject" data-object-id="${obj.id}" data-slide-id="${slideId}">
            ${isSelected ? '<div class="selection-handles"><div class="handle nw"></div><div class="handle ne"></div><div class="handle sw"></div><div class="handle se"></div></div>' : ''}
        </div>`;
    },

    _renderPresenterNotes(slide) {
        return `<div class="presenter-notes-area${AppState.presenterNotesVisible ? ' visible' : ''}">
            <div class="presenter-notes-handle" data-action="togglePresenterNotes" title="Toggle presenter notes">
                <span>&#9650;</span> Presenter notes
            </div>
            <div class="presenter-notes-content">
                <textarea class="presenter-notes-editor" data-input-id="presenterNotes" data-slide-id="${slide.id}" placeholder="Add presenter notes...">${Components._esc(slide.presenterNotes || '')}</textarea>
            </div>
        </div>`;
    },

    renderRightSidebar() {
        const slide = AppState.getSelectedSlide();
        const obj = AppState.getSelectedObject();

        let html = `<div class="right-sidebar">
            ${Components.tabs('rightPanelTabs', [
                { id: 'design', label: 'Design' },
                { id: 'animate', label: 'Animate' }
            ], AppState.activePanel)}
            <div class="right-sidebar-content">`;

        if (AppState.activePanel === 'design') {
            html += this._renderDesignPanel(slide, obj);
        } else {
            html += this._renderAnimatePanel(slide, obj);
        }

        html += '</div></div>';
        return html;
    },

    _renderDesignPanel(slide, obj) {
        if (!slide) return '<div class="panel-empty">No slide selected</div>';

        if (obj) {
            return this._renderObjectProperties(slide, obj);
        }

        return this._renderSlideProperties(slide);
    },

    _renderSlideProperties(slide) {
        const currentStyle = AppState.templateStyles.find(s => s.id === slide.templateStyle);
        let html = '<div class="properties-panel">';

        // Template Style
        html += `<div class="property-section">
            <div class="property-section-title">Template Style</div>
            ${Components.dropdown('slideTemplateStyle', slide.templateStyle, AppState.templateStyles.map(s => ({ id: s.id, name: s.name })))}
            <button class="btn btn-sm btn-ghost" data-action="remixColors" data-slide-id="${slide.id}" title="Remix template colors">Remix colors</button>
        </div>`;

        // Background
        html += `<div class="property-section">
            <div class="property-section-title">Background</div>
            <div class="bg-type-selector">
                <button class="bg-type-btn${slide.background.type === 'solid' ? ' active' : ''}" data-action="setBgType" data-type="solid">Solid</button>
                <button class="bg-type-btn${slide.background.type === 'gradient' ? ' active' : ''}" data-action="setBgType" data-type="gradient">Gradient</button>
                <button class="bg-type-btn${slide.background.type === 'image' ? ' active' : ''}" data-action="setBgType" data-type="image">Image</button>
            </div>`;
        if (slide.background.type === 'solid') {
            html += Components.colorPicker('slideBgColor', slide.background.color, 'Color');
        } else if (slide.background.type === 'gradient') {
            const grad = slide.background.gradient || { type: 'linear', angle: 135, stops: [{ color: '#1E1E1E', position: 0 }, { color: '#2D1B69', position: 100 }] };
            html += Components.colorPicker('gradientStart', grad.stops[0]?.color || '#1E1E1E', 'Start');
            html += Components.colorPicker('gradientEnd', grad.stops[1]?.color || '#2D1B69', 'End');
            html += Components.numberInput('gradientAngle', grad.angle || 135, 0, 360, 1, 'Angle');
        }
        html += '</div>';

        // Slide Number
        html += `<div class="property-section">
            <div class="property-section-title">Slide Number</div>
            ${Components.toggle('slideNumberEnabled', slide.slideNumberEnabled, 'Show number')}`;
        if (slide.slideNumberEnabled) {
            html += Components.dropdown('slideNumberCount', slide.slideNumberCount, [
                { id: 'all', name: 'All slides' },
                { id: 'within_row', name: 'Within row' }
            ], 'Count');
            html += Components.dropdown('slideNumberFormat', slide.slideNumberFormat, SLIDE_NUMBER_FORMATS.map(f => ({ id: f.id, name: `${f.name} (${f.example})` })), 'Format');
            html += Components.toggle('slideNumberIncludeTotal', slide.slideNumberIncludeTotal, 'Include total');
            html += `<button class="btn btn-sm btn-ghost" data-action="addSlideNumbersToAll">Add to all slides</button>`;
        }
        html += '</div>';

        // Export
        html += `<div class="property-section">
            <div class="property-section-title">Export</div>
            <button class="btn btn-sm" data-action="openExportModal">Export slides</button>
        </div>`;

        html += '</div>';
        return html;
    },

    _renderObjectProperties(slide, obj) {
        let html = '<div class="properties-panel">';

        // Object name
        html += `<div class="property-section">
            <div class="object-name-row">
                <input type="text" class="object-name-input" value="${Components._esc(obj.name || '')}" data-input-id="objectName" data-slide-id="${slide.id}" data-object-id="${obj.id}" placeholder="Layer name">
                <button class="icon-btn" data-action="toggleObjectLock" data-slide-id="${slide.id}" data-object-id="${obj.id}" title="${obj.locked ? 'Unlock' : 'Lock'}">${obj.locked ? '&#128274;' : '&#128275;'}</button>
                <button class="icon-btn" data-action="toggleObjectVisibility" data-slide-id="${slide.id}" data-object-id="${obj.id}" title="${obj.visible ? 'Hide' : 'Show'}">${obj.visible ? '&#128065;' : '&#128065;&#8212;'}</button>
            </div>
        </div>`;

        // Position & Size
        html += `<div class="property-section">
            <div class="property-section-title">Position & Size</div>
            <div class="position-grid">
                ${Components.numberInput('objX', obj.x, 0, 1200, 1, 'X')}
                ${Components.numberInput('objY', obj.y, 0, 675, 1, 'Y')}
                ${Components.numberInput('objW', obj.width, 1, 1200, 1, 'W')}
                ${Components.numberInput('objH', obj.height, 1, 675, 1, 'H')}
            </div>
            ${Components.numberInput('objRotation', obj.rotation || 0, -360, 360, 1, 'Rotation')}
            ${Components.slider('objOpacity', obj.opacity || 100, 0, 100, 1, 'Opacity')}
        </div>`;

        // Type-specific properties
        switch (obj.type) {
            case 'text':
                html += this._renderTextProperties(slide, obj);
                break;
            case 'shape':
                html += this._renderShapeProperties(slide, obj);
                break;
            case 'code':
                html += this._renderCodeProperties(slide, obj);
                break;
            case 'table':
                html += this._renderTableProperties(slide, obj);
                break;
            case 'liveInteraction':
                html += this._renderInteractionProperties(slide, obj);
                break;
        }

        // Delete button
        html += `<div class="property-section">
            <button class="btn btn-danger btn-sm" data-action="deleteObject" data-slide-id="${slide.id}" data-object-id="${obj.id}">Delete object</button>
        </div>`;

        html += '</div>';
        return html;
    },

    _renderTextProperties(slide, obj) {
        const fonts = ['Inter', 'Plus Jakarta Sans', 'DM Sans', 'Roboto', 'Open Sans', 'Montserrat', 'Lato', 'Poppins', 'Source Sans Pro', 'Playfair Display', 'Merriweather', 'Fira Code'];
        const weights = [
            { id: 100, name: 'Thin' }, { id: 300, name: 'Light' }, { id: 400, name: 'Regular' },
            { id: 500, name: 'Medium' }, { id: 600, name: 'Semibold' }, { id: 700, name: 'Bold' }, { id: 800, name: 'Extra Bold' }
        ];
        const aligns = [
            { id: 'left', name: 'Left' }, { id: 'center', name: 'Center' }, { id: 'right', name: 'Right' }
        ];
        return `<div class="property-section">
            <div class="property-section-title">Text</div>
            ${Components.dropdown('objFont', obj.fontFamily, fonts.map(f => ({ id: f, name: f })), 'Font')}
            <div class="inline-row">
                ${Components.numberInput('objFontSize', obj.fontSize, 8, 200, 1, 'Size')}
                ${Components.dropdown('objFontWeight', obj.fontWeight, weights, 'Weight')}
            </div>
            ${Components.dropdown('objTextAlign', obj.textAlign, aligns, 'Align')}
            ${Components.colorPicker('objTextColor', obj.color, 'Color')}
        </div>`;
    },

    _renderShapeProperties(slide, obj) {
        let html = `<div class="property-section">
            <div class="property-section-title">Shape</div>
            ${Components.dropdown('objShapeType', obj.shapeType, SHAPE_TYPES.map(s => ({ id: s.id, name: s.name })), 'Type')}
            ${Components.colorPicker('objFill', obj.fill || '#2C2C2C', 'Fill')}
            ${obj.cornerRadius !== undefined ? Components.numberInput('objCornerRadius', obj.cornerRadius, 0, 100, 1, 'Corner radius') : ''}
        </div>`;

        if (obj.stroke) {
            html += `<div class="property-section">
                <div class="property-section-title">Stroke</div>
                ${Components.colorPicker('objStrokeColor', obj.stroke.color || '#FFFFFF', 'Color')}
                ${Components.numberInput('objStrokeWidth', obj.stroke.width || 1, 0, 20, 1, 'Width')}
            </div>`;
        }

        if (obj.text !== undefined) {
            html += `<div class="property-section">
                <div class="property-section-title">Text</div>
                ${Components.textarea('objShapeText', obj.text, 'Add text...', '')}
                ${Components.numberInput('objShapeFontSize', obj.fontSize || 14, 8, 100, 1, 'Size')}
                ${Components.colorPicker('objShapeTextColor', obj.color || '#FFFFFF', 'Color')}
            </div>`;
        }

        return html;
    },

    _renderCodeProperties(slide, obj) {
        return `<div class="property-section">
            <div class="property-section-title">Code Block</div>
            ${Components.dropdown('objCodeLang', obj.language, CODE_LANGUAGES.map(l => ({ id: l, name: l })), 'Language')}
            ${Components.dropdown('objCodeTheme', obj.theme, CODE_THEMES, 'Theme')}
            ${Components.numberInput('objCodeFontSize', obj.fontSize || 14, 8, 24, 1, 'Font size')}
        </div>`;
    },

    _renderTableProperties(slide, obj) {
        return `<div class="property-section">
            <div class="property-section-title">Table</div>
            <div class="table-info">
                <span>${obj.rows} rows &times; ${obj.columns} columns</span>
                <span class="cell-count">${obj.rows * obj.columns} / 500 cells</span>
            </div>
            ${Components.toggle('tableHeaderRow', obj.headerRow, 'Header row')}
            ${Components.colorPicker('tableBorderColor', obj.borderColor || '#404040', 'Border color')}
            ${obj.headerRow ? Components.colorPicker('tableHeaderBg', obj.headerStyle?.background || '#2C2C2C', 'Header background') : ''}
            ${Components.numberInput('tableFontSize', obj.fontSize || 14, 8, 24, 1, 'Font size')}
            <div class="table-actions">
                <button class="btn btn-sm btn-ghost" data-action="addTableRow" data-slide-id="${slide.id}" data-object-id="${obj.id}">+ Row</button>
                <button class="btn btn-sm btn-ghost" data-action="addTableColumn" data-slide-id="${slide.id}" data-object-id="${obj.id}">+ Column</button>
            </div>
        </div>`;
    },

    _renderInteractionProperties(slide, obj) {
        let html = `<div class="property-section">
            <div class="property-section-title">Live Interaction</div>
            <div class="interaction-type-badge">${Components.badge(obj.interactionType, 'primary')}</div>`;

        if (obj.interactionType === 'poll') {
            html += `${Components.textInput('pollQuestion', obj.question, 'Poll question...', 'Question')}
                <div class="poll-options-editor">`;
            obj.options.forEach((opt, i) => {
                html += `<div class="poll-option-row">
                    <input type="text" class="text-input" value="${Components._esc(opt.text)}" data-input-id="pollOption" data-index="${i}" data-slide-id="${slide.id}" data-object-id="${obj.id}">
                    <span class="vote-count">${opt.votes}</span>
                </div>`;
            });
            html += `</div>
                ${Components.toggle('pollHideResults', obj.hideResults, 'Hide results until done')}`;
        } else if (obj.interactionType === 'alignment') {
            html += Components.textInput('alignmentQuestion', obj.question, 'Question...', 'Question');
        }

        html += '</div>';
        return html;
    },

    _renderAnimatePanel(slide, obj) {
        if (!slide) return '<div class="panel-empty">No slide selected</div>';

        let html = '<div class="animate-panel">';

        // Slide transition
        html += `<div class="property-section">
            <div class="property-section-title">Slide Transition</div>
            ${Components.dropdown('transitionType', slide.transition.type, TRANSITION_TYPES.map(t => ({ id: t.id, name: t.name })), 'Style')}`;

        const transType = TRANSITION_TYPES.find(t => t.id === slide.transition.type);
        if (transType && transType.hasDirection) {
            html += `<div class="direction-picker">
                <span class="direction-label">Direction:</span>
                <div class="direction-buttons">`;
            transType.directions.forEach(dir => {
                const arrows = { left: '&#8592;', right: '&#8594;', top: '&#8593;', bottom: '&#8595;' };
                html += `<button class="direction-btn${slide.transition.direction === dir ? ' active' : ''}" data-action="setTransitionDirection" data-direction="${dir}" title="${dir}">${arrows[dir]}</button>`;
            });
            html += '</div></div>';
        }

        html += Components.dropdown('transitionEasing', slide.transition.easing, EASING_PRESETS, 'Curve');
        html += Components.numberInput('transitionDuration', slide.transition.duration, 100, 2000, 50, 'Duration (ms)');
        html += Components.dropdown('transitionTiming', slide.transition.timing, [
            { id: 'immediately', name: 'Immediately' },
            { id: 'after_delay', name: 'After delay' }
        ], 'Timing');
        html += `<button class="btn btn-sm btn-ghost" data-action="applyTransitionToAll">Apply to all slides</button>`;
        html += '</div>';

        // Object animation (if object selected)
        if (obj) {
            html += `<div class="property-section">
                <div class="property-section-title">Object Animation</div>`;
            if (obj.animation) {
                html += Components.dropdown('animStyle', obj.animation.style, ANIMATION_STYLES, 'Style');
                html += Components.numberInput('animDuration', obj.animation.duration, 100, 2000, 50, 'Duration (ms)');
                html += Components.dropdown('animTiming', obj.animation.timing, [
                    { id: 'on_click', name: 'On click' },
                    { id: 'after_previous', name: 'After previous' },
                    { id: 'with_previous', name: 'With previous' }
                ], 'Timing');
                html += Components.dropdown('animDirection', obj.animation.direction, [
                    { id: 'in', name: 'In' },
                    { id: 'out', name: 'Out' }
                ], 'Animate');
                html += `<button class="btn btn-sm btn-danger" data-action="removeAnimation" data-slide-id="${slide.id}" data-object-id="${obj.id}">Remove animation</button>`;
            } else {
                if (obj.type !== 'liveInteraction') {
                    html += `<button class="btn btn-sm btn-primary" data-action="addAnimation" data-slide-id="${slide.id}" data-object-id="${obj.id}">Add animation</button>`;
                } else {
                    html += '<p class="property-note">Cannot animate interactive elements</p>';
                }
            }
            html += '</div>';
        }

        html += '</div>';
        return html;
    },

    renderModals() {
        if (!AppState.activeModal) return '';

        switch (AppState.activeModal) {
            case 'share': return this._renderShareModal();
            case 'present': return this._renderPresentModal();
            case 'export': return this._renderExportModal();
            case 'addSlide': return this._renderAddSlideModal();
            case 'shapes': return this._renderShapesModal();
            case 'assets': return this._renderAssetsModal();
            case 'interactions': return this._renderInteractionsModal();
            case 'editTableCell': return this._renderEditTableCellModal();
            case 'editText': return this._renderEditTextModal();
            case 'editCode': return this._renderEditCodeModal();
            case 'templateStyles': return this._renderTemplateStylesModal();
            case 'libraries': return this._renderLibrariesModal();
            case 'comments': return this._renderCommentsModal();
            case 'deckSettings': return this._renderDeckSettingsModal();
            case 'confirmDelete': return this._renderConfirmDeleteModal();
            default: return '';
        }
    },

    _renderShareModal() {
        const settings = AppState.deckSettings.shareSettings;
        let html = `<div class="share-section">
            <div class="share-link-section">
                <div class="property-section-title">Link access</div>
                ${Components.dropdown('shareLinkAccess', settings.linkAccess, [
                    { id: 'restricted', name: 'Restricted' },
                    { id: 'team', name: 'Anyone in team' },
                    { id: 'organization', name: 'Anyone in organization' },
                    { id: 'anyone', name: 'Anyone with link' }
                ])}
                ${Components.dropdown('shareLinkRole', settings.linkRole, [
                    { id: 'can_view', name: 'Can view' },
                    { id: 'can_edit', name: 'Can edit' }
                ], 'Role')}
            </div>
            <div class="share-options">
                ${Components.toggle('shareAllowCopy', settings.allowCopy, 'Allow copy')}
                ${Components.toggle('shareAllowDownload', settings.allowDownload, 'Allow download')}
            </div>
            <div class="share-people-section">
                <div class="property-section-title">People with access</div>
                <div class="share-people-list">
                    <div class="share-person">
                        ${Components.avatar(AppState.currentUser, 28)}
                        <span class="person-name">${Components._esc(AppState.currentUser.name)}</span>
                        <span class="person-role">Owner</span>
                    </div>`;
        AppState.collaborators.forEach(c => {
            html += `<div class="share-person">
                ${Components.avatar(c, 28)}
                <span class="person-name">${Components._esc(c.name)}</span>
                ${Components.dropdown('collabRole_' + c.id, c.role, [
                    { id: 'Editor', name: 'Can edit' },
                    { id: 'Viewer', name: 'Can view' }
                ])}
                <button class="icon-btn btn-remove-collab" data-action="removeCollaborator" data-user-id="${c.id}" title="Remove">&times;</button>
            </div>`;
        });
        html += `</div></div>
            <button class="btn btn-primary" data-action="copyPresentationLink">Copy presentation link</button>
        </div>`;

        return Components.modal('share', 'Share', html, '', 'modal-lg');
    },

    _renderPresentModal() {
        let html = `<div class="present-options">
            <div class="present-option" data-action="startPresent" data-mode="present">
                <div class="present-option-icon">&#9654;</div>
                <div class="present-option-info">
                    <div class="present-option-title">Present</div>
                    <div class="present-option-desc">Full screen presentation</div>
                </div>
            </div>
            <div class="present-option" data-action="startPresent" data-mode="present_notes">
                <div class="present-option-icon">&#9654;&#128221;</div>
                <div class="present-option-info">
                    <div class="present-option-title">Present + Notes</div>
                    <div class="present-option-desc">Presentation with presenter notes visible</div>
                </div>
            </div>
            <div class="present-divider"></div>
            <div class="present-option-row">
                ${Components.toggle('availableOffline', AppState.deckSettings.availableOffline, 'Available offline')}
            </div>
            <div class="present-option-row">
                <button class="btn btn-sm btn-ghost" data-action="copyPresentationLink">Copy presentation link</button>
            </div>
        </div>`;

        return Components.modal('present', 'Present', html);
    },

    _renderExportModal() {
        const data = AppState.modalData || { format: 'pdf', colorProfile: 'srgb', quality: 'high', slidesIncluded: 'all' };
        let html = `<div class="export-form">
            ${Components.dropdown('exportFormat', data.format, EXPORT_FORMATS, 'File type')}`;

        if (data.format === 'pdf') {
            html += Components.dropdown('exportColorProfile', data.colorProfile, PDF_COLOR_PROFILES, 'Color profile');
            html += Components.dropdown('exportQuality', data.quality, PDF_QUALITY_OPTIONS, 'Quality');
        }

        html += Components.dropdown('exportSlides', data.slidesIncluded, [
            { id: 'all', name: 'All slides' },
            { id: 'selected', name: 'Selected slide only' }
        ], 'Content');

        if (data.format === 'pptx') {
            html += `<div class="export-warning">
                <span class="warning-icon">&#9888;</span>
                <span>Some features may not export perfectly: live interactions and code blocks become static images, gradient fills may simplify.</span>
            </div>`;
        }

        html += '</div>';

        const footer = `<button class="btn btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn btn-primary" data-action="confirmExport">Export</button>`;

        return Components.modal('export', 'Export Slides', html, footer);
    },

    _renderAddSlideModal() {
        let html = `<div class="add-slide-form">
            <div class="layout-grid">`;
        SLIDE_LAYOUTS.forEach(layout => {
            html += `<div class="layout-option" data-action="confirmAddSlide" data-layout="${layout.id}">
                <div class="layout-preview layout-${layout.id}">
                    <div class="layout-icon">${this._getLayoutIcon(layout.id)}</div>
                </div>
                <div class="layout-name">${Components._esc(layout.name)}</div>
            </div>`;
        });
        html += '</div></div>';

        return Components.modal('addSlide', 'Choose Layout', html, '', 'modal-lg');
    },

    _renderShapesModal() {
        let html = '<div class="shapes-grid">';
        SHAPE_TYPES.forEach(shape => {
            html += `<div class="shape-option" data-action="insertShape" data-shape-type="${shape.id}">
                <div class="shape-icon shape-icon-${shape.id}"></div>
                <div class="shape-name">${Components._esc(shape.name)}</div>
            </div>`;
        });
        html += '</div>';
        return Components.modal('shapes', 'Shapes', html);
    },

    _renderAssetsModal() {
        let html = `<div class="assets-panel">
            ${Components.tabs('assetsTabs', [
                { id: 'components', label: 'Components' },
                { id: 'table', label: 'Table' },
                { id: 'code', label: 'Code block' },
                { id: 'slideNumber', label: 'Slide number' }
            ], AppState.modalData?.tab || 'components')}
            <div class="assets-content">`;

        const tab = AppState.modalData?.tab || 'components';
        switch (tab) {
            case 'components':
                html += `<div class="assets-libraries">`;
                AppState.libraries.filter(l => l.enabled).forEach(lib => {
                    html += `<div class="library-section">
                        <div class="library-header">${Components._esc(lib.name)} ${lib.hasUpdates ? '<span class="update-badge">Update available</span>' : ''}</div>
                        <div class="library-stats">${lib.componentCount} components, ${lib.styleCount} styles</div>
                    </div>`;
                });
                html += `<button class="btn btn-sm btn-ghost" data-action="openLibraries">Add your own</button></div>`;
                break;
            case 'table':
                html += `<div class="asset-action-card">
                    <p>Click to add a table to the current slide.</p>
                    <button class="btn btn-primary" data-action="insertTable">Insert Table</button>
                </div>`;
                break;
            case 'code':
                html += `<div class="asset-action-card">
                    <p>Add a code block with syntax highlighting.</p>
                    <button class="btn btn-primary" data-action="insertCodeBlock">Insert Code Block</button>
                </div>`;
                break;
            case 'slideNumber':
                html += `<div class="asset-action-card">
                    <p>Add slide numbers to your presentation.</p>
                    <button class="btn btn-primary" data-action="insertSlideNumber">Add to this slide</button>
                    <button class="btn btn-ghost" data-action="addSlideNumbersToAll">Add to all slides</button>
                </div>`;
                break;
        }

        html += '</div></div>';
        return Components.modal('assets', 'Assets', html, '', 'modal-lg');
    },

    _renderInteractionsModal() {
        const interactions = [
            { type: 'poll', name: 'Poll', icon: '&#128202;', desc: 'Ask a question and gather votes' },
            { type: 'stamps', name: 'Stamps', icon: '&#128077;', desc: 'Gauge audience feeling with reactions' },
            { type: 'alignment', name: 'Alignment', icon: '&#9878;', desc: 'Anonymous voting for unbiased opinions' }
        ];
        let html = '<div class="interactions-grid">';
        interactions.forEach(int => {
            html += `<div class="interaction-option" data-action="insertInteraction" data-interaction-type="${int.type}">
                <div class="interaction-option-icon">${int.icon}</div>
                <div class="interaction-option-name">${int.name}</div>
                <div class="interaction-option-desc">${int.desc}</div>
            </div>`;
        });
        html += '</div>';
        return Components.modal('interactions', 'Live Interactions', html);
    },

    _renderEditTableCellModal() {
        const data = AppState.modalData;
        if (!data) return '';
        const slide = AppState.slides.find(s => s.id === data.slideId);
        if (!slide) return '';
        const obj = slide.objects.find(o => o.id === data.objectId);
        if (!obj || !obj.cells[data.row]) return '';
        const currentValue = obj.cells[data.row][data.col] || '';

        const html = Components.textInput('tableCellValue', currentValue, 'Enter cell value...');
        const footer = `<button class="btn btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn btn-primary" data-action="confirmTableCellEdit">Save</button>`;
        return Components.modal('editTableCell', `Edit Cell (Row ${data.row + 1}, Col ${data.col + 1})`, html, footer);
    },

    _renderEditTextModal() {
        const data = AppState.modalData;
        if (!data) return '';
        const html = Components.textarea('editTextValue', data.text, 'Enter text...', '', 6);
        const footer = `<button class="btn btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn btn-primary" data-action="confirmTextEdit">Save</button>`;
        return Components.modal('editText', 'Edit Text', html, footer);
    },

    _renderEditCodeModal() {
        const data = AppState.modalData;
        if (!data) return '';
        const html = `<div class="code-edit-form">
            ${Components.dropdown('editCodeLang', data.language, CODE_LANGUAGES.map(l => ({ id: l, name: l })), 'Language')}
            ${Components.textarea('editCodeValue', data.code, 'Enter code...', '', 12)}
        </div>`;
        const footer = `<button class="btn btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn btn-primary" data-action="confirmCodeEdit">Save</button>`;
        return Components.modal('editCode', 'Edit Code', html, footer, 'modal-lg');
    },

    _renderTemplateStylesModal() {
        const currentStyleId = AppState.modalData?.styleId || AppState.deckSettings.defaultTemplateStyle;
        const style = AppState.templateStyles.find(s => s.id === currentStyleId);
        if (!style) return '';

        let html = `<div class="template-styles-editor">
            <div class="style-selector">
                ${Components.dropdown('editTemplateStyle', currentStyleId, AppState.templateStyles.map(s => ({ id: s.id, name: s.name })))}
                <input type="text" class="text-input" value="${Components._esc(style.name)}" data-input-id="templateStyleName" data-style-id="${style.id}" placeholder="Style name">
            </div>
            <div class="style-colors">
                <div class="property-section-title">Colors <button class="btn btn-sm btn-ghost" data-action="addTemplateColor" data-style-id="${style.id}">+</button></div>`;
        style.colors.forEach(color => {
            html += `<div class="template-color-row">
                <div class="color-swatch-sm" style="background:${color.value}"></div>
                <span class="color-name">${Components._esc(color.name)}</span>
                <span class="color-value">${color.value}</span>
                <button class="icon-btn btn-sm" data-action="removeTemplateColor" data-style-id="${style.id}" data-color-id="${color.id}" title="Remove">&times;</button>
            </div>`;
        });
        html += `</div>
            <div class="style-text-styles">
                <div class="property-section-title">Text Styles <button class="btn btn-sm btn-ghost" data-action="addTemplateTextStyle" data-style-id="${style.id}">+</button></div>`;
        style.textStyles.forEach(ts => {
            html += `<div class="template-text-row">
                <span class="text-style-preview" style="font-family:${ts.fontFamily};font-size:${Math.min(ts.fontSize, 20)}px;font-weight:${ts.fontWeight}">${Components._esc(ts.name)}</span>
                <span class="text-style-meta">${ts.fontFamily} ${ts.fontSize}px ${ts.fontWeight}</span>
                <button class="icon-btn btn-sm" data-action="removeTemplateTextStyle" data-style-id="${style.id}" data-text-style-id="${ts.id}" title="Remove">&times;</button>
            </div>`;
        });
        html += '</div></div>';

        const footer = `<button class="btn btn-secondary" data-action="closeModal">Done</button>`;
        return Components.modal('templateStyles', 'Edit Template Style', html, footer, 'modal-lg');
    },

    _renderLibrariesModal() {
        let html = '<div class="libraries-panel">';

        // Added libraries
        html += '<div class="property-section-title">Added Libraries</div>';
        AppState.libraries.forEach(lib => {
            html += `<div class="library-row">
                <div class="library-info">
                    <div class="library-name">${Components._esc(lib.name)} ${lib.hasUpdates ? '<span class="update-badge">Update</span>' : ''}</div>
                    <div class="library-desc">${Components._esc(lib.description)}</div>
                    <div class="library-stats">${lib.componentCount} components, ${lib.styleCount} styles, ${lib.variableCount} variables</div>
                </div>
                <div class="library-actions">
                    ${lib.hasUpdates ? `<button class="btn btn-sm btn-primary" data-action="updateLibrary" data-library-id="${lib.id}">Update</button>` : ''}
                    <button class="btn btn-sm btn-danger" data-action="removeLibrary" data-library-id="${lib.id}">Remove</button>
                </div>
            </div>`;
        });

        html += '</div>';
        const footer = `<button class="btn btn-secondary" data-action="closeModal">Done</button>`;
        return Components.modal('libraries', 'Libraries', html, footer, 'modal-lg');
    },

    _renderCommentsModal() {
        const slideId = AppState.selectedSlideId;
        const slideComments = AppState.comments.filter(c => c.slideId === slideId);
        const allComments = AppState.comments;

        let html = `<div class="comments-panel">
            ${Components.tabs('commentsTabs', [
                { id: 'slide', label: 'This slide (' + slideComments.length + ')' },
                { id: 'all', label: 'All (' + allComments.length + ')' }
            ], AppState.modalData?.tab || 'slide')}
            <div class="comments-list">`;

        const comments = (AppState.modalData?.tab === 'all') ? allComments : slideComments;

        if (comments.length === 0) {
            html += Components.emptyState('&#128172;', 'No comments yet', 'Add a comment', 'addCommentFromModal');
        } else {
            comments.forEach(comment => {
                html += `<div class="comment-thread${comment.resolved ? ' resolved' : ''}">
                    <div class="comment-main">
                        ${Components.avatar({ initials: comment.userName.split(' ').map(n => n[0]).join(''), avatarColor: comment.avatarColor }, 28)}
                        <div class="comment-content">
                            <div class="comment-header-row">
                                <span class="comment-author">${Components._esc(comment.userName)}</span>
                                <span class="comment-time">${this._formatTime(comment.createdAt)}</span>
                            </div>
                            <div class="comment-text">${Components._esc(comment.text)}</div>
                            <div class="comment-actions">
                                ${comment.resolved
                                    ? `<button class="btn btn-sm btn-ghost" data-action="unresolveComment" data-comment-id="${comment.id}">Unresolve</button>`
                                    : `<button class="btn btn-sm btn-ghost" data-action="resolveComment" data-comment-id="${comment.id}">Resolve</button>`
                                }
                                <button class="btn btn-sm btn-ghost" data-action="deleteComment" data-comment-id="${comment.id}">Delete</button>
                            </div>
                        </div>
                    </div>`;

                comment.replies.forEach(reply => {
                    html += `<div class="comment-reply">
                        ${Components.avatar({ initials: reply.userName.split(' ').map(n => n[0]).join(''), avatarColor: reply.avatarColor }, 24)}
                        <div class="comment-content">
                            <div class="comment-header-row">
                                <span class="comment-author">${Components._esc(reply.userName)}</span>
                                <span class="comment-time">${this._formatTime(reply.createdAt)}</span>
                            </div>
                            <div class="comment-text">${Components._esc(reply.text)}</div>
                        </div>
                    </div>`;
                });

                if (!comment.resolved) {
                    html += `<div class="comment-reply-input">
                        <input type="text" class="text-input" placeholder="Reply..." data-input-id="commentReply" data-comment-id="${comment.id}">
                        <button class="btn btn-sm btn-primary" data-action="submitReply" data-comment-id="${comment.id}">Reply</button>
                    </div>`;
                }

                html += '</div>';
            });
        }

        html += `</div>
            <div class="comment-add-section">
                <input type="text" class="text-input" placeholder="Add a comment..." data-input-id="newComment" id="newCommentInput">
                <button class="btn btn-primary" data-action="submitComment">Comment</button>
            </div>
        </div>`;

        return Components.modal('comments', 'Comments', html, '', 'modal-lg');
    },

    _renderDeckSettingsModal() {
        let html = `<div class="deck-settings-form">
            ${Components.textInput('settingsDeckName', AppState.deckSettings.name, 'Deck name', 'Name')}
            ${Components.dropdown('settingsAspectRatio', AppState.deckSettings.aspectRatio, [
                { id: '16:9', name: '16:9 (Widescreen)' },
                { id: '4:3', name: '4:3 (Standard)' }
            ], 'Aspect ratio')}
            <div class="property-section">
                <div class="property-section-title">Default transition</div>
                ${Components.dropdown('settingsDefaultTransType', AppState.deckSettings.defaultTransition.type, TRANSITION_TYPES.map(t => ({ id: t.id, name: t.name })))}
            </div>
            <div class="property-section">
                <div class="property-section-title">Slide numbers</div>
                ${Components.toggle('settingsSlideNumbers', AppState.deckSettings.slideNumbersEnabled, 'Enable slide numbers')}
                ${AppState.deckSettings.slideNumbersEnabled ? Components.dropdown('settingsSlideNumFormat', AppState.deckSettings.slideNumberFormat, SLIDE_NUMBER_FORMATS.map(f => ({ id: f.id, name: f.name })), 'Format') : ''}
                ${AppState.deckSettings.slideNumbersEnabled ? Components.toggle('settingsSlideNumTotal', AppState.deckSettings.slideNumberIncludeTotal, 'Include total') : ''}
            </div>
            <div class="property-section">
                <div class="property-section-title">Template</div>
                ${Components.dropdown('settingsDefaultTemplate', AppState.deckSettings.defaultTemplateStyle, AppState.templateStyles.map(s => ({ id: s.id, name: s.name })), 'Default template style')}
                <button class="btn btn-sm btn-ghost" data-action="openTemplateStyles">Edit template styles</button>
            </div>
        </div>`;

        const footer = `<button class="btn btn-secondary" data-action="closeModal">Cancel</button>
            <button class="btn btn-primary" data-action="saveDeckSettings">Save</button>`;
        return Components.modal('deckSettings', 'Deck Settings', html, footer);
    },

    _renderConfirmDeleteModal() {
        const data = AppState.modalData;
        if (!data) return '';
        return Components.confirmModal('confirmDelete', 'Delete Slide', `Are you sure you want to delete "${data.title || 'this slide'}"? This action cannot be undone.`, 'Delete', 'btn-danger');
    },

    renderToast() {
        if (!AppState.toastMessage) return '';
        return Components.toast(AppState.toastMessage);
    },

    renderContextMenu() {
        if (!AppState.contextMenuData) return '';
        const data = AppState.contextMenuData;
        return Components.contextMenu(data.items, data.x, data.y);
    },

    // Helpers
    _getSlideBackground(slide) {
        if (!slide.background) return '#1E1E1E';
        if (slide.background.type === 'solid') return slide.background.color || '#1E1E1E';
        if (slide.background.type === 'gradient') {
            const g = slide.background.gradient;
            if (g) return `linear-gradient(${g.angle || 135}deg, ${g.stops.map(s => s.color + ' ' + s.position + '%').join(', ')})`;
        }
        return '#1E1E1E';
    },

    _formatText(text) {
        if (!text) return '';
        return Components._esc(text).replace(/\n/g, '<br>');
    },

    _formatTime(isoString) {
        if (!isoString) return '';
        const d = new Date(isoString);
        const now = new Date();
        const diff = now - d;
        const days = Math.floor(diff / 86400000);
        if (days === 0) return 'Today';
        if (days === 1) return 'Yesterday';
        if (days < 7) return `${days}d ago`;
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    },

    _getLayoutIcon(layoutId) {
        const icons = {
            layout_title: '<div style="width:60%;height:20%;background:#555;margin:30% auto 8px;border-radius:2px"></div><div style="width:40%;height:8%;background:#444;margin:0 auto;border-radius:2px"></div>',
            layout_title_content: '<div style="width:60%;height:12%;background:#555;margin:8% 8% 6%;border-radius:2px"></div><div style="width:70%;height:50%;background:#3a3a3a;margin:0 8%;border-radius:2px"></div>',
            layout_two_column: '<div style="width:60%;height:12%;background:#555;margin:8% 8% 6%;border-radius:2px"></div><div style="display:flex;gap:4%;margin:0 8%"><div style="flex:1;height:45%;background:#3a3a3a;border-radius:2px"></div><div style="flex:1;height:45%;background:#3a3a3a;border-radius:2px"></div></div>',
            layout_image_left: '<div style="display:flex;height:80%;margin:10% 4%"><div style="flex:1;background:#4a4a6a;border-radius:2px"></div><div style="flex:1;padding:8%"><div style="width:80%;height:15%;background:#555;border-radius:2px;margin-bottom:8%"></div><div style="width:100%;height:40%;background:#3a3a3a;border-radius:2px"></div></div></div>',
            layout_image_right: '<div style="display:flex;height:80%;margin:10% 4%"><div style="flex:1;padding:8%"><div style="width:80%;height:15%;background:#555;border-radius:2px;margin-bottom:8%"></div><div style="width:100%;height:40%;background:#3a3a3a;border-radius:2px"></div></div><div style="flex:1;background:#4a4a6a;border-radius:2px"></div></div>',
            layout_full_image: '<div style="width:100%;height:100%;background:#4a4a6a;display:flex;align-items:center;justify-content:center;border-radius:2px"><div style="width:50%;height:15%;background:rgba(255,255,255,0.3);border-radius:2px"></div></div>',
            layout_section: '<div style="width:50%;height:20%;background:#555;margin:35% auto 8px;border-radius:2px"></div><div style="width:30%;height:8%;background:#444;margin:0 auto;border-radius:2px"></div>',
            layout_quote: '<div style="width:70%;height:3px;background:#666;margin:25% auto 10%"></div><div style="width:60%;height:25%;background:#3a3a3a;margin:0 auto 6%;border-radius:2px"></div><div style="width:30%;height:8%;background:#444;margin:0 auto;border-radius:2px"></div>',
            layout_blank: '<div style="width:100%;height:100%;border:1px dashed #444;border-radius:2px"></div>',
            layout_three_column: '<div style="width:60%;height:12%;background:#555;margin:8% 8% 6%;border-radius:2px"></div><div style="display:flex;gap:3%;margin:0 8%"><div style="flex:1;height:45%;background:#3a3a3a;border-radius:2px"></div><div style="flex:1;height:45%;background:#3a3a3a;border-radius:2px"></div><div style="flex:1;height:45%;background:#3a3a3a;border-radius:2px"></div></div>',
            layout_comparison: '<div style="width:60%;height:12%;background:#555;margin:8% 8% 6%;border-radius:2px"></div><div style="display:flex;gap:2%;margin:0 8%"><div style="flex:1;height:50%;background:#3a3a3a;border-radius:2px;border-top:3px solid #7B61FF"></div><div style="flex:1;height:50%;background:#3a3a3a;border-radius:2px;border-top:3px solid #0ACF83"></div></div>',
            layout_closing: '<div style="width:40%;height:18%;background:#555;margin:30% auto 8px;border-radius:2px"></div><div style="width:30%;height:8%;background:#444;margin:0 auto;border-radius:2px"></div>'
        };
        return icons[layoutId] || icons.layout_blank;
    }
};
