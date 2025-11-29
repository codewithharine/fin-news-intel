import csv
from pathlib import Path

# Load companies + sectors mapping
PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMPANIES_CSV = PROJECT_ROOT / "data" / "companies.csv"

COMPANIES = []  # list of dicts: {company, symbol, sector}
SECTOR_TO_SYMBOLS = {}  # sector -> [symbols]

if COMPANIES_CSV.exists():
    with COMPANIES_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row["company"].strip()
            symbol = row["symbol"].strip()
            sector = row["sector"].strip()

            COMPANIES.append({"company": company, "symbol": symbol, "sector": sector})

            if sector not in SECTOR_TO_SYMBOLS:
                SECTOR_TO_SYMBOLS[sector] = []
            SECTOR_TO_SYMBOLS[sector].append(symbol)


def map_impact(entities: dict):
    """
    entities = {
      "companies": [...],
      "sectors": [...],
      "regulators": [...],
      ...
    }
    Returns:
      {"impacted_stocks": [ {symbol, confidence, type} ]}
    """

    impacted = {}
    companies = entities.get("companies", [])
    sectors = entities.get("sectors", [])
    regulators = entities.get("regulators", [])

    # 1) Direct company mentions -> 1.0 confidence
    for comp in companies:
        for row in COMPANIES:
            if row["company"].lower() == comp.lower():
                symbol = row["symbol"]
                impacted[symbol] = {
                    "symbol": symbol,
                    "confidence": 1.0,
                    "type": "direct"
                }

    # 2) Sector-wide impact -> 0.7 confidence
    for sector in sectors:
        symbols = SECTOR_TO_SYMBOLS.get(sector, [])
        for symbol in symbols:
            if symbol not in impacted:
                impacted[symbol] = {
                    "symbol": symbol,
                    "confidence": 0.7,
                    "type": "sector"
                }

    # 3) Regulator-based heuristic (e.g., RBI -> Banking sector)
    if "RBI" in regulators:
        banking_symbols = SECTOR_TO_SYMBOLS.get("Banking", [])
        for symbol in banking_symbols:
            # if already direct, keep 1.0
            if symbol in impacted:
                # maybe boost sector impact a bit if RBI + sector
                if impacted[symbol]["type"] == "sector":
                    impacted[symbol]["confidence"] = max(
                        impacted[symbol]["confidence"], 0.75
                    )
            else:
                impacted[symbol] = {
                    "symbol": symbol,
                    "confidence": 0.75,
                    "type": "regulator"
                }

    return {"impacted_stocks": list(impacted.values())}
