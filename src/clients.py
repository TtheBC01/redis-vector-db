from redisvl.index import SearchIndex
from ollama import Client

ollama_client = Client(host='http://ollama-service:11434')

redisvl_schema = {
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

redis_index = SearchIndex.from_dict(redisvl_schema)
redis_index.connect('redis://redis-server:6379')
redis_index.create(overwrite=True)