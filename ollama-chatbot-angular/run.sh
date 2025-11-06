#!/bin/bash

# Ollama Chatbot Angular - Run Script

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Dependencies not installed!"
    echo "Please run ./install.sh first"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Warning: Cannot connect to Ollama at http://localhost:11434"
    echo "Please make sure Ollama is running:"
    echo "  ollama serve"
    echo ""
    echo "Continuing anyway..."
    echo ""
fi

# Start the development server
echo "🚀 Starting Ollama Chatbot Angular..."
echo "📱 Opening at http://localhost:4200"
echo ""
npm start
