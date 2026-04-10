from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from models import QueryRequest, QueryResponse
from rag import rag_engine

# Load environment variables
load_dotenv(override= True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing RAG Pipeline (Scraping & Embedding)...")
    rag_engine.initialize()
    print("RAG Pipeline Ready!")
    yield
    print("Shutting down API...")

# Initialize FastAPI app
app = FastAPI(title="Naive RAG API", lifespan=lifespan)

# Basic GET command to resolve the error
@app.get("/")
async def greet():
    return {"message": "Welcome to the error free RAG API"}

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        # Pass the question to our RAG engine
        answer = rag_engine.ask(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))