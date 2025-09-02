# LangChain Documentation RAG System

A Retrieval-Augmented Generation (RAG) system that provides intelligent chat capabilities for LangChain documentation using FastAPI backend, Streamlit frontend, and ChromaDB vector database.

## Architecture Overview

The system consists of three main components:

- **Backend**: FastAPI application with LangGraph agent for intelligent routing and RAG operations
- **Frontend**: Streamlit web interface for user interactions
- **Vector Database**: ChromaDB for storing and retrieving document embeddings

## Features

- Intelligent query routing between RAG and web search
- Context-aware conversations with chat history
- SQLite-based session management
- Docker containerization for easy deployment
- Support for multiple AI models

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)

### Environment Setup

1. Create `.env` file in the root directory:
```bash
# Backend Configuration
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Database Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Frontend Configuration
BACKEND_URL=http://localhost:5001
```

2. Run the entire system:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:8501
- Backend API: http://localhost:5001
- ChromaDB: http://localhost:8000

## Development

### Local Development Setup

1. Install backend dependencies:
```bash
cd app
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd frontend
pip install -r requirements.txt
```

3. Start services individually:
```bash
# Start ChromaDB
docker run -p 8000:8000 chromadb/chroma:latest

# Start backend
cd app && python main.py

# Start frontend
cd frontend && streamlit run app.py
```

## Project Structure

```
LangChainDocsRag/
├── app/                    # Backend FastAPI application
│   ├── src/               # Core application logic
│   ├── main.py            # FastAPI entry point
│   └── requirements.txt   # Python dependencies
├── frontend/              # Streamlit frontend
│   ├── app.py            # Main frontend application
│   └── requirements.txt  # Frontend dependencies
├── data_processing/       # Data ingestion scripts
├── docker-compose.yml     # Container orchestration
└── README.md             # This file
```

## API Endpoints

- `POST /chat` - Main chat endpoint for user queries
- `GET /docs` - Interactive API documentation (FastAPI)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
