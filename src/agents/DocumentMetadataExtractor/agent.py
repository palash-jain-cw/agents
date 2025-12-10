from agents.core.base import Agent
from agents.DocumentMetadataExtractor.models import (
    DocumentMetadataRequest,
    DocumentMetadataResponse,
)
from agents.DocumentMetadataExtractor.prompts import (
    document_metadata_extraction_instructions,
)
from typing import Type
from pydantic import BaseModel


class DocumentMetadataExtractor(Agent):
    def __init__(
        self,
        name: str = "DocumentMetadataExtractor",
        description: str = "Extract metadata from a document",
        instructions: str = document_metadata_extraction_instructions,
        request_model: Type[BaseModel] = DocumentMetadataRequest,
        response_model: Type[BaseModel] = DocumentMetadataResponse,
    ):
        super().__init__(
            name=name,
            description=description,
            instructions=instructions,
            request_model=request_model,
            response_model=response_model,
        )

    def format_request(self, request: DocumentMetadataRequest) -> str:
        cached_content = [self.instructions]
        variable_content = [
            f"Here is the document text: {request.document_text}. Here is the domain context: {request.domain_context}."
        ]
        return cached_content, variable_content

    def run(self, request: DocumentMetadataRequest) -> DocumentMetadataResponse:
        return super().run(request)
