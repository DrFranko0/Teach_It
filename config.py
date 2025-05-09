from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv
load_dotenv()

TogetherAPIKey = os.getenv('TogetherAPIKey')
if not TogetherAPIKey:
    raise ValueError("API key not found. Please set 'TogetherAPIKey' in your .env file.")

model = OpenAIModel(
    'meta-llama/Llama-3.3-70B-Instruct-Turbo-Free',
    provider=OpenAIProvider(
        base_url='https://api.together.xyz/v1',
        api_key=TogetherAPIKey,
    ),
)