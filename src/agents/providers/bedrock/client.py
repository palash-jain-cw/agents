import logging
from agents.core.config import settings
from functools import lru_cache
from typing import Optional
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


def validate_aws_credentials() -> bool:
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
        logger.info("Please ensure AWS credentials are set in environment variables:")
        logger.info("- AWS_ACCESS_KEY_ID")
        logger.info("- AWS_SECRET_ACCESS_KEY")
        logger.info("- AWS_REGION")
        return False
    logger.info("AWS credentials are properly set")
    return True


@lru_cache(maxsize=1)
def get_bedrock_client(
    region_name: Optional[str] = settings.AWS_DEFAULT_REGION,
) -> Optional[boto3.client]:
    """
    Get or create a singleton Bedrock client.
    Uses lru_cache to ensure only one client is created per region.

    Returns:
        Optional[boto3.client, None]: Bedrock runtime client or None if initialization fails
    """
    if not validate_aws_credentials():
        raise ValueError("AWS credentials are not properly set")

    try:
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=region_name,
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
