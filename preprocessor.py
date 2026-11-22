
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

    # Keep useful programming symbols
    text = re.sub(r'[^a-z0-9+#.\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def tokenize_text(text):

    # Preserve important technical terms
    pattern = r'\.net|c\+\+|c#|[a-z0-9]+(?:[+#.]?[a-z0-9]+)*'

    tokens = re.findall(pattern, text)

    return tokens


def remove_stopwords(tokens):

    # Preserve negation and useful technical words
    stop_words = ENGLISH_STOP_WORDS - {
        "not", "no", "without"
    }

    filtered_tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    return filtered_tokens


def preprocess_text(text):

    cleaned = clean_text(text)

    tokens = tokenize_text(cleaned)

    filtered_tokens = remove_stopwords(tokens)

    return " ".join(filtered_tokens)
