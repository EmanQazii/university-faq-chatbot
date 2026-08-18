import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.45
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
FALLBACK = (
    "Sorry, I couldn't find a relevant answer in the FAQ knowledge base. "
    "Try rephrasing your question or contact the university/SafeX support team."
)


class FAQRetriever:
    def __init__(self, faq_path: str = "data/faqs.csv"):
        self.df = pd.read_csv(faq_path)
        self.model = SentenceTransformer(MODEL_NAME)
        # embed all FAQ questions once at startup
        self.faq_embeddings = self.model.encode(
            self.df["question"].tolist(), convert_to_numpy=True
        )

    def retrieve(self, query: str) -> dict:
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        scores = cosine_similarity(query_embedding, self.faq_embeddings)[0]

        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        if best_score < THRESHOLD:
            return {
                "answer": FALLBACK,
                "matched_question": None,
                "similarity": best_score,
                "faq_id": None,
                "category": None,
                "matched": False,
            }

        row = self.df.iloc[best_idx]
        return {
            "answer": row["answer"],
            "matched_question": row["question"],
            "similarity": best_score,
            "faq_id": int(row["id"]),
            "category": row["category"],
            "matched": True,
        }