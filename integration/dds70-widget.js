(function() {
    'use strict';
    
    // DDS70 Basketball Detection Widget
    // Usage: <script src="dds70-widget.js"></script>
    //        <div id="dds70-detector"></div>
    
    const DDS70_CONFIG = {
        apiUrl: 'http://localhost:5000', // UPDATE THIS
        containerId: 'dds70-detector',
        theme: {
            primary: '#3b82f6',
            primaryHover: '#2563eb',
            background: '#ffffff',
            border: '#e5e7eb',
            text: '#111827',
            textSecondary: '#6b7280'
        }
    };

    // CSS styles
    const styles = `
        .dds70-container {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 100%;
            background: ${DDS70_CONFIG.theme.background};
            border: 1px solid ${DDS70_CONFIG.theme.border};
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .dds70-header {
            background: linear-gradient(135deg, ${DDS70_CONFIG.theme.primary} 0%, ${DDS70_CONFIG.theme.primaryHover} 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .dds70-header h3 {
            margin: 0 0 8px 0;
            font-size: 20px;
            font-weight: 600;
        }
        .dds70-header p {
            margin: 0;
            opacity: 0.9;
            font-size: 14px;
        }
        .dds70-content {
            padding: 20px;
        }
        .dds70-upload {
            border: 2px dashed ${DDS70_CONFIG.theme.border};
            border-radius: 8px;
            padding: 24px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 16px;
        }
        .dds70-upload:hover {
            border-color: ${DDS70_CONFIG.theme.primary};
            background-color: #f8faff;
        }
        .dds70-upload-text {
            color: ${DDS70_CONFIG.theme.text};
            margin-bottom: 4px;
        }
        .dds70-upload-hint {
            color: ${DDS70_CONFIG.theme.textSecondary};
            font-size: 12px;
        }
        .dds70-controls {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        .dds70-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-weight: 500;
            cursor: pointer;
            font-size: 14px;
        }
        .dds70-btn-primary {
            background: ${DDS70_CONFIG.theme.primary};
            color: white;
        }
        .dds70-btn-primary:hover:not(:disabled) {
            background: ${DDS70_CONFIG.theme.primaryHover};
        }
        .dds70-btn-primary:disabled {
            background: #9ca3af;
            cursor: not-allowed;
        }
        .dds70-btn-secondary {
            background: #f3f4f6;
            color: ${DDS70_CONFIG.theme.text};
        }
        .dds70-preview img {
            max-width: 100%;
            max-height: 300px;
            border-radius: 6px;
            margin-bottom: 16px;
            display: none;
        }
        .dds70-loading {
            text-align: center;
            padding: 24px;
            display: none;
        }
        .dds70-spinner {
            border: 3px solid #f3f4f6;
            border-top: 3px solid ${DDS70_CONFIG.theme.primary};
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: dds70-spin 1s linear infinite;
            margin: 0 auto 12px;
        }
        @keyframes dds70-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .dds70-results {
            display: none;
        }
        .dds70-result-item {
            background: #f9fafb;
            border: 1px solid ${DDS70_CONFIG.theme.border};
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
        }
        .dds70-result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .dds70-class-name {
            font-weight: 600;
            color: ${DDS70_CONFIG.theme.text};
        }
        .dds70-confidence {
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 500;
        }
        .dds70-confidence-high { background: #dcfce7; color: #166534; }
        .dds70-confidence-medium { background: #fef3c7; color: #92400e; }
        .dds70-confidence-low { background: #fee2e2; color: #991b1b; }
        .dds70-details {
            font-size: 12px;
            color: ${DDS70_CONFIG.theme.textSecondary};
        }
        .dds70-error {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #991b1b;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 16px;
            display: none;
        }
        .dds70-hidden { display: none !important; }
        @media (max-width: 640px) {
            .dds70-controls { flex-direction: column; }
            .dds70-result-header { flex-direction: column; align-items: flex-start; gap: 4px; }
        }
    `;

    // Widget HTML template
    const template = `
        <div class="dds70-container">
            <div class="dds70-header">
                <h3>🏀 Basketball Detection</h3>
                <p>AI-powered object detection</p>
            </div>
            <div class="dds70-content">
                <div class="dds70-error" id="dds70-error"></div>
                <div class="dds70-upload" id="dds70-upload">
                    <div style="font-size: 24px; margin-bottom: 8px;">📁</div>
                    <div class="dds70-upload-text">Click to upload an image</div>
                    <div class="dds70-upload-hint">Supports JPG, PNG, GIF, WebP</div>
                    <input type="file" id="dds70-input" accept="image/*" style="display: none;">
                </div>
                <div class="dds70-controls">
                    <button class="dds70-btn dds70-btn-primary" id="dds70-analyze" disabled>Analyze</button>
                    <button class="dds70-btn dds70-btn-secondary" id="dds70-clear">Clear</button>
                    <div style="display: flex; align-items: center; gap: 8px; flex: 1;">
                        <label style="font-size: 12px;">Confidence:</label>
                        <input type="range" id="dds70-confidence" min="0.1" max="1.0" step="0.05" value="0.25" style="flex: 1;">
                        <span id="dds70-confidence-val" style="font-size: 12px;">0.25</span>
                    </div>
                </div>
                <div class="dds70-preview">
                    <img id="dds70-preview-img" alt="Preview">
                </div>
                <div class="dds70-loading" id="dds70-loading">
                    <div class="dds70-spinner"></div>
                    <div>Analyzing...</div>
                </div>
                <div class="dds70-results" id="dds70-results">
                    <div style="font-weight: 600; margin-bottom: 12px; border-bottom: 1px solid ${DDS70_CONFIG.theme.border}; padding-bottom: 8px;">
                        Detection Results (<span id="dds70-count">0</span> objects, <span id="dds70-time">0ms</span>)
                    </div>
                    <div id="dds70-results-list"></div>
                </div>
            </div>
        </div>
    `;

    class DDS70Widget {
        constructor(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) {
                console.error('DDS70 Widget: Container not found');
                return;
            }
            
            this.selectedFile = null;
            this.init();
        }

        init() {
            this.injectStyles();
            this.render();
            this.bindEvents();
            this.checkAPI();
        }

        injectStyles() {
            if (!document.getElementById('dds70-styles')) {
                const styleSheet = document.createElement('style');
                styleSheet.id = 'dds70-styles';
                styleSheet.textContent = styles;
                document.head.appendChild(styleSheet);
            }
        }

        render() {
            this.container.innerHTML = template;
            this.elements = {
                error: this.container.querySelector('#dds70-error'),
                upload: this.container.querySelector('#dds70-upload'),
                input: this.container.querySelector('#dds70-input'),
                analyze: this.container.querySelector('#dds70-analyze'),
                clear: this.container.querySelector('#dds70-clear'),
                confidence: this.container.querySelector('#dds70-confidence'),
                confidenceVal: this.container.querySelector('#dds70-confidence-val'),
                preview: this.container.querySelector('#dds70-preview-img'),
                loading: this.container.querySelector('#dds70-loading'),
                results: this.container.querySelector('#dds70-results'),
                count: this.container.querySelector('#dds70-count'),
                time: this.container.querySelector('#dds70-time'),
                resultsList: this.container.querySelector('#dds70-results-list')
            };
        }

        bindEvents() {
            this.elements.upload.addEventListener('click', () => this.elements.input.click());
            this.elements.input.addEventListener('change', (e) => this.handleFileSelect(e));
            this.elements.analyze.addEventListener('click', () => this.analyzeImage());
            this.elements.clear.addEventListener('click', () => this.clearResults());
            this.elements.confidence.addEventListener('input', (e) => {
                this.elements.confidenceVal.textContent = e.target.value;
            });
        }

        async checkAPI() {
            try {
                const response = await fetch(`${DDS70_CONFIG.apiUrl}/api/health`);
                if (!response.ok) throw new Error('API not available');
            } catch (error) {
                this.showError('Detection service unavailable. Please try again later.');
            }
        }

        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith('image/')) {
                this.selectedFile = file;
                this.elements.analyze.disabled = false;
                this.hideError();
                
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.elements.preview.src = e.target.result;
                    this.elements.preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }

        async analyzeImage() {
            if (!this.selectedFile) return;

            this.setLoading(true);
            this.hideError();
            this.hideResults();

            try {
                const formData = new FormData();
                formData.append('image', this.selectedFile);
                
                const confidence = this.elements.confidence.value;
                const response = await fetch(`${DDS70_CONFIG.apiUrl}/api/detect?confidence=${confidence}`, {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                if (data.success) {
                    this.displayResults(data);
                } else {
                    this.showError(data.error || 'Analysis failed');
                }
            } catch (error) {
                this.showError('Analysis failed. Please try again.');
            } finally {
                this.setLoading(false);
            }
        }

        displayResults(data) {
            this.elements.count.textContent = data.count;
            this.elements.time.textContent = `${(data.processing_time * 1000).toFixed(0)}ms`;
            
            this.elements.resultsList.innerHTML = '';
            
            if (data.detections.length === 0) {
                this.elements.resultsList.innerHTML = '<div style="text-align: center; color: #6b7280; padding: 16px;">No objects detected. Try lowering the confidence threshold.</div>';
            } else {
                data.detections.forEach((detection, index) => {
                    const item = this.createResultItem(detection, index + 1);
                    this.elements.resultsList.appendChild(item);
                });
            }
            
            this.elements.results.style.display = 'block';
        }

        createResultItem(detection, index) {
            const div = document.createElement('div');
            div.className = 'dds70-result-item';
            
            const confidenceClass = detection.confidence > 0.7 ? 'dds70-confidence-high' : 
                                  detection.confidence > 0.5 ? 'dds70-confidence-medium' : 'dds70-confidence-low';
            
            div.innerHTML = `
                <div class="dds70-result-header">
                    <div class="dds70-class-name">#${index} ${detection.class}</div>
                    <div class="dds70-confidence ${confidenceClass}">
                        ${(detection.confidence * 100).toFixed(1)}%
                    </div>
                </div>
                <div class="dds70-details">
                    Position: (${detection.bbox.x1}, ${detection.bbox.y1}) | 
                    Size: ${detection.bbox.width}×${detection.bbox.height} | 
                    Area: ${detection.area.toLocaleString()}px²
                </div>
            `;
            
            return div;
        }

        clearResults() {
            this.selectedFile = null;
            this.elements.input.value = '';
            this.elements.preview.style.display = 'none';
            this.elements.analyze.disabled = true;
            this.hideResults();
            this.hideError();
        }

        setLoading(loading) {
            this.elements.loading.style.display = loading ? 'block' : 'none';
            this.elements.analyze.disabled = loading || !this.selectedFile;
        }

        showError(message) {
            this.elements.error.textContent = message;
            this.elements.error.style.display = 'block';
        }

        hideError() {
            this.elements.error.style.display = 'none';
        }

        hideResults() {
            this.elements.results.style.display = 'none';
        }
    }

    // Auto-initialize when DOM is ready
    function initWidget() {
        if (document.getElementById(DDS70_CONFIG.containerId)) {
            new DDS70Widget(DDS70_CONFIG.containerId);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }

    // Expose for manual initialization
    window.DDS70Widget = DDS70Widget;
})(); 