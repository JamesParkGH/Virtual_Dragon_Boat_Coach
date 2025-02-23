import requests
from decouple import config
import os
from utilsAPI import get_api_url

API_URL = get_api_url()

def get_token():
    """Retrieve API token from environment (set in batchDownload.py)."""
    token = os.environ.get("API_TOKEN")  # Get token from environment variable
    if not token:
        raise Exception("API token not found. Please log in through the web app.")
    return token
