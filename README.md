# 🧠 Financial News Intelligence System  
### AI/ML & Financial Technology Track — Tradl Hackathon 2025

This project is a **multi-agent AI system** built using **LangGraph**, **LLMs**, **semantic embeddings**, **NER**, and **FastAPI** to provide intelligent financial news analysis.

It performs:
- 📰 **News Deduplication** using semantic similarity (RAG + embeddings)  
- 🏢 **Entity Extraction** (companies, sectors, regulators)  
- 📊 **Stock Impact Mapping** with confidence scores  
- 💬 **Context-Aware Querying** (company → sector → macro)  
- 🔎 **Semantic Search** using ChromaDB  
- ⚡ **FastAPI Endpoints** for ingestion & querying  

This fully satisfies the **three core requirements** of the hackathon:
1. Intelligent Deduplication  
2. Entity Extraction & Stock Impact  
3. Context-Aware Query System  

---

# 🚀 Features

### ✔ Multi-Agent Pipeline
- Ingestion Agent  
- Deduplication Agent  
- Entity Extraction Agent  
- Impact Analysis Agent  
- Storage & Indexing Agent  
- Query Processing Agent  

### ✔ AI/ML Components
- Sentence Transformers (all-MiniLM-L6-v2) for embeddings  
- ChromaDB for vector similarity  
- spaCy for NER  
- Hybrid reasoning (semantic + entity-aware search)  

### ✔ Query Examples
| Query | What the system returns |
|-------|--------------------------|
| **HDFC Bank news** | Direct HDFC Bank news + Banking sector news + RBI policy affecting banks |
| **Banking sector update** | All stories related to the Banking sector |
| **RBI policy changes** | News mentioning RBI/regulators |
| **Interest rate impact** | Stories semantically related to rate hikes |

---

# 📂 Project Structure

fin-news-intel/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry
│   ├── graph_ingest.py      # LangGraph: ingestion pipeline
│   ├── graph_query.py       # LangGraph: query pipeline
│   ├── agents/
│   │   ├── ingestion.py
│   │   ├── deduplication.py
│   │   ├── entity_extraction.py
│   │   ├── impact_analysis.py
│   │   ├── storage_index.py
│   │   └── query_processing.py
│   ├── services/
│   │   ├── embeddings.py
│   │   ├── ner.py
│   │   ├── vector_store.py
│   │   └── db.py
│   └── config.py
├── data/
│   ├── mock_news.json       # (we’ll create this now)
│   ├── companies.csv        # (we’ll create this next)
│   └── sectors.csv          # (optional)
├── tests/
│   ├── test_deduplication.py
│   ├── test_query_patterns.py
├── README.md
├── ARCHITECTURE.md
└── requirements.txt
