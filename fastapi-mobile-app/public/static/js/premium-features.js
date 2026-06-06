/**
 * Premium Features with Authentication Check
 */

// Protected premium functions
async function calculatePremium() {
    if (!authGuard.isAuthenticated()) {
        authGuard.showAuthRequiredMessage();
        return;
    }

    const expression = document.getElementById('calcInput').value;
    const resultDiv = document.getElementById('calcResult');
    
    const token = localStorage.getItem('access_token');
    if (!token) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '❌ Please login to access premium features';
        return;
    }

    try {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '🔄 Calculating...';

        const response = await fetch(`/api/advanced-calculator/${encodeURIComponent(expression)}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                authGuard.showAuthRequiredMessage();
                return;
            }
            throw new Error('Calculation failed');
        }
        
        const data = await response.json();
        resultDiv.innerHTML = `✅ Result: ${data.result}`;
    } catch (error) {
        resultDiv.innerHTML = '❌ Error: ' + error.message;
    }
}

async function testCurrency() {
    if (!authGuard.isAuthenticated()) {
        authGuard.showAuthRequiredMessage();
        return;
    }

    const amount = document.getElementById('currencyAmount').value;
    const from = document.getElementById('fromCurrency').value;
    const to = document.getElementById('toCurrency').value;
    const resultDiv = document.getElementById('currencyResult');
    
    const token = localStorage.getItem('access_token');
    if (!token) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '❌ Please login to access premium features';
        return;
    }

    try {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '🔄 Converting...';

        const response = await fetch(`/api/currency-convert/${amount}/${from}/${to}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                authGuard.showAuthRequiredMessage();
                return;
            }
            throw new Error('Currency conversion failed');
        }
        
        const data = await response.json();
        resultDiv.innerHTML = `✅ ${amount} ${from} = ${data.converted_amount} ${to}`;
    } catch (error) {
        resultDiv.innerHTML = '❌ Error: ' + error.message;
    }
}

function showPremium() {
    if (!authGuard.isAuthenticated()) {
        authGuard.showAuthRequiredMessage();
        return;
    }
    
    hideAllSections();
    document.getElementById('premium-section').style.display = 'block';
}

// Update the global functions
window.calculatePremium = calculatePremium;
window.testCurrency = testCurrency;
window.showPremium = showPremium;
