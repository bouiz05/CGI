from abc import ABC, abstractmethod
from openai import OpenAI
from extraction.file_parser import FileParser
from extraction.extractable_content_registry import ExtractableContent
from django.conf import settings
from pydantic import BaseModel
from django.core.files.uploadedfile import UploadedFile

class ExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, file: UploadedFile, extractable_content: ExtractableContent) -> BaseModel:
        pass

class LlamaParseStrategy(ExtractionStrategy):
    def __init__(self):
        self.parser = FileParser()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract(self, file: UploadedFile, extractable_content: ExtractableContent) -> BaseModel:
        content = self.parser.parse(file.read(), file.name)

        response = self.client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": extractable_content.prompt
                    },
                    {
                        "role": "user", 
                        "content": content
                    }
                ],
                response_format=extractable_content.schema
            )
        
        return response.choices[0].message.parsed
    
class VisionStrategy(ExtractionStrategy):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _convert_pdf_to_images(self, pdf_bytes: bytes) -> bytes:
        pass

    def extract(self, file: UploadedFile, extractable_content: ExtractableContent) -> BaseModel:
        pass
         

