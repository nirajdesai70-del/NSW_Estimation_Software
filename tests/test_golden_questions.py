from __future__ import annotations
import pytest
from pathlib import Path
from ._helpers import REPO_ROOT, assert_exists

# Defer QueryService import until test execution to avoid pulling in
# sentence-transformers/torch dependencies during test collection
# (this test is marked @pytest.mark.full, so it only runs when requested)

# Golden questions - adjust path if your questions file is elsewhere
GOLDEN = REPO_ROOT / "tests" / "rag_regression_questions.yaml"

@pytest.mark.order(30)
@pytest.mark.full
def test_golden_file_exists():
    """Skip if golden questions file doesn't exist (optional test)"""
    if not GOLDEN.exists():
        pytest.skip(f"Golden questions file not found: {GOLDEN}")

@pytest.mark.order(31)
@pytest.mark.full
def test_golden_questions_return_citations():
    if not GOLDEN.exists():
        pytest.skip(f"Golden questions file not found: {GOLDEN}")
    
    # Skip if dependencies aren't available (will only run in "full" mode anyway)
    pytest.importorskip("sentence_transformers", reason="Requires sentence-transformers (full test mode)")
    pytest.importorskip("torch", reason="Requires torch (full test mode)")
    pytest.importorskip("faiss", reason="Requires faiss (full test mode)")
    from services.kb_query.query_service import QueryService
    
    import yaml
    svc = QueryService()

    data = yaml.safe_load(GOLDEN.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    assert len(questions) >= 3, "Need at least 3 golden questions."

    for q in questions[:3]:
        query = q["query"]
        out = svc.query(query_text=query, limit=10)
        assert "citations" in out and len(out["citations"]) >= 2, f"No citations for query: {query}"
        for c in out["citations"][:2]:
            assert c.get("kb_path"), f"Missing kb_path citation for query: {query}"
            assert c.get("authority"), f"Missing authority in citation for query: {query}"

@pytest.mark.order(32)
@pytest.mark.full
def test_policy_queries_surface_canonical():
    # Skip if dependencies aren't available (will only run in "full" mode anyway)
    pytest.importorskip("sentence_transformers", reason="Requires sentence-transformers (full test mode)")
    pytest.importorskip("torch", reason="Requires torch (full test mode)")
    pytest.importorskip("faiss", reason="Requires faiss (full test mode)")
    from services.kb_query.query_service import QueryService
    
    svc = QueryService()

    policy_queries = [
        "latest-only ingestion rule",
        "governance policies decision",
        "chat_mirror authority status",
    ]
    for q in policy_queries:
        out = svc.query(query_text=q, limit=10)
        auths = [c.get("authority", "WORKING").upper() for c in out.get("citations", [])]
        assert any(a == "CANONICAL" for a in auths), f"Expected CANONICAL in citations for policy query: {q}"

