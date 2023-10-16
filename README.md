# Text to SQL Generator using OpenAI and Streamlit

## Overview

This project is a Text to SQL generator using OpenAI's GPT-3.5 Turbo model integrated with Streamlit, a popular Python web application framework. The application takes natural language descriptions and generates SQL queries in response.

## Prerequisites

Before running this application, ensure you have the following prerequisites:

- OpenAI API Key: You'll need a valid OpenAI API key, which should be set as the value for the `"pass"` key in Streamlit's secrets.

## Getting Started

1. Set your OpenAI API key as a secret in Streamlit. This key is essential for interacting with the OpenAI GPT-3.5 Turbo model.

2. Define the Streamlit application, including the UI elements and initial context for the chat.

3. Initialize a chat history to store messages between the user and the assistant.

4. Display chat messages from the chat history when the application is rerun.

5. Define the initial system context for the assistant. It provides information about the role of the SQL bot and how it should respond to user queries.

6. Allow the user to input a description to generate SQL queries.

7. Display user messages and the assistant's responses in the chat container.

8. Use OpenAI's GPT-3.5 Turbo model to generate SQL queries based on the user's input.

## Usage

To use the application, follow these steps:

1. Enter your description in the chat input field. The description should contain details for the SQL query you want to generate.

2. The application will then generate an SQL query based on the provided description and display it in the chat container.

## Important Notes

- Ensure your OpenAI API key is kept secure and never shared publicly.

- The assistant's responses are generated by OpenAI's GPT-3.5 Turbo model and are based on the information provided in the conversation history.

- The assistant is designed to help users create SQL commands. It should start responses with "This is your SQL," followed by the SQL statement.

- The database consists of SQL tables, and the goal is to generate SQL queries that can be complex, including multiple joins, but they should be optimized and specific to the requirements.

- If a request can't be fulfilled with SQL, the assistant will suggest asking for a SQL-related request.

## License

This project is available under the [MIT License](LICENSE).

Please refer to OpenAI's terms of service for any specific licensing or usage restrictions related to the GPT-3.5 Turbo model.

## Acknowledgments

This project was created using OpenAI's GPT-3.5 Turbo model and Streamlit. Special thanks to the developers and contributors of these tools and libraries.
