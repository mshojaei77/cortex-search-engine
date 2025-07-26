#!/usr/bin/env python3
"""
Quick validation script to check if your Personal Search Engine setup is working.
Run this after setup.py to verify everything is configured correctly.
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Good!")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_env_file():
    """Check if .env file exists and has OpenAI key."""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Create it: echo 'OPENAI_API_KEY=sk-your-key-here' > .env")
        return False
    
    content = env_path.read_text()
    if "OPENAI_API_KEY=" in content and "sk-" in content:
        print("✅ .env file with OpenAI key found")
        return True
    else:
        print("❌ .env file missing valid OpenAI key")
        print("   Add your key: echo 'OPENAI_API_KEY=sk-your-key-here' > .env")
        return False

def check_dependencies():
    """Check if required Python packages are installed."""
    required = ["openai", "requests", "dotenv"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("   Install: pip install -r requirements.txt")
        return False
    else:
        print("✅ All Python dependencies installed")
        return True

def check_docker():
    """Check if Docker containers are running."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"],
            capture_output=True, text=True, check=True
        )
        
        if "searxng" in result.stdout and "searxng_redis" in result.stdout:
            print("✅ Docker containers running")
            return True
        else:
            print("❌ Docker containers not running")
            print("   Start them: docker-compose up -d")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker not available or containers not running")
        print("   Start containers: docker-compose up -d")
        return False

def check_searxng():
    """Check if SearXNG is responding."""
    try:
        response = requests.get("http://localhost:8888/config", timeout=5)
        if response.status_code == 200:
            print("✅ SearXNG responding on http://localhost:8888")
            return True
        else:
            print(f"❌ SearXNG returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ SearXNG not responding: {e}")
        print("   Check: docker-compose logs searxng")
        return False

def check_openai_key():
    """Test OpenAI API key."""
    try:
        from dotenv import load_dotenv
        from openai import OpenAI
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False
            
        client = OpenAI(api_key=api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        
        print("✅ OpenAI API key working")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API key test failed: {e}")
        print("   Check your key at: https://platform.openai.com/api-keys")
        return False

def main():
    """Run all validation checks."""
    print("🔍 Personal Search Engine - Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python),
        ("Environment File", check_env_file),
        ("Python Dependencies", check_dependencies),
        ("Docker Containers", check_docker),
        ("SearXNG Service", check_searxng),
        ("OpenAI API Key", check_openai_key),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔧 Checking {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, _) in enumerate(checks):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\nScore: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED!")
        print("Your setup is ready. Run: python main.py")
    else:
        print(f"\n⚠️  {total - passed} issues found. Please fix them before proceeding.")
        print("\nCommon fixes:")
        print("• Install dependencies: pip install -r requirements.txt")
        print("• Start containers: docker-compose up -d")
        print("• Check .env file: cat .env")
        print("• Run full setup: python setup.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 