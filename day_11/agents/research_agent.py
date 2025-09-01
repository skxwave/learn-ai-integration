from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from .base import tools, llm_with_tools, State


def search_node(state: State):
    system_prompt = (
        f"You are research agent. You have this list of search tools: {tools}"
        "Your task is to search by user query with your tools, and generate summary in this format:"
        "- Small agenda -> quick overview -> resume -> resourses you found (links etc.)"
        "User needs to approve your output."
    )
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    result = llm_with_tools.invoke(messages)
    return {"messages": result}


builder = StateGraph(State)
builder.add_node("search_node", search_node)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("search_node")
builder.add_edge("tools", "search_node")
builder.add_conditional_edges("search_node", tools_condition)

research_agent = builder.compile()
