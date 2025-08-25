viquta: could you teach me how rag works with this repo

GitHub Copilot: I'll help you understand how RAG (Retrieval-Augmented Generation) works using this repository. Let me first examine the codebase to understand the implementation and then explain the concepts. Now I'll explain how RAG (Retrieval-Augmented Generation) works using this repository as an example!

## What is RAG?

RAG is a technique that combines **retrieval** of relevant information from a knowledge base with **generation** using a Large Language Model (LLM). Instead of relying solely on the LLM's training data, RAG allows the model to access external, up-to-date information to provide more accurate and contextual responses.

## How RAG Works in This Repository

This repository demonstrates a complete RAG pipeline for querying PDF documents (board game rules for Monopoly and Ticket to Ride). Here's how it works:

### 1. **Document Processing & Chunking** (populate_database.py)

```
PDF Documents → Load → Split into Chunks → Generate Embeddings → Store in Vector DB
```

- **Load PDFs**: Uses `PyPDFDirectoryLoader` to read PDF files from the data folder
- **Text Splitting**: Uses `RecursiveCharacterTextSplitter` to break documents into smaller chunks (800 characters with 80 character overlap)
- **Why chunking?** LLMs have token limits, and smaller chunks help find more relevant information
- **Chunk IDs**: Creates unique identifiers like `"data/monopoly.pdf:6:2"` (source:page:chunk_index)

### 2. **Embedding Generation** (get_embedding_function.py)

```
Text Chunks → Embedding Model → Vector Representations
```

- Converts text chunks into numerical vectors (embeddings) that capture semantic meaning
- Currently configured for AWS Bedrock embeddings (can switch to local Ollama embeddings)
- These vectors enable semantic similarity search

### 3. **Vector Database Storage**

```
Embeddings → ChromaDB → Persistent Storage
```

- Uses ChromaDB to store embeddings with metadata
- Enables fast similarity search across document chunks
- Persists data locally in the `chroma/` directory

### 4. **Query Processing** (query_data.py)

This is where the RAG magic happens:

```
User Question → Find Similar Chunks → Build Context → Generate Answer
```

**Step by step:**
1. **Convert query to embedding**: Transform user question into a vector
2. **Similarity search**: Find the 5 most relevant document chunks using cosine similarity
3. **Build context**: Combine retrieved chunks into a context string
4. **Prompt construction**: Create a prompt with context + question
5. **Generate answer**: Send to Ollama (Mistral model) for final response

### 5. **The RAG Prompt Template**

```python
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
```

This prompt ensures the model only uses the retrieved information, not its training data.

## Key Components Explained

### Configuration (config.py)
- **CHUNK_SIZE = 800**: Optimal size for meaningful context without overwhelming the model
- **CHUNK_OVERLAP = 80**: Ensures important information isn't lost at chunk boundaries
- **SIMILARITY_SEARCH_K = 5**: Retrieves top 5 most relevant chunks

### Testing (test_rag.py)
- Validates RAG responses against expected answers
- Uses the LLM itself to evaluate if responses match expectations
- Tests specific factual questions about the board game rules

## RAG Workflow Example

Let's say you ask: *"How much money does a player start with in Monopoly?"*

1. **Query Processing**: Your question gets converted to an embedding vector
2. **Retrieval**: System searches ChromaDB for chunks about Monopoly starting money
3. **Context Building**: Finds relevant text chunks from the Monopoly PDF
4. **Generation**: Mistral LLM generates an answer based only on retrieved context
5. **Response**: Returns "$1500" with source references

## Benefits of This RAG Implementation

1. **Accuracy**: Answers are grounded in actual document content
2. **Transparency**: Shows source chunks for verification
3. **Updatable**: Add new PDFs without retraining models
4. **Cost-effective**: Uses smaller, local models (Ollama) instead of large cloud APIs
5. **Testable**: Includes automated testing for quality assurance

## Running the System

To see RAG in action:

1. **Setup**: Install dependencies and Ollama models
2. **Populate**: Run `python populate_database.py` to process PDFs
3. **Query**: Run `python query_data.py "your question"` to ask questions
4. **Test**: Run `pytest test_rag.py` to validate performance

This implementation shows how RAG can make any document collection searchable and queryable using natural language, providing a foundation you can extend to other domains and document types!