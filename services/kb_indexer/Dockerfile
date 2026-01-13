FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# CI-lite mode: skip heavy ML dependencies (indexer not needed for CI health checks)
# FULL mode: install full ML stack for production indexing
ARG RAG_MODE=FULL

COPY services/kb_indexer/requirements.txt /app/services/kb_indexer/

RUN if [ "$RAG_MODE" = "CI" ]; then \
      echo "CI-lite mode: skipping indexer dependencies (not needed for health checks)"; \
      pip install --no-cache-dir requests; \
    else \
      echo "FULL mode: installing complete ML stack"; \
      pip install --no-cache-dir -r services/kb_indexer/requirements.txt; \
    fi

# Copy service code
COPY services/kb_indexer/ /app/services/kb_indexer/
COPY RAG_KB/ /app/RAG_KB/

# Create RAG_INDEX directory
RUN mkdir -p /app/RAG_INDEX

CMD ["python3", "services/kb_indexer/indexer.py"]

