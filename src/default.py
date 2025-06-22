from pathlib import Path

# Configuration paths
CONFIG_DIR = Path.home() / ".termgpt"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default model values
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_MODEL_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# Default profile values
DEFAULT_PROFILE_NAME = "default"
