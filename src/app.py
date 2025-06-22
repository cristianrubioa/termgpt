import typer
from rich import print as rprint

from commands.config.app import app as config_app

app = typer.Typer(help="CLI tool for interacting with OpenAI models")

# Register command groups
app.add_typer(config_app, name="config", help="Configure settings like API tokens and defaults")


@app.callback()
def callback():
    """TermGPT CLI"""
    pass

def main():
    """Entry point for the application"""
    try:
        app()
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    main()