from json import load
import os
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")
if not AVIATIONSTACK_API_KEY:
    raise ValueError("AVIATIONSTACK_API_KEY is not set in the environment variables.")
