import json
import os
import warnings
from typing import List, Dict, Optional
import argparse
import asyncio
import requests
from tenacity import retry, stop_after_attempt, wait_random



import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from openai import AsyncOpenAI


parser = argparse.ArgumentParser(description="Launch perplexity server.")
parser.add_argument("--pplx_key", type=str, default="", help="Perplexity key.")


args = parser.parse_args()

client = AsyncOpenAI(api_key=args.pplx_key, base_url="https://api.perplexity.ai")

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {   
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]


# chat completion without streaming
response = client.chat.completions.create(
    model="sonar",
    messages=messages,
)

#####################################
# FastAPI server below
#####################################


class QueryRequest(BaseModel):
    queries: List[str]
    topk: Optional[int] = None
    return_scores: bool = False


app = FastAPI()

# 1) Build a config (could also parse from arguments).
#    In real usage, you'd parse your CLI arguments or environment variables.

# 2) Instantiate a global retriever so it is loaded once and reused.



@app.post("/retrieve")
async def retrieve_endpoint(request: QueryRequest):
    """
    Endpoint that accepts queries and performs retrieval.
    Input format:
    {
      "queries": ["What is Python?", "Tell me about neural networks."],
      "topk": 3,
      "return_scores": true
    }
    """
    if not request.topk:
        request.topk = 1  # fallback to default

    @retry(stop=stop_after_attempt(6), wait=wait_random(multiplier=1, max=5))
    async def make_pplx_call(query):
        messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {   
            "role": "user",
            "content": (
                f"{query}"
            ),
        },
        ]
        response = await client.chat.completions.create(
            model="sonar",
            messages=messages,
        )
        try:
            output = [{'document': {'contents': response.choices[0].message.content}, 'score': 1}]
        except Exception as e:
            print(e)
            output = [{'document': {'contents': "Issue searching resources. Please try again later."}, 'score': 1}]

        return output
    
    # each request can potentially have a list of queries
    # run the list of queries async
    print(request.queries)
    
    async def get_pplx_responses(request):    
        query_tasks = []
        for query in request.queries:
            query_tasks.append(asyncio.create_task(make_pplx_call(query)))
        gathered_responses = await asyncio.gather(*query_tasks)
        resp = []
        resp.extend(gathered_responses)
        return resp
    
    rr = await get_pplx_responses(request)
    return {"result": rr}


if __name__ == "__main__":
    # 3) Launch the server. By default, it listens on http://127.0.0.1:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)



