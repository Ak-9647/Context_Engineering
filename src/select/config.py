"""
Configuration management for the enhanced document retriever.

This module provides configuration classes and settings for the document retrieval system,
including PDF processing, vector search, API integration, and caching configurations.
"""

import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class PDFConfig(BaseModel):
    """Configuration for PDF processing."""
    
    pdf_directory: str = Field(default="./documents/pdfs", description="Directory containing PDF files")
    max_file_size_mb: int = Field(default=50, description="Maximum PDF file size in MB")
    extraction_timeout: int = Field(default=30, description="Timeout for PDF text extraction in seconds")
    preferred_extractor: str = Field(default="pdfplumber", description="Preferred PDF extractor: pdfplumber or pypdf2")
    
    @validator('preferred_extractor')
    def validate_extractor(cls, v):
        if v not in ['pdfplumber', 'pypdf2']:
            raise ValueError("Preferred extractor must be 'pdfplumber' or 'pypdf2'")
        return v


class VectorSearchConfig(BaseModel):
    """Configuration for vector search and embeddings."""
    
    collection_name: str = Field(default="documents", description="ChromaDB collection name")
    persist_directory: str = Field(default="./chroma_db", description="ChromaDB persistence directory")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Sentence transformer model for embeddings")
    chunk_size: int = Field(default=500, description="Text chunk size for embeddings")
    chunk_overlap: int = Field(default=50, description="Overlap between text chunks")
    max_results: int = Field(default=20, description="Maximum number of search results")
    similarity_threshold: float = Field(default=0.3, description="Minimum similarity score for results")
    
    @validator('similarity_threshold')
    def validate_threshold(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError("Similarity threshold must be between 0.0 and 1.0")
        return v


class APIConfig(BaseModel):
    """Configuration for API-based document sources."""
    
    base_url: Optional[str] = Field(default=None, description="Base URL for API document source")
    api_key: Optional[str] = Field(default=None, description="API key for authentication")
    timeout: int = Field(default=30, description="API request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of API request retries")
    retry_delay: float = Field(default=1.0, description="Delay between retries in seconds")
    headers: Dict[str, str] = Field(default_factory=dict, description="Additional HTTP headers")
    
    @validator('base_url')
    def validate_base_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError("Base URL must start with http:// or https://")
        return v


class CacheConfig(BaseModel):
    """Configuration for caching system."""
    
    cache_directory: str = Field(default="./cache", description="Cache directory path")
    max_size_mb: int = Field(default=1000, description="Maximum cache size in MB")
    document_ttl: int = Field(default=3600, description="Document cache TTL in seconds")
    search_ttl: int = Field(default=1800, description="Search results cache TTL in seconds")
    enabled: bool = Field(default=True, description="Enable/disable caching")
    cleanup_interval: int = Field(default=3600, description="Cache cleanup interval in seconds")


class LoggingConfig(BaseModel):
    """Configuration for logging system."""
    
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/document_retriever.log", description="Log file path")
    max_file_size: str = Field(default="10 MB", description="Maximum log file size")
    retention_days: int = Field(default=30, description="Log retention period in days")
    format_string: str = Field(
        default="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        description="Log format string"
    )
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()


class PerformanceConfig(BaseModel):
    """Configuration for performance optimization."""
    
    concurrent_pdf_processing: int = Field(default=3, description="Number of concurrent PDF processing tasks")
    concurrent_api_requests: int = Field(default=5, description="Number of concurrent API requests")
    batch_size: int = Field(default=10, description="Batch size for bulk operations")
    connection_pool_size: int = Field(default=10, description="HTTP connection pool size")
    enable_metrics: bool = Field(default=True, description="Enable performance metrics collection")


class DocumentRetrieverConfig(BaseSettings):
    """Main configuration for the enhanced document retriever."""
    
    # Core settings
    pdf: PDFConfig = Field(default_factory=PDFConfig)
    vector_search: VectorSearchConfig = Field(default_factory=VectorSearchConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    
    # Global settings
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    auto_index_documents: bool = Field(default=True, description="Automatically index new documents")
    validate_document_types: bool = Field(default=True, description="Validate document content types")
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env
        
    @classmethod
    def load_from_file(cls, config_file: str) -> 'DocumentRetrieverConfig':
        """Load configuration from a JSON or YAML file."""
        import json
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_path, 'r') as f:
            if config_path.suffix.lower() == '.json':
                config_data = json.load(f)
            elif config_path.suffix.lower() in ['.yaml', '.yml']:
                try:
                    import yaml
                    config_data = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML is required for YAML configuration files")
            else:
                raise ValueError("Configuration file must be JSON or YAML format")
        
        return cls(**config_data)
    
    def save_to_file(self, config_file: str) -> None:
        """Save configuration to a JSON or YAML file."""
        import json
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            if config_path.suffix.lower() == '.json':
                json.dump(self.dict(), f, indent=2)
            elif config_path.suffix.lower() in ['.yaml', '.yml']:
                try:
                    import yaml
                    yaml.safe_dump(self.dict(), f, default_flow_style=False)
                except ImportError:
                    raise ImportError("PyYAML is required for YAML configuration files")
            else:
                raise ValueError("Configuration file must be JSON or YAML format")
    
    def create_directories(self) -> None:
        """Create necessary directories based on configuration."""
        directories = [
            self.pdf.pdf_directory,
            self.vector_search.persist_directory,
            self.cache.cache_directory,
            Path(self.logging.log_file).parent
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def validate_environment(self) -> List[str]:
        """Validate the environment and return any issues."""
        issues = []
        
        # Check API configuration
        if self.api.base_url and not self.api.api_key:
            issues.append("API base URL provided but no API key configured")
        
        # Check directory permissions
        try:
            Path(self.pdf.pdf_directory).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            issues.append(f"Cannot create PDF directory: {self.pdf.pdf_directory}")
        
        # Check cache directory
        try:
            Path(self.cache.cache_directory).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            issues.append(f"Cannot create cache directory: {self.cache.cache_directory}")
        
        # Check log directory
        try:
            Path(self.logging.log_file).parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            issues.append(f"Cannot create log directory: {Path(self.logging.log_file).parent}")
        
        return issues


# Default configuration instance
default_config = DocumentRetrieverConfig()


def get_config() -> DocumentRetrieverConfig:
    """Get the current configuration."""
    return default_config


def load_config_from_env() -> DocumentRetrieverConfig:
    """Load configuration from environment variables."""
    return DocumentRetrieverConfig()


def create_sample_config(file_path: str = "config_sample.json") -> None:
    """Create a sample configuration file."""
    sample_config = DocumentRetrieverConfig()
    
    # Set some sample values
    sample_config.pdf.pdf_directory = "./documents/pdfs"
    sample_config.api.base_url = "https://api.example.com"
    sample_config.api.api_key = "your-api-key-here"
    sample_config.vector_search.embedding_model = "all-MiniLM-L6-v2"
    sample_config.cache.max_size_mb = 1000
    sample_config.debug_mode = False
    
    sample_config.save_to_file(file_path)
    print(f"Sample configuration saved to: {file_path}")


# Environment variable mapping for easy configuration
ENV_CONFIG_MAP = {
    "PDF_DIRECTORY": "pdf.pdf_directory",
    "API_BASE_URL": "api.base_url",
    "API_KEY": "api.api_key",
    "VECTOR_DB_DIR": "vector_search.persist_directory",
    "CACHE_DIR": "cache.cache_directory",
    "LOG_LEVEL": "logging.log_level",
    "DEBUG_MODE": "debug_mode"
}


if __name__ == "__main__":
    # Example usage
    config = DocumentRetrieverConfig()
    print("Default configuration loaded:")
    print(f"PDF directory: {config.pdf.pdf_directory}")
    print(f"Vector DB directory: {config.vector_search.persist_directory}")
    print(f"Cache enabled: {config.cache.enabled}")
    print(f"Debug mode: {config.debug_mode}")
    
    # Create sample configuration
    create_sample_config()
    
    # Validate environment
    issues = config.validate_environment()
    if issues:
        print("\nConfiguration issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nConfiguration validation passed!")
    
    # Create necessary directories
    config.create_directories()
    print("\nRequired directories created successfully!")