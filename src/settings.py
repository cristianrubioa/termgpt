
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

