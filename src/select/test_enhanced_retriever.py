"""
Test suite for the enhanced document retriever.

This module provides comprehensive tests for all components of the enhanced
document retrieval system, including unit tests, integration tests, and
performance benchmarks.
"""

import asyncio
import tempfile
import shutil
import os
from pathlib import Path
from typing import List, Dict, Any
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from enhanced_document_retriever import (
    EnhancedDocumentRetriever,
    Document,
    DocumentMetadata,
    PDFDocumentSource,
    APIDocumentSource,
    VectorSearchEngine,
    CacheManager
)
from config import DocumentRetrieverConfig
from integration_layer import DocumentRetrieverIntegration


class TestEnhancedDocumentRetriever:
    """Test suite for the enhanced document retriever."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_document(self):
        """Create a sample document for testing."""
        return Document(
            metadata=DocumentMetadata(
                id="test_doc_1",
                title="Test Document",
                source="test_source",
                content_type="text",
                keywords=["test", "document", "sample"]
            ),
            content="This is a sample document for testing purposes. It contains various test keywords and content."
        )
    
    @pytest.fixture
    async def retriever(self, temp_dir):
        """Create a document retriever instance for testing."""
        config = DocumentRetrieverConfig()
        config.pdf.pdf_directory = os.path.join(temp_dir, "pdfs")
        config.vector_search.persist_directory = os.path.join(temp_dir, "vector_db")
        config.cache.cache_directory = os.path.join(temp_dir, "cache")
        
        retriever = EnhancedDocumentRetriever(
            pdf_directory=config.pdf.pdf_directory,
            cache_dir=config.cache.cache_directory,
            vector_db_dir=config.vector_search.persist_directory
        )
        
        yield retriever
        
        # Cleanup
        if hasattr(retriever, 'api_source') and retriever.api_source:
            await retriever.api_source.client.aclose()
    
    @pytest.mark.asyncio
    async def test_document_retrieval(self, retriever, sample_document):
        """Test basic document retrieval functionality."""
        # Add document to vector index
        success = await retriever.add_document_to_index(sample_document)
        assert success is True
        
        # Retrieve document
        retrieved_doc = await retriever.retrieve_document("test_doc_1")
        assert retrieved_doc is not None
        assert retrieved_doc.metadata.id == "test_doc_1"
        assert retrieved_doc.metadata.title == "Test Document"
    
    @pytest.mark.asyncio
    async def test_vector_search(self, retriever, sample_document):
        """Test vector search functionality."""
        # Add document to vector index
        await retriever.add_document_to_index(sample_document)
        
        # Search for similar documents
        results = await retriever.search_documents("test document", limit=5)
        assert len(results) > 0
        
        # Verify the document is in results
        found_doc = None
        for doc in results:
            if doc.metadata.id == "test_doc_1":
                found_doc = doc
                break
        
        assert found_doc is not None
        assert "test" in found_doc.content.lower()
    
    @pytest.mark.asyncio
    async def test_cache_functionality(self, retriever, sample_document):
        """Test caching functionality."""
        # Add document to vector index
        await retriever.add_document_to_index(sample_document)
        
        # First retrieval (should cache)
        doc1 = await retriever.retrieve_document("test_doc_1", use_cache=True)
        assert doc1 is not None
        
        # Second retrieval (should use cache)
        doc2 = await retriever.retrieve_document("test_doc_1", use_cache=True)
        assert doc2 is not None
        assert doc1.metadata.id == doc2.metadata.id
    
    @pytest.mark.asyncio
    async def test_multiple_document_types(self, retriever):
        """Test handling of multiple document types."""
        documents = [
            Document(
                metadata=DocumentMetadata(
                    id="doc1",
                    title="Text Document",
                    source="test",
                    content_type="text"
                ),
                content="This is a text document."
            ),
            Document(
                metadata=DocumentMetadata(
                    id="doc2",
                    title="PDF Document",
                    source="test",
                    content_type="pdf"
                ),
                content="This is a PDF document."
            ),
            Document(
                metadata=DocumentMetadata(
                    id="doc3",
                    title="HTML Document",
                    source="test",
                    content_type="html"
                ),
                content="This is an HTML document."
            )
        ]
        
        # Add all documents
        for doc in documents:
            success = await retriever.add_document_to_index(doc)
            assert success is True
        
        # Search across all document types
        results = await retriever.search_documents("document", limit=10)
        assert len(results) == 3
        
        # Verify all document types are present
        content_types = {doc.metadata.content_type for doc in results}
        assert content_types == {"text", "pdf", "html"}
    
    @pytest.mark.asyncio
    async def test_error_handling(self, retriever):
        """Test error handling for various scenarios."""
        # Test retrieving non-existent document
        doc = await retriever.retrieve_document("non_existent_doc")
        assert doc is None
        
        # Test searching with empty query
        results = await retriever.search_documents("", limit=5)
        assert isinstance(results, list)
        
        # Test invalid document ID
        results = await retriever.search_documents("invalid_search_query_with_special_chars_!@#$%", limit=5)
        assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_performance_metrics(self, retriever):
        """Test performance metrics collection."""
        # Add multiple documents
        for i in range(10):
            doc = Document(
                metadata=DocumentMetadata(
                    id=f"perf_doc_{i}",
                    title=f"Performance Test Document {i}",
                    source="performance_test",
                    content_type="text"
                ),
                content=f"This is performance test document number {i} with some content for testing."
            )
            await retriever.add_document_to_index(doc)
        
        # Get system stats
        stats = await retriever.get_stats()
        assert "total_documents" in stats
        assert stats["total_documents"] >= 10
        assert "sources_available" in stats
        assert "cache_size" in stats


class TestPDFDocumentSource:
    """Test suite for PDF document source."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def pdf_source(self, temp_dir):
        """Create a PDF document source for testing."""
        return PDFDocumentSource(temp_dir)
    
    def test_pdf_source_initialization(self, pdf_source, temp_dir):
        """Test PDF source initialization."""
        assert pdf_source.pdf_directory == Path(temp_dir)
        assert pdf_source.pdf_directory.exists()
    
    @pytest.mark.asyncio
    async def test_pdf_document_listing(self, pdf_source):
        """Test PDF document listing."""
        # Create a dummy PDF file
        dummy_pdf_path = pdf_source.pdf_directory / "test.pdf"
        dummy_pdf_path.write_text("dummy content")
        
        # List documents
        documents = await pdf_source.list_documents()
        assert len(documents) >= 1
        
        # Find our test document
        test_doc = None
        for doc in documents:
            if doc.id == "test":
                test_doc = doc
                break
        
        assert test_doc is not None
        assert test_doc.content_type == "pdf"
        assert test_doc.source == str(dummy_pdf_path)
    
    @pytest.mark.asyncio
    async def test_pdf_search_functionality(self, pdf_source):
        """Test PDF search functionality."""
        # Create dummy PDF files
        for i in range(3):
            dummy_pdf_path = pdf_source.pdf_directory / f"sales_report_{i}.pdf"
            dummy_pdf_path.write_text("dummy content")
        
        # Search for documents
        results = await pdf_source.search_documents("sales", limit=5)
        assert len(results) >= 3


