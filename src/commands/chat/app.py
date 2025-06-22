import typer

# Import command implementations
from commands.chat.single import single_message_command
from commands.chat.interactive import interactive_chat_command

app = typer.Typer(help="Chat with AI models")

@app.callback()
def callback():
    """Chat with AI models"""
    pass

# Register commands
app.command(name="single", help="Send a single message and get a response")(single_message_command)
app.command(name="interactive", help="Start an interactive chat session")(interactive_chat_command)