#!/usr/bin/env python3
"""
Test script for Motivation Bot
This script tests all major components to ensure everything works correctly.
"""

import os
import sys
import json
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✅ PIL imported successfully")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        return False
    
    try:
        import nltk
        print("✅ NLTK imported successfully")
    except ImportError as e:
        print(f"❌ NLTK import failed: {e}")
        return False
    
    return True

def test_motivation_bot():
    """Test the motivation bot class"""
    print("\n🤖 Testing Motivation Bot...")
    
    try:
        from motivation_bot import MotivationBot, generate_quote_ollama
        print("✅ MotivationBot imported successfully")
        
        # Test bot initialization
        bot = MotivationBot()
        print("✅ MotivationBot initialized successfully")
        
        # Test CSV initialization
        if os.path.exists(bot.csv_file):
            print("✅ CSV file exists")
        else:
            print("⚠️  CSV file will be created on first run")
        
        return True
        
    except Exception as e:
        print(f"❌ MotivationBot test failed: {e}")
        return False

def test_web_app():
    """Test the Flask web application"""
    print("\n🌐 Testing Web Application...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test basic routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Main route works")
            else:
                print(f"❌ Main route failed: {response.status_code}")
                return False
            
            response = client.get('/bot_status')
            if response.status_code == 200:
                print("✅ Bot status route works")
            else:
                print(f"❌ Bot status route failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Web app test failed: {e}")
        return False

def test_config():
    """Test configuration setup"""
    print("\n⚙️  Testing Configuration...")
    
    # Check if config.json exists
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            if 'instagram' in config:
                username = config['instagram'].get('username')
                password = config['instagram'].get('password')
                
                if username and password:
                    print("✅ Instagram credentials configured")
                else:
                    print("⚠️  Instagram credentials incomplete")
            else:
                print("⚠️  Instagram section missing from config")
        except Exception as e:
            print(f"❌ Config file error: {e}")
    else:
        print("⚠️  config.json not found - create it with your Instagram credentials")
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\n📁 Testing Directories...")
    
    directories = ['generated_videos', 'music', 'uploads', 'templates']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}/ exists")
        else:
            print(f"⚠️  {directory}/ will be created on first run")
    
    return True

def test_ollama():
    """Test Ollama connection"""
    print("\n🤖 Testing Ollama Connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            print("✅ Ollama is running")
            
            # Check if llama3 model is available
            models = response.json().get('models', [])
            llama3_available = any('llama3' in model.get('name', '').lower() for model in models)
            
            if llama3_available:
                print("✅ llama3 model is available")
            else:
                print("⚠️  llama3 model not found - install it with: ollama pull llama3")
        else:
            print("⚠️  Ollama is running but may not have the required model")
            
    except requests.exceptions.RequestException:
        print("⚠️  Ollama is not running - install from https://ollama.ai/")
    
    return True

def main():
    """Run all tests"""
    print("🧪 Motivation Bot Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_motivation_bot,
        test_web_app,
        test_config,
        test_directories,
        test_ollama
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your motivation bot is ready to use.")
        print("\nNext steps:")
        print("1. Make sure Ollama is running with llama3 model")
        print("2. Configure your Instagram credentials in config.json")
        print("3. Run: python app.py")
        print("4. Open browser to: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 