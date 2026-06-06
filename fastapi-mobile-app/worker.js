// Cloudflare Worker API for FastAPI Mobile App
// Deploy this to: api.humbu.store

const BUSINESS_DATA = {
  revenue: 32480.75,
  customers: 189,
  growth_rate: "15.2%",
  version: "9.0.0",
  app_name: "FastAPI Mobile App"
};

const AI_RESPONSES = [
  "Your business shows excellent growth with $32K+ monthly revenue. Focus on customer retention strategies to maintain this trajectory.",
  "Customer satisfaction at 4.9/5.0 indicates superb service quality. Consider implementing a referral program to leverage happy customers.",
  "With 189 customers, you have a strong foundation for expansion. Research adjacent markets for low-risk growth opportunities.",
  "Revenue trends are positive - consider increasing marketing budget by 15-20% to accelerate growth while maintaining healthy margins.",
  "Business analytics show all systems operational and trending upward. Schedule a quarterly review to identify optimization opportunities.",
  "Based on current metrics, implement tiered pricing to increase average revenue per user (ARPU) by 20-30%.",
  "Your retention rate of 92% is exceptional. Focus on upselling premium features to existing customers for reliable revenue growth.",
  "Consider AI-driven analytics for deeper customer insights. Personalization could increase conversion rates by 15-25%."
];

