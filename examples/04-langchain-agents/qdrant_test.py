from qdrant_client import QdrantClient
from qdrant_client import models

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.docstore.document import Document

client = QdrantClient(host="localhost", port=6333)
# client.recreate_collection(
#     collection_name="my_collection",
#     vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
# )

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Qdrant(
    client=client,
    collection_name="my_collection",
    embeddings=embedding_model
)
docs = [
    Document(page_content="The capital of France is Paris."),
    Document(page_content="Python is a programming language."),
    Document(page_content="Qdrant is a vector database.")
]
vectorstore.add_documents(docs)


def insert_into_db():
    texts = ["Here", "is", "the", "text", "chunks.", "My", "name", "is", "Roman"]

    vectors = embedding_model.embed_documents(texts)

    points = [
        models.PointStruct(id=i, vector=vectors[i], payload={"text": texts[i]})
        for i in range(len(texts))
    ]
    client.upsert(collection_name="my_collection", points=points)


def get_from_db(query):
    query_vector = embedding_model.embed_query(query)

    results = client.search(
        collection_name="my_collection",
        query_vector=query_vector,
        limit=3, # get 3 results
    )

    for r in results:
        print(r.payload["text"], "score:", r.score)


if __name__ == "__main__":
    # insert_into_db()
    get_from_db("whats my name")
