from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class ModelName(BaseModel):
    GPT_OSS = "openai/gpt-oss-120b:free"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT_OSS)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName