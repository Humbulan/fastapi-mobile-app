/**
 * STRONG Authentication Blocker
 * Definitely prevents premium features without authentication
 */

console.log('🛡️ STRONG Auth Blocker loaded');

// Override ALL premium feature functions
function blockPremiumFeatures() {
    console.log('🔒 Blocking premium features for non-authenticated users');
    
    // Override calculatePremium
    if (typeof window.originalCalculatePremium === 'undefined') {
        window.originalCalculatePremium = window.calculatePremium;
    }
    window.calculatePremium = function() {
        if (!isUserAuthenticated()) {
            showStrongAuthMessage();
            return false;
        }
        return window.originalCalculatePremium.apply(this, arguments);
    };
    
    // Override testCurrency
    if (typeof window.originalTestCurrency === 'undefined') {
        window.originalTestCurrency = window.testCurrency;
    }
    window.testCurrency = function() {
        if (!isUserAuthenticated()) {
            showStrongAuthMessage();
            return false;
        }
        return window.originalTestCurrency.apply(this, arguments);
    };
    
    // Override showPremium
    if (typeof window.originalShowPremium === 'undefined') {
        window.originalShowPremium = window.showPremium;
    }
    window.showPremium = function() {
        if (!isUserAuthenticated()) {
            showStrongAuthMessage();
            return false;
        }
        return window.originalShowPremium.apply(this, arguments);
    };
    
    // Disable premium buttons visually
    disablePremiumButtons();
}

function isUserAuthenticated() {
    const token = localStorage.getItem('access_token');
    const username = localStorage.getItem('username');
    const isAuth = !!(token && username);
    console.log('🔍 Auth check:', { token: !!token, username: !!username, isAuth });
    return isAuth;
}

function showStrongAuthMessage() {
    console.log('🚫 Blocked premium feature access - user not authenticated');
    alert('🚫 ACCESS DENIED\n\nYou must be logged in to use premium features.\n\nPlease register or login first.');
    
    // Force focus to auth section
    const authDiv = document.getElementById('auth-status');
    if (authDiv) {
        authDiv.scrollIntoView({ behavior: 'smooth' });
        authDiv.style.background = '#fff3cd';
        authDiv.style.border = '2px solid #ffc107';
        authDiv.style.padding = '10px';
        authDiv.style.borderRadius = '5px';
        setTimeout(() => {
            authDiv.style.background = '';
            authDiv.style.border = '';
        }, 3000);
    }
}

function disablePremiumButtons() {
    const premiumButtons = document.querySelectorAll('.btn-premium, .premium-feature, [onclick*="Premium"], [onclick*="premium"]');
    
    premiumButtons.forEach(button => {
        if (!isUserAuthenticated()) {
            // Make button look disabled
            button.style.opacity = '0.5';
            button.style.cursor = 'not-allowed';
            button.style.position = 'relative';
            
            // Add overlay to prevent clicks
            if (!button.querySelector('.blocker-overlay')) {
                const overlay = document.createElement('div');
                overlay.className = 'blocker-overlay';
                overlay.style.position = 'absolute';
                overlay.style.top = '0';
                overlay.style.left = '0';
                overlay.style.width = '100%';
                overlay.style.height = '100%';
                overlay.style.cursor = 'not-allowed';
                overlay.style.zIndex = '10';
                button.style.position = 'relative';
                button.appendChild(overlay);
            }
            
            // Replace onclick handler
            button.setAttribute('data-original-onclick', button.getAttribute('onclick') || '');
            button.setAttribute('onclick', 'showStrongAuthMessage(); return false;');
        } else {
            // Restore button if authenticated
            button.style.opacity = '1';
            button.style.cursor = 'pointer';
            const overlay = button.querySelector('.blocker-overlay');
            if (overlay) overlay.remove();
            
            const originalOnClick = button.getAttribute('data-original-onclick');
            if (originalOnClick) {
                button.setAttribute('onclick', originalOnClick);
            }
        }
    });
}

// Initialize immediately
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded - initializing auth blocker');
    blockPremiumFeatures();
    disablePremiumButtons();
});

// Also check when page fully loads
window.addEventListener('load', function() {
    console.log('📄 Page fully loaded - reinforcing auth blocker');
    setTimeout(blockPremiumFeatures, 100);
    setTimeout(disablePremiumButtons, 200);
});

// Monitor auth changes
window.addEventListener('storage', function(e) {
    if (e.key === 'access_token' || e.key === 'username') {
        console.log('🔄 Auth storage changed - updating blocker');
        setTimeout(blockPremiumFeatures, 50);
        setTimeout(disablePremiumButtons, 100);
    }
});

// Create custom event for auth changes
function triggerAuthChange() {
    window.dispatchEvent(new CustomEvent('authChange'));
}
window.triggerAuthChange = triggerAuthChange;

// Monitor clicks on premium buttons
document.addEventListener('click', function(e) {
    const target = e.target;
    const isPremiumButton = target.classList.contains('btn-premium') || 
                           target.classList.contains('premium-feature') ||
                           target.closest('.btn-premium') || 
                           target.closest('.premium-feature');
    
    if (isPremiumButton && !isUserAuthenticated()) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        showStrongAuthMessage();
        return false;
    }
}, true); // Use capture phase to catch early

console.log('✅ Strong Auth Blocker initialized');
