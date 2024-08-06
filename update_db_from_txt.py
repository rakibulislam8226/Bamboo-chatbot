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


def update_database(file_path, db_name="conversations.db"):
    """
    Updates the SQLite database with conversation pairs from a file.

    Parameters:
    file_path (str): The path to the file containing conversation pairs.
    db_name (str): The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    with open(file_path, "r") as file:
        lines = file.read().splitlines()

    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            user_input = lines[i].strip().lower()
            response = lines[i + 1].strip()

            # Insert or update the conversation pair in the database
            c.execute(
                """
                INSERT OR REPLACE INTO conversations (user_input, response)
                VALUES (?, ?)
            """,
                (user_input, response),
            )
            conn.commit()
    print(f"Database has been updated based on txt file {file_path}")
    conn.close()


if __name__ == "__main__":
    chat_file = "chat.txt"
    create_database()
    update_database(chat_file)
