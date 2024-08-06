import db
from chatbot import get_response, load_conversations


def main():
    # Path to chat.txt
    chat_file = "chat.txt"

    # Create database and table
    db.create_database()

    # Load conversations into the database
    load_conversations(chat_file)

    # Interaction loop
    exit_conditions = (":q", "quit", "exit")
    while True:
        query = input("> ")
        if query.lower() in exit_conditions:
            break
        else:
            response = get_response(query)
            print(f"🪴: {response}")


if __name__ == "__main__":
    main()
