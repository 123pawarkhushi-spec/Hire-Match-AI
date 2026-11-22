from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# LOAD PRETRAINED MODEL
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# SEMANTIC SIMILARITY FUNCTION
# --------------------------------------------------

def calculate_semantic_similarity(resume_text, job_description):

    # Convert both texts into embeddings
    embeddings = model.encode([
        resume_text,
        job_description
    ])

    # Calculate cosine similarity
    similarity = cosine_similarity(
        embeddings[0].reshape(1, -1),
        embeddings[1].reshape(1, -1)
    )[0][0]

    # Convert to percentage
    similarity_score = similarity * 100

    return round(float(similarity_score), 2)
