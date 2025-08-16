from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import CharacterTextSplitter
from qdrant_client import QdrantClient

from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

llm = ChatOllama(model="mistral", temperature=0.5)
client = QdrantClient(host="localhost", port=6333)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = QdrantVectorStore(
    embedding=embeddings,
    client=client,
    collection_name="qdrant_langchain_collection"
)
system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


def reset_collection():
    """Reset the Qdrant collection"""
    try:
        client.delete_collection(collection_name="qdrant_langchain_collection")
        print("Deleted existing collection")
    except:
        pass
    
    from qdrant_client.models import Distance, VectorParams
    client.create_collection(
        collection_name="qdrant_langchain_collection",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print("Created new collection")


def load_data_into_db():
    loader = TextLoader("test.txt")
    document = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    texts = text_splitter.split_documents(document)
    vectorstore.add_documents(texts)


def llm_chain(query: str):
    retriver = vectorstore.as_retriever()
    combined_docs_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )
    retrieval_chain = create_retrieval_chain(retriver, combined_docs_chain)
    return retrieval_chain.invoke({"input": query})


if __name__ == "__main__":
    # reset_collection()
    # load_data_into_db()
    result = llm_chain("tell me exactly the first row from document about Elon Musk")
    try:
        print(result["answer"])
    except:
        print(result)
