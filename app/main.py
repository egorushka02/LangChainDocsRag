import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from src.pydantic_models import QueryInput, QueryResponse
from src.db_utils import create_chat_history, insert_chat_history, get_chat_history
from src.langgraph_agent import agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import logging, sys
import shutil
from src.utils import get_or_create_session_id, history_to_lc_messages, append_messages
from src.langchain_utils import contextualize_chain
logging.basicConfig(filename='app.log', level=logging.INFO)

app = FastAPI()

from fastapi.requests import Request

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logging.exception("Unhandled error while processing request")
        raise

create_chat_history()

# Load environment variables from .env file
load_dotenv(override=True)

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    """
    Main chat endpoint using the LangGraph agent with routing, RAG, and web search capabilities
    """
    session_id = get_or_create_session_id(query_input.session_id)
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")

    try:
        # Convert chat history to LangChain messages
        chat_history = get_chat_history(session_id)
        messages = history_to_lc_messages(chat_history)

        # Add current user message
        # 2. generate a stand-alone question
        standalone_q = contextualize_chain.invoke({
            "chat_history": messages,
            "input": query_input.question,
        })

        messages = append_messages(messages, HumanMessage(content=standalone_q))
        # Invoke the LangGrapg agent
        result = agent.invoke(
            {"messages": messages}
        )
        # Get the latest AI message
        last_message = next((m for m in reversed(result['messages'])
                             if isinstance(m, AIMessage)), None)
        
        if last_message:
            answer = last_message.content
        else:
            answer = "I apologise, but I couldn't generate a response at this time."
        
        # Store the conversation
        insert_chat_history(session_id, query_input.question, answer, query_input.model.value)
        logging.info(f"Session ID: {session_id}, AI Response: {answer}")

        return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)
    
    except Exception as e:
        logging.error(f"Error in chat")
        raise HTTPException(status_code=500, detail=f"Chat error")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        'main:app',
        host="0.0.0.0",
        port=5000,
        log_level='debug',
        reload=True
    )