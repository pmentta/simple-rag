from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Document:
    id: Optional[str] # UUID
    title: str
    content: str
    metadata: dict
    created_at: Optional[datetime] = None
    embedding: Optional[List[float]] = None