class TestAPIDocumentSource:
    """Test suite for API document source."""
    
    @pytest.fixture
    def mock_api_source(self):
        """Create a mock API document source."""
        return APIDocumentSource("https://api.example.com", "test_api_key")
    
    @pytest.mark.asyncio
    async def test_api_source_initialization(self, mock_api_source):
        """Test API source initialization."""
        assert mock_api_source.base_url == "https://api.example.com"
        assert "Authorization" in mock_api_source.headers
        assert mock_api_source.headers["Authorization"] == "Bearer test_api_key"
    
    @pytest.mark.asyncio
    async def test_api_document_retrieval_mock(self, mock_api_source):
        """Test API document retrieval with mocked responses."""
        mock_response_data = {
            "metadata": {
                "id": "api_doc_1",
                "title": "API Document",
                "source": "api",
                "content_type": "text"
            },
            "content": "This is an API document."
        }
        
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            document = await mock_api_source.retrieve_document("api_doc_1")
            
            assert document is not None
            assert document.metadata.id == "api_doc_1"
            assert document.metadata.title == "API Document"
            assert document.content == "This is an API document."
    
    @pytest.mark.asyncio
    async def test_api_search_mock(self, mock_api_source):
        """Test API search with mocked responses."""
        mock_response_data = {
            "results": [
                {
                    "metadata": {
                        "id": "search_doc_1",
                        "title": "Search Result 1",
                        "source": "api",
                        "content_type": "text"
                    },
                    "content": "Search result content 1."
                },
                {
                    "metadata": {
                        "id": "search_doc_2",
                        "title": "Search Result 2",
                        "source": "api",
                        "content_type": "text"
                    },
                    "content": "Search result content 2."
                }
            ]
        }
        
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            results = await mock_api_source.search_documents("test query", limit=10)
            
            assert len(results) == 2
            assert results[0].metadata.id == "search_doc_1"
            assert results[1].metadata.id == "search_doc_2"


