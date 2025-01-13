import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

def use_openapi():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Available GPT models:
    # - gpt-4-turbo-preview (latest, most capable)
    # - gpt-4 (standard GPT-4)
    # - gpt-3.5-turbo (faster and cheaper)
    # - gpt-3.5-turbo-16k (larger context window)
    Settings.llm = OpenAI(model="gpt-3.5-turbo", api_key=api_key)

    # Available embedding models:
    # - text-embedding-ada-002 (recommended)
    # - text-embedding-3-small (newer, cheaper)
    # - text-embedding-3-large (newer, more capable)
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002", api_key=api_key)
    
    # Configure chunking settings
    Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
    
    # Configure output and context settings
    Settings.num_output = 512
    Settings.context_window = 3900