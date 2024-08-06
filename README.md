<h1 align="center">Hi 👋, I'm Rakibul Islam</h1>
<h4 align="center">Chat with AI</h4>
<br>
<br>


### Main File: `custom_chatbot.py`

#### Description

`custom_chatbot.py` is the main script for running the chatbot. It manages loading conversations from a file into a SQLite database, querying the database for responses, and interacting with the user.

#### Key Functions

- **`create_database(db_name)`**: Creates a SQLite database and a table for storing conversation pairs.
- **`insert_conversation(user_input, response, db_name)`**: Inserts a conversation pair into the SQLite database.
- **`load_conversations(file_path, db_name)`**: Reads conversation pairs from `chat.txt` and stores them in the database.
- **`get_response(query, db_name)`**: Retrieves the response for a user query from the database.
- **`main()`**: Main function to initialize the database, load conversations, and start the chat interaction loop.

#### Running the Script

- Under development