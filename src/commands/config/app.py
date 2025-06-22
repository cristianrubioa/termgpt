import typer

# Import command implementations
from commands.config.init import init_command
from commands.config.profiles import create_profile_command, list_profiles_command, set_default_profile_command
from commands.config.api_keys import set_api_key_command
from commands.config.show import show_command

app = typer.Typer(help="Configure settings like API tokens and profiles")

@app.callback()
def callback():
    """Manage TermGPT configuration"""
    pass

# Register commands
app.command(name="init", help="Initialize configuration with default values")(init_command)
app.command(name="show", help="Show current configuration")(show_command)
app.command(name="create-profile", help="Create a new profile with custom settings")(create_profile_command)
app.command(name="list-profiles", help="List all available profiles")(list_profiles_command)
app.command(name="set-default-profile", help="Set the default profile to use")(set_default_profile_command)
app.command(name="set-api-key", help="Set API key for a specific profile")(set_api_key_command)