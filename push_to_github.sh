#!/bin/bash
# Push Mirage V3 to GitHub

echo "🚀 Pushing Mirage V3 to GitHub..."

# Configure git
git config user.name "Insider77Circle"
git config user.email "insider77circle@example.com"

# Add remote repository
git remote add origin https://github.com/Insider77Circle/mirage-v3.git

# Commit changes
git commit -m "Initial commit: Mirage V3 Cyberpunk Edition - AI-Powered Cyber Range & Honeypot Simulator"

# Push to main branch
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo "🌐 Repository: https://github.com/Insider77Circle/mirage-v3"
