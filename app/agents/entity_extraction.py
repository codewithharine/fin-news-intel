from app.services.ner import extract_entities as ner_extract_entities

def extract_entities(article):
    """
    Given an article dict with title/body,
    run NER + rules and return structured entities.
    """
    text = (article.get("title", "") or "") + " " + (article.get("body", "") or "")
    entities = ner_extract_entities(text)
    return entities
