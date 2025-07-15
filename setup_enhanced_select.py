#!/usr/bin/env python3
"""
Setup script for the enhanced SELECT pillar.

This script helps set up the enhanced document retriever system by:
- Creating necessary directories
- Installing dependencies
- Setting up configuration files
- Initializing the vector database
- Running basic tests

Usage:
    python setup_enhanced_select.py [options]

Options:
    --install-deps    Install Python dependencies
    --create-config   Create sample configuration file
    --test-system     Run system tests
    --add-samples     Add sample documents
    --full-setup      Perform complete setup
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
import subprocess
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.select.config import DocumentRetrieverConfig, create_sample_config
    from src.select.enhanced_document_retriever import EnhancedDocumentRetriever, Document, DocumentMetadata
    from src.select.integration_layer import DocumentRetrieverIntegration
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure the enhanced SELECT pillar files are in the correct location.")
    sys.exit(1)


def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print("Creating directories...")
    
    directories = [
        "documents/pdfs",
        "chroma_db",
        "cache",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    return True


def create_configuration():
    """Create sample configuration file."""
    print("Creating configuration file...")
    
    try:
        create_sample_config("config.json")
        print("✓ Configuration file created: config.json")
        
        # Also create .env template
        env_template = """# Enhanced Document Retriever Configuration

# Core settings
PDF_DIRECTORY=./documents/pdfs
VECTOR_DB_DIR=./chroma_db
CACHE_DIR=./cache

# API settings (optional)
API_BASE_URL=
API_KEY=

# Vector search settings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Cache settings
CACHE_ENABLED=true

# Logging
LOG_LEVEL=INFO
DEBUG_MODE=false
"""
        
        with open(".env.template", "w") as f:
            f.write(env_template)
        
        print("✓ Environment template created: .env.template")
        print("  Please copy to .env and customize with your settings")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create configuration: {e}")
        return False


async def test_system():
    """Run basic system tests."""
    print("Testing system...")
    
    try:
        # Test configuration
        config = DocumentRetrieverConfig()
        issues = config.validate_environment()
        
        if issues:
            print("Configuration issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✓ Configuration validation passed")
        
        # Test integration
        integration = DocumentRetrieverIntegration(config)
        success = await integration.initialize()
        
        if success:
            print("✓ Integration initialization successful")
            
            # Test document retrieval
            doc = await integration.get_document("q3_sales_performance")
            if doc:
                print("✓ Sample document retrieval successful")
            else:
                print("⚠ Sample document retrieval failed")
            
            # Test search
            results = await integration.search_documents("sales", limit=3)
            if results:
                print(f"✓ Search functionality working ({len(results)} results)")
            else:
                print("⚠ Search functionality returned no results")
            
            # Test stats
            stats = await integration.get_system_stats()
            print(f"✓ System stats: {stats}")
            
        else:
            print("✗ Integration initialization failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ System test failed: {e}")
        return False


async def add_sample_documents():
    """Add sample documents to the system."""
    print("Adding sample documents...")
    
    try:
        # Create sample PDF content (mock)
        sample_pdfs = [
            {
                "filename": "q3_sales_performance.txt",
                "content": """Q3 2023 Sales Performance Report
                
Executive Summary:
This quarter has been a resounding success for the sales department.
We have exceeded our sales targets by a significant margin, driven by strong performance in the Enterprise segment.

Key Metrics:
- Total Revenue: $11.5M (115% of target)
- New Enterprise Customers: 25 (125% of target)
- Average Deal Size: $50K (110% of target)

Sales exceeded target by 15%."""
            },
            {
                "filename": "project_phoenix_q3_retro.txt",
                "content": """Project Phoenix - Q3 Retrospective

What went well:
- The project was launched on time and on budget.
- The new features have been well-received by our initial beta testers.
- The engineering team demonstrated excellent collaboration and problem-solving skills.

What could be improved:
- User adoption is tracking 10% below our initial forecast. We need to investigate the reasons for this gap.
- The marketing campaign did not generate the expected number of leads.

Key Takeaways:
- Project Phoenix launched successfully.
- User adoption is 10% below forecast."""
            },
            {
                "filename": "monthly_metrics_report.txt",
                "content": """Monthly Metrics Report - September 2023

Performance Overview:
- Website Traffic: 125K unique visitors (+15% MoM)
- Conversion Rate: 3.2% (+0.3% MoM)
- Customer Satisfaction: 4.2/5 (stable)
- Support Tickets: 847 (-5% MoM)

Key Highlights:
- Mobile traffic increased by 22%
- Email campaign performance improved by 18%
- New feature adoption rate: 67%"""
            }
        ]
        
        # Create documents directory if it doesn't exist
        docs_dir = Path("documents/pdfs")
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Write sample documents
        for pdf_info in sample_pdfs:
            file_path = docs_dir / pdf_info["filename"]
            with open(file_path, "w") as f:
                f.write(pdf_info["content"])
            print(f"✓ Created sample document: {file_path}")
        
        # Initialize integration and add documents to vector database
        integration = DocumentRetrieverIntegration()
        await integration.initialize()
        
        for pdf_info in sample_pdfs:
            doc_id = Path(pdf_info["filename"]).stem
            success = await integration.add_document_from_file(
                f"documents/pdfs/{pdf_info['filename']}",
                doc_id
            )
            if success:
                print(f"✓ Added document to vector database: {doc_id}")
            else:
                print(f"⚠ Failed to add document to vector database: {doc_id}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to add sample documents: {e}")
        return False


async def full_setup():
    """Perform complete setup."""
    print("Performing full setup of enhanced SELECT pillar...")
    print("=" * 50)
    
    steps = [
        ("Creating directories", create_directories),
        ("Installing dependencies", install_dependencies),
        ("Creating configuration", create_configuration),
        ("Adding sample documents", add_sample_documents),
        ("Testing system", test_system),
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            if asyncio.iscoroutinefunction(step_func):
                success = await step_func()
            else:
                success = step_func()
            
            if success:
                success_count += 1
                print(f"✓ {step_name} completed successfully")
            else:
                print(f"✗ {step_name} failed")
        except Exception as e:
            print(f"✗ {step_name} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Setup completed: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("🎉 Enhanced SELECT pillar setup completed successfully!")
        print("\nNext steps:")
        print("1. Copy .env.template to .env and customize with your settings")
        print("2. Add your PDF documents to the documents/pdfs directory")
        print("3. Configure API settings if using external knowledge bases")
        print("4. Run the test suite: pytest src/select/test_enhanced_retriever.py")
        print("5. Start using the enhanced document retriever in your applications")
    else:
        print("⚠ Setup completed with some issues. Please review the errors above.")
    
    return success_count == len(steps)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Setup script for enhanced SELECT pillar")
    parser.add_argument("--install-deps", action="store_true", help="Install Python dependencies")
    parser.add_argument("--create-config", action="store_true", help="Create sample configuration file")
    parser.add_argument("--test-system", action="store_true", help="Run system tests")
    parser.add_argument("--add-samples", action="store_true", help="Add sample documents")
    parser.add_argument("--full-setup", action="store_true", help="Perform complete setup")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        # No arguments provided, show help
        parser.print_help()
        return
    
    async def run_setup():
        if args.full_setup:
            return await full_setup()
        
        success = True
        
        if args.install_deps:
            success &= install_dependencies()
        
        if args.create_config:
            success &= create_configuration()
        
        if args.add_samples:
            success &= await add_sample_documents()
        
        if args.test_system:
            success &= await test_system()
        
        return success
    
    # Run async setup
    success = asyncio.run(run_setup())
    
    if success:
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup completed with errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()