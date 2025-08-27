# RAG Tutorial V2

A Retrieval-Augmented Generation (RAG) system that enables querying PDF documents using LangChain, ChromaDB, and Ollama.

## Features

- PDF document processing and chunking
- Vector database storage with ChromaDB
- Question-answering using Ollama LLM
- Automated testing with evaluation prompts

## Setup

### Option 1: Quick Setup (Recommended)
Run the automated setup script:
```bash
chmod +x setup_ollama.sh
./setup_ollama.sh
```

### Option 2: Manual Setup

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

3. Populate the database with PDF documents:
```bash
python populate_database.py
```

## Usage

1. Query the system:
```bash
python query_data.py "Your question here"
```

2. Example queries:
```bash
python query_data.py "What are the rules of Monopoly?"
python query_data.py "How do you win at Ticket to Ride?"
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
