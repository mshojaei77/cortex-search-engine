# 🚀 Setup Guide: AI-Powered Personal Search Engine

This guide will help you set up your own privacy-focused, AI-enhanced search engine using SearXNG, OpenAI API, and React TypeScript.

## 📋 Prerequisites

Before starting, ensure you have:

- **Docker & Docker Compose** installed
- **Node.js 20+** for local development
- **OpenAI API Key** (optional, for AI features)
- **Git** for cloning repositories

## 🔧 Quick Setup (5 Minutes)

### 1. Clone and Configure

```bash
# Clone the project
git clone <your-repo-url>
cd personal-search-engine

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` file with your settings:

```env
# Required: OpenAI API Key (for AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Customize ports and hostnames
SEARXNG_HOSTNAME=localhost
SEARXNG_PORT=8080
FRONTEND_PORT=3000

# AI Features (set to 'false' to disable)
VITE_OPENAI_ENABLED=true
```

### 3. Generate SearXNG Secret Key

**Linux/Mac:**
```bash
# Replace the secret key in SearXNG settings
sed -i "s|ultrasecretkey|$(openssl rand -hex 32)|g" backend/searxng/settings.yml
```

**Windows (PowerShell):**
```powershell
# Generate and replace secret key
$secretKey = -join ((1..64) | ForEach {'{0:x}' -f (Get-Random -Max 16)})
(Get-Content backend/searxng/settings.yml) -replace 'ultrasecretkey', $secretKey | Set-Content backend/searxng/settings.yml
```

### 4. Start the Application

```bash
# Start all services
docker-compose up -d

# Monitor logs (optional)
docker-compose logs -f
```

### 5. Access Your Search Engine

- **Search Interface**: http://localhost:3000
- **SearXNG Direct**: http://localhost:8080
- **AI Service**: http://localhost:8001 (if enabled)

## 🎯 Development Setup

For local development with hot reloading:

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000 with:
- ⚡ Hot module replacement
- 🔄 Automatic browser refresh
- 🔍 Proxy to SearXNG backend

### Backend Services

Keep the backend services running with Docker:

```bash
# Start only backend services
docker-compose up -d redis searxng

# Or start with AI service
docker-compose --profile with-ai up -d
```

## 🔧 Advanced Configuration

### SearXNG Customization

Edit `backend/searxng/settings.yml` to:

- **Enable/disable search engines**: Modify the `engines` section
- **Customize categories**: Update `categories_as_tabs`
- **Adjust privacy settings**: Configure `outgoing` and `server` sections
- **Change themes**: Set `ui.default_theme`

### AI Service Configuration

The OpenAI service supports several models and configurations:

```python
# In services/openai/client.py
self.model = "gpt-4o-mini"  # Cost-effective option
# or
self.model = "gpt-4-turbo"  # Higher quality
```

### Frontend Customization

Key configuration files:

- `frontend/vite.config.ts` - Build and dev server settings
- `frontend/tailwind.config.js` - Design system and styling
- `frontend/src/services/searchApi.ts` - API configuration

## 🐳 Docker Profiles

The application supports different deployment profiles:

```bash
# Basic setup (no AI)
docker-compose up -d

# With AI enhancement
docker-compose --profile with-ai up -d

# Development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## 🔍 Troubleshooting

### Common Issues

**1. SearXNG not responding**
```bash
# Check SearXNG logs
docker-compose logs searxng

# Restart SearXNG
docker-compose restart searxng
```

**2. Frontend can't connect to backend**
```bash
# Verify proxy configuration in vite.config.ts
# Check if SearXNG is running on correct port
docker-compose ps
```

**3. AI features not working**
```bash
# Check OpenAI API key
echo $OPENAI_API_KEY

# Check AI service logs
docker-compose logs openai-service
```

**4. CORS errors**
```bash
# Ensure CORS is configured in SearXNG settings.yml
# Check Nginx proxy configuration in frontend/nginx.conf
```

### Service Health Checks

```bash
# Check all service health
docker-compose ps

# Individual service health
curl http://localhost:8080/health  # SearXNG
curl http://localhost:3000/health  # Frontend
curl http://localhost:8001/health  # AI Service
```

### Reset and Clean Installation

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: This deletes all data)
docker-compose down -v

# Remove images (to force rebuild)
docker-compose down --rmi all

# Start fresh
docker-compose up -d --build
```

## 🚀 Production Deployment

### Security Hardening

1. **Environment Variables**:
   ```bash
   # Use Docker secrets or external secret management
   docker secret create openai_key your_api_key
   ```

2. **Reverse Proxy**:
   ```bash
   # Use Caddy, Nginx, or Traefik for HTTPS termination
   # Update docker-compose.yml with proper networking
   ```

3. **Resource Limits**:
   ```yaml
   # Add to docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 512M
         cpus: '0.5'
   ```

### Performance Optimization

1. **SearXNG Caching**:
   - Redis is already configured for optimal caching
   - Monitor cache hit rates in logs

2. **Frontend Optimization**:
   - Static assets are cached for 1 year
   - Gzip compression enabled
   - Chunked loading for better performance

3. **AI Service Scaling**:
   ```bash
   # Scale AI service for high load
   docker-compose up -d --scale openai-service=3
   ```

## 📊 Monitoring and Analytics

### Log Aggregation

```bash
# Centralized logging with Docker
docker-compose logs --follow --tail=100

# Specific service logs
docker-compose logs searxng --follow
```

### Metrics Collection

Add monitoring services to `docker-compose.yml`:

```yaml
# Example: Add Prometheus monitoring
prometheus:
  image: prom/prometheus
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
```

## 🔒 Privacy and Security

### Data Protection

- **No query logging**: SearXNG is configured to not store queries
- **No user tracking**: All searches are anonymous
- **Local processing**: AI enhancement can be disabled for full privacy

### Security Features

- **Content Security Policy**: Configured in Nginx
- **HTTPS Ready**: Add SSL certificates to the reverse proxy
- **Non-root containers**: All services run with limited privileges

## 🆘 Support and Community

### Getting Help

1. **Check the logs**: Most issues are visible in Docker logs
2. **Review configuration**: Ensure all environment variables are set
3. **Community resources**:
   - [SearXNG Documentation](https://docs.searxng.org/)
   - [OpenAI API Documentation](https://platform.openai.com/docs/)
   - [React + Vite Documentation](https://vitejs.dev/)

### Contributing

Contributions are welcome! Areas for improvement:

- Additional search engines
- More AI enhancement features
- UI/UX improvements
- Performance optimizations
- Documentation updates

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## ✨ What's Next?

Once your search engine is running:

1. **Customize the UI** - Modify colors, layout, and branding
2. **Add more search engines** - Configure additional sources in SearXNG
3. **Enhance AI features** - Experiment with different OpenAI models
4. **Deploy to production** - Set up HTTPS and monitoring
5. **Share your setup** - Help others build their own private search engines

Happy searching! 🔍✨ 