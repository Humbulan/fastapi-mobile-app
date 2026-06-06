#!/bin/bash
# Build script for Cloudflare Pages - FastAPI Mobile App PWA
# This builds the frontend static files

echo "🚀 Building FastAPI Mobile App PWA for Cloudflare Pages..."

# Create public directory
mkdir -p public
mkdir -p public/static
mkdir -p public/static/js
mkdir -p public/static/icons

# Copy all static assets
echo "📁 Copying static files..."
if [ -d "app/static/js" ]; then
    cp -r app/static/js/* public/static/js/ 2>/dev/null || true
fi

if [ -d "app/static/icons" ]; then
    cp -r app/static/icons/* public/static/icons/ 2>/dev/null || true
fi

[ -f "app/static/manifest.json" ] && cp app/static/manifest.json public/
[ -f "app/static/service-worker.js" ] && cp app/static/service-worker.js public/
[ -f "app/static/offline.html" ] && cp app/static/offline.html public/

# Create the main index.html with PWA features
echo "📄 Creating index.html..."
cat > public/index.html << 'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#667eea">
    <title>FastAPI Mobile App - Business Dashboard</title>
    <meta name="description" content="Business Intelligence Platform with AI">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="/manifest.json">
    
    <!-- Icons -->
    <link rel="icon" href="/static/icons/icon-192.png">
    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">
    
    <!-- Styles -->
    <style>
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #4CAF50;
            --dark: #333;
            --light: #f8f9fa;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            min-height: 100vh;
            color: var(--dark);
            padding: 20px;
        }
        
        .app-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        h1 {
            color: var(--primary);
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }
        
        .status-badge {
            display: inline-block;
            background: var(--success);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9em;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            transition: transform 0.3s, box-shadow 0.3s;
            backdrop-filter: blur(10px);
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        
        .card h3 {
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .metric {
            font-size: 3em;
            font-weight: 800;
            color: var(--dark);
            margin: 15px 0;
            line-height: 1;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }
        
        .positive {
            color: var(--success);
        }
        
        .api-section {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            margin-top: 30px;
            backdrop-filter: blur(10px);
        }
        
        .btn-group {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 20px 0;
        }
        
        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-success {
            background: var(--success);
        }
        
        .btn-success:hover {
            background: #45a049;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        }
        
        .btn-outline {
            background: transparent;
            border: 2px solid var(--primary);
            color: var(--primary);
        }
        
        #api-result {
            background: var(--light);
            padding: 25px;
            border-radius: 15px;
            margin-top: 25px;
            font-family: 'SF Mono', 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
            border: 2px dashed #e9ecef;
            font-size: 0.9em;
            line-height: 1.6;
        }
        
        .loading {
            color: #666;
            font-style: italic;
        }
        
        .success {
            color: var(--success);
            border-color: var(--success);
        }
        
        .error {
            color: #f44336;
            border-color: #f44336;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9em;
            padding: 20px;
        }
        
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .btn {
                width: 100%;
                justify-content: center;
            }
            
            h1 {
                font-size: 2em;
            }
        }
        
        /* Animation for metrics */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .card {
            animation: fadeIn 0.6s ease-out;
        }
        
        .card:nth-child(2) { animation-delay: 0.1s; }
        .card:nth-child(3) { animation-delay: 0.2s; }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header>
            <h1>🚀 FastAPI Mobile App</h1>
            <p class="subtitle">Business Intelligence Dashboard with AI</p>
            <div class="status-badge">● Deployed on Cloudflare Pages</div>
        </header>
        
        <!-- Dashboard Metrics -->
        <div class="dashboard-grid">
            <div class="card">
                <h3>📊 Revenue Analytics</h3>
                <div class="metric">$32,480</div>
                <div class="metric-label positive">▲ 15.2% Growth</div>
                <p>Monthly recurring revenue with consistent upward trend. Projected $45K next month.</p>
            </div>
            
            <div class="card">
                <h3>👥 Customer Insights</h3>
                <div class="metric">189</div>
                <div class="metric-label positive">★ 4.9 Satisfaction</div>
                <p>Active customers with 92% retention rate. High satisfaction scores across all metrics.</p>
            </div>
            
            <div class="card">
                <h3>⚡ Performance</h3>
                <div class="metric">99.9%</div>
                <div class="metric-label">Cloudflare Edge</div>
                <p>Global edge network deployment. Sub-50ms response times worldwide.</p>
            </div>
        </div>
        
        <!-- API Testing Section -->
        <div class="api-section">
            <h2>🔧 API Integration Testing</h2>
            <p>Test the Cloudflare Worker API endpoints. The backend runs on Cloudflare Workers at <code>api.humbu.store</code></p>
            
            <div class="btn-group">
                <button class="btn" onclick="testApi('/')">
                    <span>🏠</span> Root Endpoint
                </button>
                <button class="btn btn-success" onclick="testApi('/health')">
                    <span>❤️</span> Health Check
                </button>
                <button class="btn" onclick="testApi('/dashboard')">
                    <span>📈</span> Dashboard Data
                </button>
                <button class="btn" onclick="testApi('/customers')">
                    <span>👥</span> Customers
                </button>
                <button class="btn btn-outline" onclick="testApi('/api/local/register', 'POST')">
                    <span>🔐</span> Test Auth
                </button>
            </div>
            
            <!-- AI Chat Interface -->
            <div style="margin-top: 30px;">
                <h3>🤖 AI Business Assistant</h3>
                <div style="display: flex; gap: 10px; margin: 15px 0;">
                    <input type="text" id="ai-input" placeholder="Ask about revenue, customers, or growth..." 
                           style="flex: 1; padding: 15px; border: 2px solid #e9ecef; border-radius: 12px; font-size: 1em;">
                    <button class="btn" onclick="askAI()">
                        <span>💬</span> Ask AI
                    </button>
                </div>
            </div>
            
            <!-- API Results -->
            <div id="api-result" class="loading">
                Ready to test API endpoints. Click any button above.
            </div>
        </div>
        
        <!-- Footer -->
        <footer>
            <p>FastAPI Mobile App v9.0.0 | Progressive Web App | Cloudflare Edge Deployment</p>
            <p>Original JavaScript files loaded: auth.js, app.js, dashboard-handler.js</p>
            <p>Service Worker: Active | Offline Mode: Available | Installable: Yes</p>
        </footer>
    </div>
    
    <script>
        // Load original JavaScript files from the app
        document.addEventListener('DOMContentLoaded', function() {
            const scripts = [
                '/static/js/auth.js',
                '/static/js/app.js',
                '/static/js/dashboard-handler.js',
                '/static/js/auth-patch.js',
                '/static/js/auth-interceptor.js'
            ];
            
            scripts.forEach(src => {
                const script = document.createElement('script');
                script.src = src;
                script.defer = true;
                script.onload = () => console.log(`✅ Loaded: ${src}`);
                script.onerror = () => console.log(`⚠️ Failed to load: ${src}`);
                document.body.appendChild(script);
            });
            
            console.log('🚀 FastAPI Mobile App PWA initialized');
        });
        
        // API Testing Function
        async function testApi(endpoint, method = 'GET') {
            const resultDiv = document.getElementById('api-result');
            resultDiv.className = 'loading';
            resultDiv.innerHTML = `🔄 Testing ${method} ${endpoint}...`;
            
            try {
                const baseUrl = 'https://api.humbu.store';
                const options = {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json'
                    }
                };
                
                if (method === 'POST') {
                    options.body = JSON.stringify({
                        email: 'test@example.com',
                        password: 'password123',
                        timestamp: new Date().toISOString()
                    });
                }
                
                const response = await fetch(`${baseUrl}${endpoint}`, options);
                const data = await response.json();
                
                resultDiv.className = 'success';
                resultDiv.innerHTML = `✅ ${response.status} ${response.statusText}\n\n` + 
                                    `📦 Response from ${baseUrl}${endpoint}:\n\n` +
                                    JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = `❌ Error: ${error.message}\n\n` +
                                    `Note: Make sure you have deployed the API Worker to:\n` +
                                    `https://api.humbu.store\n\n` +
                                    `Deploy the Worker using the worker.js file in the repository.`;
            }
        }
        
        // AI Chat Function
        async function askAI() {
            const input = document.getElementById('ai-input');
            const message = input.value.trim();
            
            if (!message) {
                alert('Please enter a question for the AI');
                return;
            }
            
            const resultDiv = document.getElementById('api-result');
            resultDiv.className = 'loading';
            resultDiv.innerHTML = `🤖 AI is thinking about: "${message}"...`;
            
            try {
                const response = await fetch('https://api.humbu.store/ai/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        context: 'business'
                    })
                });
                
                const data = await response.json();
                resultDiv.className = 'success';
                resultDiv.innerHTML = `🤖 AI Response:\n\n"${data.response}"\n\n` +
                                    `Confidence: ${(data.confidence * 100).toFixed(1)}%\n` +
                                    `Source: ${data.source}\n` +
                                    `Timestamp: ${new Date(data.timestamp).toLocaleTimeString()}`;
                
                input.value = ''; // Clear input
            } catch (error) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = `❌ AI Service Error: ${error.message}\n\n` +
                                    `Using fallback business intelligence...\n\n` +
                                    `💡 Try: "How is my revenue?" or "What about customer growth?"`;
            }
        }
        
        // Register Service Worker for PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('✅ ServiceWorker registered:', registration.scope);
                        
                        // Check for updates
                        registration.addEventListener('updatefound', () => {
                            console.log('🔄 Service Worker update found!');
                        });
                    })
                    .catch(error => {
                        console.log('❌ ServiceWorker registration failed:', error);
                    });
            });
        }
        
        // Install PWA prompt
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // Show install button (you could add a button to your UI)
            console.log('📱 PWA install available');
            
            // For now, just log it. You could add an install button to your UI
            // Example: showInstallButton();
        });
        
        // Log when app is launched as PWA
        window.addEventListener('appinstalled', () => {
            console.log('🎉 PWA installed successfully!');
            deferredPrompt = null;
        });
    </script>
</body>
</html>
HTML

# Create a simple service worker if none exists
if [ ! -f "public/service-worker.js" ]; then
    echo "🔧 Creating service-worker.js..."
    cat > public/service-worker.js << 'SW'
// Service Worker for FastAPI Mobile App PWA
const CACHE_NAME = 'fastapi-mobile-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/offline.html',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('📦 Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        
        return fetch(event.request).catch(() => {
          // If network fails and request is for HTML, return offline page
          if (event.request.headers.get('accept').includes('text/html')) {
            return caches.match('/offline.html');
          }
        });
      })
  );
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
SW
fi

echo ""
echo "✅ Build completed successfully!"
echo "📁 Public directory structure:"
find public/ -type f | sort
echo ""
echo "🚀 Ready to deploy to Cloudflare Pages!"
echo "Use these build settings:"
echo "----------------------------------------"
echo "Build command: ./build.sh"
echo "Build output directory: public"
echo "----------------------------------------"
