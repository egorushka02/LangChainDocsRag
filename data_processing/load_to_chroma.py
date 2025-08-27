import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import chromadb
from chromadb.config import Settings

class ChromaDBLoader:
    
    def __init__(self, host: str="localhost", port: int=8000):
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        # Chroma settings
        self.client = chromadb.HttpClient(host=host, port=port)


    def load_documents(self, json_file: str) -> list:
        """Load docs from JSON file"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        documents = []
        for item in data:
            doc = Document(
                page_content=item['text'],
                metadata={
                    "source": item["url"],
                    "title": item["title"],
                    "url": item["url"]
                }
            )
            documents.append(doc)

        return documents
    
    def split_documents(self, documents: list, chunk_size: int=3000, chunk_overlap: int=500):
        """Splitting documents to chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        return text_splitter.split_documents(documents)
    
    def recreate_collection(self, collection_name: str):
        """Delete and recreate collection"""
        try:
            if self.client.get_collection(name=collection_name):
                print(f"Collection '{collection_name}' already exists.")
                self.client.delete_collection(name=collection_name)
                print(f"Collection '{collection_name}' deleted before downloading new data.")
        except ValueError as e:
            print(f"Collection '{collection_name}' does not found. Creating new collection.")
        except Exception as e:
            print(f"There are error by checking collection '{collection_name}': {e}")

    
    def create_vector_store(self, documents: list, collection_name: str="langchain_docs"):
        """Create vector store"""
        # recreate collection to load new data
        self.recreate_collection(collection_name=collection_name)

        # Chunking docs
        split_docs = self.split_documents(documents)

        print(f"Creating vector store with {len(split_docs)} chunks...")

        # Creating Chroma DB
        vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            collection_name=collection_name,
            client=self.client
        )
        # # save
        # vector_store.persist()
        print(f"Vector store created in remote Chroma server.")

        return vector_store
    
def main():
    # loading docs
    loader = ChromaDBLoader()
    documents = loader.load_documents("data/langchain_documents.json")
    print(f"Loaded {len(documents)} documents")

    # creating new vectorstore
    vector_store = loader.create_vector_store(documents)

    # test it
    query = "What is LangChain and how does it work?"
    results = vector_store.similarity_search(query, k=3)

    print(f"\nResults for query: {query}")
    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {result.metadata['source']}")
        print(f'Content: {result.page_content}...')

    
if __name__ == "__main__":
    main()
