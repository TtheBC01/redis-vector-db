from pydantic import BaseModel
from typing import List

class DocumentPayload(BaseModel):
    payload: str | List[str]

class NomicEmbedder:
    def __init__(self, documents: DocumentPayload):
        """
        Initializes the DocumentProcessor with a list of strings.

        :param documents: List of document strings.
        """
        self.documents = documents

    def search_documents(self) -> list[str]:
        """
        Prepends "search_document: " to each document in the list.
        Use this method when storing embeddings to be searched later.

        :return: List of modified document strings.
        """
        return [f"search_document: {doc}" for doc in self.documents.payload]

    def query_documents(self) -> list[str]:
        """
        Prepends "query_document: " to each document in the list.
        Use this when constructing a query against pre-embedded 
        documents

        :return: List of modified document strings.
        """
        return [f"query_document: {doc}" for doc in self.documents.payload]
    
    def cluster_documents(self) -> list[str]:
        """
        Prepends "clustering: " to each document in the list.
        Use this to imbed documents for clustering purposes.

        :return: List of modified document strings.
        """
        return [f"clustering: {doc}" for doc in self.documents.payload]
    
    def classification_documents(self) -> list[str]:
        """
        Prepends "classification: " to each document in the list.
        Use this for embedding documents that will be run through
        a classification algorithm.

        :return: List of modified document strings.
        """
        return [f"classification: {doc}" for doc in self.documents.payload]