#!/usr/bin/env python3
"""
Setup script for the RAG tutorial project.
"""

import subprocess
import sys
import os
from utils import setup_logging, validate_directory_exists, check_ollama_connection

def install_requirements():
    """Install Python requirements."""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def check_ollama_setup():
    """Check if Ollama is properly set up."""
    print("Checking Ollama setup...")
    
    if not check_ollama_connection():
        print("❌ Ollama is not running. Please install and start Ollama:")
        print("   1. Download from https://ollama.ai")
        print("   2. Start Ollama")
        print("   3. Run: ollama pull mistral")
        print("   4. Run: ollama pull nomic-embed-text")
        return False
    
    print("✅ Ollama is running")
    return True

def setup_directories():
    """Create necessary directories."""
    print("Setting up directories...")
    validate_directory_exists("data", create_if_missing=True)
    validate_directory_exists("chroma", create_if_missing=True)
    print("✅ Directories set up")

def main():
    """Main setup function."""
    setup_logging()
    print("🚀 Setting up RAG Tutorial V2...")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Check Ollama
    check_ollama_setup()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add PDF files to the 'data' directory")
    print("2. Run: python populate_database.py")
    print("3. Run: python query_data.py 'Your question here'")

if __name__ == "__main__":
    main()
