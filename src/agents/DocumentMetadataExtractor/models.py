from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum


class DocumentType(str, Enum):
    SOP = "SOP"
    WP = "Working Practice"
    FORM = "Form"
    OTHER = "Other"


class DocumentMetadataRequest(BaseModel):
    """Document metadata request model"""

    document_text: str = Field(..., description="The text of the document")
    domain_context: Optional[dict] = Field(
        None, description="The context of the document domain"
    )


class DocumentMetadataResponse(BaseModel):
    """Document metadata model"""

    title: str = Field(..., description="The document's title/name")
    description: Optional[str] = Field(
        None,
        description="A brief summary of the document describing the processes, activities, and procedures covered by the document.",
    )
    department: Optional[str] = Field(
        None, description="The department responsible for the document"
    )
    domain: Optional[str] = Field(
        None,
        description="The document domain based on its content and the provided domain context. The domain can only be from the keys of the domain context dictionary.",
    )
    document_number: Optional[str] = Field(
        None, description="The unique identifier for this document"
    )
    document_type: DocumentType = Field(
        ...,
        description="The type of document (e.g., SOP, Policy, Manual, Guideline, Form, Other)",
    )
    document_category: Optional[Literal["Control", "Supplemental"]] = Field(
        None,
        description="The category of the document (e.g., Control, Supplemental)",
    )
    author: Optional[str] = Field(
        None, description="The person or role responsible for creating the document"
    )
    version: Optional[str] = Field(
        None, description="The current version number of the document"
    )
    effective_date: Optional[str] = Field(
        None,
        description="The date from which this version is effective (in ISO format YYYY-MM-DD)",
    )
    scope: Optional[str] = Field(
        None, description="The boundaries and applicability of this document"
    )
