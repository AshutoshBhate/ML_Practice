# What this Self-RAG API actually does
#
# On startup (lifespan in this file, initialize() in rag.py):
#   Scrapes 4 Cohere docs pages (only their <article> part), splits them into 256-token chunks,
#   embeds them with text-embedding-3-small and saves them in a local Qdrant database (./qdrant_db).
#   Later starts find ./qdrant_db and skip the scraping.
#
# On every POST /ask, a LangGraph graph runs:
#   1. retrieve: Fetches the 5 chunks closest to the question.
#   2. is_relevant (the conditional edge): An LLM grader (GradeDocuments) labels the chunks "yes" or "no"
#      one at a time, and stops at the first "yes".
#   3. If a chunk passed, generate: gpt-4o-mini answers from all 5 chunks, or says it doesn't know.
#      If none passed, rewrite: The LLM rewrites the question for a better search, and the graph goes
#      back to retrieve. After 3 rewrites (rewrite_count), it generates anyway.
#
# So it's the first half of Self-RAG: It checks the retrieved chunks before answering, but it doesn't
# check the answer afterwards (no hallucination check and no "does it answer the question" check).
#
# Run it from this folder: uvicorn main:app

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from pydantic_models import QueryRequest, QueryResponse
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
app = FastAPI(title="Self-RAG API (LangGraph)", lifespan=lifespan)

# Basic GET command to resolve the error
@app.get("/")
async def greet():
    return {"message": "Welcome to the error free RAG API"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    try:
        # Pass the question to our RAG engine
        answer = rag_engine.ask(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))