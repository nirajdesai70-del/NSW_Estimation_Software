FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/kb_indexer/requirements.txt /app/services/kb_indexer/
RUN pip install --no-cache-dir -r services/kb_indexer/requirements.txt

# Copy service code
COPY services/kb_indexer/ /app/services/kb_indexer/
COPY RAG_KB/ /app/RAG_KB/

# Create RAG_INDEX directory
RUN mkdir -p /app/RAG_INDEX

CMD ["python3", "services/kb_indexer/indexer.py"]

