#!/usr/bin/env python3
"""
Setup script for Personal Search Engine with SearXNG

This script helps with the initial setup and deployment of the search engine.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path


def run_command(command, description, check=True):
    """Run a shell command with description."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False


def check_docker():
    """Check if Docker is installed and running."""
    print("🐳 Checking Docker installation...")
    
    # Check if docker command exists
    if not run_command("docker --version", "Checking Docker installation", check=False):
        print("❌ Docker is not installed or not accessible")
        print("   Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/")
        return False
    
    # Check if Docker daemon is running
    if not run_command("docker info", "Checking Docker daemon", check=False):
        print("❌ Docker daemon is not running")
        print("   Please start Docker Desktop")
        return False
    
    print("✅ Docker is ready")
    return True


def setup_environment():
    """Set up the Python environment."""
    print("🐍 Setting up Python environment...")
    
    # Check if uv is available
    uv_available = run_command("uv --version", "Checking UV package manager", check=False)
    
    if uv_available:
        print("📦 Using UV for package management...")
        success = run_command("uv pip install -r requirements.txt", "Installing dependencies with UV")
    else:
        print("📦 UV not found, using pip...")
        success = run_command("pip install -r requirements.txt", "Installing dependencies with pip")
    
    return success


def start_searxng():
    """Start SearXNG using Docker Compose."""
    print("🚀 Starting SearXNG with Docker Compose...")
    
    # Pull latest images
    run_command("docker-compose pull", "Pulling latest Docker images")
    
    # Start services
    if run_command("docker-compose up -d", "Starting SearXNG services"):
        print("✅ SearXNG services started successfully")
        return True
    else:
        print("❌ Failed to start SearXNG services")
        return False


def wait_for_searxng():
    """Wait for SearXNG to be ready."""
    print("⏳ Waiting for SearXNG to be ready...")
    
    url = "http://localhost:8888/config"
    max_attempts = 30
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ SearXNG is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ SearXNG failed to start within timeout")
    return False


def test_search():
    """Test the search functionality."""
    print("🧪 Testing search functionality...")
    
    try:
        # Import and test our search engine
        from search_engine import SearchEngineManager
        
        manager = SearchEngineManager()
        
        # Test health check
        with manager.create_client() as client:
            health = client.get_health_status()
            if health['status'] != 'healthy':
                print(f"❌ Health check failed: {health.get('error', 'Unknown error')}")
                return False
        
        # Test AI news search
        print("   Testing AI news search...")
        results = manager.search_ai_news("2025", max_results=3)
        
        if results:
            print(f"✅ Search test successful! Found {len(results)} results")
            print(f"   Sample result: {results[0]['title'][:50]}...")
        else:
            print("⚠️  Search completed but no results found")
        
        return True
        
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False


def show_status():
    """Show the status of all services."""
    print("📊 Service Status:")
    run_command("docker-compose ps", "Checking container status")


def main():
    """Main setup function."""
    print("🔍 Personal Search Engine Setup")
    print("===============================")
    print()
    
    # Check prerequisites
    if not check_docker():
        sys.exit(1)
    
    print()
    
    # Set up Python environment
    if not setup_environment():
        print("❌ Failed to set up Python environment")
        sys.exit(1)
    
    print()
    
    # Start SearXNG
    if not start_searxng():
        sys.exit(1)
    
    print()
    
    # Wait for SearXNG to be ready
    if not wait_for_searxng():
        print("❌ SearXNG setup failed")
        print("\n🔧 Troubleshooting:")
        print("   1. Check Docker logs: docker-compose logs searxng")
        print("   2. Ensure ports 8888 is not in use")
        print("   3. Try restarting: docker-compose restart")
        sys.exit(1)
    
    print()
    
    # Test search functionality
    if test_search():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   • Web interface: http://localhost:8888")
        print("   • Run search script: python search_engine.py")
        print("   • View logs: docker-compose logs -f")
        print("   • Stop services: docker-compose down")
        print("\n💡 The search engine is now ready to use!")
    else:
        print("\n⚠️  Setup completed but search test failed")
        print("   Please check the logs and configuration")
    
    print()
    show_status()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1) 