import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Select Gemini model
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

# Validate API key
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing!")

# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY,
     http_options={
        "api_version": "v1beta"
    }
)


def get_client():
    return client
