from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_BASE_URL = os.getenv("OPEN_AI_BASE_URL")

contextualize_q_system_prompt = (
    "You are a helpful assistant with the knowledge base of langchain documentation"
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is. "
    "-> Return **only** the reformulated question (no explanations, no answers)"
)

CONTEXT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

contextualize_chain = (CONTEXT_PROMPT | ChatOpenAI(base_url=OPEN_AI_BASE_URL, api_key=OPENAI_API_KEY, temperature=0) | StrOutputParser()).with_config(run_name="contextualize_chain")