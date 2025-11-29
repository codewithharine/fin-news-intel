import csv
from pathlib import Path
import spacy

# Load small English model
# Make sure to run: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# --- Load companies from CSV ---

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMPANIES_CSV = PROJECT_ROOT / "data" / "companies.csv"

COMPANY_MAP = {}  # name_lower -> {"company": ..., "symbol": ..., "sector": ...}

if COMPANIES_CSV.exists():
    with COMPANIES_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name_lower = row["company"].strip().lower()
            COMPANY_MAP[name_lower] = {
                "company": row["company"].strip(),
                "symbol": row["symbol"].strip(),
                "sector": row["sector"].strip()
            }

# --- Simple keyword-based sector & regulator detection ---

def _detect_sectors(text: str):
    text_l = text.lower()
    sectors = set()

    if "bank" in text_l or "banking" in text_l:
        sectors.add("Banking")
    if "nbfc" in text_l or "non-banking finance" in text_l:
        sectors.add("NBFC")
    if "auto" in text_l or "vehicle" in text_l or "car " in text_l:
        sectors.add("Auto")
    if "steel" in text_l:
        sectors.add("Steel")
    if "port" in text_l or "logistics" in text_l:
        sectors.add("Ports")
    if "it services" in text_l or "sof_
