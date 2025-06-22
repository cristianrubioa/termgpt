import typer
from rich import print as rprint
from rich.markdown import Markdown

from core import config, profiles
from core.conversation import Conversation


def single_message_command(
    message: str = typer.Argument(..., help="Message to send to the AI", show_default=False),
    model: str = typer.Option(None, help="Model to use (defaults to profile's default)", show_default=False),
    profile: str = typer.Option(None, help="Profile to use (defaults to default profile)", show_default=False),
    system: str = typer.Option(None, help="Optional system message to set context", show_default=False),
):
    # Get settings
    settings = config.ensure_config_exists()
    if not settings:
        return
    
    # Get profile
    profile_obj, _profile_name = profiles.find_profile(settings, profile)
    if not profile_obj:
        return
    
    try:
        # Create conversation
        conversation = Conversation(profile_obj)
        
        # Add system message if provided
        if system:
            conversation.add_system_message(system)
        
        # Add user message
        conversation.add_user_message(message)
        
        # Get and display response
        rprint("[bold]Thinking...[/bold]")
        response = conversation.get_response(model)
        
        rprint(Markdown(response))
        
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {str(e)}")