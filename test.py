from astrapy import DataAPIClient
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.astra_db import AstraDBVectorStore
import getpass
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_endpoint = os.getenv('api_endpoint')
print(api_endpoint)
    # "\nPlease enter your Database Endpoint URL "

token = os.getenv('token')
print(token)
    # "\nPlease enter your 'Database Administrator' Token"

astra_db_store = AstraDBVectorStore(
    token=token,
    api_endpoint=api_endpoint,
    collection_name="cier2_collection",  # Existing collection
    embedding_dimension=1536
)

embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

storage_context = StorageContext.from_defaults(vector_store=astra_db_store)

# ⚠️ FIX: Load index from vector store instead of from_documents
index = VectorStoreIndex.from_vector_store(
    vector_store=astra_db_store,
    storage_context=storage_context,
    embed_model=embed_model
)


print("Question 1 ==========================================")
query_engine = index.as_query_engine()
query = """用 1000字繁體中文簡述 "Determinants of Highly-Skilled Migration –
Taiwan’s Experiences" 的內容, 不知道就說不知道 """
print("Question 1: ", query)
response = query_engine.query(query)
print(response.response)
print("=====================================================")

print("Question 2 ==========================================")
query_engine = index.as_query_engine()
query = """請翻譯 "Determinants of Highly-Skilled Migration – Taiwan's Experiences""" 
print("Question 2: ", query)
response = query_engine.query(query)
print(response.response)
print("=====================================================")

print("Question 3 ==========================================")
query_engine = index.as_query_engine()
query = """用 1000字繁體中文簡述 "高技能移民的決定因素" , 不知道就說不知道"""
print("Question 3: ", query)
response = query_engine.query(query)
print(response.response)
print("=====================================================")

print("Question 4 ==========================================")
query_engine = index.as_query_engine()
query = """用 1000字繁體中文簡述, 從台灣經驗中, 高技能移民的決定因素, 不知道就說不知道"""
print("Question 4: ", query)
response = query_engine.query(query)
print(response.response)
print("=====================================================")




