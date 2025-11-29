# System Architecture — Financial News Intelligence System

This project uses a modular **multi-agent architecture** inspired by LangGraph.  
Each agent is responsible for one stage of financial news processing.

---

## 1. Agent Overview

### 1. News Ingestion Agent
- Loads raw or mock news articles.
- Normalizes fields (id, title, body, source, timestamp).
- Passes articles to downstream agents.

### 2. Deduplication Agent
- Generates sentence embeddings using `all-MiniLM-L6-v2`.
- Uses ChromaDB for vector similarity search.
- If cosine similarity ≥ **0.85**, marks the new article as a duplicate.
- Otherwise creates a new `unique_story_id` and stores embeddings.

### 3. Entity Extraction Agent
- Uses spaCy `en_core_web_sm` for NER.
- Extracts:
  - Companies  
  - Sectors  
  - Regulators  
  - ORG entities  
- Maps detected text to structured entities using `companies.csv` and keyword heuristics.

### 4. Stock Impact Analysis Agent
Maps extracted entities to stock symbols.

Confidence rules:
- Direct company mention → **1.0**
- Sector-wide impact → **0.7**
- RBI/SEBI regulatory impact → **0.75**

Produces a structured list:

[ {symbol: "...", confidence: 1.0, type: "direct"}, {symbol: "...", confidence: 0.7, type: "sector"}, ... ]

### 5. Storage & Indexing Agent
- Stores processed unique stories in `data/stories.json`.
- Indexes embeddings + metadata in ChromaDB for future search.
- Maintains vector_store directory for persistent retrieval.

### 6. Query Processing Agent
Handles all user queries using a hybrid reasoning system:

1. Runs NER on the query.  
2. Identifies intent: company, sector, regulator.  
3. Performs semantic search using the query embedding.  
4. Applies symbolic scoring:
   - Company match → +3  
   - Sector match → +2  
   - Regulator match → +2  
5. Semantic similarity contributes additional score.  
6. Sorts stories by combined score and returns top results with explanations.

---

## 2. Pipeline Flow

### Ingestion Pipeline

News Sources → Ingestion → Deduplication → Entity Extraction → Impact Analysis → Storage (stories.json + vector_db)

### Query Pipeline

User Query → NER → Semantic Search → Symbolic Matching → Ranking → Final Response

---

## 3. Data Flow Diagram (Text Trace)

mock_news.json ↓ Ingestion Agent ↓ Deduplication Agent ↓ Entity Extraction Agent ↓ Impact Analysis Agent ↓ data/stories.json + vector_store/

For queries:

User Query ↓ NER → extract company/sector/regulator ↓ ChromaDB → semantic similarity search ↓ Combine symbolic + semantic scores ↓ Return ranked stories + reasons + impacted stocks

---

## 4. Technology Stack

| Component | Technology Used |
|----------------|-------------------------------------|
| Embeddings | Sentence Transformers (MiniLM) |
| Vector Search | ChromaDB |
| NER | spaCy (en_core_web_sm) |
| Backend API | FastAPI |
| Agents | LangGraph-inspired modular agents |
| Storage | JSON + ChromaDB persistent vectors |
| Programming | Python 3.10+ |

---

## 5. Summary

This architecture fulfills all key hackathon requirements:

- **Intelligent deduplication** of financial news  
- **Accurate entity extraction** with company/sector/regulator detection  
- **Stock impact analysis** with confidence scoring  
- **Context-aware query system** for traders and investors  
- **Multi-agent pipeline** following LangGraph design principles  

The design is modular, scalable, and ready for integration with real financial RSS feeds.


