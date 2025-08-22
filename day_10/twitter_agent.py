import json
import os
from typing import TypedDict

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


class State(TypedDict):
    input: str
    output: str


def format_tweets(tweets: list[dict[str | str]]) -> str:
    result = []

    for tweet in tweets[10:20]:
        tweet_str = f"""
Tweet by: {tweet["user"]["username"]} | {tweet["user"]["displayname"]}, user desc: {tweet["user"]["rawDescription"]}, followers: {tweet["user"]["followersCount"]}
Raw content: {tweet["rawContent"]}
Engagement: {tweet["replyCount"]} replies, {tweet["retweetCount"]} retweets, {tweet["likeCount"]} likes, {tweet["quoteCount"]}quotes
Date: {tweet["date"]}
Hashtags: {tweet["hashtags"]}
Cashtags: {tweet["cashtags"]}
"""
        result.append(tweet_str)

    return "\n\n".join(result)


def call_llm(state: State):
    with open("eth_tweets.json", encoding="utf-8") as file:
        raw_tweets = json.load(file)

    tweets = format_tweets(raw_tweets)

    prompt = f"""
Here is the list of tweets: 

{tweets}

Analyze all of them and give me the analize of cryptomarket for now.
"""

    system_message = SystemMessage(content="You are an expert in crypto, and you can analyze the market based on the latest news, such as tweets.")
    user_input = HumanMessage(content=prompt)

    result = llm.invoke([system_message, user_input])
    state["output"] = result.content
    return state


builder = StateGraph(State)
builder.add_node("llm", call_llm)
builder.set_entry_point("llm")
builder.set_finish_point("llm")

graph = builder.compile()
