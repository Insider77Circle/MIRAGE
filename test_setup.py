#!/usr/bin/env python3
"""
Mirage V3 Setup Test Script
Tests basic functionality without requiring sudo privileges
"""

import os
import sys
import asyncio
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, trying to load manually...")
    # Try to load .env file manually
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"\'')
        print("✅ Loaded environment variables manually")
    except FileNotFoundError:
        print("❌ .env file not found")

# Test environment setup
print("🔍 Mirage V3 Setup Test")
print("=" * 50)

# Test 1: Environment Variables
print("\n1. Testing Environment Variables...")
api_key = os.getenv("LLM_API_KEY", "")
if api_key and api_key != "YOUR_KIMI_API_KEY_HERE":
    print(f"✅ LLM_API_KEY found: {api_key[:20]}...")
else:
    print("❌ LLM_API_KEY not found or not configured")
    print("   Make sure your .env file contains: LLM_API_KEY=your_key_here")

# Test 2: Import Dependencies
print("\n2. Testing Dependencies...")
try:
    from openai import AsyncOpenAI
    print("✅ openai library imported successfully")
except ImportError as e:
    print(f"❌ openai library not found: {e}")
    print("   Run: pip install openai")

try:
    from faker import Faker
    print("✅ faker library imported successfully")
except ImportError as e:
    print(f"❌ faker library not found: {e}")
    print("   Run: pip install faker")

try:
    import pandas as pd
    print("✅ pandas library imported successfully")
except ImportError as e:
    print(f"❌ pandas library not found: {e}")
    print("   Run: pip install pandas")

try:
    from docx import Document
    print("✅ python-docx library imported successfully")
except ImportError as e:
    print(f"❌ python-docx library not found: {e}")
    print("   Run: pip install python-docx")

try:
    from rich.console import Console
    print("✅ rich library imported successfully")
except ImportError as e:
    print(f"❌ rich library not found: {e}")
    print("   Run: pip install rich")

# Test 3: AI Client Initialization
print("\n3. Testing AI Client...")
try:
    if api_key and api_key != "YOUR_KIMI_API_KEY_HERE":
        client = AsyncOpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        print("✅ AI client initialized successfully")
    else:
        print("⚠️  Skipping AI client test (no API key configured)")
except Exception as e:
    print(f"❌ AI client initialization failed: {e}")

# Test 4: File System Setup
print("\n4. Testing File System...")
try:
    os.makedirs("mirage_assets", exist_ok=True)
    print("✅ Assets directory created/accessible")
except Exception as e:
    print(f"❌ Assets directory creation failed: {e}")

# Test 5: Basic Import Test
print("\n5. Testing Main Script Import...")
try:
    # Add current directory to path
    sys.path.insert(0, '.')
    
    # Test basic imports from main script
    from mirage_v3_cyberpunk import WORLD_CONTEXT, system_status, log_buffer
    print("✅ Main script components imported successfully")
    print(f"   Hostname: {WORLD_CONTEXT['network']['hostname']}")
    print(f"   Initial CPU: {system_status['cpu']}%")
    print(f"   Log buffer size: {len(log_buffer)}")
except Exception as e:
    print(f"❌ Main script import failed: {e}")

# Test 6: Configuration Validation
print("\n6. Testing Configuration...")
config_issues = []

# Check ports
try:
    from mirage_v3_cyberpunk import ACTIVE_PORTS
    print(f"✅ Active ports configured: {ACTIVE_PORTS}")
except Exception as e:
    config_issues.append(f"Active ports: {e}")

# Check difficulty
try:
    from mirage_v3_cyberpunk import DIFFICULTY
    print(f"✅ Difficulty level: {DIFFICULTY}")
except Exception as e:
    config_issues.append(f"Difficulty: {e}")

# Check model
try:
    from mirage_v3_cyberpunk import MODEL_NAME
    print(f"✅ AI model: {MODEL_NAME}")
except Exception as e:
    config_issues.append(f"Model: {e}")

if config_issues:
    print("❌ Configuration issues found:")
    for issue in config_issues:
        print(f"   - {issue}")
else:
    print("✅ All configuration tests passed")

# Summary
print("\n" + "=" * 50)
print("📊 Test Summary")
print("=" * 50)

if api_key and api_key != "YOUR_KIMI_API_KEY_HERE":
    print("🎯 Ready to run: sudo python3 mirage_v3_cyberpunk.py")
    print("   Note: sudo required for privileged ports (22, 80, 443)")
else:
    print("⚠️  Setup incomplete: Configure your LLM_API_KEY in .env file")
    print("   1. Copy .env.example to .env")
    print("   2. Add your Kimi API key: LLM_API_KEY=your_key_here")

print("\n🌐 Web Interface: Open index.html in your browser")
print("🔧 For help: See README.md for detailed instructions")
