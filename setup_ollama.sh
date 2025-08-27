#!/bin/bash

# RAG Tutorial v2 - Ollama Setup Script

echo "🚀 Setting up RAG Tutorial with Ollama..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it from https://ollama.ai"
    exit 1
fi

echo "✅ Ollama found"

# Pull required models
echo "📥 Pulling Mistral model (for text generation)..."
ollama pull mistral

echo "📥 Pulling nomic-embed-text model (for embeddings)..."
ollama pull nomic-embed-text

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🗃️ Populating vector database..."
python populate_database.py

echo "✅ Setup complete! You can now query the system with:"
echo "python query_data.py 'Your question here'"
echo ""
echo "Example:"
echo "python query_data.py 'What are the rules of Monopoly?'"
