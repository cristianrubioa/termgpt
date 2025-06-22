from typing import Optional, Tuple

from rich import print as rprint
from settings import AppSettings, ProfileConfig

def find_profile(settings: AppSettings, profile_name: Optional[str] = None) -> Tuple[Optional[ProfileConfig], str]:
    """Find a profile by name or use default
    
    Args:
        settings: Application settings
        profile_name: Profile name to find, or None to use default
        
    Returns:
        Tuple[Optional[ProfileConfig], str]: (profile, profile_name)
    """
    # If profile is not specified, use the default profile
    if profile_name is None:
        profile_name = settings.default_profile
        rprint(f"Using default profile: '{profile_name}'")
    
    # Find profile
    profile = next((p for p in settings.profiles if p.name == profile_name), None)
    
    if not profile:
        rprint(f"[red]Profile '{profile_name}' does not exist. Create it first with 'termgpt config create-profile'.[/red]")
        return None, profile_name
    
    return profile, profile_name

def create_or_update_profile(settings: AppSettings, name: str, **kwargs) -> ProfileConfig:
    """Create a new profile or update existing one
    
    Args:
        settings: Application settings
        name: Profile name
        **kwargs: Profile attributes to set
        
    Returns:
        ProfileConfig: Created or updated profile
    """
    # Find existing profile
    profile = next((p for p in settings.profiles if p.name == name), None)
    
    if profile:
        # Update existing profile
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
    else:
        # Create new profile
        profile = ProfileConfig(name=name, **kwargs)
        settings.profiles.append(profile)
    
    return profile