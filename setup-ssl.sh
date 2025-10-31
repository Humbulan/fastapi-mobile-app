#!/bin/bash
# SSL Setup Script for humbu.store

echo "🚀 Setting up SSL certificates for humbu.store..."

# Create letsencrypt directory
mkdir -p letsencrypt

# Get SSL certificates from Let's Encrypt
docker run -it --rm \
    -p 80:80 \
    -v $(pwd)/letsencrypt:/etc/letsencrypt \
    certbot/certbot certonly --standalone \
    -d humbu.store -d www.humbu.store \
    --email humbulani@humbu.store --agree-tos --non-interactive

echo "✅ SSL certificates obtained successfully!"
echo "📁 Certificates stored in: ./letsencrypt/live/humbu.store/"
echo "🔐 Your site will now serve over HTTPS!"
