import typer
from rich import print as rprint

from core import config
from core import profiles
from utils import validators
from default import CONFIG_FILE

def init_command():
    if CONFIG_FILE.exists() and not typer.confirm("Configuration file already exists. Do you want to overwrite it?"):
        rprint("[yellow]Operation cancelled.[/yellow]")
        return
    
    # Get default settings or existing settings
    settings = config.get_settings()

    # Request API key
    api_key = validators.prompt_for_api_key()
    
    # Update or create default profile with API key
    profiles.create_or_update_profile(settings, settings.default_profile, api_key=api_key)

    # Save configuration
    if config.save_settings(settings):
        rprint("[green]Configuration initialized successfully.[/green]")
