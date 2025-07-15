# Enhanced Document Retriever - SELECT Pillar

This module provides an enhanced document retrieval system for the SELECT pillar of the context engineering pipeline. It integrates with real document sources and provides advanced search capabilities.

## Features

### 🔍 Multiple Document Sources
- **PDF parsing** using PyPDF2 and pdfplumber
- **API integration** for corporate knowledge bases
- **File system** document scanning
- **Vector search** for semantic similarity

### 🚀 Advanced Search Capabilities
- **ChromaDB vector database** for similarity search
- **Semantic search** using sentence transformers
- **Hybrid search** combining keyword and vector search
- **Multi-source search** across different document types

### ⚡ Performance Optimization
- **Caching layer** using diskcache for fast retrieval
- **Async/await** support for concurrent processing
- **Connection pooling** for API requests
- **Batch processing** for bulk operations

### 🛡️ Comprehensive Error Handling
- **Graceful degradation** when sources are unavailable
- **Retry mechanisms** for API failures
- **Logging** with structured output
- **Fallback strategies** for document parsing

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. Initialize the system:
```python
from src.select.integration_layer import get_integration

async def main():
    integration = await get_integration()
    print("System initialized successfully!")
```

## Quick Start

### Basic Usage

```python
import asyncio
from src.select.enhanced_document_retriever import EnhancedDocumentRetriever

async def main():
    # Initialize retriever
    retriever = EnhancedDocumentRetriever(
        pdf_directory="./documents/pdfs",
        api_base_url="https://your-api.com",
        api_key="your-api-key"
    )
    
    # Search for documents
    results = await retriever.search_documents("quarterly sales report", limit=5)
    
    for doc in results:
        print(f"Title: {doc.metadata.title}")
        print(f"Source: {doc.metadata.source}")
        print(f"Content: {doc.content[:200]}...")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
```

### Integration with Context Engineering Pipeline

```python
from src.select.integration_layer import DocumentRetrieverIntegration

async def main():
    integration = DocumentRetrieverIntegration()
    await integration.initialize()
    
    # Get relevant documents for context
    user_query = "What were our Q3 sales results?"
    user_profile = {"role": "Product Manager", "department": "Sales"}
    
    documents = await integration.get_relevant_documents(user_query, user_profile)
    
    for doc in documents:
        print(doc)
```

## Configuration

### Environment Variables

```bash
# Core settings
PDF_DIRECTORY=./documents/pdfs
API_BASE_URL=https://your-knowledge-base.com
API_KEY=your-api-key-here

# Vector database
VECTOR_DB_DIR=./chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Cache settings
CACHE_DIR=./cache
CACHE_ENABLED=true

# Logging
LOG_LEVEL=INFO
DEBUG_MODE=false
```

### Configuration File

Create a `config.json` file:

```json
{
  "pdf": {
    "pdf_directory": "./documents/pdfs",
    "max_file_size_mb": 50,
    "preferred_extractor": "pdfplumber"
  },
  "vector_search": {
    "collection_name": "documents",
    "embedding_model": "all-MiniLM-L6-v2",
    "chunk_size": 500,
    "similarity_threshold": 0.3
  },
  "api": {
    "base_url": "https://your-api.com",
    "api_key": "your-api-key",
    "timeout": 30
  },
  "cache": {
    "enabled": true,
    "max_size_mb": 1000,
    "document_ttl": 3600
  }
}
```

Load configuration:

```python
from src.select.config import DocumentRetrieverConfig

config = DocumentRetrieverConfig.load_from_file("config.json")
```

## Document Sources

### PDF Documents

Place PDF files in your configured PDF directory:

```python
# Add a PDF document
await integration.add_document_from_file("./documents/sales_report.pdf")

# Retrieve PDF content
doc = await integration.get_document("sales_report")
```

### API Integration

Configure your API source:

```python
from src.select.enhanced_document_retriever import APIDocumentSource

api_source = APIDocumentSource(
    base_url="https://your-knowledge-base.com",
    api_key="your-api-key",
    headers={"Custom-Header": "value"}
)

# The API should support these endpoints:
# GET /documents/{id} - Retrieve document by ID
# GET /search?q={query}&limit={limit} - Search documents
# GET /documents?limit={limit} - List documents
```

### Vector Search

The system automatically indexes documents for vector search:

```python
# Search using semantic similarity
results = await retriever.search_documents("financial performance metrics", limit=10)

# Results are ranked by similarity score
for doc in results:
    print(f"Similarity score: {doc.similarity_score}")
    print(f"Content: {doc.content}")
```

## Advanced Features

### Custom Document Sources

Create custom document sources:

```python
from src.select.enhanced_document_retriever import DocumentSource

class CustomDocumentSource(DocumentSource):
    async def retrieve_document(self, document_id: str) -> Optional[Document]:
        # Implement custom retrieval logic
        pass
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Document]:
        # Implement custom search logic
        pass
```

