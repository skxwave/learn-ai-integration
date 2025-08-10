import os
from langchain.prompts import PromptTemplate
from langchain.agents import tool, AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama

from ddgs import DDGS
from langchain_openai import ChatOpenAI


@tool
def user_data_tool(name: str) -> str:
    """Search user data by name"""
    user_data = {
        "roman": "Funny programmer guy!",
        "maksym": "Excellent crypto trader!",
    }
    return user_data.get(name.strip().lower(), "error")


@tool
def search_tool(query: str) -> list:
    """Tool for searching in internet through duckduckgo"""
    return DDGS().text(query, max_results=5)



tools = [user_data_tool, search_tool]
template = """
You have access to the following tools: {tools}

When you want to use a tool, respond ONLY in the format:

Thought: your reasoning
Action: one of [{tool_names}]
Action Input: the input to the action

Observation: the result of the action

When you have the final answer to the question, respond ONLY in the format:

Final Answer: <your answer here>

Question: {input}
{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(template=template)
llm = ChatOllama(
    temperature=0.5,
    model="deepseek-r1:8b",
    base_url="http://localhost:11434",
)
# llm = ChatOpenAI(
#     api_key=os.getenv("OPENROUTER_API_KEY"),
#     base_url="https://openrouter.ai/",
#     temperature=0.7,
# )
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
)

if __name__ == "__main__":
    result = agent_executor.invoke(
        {
            "input": "Use search tool and search this: langchain docs"
        }
    )
    print(result["output"])
