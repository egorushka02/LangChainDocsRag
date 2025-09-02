# Quick Start Guide

Get the LangChain RAG system up and running in minutes.

## Prerequisites

- Docker and Docker Compose installed
- API keys for OpenAI and Tavily

## Step 1: Environment Setup

1. Copy the environment template:
```bash
cp env.template .env
```

2. Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=sk-your-actual-openai-key
TAVILY_API_KEY=tvly-your-actual-tavily-key
```

## Step 2: Launch the System

Start all services with Docker Compose:
```bash
docker-compose up -d
```

## Step 3: Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:5001
- **ChromaDB**: http://localhost:8000

## Step 4: Start Chatting

1. Open http://localhost:8501 in your browser
2. Type a question about LangChain
3. The system will automatically route your query and provide an answer

## What Happens Next

1. **Router Node**: Determines if your question needs RAG or web search
2. **RAG Node**: Searches ChromaDB for relevant documentation
3. **Web Search Node**: Performs web search if additional info is needed
4. **Answer Node**: Generates a comprehensive response

## Troubleshooting

### Common Issues

**"Backend connection failed"**
- Check if backend container is running: `docker ps`
- Verify `.env` file has correct `BACKEND_URL`

**"API key error"**
- Ensure `OPENAI_API_KEY` and `TAVILY_API_KEY` are set in `.env`
- Restart containers: `docker-compose restart`

**"ChromaDB connection failed"**
- Check ChromaDB container status
- Verify ports are not conflicting

### Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [app/README.md](app/README.md) for backend development
- Review [frontend/README.md](frontend/README.md) for frontend customization
- Explore the codebase to understand the architecture

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify environment variables
3. Ensure all ports are available
4. Check Docker container status
