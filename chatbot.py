import sqlite3
import db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
            user_input = lines[i].strip().lower()
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
    responses = [row[0] for row in c.fetchall()]
    conn.close()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(responses)
    return vectorizer, tfidf_matrix, responses

def generate_response(user_input, vectorizer, tfidf_matrix, responses):
    """
    Generates a response based on similarity to existing responses.

    Parameters:
    user_input (str): The input text from the user.
    vectorizer (TfidfVectorizer): The trained TF-IDF model.
    tfidf_matrix: The TF-IDF matrix of stored responses.
    responses: The list of stored responses.

    Returns:
    str: The generated response.
    """
    user_input_tfidf = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_input_tfidf, tfidf_matrix)
    most_similar_idx = similarities.argmax()
    response = responses[most_similar_idx]

    return response

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
        (query.lower(),),
    )
    result = c.fetchone()
    conn.close()
    
    if result and result[0]:
        return result[0]
    else:
        vectorizer, tfidf_matrix, responses = train_model(db_name)
        response = generate_response(query, vectorizer, tfidf_matrix, responses)
        db.insert_user_input(query.lower(), db_name)
        return response
