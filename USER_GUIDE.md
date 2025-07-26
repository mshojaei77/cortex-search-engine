# Personal SearXNG Meta-Search Engine

A robust, production-ready Python implementation for searching "AI news 2025" using your own private SearXNG meta-search engine.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+ ✅ (You have Python 3.12.6)
- Docker Desktop ✅ (You have Docker 24.0.6)
- UV package manager ✅ (You have UV 0.6.6)

### 2. Setup & Run

```powershell
# 1. Clone or navigate to project directory
cd personal-search-engine

# 2. Create virtual environment and install dependencies
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt

# 3. Start SearXNG meta-search engine
docker-compose up -d

# 4. Wait 30-60 seconds for SearXNG to initialize, then test
python search_engine.py
```

## 📋 What's Included

### Core Files
- `docker-compose.yml` - SearXNG and Redis services
- `searxng/settings.yml` - SearXNG configuration with JSON API enabled
- `search_engine.py` - Main Python client with OOP design
- `run_search.py` - Simple script for AI news search
- `setup.py` - Automated setup and testing script
- `requirements.txt` - Python dependencies

### Key Features
- **Privacy-focused**: Your own private search engine
- **Meta-search**: Aggregates results from multiple engines (Google, Bing, DuckDuckGo, etc.)
- **Production-ready**: Robust error handling, logging, and validation
- **OOP Design**: Follows SOLID principles with clean architecture
- **Configurable**: Environment variables and flexible parameters

## 🔍 Usage Examples

### Search AI News 2025
```python
from search_engine import SearchEngineManager

manager = SearchEngineManager()
results = manager.search_ai_news("2025", max_results=10)
for result in results:
    print(f"📰 {result['title']}")
    print(f"🔗 {result['url']}")
    print(f"📝 {result['snippet']}")
    print("-" * 60)
```

### Advanced Search
```python
from search_engine import SearchConfig, SearXNGClient

config = SearchConfig(
    base_url="http://localhost:8888",
    engines=['google', 'bing', 'duckduckgo'],
    max_results=20,
    time_range='month'
)

with SearXNGClient(config) as client:
    response = client.search("artificial intelligence breakthroughs 2025")
    print(f"Found {response.total_results} results in {response.search_time:.2f}s")
```

## 🐳 Docker Management

```powershell
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs searxng

# Stop services
docker-compose down

# Update images
docker-compose pull
docker-compose up -d
```

## 🌐 Web Interface

Once running, access SearXNG web interface at: **http://localhost:8888**

## 🔧 Configuration

### Environment Variables (.env)
```bash
SEARXNG_URL=http://localhost:8888
SEARXNG_TIMEOUT=30
SEARXNG_MAX_RESULTS=10
SEARXNG_LANGUAGE=en
```

### SearXNG Settings (searxng/settings.yml)
- JSON API enabled for programmatic access
- Multiple search engines configured
- Privacy-focused default settings
- Redis caching for improved performance

## 📊 Testing

### Automated Setup & Test
```powershell
python setup.py
```

### Manual Health Check
```python
from search_engine import SearchEngineManager

manager = SearchEngineManager()
with manager.create_client() as client:
    health = client.get_health_status()
    print(health)
```

### Quick AI News Search
```powershell
python run_search.py
```

## 🛠️ Troubleshooting

### SearXNG Not Starting
1. Check if port 8888 is available: `netstat -an | findstr :8888`
2. View Docker logs: `docker-compose logs searxng`
3. Restart services: `docker-compose restart`

### Connection Errors
1. Verify SearXNG is running: `docker-compose ps`
2. Test web interface: http://localhost:8888
3. Check firewall/antivirus blocking connections

### No Search Results
1. Confirm JSON format is enabled in settings.yml
2. Check if search engines are responding: `docker-compose logs searxng`
3. Try different search terms

### Python Import Errors
1. Activate virtual environment: `.venv\Scripts\activate`
2. Reinstall dependencies: `uv pip install -r requirements.txt`
3. Check Python version: `python --version`

## 🏗️ Architecture

### Components
- **SearXNG**: Meta-search engine (Docker container)
- **Redis**: Caching layer (Docker container)
- **Python Client**: OOP interface with Pydantic models
- **Search Manager**: High-level abstraction for common tasks

### Design Principles
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible without modification
- **Dependency Inversion**: Depends on abstractions, not concretions
- **Interface Segregation**: Small, focused interfaces
- **Liskov Substitution**: Proper inheritance hierarchy

## 🔐 Privacy & Security

- **No Tracking**: SearXNG anonymizes all requests
- **Local Hosting**: Your data never leaves your machine
- **No Logs**: Search queries are not stored
- **Rate Limiting**: Built-in protection against abuse

## 📈 Performance

- **Caching**: Redis caches search results for faster responses
- **Concurrent Requests**: Multiple search engines queried simultaneously  
- **Timeout Handling**: Graceful handling of slow responses
- **Resource Limits**: Docker container limits prevent system overload

## 🔄 Updates

```powershell
# Update SearXNG
docker-compose pull searxng/searxng:latest
docker-compose up -d

# Update Python dependencies
uv pip install -r requirements.txt --upgrade
```

---

**🎉 Enjoy your private, AI-focused meta-search engine!**

For issues or questions, check the troubleshooting section above or review the Docker logs. 