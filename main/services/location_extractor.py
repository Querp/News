import spacy

nlp = spacy.load("en_core_web_lg")

def extract_locations(text: str) -> list[str]:
    if not text:
        return []

    doc = nlp(text)
    return [
        ent.text
        for ent in doc.ents
        if ent.label_ in ("GPE", "LOC")
    ]