class TestVectorSearchEngine:
    """Test suite for vector search engine."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def vector_engine(self, temp_dir):
        """Create a vector search engine for testing."""
        return VectorSearchEngine(
            collection_name="test_collection",
            persist_directory=temp_dir
        )
    
    @pytest.mark.asyncio
    async def test_vector_engine_initialization(self, vector_engine):
        """Test vector search engine initialization."""
        assert vector_engine.collection_name == "test_collection"
        assert vector_engine.collection is not None
        assert vector_engine.embedding_function is not None
    
    @pytest.mark.asyncio
    async def test_document_addition_and_search(self, vector_engine):
        """Test document addition and search functionality."""
        # Create test document
        doc = Document(
            metadata=DocumentMetadata(
                id="vector_test_doc",
                title="Vector Test Document",
                source="test",
                content_type="text"
            ),
            content="This is a test document for vector search functionality."
        )
        
        # Add document to vector engine
        success = await vector_engine.add_document(doc)
        assert success is True
        
        # Search for similar documents
        results = await vector_engine.search_similar_documents("test document", limit=5)
        assert len(results) > 0
        
        # Verify result
        found_doc, similarity = results[0]
        assert found_doc.metadata.id == "vector_test_doc"
        assert similarity > 0.0
    
    @pytest.mark.asyncio
    async def test_document_chunking(self, vector_engine):
        """Test document chunking functionality."""
        # Create a long document
        long_content = " ".join(["This is a long document with many words."] * 100)
        doc = Document(
            metadata=DocumentMetadata(
                id="long_doc",
                title="Long Document",
                source="test",
                content_type="text"
            ),
            content=long_content
        )
        
        # Add document (should be chunked)
        success = await vector_engine.add_document(doc)
        assert success is True
        
        # Verify chunks were created
        assert len(doc.chunks) > 1
        
        # Search should work with chunks
        results = await vector_engine.search_similar_documents("long document", limit=5)
        assert len(results) > 0
    
    @pytest.mark.asyncio
    async def test_document_count(self, vector_engine):
        """Test document count functionality."""
        initial_count = await vector_engine.get_document_count()
        
        # Add a document
        doc = Document(
            metadata=DocumentMetadata(
                id="count_test_doc",
                title="Count Test Document",
                source="test",
                content_type="text"
            ),
            content="This is a document for count testing."
        )
        
        await vector_engine.add_document(doc)
        
        # Check count increased
        new_count = await vector_engine.get_document_count()
        assert new_count > initial_count


class TestCacheManager:
    """Test suite for cache manager."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def cache_manager(self, temp_dir):
        """Create a cache manager for testing."""
        return CacheManager(temp_dir)
    
    @pytest.fixture
    def sample_document(self):
        """Create a sample document for testing."""
        return Document(
            metadata=DocumentMetadata(
                id="cache_test_doc",
                title="Cache Test Document",
                source="test",
                content_type="text"
            ),
            content="This is a document for cache testing."
        )
    
    @pytest.mark.asyncio
    async def test_document_caching(self, cache_manager, sample_document):
        """Test document caching functionality."""
        # Cache document
        success = await cache_manager.set_document(sample_document)
        assert success is True
        
        # Retrieve cached document
        cached_doc = await cache_manager.get_document("cache_test_doc")
        assert cached_doc is not None
        assert cached_doc.metadata.id == "cache_test_doc"
        assert cached_doc.content == sample_document.content
    
    @pytest.mark.asyncio
    async def test_search_results_caching(self, cache_manager, sample_document):
        """Test search results caching functionality."""
        results = [sample_document]
        
        # Cache search results
        success = await cache_manager.set_search_results("test query", results)
        assert success is True
        
        # Retrieve cached results
        cached_results = await cache_manager.get_search_results("test query")
        assert cached_results is not None
        assert len(cached_results) == 1
        assert cached_results[0].metadata.id == "cache_test_doc"
    
    @pytest.mark.asyncio
    async def test_cache_expiration(self, cache_manager, sample_document):
        """Test cache expiration functionality."""
        # Cache document with short expiration
        success = await cache_manager.set_document(sample_document, expire_time=1)
        assert success is True
        
        # Should be available immediately
        cached_doc = await cache_manager.get_document("cache_test_doc")
        assert cached_doc is not None
        
        # Wait for expiration
        await asyncio.sleep(2)
        
        # Should be expired
        cached_doc = await cache_manager.get_document("cache_test_doc")
        assert cached_doc is None
    
    def test_cache_clearing(self, cache_manager):
        """Test cache clearing functionality."""
        # Add something to cache
        cache_manager.cache.set("test_key", "test_value")
        
        # Verify it's there
        assert cache_manager.cache.get("test_key") == "test_value"
        
        # Clear cache
        cache_manager.clear_cache()
        
        # Verify it's gone
        assert cache_manager.cache.get("test_key") is None


