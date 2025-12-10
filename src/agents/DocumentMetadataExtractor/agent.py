from agents.core.base import SingleTurnAgent
from agents.DocumentMetadataExtractor.models import (
    DocumentMetadataRequest,
    DocumentMetadataResponse,
    DocumentMetadataFeedback,
)
from agents.core.models import Draft
from agents.DocumentMetadataExtractor.prompts import (
    document_metadata_extraction_instructions,
)
from typing import Optional
from pydantic import BaseModel
import json


class DocumentMetadataExtractor(SingleTurnAgent):
    def __init__(
        self,
        name: str = "DocumentMetadataExtractor",
        description: str = "Extract metadata from a document",
        instructions: str = document_metadata_extraction_instructions,
        request_model: BaseModel = DocumentMetadataRequest,
        response_model: BaseModel = DocumentMetadataResponse,
        feedback_model: BaseModel = DocumentMetadataFeedback,
    ):
        super().__init__(
            name=name,
            description=description,
            instructions=instructions,
            request_model=request_model,
            response_model=response_model,
            feedback_model=feedback_model,
        )

    def format_previous_draft(self, previous_draft: Draft) -> str:
        feedback_text = f"""
        Here is the previous attempt at generating the response:

        {json.dumps(previous_draft.draft.model_dump(), indent=2)}
        
        Here is the feedback for the previous attempt:
        
        {json.dumps(previous_draft.feedback.model_dump_json(indent=2))}
        """
        return feedback_text

    def format_request(
        self,
        request: DocumentMetadataRequest,
        previous_draft: Optional[DocumentMetadataResponse] = None,
    ) -> str:
        cached_content = [self.instructions]
        variable_content = [
            f"Here is the document text: {request.document_text}. Here is the domain context: {request.domain_context}."
        ]
        if previous_draft is not None:
            variable_content.append(self.format_previous_draft(previous_draft))
        return cached_content, variable_content

    def run(
        self,
        request: DocumentMetadataRequest,
        previous_draft: Optional[DocumentMetadataResponse] = None,
    ) -> DocumentMetadataResponse:
        return super().run(request, previous_draft)
