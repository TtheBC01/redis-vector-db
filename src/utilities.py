from clients import ollama_client, redis_index
from models import NomicEmbedder, DocumentPayload
from redisvl.query import VectorQuery
import numpy as np

def pull_model(model: str):
    ollama_client.pull(model)

def list_models():
    response = ollama_client.list()
    return response.models

def store_embeddings(documentpayload: DocumentPayload):
    # embed the vectors using ollama inference service
    embeds = NomicEmbedder(documents=documentpayload)
    response = ollama_client.embed(model='nomic-embed-text', input=embeds.search_documents())
    # now zip the vectors with the input data and load into redis, embeddings must be converted to bytes
    data = [{"sentence": t, "embedding": np.array(v, dtype=np.float32).tobytes()} for t, v in zip(documentpayload.payload, response.embeddings)]
    keys = redis_index.load(data)
    return response, keys

def query_embeddings(documentpayload: DocumentPayload):
    # embed the vectors using ollama inference service
    embeds = NomicEmbedder(documents=documentpayload)
    response = ollama_client.embed(model='nomic-embed-text', input=embeds.query_documents())
    # now zip the vectors with the input data and load into redis
    query = VectorQuery(vector=response.embeddings[0], vector_field_name='embedding', return_fields=['sentence'])
    results = redis_index.query(query)
    return results