from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Document:
    doc_id: str
    text: str


@dataclass
class RetrievalResult:
    doc: Document
    score: float


class SimpleVectorIndex:
    def __init__(self, documents: List[Document]) -> None:
        self.documents = documents
        self.doc_vectors: Dict[str, Dict[str, float]] = {}
        self.doc_norms: Dict[str, float] = {}
        self.idf: Dict[str, float] = {}
        self._build()

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def _build(self) -> None:
        corpus_tokens = [self._tokenize(d.text) for d in self.documents]
        df: Dict[str, int] = {}

        for tokens in corpus_tokens:
            for token in set(tokens):
                df[token] = df.get(token, 0) + 1

        n_docs = len(self.documents)
        self.idf = {
            token: math.log((1 + n_docs) / (1 + freq)) + 1.0 for token, freq in df.items()
        }

        for doc, tokens in zip(self.documents, corpus_tokens):
            tf: Dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1

            vec: Dict[str, float] = {}
            for t, count in tf.items():
                vec[t] = (count / len(tokens)) * self.idf.get(t, 0.0)

            self.doc_vectors[doc.doc_id] = vec
            self.doc_norms[doc.doc_id] = math.sqrt(sum(v * v for v in vec.values()))

    def _embed_query(self, query: str) -> Tuple[Dict[str, float], float]:
        tokens = self._tokenize(query)
        if not tokens:
            return {}, 0.0

        tf: Dict[str, int] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1

        vec: Dict[str, float] = {}
        for t, count in tf.items():
            vec[t] = (count / len(tokens)) * self.idf.get(t, 0.0)

        return vec, math.sqrt(sum(v * v for v in vec.values()))

    @staticmethod
    def _dot(a: Dict[str, float], b: Dict[str, float]) -> float:
        if len(a) > len(b):
            a, b = b, a
        return sum(v * b.get(k, 0.0) for k, v in a.items())

    def search(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        q_vec, q_norm = self._embed_query(query)
        if q_norm == 0:
            return []

        scored: List[RetrievalResult] = []
        for doc in self.documents:
            d_vec = self.doc_vectors[doc.doc_id]
            d_norm = self.doc_norms[doc.doc_id]
            if d_norm == 0:
                continue

            score = self._dot(q_vec, d_vec) / (q_norm * d_norm)
            if score > 0:
                scored.append(RetrievalResult(doc=doc, score=score))

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]


def _load_documents(data_dir: Path) -> List[Document]:
    docs: List[Document] = []
    for txt in sorted(data_dir.glob("*.txt")):
        docs.append(Document(doc_id=txt.stem, text=txt.read_text(encoding="utf-8")))
    if not docs:
        raise ValueError(f"No .txt documents found in {data_dir}")
    return docs


_BASE_DIR = Path(__file__).resolve().parent.parent
_DOCS = _load_documents(_BASE_DIR / "data")
_INDEX = SimpleVectorIndex(_DOCS)


def plan_query(user_query: str) -> dict:
    """Plan retrieval query from user input."""
    planned = user_query.strip()
    return {
        "planned_query": planned,
        "strategy": "Use the direct query first. If empty results, expand with domain synonyms.",
    }


def refine_query_if_needed(user_query: str) -> dict:
    """Refine query with domain-specific expansions for second-pass retrieval."""
    expansions = {
        "auth": "authentication sign in provider",
        "db": "database firestore collections documents",
        "rules": "security rules request auth uid allow read write",
        "price": "cost optimization reads writes budget alerts",
        "hosting": "firebase hosting deployment",
    }

    parts = user_query.strip().split()
    extra = [expansions[p.lower()] for p in parts if p.lower() in expansions]
    refined = user_query if not extra else f"{user_query} {' '.join(extra)}"
    return {
        "refined_query": refined,
        "expanded": bool(extra),
    }


def retrieve_context(query: str, top_k: int = 3) -> dict:
    """Retrieve top-k context snippets from local knowledge files."""
    top_k = max(1, min(top_k, 8))
    hits = _INDEX.search(query, top_k=top_k)

    contexts = []
    for h in hits:
        snippet = " ".join(h.doc.text.split()[:36])
        contexts.append(
            {
                "source": h.doc.doc_id,
                "score": round(h.score, 4),
                "snippet": snippet,
            }
        )

    return {
        "query": query,
        "count": len(contexts),
        "contexts": contexts,
    }


def list_knowledge_sources() -> dict:
    """List all available indexed sources."""
    return {"sources": [d.doc_id for d in _DOCS], "count": len(_DOCS)}
