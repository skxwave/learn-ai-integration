import asyncio
import json

from twscrape import API, gather


async def parse():
    api = API()

    raw_result = await gather(api.search(
        q="ethereum OR crypto OR ETH",
        limit=20,
    ))
    result = [tweet.dict() for tweet in raw_result]

    print(result)

    with open("eth_tweets.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, default=str)
    
    return result


if __name__ == "__main__":
    asyncio.run(parse())
