import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import re


class ChatHistoryManager:
    """
    Manages the chat history by allowing messages to be added, saved to a file, and displayed.

    Attributes:
        directory (str): The directory where chat history files are stored.

    Methods:
        _get_timestamp(file_format=False): Returns the current timestamp in a specified format.
        start_new_session(): Starts a new chat session and creates a new file.
        add_message(role, text): Adds a message to the current chat session file.
        display(): Displays the content of the current chat session file.
    """

    def __init__(self, directory="chat_export"):
        self.directory = directory
        self.current_file = None

    def _get_timestamp(self, file_format=False):
        format_str = "%Y-%m-%d_%H-%M-%S" if file_format else "%Y-%m-%d %H:%M:%S"
        return datetime.now().strftime(format_str)

    def start_new_session(self):
        filename = f"{self._get_timestamp(file_format=True)}.txt"
        self.current_file = os.path.join(self.directory, filename)
        self.add_message("system", "--- New Session ---")

    def add_message(self, role, text):
        if not self.current_file:
            self.start_new_session()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.current_file, "a", encoding="utf-8") as file:
            file.write(f"{timestamp} {role}: {text}\n")

    def display(self):
        if self.current_file:
            with open(self.current_file, encoding="utf-8") as file:
                print(file.read())
        else:
            print("No active chat session yet.")


def main():
    """
    Manages the chat session by interacting with the user, displaying chat history, and handling chat responses.

    Returns:
        None
    """

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set your GEMINI_API_KEY in the environment."
        )

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }

    history_manager = ChatHistoryManager()

    model = genai.GenerativeModel(
        "gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    chat = model.start_chat(history=[])

    user_name = input("Please let know your name: ")

    while True:
        user_input = input(f"{user_name}: ").strip()
        if not user_input:
            print("Please enter some text.")
            continue

        if user_input.lower() == "history":
            history_manager.display()
            continue

        if user_input.lower() == "restart":
            history_manager.add_message("system", "--- Session Ended ---")
            chat = model.start_chat(history=[])
            history_manager.start_new_session()
            continue

        if user_input.lower() == "exit":
            history_manager.add_message("system", "--- Session Ended ---")
            break

        try:
            response = chat.send_message(user_input, stream=True)
            response_text = "".join(
                [
                    (
                        chunk.text
                        if chunk.text.endswith(".")
                        else re.sub(r"\s*$", ".", chunk.text)
                    )
                    for chunk in response
                ]
            )
            print(response_text)

            history_manager.add_message(user_name, user_input)
            history_manager.add_message("gemini", response_text)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
