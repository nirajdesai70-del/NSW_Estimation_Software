FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including curl for healthcheck)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/kb_query/requirements.txt /app/services/kb_query/
COPY services/kb_indexer/requirements.txt /app/services/kb_indexer/
RUN pip install --no-cache-dir -r services/kb_query/requirements.txt && \
    pip install --no-cache-dir -r services/kb_indexer/requirements.txt

# Copy service code
COPY services/kb_query/ /app/services/kb_query/
COPY services/kb_indexer/ /app/services/kb_indexer/
COPY RAG_INDEX/ /app/RAG_INDEX/

EXPOSE 8099

CMD ["python3", "services/kb_query/query_server.py", "--port", "8099", "--host", "0.0.0.0"]

