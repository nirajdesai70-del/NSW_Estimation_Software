/**
 * RAG UI JavaScript Module
 * 
 * Handles RAG query interactions, citation display, and drawer management.
 */

(function() {
    'use strict';

    const RagUI = {
        // Configuration
        config: {
            queryEndpoint: '/ui/rag/query',
            feedbackEndpoint: '/ui/rag/feedback',
            timeout: 4000, // 4 seconds
        },

        /**
         * Initialize RAG UI components
         */
        init: function() {
            this.bindExplainWhyTriggers();
            this.setupDrawerEvents();
        },

        /**
         * Bind explain-why trigger buttons
         */
        bindExplainWhyTriggers: function() {
            document.querySelectorAll('.rag-explain-trigger').forEach(trigger => {
                trigger.addEventListener('click', (e) => {
                    e.preventDefault();
                    const wrapper = trigger.closest('.rag-explain-why-wrapper');
                    if (wrapper) {
                        const query = wrapper.dataset.query || '';
                        const context = JSON.parse(wrapper.dataset.context || '{}');
                        const drawerId = wrapper.dataset.drawerId;
                        this.queryAndDisplay(query, context, drawerId);
                    }
                });
            });
        },

        /**
         * Setup drawer events (Bootstrap offcanvas)
         * Uses event delegation to handle dynamically created drawers
         */
        setupDrawerEvents: function() {
            // Use event delegation for all offcanvas drawers
            document.addEventListener('show.bs.offcanvas', (e) => {
                const drawer = e.target;
                if (drawer && drawer.id && drawer.id.startsWith('ragExplainDrawer_')) {
                    // Reset state when drawer opens
                    this.resetDrawerState(drawer);
                }
            });

            // Bind feedback button handlers
            const self = this;
            document.addEventListener('click', async (e) => {
                const upBtn = e.target.closest('.rag-feedback-up');
                const downBtn = e.target.closest('.rag-feedback-down');
                if (!upBtn && !downBtn) return;

                const drawer = e.target.closest('.offcanvas');
                if (!drawer) return;

                const rating = upBtn ? 'up' : 'down';
                const statusEl = drawer.querySelector('.rag-feedback-status');

                try {
                    if (statusEl) statusEl.textContent = 'Sending...';

                    const payload = {
                        query: drawer.dataset.ragLastQuery || '',
                        rating,
                        context: JSON.parse(drawer.dataset.ragContext || '{}'),
                        best_authority: drawer.dataset.ragBestAuthority || 'WORKING',
                        citations: JSON.parse(drawer.dataset.ragCitations || '[]'),
                        latency_ms: parseInt(drawer.dataset.ragLatency || '0', 10) || 0,
                    };

                    const res = await fetch(self.config.feedbackEndpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': self.getCsrfToken(),
                        },
                        body: JSON.stringify(payload),
                    });

                    if (!res.ok) throw new Error(`HTTP ${res.status}`);

                    if (statusEl) statusEl.textContent = 'Thanks ✅';
                } catch (err) {
                    console.error('Feedback failed', err);
                    if (statusEl) statusEl.textContent = 'Failed to send';
                }
            });
        },

        /**
         * Query RAG service and display results
         */
        queryAndDisplay: async function(query, context = {}, drawerId = null) {
            if (!query || !query.trim()) {
                this.showError('Please provide a query.', drawerId);
                return;
            }

            // Find the drawer element
            const drawer = drawerId ? document.getElementById(drawerId) : 
                          document.querySelector('.offcanvas[id^="ragExplainDrawer_"]');
            
            if (!drawer) {
                console.error('RAG drawer not found');
                return;
            }

            this.showLoading(drawer);
            this.hideError(drawer);
            this.hideAnswer(drawer);
            this.hideCitations(drawer);
            this.hideFooter(drawer);

            // Store query and context in drawer dataset for feedback
            drawer.dataset.ragLastQuery = query.trim();
            drawer.dataset.ragContext = JSON.stringify(context || {});

            try {
                const response = await fetch(this.config.queryEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': this.getCsrfToken(),
                    },
                    body: JSON.stringify({
                        query: query.trim(),
                        context: context,
                        top_k: 8,
                    }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                this.displayResults(data, drawer);

            } catch (error) {
                console.error('RAG query failed:', error);
                this.showError(
                    error.message || 'Failed to query knowledge base. Please try again later.',
                    drawer
                );
            } finally {
                this.hideLoading(drawer);
            }
        },

        /**
         * Display query results
         */
        displayResults: function(data, drawer) {
            if (!drawer) {
                drawer = document.querySelector('.offcanvas[id^="ragExplainDrawer_"]');
            }

            // Display best authority in header
            if (data.best_authority) {
                const bestAuthEl = drawer.querySelector('[id$="BestAuthority"]');
                if (bestAuthEl) {
                    bestAuthEl.innerHTML = this.getAuthorityBadge(data.best_authority);
                }
            }

            // Display answer
            if (data.answer) {
                const answerEl = drawer.querySelector('.rag-answer-text');
                if (answerEl) {
                    answerEl.textContent = data.answer;
                    this.showAnswer(drawer);
                }
            }

            // Display citations
            if (data.citations && data.citations.length > 0) {
                this.displayCitations(data.citations, drawer);
                this.showCitations(drawer);
            } else {
                this.hideCitations(drawer);
            }

            // Display footer (versions)
            if (data.kb_version || data.index_version) {
                const kbVersionEl = drawer.querySelector('.rag-kb-version');
                const indexVersionEl = drawer.querySelector('.rag-index-version');
                const latencyEl = drawer.querySelector('.rag-latency');

                if (kbVersionEl) kbVersionEl.textContent = data.kb_version || 'unknown';
                if (indexVersionEl) indexVersionEl.textContent = data.index_version || 'unknown';
                
                if (latencyEl && data.latency_ms) {
                    latencyEl.textContent = `(${data.latency_ms}ms)`;
                }

                this.showFooter(drawer);
            }

            // Show feedback panel
            const fb = drawer.querySelector('.rag-feedback');
            if (fb) fb.style.display = 'block';
            drawer.dataset.ragLastQuery = (data._original_query || '');
            drawer.dataset.ragBestAuthority = (data.best_authority || 'WORKING');
            drawer.dataset.ragLatency = (data.latency_ms || '');
            drawer.dataset.ragCitations = JSON.stringify(data.citations || []);
        },

        /**
         * Display citations list
         */
        displayCitations: function(citations, drawer) {
            if (!drawer) {
                drawer = document.querySelector('.offcanvas[id^="ragExplainDrawer_"]');
            }
            
            const listEl = drawer ? drawer.querySelector('.rag-citations-list') : null;
            const countEl = drawer ? drawer.querySelector('.rag-citation-count') : null;
            
            if (!listEl) return;

            // Update count
            if (countEl) {
                countEl.textContent = citations.length;
            }

            // Clear existing citations
            listEl.innerHTML = '';

            // Add citations
            citations.forEach((citation, index) => {
                const item = this.createCitationItem(citation, index);
                listEl.appendChild(item);
            });
        },

        /**
         * Create citation list item
         */
        createCitationItem: function(citation, index) {
            const item = document.createElement('div');
            item.className = 'list-group-item';

            const authority = citation.authority || 'WORKING';
            const authorityBadge = this.getAuthorityBadge(authority);
            
            const title = citation.title || citation.kb_path || 'Untitled';
            const path = citation.kb_path || citation.source_path || '';
            const score = citation.score ? citation.score.toFixed(3) : '0.000';
            const lastModified = citation.last_modified || '';

            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-1">
                            <span class="badge bg-secondary me-2">#${index + 1}</span>
                            ${authorityBadge}
                        </div>
                        <h6 class="mb-1">${this.escapeHtml(title)}</h6>
                        <small class="text-muted d-block">${this.escapeHtml(path)}</small>
                        ${lastModified ? `<small class="text-muted d-block mt-1"><i class="fas fa-clock me-1"></i>${this.escapeHtml(lastModified)}</small>` : ''}
                    </div>
                    <div class="text-end">
                        <small class="text-muted">Score: ${score}</small>
                    </div>
                </div>
            `;

            return item;
        },

        /**
         * Get authority badge HTML
         */
        getAuthorityBadge: function(authority) {
            const badges = {
                'CANONICAL': '<span class="badge bg-success text-white ms-2">✅ CANONICAL</span>',
                'WORKING': '<span class="badge bg-warning text-dark ms-2">⚠️ WORKING</span>',
                'DRAFT': '<span class="badge bg-secondary text-white ms-2">🧪 DRAFT</span>',
                'DEPRECATED': '<span class="badge bg-danger text-white ms-2">❌ DEPRECATED</span>',
            };
            return badges[authority.toUpperCase()] || badges['WORKING'];
        },

        /**
         * Get best authority from citations
         */
        getBestAuthority: function(citations) {
            if (!citations || citations.length === 0) {
                return 'WORKING';
            }

            const authorityPriority = {
                'CANONICAL': 4,
                'WORKING': 3,
                'DRAFT': 2,
                'DEPRECATED': 1,
            };

            let bestAuthority = 'WORKING';
            let bestPriority = 0;

            citations.forEach(citation => {
                const auth = (citation.authority || 'WORKING').toUpperCase();
                const priority = authorityPriority[auth] || 0;
                if (priority > bestPriority) {
                    bestPriority = priority;
                    bestAuthority = auth;
                }
            });

            return bestAuthority;
        },

        /**
         * Show/hide UI states (scoped to drawer)
         */
        showLoading: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-loading') : null;
            if (el) el.style.display = 'block';
        },

        hideLoading: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-loading') : null;
            if (el) el.style.display = 'none';
        },

        showError: function(message, drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-error') : null;
            const textEl = drawer ? drawer.querySelector('.rag-explain-error-text') : null;
            if (el) el.style.display = 'block';
            if (textEl) textEl.textContent = message;
        },

        hideError: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-error') : null;
            if (el) el.style.display = 'none';
        },

        showAnswer: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-answer') : null;
            if (el) el.style.display = 'block';
        },

        hideAnswer: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-answer') : null;
            if (el) el.style.display = 'none';
        },

        showCitations: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-citations') : null;
            if (el) el.style.display = 'block';
        },

        hideCitations: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-citations') : null;
            if (el) el.style.display = 'none';
        },

        showFooter: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-footer') : null;
            if (el) el.style.display = 'block';
        },

        hideFooter: function(drawer) {
            const el = drawer ? drawer.querySelector('.rag-explain-footer') : null;
            if (el) el.style.display = 'none';
        },

        resetDrawerState: function(drawer) {
            if (!drawer) return;
            this.hideLoading(drawer);
            this.hideError(drawer);
            this.hideAnswer(drawer);
            this.hideCitations(drawer);
            this.hideFooter(drawer);
            
            // Clear best authority badge
            const bestAuthEl = drawer.querySelector('[id$="BestAuthority"]');
            if (bestAuthEl) bestAuthEl.innerHTML = '';
        },

        /**
         * Utility: Get CSRF token
         */
        getCsrfToken: function() {
            const token = document.querySelector('meta[name="csrf-token"]');
            return token ? token.getAttribute('content') : '';
        },

        /**
         * Utility: Escape HTML
         */
        escapeHtml: function(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },
    };

    // Auto-initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => RagUI.init());
    } else {
        RagUI.init();
    }

    // Export for global access
    window.RagUI = RagUI;

})();

