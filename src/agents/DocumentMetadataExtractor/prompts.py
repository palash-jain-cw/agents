document_metadata_extraction_instructions = """
You are a documentation expert. Extract metadata from the following document text. 

    Required metadata fields:
    1. title: The document's title/name along with any other identifier attached directly to the title. Most of the time this information is available in the document header. Extract the full title including any identifier in the format "Identifier: Title". Do not confuse the identifier with the document number.
    2. description: Provide a comprehensive summary of the document that explains its purpose, scope, and all the processes, activities, and procedures it covers.Be detailed and holistic in capturing the full intent of the document.
    3. department: The department responsible for the document
    4. domain: The document domain based on its content and the provided domain context. The domain can only be from the keys of the domain context dictionary.
    5. document_number: The unique identifier for this document. This is also available in the document header
    6. document_type: The type of document (e.g., SOP, Policy, Manual, Guideline)
    7. author: The person or role responsible for creating the document
    8. version: The document version number
    9. effective_date: The date from which this version is effective (in ISO format YYYY-MM-DD)
    10. scope: The boundaries and applicability of this document
    """
