"""
Mock API server for testing the enhanced document retriever.

This module provides a mock API server that simulates corporate knowledge bases
and external document sources for testing and development purposes.
"""

import asyncio
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from .dummy_data_generator import DummyDataGenerator, DummyDataConfig
from .enhanced_document_retriever import Document, DocumentMetadata


class SearchRequest(BaseModel):
    """Search request model."""
    query: str
    limit: int = 10
    filters: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    total_results: int
    results: List[Dict[str, Any]]
    execution_time_ms: int


class DocumentResponse(BaseModel):
    """Document response model."""
    metadata: Dict[str, Any]
    content: str
    
    
class DocumentListResponse(BaseModel):
    """Document list response model."""
    documents: List[Dict[str, Any]]
    total_count: int
    page: int
    page_size: int


class MockAPIServer:
    """Mock API server for corporate knowledge bases."""
    
    def __init__(self):
        self.app = FastAPI(title="Mock Corporate Knowledge Base API", version="1.0.0")
        self.documents: List[Document] = []
        self.setup_routes()
        self.load_dummy_data()
    
    def load_dummy_data(self):
        """Load dummy data for testing."""
        config = DummyDataConfig(
            num_sales_reports=20,
            num_project_docs=25,
            num_technical_docs=15,
            num_hr_docs=12,
            num_financial_docs=10
        )
        
        generator = DummyDataGenerator(config)
        self.documents = generator.generate_all_documents()
        
        print(f"Loaded {len(self.documents)} dummy documents")
    
    def setup_routes(self):
        """Set up API routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "message": "Mock Corporate Knowledge Base API",
                "version": "1.0.0",
                "endpoints": {
                    "documents": "/documents",
                    "search": "/search",
                    "document_by_id": "/documents/{document_id}",
                    "health": "/health"
                }
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "documents_loaded": len(self.documents)
            }
        
        @self.app.get("/documents", response_model=DocumentListResponse)
        async def list_documents(
            page: int = Query(1, ge=1),
            page_size: int = Query(10, ge=1, le=100),
            source: Optional[str] = Query(None),
            content_type: Optional[str] = Query(None)
        ):
            """List all documents with pagination."""
            
            # Filter documents
            filtered_docs = self.documents
            
            if source:
                filtered_docs = [doc for doc in filtered_docs if doc.metadata.source == source]
            
            if content_type:
                filtered_docs = [doc for doc in filtered_docs if doc.metadata.content_type == content_type]
            
            # Apply pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_docs = filtered_docs[start_idx:end_idx]
            
            # Convert to response format
            document_list = [
                {
                    "id": doc.metadata.id,
                    "title": doc.metadata.title,
                    "source": doc.metadata.source,
                    "content_type": doc.metadata.content_type,
                    "created_at": doc.metadata.created_at,
                    "modified_at": doc.metadata.modified_at,
                    "author": doc.metadata.author,
                    "keywords": doc.metadata.keywords,
                    "file_size": doc.metadata.file_size,
                    "page_count": doc.metadata.page_count
                }
                for doc in paginated_docs
            ]
            
            return DocumentListResponse(
                documents=document_list,
                total_count=len(filtered_docs),
                page=page,
                page_size=page_size
            )
        
        @self.app.get("/documents/{document_id}", response_model=DocumentResponse)
        async def get_document(document_id: str = Path(...)):
            """Get a specific document by ID."""
            
            # Find document
            document = None
            for doc in self.documents:
                if doc.metadata.id == document_id:
                    document = doc
                    break
            
            if not document:
                raise HTTPException(status_code=404, detail="Document not found")
            
            # Simulate API delay
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            return DocumentResponse(
                metadata={
                    "id": document.metadata.id,
                    "title": document.metadata.title,
                    "source": document.metadata.source,
                    "content_type": document.metadata.content_type,
                    "created_at": document.metadata.created_at,
                    "modified_at": document.metadata.modified_at,
                    "author": document.metadata.author,
                    "keywords": document.metadata.keywords,
                    "file_size": document.metadata.file_size,
                    "page_count": document.metadata.page_count
                },
                content=document.content
            )
        
        @self.app.get("/search", response_model=SearchResponse)
        async def search_documents(
            q: str = Query(..., description="Search query"),
            limit: int = Query(10, ge=1, le=100),
            source: Optional[str] = Query(None),
            content_type: Optional[str] = Query(None)
        ):
            """Search documents by query."""
            
            start_time = datetime.utcnow()
            
            # Filter documents
            filtered_docs = self.documents
            
            if source:
                filtered_docs = [doc for doc in filtered_docs if doc.metadata.source == source]
            
            if content_type:
                filtered_docs = [doc for doc in filtered_docs if doc.metadata.content_type == content_type]
            
            # Simple search implementation
            query_lower = q.lower()
            matching_docs = []
            
            for doc in filtered_docs:
                score = 0
                
                # Check title
                if query_lower in doc.metadata.title.lower():
                    score += 0.3
                
                # Check keywords
                for keyword in doc.metadata.keywords:
                    if query_lower in keyword.lower():
                        score += 0.2
                
                # Check content
                if query_lower in doc.content.lower():
                    score += 0.1
                    
                    # Count occurrences for better scoring
                    occurrences = doc.content.lower().count(query_lower)
                    score += min(occurrences * 0.05, 0.4)
                
                if score > 0:
                    matching_docs.append((doc, score))
            
            # Sort by relevance score
            matching_docs.sort(key=lambda x: x[1], reverse=True)
            matching_docs = matching_docs[:limit]
            
            # Convert to response format
            results = []
            for doc, score in matching_docs:
                # Create snippet
                content_lower = doc.content.lower()
                query_pos = content_lower.find(query_lower)
                
                if query_pos != -1:
                    start = max(0, query_pos - 100)
                    end = min(len(doc.content), query_pos + 200)
                    snippet = doc.content[start:end]
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(doc.content):
                        snippet = snippet + "..."
                else:
                    snippet = doc.content[:300] + "..." if len(doc.content) > 300 else doc.content
                
                results.append({
                    "id": doc.metadata.id,
                    "title": doc.metadata.title,
                    "source": doc.metadata.source,
                    "content_type": doc.metadata.content_type,
                    "author": doc.metadata.author,
                    "created_at": doc.metadata.created_at,
                    "keywords": doc.metadata.keywords,
                    "snippet": snippet,
                    "relevance_score": round(score, 3)
                })
            
            end_time = datetime.utcnow()
            execution_time = int((end_time - start_time).total_seconds() * 1000)
            
            # Simulate API delay
            await asyncio.sleep(random.uniform(0.2, 0.8))
            
            return SearchResponse(
                query=q,
                total_results=len(matching_docs),
                results=results,
                execution_time_ms=execution_time
            )
        
        @self.app.post("/search", response_model=SearchResponse)
        async def search_documents_post(request: SearchRequest):
            """Search documents by query (POST method)."""
            
            # Convert to GET parameters and call the GET endpoint
            return await search_documents(
                q=request.query,
                limit=request.limit,
                source=request.filters.get("source") if request.filters else None,
                content_type=request.filters.get("content_type") if request.filters else None
            )
        
        @self.app.get("/documents/{document_id}/similar")
        async def get_similar_documents(
            document_id: str = Path(...),
            limit: int = Query(5, ge=1, le=20)
        ):
            """Get documents similar to the specified document."""
            
            # Find the source document
            source_doc = None
            for doc in self.documents:
                if doc.metadata.id == document_id:
                    source_doc = doc
                    break
            
            if not source_doc:
                raise HTTPException(status_code=404, detail="Document not found")
            
            # Simple similarity based on keywords and source
            similar_docs = []
            
            for doc in self.documents:
                if doc.metadata.id == document_id:
                    continue
                
                similarity = 0
                
                # Same source adds similarity
                if doc.metadata.source == source_doc.metadata.source:
                    similarity += 0.3
                
                # Common keywords add similarity
                common_keywords = set(doc.metadata.keywords) & set(source_doc.metadata.keywords)
                similarity += len(common_keywords) * 0.1
                
                # Same content type adds similarity
                if doc.metadata.content_type == source_doc.metadata.content_type:
                    similarity += 0.2
                
                if similarity > 0:
                    similar_docs.append((doc, similarity))
            
            # Sort by similarity
            similar_docs.sort(key=lambda x: x[1], reverse=True)
            similar_docs = similar_docs[:limit]
            
            # Convert to response format
            results = [
                {
                    "id": doc.metadata.id,
                    "title": doc.metadata.title,
                    "source": doc.metadata.source,
                    "content_type": doc.metadata.content_type,
                    "author": doc.metadata.author,
                    "keywords": doc.metadata.keywords,
                    "similarity_score": round(score, 3)
                }
                for doc, score in similar_docs
            ]
            
            return {
                "source_document_id": document_id,
                "similar_documents": results
            }
        
        @self.app.get("/stats")
        async def get_statistics():
            """Get system statistics."""
            
            from collections import Counter
            
            sources = Counter(doc.metadata.source for doc in self.documents)
            content_types = Counter(doc.metadata.content_type for doc in self.documents)
            
            # Calculate some dummy metrics
            total_size = sum(doc.metadata.file_size or 0 for doc in self.documents)
            avg_size = total_size / len(self.documents) if self.documents else 0
            
            return {
                "total_documents": len(self.documents),
                "sources": dict(sources),
                "content_types": dict(content_types),
                "total_size_bytes": total_size,
                "average_size_bytes": int(avg_size),
                "last_updated": datetime.utcnow().isoformat()
            }
        
        @self.app.get("/sources")
        async def get_available_sources():
            """Get list of available document sources."""
            
            sources = set(doc.metadata.source for doc in self.documents)
            
            source_info = []
            for source in sources:
                docs_in_source = [doc for doc in self.documents if doc.metadata.source == source]
                source_info.append({
                    "source": source,
                    "document_count": len(docs_in_source),
                    "content_types": list(set(doc.metadata.content_type for doc in docs_in_source))
                })
            
            return {
                "sources": source_info,
                "total_sources": len(sources)
            }
        
        # Error handlers
        @self.app.exception_handler(404)
        async def not_found_handler(request, exc):
            return JSONResponse(
                status_code=404,
                content={"error": "Resource not found", "message": str(exc.detail)}
            )
        
        @self.app.exception_handler(422)
        async def validation_error_handler(request, exc):
            return JSONResponse(
                status_code=422,
                content={"error": "Validation error", "details": exc.errors()}
            )
        
        @self.app.exception_handler(500)
        async def internal_error_handler(request, exc):
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "message": "Something went wrong"}
            )
    
    def run(self, host: str = "localhost", port: int = 8000):
        """Run the mock API server."""
        print(f"Starting mock API server on http://{host}:{port}")
        print(f"API documentation available at http://{host}:{port}/docs")
        
        uvicorn.run(self.app, host=host, port=port)


class MockAPIClient:
    """Mock API client for testing without running a server."""
    
    def __init__(self):
        self.server = MockAPIServer()
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID."""
        try:
            # Find document
            for doc in self.server.documents:
                if doc.metadata.id == document_id:
                    return {
                        "metadata": {
                            "id": doc.metadata.id,
                            "title": doc.metadata.title,
                            "source": doc.metadata.source,
                            "content_type": doc.metadata.content_type,
                            "created_at": doc.metadata.created_at,
                            "author": doc.metadata.author,
                            "keywords": doc.metadata.keywords
                        },
                        "content": doc.content
                    }
            return None
        except Exception:
            return None
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search documents."""
        try:
            query_lower = query.lower()
            matching_docs = []
            
            for doc in self.server.documents:
                score = 0
                
                if query_lower in doc.metadata.title.lower():
                    score += 0.3
                
                for keyword in doc.metadata.keywords:
                    if query_lower in keyword.lower():
                        score += 0.2
                
                if query_lower in doc.content.lower():
                    score += 0.1
                    occurrences = doc.content.lower().count(query_lower)
                    score += min(occurrences * 0.05, 0.4)
                
                if score > 0:
                    matching_docs.append((doc, score))
            
            matching_docs.sort(key=lambda x: x[1], reverse=True)
            matching_docs = matching_docs[:limit]
            
            results = []
            for doc, score in matching_docs:
                results.append({
                    "id": doc.metadata.id,
                    "title": doc.metadata.title,
                    "source": doc.metadata.source,
                    "content": doc.content,
                    "relevance_score": round(score, 3)
                })
            
            return results
        except Exception:
            return []
    
    async def list_documents(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all documents."""
        try:
            documents = self.server.documents[:limit]
            return [
                {
                    "id": doc.metadata.id,
                    "title": doc.metadata.title,
                    "source": doc.metadata.source,
                    "content_type": doc.metadata.content_type,
                    "created_at": doc.metadata.created_at,
                    "author": doc.metadata.author,
                    "keywords": doc.metadata.keywords
                }
                for doc in documents
            ]
        except Exception:
            return []


