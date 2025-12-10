from typing import Type
import json
import logging
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


def extract_structured_schema(
    response_text: str, schema: Type[BaseModel]
) -> Type[BaseModel]:
    # Try to extract and validate JSON
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON object found in response")

    json_str = response_text[start:end]
    try:
        parsed_json = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in response: {e}")

    try:
        structured = schema(**parsed_json)
    except ValidationError as e:
        raise e

    logger.debug(
        f"Successfully parsed and validated structured output with schema: {schema.__name__} "
    )
    return structured
