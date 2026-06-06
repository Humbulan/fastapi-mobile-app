/**
 * Aggressive Auth Request Interceptor
 * Fixes all /api/register and /api/login requests to use local endpoints
 */

console.log('🔧 Loading auth interceptor...');

// Intercept ALL fetch requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    let url = args[0];
    
    // Convert Request object to URL string if needed
    if (url instanceof Request) {
        url = url.url;
    }
    
    // Fix auth endpoints
    if (typeof url === 'string') {
        // Fix register endpoints
        if (url.includes('/api/register') && !url.includes('/api/local/register')) {
            console.log('🔄 Interceptor: Redirecting /api/register to /api/local/register');
            args[0] = '/api/local/register';
        }
        // Fix login endpoints  
        else if (url.includes('/api/login') && !url.includes('/api/local/login')) {
            console.log('🔄 Interceptor: Redirecting /api/login to /api/local/login');
            args[0] = '/api/local/login';
        }
    }
    
    return originalFetch.apply(this, args);
};

console.log('✅ Auth interceptor loaded successfully');
