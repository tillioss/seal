import os
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

class RAGEngine:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

    def load_knowledge_base(self, docs_dir="knowledge_base"):
        vector_store_path = "vector_store.pkl"
        if os.path.exists(vector_store_path):
            with open(vector_store_path, "rb") as f:
                self.vector_store = pickle.load(f)
            return True
        return False

    def create_knowledge_base(self, templates):
        documents = []
        for template in templates:
            documents.append(Document(
                page_content=template["content"],
                metadata={"type": template["type"]}
            ))

        splits = self.text_splitter.split_documents(documents)
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        
        with open("vector_store.pkl", "wb") as f:
            pickle.dump(self.vector_store, f)

    def get_intervention_context(self, batch):
        if not self.vector_store:
            raise ValueError("Knowledge base not initialized")
        
        query = self._create_search_query(batch)
        docs = self.vector_store.similarity_search(query, k=3)
        return [doc.page_content for doc in docs]

    def _create_search_query(self, batch):
        # Handle the new data structure with EMT-specific scores
        scores = batch['scores']
        deficient_area = batch['metadata']['deficient_area']
        
        # Calculate average for the deficient area
        deficient_scores = [float(score) for score in scores[deficient_area]]
        avg_score = sum(deficient_scores) / len(deficient_scores)
        
        return f"intervention strategies for {deficient_area} with average score {avg_score:.2f}"