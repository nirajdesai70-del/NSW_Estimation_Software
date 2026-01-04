"""
Vector Index Module - Embedding-based semantic search

This module implements vector/embedding indexing for semantic similarity search
using FAISS for local, fast vector search with sentence-transformers for embeddings.
"""

from pathlib import Path
from typing import Dict, List, Optional
import json
import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class VectorIndex:
    """Vector/embedding index for semantic search using FAISS"""

    def __init__(self, index_path: Path, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector index
        
        Args:
            index_path: Path to store index files
            model_name: Sentence transformer model name (default: all-MiniLM-L6-v2)
        """
        self.index_path = index_path
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.model_name = model_name
        
        # FAISS index and metadata
        self.index = None
        self.dimension = 384  # Default for all-MiniLM-L6-v2
        self.metadata_file = index_path.parent / f"{index_path.name}.metadata.json"
        self.metadata = {}  # Maps FAISS ID to document metadata
        self.doc_id_to_faiss_id = {}  # Maps doc_id to FAISS ID (for duplicate prevention)
        
        # Embedding model
        self.encoder = None
        
    def _load_encoder(self):
        """Load the sentence transformer model"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            )
        
        if self.encoder is None:
            self.encoder = SentenceTransformer(self.model_name)
            # Get actual dimension from model
            self.dimension = self.encoder.get_sentence_embedding_dimension()

    def initialize(self, dimension: Optional[int] = None):
        """
        Initialize the FAISS index
        
        Args:
            dimension: Embedding dimension (auto-detected from model if None)
        """
        if not FAISS_AVAILABLE:
            raise ImportError(
                "faiss not installed. "
                "Install with: pip install faiss-cpu (or faiss-gpu)"
            )
        
        if dimension:
            self.dimension = dimension
        
        # Use IndexFlatIP (Inner Product) for cosine similarity
        # We'll normalize vectors for cosine similarity
        self.index = faiss.IndexFlatIP(self.dimension)
        self._load_encoder()
        self._load_metadata()

    def _normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        """Normalize vector for cosine similarity"""
        norm = np.linalg.norm(vector)
        if norm > 0:
            return vector / norm
        return vector

    def _load_metadata(self):
        """Load metadata from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                # Rebuild doc_id_to_faiss_id mapping
                self.doc_id_to_faiss_id = {}
                for faiss_id_str, meta in self.metadata.items():
                    doc_id = meta.get('doc_id', '')
                    if doc_id:
                        self.doc_id_to_faiss_id[doc_id] = int(faiss_id_str)
            except Exception:
                self.metadata = {}
                self.doc_id_to_faiss_id = {}

    def _save_metadata(self):
        """Save metadata to disk"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def add_document(self, doc_id: str, embedding: List[float], metadata: Dict):
        """
        Add a document embedding to the index
        
        Args:
            doc_id: Unique document identifier
            embedding: Document embedding vector
            metadata: Document metadata dict
        """
        if self.index is None:
            self.initialize()
        
        # Check if doc_id already exists (prevent duplicates)
        if doc_id in self.doc_id_to_faiss_id:
            # Document exists - we'll skip it (or could replace, but skip is safer during rebuild)
            # During rebuild, this shouldn't happen since we clear first
            return
        
        # Convert to numpy array and normalize
        vector = np.array(embedding, dtype=np.float32).reshape(1, -1)
        vector = self._normalize_vector(vector[0]).reshape(1, -1)
        
        # Add to FAISS index
        faiss_id = self.index.ntotal
        self.index.add(vector)
        
        # Store metadata and update mapping
        self.metadata[str(faiss_id)] = {
            'doc_id': doc_id,
            'file_path': metadata.get('file_path', ''),
            'namespace': metadata.get('namespace', ''),
            'authority': metadata.get('authority', 'WORKING'),
            'kb_path': metadata.get('kb_path', ''),
            'source_path': metadata.get('source_path', ''),
            'last_modified': metadata.get('last_modified', ''),
        }
        self.doc_id_to_faiss_id[doc_id] = faiss_id
        
        self._save_metadata()

    def search(
        self, 
        query_embedding: List[float], 
        namespace: Optional[str] = None,
        authority: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding vector
            namespace: Optional namespace filter
            authority: Optional authority filter
            limit: Max results to return
            
        Returns:
            List of dicts with document info and similarity score
        """
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Normalize query vector
        vector = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        vector = self._normalize_vector(vector[0]).reshape(1, -1)
        
        # Search in FAISS
        k = min(limit * 3, self.index.ntotal)  # Get more results for filtering
        scores, indices = self.index.search(vector, k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for invalid indices
                continue
            
            # Get metadata
            meta = self.metadata.get(str(idx), {})
            
            # Apply filters
            if namespace and meta.get('namespace') != namespace:
                continue
            if authority and meta.get('authority') != authority:
                continue
            
            results.append({
                'faiss_id': int(idx),
                'doc_id': meta.get('doc_id', ''),
                'file_path': meta.get('file_path', ''),
                'namespace': meta.get('namespace', ''),
                'authority': meta.get('authority', 'WORKING'),
                'kb_path': meta.get('kb_path', ''),
                'source_path': meta.get('source_path', ''),
                'last_modified': meta.get('last_modified', ''),
                'similarity': float(score),  # Cosine similarity (normalized inner product)
            })
            
            if len(results) >= limit:
                break
        
        return results

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using sentence-transformers
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        if self.encoder is None:
            self._load_encoder()
        
        # Generate embedding
        embedding = self.encoder.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def rebuild(self):
        """Rebuild the index (clear and reinitialize)"""
        if self.index:
            self.index.reset()
        self.metadata = {}
        self.doc_id_to_faiss_id = {}
        if self.metadata_file.exists():
            self.metadata_file.unlink()

    def save(self):
        """Save FAISS index to disk"""
        if self.index:
            faiss.write_index(self.index, str(self.index_path))
            self._save_metadata()

    def load(self):
        """Load FAISS index from disk"""
        if not self.index_path.exists():
            return False
        
        if not FAISS_AVAILABLE:
            raise ImportError("faiss not installed")
        
        self.index = faiss.read_index(str(self.index_path))
        self.dimension = self.index.d
        self._load_encoder()
        self._load_metadata()
        return True

    def get_stats(self) -> Dict:
        """Get index statistics"""
        count = self.index.ntotal if self.index else 0
        return {
            'document_count': count,
            'dimension': self.dimension,
            'model': self.model_name,
        }

