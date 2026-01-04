from __future__ import annotations
import pytest
from ._helpers import MANIFEST, INDEX_META, assert_exists, load_json, REPO_ROOT

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "services" / "kb_indexer"))
from chunk_universe import build_chunk_universe

@pytest.mark.order(20)
@pytest.mark.full
def test_index_metadata_exists():
    assert_exists(INDEX_META)

@pytest.mark.order(21)
@pytest.mark.full
def test_keyword_vector_counts_match_chunk_universe():
    manifest = load_json(MANIFEST)
    rag_kb_root = REPO_ROOT / "RAG_KB"
    chunks = build_chunk_universe(manifest, rag_kb_root)
    chunk_count = len(chunks)

    meta = load_json(INDEX_META)

    kw = meta.get("indexing_config", {}).get("keyword_doc_count")
    vec = meta.get("indexing_config", {}).get("vector_doc_count")

    assert isinstance(kw, int) and kw > 0, f"Invalid keyword_doc_count: {kw}"
    assert isinstance(vec, int) and vec > 0, f"Invalid vector_doc_count: {vec}"

    assert kw == vec, f"Mismatch: keyword_doc_count={kw} vs vector_doc_count={vec}"
    assert kw == chunk_count, f"Mismatch: chunk_universe={chunk_count} vs keyword_doc_count={kw}"

