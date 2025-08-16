from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from langchain.docstore.document import Document
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

client = QdrantClient(host="localhost", port=6333)
# client.create_collection(
#     collection_name="qdrant_langchain_collection",
#     vectors_config=VectorParams(size=384, distance=Distance.COSINE),
# )
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Qdrant(
    client=client,
    collection_name="qdrant_langchain_collection",
    embeddings=embeddings,
)
docs = [
    Document(page_content="The capital of France is Paris."),
    Document(page_content="Python is a programming language."),
    Document(page_content="Qdrant is a vector database."),
]
vectorstore.add_documents(docs)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = ChatOllama(
    temperature=0.5,
    model="deepseek-r1:8b",
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
question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

query = "What is python?"
result = chain.invoke({"input": query})

print("Answer:", result)
