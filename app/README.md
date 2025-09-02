# Backend - LangChain RAG System

FastAPI backend application that provides intelligent chat capabilities using LangGraph agents, RAG operations, and web search integration.

## Architecture

The backend is built around a LangGraph agent that intelligently routes user queries between different processing nodes:

- **Router Node**: Determines the best path for query processing
- **RAG Node**: Retrieves relevant information from ChromaDB vector database
- **Web Search Node**: Performs web searches when additional information is needed
- **Answer Node**: Generates final responses using AI models

## Core Components

### LangGraph Agent (`src/langgraph_agent.py`)
- State-based workflow management
- Conditional routing between nodes
- Handles conversation flow and context

### Database Utilities (`src/db_utils.py`)
- SQLite database for chat history
- Session management and conversation storage
- Automatic table creation and initialization

### Pydantic Models (`src/pydantic_models.py`)
- Request/response validation
- Type-safe data handling
- API contract definition

### LangChain Utilities (`src/langchain_utils.py`)
- Contextualization chains
- RAG pipeline components
- Model integration

## Setup

### Environment Variables

Create a `.env` file in the `app/` directory:

```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Database Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Application Settings
PYTHONUNBUFFERED=1
```

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

### Database Initialization

The SQLite database is automatically initialized when the application starts. The `create_chat_history()` function creates the necessary tables.

## Running the Application

### Development Mode

```bash
python main.py
```

The server will start on `http://localhost:5000` with auto-reload enabled.

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

### Docker

```bash
docker build -t rag-backend .
docker run -p 5000:5000 rag-backend
```

## API Endpoints

### POST /chat

Main chat endpoint that processes user queries.

**Request Body:**
```json
{
  "question": "string",
  "session_id": "string",
  "model": "string"
}
```

**Response:**
```json
{
  "answer": "string",
  "session_id": "string",
  "model": "string"
}
```

## Development

### Project Structure

```
app/
├── src/
│   ├── __init__.py
│   ├── chroma_utils.py      # ChromaDB operations
│   ├── db_utils.py          # Database utilities
│   ├── langchain_utils.py   # LangChain components
│   ├── langgraph_agent.py   # Main agent logic
│   ├── nodes.py             # Processing nodes
│   ├── pydantic_models.py   # Data models
│   ├── shared.py            # Shared state and types
│   ├── tools.py             # Custom tools
│   └── utils.py             # Utility functions
├── main.py                  # FastAPI application
├── requirements.txt         # Dependencies
└── Dockerfile              # Container configuration
```

### Adding New Nodes

1. Create a new function in `src/nodes.py`
2. Add the node to the graph in `src/langgraph_agent.py`
3. Update routing logic as needed


## Troubleshooting

### Common Issues

1. **ChromaDB Connection**: Ensure ChromaDB is running and accessible
2. **API Keys**: Verify all required API keys are set in `.env`
3. **Port Conflicts**: Check if port 5000 is available

