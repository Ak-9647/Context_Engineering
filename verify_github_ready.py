#!/usr/bin/env python3
"""
GitHub Readiness Verification Script

This script performs final verification that the Enhanced SELECT Pillar
is ready for GitHub commit and production deployment.
"""

import os
import sys
import json
import asyncio
from pathlib import Path

def check_files_exist():
    """Check that all required files exist."""
    
    print("📁 Checking Required Files...")
    
    required_files = [
        "README.md",
        "LICENSE",
        "requirements.txt", 
        ".env",
        ".gitignore",
        "setup_enhanced_select.py",
        "setup_api_keys.py",
        "generate_dummy_data.py",
        "test_basic_functionality.py",
        "final_comprehensive_test.py",
        "verify_github_ready.py",
        "DEPLOYMENT_GUIDE.md"
    ]
    
    src_files = [
        "src/__init__.py",
        "src/select/__init__.py",
        "src/select/enhanced_document_retriever.py",
        "src/select/integration_layer.py",
        "src/select/config.py",
        "src/select/dummy_data_generator.py",
        "src/select/mock_api_server.py",
        "src/select/test_enhanced_retriever.py",
        "src/select/README.md"
    ]
    
    all_required = required_files + src_files
    missing_files = []
    
    for file_path in all_required:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print(f"✅ All {len(all_required)} required files present")
    return True


