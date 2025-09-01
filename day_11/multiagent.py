import os
from dotenv import load_dotenv
from typing import Literal, TypedDict

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph
from langgraph.types import Command

from agents.research_agent import research_agent
from agents.base import State, llm

load_dotenv()


def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and they will go to finish point"
    )

    class Router(TypedDict):
        """Worker to route to next."""

        next: Literal[*members]  # type: ignore

    def supervisor_node(state: State) -> Command[Literal[*members]]:  # type: ignore
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]

        return Command(goto=goto, update={"next": goto})

    return supervisor_node


def chat_node(state: State):
    messages = state["messages"] + [state.get("summary", "")]
    result = llm.invoke(messages)
    return {"messages": result}


def summarizer_node(state: State):
    messages = state["messages"]

    if len(messages) < 7:
        return state
    
    prompt = f"Summarize this conversation:\n{messages}"
    summary = llm.invoke(prompt)
    state["messages"] = state["messages"][-3:]  # Shi not working (need to override messages)
    return {"summary": summary}


supervisor = make_supervisor_node(llm, ["chat_node", "research_node"])

builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("summarizer_node", summarizer_node)
builder.add_node("chat_node", chat_node)
builder.add_node("research_node", research_agent)

builder.set_entry_point("summarizer_node")
builder.add_edge("summarizer_node", "supervisor")

graph = builder.compile()

if __name__ == "__main__":
    with open("graph.png", "wb") as f:
        f.write(graph.get_graph(xray=1).draw_mermaid_png())
