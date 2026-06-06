#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Setting up Imperial Intelligence - AI Gateway"
echo "=================================================="

# Load the AI Gateway key
source ~/.ngrok_creds 2>/dev/null || {
    echo "❌ ngrok credentials not found"
    exit 1
}

# Create Node-RED configuration
mkdir -p ~/.node-red

cat > ~/.node-red/ai_gateway_config.js << EOF
// Imperial Intelligence - AI Gateway Configuration
// Loaded automatically by Node-RED

module.exports = {
    apiKey: process.env.NGROK_AI_GATEWAY_KEY || '$NGROK_AI_GATEWAY_KEY',
    gatewayUrl: 'https://your-gateway.ngrok.app',
    defaultModel: 'gpt-4o',
    fallbackModel: 'claude-3',
    audit: true,
    beiraCorridor: {
        enabled: true,
        weightTolerance: 5.0, // 5% tolerance for cargo weight
        documentCheck: true
    }
};
