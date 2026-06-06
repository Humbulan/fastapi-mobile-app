// Authentication functions for the mobile app
class AuthManager {
    constructor() {
        this.baseUrl = '/api/local';
        this.init();
    }

    init() {
        console.log('🔐 Auth Manager initialized');
        this.setupEventListeners();
        this.checkAuthStatus();
    }

    setupEventListeners() {
        // These will be set up by the main app
        console.log('⚡ Setting up auth event listeners');
    }

    async register(userData) {
        try {
            console.log('📝 Attempting registration:', userData);
            
            const response = await fetch(`${this.baseUrl}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Registration failed' }));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('✅ Registration successful:', data);
            return data;
        } catch (error) {
            console.error('❌ Registration error:', error);
            throw error;
        }
    }

    async login(credentials) {
        try {
            console.log('🔑 Attempting login:', credentials);
            
            const response = await fetch(`${this.baseUrl}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('✅ Login successful:', data);
            
            // Store tokens if available
            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
            }
            if (data.refresh_token) {
                localStorage.setItem('refresh_token', data.refresh_token);
            }
            
            return data;
        } catch (error) {
            console.error('❌ Login error:', error);
            throw error;
        }
    }

    async logout() {
        try {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            console.log('✅ Logout successful');
            
            // Redirect to home page or show login
            window.location.href = '/';
        } catch (error) {
            console.error('❌ Logout error:', error);
        }
    }

    checkAuthStatus() {
        const token = localStorage.getItem('access_token');
        return !!token;
    }

    getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }
}

// Create global instance
window.authManager = new AuthManager();
