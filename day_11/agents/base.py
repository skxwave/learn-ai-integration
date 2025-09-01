import os
from typing import Optional
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langgraph.graph import MessagesState

from tools.search import tavily_search

load_dotenv()


class State(MessagesState):
    summary: str = ""
    next: str
    approval: Optional[bool]


llm = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1/",
    api_key=os.getenv("OPENAI_API_KEY")
)
tools = [tavily_search]
llm_with_tools = llm.bind_tools(tools)
