from openai import AzureOpenAI
from config import DefaultConfig
CONFIG = DefaultConfig()

azure_openai_endpoint= CONFIG.AZURE_OPENAI_ENDPOINT
azure_openai_api_key = CONFIG.AZURE_OPENAI_API_KEY
azure_deployment_model_name = CONFIG.AZURE_DEPLOYMENT_MODEL_NAME
azure_search_endpoint = CONFIG.AZURE_SEARCH_ENDPOINT
azure_search_api_key = CONFIG.AZURE_SEARCH_API_KEY
azure_search_index = CONFIG.AZURE_SEARCH_INDEX

def get_mybot_response(user_query: str) -> str:
    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version="2024-03-01-preview",
        azure_endpoint=azure_openai_endpoint
    )

    response = client.chat.completions.create(
        model=azure_deployment_model_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps answer user questions using only the information retrieved from the provided documents. Do not use any outside knowledge. If the answer is not contained in the provided documents, say 'I don't know based on the available information.'"},
            {"role": "user", "content": user_query}
        ],
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": azure_search_endpoint,
                        "index_name": azure_search_index,
                        "authentication": {
                            "type": "api_key",
                            "key": azure_search_api_key
                        },
                    }
                }
            ]
        }
    )
    return response.choices[0].message.content
