import json
from typing import Optional

from rich import print as rprint
from settings import AppSettings, CONFIG_FILE, CONFIG_DIR

def get_settings() -> AppSettings:
    """Get application settings, creating default if not exists
    
    Returns:
        AppSettings: Application settings
    """
    if not CONFIG_FILE.exists():
        return AppSettings()
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
        return AppSettings.model_validate(config_data)
    except Exception as e:
        rprint(f"[red]Error reading configuration: {e}[/red]")
        return AppSettings()

def ensure_config_exists() -> Optional[AppSettings]:
    """Ensure config file exists and return settings, or None if missing
    
    Returns:
        Optional[AppSettings]: Settings object or None if config doesn't exist
    """
    if not CONFIG_FILE.exists():
        rprint("[yellow]Configuration file not found. Run 'termgpt config init' first.[/yellow]")
        return None
    
    return get_settings()

def save_settings(settings: AppSettings) -> bool:
    """Save settings to config file
    
    Args:
        settings: Application settings to save
        
    Returns:
        bool: Success
    """
    try:
        CONFIG_DIR.mkdir(exist_ok=True)
        CONFIG_FILE.write_text(settings.model_dump_json(indent=2))
        return True
    except Exception as e:
        rprint(f"[red]Error saving configuration: {e}[/red]")
        return False
