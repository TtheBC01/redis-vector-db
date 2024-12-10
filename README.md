# Redis vector store demo

This repo spins up a minimal docker stack that leverages [Redis](https://redis.io/) + [RedisVL](https://redis.io/docs/latest/integrate/redisvl/) as a vector database for calculating semantic similarity between text strings.

The stack defined in `docker-compose.yaml` creates an instance for Redis (for storing vector embeddings), [Ollama](https://ollama.com/) (for creating embeddings), and [FastAPI](https://fastapi.tiangolo.com/) (as a simple "business logic" gateway). 

## 1. Buid the FastAPI gateway

First you'll need to build the FastAPI server application in the `/src` directory:

```sh
git clone https://github.com/TtheBC01/redis-vector-db.git
cd redis-vector-db
docker build -t vector-gateway ./src
```

## 2. Run the stack

Once you've successfully build the server application and tagged it as `vector-gateway`, bring the stack up:

```sh
docker compose up -d
```

You should have 3 services up: `python-fastapi`, `redis-server`, and `ollama-service`. If you visit `http://localhost:8000`, you should get 

```sh
{"message":"Redis vector demo is up!"}
```

## 3. Pull an embedding model 

You'll need to download an embedding model in order to build a queryable vector store. Run the following command to pull [Nomic's](https://www.nomic.ai/) open source embedding model:

```sh
curl -X GET http://localhost:8000/load-model/?model=nomic-embed-text
```

This model embeds text strings into a 768-dimensional vector field. There are other embedding models offered by Ollama too. Check the models you have cached by running:

```sh
curl -X GET http://localhost:9000/available-models/
```

## 4. Embed some text

Try embedding some text and storing it in your Redis instance like this:

```sh
curl -X POST http://localhost:8000/embed/ -H "Content-Type: application/json" -d '{"payload": ["Paris is the capital of France.", "The dog ran after the cat.", "What day of the week is it?"]}'
```

You can embed many many "documents" at once, but if your text blob is longer than the context size of your embedding model, any text over the limit will be ignored by the model. If this is your situation, you'll need to "chunk" you documents appropriately. For reference, the `nomic-embed-text` model has a context size of 8196 tokens. 

## 5. Check similarity

Now that your Redis instance has some vectors loaded, try to query it:

```sh
curl -X GET http://localhost:8000/search/ -H "Content-Type: application/json" -d '{"payload": "Where is Paris?"}'
```

You'll get the top 3 documents that match your query string in order of relevance as well as their vector distance (computed using cosine similarity).