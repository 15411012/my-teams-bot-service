import requests
from openai import AzureOpenAI
from config import DefaultConfig
CONFIG = DefaultConfig()

# -------- Step 1: Search Azure AI Search --------
search_term = "tell me narendra collage name"
search_url = CONFIG.AZURE_SEARCH_ENDPOINT
api_key = CONFIG.AZURE_SEARCH_API_KEY

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

params = {
    "api-version": "2023-11-01",
    "search": search_term,
    "searchFields": "content"
}

response = requests.get(search_url, headers=headers, params=params)
results = response.json()


# -------- Step 2: Extract content from search --------
context = "\n".join([doc["content"] for doc in results["value"][:3]])


# -------- Step 3: Build prompt --------
prompt = f"""
You are a helpful assistant. Use the context below to answer the question.

Context:
{context}

Question:
{search_term}
"""

# -------- Step 4: Use Azure OpenAI SDK --------
endpoint = CONFIG.AZURE_OPENAI_ENDPOINT
api_key = CONFIG.AZURE_OPENAI_API_KEY
deployment_name = CONFIG.AZURE_DEPLOYMENT_MODEL_NAME

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=300
)

# -------- Step 5: Print answer --------
print("ANSWER:\n", response.choices[0].message.content)
