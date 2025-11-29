import chromadb
from chromadb.config import Settings

# Create / Load persistent database
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="vector_store"))

# Create a collection for storing stories
collection = chroma_client.get_or_create_collection(
    name="stories",
    metadata={"hnsw:space": "cosine"}
)

def add_story_embedding(story_id: str, embedding: list, metadata: dict):
    collection.add(
        ids=[story_id],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def find_similar_stories(embedding: list, n_results: int = 3):
    """
    Returns top similar stories with cosine similarity scores.
    """
    if not embedding:
        return []

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    return results
