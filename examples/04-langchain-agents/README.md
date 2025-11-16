# Example 04: LangChain Agents

Exploring **agent-based AI systems** using LangChain's **ReAct** framework with tool calling, web search, and vector database integration.

## What You'll Learn

- Building ReAct agents with LangChain
- Creating custom tools for agents
- Integrating DuckDuckGo search
- Setting up Qdrant vector database
- Agent prompt engineering
- Handling agent execution and errors

## Files

- `langchain_agent_test.py` - ReAct agent with custom tools
- `langchain_test.py` - Basic LangChain experiments
- `qdrant_langchain.py` - Vector database setup
- `qdrant_test.py` - Qdrant client testing

## Running the Examples

### ReAct Agent
```bash
python langchain_agent_test.py
```

### Qdrant Setup
```bash
# Start Qdrant
docker run --publish 6333:6333 \\
  --volume /path/to/qdrant_storage:/qdrant/storage \\
  qdrant/qdrant

# Test connection
python qdrant_test.py
```

## Key Concepts

### ReAct Pattern
**Reasoning + Acting** - Agent alternates between:
1. **Thought** - Reasoning about the task
2. **Action** - Using a tool
3. **Observation** - Processing tool results
4. **Final Answer** - Responding to user

### Custom Tools

```python
@tool
def user_data_tool(name: str) -> str:
    \"\"\"Search user data by name\"\"\"
    user_data = {
        "roman": "Funny programmer guy!",
        "maksym": "Excellent crypto trader!",
    }
    return user_data.get(name.strip().lower(), "error")

@tool
def search_tool(query: str) -> list:
    \"\"\"Tool for searching in internet through duckduckgo\"\"\"
    return DDGS().text(query, max_results=5)
```

## Technologies

- **LangChain** - Agent framework
- **Ollama/OpenRouter** - LLM providers
- **DuckDuckGo** - Web search (no API key needed!)
- **Qdrant** - Vector database

## Agent Configuration

```python
# Define tools
tools = [user_data_tool, search_tool]

# Create prompt template (ReAct format)
template = \"\"\"
You have access to the following tools: {tools}

When you want to use a tool, respond ONLY in the format:
Thought: your reasoning
Action: one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

When you have the final answer:
Final Answer: <your answer here>

Question: {input}
{agent_scratchpad}
\"\"\"

# Create agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # See reasoning process
    handle_parsing_errors=True,
    max_iterations=3,
)
```

## Using Ollama (Local Models)

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    temperature=0.5,
    model="deepseek-r1:8b",
    base_url="http://localhost:11434",
)
```

## Using OpenRouter

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/",
    temperature=0.7,
)
```

## Example Interactions

```
Input: "Search for langchain docs"

Thought: I need to search the internet for langchain documentation
Action: search_tool
Action Input: langchain docs
Observation: [Search results with links]
Final Answer: Here are the official LangChain docs...
```

## Vector Database Integration

Qdrant setup for semantic search:

```python
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

client = QdrantClient(host="localhost", port=6333)
vectorstore = QdrantVectorStore(
    embedding=embeddings,
    client=client,
    collection_name="my_collection"
)
```

## Best Practices

1. **Clear Tool Descriptions** - Help the agent understand when to use each tool
2. **Error Handling** - Use `handle_parsing_errors=True`
3. **Max Iterations** - Prevent infinite loops
4. **Verbose Mode** - Debug agent reasoning
5. **Temperature** - Lower for focused tasks, higher for creative ones

## Common Issues

### Agent Not Using Tools
- Check tool descriptions are clear
- Verify prompt template includes tool instructions
- Ensure model supports function calling (not all do)

### Parsing Errors
- Enable `handle_parsing_errors=True`
- Adjust temperature (lower can help)
- Simplify prompt template

### Qdrant Connection Failed
- Ensure Docker container is running
- Check port 6333 is accessible
- Verify volume permissions

## Configuration

```bash
# For OpenRouter
OPENROUTER_API_KEY=your-key-here

# For Ollama (default)
# No API key needed, just run: ollama serve
```

## Next Steps

- Explore Example 05 for advanced RAG with Qdrant
- Try Example 07 for LangGraph-based agents
- Add more custom tools for your use case

## Resources

- [LangChain Agents Docs](https://python.langchain.com/docs/modules/agents/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
