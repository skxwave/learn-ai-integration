from langgraph.graph.state import StateGraph
from langgraph.graph.message import MessagesState
from langgraph.graph import START
from langgraph.prebuilt import tools_condition, ToolNode

from langchain_openai import ChatOpenAI

from ddgs import DDGS
import requests


def search_tool(query: str):
    """
    Tool for searching in DuckDuckGo by query.
    
    Params:
    - Query: str - the query to search
    """
    with DDGS() as ddg:
        results = ddg.text(query, max_results=3)
    if not results:
        return "No results found."
    formatted = "\n".join(f"- {r['title']} ({r['href']})" for r in results)
    return formatted


def bybit_ticker_data(ticker: str, category: str = "spot"):
    """
    Tool to fetch the latest ticker info from Bybit.

    Args:
        ticker (str): The symbol to query, e.g., "BTCUSDT".
        category (str): Market category. Can be only "linear", "spot", "inverse", or "option"

    Returns:
        str: A formatted string with the latest price and 24h change.
    """
    if "USDT" not in ticker.upper():
        ticker += "USDT"
    url = f"https://api.bybit.com/v5/market/tickers?category={category.lower()}&symbol={ticker.upper()}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if "result" not in data or not data["result"]:
            return f"No data found for ticker: {ticker}"
        
        ticker_data = data["result"]["list"][0]
        price = ticker_data.get("lastPrice")
        change_24h = ticker_data.get("price24hPcnt")

        return f"Ticker: {ticker.upper()}, Price: {price}, 24h Change: {change_24h}"
    
    except requests.RequestException as e:
        return f"Error fetching ticker {ticker}: {e}"


llm = ChatOpenAI(
    model="qwen/qwen3-coder:free",  # Using model that support tools
    temperature=0.4,
    base_url="https://openrouter.ai/api/v1",
)
tools = [
    search_tool,
    bybit_ticker_data,
]
llm_with_tools = llm.bind_tools(tools)


def llm_call(state: MessagesState):
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": result}


workflow = StateGraph(MessagesState)
workflow.add_node("llm_call", llm_call)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("llm_call")
workflow.add_edge("tools", "llm_call")
workflow.add_conditional_edges(
    "llm_call",
    tools_condition,
)

graph = workflow.compile()
