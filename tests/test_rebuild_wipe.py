from __future__ import annotations
import os
import time
import subprocess
from pathlib import Path
import pytest
from tests._helpers import REPO_ROOT, RAG_INDEX

KEYWORD_DB = RAG_INDEX / "keyword_index.db"
VECTOR_FAISS = RAG_INDEX / "vector_index.faiss"
VECTOR_META = RAG_INDEX / "vector_index.faiss.metadata.json"
INDEX_META = RAG_INDEX / "index_metadata.json"

@pytest.mark.order(10)
@pytest.mark.full
def test_rebuild_wipes_and_recreates_indexes():
    # Ensure index directory exists
    RAG_INDEX.mkdir(parents=True, exist_ok=True)
    
    # Touch files to simulate existing artifacts (only if they don't exist)
    for p in [KEYWORD_DB, VECTOR_FAISS, INDEX_META]:
        if not p.exists():
            p.write_text("dummy", encoding="utf-8")
        time.sleep(0.05)

    # Run rebuild (adjust command if your CLI differs)
    cmd = ["python3", "services/kb_indexer/indexer.py", "--rebuild"]
    res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)

    assert res.returncode == 0, f"Indexer rebuild failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"

    # After rebuild, real artifacts must exist and not be the dummy text
    assert KEYWORD_DB.exists(), "keyword_index.db not created after rebuild."
    assert VECTOR_FAISS.exists(), "vector_index.faiss not created after rebuild."
    assert INDEX_META.exists(), "index_metadata.json not created after rebuild."

    # keyword_index.db and vector_index.faiss are binary-ish; size should be > 0
    assert KEYWORD_DB.stat().st_size > 20, "keyword_index.db too small; wipe/rebuild likely failed."
    assert VECTOR_FAISS.stat().st_size > 20, "vector_index.faiss too small; wipe/rebuild likely failed."
    
    # index_metadata.json should be valid JSON, not "dummy"
    import json
    meta_content = INDEX_META.read_text(encoding="utf-8")
    assert meta_content != "dummy", "index_metadata.json was not regenerated"
    json.loads(meta_content)  # Should not raise

