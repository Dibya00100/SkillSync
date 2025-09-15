#!/usr/bin/env python3
"""
NLP Setup Script for SkillSync
Installs required NLP models and dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 SkillSync NLP Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("❌ Failed to download spaCy model")
        print("💡 Try running: python -m spacy download en_core_web_sm")
    
    # Download NLTK data
    print("\n🔄 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded successfully")
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
    
    # Test imports
    print("\n🔄 Testing NLP imports...")
    try:
        import spacy
        import transformers
        import sentence_transformers
        import sklearn
        import nltk
        import textblob
        print("✅ All NLP libraries imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Some NLP features may not work properly")
    
    # Test spaCy model
    print("\n🔄 Testing spaCy model...")
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("This is a test sentence.")
        print("✅ spaCy model loaded successfully")
    except OSError:
        print("❌ spaCy model not found")
        print("💡 Run: python -m spacy download en_core_web_sm")
    except Exception as e:
        print(f"❌ spaCy test failed: {e}")
    
    # Test sentence transformer
    print("\n🔄 Testing sentence transformer...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(["This is a test"])
        print("✅ Sentence transformer loaded successfully")
    except Exception as e:
        print(f"❌ Sentence transformer test failed: {e}")
        print("💡 This may take some time on first run")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Start the backend: cd backend && python app.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Open http://localhost:3000 in your browser")
    print("\n💡 Note: First run may be slower as models are downloaded")

if __name__ == "__main__":
    main()
