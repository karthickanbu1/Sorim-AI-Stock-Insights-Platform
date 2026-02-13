#!/bin/bash

# RealTicker Frontend Startup Script

echo "🚀 Starting RealTicker Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
fi

# Start the development server
echo "✅ Starting React development server..."
npm start
