# RAG Tutorial V2

A Retrieval-Augmented Generation (RAG) system that enables querying PDF documents using LangChain, ChromaDB, and Ollama.

## Features

- PDF document processing and chunking
- Vector database storage with ChromaDB
- Question-answering using Ollama LLM
- Automated testing with evaluation prompts

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install and set up Ollama:
   - Download from [ollama.ai](https://ollama.ai)
   - Pull the required models:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

3. Configure embeddings:
   - For AWS Bedrock: Set up AWS credentials
   - For local Ollama: Uncomment the Ollama embeddings in `get_embedding_function.py`

## Usage

1. Populate the database with PDF documents:
```bash
python populate_database.py
```

2. Query the system:
```bash
python query_data.py "Your question here"
```

3. Run tests:
```bash
pytest test_rag.py
```

## Project Structure

- `data/` - PDF documents to be processed
- `get_embedding_function.py` - Embedding configuration
- `populate_database.py` - Database population script
- `query_data.py` - Query interface
- `test_rag.py` - Automated tests
- `chroma/` - Vector database storage (auto-generated)

## Configuration

Edit `get_embedding_function.py` to switch between:
- AWS Bedrock embeddings (default)
- Local Ollama embeddings (commented out)
