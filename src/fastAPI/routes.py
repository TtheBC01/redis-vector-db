from fastapi import APIRouter, HTTPException
from .utilities import pull_model, list_models, store_embeddings, query_embeddings
from .models import DocumentPayload

from redis import Redis
from rq import Queue

redis_client = Redis.from_url('redis://redis-server:6379')
redis_queue = Queue(connection=redis_client)

router = APIRouter()

@router.get('/load-model/')
async def load_model(model: str):
    try:
        # Attempt to pull the model
        pull_model(model=model)
        return {"model": model, "status": "success"}
    except Exception as e:
        # Handle any other unexpected exceptions
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.get('/available-models/')
async def get_models():
    try:
        models = list_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.post('/embed/')
async def create_embedding(documentpayload: DocumentPayload):
    try:
        response, keys = store_embeddings(documentpayload=documentpayload)
        return {"response": response, "keys": keys}
        # job = redis_queue.enqueue(store_embeddings, documentpayload)
        # return {"job_id": job.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.get('/search/')
async def search_embeddings(documentpayload: DocumentPayload):
    try:
        results = query_embeddings(documentpayload=documentpayload)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")