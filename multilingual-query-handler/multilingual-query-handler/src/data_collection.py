from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
    DirectoryLoader
)
from typing import List
import os


class DataCollector:
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def load_pdfs(self, pdf_path: str):
        """Load PDF documents"""
        loader = PyPDFLoader(pdf_path)
        return loader.load()

    def load_text_files(self, directory: str):
        """Load all text files from directory"""
        loader = DirectoryLoader(
            directory,
            glob="**/*.txt",
            loader_cls=lambda path: TextLoader(path, encoding="utf-8")
        )
        return loader.load()

    def load_web_pages(self, urls: List[str]):
        """Load content from web pages"""
        loader = WebBaseLoader(urls)
        return loader.load()

    def load_all_data(self):
        """Load all available data sources"""
        documents = []

        # Load PDFs
        for file in os.listdir(self.data_dir):
            if file.endswith('.pdf'):
                docs = self.load_pdfs(os.path.join(self.data_dir, file))
                documents.extend(docs)

        # Load txt files
        txt_docs = self.load_text_files(self.data_dir)
        documents.extend(txt_docs)

        return documents
