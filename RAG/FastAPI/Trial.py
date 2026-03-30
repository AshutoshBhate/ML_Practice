from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello_function():
    return {"message" : "Hello Dragon Warrior"}