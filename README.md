# Personal Search Engine

A privacy-focused, conversational AI-powered search engine that combines SearXNG with AI to deliver intelligent, synthesized results - no search engine API keys required.

Building specialized AI agents for different purposes? That's exactly what this is for. Academic research, social media monitoring, financial analysis, coding assistance—you name it.

*Forget the corporate trackers. Let's make searching fun again.*

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Background & Rationale

Here's the deal: I'm merging two powerful concepts—a private search proxy and a large language model. The result? A local, conversational search agent that cuts through SEO garbage and ad-trackers. It lives in your terminal, where real work happens.

Standard web search is broken for developers. The signal-to-noise ratio is plummeting. You're fighting blog spam, outdated answers, and content farms. My goals are simple: privacy (no query logging) and efficiency (synthesized answers, not endless link lists).

This setup aggregates results from multiple engines via self-hosted SearXNG, then feeds clean data to OpenAI for smart synthesis. You get direct answers, CLI-style, without leaving your command line or dodging sponsored junk.

It's not a new search engine - it's a better client for the web we already have.

---

## See It in Action

Picture this: You're in your terminal, the cursor blinking patiently. Your coffee's gone cold, but you're in the zone. You fire up the app, ask a question, and boom - this is what you get. (This is a real example, but web results can be a fickle beast).

```md
Web Search Assistant (type 'exit' to quit)
> What are the latest developments in nuclear fusion energy as of late 2025?

Assistant: As of late 2025, here are some notable developments in nuclear fusion energy:

1. **Commercial Fusion Plant Advances**: Google has entered into an investment and offtake agreement with Commonwealth Fusion Systems for 200 MW of power from its first ARC commercial fusion plant. This represents a significant step towards commercialization of fusion energy.

2. **Breakthrough Results**: There have been record-breaking results related to fusion power, with innovations in compact tokamak designs aimed at producing substantial electricity output, like the proposed ARC reactor, which is designed to produce up to 400 megawatts of electricity.

For more detailed information, you may refer to the articles [here](https://www.world-nuclear-news.org/articles/google-backs-fusion-power) and [here](https://www.scientificamerican.com/article/record-breaking-results-bring-fusion-power-closer-to-reality/).

These developments reflect a growing momentum in the field of nuclear fusion, with significant investments and technological advancements that may lead to practical applications in the near future.

> intresting tell me more about the Google investment

Assistant: Recently, Google (Alphabet Inc.) has made a significant investment in the artificial intelligence startup Anthropic, agreeing to invest up to $2 billion. This move intensifies competition in the AI sector, where both Google and Anthropic are vying for leadership. 

- **Details of the Investment**: On October 31, 2023, it was reported that Google had initiated a $500 million upfront investment in Anthropic, with plans to commit further funding later. This agreement underscores Google's commitment to advancing its own AI capabilities, particularly as it seeks to compete with other major players like OpenAI.

- **Background on Anthropic**: Anthropic is known for its development of AI systems and has positioned itself as a serious contender in the AI landscape, competing directly with OpenAI. Google’s investment is likely aimed at enhancing its own AI technologies and expanding its influence in the evolving market.

This partnership indicates a strategic shift in how tech giants are prioritizing AI development and the race to dominate the next generation of AI technologies. 

For more details, you can read the articles [here](https://www.forbes.com/sites/qai/2023/10/31/google-invests-in-anthropic-for-2-billion-as-ai-race-heats-up/) or [here](https://www.reuters.com/technology/google-agrees-invest-up-2-bln-openai-rival-anthropic-wsj-2023-10-27/).
```

That's it! Real answers, no tracking, all from your own setup. Want to try it yourself?

---

## Quick Start: The 60-Second Install

> **TL;DR:** Got Docker, Python 3.8+, and an OpenAI key? You're ready. This clones, configures, and launches in minutes.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/personal-search-engine.git
cd personal-search-engine

# 2. Configure your API key securely (add .env to .gitignore!)
echo "OPENAI_API_KEY=sk-YOUR_API_KEY_HERE" > .env

