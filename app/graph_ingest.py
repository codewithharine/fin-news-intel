import json
from pathlib import Path

from app.agents.deduplication import deduplicate
from app.agents.entity_extraction import extract_entities
from app.agents.impact_analysis import map_impact


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MOCK_NEWS_PATH = PROJECT_ROOT / "data" / "mock_news.json"
STORIES_PATH = PROJECT_ROOT / "data" / "stories.json"


def run_ingestion_pipeline():
    """
    Load articles from mock_news.json, run:
      1) deduplication
      2) entity extraction
      3) impact mapping
    and save a summary for each unique story into data/stories.json.
    """
    if not MOCK_NEWS_PATH.exists():
        print(f"❌ mock_news.json not found at {MOCK_NEWS_PATH}")
        return

    with MOCK_NEWS_PATH.open(encoding="utf-8") as f:
        articles = json.load(f)

    print(f"📥 Loaded {len(articles)} articles")

    story_summaries = {}

    for article in articles:
        print("\n" + "-" * 60)
        print(f"📰 Article {article['id']}: {article['title']}")

        # 1) Deduplication
        dedup_result = deduplicate(article)
        story_id = dedup_result["unique_story_id"]
        is_duplicate = dedup_result["duplicate_of"] is not None

        if is_duplicate:
            print(f"🔁 Duplicate of story: {story_id} (sim={dedup_result['similarity']:.2f})")
            # For duplicates, we don't recompute entities/impact
            continue
        else:
            print(f"✨ New unique story: {story_id}")

        # 2) Entity extraction
        entities = extract_entities(article)
        print(f"🏢 Companies: {entities.get('companies')}")
        print(f"🏦 Sectors: {entities.get('sectors')}")
        print(f"🏛️ Regulators: {entities.get('regulators')}")

        # 3) Impact mapping
        impact = map_impact(entities)
        impacted_stocks = impact["impacted_stocks"]

        if impacted_stocks:
            print("📊 Impacted stocks:")
            for s in impacted_stocks:
                print(
                    f"   - {s['symbol']} (conf={s['confidence']}, type={s['type']})"
                )
        else:
            print("📊 Impacted stocks: None detected")

        # Save summary (we also keep published_at for later ranking if needed)
        story_summaries[story_id] = {
            "story_id": story_id,
            "article_id": article["id"],
            "title": article["title"],
            "body": article.get("body", ""),
            "published_at": article.get("published_at", ""),
            "entities": entities,
            "impacted_stocks": impacted_stocks,
        }

    # Save to data/stories.json
    STORIES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STORIES_PATH.open("w", encoding="utf-8") as f:
        json.dump(list(story_summaries.values()), f, indent=2, ensure_ascii=False)

    print("\n✅ Ingestion pipeline finished.")
    print(f"Unique stories found: {len(story_summaries)}")
    print(f"💾 Saved to: {STORIES_PATH}")

    return story_summaries


if __name__ == "__main__":
    run_ingestion_pipeline()
