import sqlite3


def create_database(db_name="conversations.db"):
    """
    Creates a SQLite database and a table for storing conversation pairs if it doesn't exist.

    Parameters:
    db_name (str): The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT UNIQUE,
            response TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def insert_user_input(user_input, db_name="conversations.db"):
    """
    Inserts a unique user input into the SQLite database.

    Parameters:
    user_input (str): The user input text.
    db_name (str): The name of the SQLite database file.
    """
    if user_input is None:
        return

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Check if the user_input already exists
    c.execute("SELECT * FROM conversations WHERE user_input = ?", (user_input,))
    existing_input = c.fetchone()

    if not existing_input:
        # Insert the user input if unique
        c.execute(
            "INSERT INTO conversations (user_input) VALUES (?)",
            (user_input,),
        )
        conn.commit()

    conn.close()
