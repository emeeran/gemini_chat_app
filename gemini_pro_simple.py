import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

class ChatHistoryManager:
    def __init__(self, directory="chat_export"):
        # Initialize the ChatHistoryManager with a directory to store chat logs
        self.directory = directory
        self.current_file = None
        # Create the directory if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def _get_timestamp(self, file_format=False):
        # Private method to get the current timestamp
        # If file_format is True, format the timestamp for filenames
        format_str = "%Y-%m-%d_%H-%M-%S" if file_format else "%Y-%m-%d %H:%M:%S"
        return datetime.now().strftime(format_str)

    def start_new_session(self):
        # Start a new chat session
        # Create a new file with the current timestamp in the directory
        filename = f"{self._get_timestamp(file_format=True)}.txt"
        self.current_file = os.path.join(self.directory, filename)
        # Add a system message to the new file
        self.add_message("system", "--- New Session ---")

    def add_message(self, role, text):
        # Add a message to the current chat session
        # If there is no current session, start a new one
        if not self.current_file:
            self.start_new_session()
        # Write the message to the current file
        with open(self.current_file, "a", encoding="utf-8") as file:
            file.write(f"{self._get_timestamp()} {role}: {text}\n")

    def display(self):
        # Display the chat history of the current session
        # If there is no current session, print a message
        if self.current_file:
            with open(self.current_file, encoding="utf-8") as file:
                print(file.read())
        else:
            print("No active chat session yet.")

def main():
    # Load environment variables
    load_dotenv()
    # Get the API key from the environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    # If there is no API key, raise an error
    if not api_key:
        raise ValueError("API key not found. Please set your GEMINI_API_KEY in the environment.")
    # Configure the generative AI with the API key
    genai.configure(api_key=api_key)

    # Create a new ChatHistoryManager
    history_manager = ChatHistoryManager()
    # Create a new generative AI model
    model = genai.GenerativeModel("gemini-pro")
    # Start a new chat with the model
    chat = model.start_chat(history=[])

    # Ask the user for their name
    user_name = input("Please, let me know your name: ")

    while True:
        # Get input from the user
        user_input = input(f"{user_name}: ").strip()
        # If the user didn't enter anything, ask them to enter some text
        if not user_input:
            print("Please enter some text.")
            continue

        # If the user entered a command, execute the command
        if user_input.lower() in ["history", "restart", "exit"]:
            if user_input.lower() == "history":
                history_manager.display()
            elif user_input.lower() == "restart":
                history_manager.add_message("system", "--- Session Ended ---")
                chat = model.start_chat(history=[])
                history_manager.start_new_session()
            elif user_input.lower() == "exit":
                history_manager.add_message("system", "--- Session Ended ---")
                break
            continue

        try:
            # Send the user's message to the chat and get a response
            response = chat.send_message(user_input, stream=True)
            # Format the response text
            response_text = "".join(chunk.text for chunk in response)
            # Print the response text
            print(response_text)
            # Add the user's message and the response to the chat history
            history_manager.add_message(user_name, user_input)
            history_manager.add_message("gemini", response_text)
        except Exception as e:
            # If an error occurred, print the error
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # If the script is being run directly, call the main function
    main()
