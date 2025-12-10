import logging
from typing import Optional


def configure_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None,
) -> None:
    """
    Configure logging for the agents package.
    
    This function sets up a centralized logging configuration that will be used
    throughout the package. It only configures logging if no handlers are already
    configured, preventing duplicate handlers.
    
    Args:
        level: Logging level (default: logging.INFO)
        format_string: Custom format string for log messages
        date_format: Custom date format string
    """
    # Only configure if no handlers are already set up
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return
    
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    
    logging.basicConfig(
        level=level,
        format=format_string,
        datefmt=date_format,
        force=True,  # Override any existing configuration
    )


# Configure logging when the module is imported
configure_logging()


