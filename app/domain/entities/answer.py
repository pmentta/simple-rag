from dataclasses import dataclass
from typing import List
from .document import Document

@dataclass
class Answer:
    text: str
    sources: List[Document]
