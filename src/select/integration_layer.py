"""
Integration layer for the enhanced document retriever.

This module provides integration with the existing context engineering pipeline,
maintaining backward compatibility while adding enhanced features.
"""

import asyncio
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

from .enhanced_document_retriever import (
    EnhancedDocumentRetriever,
    Document,
    DocumentMetadata,
    get_q3_sales_performance_pdf,
    get_project_phoenix_q3_retro
)
from .config import DocumentRetrieverConfig, get_config
from loguru import logger


class DocumentRetrieverIntegration:
    """Integration layer for the enhanced document retriever."""
    
    def __init__(self, config: Optional[DocumentRetrieverConfig] = None):
        self.config = config or get_config()
        self.retriever: Optional[EnhancedDocumentRetriever] = None
        self._initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the enhanced document retriever."""
        if self._initialized:
            return True
        
        try:
            # Create necessary directories
            self.config.create_directories()
            
            # Initialize the enhanced retriever
            self.retriever = EnhancedDocumentRetriever(
                pdf_directory=self.config.pdf.pdf_directory,
                api_base_url=self.config.api.base_url,
                api_key=self.config.api.api_key,
                cache_dir=self.config.cache.cache_directory,
                vector_db_dir=self.config.vector_search.persist_directory
            )
            
            # Add any existing sample documents to the system
            await self._add_sample_documents()
            
            self._initialized = True
            logger.info("Document retriever integration initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize document retriever: {str(e)}")
            return False
    
    async def _add_sample_documents(self) -> None:
        """Add sample documents to the system for demonstration."""
        try:
            # Create sample documents from the original mock data
            sample_docs = [
                Document(
                    metadata=DocumentMetadata(
                        id="q3_sales_performance",
                        title="Q3 2023 Sales Performance Report",
                        source="mock_data",
                        content_type="text",
                        keywords=["sales", "performance", "Q3", "2023", "revenue", "enterprise"]
                    ),
                    content=await get_q3_sales_performance_pdf()
                ),
                Document(
                    metadata=DocumentMetadata(
                        id="project_phoenix_q3_retro",
                        title="Project Phoenix Q3 Retrospective",
                        source="mock_data",
                        content_type="text",
                        keywords=["project", "phoenix", "retrospective", "Q3", "launch"]
                    ),
                    content=await get_project_phoenix_q3_retro()
                )
            ]
            
            # Add documents to the vector index
            for doc in sample_docs:
                await self.retriever.add_document_to_index(doc)
            
            logger.info(f"Added {len(sample_docs)} sample documents to the system")
            
        except Exception as e:
            logger.error(f"Error adding sample documents: {str(e)}")
    
    async def get_document(self, document_id: str) -> Optional[str]:
        """Get a document by ID (legacy interface)."""
        if not self._initialized:
            await self.initialize()
        
        try:
            document = await self.retriever.retrieve_document(document_id)
            return document.content if document else None
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {str(e)}")
            return None
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for documents and return results in a structured format."""
        if not self._initialized:
            await self.initialize()
        
        try:
            documents = await self.retriever.search_documents(query, limit)
            
            # Convert to structured format
            results = []
            for doc in documents:
                results.append({
                    "id": doc.metadata.id,
                    "title": doc.metadata.title,
                    "source": doc.metadata.source,
                    "content": doc.content,
                    "keywords": doc.metadata.keywords,
                    "content_type": doc.metadata.content_type
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    async def get_relevant_documents(self, query: str, context: Optional[str] = None) -> List[str]:
        """Get relevant documents for a query (optimized for context engineering)."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Enhance query with context if provided
            enhanced_query = query
            if context:
                enhanced_query = f"{context} {query}"
            
            documents = await self.retriever.search_documents(enhanced_query, limit=5)
            
            # Return document contents formatted for context engineering
            formatted_docs = []
            for doc in documents:
                formatted_content = f"Document: {doc.metadata.title}\nSource: {doc.metadata.source}\n\n{doc.content}"
                formatted_docs.append(formatted_content)
            
            return formatted_docs
            
        except Exception as e:
            logger.error(f"Error getting relevant documents: {str(e)}")
            return []
    
    async def add_document_from_file(self, file_path: str, document_id: Optional[str] = None) -> bool:
        """Add a document from a file path."""
        if not self._initialized:
            await self.initialize()
        
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            # Generate document ID if not provided
            if not document_id:
                document_id = file_path.stem
            
            # Determine content type
            content_type = "text"
            if file_path.suffix.lower() == ".pdf":
                content_type = "pdf"
            
            # Create document metadata
            stat = file_path.stat()
            metadata = DocumentMetadata(
                id=document_id,
                title=file_path.name,
                source=str(file_path),
                content_type=content_type,
                created_at=str(stat.st_ctime),
                modified_at=str(stat.st_mtime),
                file_size=stat.st_size
            )
            
            # Read content based on file type
            if content_type == "pdf":
                # Use the PDF source to extract content
                pdf_doc = await self.retriever.pdf_source.retrieve_document(document_id)
                if pdf_doc:
                    document = Document(metadata=metadata, content=pdf_doc.content)
                else:
                    logger.error(f"Failed to extract PDF content from {file_path}")
                    return False
            else:
                # Read text content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                document = Document(metadata=metadata, content=content)
            
            # Add to vector index
            success = await self.retriever.add_document_to_index(document)
            if success:
                logger.info(f"Successfully added document {document_id} from {file_path}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error adding document from file {file_path}: {str(e)}")
            return False
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        if not self._initialized:
            await self.initialize()
        
        try:
            stats = await self.retriever.get_stats()
            stats.update({
                "config": {
                    "pdf_directory": self.config.pdf.pdf_directory,
                    "vector_db_directory": self.config.vector_search.persist_directory,
                    "cache_enabled": self.config.cache.enabled,
                    "debug_mode": self.config.debug_mode
                }
            })
            return stats
        except Exception as e:
            logger.error(f"Error getting system stats: {str(e)}")
            return {}
    
    async def clear_cache(self) -> bool:
        """Clear the document cache."""
        if not self._initialized:
            await self.initialize()
        
        try:
            self.retriever.cache_manager.clear_cache()
            logger.info("Document cache cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    async def reindex_documents(self) -> bool:
        """Reindex all documents in the system."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Get all documents
            all_docs = await self.retriever.list_all_documents()
            
            # Reindex each document
            reindexed_count = 0
            for doc_meta in all_docs:
                document = await self.retriever.retrieve_document(doc_meta.id, use_cache=False)
                if document:
                    await self.retriever.add_document_to_index(document)
                    reindexed_count += 1
            
            logger.info(f"Reindexed {reindexed_count} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error reindexing documents: {str(e)}")
            return False
    
    async def __aenter__(self):
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.retriever:
            await self.retriever.__aexit__(exc_type, exc_val, exc_tb)


# Global integration instance
_integration_instance: Optional[DocumentRetrieverIntegration] = None


async def get_integration() -> DocumentRetrieverIntegration:
    """Get the global integration instance."""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = DocumentRetrieverIntegration()
        await _integration_instance.initialize()
    return _integration_instance


# Legacy compatibility functions with enhanced features
async def get_enhanced_q3_sales_performance_pdf() -> str:
    """Enhanced version of the Q3 sales performance PDF retrieval."""
    integration = await get_integration()
    document = await integration.get_document("q3_sales_performance")
    return document or await get_q3_sales_performance_pdf()


async def get_enhanced_project_phoenix_q3_retro() -> str:
    """Enhanced version of the Project Phoenix Q3 retro retrieval."""
    integration = await get_integration()
    document = await integration.get_document("project_phoenix_q3_retro")
    return document or await get_project_phoenix_q3_retro()


async def search_for_relevant_documents(query: str, context: Optional[str] = None) -> List[str]:
    """Search for relevant documents based on query and context."""
    integration = await get_integration()
    return await integration.get_relevant_documents(query, context)


async def add_pdf_document(pdf_path: str, document_id: Optional[str] = None) -> bool:
    """Add a PDF document to the system."""
    integration = await get_integration()
    return await integration.add_document_from_file(pdf_path, document_id)


async def get_document_search_results(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get structured search results for documents."""
    integration = await get_integration()
    return await integration.search_documents(query, limit)


# Context engineering pipeline integration
class ContextEngineeringIntegration:
    """Integration for the context engineering pipeline."""
    
    def __init__(self):
        self.integration: Optional[DocumentRetrieverIntegration] = None
    
    async def initialize(self):
        """Initialize the integration."""
        self.integration = await get_integration()
    
    async def get_documents_for_context(self, user_query: str, user_profile: Dict[str, Any]) -> List[str]:
        """Get documents relevant to the user query and profile for context engineering."""
        if not self.integration:
            await self.initialize()
        
        # Enhance query with user profile information
        profile_context = f"User role: {user_profile.get('role', 'unknown')}"
        if user_profile.get('department'):
            profile_context += f", Department: {user_profile['department']}"
        
        return await self.integration.get_relevant_documents(user_query, profile_context)
    
    async def search_by_keywords(self, keywords: List[str], limit: int = 5) -> List[str]:
        """Search documents by keywords."""
        if not self.integration:
            await self.initialize()
        
        query = " ".join(keywords)
        documents = await self.integration.search_documents(query, limit)
        
        return [doc["content"] for doc in documents]
    
    async def get_document_summaries(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        """Get document summaries for quick context."""
        if not self.integration:
            await self.initialize()
        
        documents = await self.integration.search_documents(query, limit)
        
        summaries = []
        for doc in documents:
            # Create a summary (first 200 characters)
            summary = doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"]
            summaries.append({
                "title": doc["title"],
                "summary": summary,
                "source": doc["source"]
            })
        
        return summaries


# Example usage and testing
async def main():
    """Example usage of the integration layer."""
    
    # Test basic integration
    integration = await get_integration()
    
    # Test document retrieval
    doc = await integration.get_document("q3_sales_performance")
    print(f"Retrieved document: {doc[:100]}..." if doc else "Document not found")
    
    # Test search functionality
    results = await integration.search_documents("sales performance", limit=3)
    print(f"Search results: {len(results)} documents found")
    
    # Test context engineering integration
    context_integration = ContextEngineeringIntegration()
    await context_integration.initialize()
    
    user_profile = {"role": "Product Manager", "department": "Sales"}
    context_docs = await context_integration.get_documents_for_context(
        "What were our Q3 sales results?", 
        user_profile
    )
    print(f"Context documents: {len(context_docs)} documents retrieved")
    
    # Test system stats
    stats = await integration.get_system_stats()
    print(f"System stats: {stats}")


if __name__ == "__main__":
    asyncio.run(main())