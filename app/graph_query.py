from app.agents.query_processing import process_query


def run_query_pipeline(query: str):
    """
    Simple wrapper over process_query.
    Can be used from FastAPI or CLI.
    """
    return process_query(query)


if __name__ == "__main__":
    # Tiny CLI for quick testing
    print("💬 Financial News Query CLI (blank to exit)")
    while True:
        q = input("\nEnter query: ").strip()
        if not q:
            break
        result = run_query_pipeline(q)
        stories = result.get("stories", [])
        print(f"\nFound {len(stories)} stories:")
        for s in stories:
            print(f"- [{s['story_id']}] {s['title']} (score={s['score']:.2f})")
            if s["impacted_stocks"]:
                print("  Impacted stocks:")
                for st in s["impacted_stocks"]:
                    print(f"    • {st['symbol']} (conf={st['confidence']}, type={st['type']})")
            if s["reasons"]:
                print("  Reasons:", "; ".join(s["reasons"]))
