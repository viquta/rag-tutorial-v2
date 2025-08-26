import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from get_embedding_function import get_embedding_function
from config import OLLAMA_MODEL

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context. When stating facts, include citations in square brackets referring to the source document and page.

Context with sources:
{context}

---

Answer the question based on the above context: {question}

Instructions:
- Include citations like [Source: document_name, Page: X] after each fact
- Be specific about which source supports each claim
- If multiple sources support the same fact, cite all relevant sources
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    # Build context with source information for each chunk
    context_parts = []
    for i, (doc, score) in enumerate(results):
        source_id = doc.metadata.get("id", "Unknown")
        source_parts = source_id.split(":")
        if len(source_parts) >= 2:
            filename = source_parts[0].split("/")[-1] if "/" in source_parts[0] else source_parts[0]
            page_num = source_parts[1]
            source_info = f"[Source: {filename}, Page: {page_num}]"
        else:
            source_info = f"[Source: {source_id}]"
        
        context_parts.append(f"{source_info}\n{doc.page_content}")
    
    context_text = "\n\n---\n\n".join(context_parts)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = OllamaLLM(model=OLLAMA_MODEL)
    response_text = model.invoke(prompt)

    # Extract and format sources for display
    sources = []
    for doc, score in results:
        source_id = doc.metadata.get("id", "Unknown")
        source_parts = source_id.split(":")
        if len(source_parts) >= 2:
            filename = source_parts[0].split("/")[-1] if "/" in source_parts[0] else source_parts[0]
            page_num = source_parts[1]
            sources.append(f"{filename} (Page {page_num})")
        else:
            sources.append(source_id)
    
    formatted_response = f"Response: {response_text}\n\nSources used: {', '.join(sources)}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
