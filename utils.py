"""
Utility functions for the RAG system.
"""

import os
import logging
from typing import Optional

def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_file_exists(file_path: str) -> bool:
    """Validate that a file exists."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return False
    return True

def validate_directory_exists(dir_path: str, create_if_missing: bool = False) -> bool:
    """Validate that a directory exists, optionally create it."""
    if not os.path.exists(dir_path):
        if create_if_missing:
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Created directory: {dir_path}")
            return True
        else:
            logging.error(f"Directory not found: {dir_path}")
            return False
    return True

def check_ollama_connection() -> bool:
    """Check if Ollama is running and accessible."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Failed to connect to Ollama: {e}")
        return False
