# Example 07: LangGraph Chatbot

Building an intelligent **chatbot** using **LangGraph** with the **ReAct** (Reasoning + Acting) pattern and tool integration.

## What You'll Learn

- LangGraph state management for chatbots
- ReAct agent pattern implementation
- Tool binding and execution
- DuckDuckGo search integration
- Bybit cryptocurrency API integration
- Conditional routing in graphs

## Files

### Studio Setup
- `studio/chatbot.py` - Main chatbot graph implementation
- `studio/tools.py` - Tool definitions (search, ticker data)
- `studio/langgraph.json` - LangGraph configuration

## Running the Example

### Using LangGraph Studio (Recommended)

```bash
cd studio
langgraph dev

# Open browser to:
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

### Direct Python Execution

```bash
cd studio
python chatbot.py
```

## Features

### Integrated Tools

#### 1. DuckDuckGo Search
```python
search_tool(query: str)
```
- Real-time web search
- Returns top 3 results with links
- Perfect for current information

#### 2. Bybit Ticker Data
```python
bybit_ticker_data(ticker: str, category: str)
```
- Fetch cryptocurrency prices
- 24-hour price changes
- Supports: spot, linear, inverse, option

### Example Interactions

**Web Search:**
```
User: What's the latest news about LangChain?
Bot: [Uses search_tool] Here's what I found...
```

**Crypto Prices:**
```
User: What's the current BTC price?
Bot: [Uses bybit_ticker_data] Bitcoin (BTCUSDT): $X, 24h Change: Y%
```

**Mixed Reasoning:**
```
User: Should I buy ETH based on recent trends?
Bot: [Uses search_tool + bybit_ticker_data] Based on current price...
```

## Architecture

```
User Message
    ↓
LLM (ReAct Reasoning)
    ↓
Decision: Use Tool?
    ├─ Yes → Execute Tool → LLM (Process Results)
    └─ No → Direct Response
    ↓
Final Answer
```

## Technologies

- **LangGraph** - State management and orchestration
- **OpenRouter** - Access to Qwen-3-Coder (free tier)
- **DuckDuckGo** - Web search API
- **Bybit API** - Cryptocurrency market data
- **LangGraph Studio** - Visual debugging and testing

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your-openrouter-key  # Use with OpenRouter base URL
```

### Model Configuration
```python
llm = ChatOpenAI(
    model="qwen/qwen3-coder:free",
    temperature=0.4,
    base_url="https://openrouter.ai/api/v1",
)
```

## Graph Structure

```python
StateGraph(MessagesState)
    ├─ llm_call (node)
    │   └─ Invokes LLM with tools
    ├─ tools (node)
    │   └─ Executes selected tool
    └─ Conditional edges
        └─ Route based on tool calls
```

## Customization

### Adding New Tools

```python
def your_tool(param: str) -> str:
    """
    Tool description for the LLM.
    
    Args:
        param: Description
    
    Returns:
        Result description
    """
    # Your implementation
    return result

tools = [search_tool, bybit_ticker_data, your_tool]
```

### Changing the Model

```python
# Use GPT-4
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Use Ollama locally
from langchain_ollama import ChatOllama
llm = ChatOllama(
    model="mistral",
    temperature=0.5,
)
```

## LangGraph Studio Features

- **Visual Graph** - See your agent's decision flow
- **Step-through Debugging** - Pause at each node
- **State Inspection** - View state at each step
- **Interactive Testing** - Chat with your bot in real-time
- **Trace Visualization** - Understand tool calls and reasoning

## Best Practices

1. **Tool Descriptions** - Make them clear and specific
2. **Temperature** - Lower (0.2-0.4) for tool-use, higher for creative chat
3. **Error Handling** - Always handle API failures gracefully
4. **State Management** - Keep state schema simple
5. **Testing** - Use Studio for rapid iteration

## Common Issues

### Tools Not Being Called
- Check tool descriptions are clear
- Verify model supports function calling
- Lower temperature can help

### API Errors
- Ensure environment variables are set
- Check API key validity
- Handle rate limits and timeouts

## Next Steps

- Add more tools (calculator, database queries, etc.)
- Implement memory persistence (see Example 03)
- Deploy to production (see Example 09)
- Try advanced patterns (see Example 08)

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Tool Use Guide](https://python.langchain.com/docs/modules/agents/tools/)
