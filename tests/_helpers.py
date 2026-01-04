from __future__ import annotations
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAG_INDEX = REPO_ROOT / "RAG_INDEX"
KB_PACK = REPO_ROOT / "RAG_KB" / "phase5_pack"
MANIFEST = KB_PACK / "00_INDEX.json"
INDEX_META = RAG_INDEX / "index_metadata.json"

def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))

def assert_exists(p: Path):
    assert p.exists(), f"Missing required file: {p}"

