import typer
from rich import print as rprint

from core import config
from core import profiles
from utils import validators

def set_api_key_command(
    api_key: str = typer.Option(..., prompt=True, hide_input=True, help="OpenAI API key", show_default=False),
    profile: str = typer.Option(None, help="Profile name (uses default profile if not specified)", show_default=False)
):
    # Ensure config exists
    settings = config.ensure_config_exists()
    if not settings:
        return
    
    # Find profile
    profile_obj, profile_name = profiles.find_profile(settings, profile)
    if not profile_obj:
        return
    
    # Validate API key
    if not validators.validate_api_key(api_key):
        rprint("[yellow]Warning: API key format looks unusual. Continuing anyway.[/yellow]")
    
    # Update profile
    profile_obj.api_key = api_key
    
    # Save configuration
    if config.save_settings(settings):
        rprint(f"[green]API key set for profile '{profile_name}'.[/green]")