FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including curl for healthcheck)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# CI-lite mode: install minimal deps for health checks only
# FULL mode: install full ML stack for production inference
ARG RAG_MODE=FULL

COPY services/kb_query/requirements.txt /app/services/kb_query/
COPY services/kb_indexer/requirements.txt /app/services/kb_indexer/

RUN if [ "$RAG_MODE" = "CI" ]; then \
      echo "CI-lite mode: installing minimal dependencies for health checks"; \
      pip install --no-cache-dir fastapi>=0.100.0 uvicorn[standard]>=0.23.0 pydantic>=2.0.0 requests; \
    else \
      echo "FULL mode: installing complete ML stack"; \
      pip install --no-cache-dir -r services/kb_query/requirements.txt && \
      pip install --no-cache-dir -r services/kb_indexer/requirements.txt; \
    fi

# Copy service code
COPY services/kb_query/ /app/services/kb_query/
COPY services/kb_indexer/ /app/services/kb_indexer/
COPY RAG_INDEX/ /app/RAG_INDEX/

EXPOSE 8099

CMD ["python3", "services/kb_query/query_server.py", "--port", "8099", "--host", "0.0.0.0"]

