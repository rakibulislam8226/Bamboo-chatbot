import sqlite3


def export_chat_to_file(db_name="conversations.db", output_file="chat.txt"):
    """
    Exports chat conversations from the SQLite database to a text file.

    Parameters:
    db_name (str): The name of the SQLite database file.
    output_file (str): The path to the output text file.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Query to get all conversation pairs
    c.execute(
        """
        SELECT user_input, response FROM conversations
    """
    )

    # Fetch all rows from the query
    rows = c.fetchall()
    conn.close()

    # Write to the output file
    with open(output_file, "w") as file:
        for row in rows:
            user_input, response = row
            file.write(f"{user_input}\n{response}\n")

    print(f"Chat history has been exported to {output_file}")


if __name__ == "__main__":
    export_chat_to_file()
