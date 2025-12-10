from typing import List, Type, Optional
import json
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def format_cache_block(
    cached_content: Optional[List[str]] = None,
    cache_control: Optional[str] = "ephemeral",
) -> List[dict]:
    if cached_content is None:
        return []
    else:
        return [
            {
                "type": "text",
                "text": cached_block,
                "cache_control": {"type": cache_control},
            }
            for cached_block in cached_content
        ]


def format_variable_block(variable_content: Optional[List[str]] = None) -> List[dict]:
    if variable_content is None:
        return []
    else:
        return [
            {
                "type": "text",
                "text": variable_block,
            }
            for variable_block in variable_content
        ]


def format_structured_schema(schema: Optional[Type[BaseModel]] = None) -> dict:
    if schema is None:
        return []
    else:
        schema_json = json.dumps(schema.model_json_schema(), indent=2)
        schema_block = f"Adhere strictly to the below output schema:\n\n{schema_json}"
        logger.debug(
            f"Added schema definition to cached content blocks: {schema.__name__}"
        )
        return [
            {
                "type": "text",
                "text": schema_block,
                "cache_control": {"type": "ephemeral"},
            }
        ]


def format_content_blocks(
    cached_content: Optional[List[str]] = None,
    variable_content: Optional[List[str]] = None,
    schema: Optional[Type[BaseModel]] = None,
) -> List[dict]:
    logger.debug(
        f"Formatting content blocks with {len(cached_content) + (1 if schema is not None else 0)} cached content blocks and {len(variable_content)} variable content blocks"
    )
    return (
        format_cache_block(cached_content)
        + format_structured_schema(schema)
        + format_variable_block(variable_content)
    )
