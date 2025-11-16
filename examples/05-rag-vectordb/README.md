# Example 05: RAG & Vector Database

Production-ready **RAG (Retrieval-Augmented Generation)** implementation using **Qdrant** vector database and **LangChain**.

## What You'll Learn

- Setting up Qdrant vector database
- Document loading and text splitting strategies
- Creating and managing vector collections
- Building retrieval chains with LangChain
- Production RAG patterns

## Files

- `rag_test.py` - Complete RAG implementation with Qdrant
- `test.txt` - Sample document for testing

## Running the Example

### 1. Start Qdrant Database
```bash
docker run --publish 6333:6333 \\
  --volume /path/to/qdrant_storage:/qdrant/storage \\
  qdrant/qdrant
```

### 2. Initialize the Database
```bash
python rag_test.py
# Uncomment these lines in main() first:
# reset_collection()
# load_data_into_db()
```

### 3. Query the System
```bash
python rag_test.py
# Comment out reset/load, keep the query line
```

## Key Features

### Vector Database Setup
- Create/delete collections
- Configure vector dimensions and distance metrics
- Manage embeddings efficiently

### Document Processing
- Load documents from files
- Split into chunks with overlap
- Generate embeddings with HuggingFace models

### Retrieval Chain
- Semantic search with vector similarity
- Context-aware response generation
- Concise answer formatting

## Technologies

- **Qdrant** - High-performance vector database
- **LangChain** - Framework for LLM applications
- **HuggingFace** - Embedding models
- **Ollama** - Local LLM (Mistral)

## Configuration

Required setup:
```bash
# Environment variables
# None required for Ollama local setup

# Qdrant connection
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

## Architecture

```
Document → TextLoader → CharacterTextSplitter → 
→ HuggingFaceEmbeddings → Qdrant VectorStore → 
→ Retriever → create_retrieval_chain → LLM Response
```

## Advanced Usage

### Custom Collection Settings
```python
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(
        size=384,  # Match embedding dimension
        distance=Distance.COSINE
    ),
)
```

### Optimizing Chunks
```python
text_splitter = CharacterTextSplitter(
    chunk_size=1000,      # Adjust for your use case
    chunk_overlap=100,    # Preserve context between chunks
)
```

## Next Steps

- Try Example 06 for LangGraph fundamentals
- Explore Example 04 for agent-based approaches
