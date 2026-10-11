"""
Pydantic schemas for FastAPI validation.

Each class describes the exact shape of a JSON body. FastAPI uses them in two directions:
  * Request models (ChatRequest): incoming JSON is parsed and checked. A bad body
    (e.g. missing `thread_id`, or a 1-character question) is rejected with HTTP 422
    automatically, so app.py never sees invalid data.
  * Response models (ChatResponse, UploadResponse): whatever app.py returns is
    validated and converted to JSON with exactly these fields.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# Body of POST /api/chat, sent by static/app.js:
#   {"question": "...", "thread_id": "incident-..."}
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)  # `...` = required
    # Identifies the conversation; the SQLite memory is keyed by this value.
    thread_id: str = Field(..., min_length=3, max_length=120)


# One evidence item shown under an answer (a runbook chunk or a web page).
class SourceItem(BaseModel):
    type: Literal["internal", "web"]
    title: str = ""
    source: str = ""
    url: Optional[str] = None
    page: Optional[int] = None


# Response of POST /api/chat. static/app.js reads these fields to draw the answer and tags.
class ChatResponse(BaseModel):
    answer: str
    route: str
    used_web_search: bool
    support_status: str = ""
    usefulness: str = ""
    sources: List[SourceItem] = []
    trace: List[str] = []
    thread_id: str
    memory_turns: int = 0  # how many past turns are stored for this thread_id


# Response of POST /api/upload.
class UploadResponse(BaseModel):
    filename: str
    chunks_indexed: int
    namespace: str
