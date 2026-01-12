#!/usr/bin/env python3
"""
KB Indexer - Builds searchable indexes from RAG Knowledge Pack

This service reads from RAG_KB/phase5_pack/ and creates searchable indexes
for fast retrieval by the query service. Uses BM25 keyword search (SQLite FTS5)
and semantic search (FAISS + sentence-transformers).

Usage:
    python3 indexer.py [--rebuild] [--update] [--verbose]
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse

from keyword_index import KeywordIndex
from vector_index import VectorIndex
from chunk_universe import build_chunk_universe, chunk_text, MAX_CHUNK_SIZE, CHUNK_OVERLAP, MIN_CHUNK_LENGTH

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent
RAG_KB_ROOT = REPO_ROOT / "RAG_KB"
KB_PACK_ROOT = RAG_KB_ROOT / "phase5_pack"
CHAT_MIRROR_ROOT = REPO_ROOT / "RAG_KB" / "chat_mirror"
INDEX_ROOT = REPO_ROOT / "RAG_INDEX"


def wipe_index_artifacts(index_root: Path):
    """Wipe all index artifacts for clean rebuild"""
    targets = [
        index_root / "keyword_index.db",  # Old SQLite file (if exists)
        index_root / "keyword_index_metadata.json",  # New rank-bm25 metadata
        index_root / "vector_index.faiss",
        index_root / "vector_index.faiss.metadata.json",
        index_root / "embeddings.npy",
        index_root / "index_metadata.json",
    ]
    for t in targets:
        if t.exists():
            if t.is_file():
                t.unlink()
            elif t.is_dir():
                shutil.rmtree(t)




class KBIndexer:
    """Main indexer orchestrator"""

    def __init__(self, rebuild: bool = False, verbose: bool = False):
        self.rebuild = rebuild
        self.verbose = verbose
        self.index_root = INDEX_ROOT
        self.index_root.mkdir(parents=True, exist_ok=True)
        
        # Initialize index objects
        keyword_db_path = self.index_root / "keyword_index.db"
        vector_index_path = self.index_root / "vector_index.faiss"
        
        self.keyword_index = KeywordIndex(keyword_db_path)
        self.vector_index = VectorIndex(vector_index_path)
    
    def chunk_text(self, text: str) -> List[str]:
        """Wrapper for chunk_text function from chunk_universe module"""
        return chunk_text(text)

    def load_kb_manifest(self) -> Optional[Dict]:
        """Load the KB index manifest"""
        manifest_path = KB_PACK_ROOT / "00_INDEX.json"
        if not manifest_path.exists():
            print("Error: KB manifest not found. Run kb_refresh first.")
            return None

        with open(manifest_path, "r") as f:
            return json.load(f)

    def extract_metadata_header(self, content: str) -> Dict:
        """Extract metadata from YAML front matter"""
        metadata = {}
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.MULTILINE | re.DOTALL)
        if match:
            yaml_content = match.group(1)
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        return metadata

    def index_documents(self, manifest: Dict):
        """Index all documents from KB pack using single canonical chunk universe"""
        print("Indexing documents...")

        files = manifest.get("files", [])
        print(f"Found {len(files)} files to index")

        # Build ONE canonical chunk universe (single source of truth)
        chunks = build_chunk_universe(manifest, RAG_KB_ROOT)
        print(f"Built chunk universe: {len(chunks)} chunks")

        # Connect to keyword index
        with self.keyword_index:
            # Initialize keyword index tables
            if self.rebuild:
                self.keyword_index.rebuild()
            else:
                self.keyword_index.create_tables()
            
            # Initialize vector index
            if self.rebuild:
                self.vector_index.rebuild()
            
            try:
                self.vector_index.load()
                if self.verbose:
                    print("  Loaded existing vector index")
            except:
                self.vector_index.initialize()
            
            # Index chunks to keyword index (chunk universe already has no duplicates)
            for chunk in chunks:
                doc_id = chunk["doc_id"]
                
                # Build metadata dict
                doc_metadata = {
                    'filename': chunk["kb_path"].split('/')[-1],
                    'title': chunk["kb_path"].split('/')[-1],
                    'file_path': str(RAG_KB_ROOT / chunk["kb_path"]),
                    'namespace': chunk["namespace"],
                    'authority': chunk["authority"],
                    'kb_path': chunk["kb_path"],
                    'source_path': chunk["source_path"],
                    'last_modified': chunk["last_modified"],
                }
                
                # Add to keyword index (handles duplicates internally)
                self.keyword_index.add_document(doc_id, chunk["text"], doc_metadata)
            
            # Index same chunks to vector index
            for chunk in chunks:
                doc_id = chunk["doc_id"]
                
                # Build metadata dict (same as keyword)
                doc_metadata = {
                    'filename': chunk["kb_path"].split('/')[-1],
                    'title': chunk["kb_path"].split('/')[-1],
                    'file_path': str(RAG_KB_ROOT / chunk["kb_path"]),
                    'namespace': chunk["namespace"],
                    'authority': chunk["authority"],
                    'kb_path': chunk["kb_path"],
                    'source_path': chunk["source_path"],
                    'last_modified': chunk["last_modified"],
                }
                
                # Generate embedding and add to vector index (handles duplicates internally)
                try:
                    embedding = self.vector_index.generate_embedding(chunk["text"])
                    self.vector_index.add_document(doc_id, embedding, doc_metadata)
                except Exception as e:
                    if self.verbose:
                        print(f"    Warning: Failed to generate embedding for {doc_id}: {e}")
            
            # Save vector index
            self.vector_index.save()
            
            print(f"  Indexed {len(chunks)} chunks from {len(files)} files")

    def save_index_metadata(self, manifest: Dict):
        """Save index metadata alongside KB version"""
        from datetime import datetime
        
        # Get stats from indexes
        keyword_stats = {}
        vector_stats = {}
        
        with self.keyword_index:
            keyword_stats = self.keyword_index.get_stats()
        
        try:
            vector_stats = self.vector_index.get_stats()
        except:
            pass
        
        metadata = {
            "kb_version": manifest.get("version"),
            "kb_last_refresh": manifest.get("last_refresh"),
            "index_version": "1.0",
            "index_timestamp": datetime.now().isoformat(),
            "file_count": len(manifest.get("files", [])),
            "keyword_index": keyword_stats,
            "vector_index": vector_stats,
            "indexing_config": {
                "chunk_size": MAX_CHUNK_SIZE,
                "chunk_overlap": CHUNK_OVERLAP,
                "min_chunk_length": MIN_CHUNK_LENGTH,
                "keyword_doc_count": keyword_stats.get("document_count", 0),
                "vector_doc_count": vector_stats.get("document_count", 0),
            },
        }

        metadata_path = self.index_root / "index_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def run(self):
        """Execute indexing process"""
        print("=" * 60)
        print("KB Indexer")
        print("=" * 60)

        manifest = self.load_kb_manifest()
        if not manifest:
            print("Cannot proceed without KB manifest")
            return

        print(f"KB Version: {manifest.get('version')}")
        print(f"KB Last Refresh: {manifest.get('last_refresh')}")
        print()

        if self.rebuild:
            print("Rebuilding all indexes...")
            print("Wiping existing index artifacts...")
            wipe_index_artifacts(self.index_root)
            print()

        # Index documents (this handles both keyword and vector)
        self.index_documents(manifest)

        # Save metadata
        self.save_index_metadata(manifest)

        print()
        print("=" * 60)
        print("Indexing Complete!")
        print("=" * 60)
        
        # Print stats
        with self.keyword_index:
            stats = self.keyword_index.get_stats()
            print(f"Keyword Index: {stats['document_count']} documents")
        
        try:
            stats = self.vector_index.get_stats()
            print(f"Vector Index: {stats['document_count']} documents")
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description="Index RAG Knowledge Pack")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild all indexes")
    parser.add_argument("--update", action="store_true", help="Incremental update (not yet implemented)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    indexer = KBIndexer(rebuild=args.rebuild, verbose=args.verbose)
    indexer.run()


if __name__ == "__main__":
    main()

