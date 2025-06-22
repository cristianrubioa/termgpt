import openai
from rich import print as rprint
from typing import Dict, List, Optional, Any

from settings import ProfileConfig, ModelConfig


class OpenAIClient:
    """Client for interacting with OpenAI API"""
    
    def __init__(self, profile: ProfileConfig):
        """Initialize OpenAI client with profile settings
        
        Args:
            profile: User profile with API key and model settings
        """
        self.profile = profile
        self.client = openai.OpenAI(api_key=profile.api_key)
        
        # Validate API key is set
        if not profile.api_key:
            raise ValueError("API key not set. Run 'termgpt config set-api-key' first.")
    
    def get_model_config(self, model_name: Optional[str] = None) -> ModelConfig:
        """Get configuration for specified model or default model
        
        Args:
            model_name: Name of model to get config for, or None for default
            
        Returns:
            ModelConfig: Model configuration
        """
        if not model_name:
            model_name = self.profile.default_model
            
        # Find model config
        model_config = next(
            (m for m in self.profile.models if m.name == model_name), 
            None
        )
        
        # If not found, use first model or create default
        if not model_config and self.profile.models:
            model_config = self.profile.models[0]
        elif not model_config:
            model_config = ModelConfig(name=model_name)
            
        return model_config
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send chat completion request to OpenAI API
        
        Args:
            messages: List of message objects with role and content
            model: Model name to use, or None for default
            **kwargs: Additional parameters to pass to API
            
        Returns:
            Dict: API response
        """
        # Get model name and config
        model_name = model or self.profile.default_model
        model_config = self.get_model_config(model_name)
        
        # Prepare parameters
        params = {
            "model": model_name,
            "messages": messages,
            "temperature": model_config.temperature,
            "max_tokens": model_config.max_tokens,
            "top_p": model_config.top_p,
            "frequency_penalty": model_config.frequency_penalty,
            "presence_penalty": model_config.presence_penalty,
        }
        
        # Override with any provided kwargs
        params.update(kwargs)
        
        try:
            # Send request to OpenAI
            return self.client.chat.completions.create(**params)
        except openai.APIError as e:
            rprint(f"[red]OpenAI API Error: {str(e)}[/red]")
            raise