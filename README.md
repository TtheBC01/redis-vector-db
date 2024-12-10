# Redis vector store demo

Short example of how to use Redis as a vector database with ollama for embeddings. 

## Buid the fastAPI gateway

First you'll need to build the server application in the `/src` directory:

```sh
cd src
docker build -t vector-gateway .
```

## Run the stack

Once you've successfully build the server application and tagged it as `vector-gateway`, bring the stack up:

```sh
docker compose up -d
```

You should have 3 services up; the fastAPI server, redis stack server, and ollama service. 

## Embed some text

```sh
curl -X POST http://localhost:8000/embed/ -H "Content-Type: application/json" -d '{"payload": ["Paris is the capital of France.", "The dog ran after the cat.", "What day of the week is it?"]}'
```