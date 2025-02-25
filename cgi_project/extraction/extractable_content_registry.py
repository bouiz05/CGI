from enum import Enum
from typing import Type, Dict, List
from pydantic import BaseModel

class ExtractableContent:
    def __init__(self, type: str, prompt: str, schema: Type[BaseModel]):
        self.type = type
        self.prompt = prompt
        self.schema = schema
    
    def __str__(self):
        return self.name

class ExtractableContentRegistry:
    _types: Dict[str, ExtractableContent] = {}
    
    @classmethod
    def register(cls, doc_type: ExtractableContent):
        cls._types[doc_type.type] = doc_type
    
    @classmethod
    def get(cls, type: str) -> ExtractableContent:
        if type not in cls._types:
            raise ValueError(f"Unknown document type: {type}")
        return cls._types[type]
    
    @classmethod
    def get_all(cls) -> List[ExtractableContent]:
        return list(cls._types.values())

