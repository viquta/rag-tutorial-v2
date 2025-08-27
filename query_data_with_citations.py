import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import re

from get_embedding_function import get_embedding_function
from config import OLLAMA_MODEL

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an expert assistant that provides accurate answers with proper citations. 

Context sources:
{context}

Question: {question}

Instructions:
1. Answer the question using ONLY the information provided in the context above
2. For each fact you state, include a citation in this format: [Doc: filename, Page: X]
3. If multiple sources support the same fact, cite all relevant sources
4. If you cannot find the answer in the provided context, say "I cannot find this information in the provided sources"
5. Be specific and accurate with your citations

Answer:"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag_with_citations(query_text)

def extract_source_info(source_id: str) -> dict:
    """Extract readable source information from the chunk ID."""
    source_parts = source_id.split(":")
    info = {
        "filename": "Unknown",
        "page": "Unknown", 
        "chunk": "Unknown"
    }
    
    if len(source_parts) >= 3:
        # Format: "data/monopoly.pdf:6:2"
        filepath = source_parts[0]
        info["filename"] = filepath.split("/")[-1] if "/" in filepath else filepath
        info["page"] = source_parts[1]
        info["chunk"] = source_parts[2]
    elif len(source_parts) >= 2:
        info["filename"] = source_parts[0]
        info["page"] = source_parts[1]
    
    return info

def query_rag_with_citations(query_text: str):
    """Enhanced RAG query with better citation handling."""
    
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)
    
    if not results:
        print("No relevant documents found.")
        return "No relevant documents found."

    # Build context with numbered sources for easy citation
    context_parts = []
    source_mapping = {}
    
    for i, (doc, score) in enumerate(results, 1):
        source_id = doc.metadata.get("id", f"Unknown_{i}")
        source_info = extract_source_info(source_id)
        
        # Create readable source reference
        source_ref = f"Source {i}: {source_info['filename']}, Page {source_info['page']}"
        source_mapping[i] = source_info
        
        context_parts.append(f"{source_ref}\nContent: {doc.page_content}")
    
    context_text = "\n\n" + "\n\n".join(context_parts)
    
    # Generate response
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    model = Ollama(model=OLLAMA_MODEL)
    response_text = model.invoke(prompt)
    
    # Format final response with source summary
    sources_summary = "\n".join([
        f"Source {i}: {info['filename']} (Page {info['page']})" 
        for i, info in source_mapping.items()
    ])
    
    formatted_response = f"""Answer: {response_text}

Sources Referenced:
{sources_summary}

Similarity Scores: {[f'{score:.3f}' for _, score in results]}"""
    
    print(formatted_response)
    return response_text

def query_rag_with_inline_citations(query_text: str):
    """Alternative version with automatic inline citation insertion."""
    
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_score(query_text, k=5)
    
    # Build context with citation markers
    context_parts = []
    citations = {}
    
    for i, (doc, score) in enumerate(results, 1):
        source_id = doc.metadata.get("id", f"Unknown_{i}")
        source_info = extract_source_info(source_id)
        
        citation_key = f"[{i}]"
        citations[i] = f"{source_info['filename']}, Page {source_info['page']}"
        
        # Add citation markers to content
        content_with_citation = f"{doc.page_content} {citation_key}"
        context_parts.append(content_with_citation)
    
    context_text = "\n\n".join(context_parts)
    
    # Enhanced prompt for inline citations
    inline_prompt = f"""
    Based on the following context with citation numbers, answer the question and include the citation numbers after relevant facts.
    
    Context:
    {context_text}
    
    Question: {query_text}
    
    Instructions: Include citation numbers [1], [2], etc. after facts from those sources.
    
    Answer:"""
    
    model = Ollama(model=OLLAMA_MODEL)
    response_text = model.invoke(inline_prompt)
    
    # Add bibliography
    bibliography = "\n\nReferences:\n" + "\n".join([
        f"[{i}] {citation}" for i, citation in citations.items()
    ])
    
    final_response = response_text + bibliography
    print(final_response)
    return response_text

if __name__ == "__main__":
    main()
