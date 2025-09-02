# Frontend - LangChain RAG Chat Interface

Streamlit-based web interface that provides an intuitive chat experience for interacting with the LangChain RAG system.

## Overview

The frontend is built with Streamlit and provides:
- Real-time chat interface
- Session management with unique session IDs
- Model selection capabilities
- Chat history display
- Responsive design for various screen sizes

## Features

- **Chat Interface**: Clean, conversational UI similar to modern chat applications
- **Session Management**: Automatic session creation and persistence
- **Model Selection**: Dropdown for choosing different AI models
- **Real-time Updates**: Immediate response display without page refresh
- **Error Handling**: User-friendly error messages for failed requests

## Architecture

### Core Components

- **Session State**: Manages user sessions and chat history
- **API Integration**: Communicates with backend via HTTP requests
- **UI Components**: Streamlit widgets for user interaction
- **State Management**: Persistent chat history within sessions

### Data Flow

1. User inputs question in chat interface
2. Frontend sends POST request to backend `/chat` endpoint
3. Backend processes query and returns response
4. Frontend displays response and updates chat history
5. Session state maintains conversation context

## Setup

### Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
# Backend API Configuration
BACKEND_URL=http://localhost:5001

# Optional: Custom styling and configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

### Configuration

The application automatically configures:
- Page title and icon
- Session state initialization
- Model selection options
- Backend URL connection

## Running the Application

### Development Mode

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

### Production Mode

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker

```bash
docker build -t rag-frontend .
docker run -p 8501:8501 rag-frontend
```

## User Interface

### Main Components

1. **Header**: Application title and branding
2. **Sidebar**: Model selection and configuration options
3. **Chat Area**: Main conversation interface
4. **Input Field**: Text input for user questions
5. **Chat History**: Scrollable conversation thread

### Session Management

- Each user gets a unique session ID
- Chat history persists during the session
- Sessions are managed automatically by Streamlit

### Model Selection

Currently supports:
- `openai/gpt-oss-120b:free` (default)

Additional models can be added by modifying the `options` list in the selectbox.

## Development

### Project Structure

```
frontend/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
└── README.md          # This file
```

### Customization

#### Adding New Models

Modify the model selection in `app.py`:

```python
model = st.selectbox(
    "Select a model",
    options=["model1", "model2", "model3"],
    index=0,
)
```

#### Styling Changes

Use Streamlit's built-in styling options or custom CSS:

```python
st.markdown("""
<style>
.custom-css {
    color: blue;
}
</style>
""", unsafe_allow_html=True)
```

#### Adding New Features

1. Extend the sidebar with additional controls
2. Add new state variables to `st.session_state`
3. Implement additional API endpoints integration

## API Integration

### Backend Communication

The frontend communicates with the backend through:
- HTTP POST requests to `/chat` endpoint
- JSON payload with question, session_id, and model
- Response parsing and error handling

### Error Handling

- Network timeouts (120 seconds)
- HTTP error responses
- User-friendly error messages
- Graceful degradation

## Testing

### Manual Testing

1. Start the application
2. Test chat functionality with various inputs
3. Verify session persistence
4. Test error scenarios

### Automated Testing

```bash
# Install testing dependencies
pip install pytest streamlit-testing

# Run tests
pytest tests/
```

## Deployment

### Streamlit Cloud

1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically on push

### Docker Deployment

```bash
docker build -t rag-frontend .
docker run -d -p 8501:8501 rag-frontend
```

### Environment Considerations

- Ensure backend is accessible from frontend
- Set appropriate CORS headers if needed
- Configure network security for production

## Troubleshooting

### Common Issues

1. **Backend Connection**: Verify `BACKEND_URL` is correct
2. **Port Conflicts**: Check if port 8501 is available
3. **Session Issues**: Clear browser cache and restart

### Debug Mode

Enable debug logging:

```bash
streamlit run app.py --logger.level debug
```

### Performance

- Chat history is stored in memory (session state)
- Large conversations may impact performance
- Consider implementing pagination for very long histories
