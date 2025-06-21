import typer

from cli.config.commands import config
# from cli.variables.commands import app as variable_app

app = typer.Typer()

app.command(help="Configure general settings for the CLI.")(config)
# app.add_typer(variable_app, name="variables")

if __name__ == "__main__":
    app()