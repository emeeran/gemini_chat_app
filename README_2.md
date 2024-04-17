# Chat Interface with Generative AI

This documentation provides a detailed overview of a Python program designed to interface with a generative AI model for chatting, manage chat history, and leverage environment variables for configuration. The program includes a chat history manager, integrates with an AI chat model provided by Google (referred to as `genai` in the code), and allows for commands within the chat for session management.

## Table of Contents

* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Environment Variables](#environment-variables)
* [Classes and Methods](#classes-and-methods)
    * [ChatHistoryManager](#chathistorymanager)
* [Safety Settings](#safety-settings)
* [Command Reference](#command-reference)
* [License](#license)

## Features

* Start a new chat session with generative AI.
* Keep a log of the chat history in text files.
* Control chat sessions with commands ('history', 'restart', 'exit').
* Dynamic response formatting and error handling.

## Requirements

* Python 3.8+
* `dotenv` library for loading environment variables.
* `os` and `datetime` modules for managing directories and timestamps.
* `re` module for regular expression operations.
* Google's `generativeai` library for AI interaction.

## Installation

To get started with this program, ensure you have Python installed and then follow these steps:

1. Clone the repository or download the source code.
2. Install required Python libraries:

```bash
pip install python-dotenv google-generativeai
```

## Usage

1. **Set Up Environment Variables:** Create a `.env` file in the root directory of the project and add your `GEMINI_API_KEY`:

```
GEMINI_API_KEY=your_api_key_here
```

2. **Run the Program:** Execute the main script to start interacting with the generative AI.

```bash
python script_name.py


3. **Chat Commands:**
   - Type `history` to view the current session's chat history.
   - Type `restart` to end the current session and start a new one.
   - Type `exit` to terminate the chat session.

## Environment Variables

- `GEMINI_API_KEY`: Required for authenticating with the Google Generative AI service.

## Classes and Methods

### ChatHistoryManager

Manages chat histories, including starting new sessions, adding messages, and displaying the history.

**Methods:**

- `__init__(self, directory="chat_export")`: Initializes a new instance, optionally setting a directory for storing histories.
- `_get_timestamp(self, file_format=False)`: Returns the current timestamp, formatted for filenames if `file_format=True`.
- `start_new_session(self)`: Starts a new chat session, creating a new file for logging.
- `add_message(self, role, text)`: Adds a message to the current session's log file.
- `display(self)`: Displays the current session's chat history.

## Safety Settings

Customize safety settings within the code to filter responses based on content categories, such as harassment or hate speech. Adjust these settings in the `safety_settings` dictionary according to your requirements.

## Command Reference

- `history`: Displays the chat history of the current session.
- `restart`: Ends the current session and starts a new one, logging the transition.
- `exit`: Ends the current session without starting a new one.

## License

Please ensure you comply with Google's licensing and usage terms for the Generative AI service and consider open-source licenses for your adaptation of this code.
```
