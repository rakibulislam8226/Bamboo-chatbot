import sqlite3
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import db


def preprocess_text(text):
    """
    Preprocesses the text by removing punctuation and converting to lowercase.

    Parameters:
    text (str): The input text to preprocess.

    Returns:
    str: The preprocessed text.
    """
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator).lower()


def load_conversations(file_path, db_name="conversations.db"):
    """
    Loads conversation pairs from a file, converts inputs to lowercase,
    and stores them in a SQLite database.

    Parameters:
    file_path (str): The path to the file containing conversation pairs.
    db_name (str): The name of the SQLite database file.
    """
    with open(file_path, "r") as file:
        lines = file.read().splitlines()

    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            user_input = preprocess_text(lines[i].strip().lower())
            response = lines[i + 1].strip()
            db.insert_user_input(user_input, db_name)


def train_model(db_name="conversations.db"):
    """
    Trains a TF-IDF model based on stored responses.

    Parameters:
    db_name (str): The name of the SQLite database file.

    Returns:
    tuple: (TfidfVectorizer, tfidf_matrix, responses)
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT response FROM conversations WHERE response IS NOT NULL")
    responses = [preprocess_text(row[0]) for row in c.fetchall()]
    conn.close()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(responses)
    return vectorizer, tfidf_matrix, responses


def generate_response(user_input, vectorizer, tfidf_matrix, responses, threshold=0.5):
    """
    Generates a response based on similarity to existing responses.

    Parameters:
    user_input (str): The input text from the user.
    vectorizer (TfidfVectorizer): The trained TF-IDF model.
    tfidf_matrix: The TF-IDF matrix of stored responses.
    responses: The list of stored responses.
    threshold (float): The similarity threshold for determining a match.

    Returns:
    str: The generated response.
    """
    user_input_preprocessed = preprocess_text(user_input)
    user_input_tfidf = vectorizer.transform([user_input_preprocessed])
    similarities = cosine_similarity(user_input_tfidf, tfidf_matrix)
    max_similarity = similarities.max()

    if max_similarity >= threshold:
        most_similar_idx = similarities.argmax()
        response = responses[most_similar_idx]
        return response
    else:
        return (
            "I am sorry I do not understand, But I store your input for further update."
        )


def get_response(query, db_name="conversations.db"):
    """
    Retrieves the response to a query from the SQLite database or generates a response based on similarity.

    Parameters:
    query (str): The user input.
    db_name (str): The name of the SQLite database file.

    Returns:
    str: The response to the query.
    """
    if query is None:
        return "I am sorry, but I do not understand."

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        """
        SELECT response FROM conversations
        WHERE user_input = ?
    """,
        (preprocess_text(query.lower()),),
    )
    result = c.fetchone()
    conn.close()

    if result and result[0]:
        return result[0]
    else:
        vectorizer, tfidf_matrix, responses = train_model(db_name)
        response = generate_response(query, vectorizer, tfidf_matrix, responses)
        db.insert_user_input(preprocess_text(query.lower()), db_name)
        return response
