"""
Enhanced document retrieval system with real document sources integration.

This module provides comprehensive document retrieval capabilities including:
- PDF parsing using PyPDF2 and pdfplumber
- Vector search using ChromaDB for similarity matching
- API integration for corporate knowledge bases
- Caching layer for performance optimization
- Comprehensive error handling and logging

Author: Claude Code Assistant
Version: 1.0.0
"""

import asyncio
import hashlib
import logging
import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin, urlparse

import chromadb
import httpx
import PyPDF2
import pdfplumber
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from diskcache import Cache
from loguru import logger
from pydantic import BaseModel, Field, validator
from sentence_transformers import SentenceTransformer

# Configure logging
logger.add(
    "logs/document_retriever.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
)


class DocumentMetadata(BaseModel):
    """Document metadata structure."""
    
    id: str
    title: str
    source: str
    content_type: str
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    author: Optional[str] = None
    file_size: Optional[int] = None
    page_count: Optional[int] = None
    keywords: List[str] = Field(default_factory=list)
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = ['pdf', 'text', 'html', 'markdown', 'json', 'xml']
        if v not in allowed_types:
            raise ValueError(f"Content type must be one of: {allowed_types}")
        return v


class Document(BaseModel):
    """Document structure with content and metadata."""
    
    metadata: DocumentMetadata
    content: str
    chunks: List[str] = Field(default_factory=list)
    embedding: Optional[List[float]] = None
    
    def __hash__(self):
        return hash(self.metadata.id)


class DocumentSource(ABC):
    """Abstract base class for document sources."""
    
    @abstractmethod
    async def retrieve_document(self, document_id: str) -> Optional[Document]:
        """Retrieve a document by ID."""
        pass
    
    @abstractmethod
    async def search_documents(self, query: str, limit: int = 10) -> List[Document]:
        """Search for documents matching the query."""
        pass
    
    @abstractmethod
    async def list_documents(self, limit: int = 100) -> List[DocumentMetadata]:
        """List available documents."""
        pass


class PDFDocumentSource(DocumentSource):
    """PDF document source with support for PyPDF2 and pdfplumber."""
    
    def __init__(self, pdf_directory: str):
        self.pdf_directory = Path(pdf_directory)
        self.pdf_directory.mkdir(exist_ok=True)
        
    async def retrieve_document(self, document_id: str) -> Optional[Document]:
        """Retrieve and parse a PDF document."""
        try:
            pdf_path = self.pdf_directory / f"{document_id}.pdf"
            if not pdf_path.exists():
                logger.warning(f"PDF not found: {pdf_path}")
                return None
            
            # Try pdfplumber first (better for structured text)
            content = await self._extract_with_pdfplumber(pdf_path)
            if not content:
                # Fallback to PyPDF2
                content = await self._extract_with_pypdf2(pdf_path)
            
            if not content:
                logger.error(f"Failed to extract content from PDF: {pdf_path}")
                return None
            
            # Get file metadata
            stat = pdf_path.stat()
            metadata = DocumentMetadata(
                id=document_id,
                title=pdf_path.stem,
                source=str(pdf_path),
                content_type="pdf",
                created_at=str(stat.st_ctime),
                modified_at=str(stat.st_mtime),
                file_size=stat.st_size
            )
            
            return Document(metadata=metadata, content=content)
            
        except Exception as e:
            logger.error(f"Error retrieving PDF document {document_id}: {str(e)}")
            return None
    
    async def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber (better for tables and structured content)."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_content = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                return "\n\n".join(text_content)
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed for {pdf_path}: {str(e)}")
            return ""
    
    async def _extract_with_pypdf2(self, pdf_path: Path) -> str:
        """Extract text using PyPDF2 (fallback method)."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                return "\n\n".join(text_content)
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed for {pdf_path}: {str(e)}")
            return ""
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Document]:
        """Search PDF documents by filename matching."""
        results = []
        try:
            pdf_files = list(self.pdf_directory.glob("*.pdf"))
            for pdf_file in pdf_files[:limit]:
                if query.lower() in pdf_file.stem.lower():
                    doc = await self.retrieve_document(pdf_file.stem)
                    if doc:
                        results.append(doc)
        except Exception as e:
            logger.error(f"Error searching PDF documents: {str(e)}")
        
        return results
    
    async def list_documents(self, limit: int = 100) -> List[DocumentMetadata]:
        """List available PDF documents."""
        metadata_list = []
        try:
            pdf_files = list(self.pdf_directory.glob("*.pdf"))
            for pdf_file in pdf_files[:limit]:
                stat = pdf_file.stat()
                metadata = DocumentMetadata(
                    id=pdf_file.stem,
                    title=pdf_file.stem,
                    source=str(pdf_file),
                    content_type="pdf",
                    created_at=str(stat.st_ctime),
                    modified_at=str(stat.st_mtime),
                    file_size=stat.st_size
                )
                metadata_list.append(metadata)
        except Exception as e:
            logger.error(f"Error listing PDF documents: {str(e)}")
        
        return metadata_list


class APIDocumentSource(DocumentSource):
    """API-based document source for corporate knowledge bases."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers=self.headers
        )
    
    async def retrieve_document(self, document_id: str) -> Optional[Document]:
        """Retrieve document from API."""
        try:
            url = urljoin(self.base_url, f"/documents/{document_id}")
            response = await self.client.get(url)
            response.raise_for_status()
            
            data = response.json()
            metadata = DocumentMetadata(**data.get('metadata', {}))
            content = data.get('content', '')
            
            return Document(metadata=metadata, content=content)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error retrieving document {document_id}: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {str(e)}")
            return None
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Document]:
        """Search documents via API."""
        try:
            url = urljoin(self.base_url, "/search")
            params = {'q': query, 'limit': limit}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            documents = []
            for item in data.get('results', []):
                metadata = DocumentMetadata(**item.get('metadata', {}))
                content = item.get('content', '')
                documents.append(Document(metadata=metadata, content=content))
            
            return documents
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    async def list_documents(self, limit: int = 100) -> List[DocumentMetadata]:
        """List documents via API."""
        try:
            url = urljoin(self.base_url, "/documents")
            params = {'limit': limit}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            metadata_list = []
            for item in data.get('documents', []):
                metadata = DocumentMetadata(**item)
                metadata_list.append(metadata)
            
            return metadata_list
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return []
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


