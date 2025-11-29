from app.services.embeddings import embed
from app.services.vector_store import add_story_embedding, find_similar_stories

SIMILARITY_THRESHOLD = 0.85  # Adjust if needed

def deduplicate(article):
    """
    Takes an article and determines if it's a duplicate of an existing story.
    Returns:
      - unique_story_id (new or existing)
      - duplicate_of (None or existing story)
    """
    text = article.get("title", "") + " " + article.get("body", "")
    emb = embed(text)

    # Search for similar stories
    search = find_similar_stories(emb, n_results=1)

    if search and search["ids"] and len(search["ids"][0]) > 0:
        most_similar_id = search["ids"][0][0]
        similarity = search["distances"][0][0]  # Chroma returns cosine distance (lower is better)

        # Convert distance to similarity (cosine)
        cosine_similarity = 1 - similarity

        if cosine_similarity >= SIMILARITY_THRESHOLD:
            # Duplicate found
            return {
                "unique_story_id": most_similar_id,
                "duplicate_of": most_similar_id,
                "similarity": cosine_similarity
            }

    # If no duplicates → create new story
    story_id = f"story_{article['id']}"
    add_story_embedding(story_id, emb, metadata={"headline": article.get("title")})

    return {
        "unique_story_id": story_id,
        "duplicate_of": None,
        "similarity": 1.0
    }
