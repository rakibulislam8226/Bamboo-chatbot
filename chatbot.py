import sqlite3

import db


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
            db.insert_conversation(user_input, response, db_name)


def get_response(query, db_name="conversations.db"):
    """
    Retrieves the response to a query from the SQLite database.

    Parameters:
    query (str): The user input.
    db_name (str): The name of the SQLite database file.

    Returns:
    str: The response to the query.
    """
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
    if result:
        return result[0]
    else:
        return "I am sorry, but I do not understand."
