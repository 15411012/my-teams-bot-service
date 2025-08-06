import os
from dotenv import load_dotenv
load_dotenv()

class DefaultConfig:


    APP_ID = os.environ.get("MICROSOFT_APP_ID")
    APP_PASSWORD = os.environ.get("MICROSOFT_APP_PASSWORD")
    # ====== Azure OpenAI Setup ======
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
    AZURE_DEPLOYMENT_MODEL_NAME = os.environ.get("AZURE_DEPLOYMENT_MODEL_NAME")

    # ====== Azure AI Search Setup ======
    AZURE_SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_API_KEY = os.environ.get("AZURE_SEARCH_API_KEY")
    AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")