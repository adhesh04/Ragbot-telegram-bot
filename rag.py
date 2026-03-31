import chromadb
import ollama
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize ChromaDB (local, no server needed)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("pdf_docs")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def ingest_pdf(pdf_path: str, doc_name: str):
    """Read a PDF, chunk it, embed it, store in ChromaDB."""
    reader = PdfReader(pdf_path)
    full_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    
    chunks = splitter.split_text(full_text)
    print(f"Ingesting {len(chunks)} chunks from {doc_name}...")

    for i, chunk in enumerate(chunks):
        # Use Ollama's embedding model (pull it first: ollama pull nomic-embed-text)
        embedding = ollama.embeddings(model="nomic-embed-text", prompt=chunk)["embedding"]
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{doc_name}_chunk_{i}"],
            metadatas=[{"source": doc_name}]
        )
    print(f"Done. {len(chunks)} chunks stored.")

def search_pdf(query: str, n_results: int = 5) -> str:
    """Embed the query and retrieve top matching chunks."""
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    
    if not results["documents"][0]:
        return "No relevant content found in uploaded PDFs."
    
    context = "\n\n---\n\n".join(results["documents"][0])
    return context