import typer
from rich import print as rprint

from core.config import ensure_config_exists, save_settings
from core.profiles import find_profile
from utils.validators import prompt_for_api_key
from settings import ProfileConfig, ModelConfig
from default import DEFAULT_MODEL

def create_profile_command(
    name: str = typer.Option(..., prompt=True, help="Profile name"),
    api_key: str = typer.Option(None, prompt=False, hide_input=True, help="OpenAI API key"),
    model: str = typer.Option(None, help="Default model for this profile"),
    set_as_default: bool = typer.Option(None, help="Set this profile as the default")
):
    settings = ensure_config_exists()
    if not settings:
        return
    
    # Check if profile already exists
    profile_exists = any(p.name == name for p in settings.profiles)
    if profile_exists:
        overwrite = typer.confirm(f"Profile '{name}' already exists. Do you want to overwrite it?")
        if not overwrite:
            rprint("[yellow]Operation cancelled.[/yellow]")
            return
        # Remove existing profile
        settings.profiles = [p for p in settings.profiles if p.name != name]
    
    # Request API key if not provided
    if api_key is None:
        api_key = prompt_for_api_key()
    
    # Request model if not provided, showing the default
    if model is None:
        model = typer.prompt(f"Enter default model", default=DEFAULT_MODEL)
    
    # Create new profile
    new_profile = ProfileConfig(name=name, api_key=api_key, default_model=model)
    
    # Ask for additional model parameters
    customize_model = typer.confirm("Do you want to customize model parameters?", default=False)
    if customize_model:
        # Get default values from ModelConfig
        default_config = ModelConfig()
        
        temperature = typer.prompt(
            f"Temperature (0.0-1.0)", 
            default=default_config.temperature, 
            type=float
        )
        max_tokens = typer.prompt(
            f"Max tokens", 
            default=default_config.max_tokens, 
            type=int
        )
        top_p = typer.prompt(
            f"Top P (0.0-1.0)", 
            default=default_config.top_p, 
            type=float
        )
        
        # Update the model config
        new_profile.models = [ModelConfig(
            name=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=default_config.frequency_penalty,
            presence_penalty=default_config.presence_penalty
        )]
    
    settings.profiles.append(new_profile)
    
    # Ask if this should be the default profile if not specified in options
    if set_as_default is None:
        # If this is the first profile, suggest making it default
        is_first_profile = len(settings.profiles) == 1
        default_choice = is_first_profile
        set_as_default = typer.confirm(
            f"Do you want to set '{name}' as the default profile?", 
            default=default_choice
        )
    
    if set_as_default:
        settings.default_profile = name
        rprint(f"[green]Profile '{name}' set as default.[/green]")
    
    # Save configuration
    if save_settings(settings):
        rprint(f"[green]Profile '{name}' created successfully.[/green]")

def list_profiles_command():
    settings = ensure_config_exists()
    if not settings:
        return
    
    rprint("[bold]Available profiles:[/bold]")
    for profile in settings.profiles:
        is_default = " [green](default)[/green]" if profile.name == settings.default_profile else ""
        has_key = "[green]✓[/green]" if profile.api_key else "[red]✗[/red]"
        rprint(f"  • {profile.name}{is_default} - API Key: {has_key} - Model: {profile.default_model}")

def set_default_profile_command(
    name: str = typer.Argument(..., help="Profile name to set as default")
):
    settings = ensure_config_exists()
    if not settings:
        return
    
    # Check if profile exists
    profile_exists = any(p.name == name for p in settings.profiles)
    if not profile_exists:
        rprint(f"[red]Profile '{name}' does not exist. Create it first with 'termgpt config create-profile'.[/red]")
        return
    
    # Set as default
    settings.default_profile = name
    
    # Save configuration
    if save_settings(settings):
        rprint(f"[green]Default profile set to '{name}'.[/green]")