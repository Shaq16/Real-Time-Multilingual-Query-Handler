# main.py

from src.data_collection import DataCollector
from src.preprocessing import DataPreprocessor
from src.chunking import TextChunker
from src.embeddings import VectorStoreManager


def build_knowledge_base():
    """Build the complete knowledge base"""

    print("\nStep 1: Collecting data...")
    # FIX: Corrected the data_dir path to be relative to the script's execution folder
    # Assuming you run the script from the 'multilingual-query-handler' directory.
    collector = DataCollector(data_dir="data/raw")
    documents = collector.load_all_data()
    print(f"Loaded {len(documents)} documents")

    # If documents are not loaded, we stop here to prevent the ValueError later
    if not documents:
        print("\n🛑 Aborting: No documents were loaded. Check your data file and path.")
        return False
        
    print("\nStep 2: Preprocessing data...")
    preprocessor = DataPreprocessor()
    cleaned_docs = preprocessor.preprocess_documents(documents)
    print(f"Cleaned {len(cleaned_docs)} documents")

    print("\nStep 3: Chunking documents...")
    chunker = TextChunker()
    chunks = chunker.chunk_documents(cleaned_docs)
    print(f"Created {len(chunks)} chunks")

    # If chunking results in 0 chunks (shouldn't happen if documents are loaded, but good safety check)
    if not chunks:
        print("\n🛑 Aborting: Chunking resulted in 0 chunks.")
        return False

    print("\nStep 4: Creating vector store...")
    vector_manager = VectorStoreManager()
    vector_manager.create_vectorstore(chunks)
    print("Vector store created successfully!")

    return True


if __name__ == "__main__":
    if build_knowledge_base():
        print("\n Knowledge base built! Run this to start UI:")
        print("\nPYTHONPATH=. streamlit run ui/app.py\n")