import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Initialize embedding
embeddings = HuggingFaceBgeEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to remote Chroma server
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME")

# Create HTTP Chroma client, using host and port
client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

# Create langchain chroma object by passing the client and collection name
vectorstore = Chroma(
    client=client,
    collection_name=CHROMA_COLLECTION_NAME,
    embedding_function=embeddings
)