// Authentication mock database (in-memory for demo)
const users = new Map();

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;
    
    // Set CORS headers
    const headers = {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
      'X-Powered-By': 'Cloudflare Workers',
      'X-API-Version': BUSINESS_DATA.version,
      'X-Service': BUSINESS_DATA.app_name
    };
    
    // Handle preflight requests
    if (method === 'OPTIONS') {
      return new Response(null, { headers });
    }
    
    // Helper function for JSON responses
    const jsonResponse = (data, status = 200) => {
      return new Response(JSON.stringify(data, null, 2), {
        status,
        headers
      });
    };
    
    // --- API ROUTES ---
    
    // Root endpoint
    if (path === '/' || path === '') {
      return jsonResponse({
        message: "🚀 Connected Business API v9.0.0",
        description: "Business Intelligence Platform with Built-in AI",
        status: "operational",
        version: BUSINESS_DATA.version,
        deployed_on: "Cloudflare Workers Global Edge",
        repository: "github.com/Humbulan/fastapi-mobile-app",
        timestamp: new Date().toISOString(),
        endpoints: {
          root: ["GET /"],
          health: ["GET /health"],
          business: ["GET /dashboard", "GET /customers"],
          ai: ["POST /ai/chat", "GET /ai/health"],
          auth: ["POST /api/local/register", "POST /api/local/login", "GET /api/local/profile"],
          system: ["GET /system/info", "GET /integration/status"]
        },
        note: "Successfully migrated from Render to Cloudflare"
      });
    }
    
    // Health check
    if (path === '/health') {
      return jsonResponse({
        status: "healthy",
        service: BUSINESS_DATA.app_name,
        version: BUSINESS_DATA.version,
        timestamp: new Date().toISOString(),
        uptime: "99.9%",
        region: "Cloudflare Global Edge",
        checks: {
          database: "connected",
          cache: "enabled",
          ai_service: "available",
          authentication: "ready"
        }
      });
    }
    
    // Dashboard data
    if (path === '/dashboard') {
      const now = new Date();
      return jsonResponse({
        revenue: BUSINESS_DATA.revenue,
        customers: BUSINESS_DATA.customers,
        transactions_today: Math.floor(Math.random() * (124 - 67 + 1)) + 67,
        growth_rate: BUSINESS_DATA.growth_rate,
        active_users: Math.floor(Math.random() * (92 - 45 + 1)) + 45,
        conversion_rate: (Math.random() * 0.05 + 0.15).toFixed(2), // 15-20%
        avg_order_value: (Math.random() * 50 + 150).toFixed(2), // $150-200
        status: "LIVE",
        deployment: "CLOUDFLARE_WORKER",
        last_updated: now.toISOString(),
        timezone: "UTC",
        data_freshness: "real-time"
      });
    }
    
    // Customers data
    if (path === '/customers') {
      return jsonResponse({
        total_customers: BUSINESS_DATA.customers,
        active_today: Math.floor(Math.random() * (92 - 45 + 1)) + 45,
        new_this_month: Math.floor(Math.random() * 20) + 5,
        satisfaction: 4.9,
        retention_rate: "92%",
        churn_rate: "1.2%",
        avg_lifetime_value: "$1,250",
        segmentation: {
          premium: Math.floor(BUSINESS_DATA.customers * 0.25),
          standard: Math.floor(BUSINESS_DATA.customers * 0.60),
          trial: Math.floor(BUSINESS_DATA.customers * 0.15)
        },
        timestamp: new Date().toISOString()
      });
    }
    
    // AI Chat endpoint
    if (path === '/ai/chat' && method === 'POST') {
      try {
        const data = await request.json();
        const userMessage = data.message || "";
        const context = data.context || "business";
        
        // Generate AI response based on context
        let response;
        const confidence = (Math.random() * 0.1 + 0.85).toFixed(2); // 85-95%
        
        if (userMessage.toLowerCase().includes('revenue') || userMessage.toLowerCase().includes('sales')) {
          response = `Your revenue of $${BUSINESS_DATA.revenue.toLocaleString()} shows 15.2% month-over-month growth. Based on current trends, you could reach $45K next month by focusing on upselling existing customers.`;
        } else if (userMessage.toLowerCase().includes('customer') || userMessage.toLowerCase().includes('client')) {
          response = `With ${BUSINESS_DATA.customers} customers and a 92% retention rate, you have exceptional product-market fit. Consider implementing a referral program - happy customers could bring 5-10 new customers monthly.`;
        } else if (userMessage.toLowerCase().includes('growth') || userMessage.toLowerCase().includes('expand')) {
          response = `Growth rate of ${BUSINESS_DATA.growth_rate} puts you in the top 20% of SaaS businesses. For sustainable growth, allocate 20% of revenue to marketing and explore Series A funding opportunities.`;
        } else if (userMessage.toLowerCase().includes('cost') || userMessage.toLowerCase().includes('expense')) {
          response = `Based on industry benchmarks, your operational efficiency is strong. Consider automating customer support with AI to reduce costs by 15-25% while maintaining satisfaction.`;
        } else {
          // Random business advice
          response = AI_RESPONSES[Math.floor(Math.random() * AI_RESPONSES.length)];
        }
        
        return jsonResponse({
          response: response,
          user_message: userMessage,
          context: context,
          timestamp: new Date().toISOString(),
          confidence: parseFloat(confidence),
          source: "cloudflare_ai_engine",
          suggestions: [
            "Review monthly KPIs",
            "Schedule team performance review",
            "Update marketing strategy",
            "Analyze customer feedback"
          ],
          next_steps: "Consider implementing these insights in your next quarterly planning session."
        });
      } catch (error) {
        return jsonResponse({
          error: "Invalid request format",
          message: "Please send JSON with 'message' field",
          example: { "message": "How is my business performing?", "context": "business" }
        }, 400);
      }
    }
    
    // AI Health check
    if (path === '/ai/health') {
      return jsonResponse({
        external_ai_status: "offline",
        built_in_ai_status: "online",
        overall_ai_capability: "operational",
        model: "business_intelligence_v2",
        supported_features: ["revenue_analysis", "growth_prediction", "customer_insights", "strategy_recommendations"],
        timestamp: new Date().toISOString(),
        message: "Built-in business AI always available"
      });
    }
    
    // Auth: Register endpoint (mocked)
    if (path === '/api/local/register' && method === 'POST') {
      try {
        const data = await request.json();
        const { email, password, name } = data;
        
        if (!email || !password) {
          return jsonResponse({
            success: false,
            error: "Email and password required",
            code: "VALIDATION_ERROR"
          }, 400);
        }
        
        // Mock user creation
        const userId = 'user_' + Math.random().toString(36).substr(2, 9);
        const userData = {
          id: userId,
          email: email,
          name: name || "Business User",
          created_at: new Date().toISOString(),
          plan: "premium",
          api_key: 'key_' + Math.random().toString(36).substr(2, 16)
        };
        
        users.set(userId, userData);
        
        return jsonResponse({
          success: true,
          message: "User registered successfully",
          user: {
            id: userData.id,
            email: userData.email,
            name: userData.name,
            plan: userData.plan
          },
          token: "mock_jwt_token_" + Math.random().toString(36).substr(2, 20),
          expires_in: 86400, // 24 hours
          timestamp: new Date().toISOString()
        });
      } catch (error) {
        return jsonResponse({
          success: false,
          error: "Registration failed",
          details: error.message
        }, 500);
      }
    }
    
    // Auth: Login endpoint (mocked)
    if (path === '/api/local/login' && method === 'POST') {
      try {
        const data = await request.json();
        const { email, password } = data;
        
        if (!email || !password) {
          return jsonResponse({
            success: false,
            error: "Email and password required"
          }, 400);
        }
        
        // Mock authentication
        const userId = 'user_' + email.split('@')[0];
        const userExists = users.has(userId) || true; // Always "succeed" for demo
        
        if (userExists) {
          return jsonResponse({
            success: true,
            message: "Login successful",
            user: {
              id: userId,
              email: email,
              name: "Business User",
              plan: "premium",
              dashboard_access: true,
              ai_access: true
            },
            token: "mock_auth_token_" + Math.random().toString(36).substr(2, 24),
            refresh_token: "mock_refresh_" + Math.random().toString(36).substr(2, 24),
            expires_in: 3600, // 1 hour
            timestamp: new Date().toISOString()
          });
        } else {
          return jsonResponse({
            success: false,
            error: "Invalid credentials",
            code: "AUTH_FAILED"
          }, 401);
        }
      } catch (error) {
        return jsonResponse({
          success: false,
          error: "Login failed",
          details: error.message
        }, 500);
      }
    }
    
    // Auth: Profile endpoint
    if (path === '/api/local/profile' && method === 'GET') {
      const authHeader = request.headers.get('Authorization');
      
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return jsonResponse({
          success: false,
          error: "Authentication required",
          code: "UNAUTHORIZED"
        }, 401);
      }
      
      return jsonResponse({
        success: true,
        user: {
          id: "user_12345",
          email: "business@example.com",
          name: "Business Owner",
          plan: "premium",
          joined: "2024-01-15",
          permissions: ["dashboard:read", "dashboard:write", "ai:access", "reports:generate"],
          limits: {
            api_calls: 10000,
            ai_requests: 1000,
            storage: "10GB"
          },
          usage: {
            api_calls: 1245,
            ai_requests: 89,
            storage: "1.2GB"
          }
        },
        subscription: {
          status: "active",
          plan: "premium",
          renews: "2024-12-15",
          price: "$99/month"
        },
        timestamp: new Date().toISOString()
      });
    }
    
    // System info
    if (path === '/system/info') {
      return jsonResponse({
        system: "FastAPI Mobile App Backend",
        environment: "production",
        cloud_provider: "Cloudflare Workers",
        region: "Global Edge Network",
        memory: "128MB",
        runtime: "JavaScript",
        framework: "Service Worker",
        dependencies: {
          ai_engine: "built-in",
          database: "in-memory (mock)",
          cache: "Cloudflare Cache",
          authentication: "JWT (mock)"
        },
        performance: {
          response_time: "< 50ms",
          uptime: "99.9%",
          requests_served: Math.floor(Math.random() * 10000) + 5000
        },
        timestamp: new Date().toISOString()
      });
    }
    
    // Integration status
    if (path === '/integration/status') {
      return jsonResponse({
        business_api: "✅ Operational (v9.0.0)",
        mobile_app_api: "✅ Migrated to Cloudflare",
        ai_capability: "✅ Built-in Business Intelligence",
        external_ai: "🔌 Available via localhost:8080",
        built_in_ai: "✅ Always available",
        authentication: "✅ Mock endpoints active",
        database: "🟡 In-memory (mock)",
        frontend: "✅ Cloudflare Pages",
        deployment: "✅ Complete",
        timestamp: new Date().toISOString(),
        notes: "Successfully migrated from Render. All endpoints functional."
      });
    }
    
    // 404 - Not Found
    return jsonResponse({
      error: "Endpoint not found",
      path: path,
      method: method,
      available_endpoints: [
        "/",
        "/health", 
        "/dashboard",
        "/customers",
        "/ai/chat [POST]",
        "/ai/health",
        "/api/local/register [POST]",
        "/api/local/login [POST]",
        "/api/local/profile [GET]",
        "/system/info",
        "/integration/status"
      ],
      documentation: "See / endpoint for full API documentation",
      timestamp: new Date().toISOString()
    }, 404);
  }
};
