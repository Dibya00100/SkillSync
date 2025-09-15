#!/bin/bash

# SkillSync Installation Script
echo "🚀 SkillSync Installation Script"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Download spaCy model
echo "🧠 Downloading spaCy English model..."
python3 -m spacy download en_core_web_sm

if [ $? -eq 0 ]; then
    echo "✅ spaCy model downloaded successfully"
else
    echo "⚠️  spaCy model download failed. You may need to run: python3 -m spacy download en_core_web_sm"
fi

# Check if Node.js is installed for frontend
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
    
    # Install frontend dependencies
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    
    if [ $? -eq 0 ]; then
        echo "✅ Frontend dependencies installed successfully"
    else
        echo "❌ Failed to install frontend dependencies"
    fi
    cd ..
else
    echo "⚠️  Node.js not found. Frontend setup skipped."
    echo "   Install Node.js to run the frontend: https://nodejs.org/"
fi

# Run NLP setup
echo "🔧 Running NLP setup..."
python3 setup_nlp.py

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Start backend: cd backend && python3 app.py"
echo "2. Start frontend: cd frontend && npm start"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "💡 Note: First run may be slower as AI models are downloaded"
