
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from default import *

class ModelConfig(BaseModel):
    """Configuration for an OpenAI model"""
    name: str = DEFAULT_MODEL
    temperature: float = Field(default_factory=lambda: DEFAULT_MODEL_CONFIG["temperature"])
    max_tokens: int = Field(default_factory=lambda: DEFAULT_MODEL_CONFIG["max_tokens"])
    top_p: float = Field(default_factory=lambda: DEFAULT_MODEL_CONFIG["top_p"])
    frequency_penalty: float = Field(default_factory=lambda: DEFAULT_MODEL_CONFIG["frequency_penalty"])
    presence_penalty: float = Field(default_factory=lambda: DEFAULT_MODEL_CONFIG["presence_penalty"])

class ProfileConfig(BaseModel):
    """Configuration for a user profile"""
    name: str = DEFAULT_PROFILE_NAME
    api_key: Optional[str] = None
    default_model: str = DEFAULT_MODEL
    models: List[ModelConfig] = [ModelConfig()]
    
    model_config = ConfigDict(
        extra="allow",
        hide_input_in_errors=True
    )

class AppSettings(BaseSettings):
    """Global application configuration"""
    default_profile: str = DEFAULT_PROFILE_NAME
    profiles: List[ProfileConfig] = [ProfileConfig()]
    
    model_config = SettingsConfigDict(
        env_prefix="TERMGPT_",
    )

def get_settings():
    """Get application settings, always reading from the config file"""
    if CONFIG_FILE.exists():
        # Read the file manually
        import json
        try:
            with open(CONFIG_FILE, "r") as f:
                config_data = json.load(f)
            # Create settings from the loaded data
            return AppSettings.model_validate(config_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
        except PermissionError:
            print(f"Permission denied when reading {CONFIG_FILE}")
        except Exception as e:
            print(f"Unexpected error reading config file: {e}")
    
    # Fall back to default settings if file doesn't exist or has errors
    return AppSettings()

