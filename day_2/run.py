from pydantic import BaseModel, Field

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_ollama.llms import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig


class Paragraph(BaseModel):
    original_paragraph: str = Field(description="The original paragraph")
    edited_paragraph: str = Field(description="The improved edited paragraph")
    feedback: str = Field(description="Constructive feedback on the original paragraph")


llm = OllamaLLM(
    model="mistral",
    temperature=0.7,
    streaming=True,
    callbacks=[
        StreamingStdOutCallbackHandler(),
    ],
)
structured_llm = llm.with_structured_output(Paragraph) # Ollama doesn't support this shit :(((

system_prompt = SystemMessagePromptTemplate.from_template(
    """Your name is Romaniollo. You are a specialist in python language development. You will receive the questions below, and you will give good structured
    answers, but also being funny and kind.""",
)

user_prompt = HumanMessagePromptTemplate.from_template(
    """I have a question:

    {question}
    
    Answer: """,
    input_valiables=["question"],
)

# We can merge our prompts into one with ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])

chain = (
    {
        "question": lambda x: x["user_question"], # this shit its just REMAPPING variables
    }
    | prompt
    | llm
)

result_1 = chain.invoke({"user_question": "Tell me shortly about OOP"})
# print(result_1)
