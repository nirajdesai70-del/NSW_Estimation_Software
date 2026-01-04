"""
KB Query Service - Fast query API for RAG Knowledge Base

This service provides query endpoints that read from RAG_INDEX/
and return answers with citations. Uses hybrid search combining
BM25 keyword search and semantic vector search.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add kb_indexer directory to path to import index modules
KB_INDEXER_DIR = Path(__file__).parent.parent / "kb_indexer"
if str(KB_INDEXER_DIR) not in sys.path:
    sys.path.insert(0, str(KB_INDEXER_DIR))

from keyword_index import KeywordIndex
from vector_index import VectorIndex


class QueryService:
    """Main query service with hybrid search"""

    def __init__(self, index_root: Optional[Path] = None):
        """
        Initialize query service
        
        Args:
            index_root: Path to RAG_INDEX/ (defaults to REPO_ROOT/RAG_INDEX)
        """
        REPO_ROOT = Path(__file__).parent.parent.parent
        self.index_root = index_root or (REPO_ROOT / "RAG_INDEX")
        
        # Initialize index objects
        keyword_db_path = self.index_root / "keyword_index.db"
        vector_index_path = self.index_root / "vector_index.faiss"
        
        self.keyword_index = KeywordIndex(keyword_db_path)
        self.vector_index = VectorIndex(vector_index_path)
        
        # Load indexes
        self._load_indexes()

    def _load_indexes(self):
        """Load keyword and vector indexes"""
        # Vector index needs to be loaded explicitly
        try:
            self.vector_index.load()
        except Exception as e:
            print(f"Warning: Could not load vector index: {e}")
            # Vector index will be initialized on first use

    def _normalize_score(self, score: float, min_score: float, max_score: float) -> float:
        """Normalize score to 0-1 range"""
        if max_score == min_score:
            return 1.0
        return (score - min_score) / (max_score - min_score)

    def _merge_results(
        self, 
        keyword_results: List[Dict], 
        vector_results: List[Dict],
        keyword_weight: float = 0.4,
        vector_weight: float = 0.6
    ) -> List[Dict]:
        """
        Merge keyword and vector results with hybrid ranking
        
        Args:
            keyword_results: Results from keyword search (BM25 scores)
            vector_results: Results from vector search (similarity scores)
            keyword_weight: Weight for keyword scores (default 0.4)
            vector_weight: Weight for vector scores (default 0.6)
            
        Returns:
            Merged and ranked results
        """
        # Normalize scores
        if keyword_results:
            keyword_scores = [r.get('rank', 0) for r in keyword_results]
            # rank-bm25 scores are positive (higher is better)
            min_kw, max_kw = min(keyword_scores), max(keyword_scores)
            for r in keyword_results:
                # Normalize BM25 score (higher is better)
                r['normalized_keyword_score'] = self._normalize_score(r['rank'], min_kw, max_kw)
        else:
            for r in keyword_results:
                r['normalized_keyword_score'] = 0.0
        
        if vector_results:
            vector_scores = [r.get('similarity', 0) for r in vector_results]
            min_vec, max_vec = min(vector_scores), max(vector_scores)
            for r in vector_results:
                r['normalized_vector_score'] = self._normalize_score(r['similarity'], min_vec, max_vec)
        else:
            for r in vector_results:
                r['normalized_vector_score'] = 0.0
        
        # Combine results by doc_id
        combined = {}
        
        # Add keyword results
        for r in keyword_results:
            doc_id = r.get('source_path', '') + r.get('kb_path', '')
            combined[doc_id] = {
                **r,
                'keyword_score': r.get('normalized_keyword_score', 0.0),
                'vector_score': 0.0,
            }
        
        # Add/merge vector results
        for r in vector_results:
            doc_id = r.get('source_path', '') + r.get('kb_path', '')
            if doc_id in combined:
                combined[doc_id]['vector_score'] = r.get('normalized_vector_score', 0.0)
                # Update other fields if vector result has better info
                if r.get('similarity', 0) > combined[doc_id].get('similarity', 0):
                    combined[doc_id].update({
                        k: v for k, v in r.items() 
                        if k not in ['normalized_vector_score', 'similarity']
                    })
            else:
                combined[doc_id] = {
                    **r,
                    'keyword_score': 0.0,
                    'vector_score': r.get('normalized_vector_score', 0.0),
                }
        
        # Calculate hybrid scores
        for doc_id, result in combined.items():
            hybrid_score = (
                keyword_weight * result.get('keyword_score', 0.0) +
                vector_weight * result.get('vector_score', 0.0)
            )
            result['hybrid_score'] = hybrid_score
        
        # Sort by hybrid score (descending)
        merged = sorted(combined.values(), key=lambda x: x.get('hybrid_score', 0), reverse=True)
        
        return merged

    def _apply_ranking_boosts(self, results: List[Dict], query_text: str) -> List[Dict]:
        """
        Apply deterministic re-rank boosts: authority boost + namespace boost
        
        Authority boosts:
        - CANONICAL: +0.25
        - WORKING: +0.05
        - DRAFT: -0.10
        - DEPRECATED: -0.25
        
        Namespace boosts (for policy/governance queries):
        - Governance/master/decision/flags docs: +0.20
        """
        # Check if query is policy/governance-related
        policy_keywords = ["rule", "policy", "authority", "canonical", "decision", "promotion", "governance"]
        is_policy_query = any(keyword in query_text.lower() for keyword in policy_keywords)
        
        # Governance namespace patterns (exact path matches)
        governance_patterns = [
            "phase5_pack/04_RULES_LIBRARY/governance/",
            "RAG_RULEBOOK.md",
            "08_PROMOTION_WORKFLOW.md",
            "01_CANONICAL_MASTER.md",
            "02_DECISIONS_LOG.md",
            "03_FEATURE_FLAGS.md",
        ]
        
        boosted = []
        for result in results:
            # Start with existing hybrid score
            final_score = result.get("hybrid_score", result.get("rank", result.get("similarity", 0)))
            
            # Authority boost
            authority = result.get("authority", "WORKING").upper()
            if authority == "CANONICAL":
                final_score += 0.25
            elif authority == "WORKING":
                final_score += 0.05
            elif authority == "DRAFT":
                final_score -= 0.10
            elif authority == "DEPRECATED":
                final_score -= 0.25
            
            # Namespace boost (for policy queries)
            if is_policy_query:
                kb_path = result.get("kb_path", "")
                source_path = result.get("source_path", "")
                path_str = f"{kb_path} {source_path}"
                
                for pattern in governance_patterns:
                    if pattern in path_str:
                        final_score += 0.20
                        break  # Only apply once
            
            # Update result with boosted score
            result["boosted_score"] = final_score
            boosted.append(result)
        
        # Re-sort by boosted score (descending)
        boosted.sort(key=lambda x: x.get("boosted_score", 0), reverse=True)
        
        return boosted

    def query(
        self,
        query_text: str,
        namespace: Optional[str] = None,
        authority: Optional[str] = None,
        limit: int = 10,
    ) -> Dict:
        """
        Query the knowledge base using hybrid search
        
        Args:
            query_text: Query string
            namespace: Optional namespace filter (e.g., "phase5_docs")
            authority: Optional authority filter (e.g., "CANONICAL")
            limit: Max results to return
            
        Returns:
            Dict with answer, citations, and metadata
        """
        if not query_text.strip():
            return {
                "answer": "Please provide a query.",
                "citations": [],
                "kb_version": self._get_kb_version(),
                "index_version": self._get_index_version(),
            }
        
        # Perform keyword search
        keyword_results = []
        try:
            with self.keyword_index:
                keyword_results = self.keyword_index.search(
                    query_text,
                    namespace=namespace,
                    authority=authority,
                    limit=limit * 2  # Get more for merging
                )
        except Exception as e:
            print(f"Warning: Keyword search failed: {e}")
        
        # Perform vector search
        vector_results = []
        try:
            # Generate query embedding
            query_embedding = self.vector_index.generate_embedding(query_text)
            
            # Search
            vector_results = self.vector_index.search(
                query_embedding,
                namespace=namespace,
                authority=authority,
                limit=limit * 2  # Get more for merging
            )
        except Exception as e:
            print(f"Warning: Vector search failed: {e}")
        
        # Merge results
        merged_results = self._merge_results(keyword_results, vector_results)
        
        # Apply authority and namespace boosts (Step 5.4)
        boosted_results = self._apply_ranking_boosts(merged_results, query_text)
        
        # Take top results
        top_results = boosted_results[:limit]
        
        # Format citations
        citations = [self.format_citation(r) for r in top_results]
        
        # Generate simple answer (could be enhanced with LLM in future)
        answer_parts = []
        if top_results:
            answer_parts.append(f"Found {len(top_results)} relevant document(s):")
            for i, result in enumerate(top_results[:3], 1):  # Top 3
                answer_parts.append(
                    f"{i}. {result.get('title', result.get('filename', 'Document'))} "
                    f"({result.get('namespace', 'unknown')}, {result.get('authority', 'WORKING')})"
                )
        else:
            answer_parts.append("No relevant documents found.")
        
        return {
            "answer": "\n".join(answer_parts),
            "citations": citations,
            "kb_version": self._get_kb_version(),
            "index_version": self._get_index_version(),
            "result_count": len(top_results),
        }

    def _get_kb_version(self) -> str:
        """Get KB version from index metadata"""
        metadata_path = self.index_root / "index_metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    return metadata.get("kb_version", "unknown")
            except Exception:
                pass
        return "unknown"

    def _get_index_version(self) -> str:
        """Get index version from index metadata"""
        metadata_path = self.index_root / "index_metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    return metadata.get("index_version", "unknown")
            except Exception:
                pass
        return "unknown"

    def search_keyword(
        self, 
        query: str, 
        namespace: Optional[str] = None,
        authority: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Search using keyword index only"""
        with self.keyword_index:
            return self.keyword_index.search(query, namespace=namespace, authority=authority, limit=limit)

    def search_vector(
        self, 
        query: str,
        namespace: Optional[str] = None,
        authority: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Search using vector index only"""
        query_embedding = self.vector_index.generate_embedding(query)
        return self.vector_index.search(query_embedding, namespace=namespace, authority=authority, limit=limit)

    def format_citation(self, doc: Dict) -> Dict:
        """Format document as citation"""
        return {
            "file": doc.get("source_path", doc.get("file_path", "")),
            "kb_path": doc.get("kb_path", ""),
            "title": doc.get("title", doc.get("filename", "")),
            "authority": doc.get("authority", "WORKING"),
            "namespace": doc.get("namespace", ""),
            "last_modified": doc.get("last_modified", ""),
            "score": doc.get("hybrid_score", doc.get("rank", doc.get("similarity", 0))),
        }


def main():
    """CLI interface for query service"""
    import argparse

    parser = argparse.ArgumentParser(description="Query RAG Knowledge Base")
    parser.add_argument("query", help="Query string")
    parser.add_argument("--namespace", help="Filter by namespace")
    parser.add_argument("--authority", help="Filter by authority")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    args = parser.parse_args()

    service = QueryService()
    result = service.query(
        args.query,
        namespace=args.namespace,
        authority=args.authority,
        limit=args.limit,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

