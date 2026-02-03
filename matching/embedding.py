from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

TOKEN_RE = re.compile(r"[\w\u3040-\u30ff\u4e00-\u9faf]+")


@dataclass(frozen=True)
class EmbeddingResult:
    score: float
    shared_terms: List[str]


class SimpleTfidfEmbedder:
    def __init__(self, documents: Iterable[str]) -> None:
        self._documents = list(documents)
        self._doc_count = len(self._documents)
        self._doc_freq = self._build_doc_freq(self._documents)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [token.lower() for token in TOKEN_RE.findall(text)]

    @staticmethod
    def _build_doc_freq(docs: Iterable[str]) -> Dict[str, int]:
        doc_freq: Dict[str, int] = {}
        for doc in docs:
            tokens = set(SimpleTfidfEmbedder._tokenize(doc))
            for token in tokens:
                doc_freq[token] = doc_freq.get(token, 0) + 1
        return doc_freq

    def _vectorize(self, text: str) -> Tuple[Dict[str, float], List[str]]:
        tokens = self._tokenize(text)
        counts = Counter(tokens)
        tfidf: Dict[str, float] = {}
        for token, count in counts.items():
            idf = math.log((1 + self._doc_count) / (1 + self._doc_freq.get(token, 0))) + 1
            tfidf[token] = (count / len(tokens)) * idf
        return tfidf, list(counts.keys())

    @staticmethod
    def _cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        if not vec_a or not vec_b:
            return 0.0
        dot = sum(weight * vec_b.get(term, 0.0) for term, weight in vec_a.items())
        norm_a = math.sqrt(sum(weight ** 2 for weight in vec_a.values()))
        norm_b = math.sqrt(sum(weight ** 2 for weight in vec_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def similarity(self, text_a: str, text_b: str, top_terms: int = 6) -> EmbeddingResult:
        vec_a, tokens_a = self._vectorize(text_a)
        vec_b, tokens_b = self._vectorize(text_b)
        score = self._cosine_similarity(vec_a, vec_b)
        shared = sorted(set(tokens_a).intersection(tokens_b))[:top_terms]
        return EmbeddingResult(score=score, shared_terms=shared)
