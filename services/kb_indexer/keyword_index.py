"""
Keyword Index Module - rank-bm25 for fast keyword search

This module implements keyword/BM25 indexing using rank-bm25 library
for fast, accurate keyword search without requiring a database.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    from rank_bm25 import BM25Okapi
    RANK_BM25_AVAILABLE = True
except ImportError:
    RANK_BM25_AVAILABLE = False


class KeywordIndex:
    """rank-bm25-based keyword index with file-based persistence"""

    def __init__(self, index_path: Path):
        """
        Initialize keyword index
        
        Args:
            index_path: Path to store index files (will use .json for metadata)
        """
        self.index_path = index_path
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        # BM25 index
        self.bm25 = None
        self.corpus = []  # List of tokenized documents
        self.doc_ids = []  # List of doc_ids matching corpus indices
        self.metadata = {}  # Maps doc_id to document metadata
        
        # Metadata file
        self.metadata_file = index_path.parent / f"{index_path.stem}_metadata.json"
        
        # Dirty flag for deferred rebuild
        self._dirty = False
        
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization (split on whitespace, lowercase)"""
        return text.lower().split()
    
    def connect(self):
        """Connect/initialize index (no-op for file-based, kept for compatibility)"""
        self._load_metadata()
    
    def close(self):
        """Close index (rebuild if dirty, then save)."""
        if getattr(self, "_dirty", False):
            self.rebuild()
        else:
            self._save_metadata_atomic()
    
    def _load_metadata(self):
        """Load metadata from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                    self.metadata = data.get('metadata', {})
                    self.doc_ids = data.get('doc_ids', [])
                    self.corpus = data.get('corpus', [])
                    
                    # Normalize ordering to be deterministic
                    if self.doc_ids and self.corpus and len(self.doc_ids) == len(self.corpus):
                        pairs = sorted(zip(self.doc_ids, self.corpus), key=lambda x: x[0])
                        self.doc_ids = [p[0] for p in pairs]
                        self.corpus = [p[1] for p in pairs]
                    
                    # Rebuild BM25 index if we have corpus
                    if self.corpus:
                        self.bm25 = BM25Okapi(self.corpus)
            except Exception as e:
                self.metadata = {}
                self.doc_ids = []
                self.corpus = []
    
    def _save_metadata(self):
        """Save metadata to disk (legacy method, use _save_metadata_atomic)"""
        self._save_metadata_atomic()
    
    def _save_metadata_atomic(self):
        """Save metadata atomically to disk (write temp, fsync, rename)."""
        data = {
            'metadata': self.metadata,
            'doc_ids': self.doc_ids,
            'corpus': self.corpus,
            'updated_at': datetime.now().isoformat(),
        }
        
        tmp_file = self.metadata_file.with_suffix(self.metadata_file.suffix + ".tmp")
        with open(tmp_file, 'w') as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        
        tmp_file.replace(self.metadata_file)
    
    def create_tables(self):
        """Create/initialize index (no-op for file-based, kept for compatibility)"""
        if not RANK_BM25_AVAILABLE:
            raise ImportError(
                "rank-bm25 not installed. "
                "Install with: pip install rank-bm25"
            )
        if self.bm25 is None and self.corpus:
            self.bm25 = BM25Okapi(self.corpus)
    
    def add_document(self, doc_id: str, content: str, metadata: Dict):
        """
        Add a document to the index
        
        Args:
            doc_id: Unique document identifier
            content: Document text content
            metadata: Dict with title, file_path, namespace, authority, kb_path, source_path, last_modified
        """
        if not RANK_BM25_AVAILABLE:
            raise ImportError("rank-bm25 not installed")
        
        # Check if doc_id already exists (prevent duplicates)
        if doc_id in self.metadata:
            # Document exists - find and update
            try:
                idx = self.doc_ids.index(doc_id)
                # Update corpus and metadata
                self.corpus[idx] = self._tokenize(content)
                self.metadata[doc_id] = {
                    'title': metadata.get('title', metadata.get('filename', '')),
                    'file_path': metadata.get('file_path', ''),
                    'namespace': metadata.get('namespace', ''),
                    'authority': metadata.get('authority', 'WORKING'),
                    'kb_path': metadata.get('kb_path', ''),
                    'source_path': metadata.get('source_path', ''),
                    'last_modified': metadata.get('last_modified', ''),
                    'indexed_at': datetime.now().isoformat(),
                }
                # Mark index dirty; rebuild will occur in rebuild() / close()
                self._dirty = True
                return
            except ValueError:
                pass  # Not found, will add new
        
        # Add new document
        tokenized = self._tokenize(content)
        self.corpus.append(tokenized)
        self.doc_ids.append(doc_id)
        self.metadata[doc_id] = {
            'title': metadata.get('title', metadata.get('filename', '')),
            'file_path': metadata.get('file_path', ''),
            'namespace': metadata.get('namespace', ''),
            'authority': metadata.get('authority', 'WORKING'),
            'kb_path': metadata.get('kb_path', ''),
            'source_path': metadata.get('source_path', ''),
            'last_modified': metadata.get('last_modified', ''),
            'indexed_at': datetime.now().isoformat(),
        }
        
        # Mark index dirty; rebuild will occur in rebuild() / close()
        self._dirty = True
    
    def search(
        self, 
        query: str, 
        namespace: Optional[str] = None,
        authority: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search for documents matching query using BM25 ranking
        
        Args:
            query: Search query string
            namespace: Optional namespace filter
            authority: Optional authority filter
            limit: Max results to return
            
        Returns:
            List of dicts with document info and BM25 score
        """
        if self.bm25 is None or len(self.corpus) == 0:
            return []
        
        # Tokenize query
        query_tokens = self._tokenize(query)
        
        # Get BM25 scores
        scores = self.bm25.get_scores(query_tokens)
        
        # Create list of (score, index) pairs
        scored_docs = [(score, idx) for idx, score in enumerate(scores)]
        
        # Sort by score (descending)
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        
        # Apply filters and build results
        results = []
        for score, idx in scored_docs:
            if score <= 0:
                continue  # Skip zero/negative scores
            
            doc_id = self.doc_ids[idx]
            meta = self.metadata.get(doc_id, {})
            
            # Apply filters
            if namespace and meta.get('namespace') != namespace:
                continue
            if authority and meta.get('authority') != authority:
                continue
            
            results.append({
                'doc_id': doc_id,
                'title': meta.get('title', ''),
                'file_path': meta.get('file_path', ''),
                'namespace': meta.get('namespace', ''),
                'authority': meta.get('authority', 'WORKING'),
                'kb_path': meta.get('kb_path', ''),
                'source_path': meta.get('source_path', ''),
                'last_modified': meta.get('last_modified', ''),
                'rank': float(score),  # BM25 score (higher is better)
            })
            
            if len(results) >= limit:
                break
        
        return results
    
    def rebuild(self):
        """Rebuild BM25 index deterministically and persist state."""
        if not RANK_BM25_AVAILABLE:
            raise ImportError("rank-bm25 not installed")
        
        if not self.corpus or not self.doc_ids:
            self.bm25 = None
            self._dirty = False
            self._save_metadata_atomic()
            return
        
        # Enforce deterministic ordering by doc_id
        pairs = sorted(zip(self.doc_ids, self.corpus), key=lambda x: x[0])
        self.doc_ids = [p[0] for p in pairs]
        self.corpus = [p[1] for p in pairs]
        
        self.bm25 = BM25Okapi(self.corpus)
        self._dirty = False
        self._save_metadata_atomic()
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        return {
            'document_count': len(self.corpus),
            'namespace_count': len(set(m.get('namespace', '') for m in self.metadata.values())),
        }
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
