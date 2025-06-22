import typer
from rich import print as rprint

def validate_api_key(api_key: str) -> bool:
    """Validate OpenAI API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        bool: True if valid
    """
    # Basic validation - OpenAI keys typically start with "sk-" and are 51 chars
    if not api_key or not api_key.startswith("sk-") or len(api_key) < 20:
        return False
    return True

def prompt_for_api_key() -> str:
    """Prompt user for API key with validation
    
    Returns:
        str: Valid API key
    """
    api_key = ""
    while not api_key:
        api_key = typer.prompt("Enter your OpenAI API key", hide_input=True, default="")
        if not api_key:
            rprint("[yellow]API key is required. Please enter a valid API key.[/yellow]")
        elif not validate_api_key(api_key):
            rprint("[yellow]Invalid API key format. API keys typically start with 'sk-'.[/yellow]")
            api_key = ""
    
    return api_key