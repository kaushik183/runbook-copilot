"""
FastAPI entry point for CloudOps Sentinel.

FastAPI in one paragraph: you create an `app` object, then decorate normal Python
functions with `@app.get(...)` / `@app.post(...)`. Each decorated function becomes
an HTTP endpoint. FastAPI reads the function's type hints to:
  * validate the incoming request (e.g. `payload: ChatRequest` -> JSON body must match),
  * convert the return value to JSON (shaped by `response_model=`),
  * auto-generate interactive docs at /docs.

Run locally:  uvicorn app:app --reload        (then open http://127.0.0.1:8000)
"""

from pathlib import Path
import shutil
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool


from src.models import ChatRequest, ChatResponse, UploadResponse
from src.self_rag import run_self_rag
from src.ingestion import ingest_file, namespace, SUPPORTED
from src.db import init_db, save_audit, latest_audits
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

ROOT = Path(__file__).resolve().parent
UPLOADS = ROOT / "uploads"
UPLOADS.mkdir(exist_ok=True)


# The application object. uvicorn looks this up via "app:app" (file app.py, variable app).
app = FastAPI(
    title="CloudOps Sentinel — Enterprise Incident Response Self-RAG Copilot",
    version="2.0.0",
    description="Self-RAG copilot for cloud operations, production troubleshooting, and incident-response runbooks.",
)
# Serve everything in ./static (app.js, styles.css) at URLs starting with /static/...
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")
# Jinja2 renders HTML files from ./templates (we only use it to return index.html).
templates = Jinja2Templates(directory=str(ROOT / "templates"))


# Runs once when the server starts: makes sure the SQLite audit table exists.
@app.on_event("startup")
def startup():
    init_db()


# GET / -> the chat UI. The browser then loads /static/app.js, which calls the /api/* endpoints below.
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


# GET /api/health -> simple liveness check (used by the Docker HEALTHCHECK).
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "cloudops-sentinel-self-rag"}


# POST /api/chat
# - `payload: ChatRequest` tells FastAPI to parse the JSON body into a ChatRequest
#   (src/models.py). Missing/invalid fields are rejected with a 422 before this code runs.
# - `response_model=ChatResponse` makes FastAPI validate and serialize what we return.
# - The function is `async`, but run_self_rag is slow, blocking code (many LLM calls),
#   so we push it onto a worker thread with run_in_threadpool. That keeps the server
#   free to handle other requests in the meantime.
@app.post("/api/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    try:
        # thread_id comes from the browser (localStorage) and selects which saved
        # conversation the SQLite memory should load. See src/self_rag.py -> run_self_rag.
        result = await run_in_threadpool(
            run_self_rag, payload.question.strip(), payload.thread_id.strip()
        )
        # Store a copy of every Q&A in the audit table (data/audit.db).
        await run_in_threadpool(save_audit, payload.question, result)
        return ChatResponse(**result)
    except Exception as e:
        # HTTPException turns into a JSON error: {"detail": "..."} with status 500.
        # static/app.js shows `detail` in the chat as "Request failed: ...".
        raise HTTPException(status_code=500, detail=str(e))


# POST /api/upload
# `file: UploadFile = File(...)` means "expect a multipart form with a field named file"
# (this is what the browser's FormData sends). Requires the python-multipart package.
@app.post("/api/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED:
        raise HTTPException(status_code=400, detail="Supported: PDF, TXT, MD, DOCX")
    # Path(...).name strips any directory parts, so "../../etc/x.md" can't escape uploads/.
    safe_name = Path(file.filename).name
    target = UPLOADS / safe_name
    with target.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        # Chunk + embed + upsert into Pinecone (blocking, so run it on a worker thread).
        count = await run_in_threadpool(ingest_file, target)
        return UploadResponse(
            filename=safe_name, chunks_indexed=count, namespace=namespace()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET /api/audits?limit=20 -> latest audit rows. `limit: int = 20` is read from the
# query string; FastAPI converts it to int (and rejects non-numbers) for us.
@app.get("/api/audits")
def audits(limit: int = 20):
    return latest_audits(min(max(limit, 1), 100))


# `python app.py` also works; it starts uvicorn on port 8000 with auto-reload.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