# 3. Setup and run
python setup.py && python main.py
```

**Running into issues?** Run this health check:
```bash
python validate_setup.py
```

*Still having trouble? Check the detailed troubleshooting below.*

---

## Why Build This? Features That Actually Matter

Why go DIY? Simple. You get privacy and intelligence without the usual compromises.

- 🕵️‍♂️ **True Privacy**: Your queries stay local. No more fueling the ad-tech machine with your late-night debugging sessions.
- 🤖 **AI That Understands Context**: It synthesizes answers, not just link dumps. Think of it as a smart research assistant that's always on call.
- 💬 **Terminal-Native**: A pure CLI workflow for developers who live in the command line.
- 🐳 **Docker-Powered**: Containers handle all the messy setup. Just run and go.
- 🐍 **Python-Based**: The code is clean, modular, and easy to hack on. Go ahead, make it your own.
- ⚙️ **Fully Customizable**: Tweak search engines, AI models, and behaviors through simple config files.

Bonus: you're building an ethical, surveillance-free alternative to mainstream search. How cool is that?

---

## How It Works: Under the Hood

No black boxes here. The architecture is straightforward and easy to debug. SearXNG aggregates search results anonymously, and then OpenAI synthesizes them into a coherent answer.

```mermaid
graph TD
    User[👨‍💻 You, the Terminal Wizard] --> PythonApp[🐍 The App (main.py)]
    subgraph "Your Python Realm"
        PythonApp -- "Hey, what's up with...?" --> OpenAI_Agent[🤖 OpenAI Agent]
        OpenAI_Agent -- "Hmm, need fresh web intel" --> SearchManager[🔍 SearchEngineManager]
        SearchManager -- "Query time!" --> SearXNG_Client[🔌 SearXNGClient]
    end
    SearXNG_Client -- "HTTP magic" --> SearXNG_Service[🐳 SearXNG Docker Container]
    subgraph "Docker Land (docker-compose.yml)"
        SearXNG_Service -- "Cache me if you can" --> Redis_Service[📦 Redis Cache]
    end
    SearXNG_Service -- "Fetching from the wild web" --> Internet[🌐 Real Search Engines (Google, Bing, etc.)]
    Internet -- "Raw results" --> SearXNG_Service
    SearXNG_Service -- "Clean JSON" --> SearXNG_Client
    SearXNG_Client -- "Parsed goodies" --> SearchManager
    SearchManager -- "Refined info" --> OpenAI_Agent
    OpenAI_Agent -- "Brainstorm with OpenAI API" --> OpenAI_API[☁️ OpenAI Cloud]
    OpenAI_API -- "Wit and wisdom" --> OpenAI_Agent
    OpenAI_Agent -- "Here's the deets" --> PythonApp
    PythonApp -- "Terminal output" --> User
```

Here's the step-by-step flow:
1. It all starts with your question in the CLI.
2. The AI agent figures out if it needs to hit the web for fresh info.
3. If so, the search manager queries your local SearXNG instance.
4. SearXNG does the heavy lifting: aggregates results from multiple engines and caches them in Redis.
5. Clean results are fed back to the AI agent, which uses OpenAI to cook up a synthesized answer.

The modular design makes it easy to swap AI models or add new tools.

---

## Installation: The Complete Setup Guide

### Prerequisites Check

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

### 5. Fire It Up!

```bash
python main.py
```

You should see:
```bash
Web Search Assistant (type 'exit' to quit)
> 
```

Type a question and watch the magic happen!

---

## Usage Examples

### Basic Chat Mode

```bash
$ python main.py
> What's the difference between async and await in Python?
Assistant: [Detailed explanation with web sources]

> How do I fix Docker container permission errors?
Assistant: [Practical solutions with commands]

> exit
Exiting...
```

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

## License

MIT License - use, modify, and share freely. See `LICENSE` for complete details.

Built with ❤️ by developers, for developers. If this project saves you time or brings you joy, consider dropping a ⭐ on the repository!

---

## Sources & References

- **SearXNG**: [searxng.github.io](https://searxng.github.io) - Privacy-focused meta-search engine
- **OpenAI**: [platform.openai.com](https://platform.openai.com/) - AI API platform  
- **Docker**: [docker.com](https://docker.com) - Containerization platform
- **Python**: [python.org](https://python.org) - Programming language

---

## What's Next?

- [ ] **Streaming responses** for real-time conversation feel
- [ ] **Conversation memory** for intelligent follow-up questions  
- [ ] **Web interface** for users who prefer browsers over terminals
- [ ] **Local model support** (Ollama, LM Studio, etc.)
- [ ] **Plugin system** for custom search tools and integrations
- [ ] **Multi-language support** for global accessibility

Have ideas or suggestions? Open an issue or start a discussion! 