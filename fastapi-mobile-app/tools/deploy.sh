#!/bin/bash
# Complete Deployment Script for FastAPI App

echo "🚀 Starting deployment for humbu.store..."

# Step 1: Build the Docker images
echo "📦 Building Docker images..."
docker-compose build

# Step 2: Setup SSL certificates
echo "🔐 Setting up SSL certificates..."
./setup-ssl.sh

# Step 3: Start all services
echo "🌐 Starting services..."
docker-compose up -d

# Step 4: Check status
echo "✅ Deployment complete!"
echo "📊 Checking services..."
docker-compose ps

echo ""
echo "🎉 Your FastAPI app is now live at:"
echo "   🔗 https://humbu.store"
echo "   🔗 https://www.humbu.store (redirects to main domain)"
echo ""
echo "📱 Mobile PWA ready with HTTPS!"
