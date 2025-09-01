from typing import TypedDict, List, Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_BASE_URL = os.getenv("OPEN_AI_BASE_URL")


# Pydantic schemas
class RouteDecision(BaseModel):
    route: Literal["rag", "answer", "web"]
    reply: str | None = Field(None, description="Filled only when route = 'end'")

class RagJudge(BaseModel):
    sufficient: bool

# LLM instances with structured output where needed
router_llm = ChatOpenAI(base_url=OPEN_AI_BASE_URL, api_key=OPENAI_API_KEY, temperature=0).with_structured_output(RouteDecision)
judge_llm = ChatOpenAI(base_url=OPEN_AI_BASE_URL, api_key=OPENAI_API_KEY, temperature=0).with_structured_output(RagJudge)
answer_llm = ChatOpenAI(base_url=OPEN_AI_BASE_URL, api_key=OPENAI_API_KEY, temperature=0.7)

# Shared state type
class AgentState(TypedDict, total=False):
    messages: List[BaseMessage]
    route: Literal["rag", "answer", "end"]
    rag: str
    web: str