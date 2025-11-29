from sentence_transformers import SentenceTransformer

# Load small, fast model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text: str):
    """
    Returns a vector embedding for the given text.
    """
    if not text:
        return []
    return model.encode(text).tolist()
