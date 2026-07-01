import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.backend.retriever import retrieve_facts
from src.backend.guardrails import check_query
from src.backend.generator import generate_response, format_final_reply
from src.backend.scheduler import start_ingestion_daemon
import asyncio

app = FastAPI(
    title="Facts-Only Mutual Fund FAQ Assistant",
    description="A lightweight RAG-based assistant for ICICI Prudential mutual fund schemes (referencing Groww context). Strictly facts-only, no investment advice.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    # Start automated daily ingestion background scheduler
    asyncio.create_task(start_ingestion_daemon())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    is_refused: bool
    answer: str
    citation_url: str
    last_updated: str
    footer: str
    scheme_referenced: str
    refusal_reason: str = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    # Step 1: Guardrails (Refusal & PII Check)
    guardrail_res = check_query(query)
    if guardrail_res.get("is_refused", False):
        reply = format_final_reply(guardrail_res, {})
        return ChatResponse(**reply)
        
    # Step 2: Retrieve Facts from Corpus
    retrieved_chunks = retrieve_facts(query, top_k=2)
    
    # Step 3: Generate Facts-Only Response
    gen_res = generate_response(query, retrieved_chunks)
    
    # Step 4: Format Final Reply
    reply = format_final_reply(guardrail_res, gen_res)
    return ChatResponse(**reply)

@app.get("/api/schemes")
async def get_schemes():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    corpus_path = os.path.join(base_dir, "data", "corpus.json")
    if os.path.exists(corpus_path):
        with open(corpus_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "amc": data.get("amc", ""),
                "reference_context": data.get("reference_context", ""),
                "schemes": data.get("schemes", []),
                "official_urls": data.get("official_urls", [])
            }
    return {"schemes": []}

@app.get("/api/examples")
async def get_examples():
    return {
        "examples": [
            "What is the expense ratio of ICICI Prudential Large Cap Fund?",
            "What is the exit load and minimum SIP amount for the Flexicap Fund?",
            "How can I download my Statement of Account or Capital Gains report?"
        ],
        "refusal_examples": [
            "Should I invest in ICICI Prudential Top 100 Fund?",
            "Which mutual fund is better for maximum returns?"
        ]
    }

# Mount static files for frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_index():
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend index.html not found. Please verify src/frontend exists."}

@app.get("/styles.css")
async def serve_styles():
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
    css_file = os.path.join(frontend_dir, "styles.css")
    if os.path.exists(css_file):
        return FileResponse(css_file, media_type="text/css")
    raise HTTPException(status_code=404, detail="styles.css not found")

@app.get("/app.js")
async def serve_js():
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
    js_file = os.path.join(frontend_dir, "app.js")
    if os.path.exists(js_file):
        return FileResponse(js_file, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="app.js not found")
