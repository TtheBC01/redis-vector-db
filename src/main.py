from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from redisvl.index import SearchIndex
from redisvl.query import VectorQuery

from ollama import Client

import numpy as np

from typing import List

ollama_client = Client(
  host='http://ollama-service:11434',
)

redis_schema = {
    "index": {
        "name": "vectorizers",
        "prefix": "doc",
        "storage_type": "hash",
    },
    "fields": [
        {"name": "sentence", "type": "text"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "dims": 768,
                "distance_metric": "cosine",
                "algorithm": "flat",
            }
        }
    ]
}

redis_index = SearchIndex.from_dict(redis_schema)
redis_index.connect('redis://redis-server:6379')
redis_index.create(overwrite=True)

class TextPayload(BaseModel):
    payload: str | List[str]
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Redis vector demo is up!'}

@app.get('/load-model/')
async def load_model(model: str):
    try:
        # Attempt to pull the model
        ollama_client.pull(model)
        return {"model": model, "status": "success"}
    except Exception as e:
        # Handle any other unexpected exceptions
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@app.get('/available-models/')
async def get_models():
    try:
        response = ollama_client.list()
        return response.models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@app.post('/embed/')
async def create_embedding(textpayload: TextPayload):
    try:
        # embed the vectors using ollama inference service
        response = ollama_client.embed(model='nomic-embed-text', input=textpayload.payload)
        # now zip the vectors with the input data and load into redis, embeddings must be converted to bytes
        data = [{"sentence": t, "embedding": np.array(v, dtype=np.float32).tobytes()} for t, v in zip(textpayload.payload, response.embeddings)]
        keys = redis_index.load(data)
        return {"model": response.model, "duration": response.total_duration, "tokens": response.prompt_eval_count, "keys": keys}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@app.get('/search/')
async def search_embeddings(textpayload: TextPayload):
    try:
        print("Query:", textpayload.payload)
        # embed the vectors using ollama inference service
        response = ollama_client.embed(model='nomic-embed-text', input=textpayload.payload)
        # now zip the vectors with the input data and load into redis
        query = VectorQuery(vector=response.embeddings[0], vector_field_name='embedding', return_fields=['sentence'])
        results = redis_index.query(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")