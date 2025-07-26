# Personal Search Engine 🤖💬
Hey there, fellow code wrangler! Ever wished you had a search engine that's as private as your late-night coding sessions, as smart as your favorite AI sidekick, and runs right on your machine? Well, buckle up, because this is your personal conversational search beast, powered by SearXNG and OpenAI.

*Forget the corporate trackers. Let's make searching fun (and private) again.*

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 30-Second Demo: See It in Action

Picture this: You're hunkered down in your terminal, caffeinated beverage in hand, and you fire up the app. Here's what it looks like when you toss a timely question its way. (Pro tip: This is a real-ish example based on actual tech—your results might vary with the web's mood.)

```bash
$ python main.py
Web Search Assistant (type 'exit' to quit)
> What are the latest developments in nuclear fusion energy as of late 2024?

Assistant: Alright, let's geek out on some fusion goodness. I hit up the web for the freshest scoops, and here's the lowdown:

1. **WEST's Epic Plasma Run**: Over in France, the WEST tokamak (that's Tungsten Environment in Steady-state Tokamak for the uninitiated) just nailed a new record—sustaining high-power plasma for a solid 6 minutes. That's huge for figuring out how to keep these reactions going without everything melting down.

2. **JET's Energy High Score**: The Joint European Torus crew in the UK reconfirmed their beast mode with 59 megajoules of energy from a 5-second burst. But in 2024, fresh analysis showed even better efficiency, pushing us closer to that 'net gain' holy grail.

3. **AI to the Rescue**: DeepMind and pals are dropping AI bombs on plasma control. Their models predict disruptions in real-time, basically playing whack-a-mole with instabilities to keep reactors humming smoothly.

4. **Private Fusion Frenzy**: Startups like Commonwealth Fusion Systems are stacking cash (hundreds of millions) and aiming for demo reactors by mid-decade. They're using fancy high-temp superconductors to make smaller, cheaper tokamaks.

5. **Global Strategy Vibes**: The US Department of Energy dropped their Fusion Energy Strategy in 2024, laying out a roadmap to commercial fusion by the 2030s. Meanwhile, the IAEA's World Fusion Outlook is all about international collab for clean energy wins.

Fusion's still the ultimate long game—think decades, not days—but these breakthroughs are like leveling up in a boss fight. Unlimited clean power? We're getting there, one plasma pulse at a time.
```

Boom! Real answers, no creepy ads, all served up privately from your own setup. If that doesn't make you want to clone this repo, I don't know what will.

---

## Quick Start: The 60-Second Install

> **TL;DR:** Got Docker, Python 3.8+, and an OpenAI key? You're basically set. This one-liner clones, sets up your key, runs the magic setup script, and launches the agent. (Windows folks, swap those backslashes for forwards if needed—cross-platform life.)

```bash
# 1. Clone the repo (because why not?)
git clone https://github.com/your-username/personal-search-engine.git
cd personal-search-engine

# 2. Stash your API key safely
# This creates a .env file. Pro tip: Add it to .gitignore so you don't accidentally commit your secrets!
echo "OPENAI_API_KEY=sk-YOUR_API_KEY_HERE" > .env

# 3. Let 'er rip!
# This bad boy checks your setup, installs Python deps, fires up Docker containers, and gets everything humming.
python setup.py && python main.py
```

*Quick note: If setup.py throws a tantrum (maybe Docker's not running?), peek at the detailed install below. We've all been there.*

---

## Why Bother? (The Features That'll Make You Smirk)

Okay, real talk: In a world of ad-riddled search giants, why roll your own? Because this isn't just a search tool—it's your geeky side project that levels up your daily grind. Here's the scoop, served with a side of casual geekery:

- 🕵️‍♂️ **Privacy Mode: Activated**: Your queries stay on your machine. No Big Brother logging your "how to fix my code at 3AM" searches. SearXNG aggregates from real engines without the tracking cookies.

- 🤖 **AI That Actually Gets You**: Powered by OpenAI's models, this agent doesn't just spit links—it converses. Ask "Why is my Python script slow?" and it might search, synthesize, and suggest optimizations. Like having a smarter rubber duck.

- 💬 **Terminal Magic**: No bloated web apps here. It's all CLI, baby. Type, hit enter, get answers. Perfect for us keyboard warriors who live in the terminal.

- 🐳 **Docker Simplicity**: One `docker-compose up` and boom—SearXNG and Redis are running in containers. No messing with manual installs or config nightmares.

- 🐍 **Pythonic and Hackable**: The core is clean Python code. Want to add custom tools? Tweak the agent prompt? Dive into `search_engine/` and make it yours. We're talking SOLID principles, OOP goodness, and easy extensibility.

- ⚙️ **Tweak Fest**: Edit `searxng/settings.yml` to pick your search engines, set timeouts, or even theme it (if you go web mode later). It's your playground.

Bonus: It's lightweight, self-hosted, and scales with your curiosity. Ever wanted to build an AI that searches the web ethically? This is your starter kit.

---

## How It Works (The Guts)

Let's pop the hood on this thing. At its core, it's a clever pipeline that blends self-hosted search with AI smarts. I'll break it down like I'm explaining it to a buddy over coffee (or energy drinks).

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

Step-by-step geekery:

1. **You Query**: Type your question in the CLI. Simple as that.

2. **Agent Decides**: The OpenAI agent (running locally via API calls) figures if it needs web data. It's smart—uses tools like a pro.

3. **Search Kickoff**: If needed, it calls the SearchEngineManager, which handles the heavy lifting with config and error handling.

4. **SearXNG in Action**: This meta-search engine (in Docker) pings multiple sources anonymously, caches in Redis for speed, and returns JSON.

5. **AI Synthesis**: Results feed back to the agent, which crafts a natural response using OpenAI's models. No copy-paste links; think summarized insights.

It's modular, so if you're feeling adventurous, you can swap OpenAI for another LLM or add more tools. Solid OOP under the hood keeps it maintainable.

---

## Installation: Let's Get You Set Up (Noob-Friendly Edition)

Alright, newbie or pro, I've got you. We'll take it slow, with tips and troubleshooting. If you're on Windows, macOS, or Linux, this should work (just mind the slashes—use / for paths).

### What You'll Need (Prerequisites)
- **Docker & Docker Compose**: This runs the search backend. Grab [Docker Desktop](https://www.docker.com/products/docker-desktop/) if you haven't. (Tip: On Linux, install via your package manager for extra points.)
- **Python 3.8+**: Most systems have it. Check with `python --version`. If not, [download here](https://www.python.org/downloads/).
- **OpenAI API Key**: Sign up at [platform.openai.com](https://platform.openai.com/), grab a key, and keep it secret. (Free tier works for testing, but watch those API costs.)

Got that? Cool. Let's roll.

### 1. Clone and Navigate

Fire up your terminal and:

```bash
git clone https://github.com/your-username/personal-search-engine.git
cd personal-search-engine
```

(Replace `your-username` with the actual repo owner. Fork it if you want to tinker!)

### 2. Virtual Environment: Keep It Clean

Virtual envs are like sandboxes—prevent global mess. Highly recommended.

```bash
# Create it
python -m venv .venv

# Activate it
# macOS/Linux:
source .venv/bin/activate

# Windows (PowerShell or cmd):
.venv\\Scripts\\activate
```

See that (.venv) in your prompt? You're in the zone.

### 3. Set Your Secrets (.env File)

This is where your API key lives. Don't commit this file—add it to .gitignore.

```bash
# Copy the example (if it exists) or create fresh
cp .env.example .env  # Or just echo if no example

# Edit .env with your fave editor (nano, vim, VS Code)
# Add this line:
OPENAI_API_KEY=sk-YOUR_API_KEY_HERE
```

Tip: If you forget this, the app will yell about missing keys. We've all done it.

### 4. Run the Setup Script

This is the magic: It checks if Docker's running, installs Python packages via pip (or uv if you're fancy—see user rules), and spins up the containers.

```bash
python setup.py
```

What does it do under the hood?
- Installs deps from requirements.txt (things like openai, dotenv).
- Starts Docker Compose: Launches SearXNG and Redis.
- Tests the connection. If something's off, it'll tell you.

If you see "🎉 Setup completed successfully!", high-five yourself. Common hiccups:
- Docker not running? Start it.
- Port 8888 in use? Edit docker-compose.yml to change it.
- Firewall issues? Check your settings.

No luck? Hit the issues tab on GitHub or drop a line.

---

## Usage: Let's Play!

Now that it's installed, time to have fun. This section's packed with examples and tips.

### Fire Up the Main Agent

The star of the show:

```bash
python main.py
```

You'll get a prompt. Type questions, get answers. Type 'exit' to bail. Pro tip: It's conversational but stateless right now—each query is fresh.

Example session:
> You: Explain quantum computing like I'm 5.
> Assistant: [Fun, simplified explanation, maybe with a web search for accuracy]

### Library Mode: Integrate It Anywhere

Building your own app? Import and go.

```python
# your_script.py
from search_engine import SearchEngineManager, display_results

# Quick and dirty search
manager = SearchEngineManager()  # Grabs config from env or defaults
results = manager.quick_search("best python tips for beginners", max_results=10)

# Pretty print
display_results(results, title="Python Noob Hacks")

# Go fancy: Handle exceptions, customize params
try:
    advanced_results = manager.client.search(
        query="retro gaming history",
        engines=["google", "bing"],
        categories=["general"]
    )
    print(advanced_results)
except Exception as e:
    print(f"Oops: {e}")
```

See example.py for more. It's all OOP, so extend classes if you want custom behavior.

Tip: Check config.py for defaults. Override with env vars like SEARXNG_URL.

---

## Roadmap: What's Next? (And the Quirky Bits)

This project's young, but I've got big plans. Think of this as the beta version—solid, but with room for your input.

- [ ] **Web UI Option**: A chill Streamlit dashboard for non-terminal folks. Point, click, search.
- [ ] **Response Streaming**: Make answers appear in real-time, like chatting with a fast typer.
- [ ] **Memory Lane**: Add chat history so the agent remembers your last question. "Follow up on that fusion thing?"
- [ ] **Tool Belt Expansion**: Plug in a calculator, weather API, or even a code runner for ultimate utility.
- [ ] **Perf Tweaks**: Optimize for speed, maybe add local caching beyond Redis.

**Quirks to Know (Because Nothing's Perfect)**:
- **Goldfish Memory**: No session history yet—each query's a clean slate.
- **Error Handling**: It's there, but if the web's down or API limits hit, it might grumble. Check logs.
- **API Costs**: OpenAI isn't free forever. Monitor your usage.
- **Docker Drama**: If containers crash, `docker-compose logs` is your friend.
- **Windows Paths**: Use forward slashes (/) in configs for harmony.

Spot a bug? Love a feature? Jump to contributing!

---

## Contributing: Join the Party!

Hey, if this tickles your geek bone, why not contribute? We're all about that open-source vibe. Whether it's a bug fix, new feature, or just a doc tweak, PRs make the world go round.

1. Fork the repo (click that button on GitHub).
2. Create a branch: `git checkout -b feat/awesome-new-thing`.
3. Hack away, commit: `git commit -m 'feat: add awesome new thing'`. (We dig Conventional Commits—keeps things tidy.)
4. Push: `git push origin feat/awesome-new-thing`.
5. Open a PR and tell us what's up.

Update tests if you touch code (run 'em with pytest). Docs too. Questions? Open an issue first—we're friendly.

---

## License

MIT all the way. Free to use, tweak, and share. See LICENSE for the legalese. Built with ❤️ by [Your Name/Org]. If this saves you time (or sanity), drop a star on the repo! 