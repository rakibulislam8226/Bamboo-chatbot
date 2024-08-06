import db
from chatbot import get_response


def main():
    """
    Main function to interact with the chatbot. Assumes that the database has
    already been created and updated with conversation pairs from chat.txt.
    Runs an interaction loop to get user input and provide responses.
    """
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
