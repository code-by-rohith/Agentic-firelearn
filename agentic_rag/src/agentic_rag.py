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
    """Tiny bag-of-words index for demo purposes."""

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

            norm = math.sqrt(sum(v * v for v in vec.values()))
            self.doc_vectors[doc.doc_id] = vec
            self.doc_norms[doc.doc_id] = norm

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

        norm = math.sqrt(sum(v * v for v in vec.values()))
        return vec, norm

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
            sim = self._dot(q_vec, d_vec) / (q_norm * d_norm)
            if sim > 0:
                scored.append(RetrievalResult(doc=doc, score=sim))

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]


class AgenticRAG:
    """
    Minimal agentic RAG loop:
    1) Plan query
    2) Retrieve
    3) Reflect and optionally expand query
    4) Answer with citations
    """

    def __init__(self, data_dir: Path) -> None:
        self.documents = self._load_documents(data_dir)
        self.index = SimpleVectorIndex(self.documents)

    @staticmethod
    def _load_documents(data_dir: Path) -> List[Document]:
        docs: List[Document] = []
        for txt in sorted(data_dir.glob("*.txt")):
            docs.append(Document(doc_id=txt.stem, text=txt.read_text(encoding="utf-8")))
        if not docs:
            raise ValueError(f"No .txt documents found in {data_dir}")
        return docs

    @staticmethod
    def _plan_query(user_query: str) -> str:
        # Placeholder planner. In production, use an LLM planner.
        return user_query.strip()

    @staticmethod
    def _expand_query_if_needed(original_query: str, first_pass: List[RetrievalResult]) -> str:
        if first_pass:
            return original_query
        expansions = {
            "auth": "authentication",
            "db": "database firestore",
            "rules": "security rules access control",
            "price": "cost optimization budget",
        }
        words = original_query.lower().split()
        extra = [expansions[w] for w in words if w in expansions]
        if not extra:
            return original_query
        return f"{original_query} {' '.join(extra)}"

    @staticmethod
    def _compose_answer(query: str, contexts: List[RetrievalResult]) -> str:
        if not contexts:
            return (
                "I could not find relevant context in the indexed documents. "
                "Try adding more domain documents or rephrasing the question."
            )

        top = contexts[0]
        snippets = []
        sources = []

        for item in contexts:
            short = " ".join(item.doc.text.strip().split()[:28])
            snippets.append(f"[{item.doc.doc_id}] {short}...")
            sources.append(item.doc.doc_id)

        summary = (
            f"Answer (grounded): Based on the indexed docs, for '{query}', "
            f"the strongest source is '{top.doc.doc_id}'.\n"
            f"Relevant context:\n- " + "\n- ".join(snippets) + "\n"
            f"Citations: {', '.join(sources)}"
        )
        return summary

    def ask(self, user_query: str, top_k: int = 3) -> str:
        planned_query = self._plan_query(user_query)
        first_pass = self.index.search(planned_query, top_k=top_k)

        refined_query = self._expand_query_if_needed(planned_query, first_pass)
        final_hits = first_pass if refined_query == planned_query else self.index.search(refined_query, top_k=top_k)

        return self._compose_answer(user_query, final_hits)


def run_cli() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    rag = AgenticRAG(data_dir=base_dir / "data")

    print("Agentic RAG demo. Type 'exit' to quit.")
    while True:
        query = input("\nYou> ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Bye.")
            break
        if not query:
            continue
        print(f"\nRAG> {rag.ask(query)}")


if __name__ == "__main__":
    run_cli()
