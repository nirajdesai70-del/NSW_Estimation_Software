from __future__ import annotations
import pytest
from pathlib import Path
from tests._helpers import REPO_ROOT, MANIFEST, assert_exists, load_json

# Import from pure stdlib module (safe for lite tests, no FAISS dependencies)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "services" / "kb_indexer"))
from chunk_universe import build_chunk_universe

@pytest.mark.order(1)
def test_manifest_exists():
    assert_exists(MANIFEST)

@pytest.mark.order(2)
def test_chunk_universe_no_duplicates():
    manifest = load_json(MANIFEST)
    rag_kb_root = REPO_ROOT / "RAG_KB"
    chunks = build_chunk_universe(manifest, rag_kb_root)

    assert len(chunks) > 0, "Chunk universe is empty; run kb_refresh + indexer first."

    doc_ids = [c["doc_id"] for c in chunks]
    assert len(doc_ids) == len(set(doc_ids)), "Duplicate doc_id detected in chunk universe."

@pytest.mark.order(3)
def test_chunk_universe_has_required_fields():
    manifest = load_json(MANIFEST)
    rag_kb_root = REPO_ROOT / "RAG_KB"
    chunks = build_chunk_universe(manifest, rag_kb_root)
    
    if len(chunks) == 0:
        pytest.skip("No chunks to test (run kb_refresh + indexer first)")
    
    required = {"doc_id", "kb_path", "source_path", "namespace", "authority", "last_modified", "text"}

    sample = chunks[0]
    missing = required - set(sample.keys())
    assert not missing, f"Chunk missing fields: {missing}"
    assert isinstance(sample["text"], str) and len(sample["text"].strip()) > 0

