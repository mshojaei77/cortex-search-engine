# Developer Guide

This guide provides detailed information for developers and advanced users who want to customize, contribute to, or troubleshoot the Personal Search Engine. For a quick start, see the main [README.md](./README.md).

---

## Installation: The Complete Setup Guide

Before you start, make sure you have these three things:

- **Docker Desktop**: Download from [docker.com](https://www.docker.com/products/docker-desktop/). Launch it after installation.
- **Python 3.8+**: Check your version with `python --version` or `python3 --version`
- **OpenAI API Key**: Grab one from [platform.openai.com](https://platform.openai.com/signup)

Run these quick verification commands:
```bash
# Verify Docker is running
docker --version
docker info  # Should show system info, not errors

# Verify Python version
python --version  # Should show 3.8 or higher
```

### Step-by-Step Setup

#### 1. Clone and Navigate

```bash
git clone https://github.com/your-username/personal-search-engine.git
cd personal-search-engine
```

#### 2. Set Up Your Environment

**Create a virtual environment (highly recommended):**
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# You should see (.venv) in your terminal prompt
```

**Configure your OpenAI API key:**
```bash
# Create .env file with your API key
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env

# Verify the file was created
cat .env  # Should display your key
```

#### 3. Run the Automated Setup Script

This script handles all the heavy lifting for you:

```bash
python setup.py
```

**What happens behind the scenes:**
- ✅ Verifies Docker is running
- 📦 Installs Python dependencies (uses `uv` for faster installation)
- 🐳 Pulls and starts Docker containers (SearXNG + Redis)
- ⏳ Waits for services to become ready
- 🧪 Tests the search functionality
- ✅ Confirms everything works properly

**Expected output:**
```bash
🔍 Personal Search Engine Setup
===============================

🐳 Checking Docker installation...
✅ Docker is ready

🐍 Setting up Python environment...
📦 Using UV for package management...
✅ Installing dependencies with UV completed successfully

🚀 Starting SearXNG with Docker Compose...
✅ SearXNG services started successfully

⏳ Waiting for SearXNG to be ready...
✅ SearXNG is ready!

🧪 Testing search functionality...
✅ Search test successful! Found 3 results

🎉 Setup completed successfully!

📋 Next steps:
   • Web interface: http://localhost:8888
   • Run the main assistant: python main.py
   • Run example script: python example.py
   • View logs: docker-compose logs -f
   • Stop services: docker-compose down

💡 The search engine is now ready to use!
✅ OpenAI API key detected

📊 Service Status:
       Name                     Command               State           Ports
searxng_redis     docker-entrypoint.sh redis ...   Up      6379/tcp
searxng           /sbin/tini -- /usr/local/s ...   Up      0.0.0.0:8888->8080/tcp
```

### 4. Validate Everything Works

Before diving in, run a quick health check:

```bash
python validate_setup.py
```

This checks all components and gives you a score. You should see:
```bash
🔍 Personal Search Engine - Setup Validation
==================================================

🔧 Checking Python Version...
✅ Python 3.12.6 - Good!

🔧 Checking Environment File...
✅ .env file with OpenAI key found

🔧 Checking Python Dependencies...
✅ All Python dependencies installed

🔧 Checking Docker Containers...
✅ Docker containers running

🔧 Checking SearXNG Service...
✅ SearXNG responding on http://localhost:8888

🔧 Checking OpenAI API Key...
✅ OpenAI API key working

==================================================
📊 VALIDATION SUMMARY
==================================================
✅ PASS Python Version
✅ PASS Environment File
✅ PASS Python Dependencies
✅ PASS Docker Containers
✅ PASS SearXNG Service
✅ PASS OpenAI API Key

Score: 6/6 checks passed

🎉 ALL CHECKS PASSED!
Your setup is ready. Run: python main.py
```

---

## Advanced Usage & Testing

### Library Usage

```python
from search_engine import SearchEngineManager, display_results

# Quick search
manager = SearchEngineManager()
results = manager.quick_search("python tips 2024", max_results=5)
display_results(results, title="Python Tips")

# Advanced usage
with manager.create_client() as client:
    response = client.search(
        query="rust vs go performance",
        engines=["google", "bing"],
        categories=["general"]
    )
    print(f"Found {len(response.results)} results")
```

### Test Your Setup

```bash
# Quick validation (recommended first step)
python validate_setup.py

# Run the example script
python example.py

# Check web interface
# Open browser to http://localhost:8888

# Check service status
docker-compose ps
```

---

## Troubleshooting Common Issues

### Setup Problems

**"Docker daemon not running"**
```bash
# Solution: Start Docker Desktop
# Windows/Mac: Launch Docker Desktop application
# Linux: sudo systemctl start docker
```

**"Port 8888 already in use"**
```bash
# Check what's using the port
lsof -i :8888  # macOS/Linux
netstat -ano | findstr :8888  # Windows

# Solution: Change the port in docker-compose.yml
# Edit "8888:8080" to "8889:8080", then restart:
docker-compose down && docker-compose up -d
```

**"OpenAI API key not found"**
```bash
# Check if .env file exists and has the correct format
cat .env
# Should display: OPENAI_API_KEY=sk-...

# If missing or incorrectly formatted:
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**"Python dependencies failed to install"**
```bash
# Try installing without uv
pip install -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
```

### Runtime Issues

**"Search test failed"**

I've been there. You see the error and your heart sinks a little. Don't worry, it's usually an easy fix.
```bash
# Check container logs for errors
docker-compose logs searxng
docker-compose logs redis

# Restart the containers
docker-compose restart

# Complete reset if needed
docker-compose down
docker-compose up -d
```

**"Assistant not responding"**
```bash
# Verify OpenAI API key is working
python test_openai.py

# Test network connectivity to SearXNG. Is it reachable?
curl -s http://localhost:8888/config
```

**"Permission denied errors"**
```bash
# On Linux/Mac, fix file permissions
sudo chown -R $USER:$USER .
```

### Performance Issues

**"Slow responses"**
- Switch to `gpt-4o-mini` instead of `gpt-4` for faster, cheaper responses
- Check your internet connection speed
- Monitor OpenAI usage at platform.openai.com

**"High API costs"**
- Use the `gpt-4o-mini` model (significantly cheaper)
- Reduce `max_results` in search configurations
- Track usage in your OpenAI dashboard

---

## Configuration & Customization

### Environment Variables

Create `.env.example` for reference:
```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (with defaults)
SEARXNG_URL=http://localhost:8888
SEARXNG_TIMEOUT=30
MAX_SEARCH_RESULTS=10
```

### SearXNG Configuration

Edit `searxng/settings.yml` to:
- Add/remove search engines
- Change result limits
- Modify timeout settings
- Customize appearance

### Docker Configuration

Edit `docker-compose.yml` to:
- Change ports (if 8888 conflicts)
- Adjust memory limits
- Add volume mounts
- Configure networking

---

## Performance & Costs

**Typical Response Times:**
- Search aggregation: 1-3 seconds
- AI synthesis: 2-5 seconds
- End-to-end: 3-8 seconds per query

**OpenAI API Costs (2024 pricing):**
- `gpt-4o-mini`: ~$0.0008 per query
- `gpt-4-turbo`: ~$0.003 per query
- Mini model delivers 1000+ queries per dollar

**System Resource Usage:**
- RAM: ~200MB (Docker containers + Python app)
- Storage: ~500MB (Docker images)
- CPU: Minimal when idle, brief spikes during queries

---

## Advanced Usage

### Custom Tools

Extend the agent with new capabilities:

```python
# Add to main.py
def calculator_tool(expression: str) -> float:
    """Simple calculator tool."""
    return eval(expression)  # Don't do this in production!

# Register with OpenAI function calling
```

### Alternative Models

Swap OpenAI for local models:

```python
# Use Ollama for local inference
from ollama import Client
client = Client(host='http://localhost:11434')
```

### Batch Processing

Process multiple queries:

```python
queries = ["question 1", "question 2", "question 3"]
for query in queries:
    result = run_agent(query)
    print(f"Q: {query}\nA: {result}\n")
```

---

## Contributing

Found a bug or want to add a feature? Let's build this together!

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feat/awesome-feature`
3. **Write** your code
4. **Test** everything with `python setup.py`
5. **Commit** using conventional format: `git commit -m "feat: add awesome feature"`
6. **Push** and create a pull request

**Development environment setup:**
```bash
# Install development dependencies
pip install pytest black isort mypy

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy .
```

---

## Sources & References

- **SearXNG**: [searxng.github.io](https://searxng.github.io) - Privacy-focused meta-search engine
- **OpenAI**: [platform.openai.com](https://platform.openai.com/) - AI API platform  
- **Docker**: [docker.com](https://docker.com) - Containerization platform
- **Python**: [python.org](https://python.org) - Programming language 