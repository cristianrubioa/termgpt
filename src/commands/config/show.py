from rich import print as rprint
from core import config

def show_command():
    settings = config.ensure_config_exists()
    if not settings:
        return
    
    # Hide API keys in output
    safe_settings = settings.model_dump()
    for profile in safe_settings["profiles"]:
        profile["api_key"] = "******" if profile["api_key"] else "[not set]"
    
    rprint(safe_settings)