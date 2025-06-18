#!/usr/bin/env python3
"""
Deployment script for Motivation Bot
This script helps set up the application for first-time users.
"""

import os
import json
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_config():
    """Set up configuration file"""
    print("\n⚙️  Setting up configuration...")
    
    if os.path.exists("config.json"):
        print("✅ config.json already exists")
        return True
    
    print("Please enter your Instagram credentials:")
    username = input("Instagram Username: ").strip()
    password = input("Instagram Password: ").strip()
    
    if not username or not password:
        print("❌ Username and password are required")
        return False
    
    config = {
        "instagram": {
            "username": username,
            "password": password
        }
    }
    
    try:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ["generated_videos", "music", "uploads", "templates"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/")
        else:
            print(f"✅ {directory}/ already exists")

def download_nltk_data():
    """Download required NLTK data"""
    print("\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False

def check_ollama():
    """Check if Ollama is available"""
    print("\n🤖 Checking Ollama availability...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("⚠️  Ollama is running but may not have the required model")
            return False
    except requests.exceptions.RequestException:
        print("⚠️  Ollama is not running. You'll need to install and run Ollama for AI quote generation.")
        print("   Visit: https://ollama.ai/")
        return False

def main():
    """Main deployment function"""
    print("🚀 Motivation Bot Deployment Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Download NLTK data
    download_nltk_data()
    
    # Check Ollama
    check_ollama()
    
    # Setup configuration
    if not setup_config():
        print("\n⚠️  You can manually create config.json later")
    
    print("\n🎉 Deployment completed successfully!")
    print("\nNext steps:")
    print("1. Make sure Ollama is running with the llama3 model")
    print("2. Run: python app.py")
    print("3. Open your browser to: http://localhost:5000")
    print("\nFor help, see the README.md file")

if __name__ == "__main__":
    main() 