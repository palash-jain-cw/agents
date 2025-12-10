import logging
from agents.core.config import settings
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from typing import List, Type, Optional, Tuple, Dict, Any
import json
from pydantic import BaseModel
from agents.providers.bedrock.formatters import format_content_blocks
from agents.shared.utils import extract_structured_schema

logger = logging.getLogger(__name__)


class BedrockAnthropicClient:
    def __init__(
        self,
        region_name: Optional[str] = settings.AWS_DEFAULT_REGION,
        model_id: Optional[str] = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    ):
        self.region_name = region_name
        self.client = self.get_bedrock_client()
        self.model_id = model_id

    def validate_aws_credentials(self) -> bool:
        """
        Validate that required AWS credentials are set in environment variables.

        Returns:
            bool: True if credentials are properly set, False otherwise
        """
        required_vars = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_DEFAULT_REGION",
        ]
        missing_vars = [var for var in required_vars if not getattr(settings, var)]

        if missing_vars:
            logger.error(
                f"Missing required AWS environment variables: {', '.join(missing_vars)}"
            )
            logger.info(
                "Please ensure AWS credentials are set in environment variables:"
            )
            logger.info("- AWS_ACCESS_KEY_ID")
            logger.info("- AWS_SECRET_ACCESS_KEY")
            logger.info("- AWS_REGION")
            return False
        logger.info("AWS credentials are properly set")
        return True

    def get_bedrock_client(
        self,
    ) -> Optional[boto3.client]:
        """
        Get or create a singleton Bedrock client.
        Uses lru_cache to ensure only one client is created per region.

        Returns:
            Optional[boto3.client, None]: Bedrock runtime client or None if initialization fails
        """
        if not self.validate_aws_credentials():
            raise ValueError("AWS credentials are not properly set")

        try:
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=self.region_name,
            )
            # Increase read timeout for longer responses; modest connect timeout and retries
            client_config = Config(
                read_timeout=180,
                connect_timeout=10,
                retries={"max_attempts": 3, "mode": "standard"},
            )
            return session.client(service_name="bedrock-runtime", config=client_config)
        except (ClientError, NoCredentialsError) as e:
            logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            raise e

    def query(
        self,
        cached_content: Optional[List[str]] = None,
        variable_content: Optional[List[str]] = None,
        schema: Optional[Type[BaseModel]] = None,
        max_tokens: Optional[int] = 1000,
        temperature: Optional[float] = 0.5,
    ) -> Tuple[str, dict]:
        content_blocks = format_content_blocks(cached_content, variable_content, schema)
        logger.info(
            f"Invoking model {self.model_id} with {len(content_blocks)} content blocks"
        )
        payload: Dict[str, Any] = {
            "messages": [
                {
                    "role": "user",
                    "content": content_blocks,
                }
            ],
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json",
        )
        logger.debug(f"Response: {response}")
        result = json.loads(response["body"].read())
        response_text = result.get("content", [{"text": ""}])[0].get("text", "")
        usage = result.get("usage", {})
        logger.debug(f"Usage: {usage}")
        if schema is not None:
            logger.debug(
                f"Extracting structured response for schema: {schema.__name__}"
            )
            structured_response = extract_structured_schema(response_text, schema)
            logger.debug(f"Structured response: {structured_response}")
            return structured_response, usage
        else:
            return response_text, usage
