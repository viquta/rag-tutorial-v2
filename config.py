"""
Configuration settings for the RAG system.
"""

# Database settings
CHROMA_PATH = "chroma"
DATA_PATH = "data"

# Text splitting settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 80

# Retrieval settings
SIMILARITY_SEARCH_K = 5

# Model settings
OLLAMA_MODEL = "gpt-oss:20b"
EMBEDDING_MODEL = "nomic-embed-text"

# AWS Bedrock settings (if using Bedrock)
AWS_REGION = "us-east-1"
AWS_PROFILE = "default"

# Citation settings
INCLUDE_CITATIONS = True
CITATION_FORMAT = "numbered"  # Options: "numbered", "inline", "bibliography"
SHOW_SIMILARITY_SCORES = False
MAX_CITATION_LENGTH = 50
