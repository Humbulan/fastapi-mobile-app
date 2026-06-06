/**
 * Authentication Guard for Premium Features
 * Prevents access to premium features without authentication
 */

class AuthGuard {
    constructor() {
        this.init();
    }

    init() {
        console.log('🛡️ Auth Guard initialized');
        this.protectPremiumFeatures();
        this.setupAuthListeners();
    }

    protectPremiumFeatures() {
        // Protect all premium feature buttons
        document.addEventListener('DOMContentLoaded', () => {
            this.checkAuthStatus();
        });

        // Also check when premium buttons are clicked
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('premium-feature') || 
                e.target.classList.contains('btn-premium') ||
                e.target.closest('.premium-feature') ||
                e.target.closest('.btn-premium')) {
                
                if (!this.isAuthenticated()) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.showAuthRequiredMessage();
                    return false;
                }
            }
        });
    }

    setupAuthListeners() {
        // Listen for auth status changes
        window.addEventListener('storage', (e) => {
            if (e.key === 'access_token') {
                this.checkAuthStatus();
            }
        });

        // Custom event for auth changes
        document.addEventListener('authStatusChanged', () => {
            this.checkAuthStatus();
        });
    }

    isAuthenticated() {
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username');
        return !!(token && username);
    }

    checkAuthStatus() {
        const isAuthenticated = this.isAuthenticated();
        const premiumButtons = document.querySelectorAll('.premium-feature, .btn-premium');
        
        premiumButtons.forEach(button => {
            if (isAuthenticated) {
                button.disabled = false;
                button.style.opacity = '1';
                button.style.cursor = 'pointer';
                button.title = '';
            } else {
                button.disabled = true;
                button.style.opacity = '0.6';
                button.style.cursor = 'not-allowed';
                button.title = 'Please login to access this feature';
                
                // Replace click behavior for premium buttons
                button.onclick = (e) => {
                    e.preventDefault();
                    this.showAuthRequiredMessage();
                    return false;
                };
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
                    <a href="#" class="logout-btn" style="color: #dc3545;">Logout</a>
                `;
            } else {
                authDiv.innerHTML = `
                    <a href="#" onclick="showLogin()">Login</a> | 
                    <a href="#" onclick="showRegister()">Register</a>
                `;
            }
        }
    }

    showAuthRequiredMessage() {
        alert('🔐 Authentication Required\n\nPlease login or register to access premium features.');
        
        // Optionally show login form
        if (typeof showLogin === 'function') {
            setTimeout(() => {
                if (confirm('Would you like to login now?')) {
                    showLogin();
                }
            }, 100);
        }
    }

    requireAuth(callback) {
        return (...args) => {
            if (!this.isAuthenticated()) {
                this.showAuthRequiredMessage();
                return false;
            }
            return callback(...args);
        };
    }
}

// Create global instance
window.authGuard = new AuthGuard();

// Protect specific premium functions
if (typeof calculatePremium === 'function') {
    window.calculatePremium = authGuard.requireAuth(calculatePremium);
}

if (typeof testCurrency === 'function') {
    window.testCurrency = authGuard.requireAuth(testCurrency);
}

if (typeof showPremium === 'function') {
    window.showPremium = authGuard.requireAuth(showPremium);
}
