#!/bin/bash

# Ollama Chatbot Angular - Installation Script

echo "🚀 Setting up Ollama Chatbot Angular..."

# Check if Node.js is installed
if ! command -v node &> /dev/null
then
    echo "❌ Node.js is not installed!"
    echo "Please install Node.js 18.x or higher from https://nodejs.org"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo "❌ npm is not installed!"
    exit 1
fi

echo "✅ npm version: $(npm --version)"

# Check if Angular CLI is installed globally
if ! command -v ng &> /dev/null
then
    echo "📦 Angular CLI not found. Installing globally..."
    npm install -g @angular/cli
fi

echo "✅ Angular CLI version: $(ng version --minimal)"

# Install dependencies
echo "📥 Installing project dependencies..."
npm install

echo ""
echo "✨ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Start Ollama: ollama serve"
echo "  2. Pull a model: ollama pull gemma3:1b"
echo "  3. Run the app: npm start"
echo "  4. Open browser: http://localhost:4200"
echo ""
