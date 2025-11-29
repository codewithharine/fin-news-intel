from fastapi import FastAPI, Query
from typing import Optional

from app.graph_ingest import run_ingestion_pipeline
from app.graph_query import run_query_pipeline

app = FastAPI(
    title="Financial News Intelligence API",
    description="Multi-agent AI system for financial news dedup, entity extraction, and intelligent querying.",
    version="0.1.0",
)


@app.get("/")
def home():
    return {"status": "Financial News Intelligence System Running 🚀"}


@app.post("/ingest_mock")
def ingest_mock_news():
    """
    Run the ingestion pipeline on data/mock_news.json.
    Creates unique stories, extracts entities, maps stock impact,
    saves to data/stories.json and updates vector DB.
    """
    summaries = run_ingestion_pipeline()
    if summaries is None:
        return {"success": False, "message": "mock_news.json not found"}
    return {
        "success": True,
        "unique_stories": len(summaries),
        "message": "Ingestion pipeline completed on mock dataset."
    }


@app.get("/query")
def query_news(
    q: str = Query(..., description="Natural language query, e.g. 'HDFC Bank news'"),
    top_k: int = Query(5, description="Maximum number of stories to return")
):
    """
    Query the processed stories with a natural language question.
    Example queries:
      - HDFC Bank news
      - Banking sector update
      - RBI policy changes
      - Interest rate impact
    """
    result = run_query_pipeline(q)
    # Optionally trim to top_k
    stories = result.get("stories", [])[:top_k]
    result["stories"] = stories
    return result
