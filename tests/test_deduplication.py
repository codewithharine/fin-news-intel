from app.agents.deduplication import deduplicate

def test_dedup():
    article1 = {
        "id": "A1",
        "title": "RBI hikes repo rate by 25 bps",
        "body": "Reserve Bank increases policy rate to tackle inflation"
    }

    article2 = {
        "id": "A2",
        "title": "Reserve Bank raises policy rate",
        "body": "RBI increases interest rate by 0.25%"
    }

    r1 = deduplicate(article1)
    r2 = deduplicate(article2)

    print(r1)
    print(r2)

    assert r2["duplicate_of"] == r1["unique_story_id"]
