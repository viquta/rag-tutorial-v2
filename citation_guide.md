# RAG with Citations - Implementation Guide

This document explains how to enhance your RAG system with proper citations and references.

## Why Add Citations?

1. **Trustworthiness**: Users can verify facts
2. **Transparency**: Shows which sources support each claim  
3. **Academic rigor**: Proper attribution of information
4. **Debugging**: Helps identify which chunks are being retrieved

## Implementation Methods

### Method 1: Enhanced Prompt Instructions

The simplest approach is to modify your prompt template to explicitly request citations:

```python
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
```

### Method 2: Structured Context with Source Labels

Modify the context building to include source information:

```python
# Build context with source information for each chunk
context_parts = []
for i, (doc, score) in enumerate(results):
    source_id = doc.metadata.get("id", "Unknown")
    source_parts = source_id.split(":")
    if len(source_parts) >= 2:
        filename = source_parts[0].split("/")[-1]
        page_num = source_parts[1]
        source_info = f"[Source: {filename}, Page: {page_num}]"
    else:
        source_info = f"[Source: {source_id}]"
    
    context_parts.append(f"{source_info}\n{doc.page_content}")

context_text = "\n\n---\n\n".join(context_parts)
```

### Method 3: Numbered Citation System

Use numbered references for cleaner citations:

```python
# Build context with numbered sources
context_parts = []
source_mapping = {}

for i, (doc, score) in enumerate(results, 1):
    source_id = doc.metadata.get("id", f"Unknown_{i}")
    source_info = extract_source_info(source_id)
    
    source_ref = f"Source {i}: {source_info['filename']}, Page {source_info['page']}"
    source_mapping[i] = source_info
    
    context_parts.append(f"{source_ref}\nContent: {doc.page_content}")
```

## Example Output

### Before (No Citations):
```
Response: A player starts with $1500 in Monopoly.
Sources: ['data/monopoly.pdf:2:1']
```

### After (With Citations):
```
Answer: A player starts with $1500 in Monopoly [Source: monopoly.pdf, Page: 2]. This includes two $500 bills, two $100 bills, two $50 bills, six $20 bills, five $10 bills, five $5 bills, and five $1 bills [Source: monopoly.pdf, Page: 2].

Sources Referenced:
Source 1: monopoly.pdf (Page 2)
Source 2: monopoly.pdf (Page 3)

Similarity Scores: ['0.234', '0.198']
```

## Advanced Features

### 1. Multiple Citation Formats
- **Inline**: [1], [2], [3] with bibliography
- **Parenthetical**: (monopoly.pdf, p.2)
- **Academic**: (Monopoly Rules, 2023, p.2)

### 2. Confidence Scoring
Include similarity scores to show retrieval confidence:
```python
# Show how confident the retrieval was
for doc, score in results:
    confidence = "High" if score < 0.3 else "Medium" if score < 0.6 else "Low"
    print(f"Confidence: {confidence} (Score: {score:.3f})")
```

### 3. Source Quality Indicators
- Page numbers for precise reference
- Chunk indices for exact location
- Document sections if available

## Best Practices

1. **Prompt Engineering**: Be explicit about citation requirements
2. **Source Formatting**: Make citations human-readable
3. **Fallback Handling**: Handle missing metadata gracefully
4. **Consistency**: Use the same citation format throughout
5. **Verification**: Include similarity scores for transparency

## Testing Citations

Add tests to verify citation quality:

```python
def test_citation_format():
    response = query_rag_with_citations("Test question")
    assert "[Source:" in response or "[Doc:" in response
    assert "Page:" in response
```

## Integration with Existing Code

To add citations to your current system:

1. Modify `query_data.py` prompt template
2. Update context building in `query_rag()` function  
3. Add citation configuration to `config.py`
4. Update tests to verify citation presence
5. Consider creating a separate `query_data_with_citations.py` for comparison

This enhancement makes your RAG system more professional and trustworthy while maintaining the same core functionality.