### Caching Strategies

Control caching behavior:

```python
# Disable cache for specific request
doc = await retriever.retrieve_document("doc_id", use_cache=False)

# Clear cache
await integration.clear_cache()

# Configure cache settings
config.cache.document_ttl = 7200  # 2 hours
config.cache.search_ttl = 900     # 15 minutes
```

### Performance Monitoring

Get system statistics:

```python
stats = await integration.get_system_stats()
print(f"Total documents: {stats['total_documents']}")
print(f"Cache size: {stats['cache_size']}")
print(f"Sources available: {stats['sources_available']}")
```

## API Reference

### EnhancedDocumentRetriever

Main class for document retrieval:

```python
class EnhancedDocumentRetriever:
    def __init__(self, pdf_directory: str, api_base_url: str = None, ...):
        """Initialize the document retriever."""
    
    async def retrieve_document(self, document_id: str, use_cache: bool = True) -> Optional[Document]:
        """Retrieve a document by ID."""
    
    async def search_documents(self, query: str, limit: int = 10, use_cache: bool = True) -> List[Document]:
        """Search for documents using vector similarity."""
    
    async def add_document_to_index(self, document: Document) -> bool:
        """Add a document to the vector index."""
```

### DocumentRetrieverIntegration

Integration layer for the context engineering pipeline:

```python
class DocumentRetrieverIntegration:
    async def initialize(self) -> bool:
        """Initialize the integration."""
    
    async def get_document(self, document_id: str) -> Optional[str]:
        """Get a document by ID (legacy interface)."""
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search documents and return structured results."""
    
    async def get_relevant_documents(self, query: str, context: Optional[str] = None) -> List[str]:
        """Get relevant documents for context engineering."""
```

## Error Handling

The system provides comprehensive error handling:

```python
# Graceful degradation
try:
    doc = await retriever.retrieve_document("doc_id")
except Exception as e:
    logger.error(f"Document retrieval failed: {e}")
    # Fall back to alternative source or cached data

# API failures
try:
    results = await api_source.search_documents("query")
except httpx.HTTPStatusError as e:
    logger.error(f"API request failed: {e.response.status_code}")
    # Use local search or cached results
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest src/select/test_enhanced_retriever.py -v

# Run specific test categories
pytest src/select/test_enhanced_retriever.py::TestEnhancedDocumentRetriever -v
pytest src/select/test_enhanced_retriever.py::TestPerformanceBenchmarks -v

# Run with coverage
pytest src/select/test_enhanced_retriever.py --cov=src.select --cov-report=html
```

## Performance Considerations

### Optimization Tips

1. **Batch Operations**: Process multiple documents in batches
2. **Connection Pooling**: Use connection pooling for API requests
3. **Caching**: Enable caching for frequently accessed documents
4. **Chunking**: Optimize chunk sizes for your document types
5. **Indexing**: Pre-index documents during off-peak hours

### Monitoring

Monitor system performance:

```python
# Enable performance metrics
config.performance.enable_metrics = True

# Monitor concurrent operations
config.performance.concurrent_pdf_processing = 3
config.performance.concurrent_api_requests = 5
```

## Migration from Legacy System

To migrate from the legacy document retriever:

1. **Backward Compatibility**: The system provides legacy functions:
   ```python
   # Legacy function still works
   content = await get_q3_sales_performance_pdf()
   
   # Enhanced version with search capabilities
   content = await get_enhanced_q3_sales_performance_pdf()
   ```

2. **Gradual Migration**: Replace calls incrementally:
   ```python
   # Old way
   from src.select.document_retriever import get_q3_sales_performance_pdf
   
   # New way
   from src.select.integration_layer import get_integration
   integration = await get_integration()
   content = await integration.get_document("q3_sales_performance")
   ```

3. **Enhanced Features**: Access new capabilities:
   ```python
   # Search across all documents
   results = await integration.search_documents("sales performance")
   
   # Get contextual documents
   docs = await integration.get_relevant_documents("Q3 results", "sales context")
   ```

## Troubleshooting

### Common Issues

1. **ChromaDB Connection**: Ensure ChromaDB directory is writable
2. **PDF Parsing**: Install both PyPDF2 and pdfplumber for best results
3. **API Timeouts**: Increase timeout values for slow APIs
4. **Memory Usage**: Monitor vector database size and use appropriate chunk sizes

### Debug Mode

Enable debug mode for detailed logging:

```python
config.debug_mode = True
config.logging.log_level = "DEBUG"
```

### Validation

Validate your configuration:

```python
issues = config.validate_environment()
if issues:
    for issue in issues:
        print(f"Issue: {issue}")
```

## Contributing

To contribute to the enhanced document retriever:

1. Follow the existing code style with type hints and docstrings
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure backward compatibility where possible

## License

This module is part of the context engineering pipeline and follows the same license terms as the parent project.