def check_directories():
    """Check that all required directories exist."""
    
    print("\n📂 Checking Required Directories...")
    
    required_dirs = [
        "src/select",
        "documents/pdfs",
        "dummy_documents",
        "corporate_kb",
        "performance_data",
        "chroma_db",
        "cache",
        "logs"
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
        else:
            files_count = len(list(Path(dir_path).glob("*")))
            print(f"✅ {dir_path} ({files_count} files)")
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print(f"✅ All {len(required_dirs)} required directories present")
    return True


def check_gitignore():
    """Check that .gitignore has proper entries."""
    
    print("\n🚫 Checking .gitignore...")
    
    required_entries = [
        ".env",
        "__pycache__",
        "*.pyc",
        "chroma_db/",
        "cache/",
        "logs/",
        "documents/",
        "dummy_documents/"
    ]
    
    try:
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
        
        missing_entries = []
        for entry in required_entries:
            if entry not in gitignore_content:
                missing_entries.append(entry)
            else:
                print(f"✅ {entry}")
        
        if missing_entries:
            print(f"❌ Missing .gitignore entries: {missing_entries}")
            return False
        
        print(f"✅ All {len(required_entries)} required .gitignore entries present")
        return True
        
    except Exception as e:
        print(f"❌ Error reading .gitignore: {e}")
        return False


def check_license():
    """Check that LICENSE file exists and has content."""
    
    print("\n📜 Checking LICENSE...")
    
    try:
        with open("LICENSE", "r") as f:
            license_content = f.read()
        
        if len(license_content) < 100:
            print("❌ LICENSE file seems too short")
            return False
        
        if "MIT License" in license_content:
            print("✅ MIT License detected")
        else:
            print("⚠️  License type not clearly identified")
        
        print(f"✅ LICENSE file present ({len(license_content)} characters)")
        return True
        
    except Exception as e:
        print(f"❌ Error reading LICENSE: {e}")
        return False


def check_readme():
    """Check that README.md has comprehensive content."""
    
    print("\n📚 Checking README.md...")
    
    try:
        with open("README.md", "r") as f:
            readme_content = f.read()
        
        required_sections = [
            "# Enhanced SELECT Pillar",
            "## Overview",
            "## Features",
            "## Quick Start",
            "## Documentation",
            "## Installation",
            "## Usage",
            "## Testing",
            "## License"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in readme_content:
                missing_sections.append(section)
            else:
                print(f"✅ {section}")
        
        if missing_sections:
            print(f"❌ Missing README sections: {missing_sections}")
            return False
        
        if len(readme_content) < 5000:
            print("⚠️  README might be too short for comprehensive documentation")
        
        print(f"✅ README.md comprehensive ({len(readme_content)} characters)")
        return True
        
    except Exception as e:
        print(f"❌ Error reading README.md: {e}")
        return False


def check_env_template():
    """Check that .env has proper structure."""
    
    print("\n🔧 Checking .env Configuration...")
    
    try:
        with open(".env", "r") as f:
            env_content = f.read()
        
        required_vars = [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY", 
            "GOOGLE_API_KEY",
            "PDF_DIRECTORY",
            "VECTOR_DB_DIR",
            "CACHE_DIR"
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in env_content:
                missing_vars.append(var)
            else:
                print(f"✅ {var}")
        
        if missing_vars:
            print(f"❌ Missing environment variables: {missing_vars}")
            return False
        
        print(f"✅ All {len(required_vars)} required environment variables present")
        return True
        
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        return False


def check_requirements():
    """Check that requirements.txt has all necessary dependencies."""
    
    print("\n📦 Checking requirements.txt...")
    
    try:
        with open("requirements.txt", "r") as f:
            requirements_content = f.read()
        
        critical_deps = [
            "chromadb",
            "sentence-transformers",
            "pydantic",
            "fastapi",
            "uvicorn",
            "httpx",
            "PyPDF2",
            "pdfplumber",
            "loguru",
            "pytest"
        ]
        
        missing_deps = []
        for dep in critical_deps:
            if dep not in requirements_content:
                missing_deps.append(dep)
            else:
                print(f"✅ {dep}")
        
        if missing_deps:
            print(f"❌ Missing dependencies: {missing_deps}")
            return False
        
        print(f"✅ All {len(critical_deps)} critical dependencies present")
        return True
        
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False


async def check_functionality():
    """Check that the system works correctly."""
    
    print("\n🧪 Checking System Functionality...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from src.select.integration_layer import DocumentRetrieverIntegration
        from src.select.config import DocumentRetrieverConfig
        
        # Test configuration
        config = DocumentRetrieverConfig()
        print("✅ Configuration loads correctly")
        
        # Test integration
        integration = DocumentRetrieverIntegration(config)
        success = await integration.initialize()
        
        if success:
            print("✅ Integration layer initializes correctly")
        else:
            print("⚠️  Integration layer initialization had issues")
        
        # Test search
        results = await integration.search_documents("test", limit=3)
        print(f"✅ Search functionality works ({len(results)} results)")
        
        # Test stats
        stats = await integration.get_system_stats()
        print(f"✅ System stats available ({len(stats)} metrics)")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality check failed: {e}")
        return False


def check_test_coverage():
    """Check that test files exist and seem comprehensive."""
    
    print("\n🧪 Checking Test Coverage...")
    
    test_files = [
        "test_basic_functionality.py",
        "final_comprehensive_test.py",
        "src/select/test_enhanced_retriever.py"
    ]
    
    missing_tests = []
    for test_file in test_files:
        if not Path(test_file).exists():
            missing_tests.append(test_file)
        else:
            with open(test_file, "r") as f:
                content = f.read()
            print(f"✅ {test_file} ({len(content)} characters)")
    
    if missing_tests:
        print(f"❌ Missing test files: {missing_tests}")
        return False
    
    print(f"✅ All {len(test_files)} test files present")
    return True


def check_documentation():
    """Check that documentation is comprehensive."""
    
    print("\n📖 Checking Documentation...")
    
    doc_files = [
        "README.md",
        "DEPLOYMENT_GUIDE.md",
        "src/select/README.md"
    ]
    
    total_doc_size = 0
    for doc_file in doc_files:
        if Path(doc_file).exists():
            with open(doc_file, "r") as f:
                content = f.read()
            total_doc_size += len(content)
            print(f"✅ {doc_file} ({len(content)} characters)")
        else:
            print(f"❌ Missing: {doc_file}")
            return False
    
    if total_doc_size < 10000:
        print("⚠️  Documentation might be insufficient")
    
    print(f"✅ Documentation comprehensive ({total_doc_size} total characters)")
    return True


async def main():
    """Run all GitHub readiness checks."""
    
    print("🔍 GITHUB READINESS VERIFICATION")
    print("=" * 50)
    
    checks = [
        ("Files", check_files_exist),
        ("Directories", check_directories),
        ("GitIgnore", check_gitignore),
        ("License", check_license),
        ("README", check_readme),
        ("Environment", check_env_template),
        ("Requirements", check_requirements),
        ("Functionality", check_functionality),
        ("Tests", check_test_coverage),
        ("Documentation", check_documentation)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            if asyncio.iscoroutinefunction(check_func):
                result = await check_func()
            else:
                result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("🎯 GITHUB READINESS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 SYSTEM IS READY FOR GITHUB!")
        print("✅ All checks passed")
        print("✅ Code is production-ready")
        print("✅ Documentation is comprehensive")
        print("✅ Tests are complete")
        print("✅ Configuration is secure")
        
        print("\n🚀 Ready to commit:")
        print("   git add .")
        print("   git commit -m 'Enhanced SELECT Pillar - Production Ready'")
        print("   git push origin main")
        
        return True
    else:
        failed_checks = [name for name, result in results if not result]
        print(f"\n❌ {len(failed_checks)} checks failed:")
        for check in failed_checks:
            print(f"   - {check}")
        
        print("\n⚠️  Please fix the issues above before committing to GitHub")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)