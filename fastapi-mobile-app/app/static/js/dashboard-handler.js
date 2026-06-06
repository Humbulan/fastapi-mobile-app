/**
 * Dashboard Access Handler
 * Handles authenticated access to the dashboard with proper token sending
 */

class DashboardHandler {
    constructor() {
        this.init();
    }

    init() {
        console.log('🚀 Dashboard Handler initialized');
        this.setupDashboardLink();
        this.setupAuthButtons();
    }

    setupDashboardLink() {
        document.addEventListener('DOMContentLoaded', () => {
            this.updateDashboardLink();
        });

        window.addEventListener('storage', (e) => {
            if (e.key === 'access_token' || e.key === 'username') {
                setTimeout(() => this.updateDashboardLink(), 100);
            }
        });
    }

    setupAuthButtons() {
        // Intercept all auth-required button clicks
        document.addEventListener('click', (e) => {
            const target = e.target;
            
            // Handle dashboard button
            if (target.id === 'dashboard-btn' || target.classList.contains('go-to-dashboard')) {
                e.preventDefault();
                this.accessDashboard();
                return false;
            }
            
            // Handle other protected buttons
            if (target.classList.contains('protected-btn')) {
                e.preventDefault();
                this.handleProtectedAction(target.dataset.action);
                return false;
            }
        });
    }

    updateDashboardLink() {
        const isAuthenticated = this.isAuthenticated();
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username');
        
        console.log('🔍 Dashboard Link Update:', { isAuthenticated, token, username });
        
        // Update any dashboard buttons on the page
        const dashboardButtons = document.querySelectorAll('#dashboard-btn, .go-to-dashboard');
        dashboardButtons.forEach(btn => {
            if (isAuthenticated && token) {
                btn.style.display = 'inline-block';
                btn.disabled = false;
                btn.innerHTML = '🎯 Go to Dashboard';
            } else {
                btn.style.display = 'none';
                btn.disabled = true;
                btn.innerHTML = '🔒 Login Required';
            }
        });

        // Update auth status display
        this.updateAuthDisplay();
    }

    updateAuthDisplay() {
        const isAuthenticated = this.isAuthenticated();
        const username = localStorage.getItem('username');
        const authDiv = document.getElementById('auth-status');
        
        if (authDiv) {
            if (isAuthenticated) {
                authDiv.innerHTML = `
                    ✅ Logged in as <strong>${username}</strong> | 
                    <a href="#" onclick="dashboardHandler.logout()" style="color: #dc3545;">Logout</a>
                `;
            } else {
                authDiv.innerHTML = `
                    <a href="#" onclick="showLogin()">Login</a> | 
                    <a href="#" onclick="showRegister()">Register</a>
                `;
            }
        }
    }

    isAuthenticated() {
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username');
        const isAuth = !!(token && username);
        console.log('🔐 Auth Check:', { token: !!token, username: !!username, isAuth });
        return isAuth;
    }

    async accessDashboard() {
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username');
        
        console.log('🎯 Accessing Dashboard:', { token, username });

        if (!this.isAuthenticated()) {
            alert('🔐 Please login first to access the dashboard.');
            return;
        }

        // Show loading state
        this.showLoading('Accessing Dashboard...');

        try {
            console.log('🔑 Sending request to /dashboard with token');
            
            // Method 1: Use fetch with Authorization header
            const response = await fetch('/dashboard', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            });

            console.log('📨 Response status:', response.status);
            
            if (response.ok) {
                console.log('✅ Dashboard access successful, redirecting...');
                // If fetch works, the server will return the dashboard HTML
                // We need to handle the response properly
                const html = await response.text();
                document.open();
                document.write(html);
                document.close();
            } else {
                console.log('❌ Fetch failed, status:', response.status);
                
                // Try alternative method: redirect with query parameter
                console.log('🔄 Trying alternative method with query parameter...');
                window.location.href = `/dashboard?token=${encodeURIComponent(token)}`;
            }

        } catch (error) {
            console.error('❌ Dashboard access error:', error);
            
            // Final fallback: try direct redirect with query parameter
            console.log('🔄 Using query parameter fallback...');
            window.location.href = `/dashboard?token=${encodeURIComponent(token)}`;
        } finally {
            this.hideLoading();
        }
    }

    async handleProtectedAction(action) {
        const token = localStorage.getItem('access_token');
        
        if (!this.isAuthenticated()) {
            alert('🔐 Please login first.');
            return;
        }

        this.showLoading(`Processing ${action}...`);

        try {
            let response;
            switch(action) {
                case 'calculator':
                    response = await fetch('/api/calculator', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    break;
                case 'text-tools':
                    response = await fetch('/api/text-tools', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    break;
                case 'premium':
                    response = await fetch('/api/premium-features', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    break;
                default:
                    throw new Error('Unknown action');
            }

            if (response.ok) {
                const data = await response.json();
                alert(`✅ ${action} accessed successfully!`);
            } else {
                throw new Error(`Failed to access ${action}`);
            }

        } catch (error) {
            console.error(`❌ ${action} error:`, error);
            alert(`❌ Failed to access ${action}: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    showLoading(message = 'Loading...') {
        let loadingDiv = document.getElementById('global-loading');
        if (!loadingDiv) {
            loadingDiv = document.createElement('div');
            loadingDiv.id = 'global-loading';
            loadingDiv.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.7);
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                font-size: 18px;
            `;
            document.body.appendChild(loadingDiv);
        }
        
        loadingDiv.innerHTML = `
            <div style="text-align: center;">
                <div style="font-size: 48px; margin-bottom: 20px;">⏳</div>
                <div>${message}</div>
                <div style="font-size: 14px; margin-top: 10px; opacity: 0.8;">Please wait...</div>
            </div>
        `;
        loadingDiv.style.display = 'flex';
    }

    hideLoading() {
        const loading = document.getElementById('global-loading');
        if (loading) {
            loading.style.display = 'none';
        }
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
        localStorage.removeItem('premium');
        alert('✅ Logged out successfully');
        window.location.href = '/';
        return false;
    }
}

// Create global instance
window.dashboardHandler = new DashboardHandler();

// Global function for dashboard access
window.accessDashboard = function() {
    window.dashboardHandler.accessDashboard();
};

// Debug function
window.debugAuth = function() {
    const token = localStorage.getItem('access_token');
    const username = localStorage.getItem('username');
    console.log('🐛 Auth Debug:', { token, username });
    alert(`Auth Debug:\\nToken: ${token ? 'PRESENT' : 'MISSING'}\\nUsername: ${username || 'MISSING'}`);
};
