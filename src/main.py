from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Redis vector demo is up!'}
