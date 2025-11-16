from langchain.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_ollama import ChatOllama


llm = ChatOllama(
    temperature=0.5,
    model="mistral",
    base_url="http://localhost:11434",
)
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are funny helpful assistant, and like to answer to questions with a dark jokes"
)
user_prompt = HumanMessagePromptTemplate.from_template(
    "I have a question to you: {user_question}. Give me an answer to it like you always do",
    input_valiables=["question"],
)
prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])
chain = prompt | llm
result = chain.invoke({"user_question": "What is python?"})

if __name__ == "__main__":
    print(result.content)
