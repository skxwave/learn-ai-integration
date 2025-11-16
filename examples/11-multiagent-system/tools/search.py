from langchain.tools import tool
from langchain_community.tools import TavilySearchResults


@tool
def tavily_search(query: str, max_results: int = 5) -> str:
    """
    Tool for searching in web with Tavily.

    Args:
        query (str): Query to search.
        max_results (int): Maximum results.
    """
    tavily_search = TavilySearchResults(max_results=max_results)
    results = tavily_search.invoke(query)
    formatted_result = "\n\n---\n\n".join(
        [
            f'<Document href="{result["url"]}">\n{result["content"]}\n</Document>'
            for result in results
        ]
    )

    return formatted_result
