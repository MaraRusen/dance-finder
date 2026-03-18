import cohere
import os
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def rerank_classes(query: str, classes: list) -> list:
    """Use Cohere Rerank to sort classes by semantic relevance to query."""
    if not classes or not query:
        return classes
    try:
        documents = [
            f"{c.get('style','')} {c.get('level','')} {c.get('studio','')} "
            f"{c.get('teacher',{}).get('name','')} {c.get('price_label','')} "
            f"{c.get('teacher',{}).get('bio','')}"
            for c in classes
        ]
        results = co.rerank(
            query=query,
            documents=documents,
            model="rerank-english-v3.0",
            top_n=len(classes)
        )
        return [classes[r.index] for r in results.results]
    except Exception as e:
        print(f"Rerank failed: {e}")
        return classes
    