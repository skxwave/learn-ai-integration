# 🤖 AI Integration Examples

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://python.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.4+-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive collection of hands-on examples demonstrating AI integration patterns using **LangChain**, **LangGraph**, **FastAPI**, and various LLM providers. This repository showcases practical implementations of RAG systems, AI agents, multi-agent architectures, and production deployment strategies.

## 🎯 What's Inside

This repository contains **11 progressive examples** covering the full spectrum of AI application development:

- ✅ **RAG (Retrieval-Augmented Generation)** with vector databases
- ✅ **AI Agents** with tool calling and memory management
- ✅ **Multi-Agent Systems** with supervisor patterns
- ✅ **LangGraph** for complex agentic workflows
- ✅ **Production Deployment** with Docker and LangGraph Cloud
- ✅ **Real-world Applications** (chatbots, sentiment analysis, research assistants)

## 📚 Examples Overview

### Foundation Examples (01-05)

| # | Example | Technologies | Description |
|---|---------|-------------|-------------|
| **01** | [FastAPI Basics](examples/01-fastapi-basics/) | FastAPI, OpenAI, FAISS | Building REST APIs with AI endpoints, basic RAG implementation |
| **02** | [LangChain Prompts](examples/02-langchain-prompts/) | LangChain, Prompt Templates | Prompt engineering, template creation, chain composition |
| **03** | [Chatbot Memory](examples/03-chatbot-memory/) | Ollama, SQLite | Building conversational AI with persistent memory |
| **04** | [LangChain Agents](examples/04-langchain-agents/) | ReAct, DuckDuckGo, Qdrant | Tool-calling agents, vector database integration |
| **05** | [RAG & Vector DB](examples/05-rag-vectordb/) | Qdrant, HuggingFace Embeddings | Production-ready RAG with vector similarity search |

### LangGraph Examples (06-09)

| # | Example | Technologies | Description |
|---|---------|-------------|-------------|
| **06** | [LangGraph Fundamentals](examples/06-langgraph-fundamentals/) | LangGraph Studio, State Management | Core concepts: graphs, nodes, edges, state schemas |
| **07** | [LangGraph Chatbot](examples/07-langgraph-chatbot/) | ReAct, Tool Binding | Building a chatbot with LangGraph and tool integration |
| **08** | [LangGraph Advanced](examples/08-langgraph-advanced/) | Subgraphs, Parallelization | Complex workflows, map-reduce patterns, memory stores |
| **09** | [Deployment](examples/09-deployment/) | Docker, LangGraph Cloud | Containerization and cloud deployment strategies |

### Advanced Examples (10-11)

| # | Example | Technologies | Description |
|---|---------|-------------|-------------|
| **10** | [Twitter Sentiment Analysis](examples/10-twitter-sentiment/) | Twitter API, Sentiment Analysis | Crypto market analysis from social media data |
| **11** | [Multi-Agent System](examples/11-multiagent-system/) | Supervisor Pattern, Tavily | Coordinated agents with research and chat capabilities |

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** (required for optimal LangGraph compatibility)
- **API Keys** (at least one):
  - [OpenAI](https://platform.openai.com/api-keys) or [OpenRouter](https://openrouter.ai/keys)
  - [Tavily](https://tavily.com/) (for web search tools)
- **Optional**:
  - [Ollama](https://ollama.ai/) (for local models)
  - [Docker](https://www.docker.com/) (for deployment examples)
  - [Qdrant](https://qdrant.tech/) (vector database - can run via Docker)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/skxwave/learn-ai-integration.git
   cd learn-ai-integration
   ```

2. **Create virtual environment**
   ```bash
   uv venv .venv

   # Or with python venv
   python -m venv .venv
   
   # On Windows
   venv\\Scripts\\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## 🛠️ Tech Stack

### Core Frameworks
- **[LangChain](https://python.langchain.com/)** - Framework for LLM application development
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - Library for building stateful, multi-actor applications
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework for building APIs

### LLM Providers
- **[OpenAI](https://openai.com/)** - GPT-4, GPT-3.5
- **[OpenRouter](https://openrouter.ai/)** - Access to multiple models (Qwen, DeepSeek, etc.)
- **[Ollama](https://ollama.ai/)** - Local model deployment (Mistral, Llama, DeepSeek)

### Vector Databases & Tools
- **[Qdrant](https://qdrant.tech/)** - High-performance vector database
- **[FAISS](https://github.com/facebookresearch/faiss)** - Efficient similarity search
- **[HuggingFace](https://huggingface.co/)** - Embeddings and model hub
- **[Tavily](https://tavily.com/)** - AI-optimized search API

## 🏗️ Architecture Patterns

### RAG Pattern (Examples 01, 05)
```
User Query → Embedding → Vector Search → Context Retrieval → LLM → Response
```

### Agent Pattern (Examples 04, 07)
```
User Input → Agent (Reasoning) → Tool Selection → Tool Execution → Agent (Response)
```

### Multi-Agent Pattern (Example 11)
```
User Request → Supervisor Agent → Worker Agents (Research/Chat) → Aggregated Response
```

## 🔧 Development Setup

### Running Vector Database (Qdrant)
```bash
docker run --publish 6333:6333 \\
  --volume /path/to/qdrant_storage:/qdrant/storage \\
  qdrant/qdrant
```

### LangSmith Setup (Recommended)
```bash
export LANGSMITH_API_KEY="your-key"
export LANGSMITH_TRACING_V2=true
export LANGSMITH_PROJECT="ai-integration-examples"
```

## 📊 Project Structure

```
ai-integration-examples/
├── examples/                    # All learning examples
│   ├── 01-fastapi-basics/      # FastAPI + RAG basics
│   ├── 02-langchain-prompts/   # Prompt engineering
│   ├── ...                     # Other examples
│   └── 11-multiagent-system/   # Advanced multi-agent
├── core/                        # Shared utilities
├── tests/                       # Test templates (separate project)
├── .env.example                 # Environment template
├── pyproject.toml              # Project dependencies
├── requirements.txt            # Pip dependencies
└── README.md                   # This file
```

## 🤝 Contributing

This is a personal learning repository, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new example'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the amazing framework
- [LangChain Academy](https://academy.langchain.com/) for educational resources
- The open-source AI community
