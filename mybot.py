from openai import AzureOpenAI
from config import DefaultConfig
CONFIG = DefaultConfig()

# Set up credentials
endpoint = CONFIG.AZURE_OPENAI_ENDPOINT
api_key = CONFIG.AZURE_OPENAI_API_KEY
deployment_name = CONFIG.AZURE_DEPLOYMENT_MODEL_NAME

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)


# Send a chat request
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of India?"}
    ],
    max_tokens=100
)

print(response.choices[0].message.content)