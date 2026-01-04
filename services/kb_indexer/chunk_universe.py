"""
Chunk Universe Builder - Pure stdlib module for building chunk universes

This module contains pure functions for chunking text and building chunk universes
from manifests. It has no dependencies on FAISS, sentence-transformers, or any
external packages beyond the Python standard library.

This allows lite tests to import these functions without triggering heavy dependencies.
"""

import re
from pathlib import Path
from typing import Dict, List

# Chunking configuration (must match indexer.py)
MAX_CHUNK_SIZE = 1000  # Maximum characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks
MIN_CHUNK_LENGTH = 40  # Minimum chunk length to index (skip rule - must be symmetric for both indexes)


def chunk_text(text: str) -> List[str]:
    """
    Chunk text into smaller pieces for better search granularity
    
    Args:
        text: Text to chunk
        
    Returns:
        List of text chunks
    """
    # Remove metadata header if present
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.MULTILINE | re.DOTALL)
    
    # Simple chunking: split by paragraphs, then combine
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If adding this paragraph would exceed max size, save current chunk
        if current_chunk and len(current_chunk) + len(para) > MAX_CHUNK_SIZE:
            chunks.append(current_chunk)
            # Start new chunk with overlap (last part of previous chunk)
            overlap_start = max(0, len(current_chunk) - CHUNK_OVERLAP)
            current_chunk = current_chunk[overlap_start:] + "\n\n" + para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # If no chunks created (text was very short), return full text
    if not chunks:
        chunks = [text] if text else []
    
    return chunks


def build_chunk_universe(manifest: Dict, rag_kb_root: Path) -> List[Dict]:
    """
    Build ONE canonical chunk universe from manifest.
    
    This is a pure function with no external dependencies beyond stdlib.
    
    Args:
        manifest: Manifest dictionary with "files" list
        rag_kb_root: Path to RAG_KB root directory
        
    Returns:
        List of chunks with stable doc_id format: {kb_path}#chunk:{i}
        This is the single source of truth for both keyword and vector indexes.
    """
    chunks = []
    seen_doc_ids = set()
    
    files = manifest.get("files", [])
    
    for file_entry in files:
        kb_path_str = file_entry.get("kb_path", "")
        if not kb_path_str:
            continue
        
        # Resolve kb_path (may be relative to RAG_KB_ROOT)
        kb_file = rag_kb_root / kb_path_str
        if not kb_file.exists():
            continue
        
        try:
            # Read content
            content = kb_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        
        # Chunk once (this is the only place chunking happens)
        chunk_list = chunk_text(content)
        
        for i, chunk_content in enumerate(chunk_list):
            chunk_content = chunk_content.strip()
            
            # Skip rule (must be symmetric for both indexes)
            if len(chunk_content) < MIN_CHUNK_LENGTH:
                continue
            
            # Stable doc_id format
            doc_id = f"{kb_path_str}#chunk:{i}"
            
            # Prevent duplicates
            if doc_id in seen_doc_ids:
                continue
            seen_doc_ids.add(doc_id)
            
            chunks.append({
                "doc_id": doc_id,
                "kb_path": kb_path_str,
                "source_path": file_entry.get("source_path", ""),
                "namespace": file_entry.get("namespace", ""),
                "authority": file_entry.get("authority", "WORKING"),
                "last_modified": file_entry.get("last_modified", ""),
                "text": chunk_content,
            })
    
    return chunks

