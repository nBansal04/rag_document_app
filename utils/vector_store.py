import os
import requests
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from utils.pdf_loader import load_and_split_pdf

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

def collection_exists(name):
    response = requests.get(f"{QDRANT_URL}/collections/{name}")
    return response.status_code == 200

def load_or_create_vector_store(file_bytes, collection_name):
    if collection_exists(collection_name):
        return QdrantVectorStore.from_existing_collection(
            url=QDRANT_URL,
            collection_name=collection_name,
            embedding=embedding_model
        )
    else:
        docs = load_and_split_pdf(file_bytes)
        return QdrantVectorStore.from_documents(
            documents=docs,
            embedding=embedding_model,
            url=QDRANT_URL,
            collection_name=collection_name,
        )