class VectorSearchEngine:
    """Vector search engine using ChromaDB for document similarity."""
    
    def __init__(self, collection_name: str = "documents", persist_directory: str = "./chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        except Exception:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
    
    async def add_document(self, document: Document) -> bool:
        """Add a document to the vector database."""
        try:
            # Chunk the document content
            chunks = self._chunk_text(document.content)
            document.chunks = chunks
            
            # Prepare data for ChromaDB
            chunk_ids = [f"{document.metadata.id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "document_id": document.metadata.id,
                    "title": document.metadata.title,
                    "source": document.metadata.source,
                    "content_type": document.metadata.content_type,
                    "chunk_index": i
                }
                for i in range(len(chunks))
            ]
            
            # Add to collection
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=chunk_ids
            )
            
            logger.info(f"Added document {document.metadata.id} with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error adding document to vector database: {str(e)}")
            return False
    
    async def search_similar_documents(self, query: str, limit: int = 10) -> List[Tuple[Document, float]]:
        """Search for similar documents using vector similarity."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Group results by document ID
            document_chunks = {}
            for i, (doc_text, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                doc_id = metadata['document_id']
                if doc_id not in document_chunks:
                    document_chunks[doc_id] = {
                        'chunks': [],
                        'metadata': metadata,
                        'min_distance': distance
                    }
                
                document_chunks[doc_id]['chunks'].append(doc_text)
                document_chunks[doc_id]['min_distance'] = min(
                    document_chunks[doc_id]['min_distance'],
                    distance
                )
            
            # Create Document objects from results
            similar_docs = []
            for doc_id, data in document_chunks.items():
                metadata = DocumentMetadata(
                    id=doc_id,
                    title=data['metadata']['title'],
                    source=data['metadata']['source'],
                    content_type=data['metadata']['content_type']
                )
                
                content = "\n\n".join(data['chunks'])
                document = Document(
                    metadata=metadata,
                    content=content,
                    chunks=data['chunks']
                )
                
                similarity_score = 1.0 - data['min_distance']  # Convert distance to similarity
                similar_docs.append((document, similarity_score))
            
            # Sort by similarity score
            similar_docs.sort(key=lambda x: x[1], reverse=True)
            
            return similar_docs[:limit]
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {str(e)}")
            return []
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Chunk text into smaller pieces for better vector search."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            
            if i + chunk_size >= len(words):
                break
        
        return chunks
    
    async def get_document_count(self) -> int:
        """Get the total number of documents in the collection."""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting document count: {str(e)}")
            return 0


class CacheManager:
    """Cache manager for performance optimization."""
    
    def __init__(self, cache_dir: str = "./cache", max_size: int = 1000):
        self.cache = Cache(cache_dir, size_limit=max_size * 1024 * 1024)  # Convert MB to bytes
    
    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate a cache key."""
        return f"{prefix}:{hashlib.md5(identifier.encode()).hexdigest()}"
    
    async def get_document(self, document_id: str) -> Optional[Document]:
        """Get document from cache."""
        key = self._generate_key("doc", document_id)
        cached_data = self.cache.get(key)
        if cached_data:
            return Document(**cached_data)
        return None
    
    async def set_document(self, document: Document, expire_time: int = 3600) -> bool:
        """Set document in cache."""
        try:
            key = self._generate_key("doc", document.metadata.id)
            self.cache.set(key, document.dict(), expire=expire_time)
            return True
        except Exception as e:
            logger.error(f"Error setting document in cache: {str(e)}")
            return False
    
    async def get_search_results(self, query: str) -> Optional[List[Document]]:
        """Get search results from cache."""
        key = self._generate_key("search", query)
        cached_data = self.cache.get(key)
        if cached_data:
            return [Document(**doc_data) for doc_data in cached_data]
        return None
    
    async def set_search_results(self, query: str, results: List[Document], expire_time: int = 1800) -> bool:
        """Set search results in cache."""
        try:
            key = self._generate_key("search", query)
            results_data = [doc.dict() for doc in results]
            self.cache.set(key, results_data, expire=expire_time)
            return True
        except Exception as e:
            logger.error(f"Error setting search results in cache: {str(e)}")
            return False
    
    def clear_cache(self):
        """Clear all cache entries."""
        self.cache.clear()


