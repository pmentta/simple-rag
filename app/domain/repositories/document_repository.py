from abc import ABC, abstractmethod
from typing import List
from ..entities.document import Document

class DocumentRepository(ABC):
    @abstractmethod
    def save(self, document: Document) -> Document:
        pass

    @abstractmethod
    def search_similar(self, query_vector: List[float], limit: int = 5) -> List[Document]:
        pass
