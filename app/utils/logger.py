"""
Logging Configuration
"""
import logging
import sys
from typing import Optional

from app.config import settings


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Setup logger with configuration.
    
    Args:
        name: Logger name
        level: Log level (overrides config)
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Set level
    log_level = level or settings.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logger.level)
    
    # Create formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    
    # Add handler
    logger.addHandler(handler)
    
    return logger


# Default logger
default_logger = setup_logger("app")


def get_logger(name: str) -> logging.Logger:
    """
    Get logger for module.
    
    Args:
        name: Module name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
