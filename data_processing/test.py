import chromadb
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

# --- 1. Инициализация эмбеддингов ---
embeddings = HuggingFaceBgeEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- 2. Подключение к удаленному серверу Chroma ---
chroma_host = "localhost" # Или IP-адрес сервера, если он не на localhost
chroma_port = 8000
collection_name = "langchain_docs"

# Создаем HTTP-клиент Chroma, указывая хост и порт
client = chromadb.HttpClient(host=chroma_host, port=chroma_port)

# Создаем объект LangChain Chroma, передавая клиент и имя коллекции
vectordb = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=embeddings
)

# --- 3. Задаем вопрос (similarity search) ---
query = "Как мне использовать Chroma vector database?"
print(f"Ищем похожие документы для запроса: '{query}'")

results = vectordb.similarity_search(query, k=10)

# --- 4. Выводим результаты ---
print("\n--- Найденные документы ---")
for i, doc in enumerate(results):
    print(f"\n[{i+1}] Source: {doc.metadata.get('source', 'N/A')}")
    print(f"Title: {doc.metadata.get('title', 'N/A')}")
    print(f"Content: {doc.page_content}...")