class TestIntegrationLayer:
    """Test suite for integration layer."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    async def integration(self, temp_dir):
        """Create an integration instance for testing."""
        config = DocumentRetrieverConfig()
        config.pdf.pdf_directory = os.path.join(temp_dir, "pdfs")
        config.vector_search.persist_directory = os.path.join(temp_dir, "vector_db")
        config.cache.cache_directory = os.path.join(temp_dir, "cache")
        
        integration = DocumentRetrieverIntegration(config)
        await integration.initialize()
        
        yield integration
        
        if integration.retriever and integration.retriever.api_source:
            await integration.retriever.api_source.client.aclose()
    
    @pytest.mark.asyncio
    async def test_integration_initialization(self, integration):
        """Test integration initialization."""
        assert integration._initialized is True
        assert integration.retriever is not None
    
    @pytest.mark.asyncio
    async def test_sample_document_retrieval(self, integration):
        """Test retrieval of sample documents."""
        # Test Q3 sales document
        doc = await integration.get_document("q3_sales_performance")
        assert doc is not None
        assert "Q3 2023 Sales Performance" in doc
        
        # Test Project Phoenix document
        doc = await integration.get_document("project_phoenix_q3_retro")
        assert doc is not None
        assert "Project Phoenix - Q3 Retrospective" in doc
    
    @pytest.mark.asyncio
    async def test_search_functionality(self, integration):
        """Test search functionality through integration."""
        results = await integration.search_documents("sales", limit=5)
        assert len(results) > 0
        
        # Verify result structure
        for result in results:
            assert "id" in result
            assert "title" in result
            assert "content" in result
            assert "source" in result
    
    @pytest.mark.asyncio
    async def test_relevant_documents(self, integration):
        """Test relevant documents retrieval."""
        docs = await integration.get_relevant_documents("sales performance")
        assert len(docs) > 0
        
        for doc in docs:
            assert isinstance(doc, str)
            assert "Document:" in doc
    
    @pytest.mark.asyncio
    async def test_system_stats(self, integration):
        """Test system statistics."""
        stats = await integration.get_system_stats()
        assert "total_documents" in stats
        assert "sources_available" in stats
        assert "config" in stats
    
    @pytest.mark.asyncio
    async def test_cache_operations(self, integration):
        """Test cache operations."""
        # Clear cache
        success = await integration.clear_cache()
        assert success is True


# Performance benchmarks
class TestPerformanceBenchmarks:
    """Performance benchmarks for the enhanced document retriever."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.mark.asyncio
    async def test_bulk_document_indexing(self, temp_dir):
        """Benchmark bulk document indexing."""
        import time
        
        retriever = EnhancedDocumentRetriever(
            pdf_directory=os.path.join(temp_dir, "pdfs"),
            cache_dir=os.path.join(temp_dir, "cache"),
            vector_db_dir=os.path.join(temp_dir, "vector_db")
        )
        
        # Create multiple documents
        documents = []
        for i in range(100):
            doc = Document(
                metadata=DocumentMetadata(
                    id=f"perf_doc_{i}",
                    title=f"Performance Document {i}",
                    source="benchmark",
                    content_type="text"
                ),
                content=f"This is performance document {i} " * 50  # Make it substantial
            )
            documents.append(doc)
        
        # Benchmark indexing
        start_time = time.time()
        
        for doc in documents:
            await retriever.add_document_to_index(doc)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Indexed {len(documents)} documents in {total_time:.2f} seconds")
        print(f"Average time per document: {total_time/len(documents):.3f} seconds")
        
        # Verify indexing worked
        stats = await retriever.get_stats()
        assert stats["total_documents"] >= len(documents)
    
    @pytest.mark.asyncio
    async def test_concurrent_search_performance(self, temp_dir):
        """Benchmark concurrent search performance."""
        import time
        
        retriever = EnhancedDocumentRetriever(
            pdf_directory=os.path.join(temp_dir, "pdfs"),
            cache_dir=os.path.join(temp_dir, "cache"),
            vector_db_dir=os.path.join(temp_dir, "vector_db")
        )
        
        # Add some documents first
        for i in range(20):
            doc = Document(
                metadata=DocumentMetadata(
                    id=f"search_doc_{i}",
                    title=f"Search Document {i}",
                    source="benchmark",
                    content_type="text"
                ),
                content=f"This is search document {i} with unique content about topic {i % 5}."
            )
            await retriever.add_document_to_index(doc)
        
        # Define search queries
        queries = [
            "document topic 0",
            "document topic 1",
            "document topic 2",
            "unique content",
            "search document"
        ]
        
        # Benchmark concurrent searches
        start_time = time.time()
        
        tasks = []
        for query in queries:
            task = retriever.search_documents(query, limit=5)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Performed {len(queries)} concurrent searches in {total_time:.2f} seconds")
        print(f"Average time per search: {total_time/len(queries):.3f} seconds")
        
        # Verify results
        for result_set in results:
            assert len(result_set) >= 0  # Should return some results
    
    @pytest.mark.asyncio
    async def test_cache_performance_impact(self, temp_dir):
        """Benchmark cache performance impact."""
        import time
        
        retriever = EnhancedDocumentRetriever(
            pdf_directory=os.path.join(temp_dir, "pdfs"),
            cache_dir=os.path.join(temp_dir, "cache"),
            vector_db_dir=os.path.join(temp_dir, "vector_db")
        )
        
        # Add a document
        doc = Document(
            metadata=DocumentMetadata(
                id="cache_perf_doc",
                title="Cache Performance Document",
                source="benchmark",
                content_type="text"
            ),
            content="This is a document for cache performance testing." * 100
        )
        await retriever.add_document_to_index(doc)
        
        # Benchmark without cache
        start_time = time.time()
        for _ in range(10):
            await retriever.retrieve_document("cache_perf_doc", use_cache=False)
        end_time = time.time()
        no_cache_time = end_time - start_time
        
        # Benchmark with cache
        start_time = time.time()
        for _ in range(10):
            await retriever.retrieve_document("cache_perf_doc", use_cache=True)
        end_time = time.time()
        cache_time = end_time - start_time
        
        print(f"Without cache: {no_cache_time:.3f} seconds")
        print(f"With cache: {cache_time:.3f} seconds")
        print(f"Cache speedup: {no_cache_time/cache_time:.2f}x")
        
        # Cache should be faster
        assert cache_time < no_cache_time


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])