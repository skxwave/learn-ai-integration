import os
from typing import List

from openai import OpenAI
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

with open("day_1/data/test.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()


def split_text(text: str, max_words: int = 100) -> List[str]:
    sentences = text.split(". ")
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len((chunk + sentence).split()) < max_words:
            chunk += sentence + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + ". "
    if chunk:
        chunks.append(chunk.strip())
    return chunks


chunks = split_text(raw_text)
chunk_embeddings = embed_model.encode(chunks).astype("float32")

index = faiss.IndexFlatL2(chunk_embeddings.shape[1])
index.add(chunk_embeddings)


def search_similar_chunks(query: str, k: int = 3) -> List[str]:
    query_embedding = embed_model.encode([query]).astype("float32")
    _, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]


def generate_answer(question: str) -> str:
    relevant_chunks = search_similar_chunks(question)
    context = "\n---\n".join(relevant_chunks)

    prompt = f"Answer the question based on the following context. Context: {context} Question: {question} Answer:"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    while True:
        user_q = input("\nAsk something about the document:\n> ")
        if user_q.lower() in ["exit", "quit"]:
            break

        answer = generate_answer(user_q)
        print("\n💬 Answer:\n", answer)