def create_mock_responses_file():
    """Create a JSON file with mock API responses for testing."""
    
    client = MockAPIClient()
    
    # Generate sample responses
    responses = {
        "documents": [],
        "search_results": {},
        "document_details": {}
    }
    
    # Get all documents
    documents = asyncio.run(client.list_documents(limit=50))
    responses["documents"] = documents
    
    # Generate search results for common queries
    search_queries = [
        "sales performance",
        "project retrospective", 
        "technical documentation",
        "HR policy",
        "financial forecast",
        "budget analysis",
        "quarterly results",
        "software architecture",
        "employee handbook",
        "expense report"
    ]
    
    for query in search_queries:
        results = asyncio.run(client.search_documents(query, limit=5))
        responses["search_results"][query] = {
            "query": query,
            "total_results": len(results),
            "results": results
        }
    
    # Get detailed information for a few documents
    sample_doc_ids = [doc["id"] for doc in documents[:10]]
    
    for doc_id in sample_doc_ids:
        doc_detail = asyncio.run(client.get_document(doc_id))
        if doc_detail:
            responses["document_details"][doc_id] = doc_detail
    
    # Save to file
    with open("mock_api_responses.json", "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=2, ensure_ascii=False)
    
    print("Mock API responses saved to mock_api_responses.json")
    print(f"Generated {len(responses['documents'])} documents")
    print(f"Generated {len(responses['search_results'])} search queries")
    print(f"Generated {len(responses['document_details'])} document details")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Mock API server for document retrieval testing")
    parser.add_argument("--host", default="localhost", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--generate-responses", action="store_true", help="Generate mock responses file")
    
    args = parser.parse_args()
    
    if args.generate_responses:
        create_mock_responses_file()
    else:
        server = MockAPIServer()
        server.run(host=args.host, port=args.port)