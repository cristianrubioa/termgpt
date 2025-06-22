import typer
from rich import print as rprint

from settings import ProfileConfig, CONFIG_DIR, CONFIG_FILE, get_settings
from default import DEFAULT_MODEL

app = typer.Typer(help="Configure settings like API tokens and profiles")

@app.callback()
def callback():
    """Manage TermGPT configuration"""
    pass

@app.command(help="Initialize configuration with default values")
def init():
    if CONFIG_FILE.exists() and not typer.confirm("Configuration file already exists. Do you want to overwrite it?"):
        rprint("[yellow]Operation cancelled.[/yellow]")
        return
    
    settings = get_settings()

    # Request API key
    api_key = ""
    while not api_key:
        api_key = typer.prompt("Enter your OpenAI API key", hide_input=True, default="")
        if not api_key:
            rprint("[yellow]API key is required. Please enter a valid API key.[/yellow]")
    
    # Find default profile or create it
    default_profile = next((p for p in settings.profiles if p.name == "default"), None)
    if default_profile:
        default_profile.api_key = api_key
    else:
        settings.profiles.append(ProfileConfig(name="default", api_key=api_key))
    
    # Save configuration
    CONFIG_DIR.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(settings.model_dump_json(indent=2))
    rprint("[green]Configuration initialized successfully.[/green]")

@app.command(help="Show current configuration")
def show():
    if not CONFIG_FILE.exists():
        rprint("[yellow]Configuration file not found. Run 'termgpt config init' first.[/yellow]")
        return
    
    settings = get_settings()

    # Hide API keys in output
    safe_settings = settings.model_dump()
    for profile in safe_settings["profiles"]:
        profile["api_key"] = "******"
    
    rprint(safe_settings)

@app.command(help="Set API key for a specific profile")
def set_api_key(
    api_key: str = typer.Option(..., prompt=True, hide_input=True, help="OpenAI API key"),
    profile: str = typer.Option(None, help="Profile name (uses default profile if not specified)")
):
    if not CONFIG_FILE.exists():
        rprint("[yellow]Configuration file not found. Run 'termgpt config init' first.[/yellow]")
        return
    
    settings = get_settings()
    
    # If profile is not specified, use the default profile
    if profile is None:
        profile = settings.default_profile
        rprint(f"Using default profile: '{profile}'")
    
    # Find profile
    profile_found = False
    for p in settings.profiles:
        if p.name == profile:
            p.api_key = api_key
            profile_found = True
            break
    
    if not profile_found:
        rprint(f"[red]Profile '{profile}' does not exist. Create it first with 'termgpt config create-profile'.[/red]")
        return
    
    # Save configuration
    CONFIG_FILE.write_text(settings.model_dump_json(indent=2))
    rprint(f"[green]API key set for profile '{profile}'.[/green]")

@app.command(help="Create a new profile with custom settings")
def create_profile(
    name: str = typer.Option(..., prompt=True, help="Profile name"),
    api_key: str = typer.Option(None, prompt=False, hide_input=True, help="OpenAI API key"),
    model: str = typer.Option(None, help="Default model for this profile")
):
    if not CONFIG_FILE.exists():
        rprint("[yellow]Configuration file not found. Run 'termgpt config init' first.[/yellow]")
        return
    
    settings = get_settings()
    
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
        api_key = ""
        while not api_key:
            api_key = typer.prompt("Enter your OpenAI API key", hide_input=True, default="")
            if not api_key:
                rprint("[yellow]API key is required. Please enter a valid API key.[/yellow]")
    
    # Request model if not provided, showing the default
    if model is None:
        model = typer.prompt(f"Enter default model", default=DEFAULT_MODEL)
    
    # Create new profile
    new_profile = ProfileConfig(name=name, api_key=api_key, default_model=model)
    
    # Ask for additional model parameters
    customize_model = typer.confirm("Do you want to customize model parameters?", default=False)
    if customize_model:
        # Get default values from ModelConfig
        from settings import ModelConfig
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
    
    # Save configuration
    CONFIG_FILE.write_text(settings.model_dump_json(indent=2))
    rprint(f"[green]Profile '{name}' created successfully.[/green]")

@app.command(help="List all available profiles")
def list_profiles():
    if not CONFIG_FILE.exists():
        rprint("[yellow]Configuration file not found. Run 'termgpt config init' first.[/yellow]")
        return
    
    settings = get_settings()
    
    rprint("[bold]Available profiles:[/bold]")
    for profile in settings.profiles:
        is_default = " [green](default)[/green]" if profile.name == settings.default_profile else ""
        has_key = "[green]✓[/green]" if profile.api_key else "[red]✗[/red]"
        rprint(f"  • {profile.name}{is_default} - API Key: {has_key} - Model: {profile.default_model}")

@app.command(help="Set the default profile to use")
def set_default_profile(
    name: str = typer.Argument(..., help="Profile name to set as default")
):
    if not CONFIG_FILE.exists():
        rprint("[yellow]Configuration file not found. Run 'termgpt config init' first.[/yellow]")
        return
    
    settings = get_settings()
    
    # Check if profile exists
    profile_exists = any(p.name == name for p in settings.profiles)
    if not profile_exists:
        rprint(f"[red]Profile '{name}' does not exist. Create it first with 'termgpt config create-profile'.[/red]")
        return
    
    # Set as default
    settings.default_profile = name
    
    # Save configuration
    CONFIG_FILE.write_text(settings.model_dump_json(indent=2))
    rprint(f"[green]Default profile set to '{name}'.[/green]")
