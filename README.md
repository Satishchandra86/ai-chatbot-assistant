# AI Chatbot Assistant

A chatbot web application built with Python, Flask, SQLite,
HTML, CSS, JavaScript, and an optional AI API.

## Features

- Interactive chat interface
- AI-generated answers when configured
- Offline demonstration mode
- Persistent conversation history
- Clear chat functionality
- Responsive design

## Requirements

- Python 3.10 or later
- VS Code or another code editor
- Internet access for package installation
- AI API key for AI-generated responses

## Installation on Windows

Open PowerShell inside the project directory.

Create a virtual environment:

    py -m venv .venv

Activate it:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install -r requirements.txt

Create your local configuration:

    Copy-Item .env.example .env

Start the application:

    python app.py

Open this address in your browser:

    http://127.0.0.1:5000

## AI setup

Open the .env file and configure OPENAI_API_KEY.
Restart the server after changing the configuration.

Check your AI provider's current pricing and model access.

## Database

SQLite stores chat messages in chat_history.db.
The database is created automatically.

## Security

Do not publish API keys or the local database.
Do not use Flask's development server for public deployment.
Add authentication, rate limits, and production security
before exposing the app to other users.