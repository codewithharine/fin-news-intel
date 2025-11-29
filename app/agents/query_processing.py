import json
from pathlib import Path

from app.services.ner import extract_entities as ner_extract_entities
from app.services.embeddings import embed
from app.services.vector_store import find_similar_stories

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STORIES_PATH = PROJECT_ROOT / "data" / "stories.json"


def _load_stories():
    if not STORIES_PATH.exists():
        return []
    with STORIES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def process_query(query: str, top_k: int = 10):
    """
    Core query processing:
      - run entity extraction on the query
      - use entity-based filters (company/sector/regulator)
      - use semantic search via embeddings + Chroma
      - combine scores and return ranked stories
    """
    stories = _load_stories()
    if not stories:
        return {
            "stories": [],
            "message": "No stories found. Run ingestion pipeline first."
        }

    # 1) Understand query (entities + intent-ish)
    q_entities = ner_extract_entities(query)
    q_companies = set(q_entities.get("companies", []))
    q_sectors = set(q_entities.get("sectors", []))
    q_regulators = set(q_entities.get("regulators", []))

    # 2) Base scoring with rule-based signals
    scores = {}  # story_id -> score
    reasons = {}  # story_id -> list of reasons

    def add_score(story_id, value, reason):
        scores[story_id] = scores.get(story_id, 0.0) + value
        reasons.setdefault(story_id, []).append(reason)

    # rule-based match
    for story in stories:
        sid = story["story_id"]
        ents = story.get("entities", {})
        s_companies = set(ents.get("companies", []))
        s_sectors = set(ents.get("sectors", []))
        s_regulators = set(ents.get("regulators", []))

        # Company match (strong)
        if q_companies and s_companies & q_companies:
            add_score(sid, 3.0, "Company match")

        # Sector match
        if q_sectors and s_sectors & q_sectors:
            add_score(sid, 2.0, "Sector match")

        # Regulator match
        if q_regulators and s_regulators & q_regulators:
            add_score(sid, 2.0, "Regulator match")

    # 3) Semantic similarity using vector search
    q_emb = embed(query)
    vs_results = find_similar_stories(q_emb, n_results=top_k)

    if vs_results and vs_results.get("ids"):
        ids_list = vs_results["ids"][0]
        distances = vs_results.get("distances", [[None] * len(ids_list)])[0]

        for story_id, dist in zip(ids_list, distances):
            if dist is None:
                continue
            # Chroma cosine: lower distance = closer; similarity ~ (1 - dist)
            sim = 1 - dist
            add_score(story_id, sim * 2.0, f"Semantic match (sim={sim:.2f})")

    # 4) Turn scores into ranked list
    # map story_id -> story dict
    story_map = {s["story_id"]: s for s in stories}

    ranked = sorted(
        [sid for sid in scores.keys() if sid in story_map],
        key=lambda x: scores[x],
        reverse=True
    )

    result_stories = []
    for sid in ranked[:top_k]:
        st = story_map[sid]
        result_stories.append({
            "story_id": sid,
            "article_id": st["article_id"],
            "title": st["title"],
            "published_at": st.get("published_at", ""),
            "entities": st.get("entities", {}),
            "impacted_stocks": st.get("impacted_stocks", []),
            "score": scores[sid],
            "reasons": reasons.get(sid, [])
        })

    return {
        "query": query,
        "query_entities": q_entities,
        "stories": result_stories
    }
