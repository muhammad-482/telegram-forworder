import json
import os


# File to store chat data
chat_data_file = "chat_data.json"


# Load data from file or create an empty dictionary
def load_data():
    """Load chat data from a JSON file, or create a new file if it doesn't exist."""
    if not os.path.exists(chat_data_file):  # Check if file exists
        with open(chat_data_file, "w") as file:
            json.dump({}, file)  # Create an empty JSON file
        return {}  # Return empty dictionary

    try:
        with open(chat_data_file, "r") as file:
            return json.load(file)  # Load existing data
    except json.JSONDecodeError:
        print("Warning: chat_data_file contains invalid JSON. Resetting to empty.")
        with open(chat_data_file, "w") as file:
            json.dump({}, file)  # Reset file if corrupted
        return {}
            
# Add or update chat data (chat_id and last_message_id)
def add_or_update_chat(chat_id, last_message_id):
    data = load_data()  # Load existing data
    data[str(chat_id)] = last_message_id  # Add/update chat
    save_data(data)  # Save changes
    print(f"✅ Chat {chat_id} updated to message {last_message_id}.")


# Get last message ID of a chat
def get_last_message(chat_id):
    data = load_data()
    return data.get(str(chat_id))

# Save data to file
def save_data(data):
    with open(chat_data_file, "w") as file:
        json.dump(data, file, indent=4)