from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from ollama import Client
import numpy as np

def pull_model(model: str):
    ollama_client = Client(host='http://ollama-service:11434')
    ollama_client.pull(model)

def list_models():
    ollama_client = Client(host='http://ollama-service:11434')
    response = ollama_client.list()
    return response.models

def store_embeddings(documentpayload):
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
    ollama_client = Client(host='http://ollama-service:11434')
    # embed the vectors using ollama inference service
    response = ollama_client.embed(model='nomic-embed-text', input=documentpayload.payload)
    # now zip the vectors with the input data and load into redis, embeddings must be converted to bytes
    data = [{"sentence": t, "embedding": np.array(v, dtype=np.float32).tobytes()} for t, v in zip(documentpayload.payload, response.embeddings)]
    keys = redis_index.load(data)
    return response, keys

def query_embeddings(documentpayload):
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
    ollama_client = Client(host='http://ollama-service:11434')
    # embed the vectors using ollama inference service
    response = ollama_client.embed(model='nomic-embed-text', input=documentpayload.payload)
    # now zip the vectors with the input data and load into redis
    query = VectorQuery(vector=response.embeddings[0], vector_field_name='embedding', return_fields=['sentence'])
    results = redis_index.query(query)
    return results