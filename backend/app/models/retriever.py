import faiss
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import Config
import pickle

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(Config.SENTENCE_TRANSFORMER_MODEL)
        self.index_path = "faiss_index.bin"
        self.docs_path = "documents.pkl"
        self.index = faiss.IndexFlatL2(384)  
        self.documents = []

        self.load_index()

    def add_documents(self, documents):
        print(f"Before adding: {self.index.ntotal} documents in index")
        self.documents.extend(documents)
        embeddings = np.array(self.model.encode(documents)).astype('float32')
        self.index.add(embeddings)

        self.save_index()
        print(f"After adding: {self.index.ntotal} documents in index")

    def retrieve(self, query, k=3):
        if self.index.ntotal == 0:
            print("Warning: No documents in index!")
            return []

        query_embedding = np.array(self.model.encode([query])).astype('float32')
        distances, indices = self.index.search(query_embedding, k)

        print(f"Retrieved indices: {indices[0]}")
        return indices[0]

    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.docs_path, "wb") as f:
            pickle.dump(self.documents, f)
        print("FAISS index and documents saved.")

    def load_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            if os.path.exists(self.docs_path):
                with open(self.docs_path, "rb") as f:
                    self.documents = pickle.load(f)
            print("FAISS index and documents loaded.")
