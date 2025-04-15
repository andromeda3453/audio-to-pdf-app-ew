from sentence_transformers import SentenceTransformer, util

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def match_template(text: str, templates: dict) -> str:
    """
    Uses sentence-transformers to find which template description 
    is most semantically similar to the transcript.
    """
    query_emb = embed_model.encode(text, convert_to_tensor=True)
    scores = {}

    for key, tdata in templates.items():
        desc_emb = embed_model.encode(tdata["description"], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_emb, desc_emb).item()
        scores[key] = similarity

    best_match = max(scores, key=scores.get)
    return best_match
