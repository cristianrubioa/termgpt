import typer
from rich import print as rprint
from rich.markdown import Markdown

from core import config, profiles
from core.conversation import Conversation


def interactive_chat_command(
    model: str = typer.Option(None, help="Model to use (defaults to profile's default)", show_default=False),
    profile: str = typer.Option(None, help="Profile to use (defaults to default profile)", show_default=False),
    system: str = typer.Option(None, help="Optional system message to set context", show_default=False),
):
    # Get settings
    settings = config.ensure_config_exists()
    if not settings:
        return
    
    # Get profile
    profile_obj, profile_name = profiles.find_profile(settings, profile)
    if not profile_obj:
        return
    
    try:
        # Create conversation
        conversation = Conversation(profile_obj)
        
        # Add system message if provided
        if system:
            conversation.add_system_message(system)
            rprint(f"[dim]System message set: {system}[/dim]")
        
        # Display welcome message
        model_name = model or profile_obj.default_model
        rprint(f"[bold]Starting chat with {model_name} using profile '{profile_name}'[/bold]")
        rprint("[dim]Type 'exit', 'quit', or press Ctrl+C to end the conversation[/dim]")
        rprint("[dim]Type 'clear' to clear the conversation history[/dim]")
        
        # Main chat loop
        while True:
            # Get user input
            user_input = typer.prompt("\nYou")
            
            # Check for exit commands
            if user_input.lower() in ("exit", "quit"):
                rprint("[bold]Ending conversation[/bold]")
                break
                
            # Check for clear command
            if user_input.lower() == "clear":
                conversation.clear()
                if system:
                    conversation.add_system_message(system)
                rprint("[bold]Conversation history cleared[/bold]")
                continue
            
            # Add user message
            conversation.add_user_message(user_input)
            
            # Get and display response
            rprint("[bold]Thinking...[/bold]")
            response = conversation.get_response(model)
            
            rprint("\n[bold green]AI:[/bold green]")
            rprint(Markdown(response))
            
    except KeyboardInterrupt:
        rprint("\n[bold]Conversation ended by user[/bold]")
    except Exception as e:
        rprint(f"\n[bold red]Error:[/bold red] {str(e)}")