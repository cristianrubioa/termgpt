from typing import Dict, List, Optional
from rich import print as rprint
from rich.markdown import Markdown

from core.openai_client import OpenAIClient
from settings import ProfileConfig


class Conversation:
    """Manages a conversation with an AI model"""
    
    def __init__(self, profile: ProfileConfig):
        """Initialize conversation with profile settings
        
        Args:
            profile: User profile with API key and model settings
        """
        self.profile = profile
        self.client = OpenAIClient(profile)
        self.messages: List[Dict[str, str]] = []
        self.model = profile.default_model
    
    def add_system_message(self, content: str) -> None:
        """Add system message to conversation
        
        Args:
            content: Message content
        """
        self.messages.append({"role": "system", "content": content})
    
    def add_user_message(self, content: str) -> None:
        """Add user message to conversation
        
        Args:
            content: Message content
        """
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str) -> None:
        """Add assistant message to conversation
        
        Args:
            content: Message content
        """
        self.messages.append({"role": "assistant", "content": content})
    
    def get_response(self, model: Optional[str] = None) -> str:
        """Get response from AI for current conversation
        
        Args:
            model: Model name to use, or None for default
            
        Returns:
            str: AI response text
        """
        # Use specified model or default
        model_name = model or self.model
        
        # Get response from OpenAI
        response = self.client.chat_completion(self.messages, model=model_name)
        
        # Extract and add response to conversation
        content = response.choices[0].message.content
        self.add_assistant_message(content)
        
        return content
    
    def display_messages(self, include_system: bool = False) -> None:
        """Display conversation messages
        
        Args:
            include_system: Whether to include system messages
        """
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            
            # Skip system messages if not requested
            if role == "system" and not include_system:
                continue
                
            # Format based on role
            if role == "user":
                rprint("\n[bold blue]You:[/bold blue]")
                rprint(content)
            elif role == "assistant":
                rprint("\n[bold green]AI:[/bold green]")
                rprint(Markdown(content))
            elif role == "system" and include_system:
                rprint("\n[bold yellow]System:[/bold yellow]")
                rprint(content)
        
        rprint("\n")
    
    def clear(self) -> None:
        """Clear conversation history"""
        self.messages = []