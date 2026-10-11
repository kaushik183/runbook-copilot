# ---------------------------------------------------------------------------
# Runbook Copilot container image
#
# Build:  docker build -t runbook-copilot .
# Run:    docker compose up -d --build        (recommended, see docker-compose.yml)
# ---------------------------------------------------------------------------

# Small official Python image (Debian based). Works on both x86_64 and ARM (e.g. Oracle Ampere VMs).
FROM python:3.11-slim

# PYTHONDONTWRITEBYTECODE: don't create __pycache__ files inside the image
# PYTHONUNBUFFERED: print logs immediately (so `docker logs` shows them live)
# PIP_NO_CACHE_DIR: keep the image smaller
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first, in their own layer. Docker caches this step, so code-only
# changes rebuild in seconds instead of reinstalling every package.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code (files listed in .dockerignore, like .env and data/, are skipped).
COPY . .

# SQLite files (data/) and uploaded runbooks (uploads/) live here.
# docker-compose.yml mounts volumes on these folders so they survive container rebuilds.
RUN mkdir -p data uploads

# Port the app listens on. Hosts like Render inject their own PORT value; locally it stays 8000.
ENV PORT=8000
EXPOSE 8000

# Docker marks the container "unhealthy" if GET /api/health stops answering.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ[\"PORT\"]}/api/health', timeout=4)" || exit 1

# One uvicorn worker on purpose: the LangGraph graph and its SQLite connection live in
# process memory, and SQLite is happiest with a single writer process.
# Shell form (no [...]) so ${PORT} is expanded; `exec` lets uvicorn receive stop signals directly.
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT}
