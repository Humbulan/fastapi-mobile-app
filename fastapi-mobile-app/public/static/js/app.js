// Main application JavaScript
class MobileApp {
    constructor() {
        this.authManager = window.authManager;
        this.init();
    }

    init() {
        console.log('🚀 Mobile App initializing...');
        this.setupAuthForms();
        this.setupNavigation();
        this.checkAuthentication();
    }

    setupAuthForms() {
        // Setup registration form if it exists
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        // Setup login form if it exists
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        // Setup logout button if it exists
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => this.handleLogout(e));
        }
    }

    async handleRegister(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const userData = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
            full_name: formData.get('full_name') || ''
        };

        try {
            const result = await this.authManager.register(userData);
            this.showMessage('✅ Registration successful! Please login.', 'success');
            event.target.reset();
            
            // Optionally redirect to login
            setTimeout(() => {
                this.showLoginForm();
            }, 2000);
        } catch (error) {
            this.showMessage(`❌ Registration failed: ${error.message}`, 'error');
        }
    }

    async handleLogin(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const credentials = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        try {
            const result = await this.authManager.login(credentials);
            this.showMessage('✅ Login successful!', 'success');
            
            // Redirect or update UI
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } catch (error) {
            this.showMessage(`❌ Login failed: ${error.message}`, 'error');
        }
    }

    async handleLogout(event) {
        event.preventDefault();
        await this.authManager.logout();
    }

    showMessage(message, type = 'info') {
        // Create or use existing message container
        let messageDiv = document.getElementById('message');
        if (!messageDiv) {
            messageDiv = document.createElement('div');
            messageDiv.id = 'message';
            messageDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 5px;
                color: white;
                z-index: 1000;
                max-width: 300px;
                word-wrap: break-word;
            `;
            document.body.appendChild(messageDiv);
        }

        messageDiv.textContent = message;
        messageDiv.style.backgroundColor = type === 'error' ? '#dc3545' : 
                                         type === 'success' ? '#28a745' : '#17a2b8';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
        
        messageDiv.style.display = 'block';
    }

    showLoginForm() {
        // Implementation depends on your UI structure
        console.log('Showing login form');
    }

    checkAuthentication() {
        const isAuthenticated = this.authManager.checkAuthStatus();
        if (isAuthenticated) {
            console.log('User is authenticated');
            // Update UI for authenticated user
        } else {
            console.log('User is not authenticated');
            // Update UI for guest
        }
    }

    setupNavigation() {
        // Setup any navigation-related functionality
        console.log('Navigation setup complete');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.mobileApp = new MobileApp();
    console.log('🎉 Mobile App initialized successfully!');
});
