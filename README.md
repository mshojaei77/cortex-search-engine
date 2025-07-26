# AI-Powered Personal Search Engine

A modern, privacy-focused search engine that combines SearXNG metasearch capabilities with OpenAI's intelligent function calling to provide enhanced, AI-powered search results.

## 🌟 Features

- **Privacy-First**: Built on SearXNG for complete search privacy
- **AI-Enhanced**: OpenAI function calling for intelligent search result processing
- **Modern UI**: React TypeScript frontend with Vite for blazing-fast performance
- **Responsive Design**: Beautiful, mobile-first interface
- **Real-time Search**: Instant search with modern UX patterns
- **Dockerized**: Complete containerization for easy deployment
- **Production-Ready**: Error handling, loading states, and optimizations

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   OpenAI API     │    │   SearXNG       │
│   (TypeScript)   │◄──►│   Functions      │◄──►│   Backend       │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 20+ 
- Docker & Docker Compose
- OpenAI API key

### Environment Setup

1. Clone and setup:
```bash
git clone <your-repo>
cd personal-search-engine
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Add your OpenAI API key to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
SEARXNG_HOSTNAME=localhost
```

4. Start the application:
```bash
docker-compose up -d
npm install
npm run dev
```

5. Open http://localhost:3000

## 📁 Project Structure

```
personal-search-engine/
├── backend/
│   ├── searxng/
│   │   └── settings.yml
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   └── package.json
├── services/
│   └── openai/
└── docker-compose.yml
```

## 🛠️ Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS
- **Backend**: SearXNG (metasearch engine)
- **AI**: OpenAI GPT-4 with function calling
- **Containerization**: Docker, Docker Compose
- **Build Tools**: Vite, ESBuild, SWC

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm run dev
```

### Backend Services
```bash
docker-compose up searxng redis
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `SEARXNG_HOSTNAME` | SearXNG hostname | localhost |
| `SEARXNG_PORT` | SearXNG port | 8080 |
| `FRONTEND_PORT` | Frontend port | 3000 |

## 📋 TODO

- [x] SearXNG Docker setup
- [x] OpenAI function calling service
- [x] React TypeScript frontend
- [x] Modern UI components
- [x] Search result processing
- [x] Error handling and loading states
- [x] Production optimizations
- [x] Docker Compose orchestration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SearXNG](https://docs.searxng.org/) - Privacy-respecting metasearch engine
- [OpenAI](https://openai.com/) - AI-powered function calling
- [React](https://react.dev/) - Modern UI framework
- [Vite](https://vitejs.dev/) - Next-generation frontend tooling 