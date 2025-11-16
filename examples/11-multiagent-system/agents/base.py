import os
from typing import Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from tools.search import tavily_search

load_dotenv()


class State(MessagesState):
    summary: str = ""
    next: str
    approval: Optional[bool]


llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
)
tools = [tavily_search]
llm_with_tools = llm.bind_tools(tools)
