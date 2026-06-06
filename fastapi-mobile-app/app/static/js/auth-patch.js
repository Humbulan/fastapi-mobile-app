/**
 * Auth Patch - Fixes the inline JavaScript functions
 */

console.log('🔧 Loading auth patch...');

// Override the problematic showLogin function
if (typeof showLogin === 'function') {
    const originalShowLogin = showLogin;
    window.showLogin = async function() {
        const username = prompt('Enter username:');
        const password = prompt('Enter password:');
        if (username && password) {
            try {
                console.log('🔑 Patch: Fixed login request');
                const response = await fetch('/api/local/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`Login failed: ${response.status}`);
                }
                
                const data = await response.json();
                if (response.ok) {
                    currentUser = data.username;
                    currentToken = data.access_token;
                    updateAuthUI();
                    alert('✅ Login successful! Welcome ' + data.username);
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('❌ Login failed: ' + error.message);
            }
        }
    };
    console.log('✅ Patched showLogin function');
}

// Override the problematic showRegister function  
if (typeof showRegister === 'function') {
    const originalShowRegister = showRegister;
    window.showRegister = async function() {
        const username = prompt('Enter username:');
        const email = prompt('Enter email:');
        const fullName = prompt('Enter full name:');
        const password = prompt('Enter password:');
        if (username && email && fullName && password) {
            try {
                console.log('📝 Patch: Fixed register request');
                const response = await fetch('/api/local/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        email: email,
                        password: password,
                        full_name: fullName
                    })
                });
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `Registration failed: ${response.status}`);
                }
                
                const data = await response.json();
                alert('✅ Registration successful! Welcome ' + data.username);
            } catch (error) {
                console.error('Registration error:', error);
                alert('❌ Registration failed: ' + error.message);
            }
        }
    };
    console.log('✅ Patched showRegister function');
}

console.log('✅ Auth patch loaded successfully');