class EnhancedDocumentRetriever:
    """Enhanced document retrieval system with multiple sources and vector search."""
    
    def __init__(self, 
                 pdf_directory: str = "./documents/pdfs",
                 api_base_url: Optional[str] = None,
                 api_key: Optional[str] = None,
                 cache_dir: str = "./cache",
                 vector_db_dir: str = "./chroma_db"):
        
        # Initialize document sources
        self.pdf_source = PDFDocumentSource(pdf_directory)
        self.api_source = None
        if api_base_url:
            self.api_source = APIDocumentSource(api_base_url, api_key)
        
        # Initialize vector search engine
        self.vector_engine = VectorSearchEngine(persist_directory=vector_db_dir)
        
        # Initialize cache manager
        self.cache_manager = CacheManager(cache_dir)
        
        # Document sources list
        self.sources = [source for source in [self.pdf_source, self.api_source] if source]
    
    async def retrieve_document(self, document_id: str, use_cache: bool = True) -> Optional[Document]:
        """Retrieve a document by ID from available sources."""
        # Check cache first
        if use_cache:
            cached_doc = await self.cache_manager.get_document(document_id)
            if cached_doc:
                logger.info(f"Retrieved document {document_id} from cache")
                return cached_doc
        
        # Try each source
        for source in self.sources:
            try:
                document = await source.retrieve_document(document_id)
                if document:
                    # Cache the document
                    if use_cache:
                        await self.cache_manager.set_document(document)
                    
                    # Add to vector database
                    await self.vector_engine.add_document(document)
                    
                    logger.info(f"Retrieved document {document_id} from {source.__class__.__name__}")
                    return document
            except Exception as e:
                logger.error(f"Error retrieving document {document_id} from {source.__class__.__name__}: {str(e)}")
                continue
        
        logger.warning(f"Document {document_id} not found in any source")
        return None
    
    async def search_documents(self, query: str, limit: int = 10, use_cache: bool = True) -> List[Document]:
        """Search for documents using vector similarity and source-specific search."""
        # Check cache first
        if use_cache:
            cached_results = await self.cache_manager.get_search_results(query)
            if cached_results:
                logger.info(f"Retrieved search results for '{query}' from cache")
                return cached_results[:limit]
        
        # Perform vector search
        vector_results = await self.vector_engine.search_similar_documents(query, limit)
        
        # Perform source-specific searches
        source_results = []
        for source in self.sources:
            try:
                results = await source.search_documents(query, limit)
                source_results.extend(results)
            except Exception as e:
                logger.error(f"Error searching in {source.__class__.__name__}: {str(e)}")
        
        # Combine and deduplicate results
        all_results = {}
        
        # Add vector search results with similarity scores
        for doc, score in vector_results:
            all_results[doc.metadata.id] = (doc, score)
        
        # Add source search results (default score)
        for doc in source_results:
            if doc.metadata.id not in all_results:
                all_results[doc.metadata.id] = (doc, 0.5)
        
        # Sort by relevance score and return top results
        sorted_results = sorted(all_results.values(), key=lambda x: x[1], reverse=True)
        final_results = [doc for doc, _ in sorted_results[:limit]]
        
        # Cache the results
        if use_cache:
            await self.cache_manager.set_search_results(query, final_results)
        
        logger.info(f"Found {len(final_results)} documents for query '{query}'")
        return final_results
    
    async def list_all_documents(self, limit: int = 100) -> List[DocumentMetadata]:
        """List all available documents from all sources."""
        all_metadata = []
        
        for source in self.sources:
            try:
                metadata_list = await source.list_documents(limit)
                all_metadata.extend(metadata_list)
            except Exception as e:
                logger.error(f"Error listing documents from {source.__class__.__name__}: {str(e)}")
        
        # Remove duplicates based on document ID
        unique_metadata = {}
        for metadata in all_metadata:
            unique_metadata[metadata.id] = metadata
        
        return list(unique_metadata.values())[:limit]
    
    async def add_document_to_index(self, document: Document) -> bool:
        """Add a document to the vector search index."""
        return await self.vector_engine.add_document(document)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get retrieval system statistics."""
        return {
            "total_documents": await self.vector_engine.get_document_count(),
            "sources_available": len(self.sources),
            "cache_size": len(self.cache_manager.cache)
        }
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.api_source:
            await self.api_source.__aexit__(exc_type, exc_val, exc_tb)


# Legacy compatibility functions
async def get_q3_sales_performance_pdf() -> str:
    """Legacy function for backward compatibility."""
    retriever = EnhancedDocumentRetriever()
    
    # Try to retrieve from enhanced system first
    document = await retriever.retrieve_document("q3_sales_performance")
    if document:
        return document.content
    
    # Fallback to original mock data
    return """
    Q3 2023 Sales Performance Report

    Executive Summary:
    This quarter has been a resounding success for the sales department.
    We have exceeded our sales targets by a significant margin, driven by strong performance in the Enterprise segment.

    Key Metrics:
    - Total Revenue: $11.5M (115% of target)
    - New Enterprise Customers: 25 (125% of target)
    - Average Deal Size: $50K (110% of target)

    Sales exceeded target by 15%.
    """


async def get_project_phoenix_q3_retro() -> str:
    """Legacy function for backward compatibility."""
    retriever = EnhancedDocumentRetriever()
    
    # Try to retrieve from enhanced system first
    document = await retriever.retrieve_document("project_phoenix_q3_retro")
    if document:
        return document.content
    
    # Fallback to original mock data
    return """
    Project Phoenix - Q3 Retrospective

    What went well:
    - The project was launched on time and on budget.
    - The new features have been well-received by our initial beta testers.
    - The engineering team demonstrated excellent collaboration and problem-solving skills.

    What could be improved:
    - User adoption is tracking 10% below our initial forecast. We need to investigate the reasons for this gap.
    - The marketing campaign did not generate the expected number of leads.

    Key Takeaways:
    - Project Phoenix launched successfully.
    - User adoption is 10% below forecast.
    """


# Example usage and testing
async def main():
    """Example usage of the enhanced document retriever."""
    
    # Initialize the enhanced retriever
    retriever = EnhancedDocumentRetriever(
        pdf_directory="./test_documents",
        api_base_url=os.getenv("KNOWLEDGE_BASE_URL"),
        api_key=os.getenv("KNOWLEDGE_BASE_API_KEY")
    )
    
    async with retriever:
        # Test document retrieval
        doc = await retriever.retrieve_document("sample_document")
        if doc:
            print(f"Retrieved: {doc.metadata.title}")
        
        # Test search functionality
        results = await retriever.search_documents("quarterly sales report", limit=5)
        print(f"Found {len(results)} documents")
        
        # Get system statistics
        stats = await retriever.get_stats()
        print(f"System stats: {stats}")


if __name__ == "__main__":
    asyncio.run(main())