import typer

from commands.config import app as config_app
# from src.commands.chat import chat_app

app = typer.Typer(help="CLI tool for interacting with OpenAI models")

app.add_typer(config_app, name="config", help="Configure settings like API tokens and defaults")
# app.add_typer(profiles_app, name="profiles", help="Manage different user profiles")
# app.add_typer(chat_app, name="chat", help="Start a chat session with an AI model")

if __name__ == "__main__":
    app()