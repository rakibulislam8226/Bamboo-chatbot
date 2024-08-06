import sqlite3


def create_database(db_name="conversations.db"):
    """
    Creates a SQLite database and a table for storing conversation pairs.

    Parameters:
    db_name (str): The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def insert_conversation(user_input, response, db_name="conversations.db"):
    """
    Inserts a conversation pair into the SQLite database.

    Parameters:
    user_input (str): The user input.
    response (str): The corresponding response.
    db_name (str): The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO conversations (user_input, response)
        VALUES (?, ?)
    """,
        (user_input, response),
    )
    conn.commit()
    conn.close()
