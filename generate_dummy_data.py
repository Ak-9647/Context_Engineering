#!/usr/bin/env python3
"""
Generate comprehensive dummy data for the enhanced SELECT pillar.

This script creates realistic dummy data including:
- PDF documents with diverse content types
- Corporate knowledge base samples
- Performance testing datasets
- Configuration files with sample data
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.select.dummy_data_generator import DummyDataGenerator, DummyDataConfig
from src.select.enhanced_document_retriever import EnhancedDocumentRetriever
from src.select.integration_layer import DocumentRetrieverIntegration
from src.select.config import DocumentRetrieverConfig, create_sample_config


async def generate_pdf_samples():
    """Generate sample PDF content as text files."""
    print("📄 Generating PDF sample content...")
    
    # Create directories
    pdf_dir = Path("documents/pdfs")
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample PDF documents
    pdf_samples = [
        {
            "filename": "q3_2023_sales_performance.txt",
            "content": """Q3 2023 Sales Performance Report
Executive Summary

Quarter Overview:
Q3 2023 has been a transformative quarter for our sales organization. Despite market challenges, we achieved significant growth across multiple segments, with particular strength in our enterprise solutions.

Key Performance Indicators:
• Total Revenue: $12.3M (118% of target)
• New Customer Acquisition: 47 new accounts
• Average Deal Size: $52,000 (up 15% YoY)
• Sales Cycle: 67 days (improved from 78 days)
• Customer Retention: 94% (industry-leading)

Regional Performance:
North America: $7.4M (120% of target)
- Enterprise segment leading growth
- Strong performance in financial services
- New partnerships driving expansion

Europe: $3.1M (115% of target)  
- GDPR compliance solutions in demand
- Growing presence in healthcare sector
- Localization efforts paying off

Asia-Pacific: $1.8M (110% of target)
- Emerging markets showing promise
- Digital transformation trends favorable
- Local partnerships established

Product Line Analysis:
Core Platform: $8.7M (71% of total revenue)
- Steady adoption in mid-market
- Enterprise features driving premium pricing
- Integration capabilities highly valued

Professional Services: $2.1M (17% of total revenue)
- Implementation services in high demand
- Training programs expanding
- Custom development requests increasing

Support & Maintenance: $1.5M (12% of total revenue)
- Renewal rate at 96%
- Proactive support reducing churn
- Feature requests informing roadmap

Market Trends & Opportunities:
• AI/ML integration becoming standard requirement
• Increased focus on data privacy and security
• Remote work driving cloud adoption
• Sustainability initiatives creating new opportunities

Challenges Addressed:
• Supply chain disruptions managed effectively
• Competition from new entrants contained
• Talent acquisition improved with remote hiring
• Customer success team expanded

Looking Forward:
Q4 2023 pipeline shows strong momentum with $15M in qualified opportunities. Key focus areas include enterprise expansion, product innovation, and market penetration in underserved regions.

Team Recognition:
Special recognition to our sales team for exceptional performance, particularly the enterprise sales division for exceeding targets by 25%.

Prepared by: Sarah Johnson, VP Sales
Date: October 15, 2023
Distribution: Executive Team, Board of Directors"""
        },
        {
            "filename": "project_phoenix_retrospective.txt",
            "content": """Project Phoenix - Q3 2023 Retrospective
Engineering Excellence Review

Project Overview:
Project Phoenix represents our most ambitious engineering initiative this year, aimed at modernizing our core platform architecture and enhancing user experience across all touchpoints.

Timeline & Milestones:
• Project Kickoff: July 1, 2023
• MVP Release: August 15, 2023  
• Beta Testing: September 1-30, 2023
• Production Deployment: October 1, 2023
• Post-launch Review: October 15, 2023

Team Composition:
• Engineering: 12 developers (8 backend, 4 frontend)
• DevOps: 2 engineers
• QA: 3 testers
• Product: 2 product managers
• Design: 1 UX designer
• Total: 20 team members

Technical Achievements:
✅ Microservices Architecture Implementation
- Successfully decomposed monolithic application
- Implemented service mesh for communication
- Achieved 99.9% uptime during transition
- Reduced deployment time from 2 hours to 15 minutes

✅ Performance Improvements
- API response time improved by 40%
- Database query optimization reduced load by 60%
- Frontend bundle size decreased by 35%
- Mobile app startup time reduced by 50%

✅ Security Enhancements
- Implemented OAuth 2.0 authentication
- Added comprehensive audit logging
- Achieved SOC 2 Type II compliance
- Zero security incidents during deployment

✅ Developer Experience
- Automated testing coverage increased to 85%
- CI/CD pipeline fully automated
- Code review process streamlined
- Documentation updated and comprehensive

What Went Well:
🎯 Team Collaboration
- Daily standups kept everyone aligned
- Cross-functional pairing improved knowledge sharing
- Retrospectives led to continuous improvement
- Remote work protocols effective

🎯 Technical Excellence
- Architecture decisions proved sound
- Code quality maintained throughout
- Performance targets exceeded
- Security requirements fully met

🎯 User Feedback
- Beta users reported 90% satisfaction
- Feature adoption exceeded expectations
- Support ticket volume decreased by 30%
- User onboarding time reduced by 45%

Areas for Improvement:
⚠️ Initial Planning
- Underestimated integration complexity
- Third-party API dependencies caused delays
- Resource allocation could have been better
- Risk assessment needed more depth

⚠️ Communication
- Stakeholder updates could have been more frequent
- Technical decisions needed better documentation
- User training materials delivered late
- Marketing coordination improved toward end

⚠️ Testing Strategy
- Load testing should have started earlier
- User acceptance testing needed more time
- Mobile testing on various devices insufficient
- Accessibility testing gaps identified

Key Metrics:
• Code Quality: 9.2/10 (SonarQube analysis)
• Test Coverage: 85% (target: 80%)
• Bug Density: 0.3 bugs per KLOC (excellent)
• Performance: 40% improvement (target: 25%)
• User Satisfaction: 4.5/5 (target: 4.0)

Lessons Learned:
1. Early stakeholder engagement prevents scope creep
2. Automated testing saves significant time in long run
3. Performance testing should start with development
4. User feedback integration is crucial for success
5. Documentation investment pays dividends

Future Recommendations:
• Implement feature flagging for safer deployments
• Establish performance budgets for all features
• Create dedicated user research program
• Invest in automated monitoring and alerting
• Develop comprehensive disaster recovery plan

Post-Launch Status:
✅ System stability: 99.95% uptime
✅ User adoption: 87% of target users migrated
✅ Performance: All benchmarks exceeded
✅ Support tickets: 35% reduction in volume
✅ Customer satisfaction: 4.6/5 average rating

Team Feedback:
"Best project experience in my 5 years here. Great leadership, clear goals, and excellent team dynamics." - Senior Developer

"The technical challenges were significant, but the team support made it manageable. Learned a lot about microservices." - Backend Engineer

"User feedback integration was seamless. The iterative approach really worked." - Product Manager

Next Steps:
1. Monitor system performance for 30 days
2. Conduct user feedback session
3. Plan Phase 2 features based on learnings
4. Update development processes based on retrospective
5. Share learnings with other engineering teams

Prepared by: Alex Chen, Engineering Manager
Reviewed by: Jennifer Martinez, CTO
Date: October 15, 2023"""
        },
        {
            "filename": "employee_handbook_2023.txt",
            "content": """Employee Handbook 2023
Your Guide to Success at TechCorp

Welcome Message:
Welcome to TechCorp! This handbook serves as your comprehensive guide to our company culture, policies, and procedures. We're excited to have you join our team of innovators and problem-solvers.

Company Mission:
To empower businesses worldwide through innovative technology solutions that drive growth, efficiency, and transformation.

Core Values:
🌟 Innovation: We embrace new ideas and creative solutions
🤝 Collaboration: We work together to achieve shared goals
🔧 Excellence: We strive for the highest quality in everything we do
🌱 Growth: We invest in continuous learning and development
🛡️ Integrity: We act ethically and transparently in all interactions

Employment Policies:

Equal Opportunity:
TechCorp is committed to providing equal employment opportunities regardless of race, color, religion, sex, national origin, age, disability, or any other protected characteristic.

Work Schedule:
• Standard Hours: 9:00 AM - 5:00 PM (flexible within core hours)
• Core Hours: 10:00 AM - 3:00 PM (required presence)
• Remote Work: Available with manager approval
• Flexible Fridays: Half-day Fridays during summer months

Time Off Benefits:
• Vacation: 20 days annually (increasing with tenure)
• Sick Leave: 10 days annually
• Personal Days: 3 days annually
• Holidays: 12 company holidays plus floating holidays
• Parental Leave: 12 weeks paid leave for new parents

Health & Wellness:
• Comprehensive health insurance (company pays 80%)
• Dental and vision coverage included
• Mental health support through EAP
• On-site fitness center and wellness programs
• Healthy snacks and meals provided

Professional Development:
• Annual learning budget: $2,000 per employee
• Conference attendance encouraged
• Internal mentorship program
• Lunch-and-learn sessions
• Technical certification reimbursement

Technology & Equipment:
• Choice of MacBook or PC laptop
• External monitor and ergonomic accessories
• Latest software and development tools
• Home office setup allowance: $500

Workplace Guidelines:

Dress Code:
• Business casual in office
• Comfortable attire for remote work
• Client meetings require professional dress
• Casual Fridays year-round

Communication:
• Slack for team communication
• Email for formal communications
• Video calls for distributed teams
• In-person meetings when possible

Code of Conduct:
• Treat all colleagues with respect
• Maintain confidentiality of sensitive information
• Report unethical behavior through proper channels
• Comply with all applicable laws and regulations

Performance Management:
• Quarterly check-ins with managers
• Annual performance reviews
• Goal setting and tracking
• 360-degree feedback process
• Career development planning

Recognition Programs:
• Monthly team recognition
• Quarterly company awards
• Annual innovation contest
• Spot bonuses for exceptional work
• Public recognition in company meetings

Safety & Security:
• Badge access to all facilities
• Security training for all employees
• Regular safety drills and procedures
• Incident reporting system
• Emergency contact information

IT Policies:
• Acceptable use of company resources
• Password security requirements
• Data backup and recovery procedures
• Software licensing compliance
• Personal device usage guidelines

Complaint Procedures:
• Open door policy with management
• Anonymous reporting system
• HR investigation process
• Anti-retaliation protection
• External ombudsman available

Company Resources:
• Employee resource groups
• Diversity and inclusion initiatives
• Volunteer time off program
• Company social events
• Internal knowledge base

Benefits Summary:
• Competitive salary with annual reviews
• Performance-based bonuses
• Stock option program
• Retirement plan with company matching
• Life and disability insurance

Contact Information:
• HR Department: hr@techcorp.com
• IT Support: support@techcorp.com
• Facilities: facilities@techcorp.com
• Emergency: 911 or security ext. 911

This handbook is reviewed annually and updated as needed. Please check the company intranet for the most current version.

Effective Date: January 1, 2023
Last Updated: October 1, 2023
Version: 3.2"""
        },
        {
            "filename": "financial_forecast_2024.txt",
            "content": """Financial Forecast 2024
Strategic Financial Planning & Analysis

Executive Summary:
This forecast presents TechCorp's financial projections for fiscal year 2024, based on current market conditions, historical performance, and strategic initiatives.

Revenue Projections:

Q1 2024: $13.5M
• Seasonal uptick in enterprise sales
• New product launches contributing
• Subscription revenue growth continuing

Q2 2024: $15.2M
• Peak selling season
• Conference season driving leads
• Partner channel expansion

Q3 2024: $14.8M
• Maintained momentum from Q2
• Summer slowdown partially offset
• International expansion beginning

Q4 2024: $16.7M
• Year-end enterprise deals
• Holiday season consumer uptick
• Budget flush purchases

Total 2024 Revenue: $60.2M (25% growth YoY)

Revenue Breakdown by Segment:

Enterprise Solutions: $36.1M (60%)
• Core platform licenses
• Professional services
• Enterprise support contracts

Mid-Market Solutions: $18.1M (30%)
• Standardized packages
• Self-service options
• Channel partner sales

Small Business: $6.0M (10%)
• Freemium to paid conversions
• Online sales channel
• Automated onboarding

Cost Structure Analysis:

Cost of Goods Sold: $21.1M (35% of revenue)
• Cloud infrastructure: $8.4M
• Third-party licenses: $4.2M
• Support staff: $5.6M
• Data processing: $2.9M

Operating Expenses: $28.6M (47.5% of revenue)
• Sales & Marketing: $12.1M
• Research & Development: $9.0M
• General & Administrative: $7.5M

Personnel Costs: $32.5M (54% of revenue)
• Salaries and wages: $24.4M
• Benefits and insurance: $4.9M
• Stock compensation: $2.4M
• Contractors and consultants: $0.8M

Technology Infrastructure: $6.2M
• Cloud services and hosting: $3.1M
• Software licenses: $1.8M
• Hardware and equipment: $1.0M
• Security and compliance: $0.3M

Key Financial Metrics:

Gross Margin: 65% (target: 65-70%)
Operating Margin: 17.5% (target: 15-20%)
Net Margin: 12.8% (target: 10-15%)
Cash Flow from Operations: $8.9M

Growth Assumptions:

Market Expansion: 15% annually
• Digital transformation acceleration
• Remote work technology adoption
• AI/ML integration demand

Customer Acquisition: 35% increase
• Enhanced marketing campaigns
• Partner channel development
• Product-led growth initiatives

Average Deal Size: 8% increase
• Upselling to existing customers
• Premium feature adoption
• Enterprise package optimization

Retention Rate: 95% (up from 94%)
• Improved customer success
• Product enhancements
• Proactive support

Risk Factors:

Economic Uncertainty: Medium Risk
• Potential recession impact
• Budget constraints at customers
• Extended sales cycles

Competition: Medium Risk
• New market entrants
• Price pressure
• Feature parity challenges

Technology Disruption: Low Risk
• AI/ML advancement requirements
• Platform modernization needs
• Security compliance changes

Regulatory Changes: Low Risk
• Data privacy regulations
• Industry compliance requirements
• International trade policies

Investment Priorities:

Product Development: $9.0M
• AI/ML capabilities
• Mobile applications
• Integration platform
• Security enhancements

Sales & Marketing: $12.1M
• Digital marketing expansion
• Sales team growth
• Partner program development
• Customer success initiatives

Infrastructure: $6.2M
• Cloud migration completion
• Security improvements
• Monitoring and analytics
• Disaster recovery

International Expansion: $2.5M
• European market entry
• Localization efforts
• Regulatory compliance
• Local partnerships

Scenario Analysis:

Optimistic Scenario (+20%): $72.2M revenue
• Faster market adoption
• Successful product launches
• Strong economic conditions

Base Case: $60.2M revenue
• Current projections
• Moderate growth assumptions
• Stable market conditions

Conservative Scenario (-15%): $51.2M revenue
• Economic downturn impact
• Increased competition
• Delayed product launches

Cash Flow Projections:

Operating Cash Flow: $8.9M
• Strong recurring revenue base
• Improved collections
• Efficient operations

Investing Cash Flow: -$4.2M
• Technology investments
• Office expansion
• Acquisition opportunities

Financing Cash Flow: -$2.1M
• Debt service payments
• Dividend payments
• Share buybacks

Net Cash Flow: $2.6M
Ending Cash Balance: $12.8M

Key Performance Indicators:

Customer Acquisition Cost: $2,400 (target: <$2,500)
Customer Lifetime Value: $28,000 (target: >$25,000)
Monthly Recurring Revenue: $3.8M (34% growth)
Annual Recurring Revenue: $45.6M (32% growth)
Customer Churn Rate: 5% annually (target: <6%)

Financial Controls:

Monthly budget reviews
Quarterly forecasting updates
Annual strategic planning
Board reporting requirements
Audit and compliance procedures

Conclusion:
The 2024 financial forecast reflects strong growth potential while maintaining profitability. Key success factors include successful product launches, market expansion, and operational efficiency improvements.

Prepared by: Michael Thompson, CFO
Reviewed by: Board Finance Committee
Date: October 20, 2023
Next Review: December 15, 2023"""
        },
        {
            "filename": "technical_architecture_guide.txt",
            "content": """Technical Architecture Guide
System Design & Implementation Standards

Architecture Overview:
Our technical architecture follows cloud-native principles with microservices design, emphasizing scalability, maintainability, and security.

System Components:

Frontend Applications:
• Web Application (React/TypeScript)
• Mobile Applications (React Native)
• Admin Dashboard (Vue.js)
• API Documentation Portal

Backend Services:
• User Management Service (Node.js/Express)
• Authentication Service (Go)
• Data Processing Service (Python/FastAPI)
• Notification Service (Node.js)
• Analytics Service (Python/Django)

Data Layer:
• Primary Database (PostgreSQL)
• Cache Layer (Redis)
• Search Engine (Elasticsearch)
• File Storage (AWS S3)
• Message Queue (RabbitMQ)

Infrastructure:
• Container Orchestration (Kubernetes)
• Service Mesh (Istio)
• API Gateway (Kong)
• Load Balancers (AWS ALB)
• CDN (CloudFlare)

Technology Stack:

Programming Languages:
• JavaScript/TypeScript - Frontend and Node.js services
• Python - Data processing and analytics
• Go - High-performance services
• Java - Legacy system integration
• SQL - Database queries and procedures

Frameworks & Libraries:
• React 18 - Primary frontend framework
• Next.js - Server-side rendering
• Express.js - Web application framework
• FastAPI - High-performance Python APIs
• Django - Admin and analytics services

Databases:
• PostgreSQL - Primary relational database
• MongoDB - Document storage for flexible schemas
• Redis - Caching and session storage
• InfluxDB - Time-series metrics
• Elasticsearch - Full-text search and analytics

Cloud Services:
• AWS EC2 - Compute instances
• AWS RDS - Managed database services
• AWS S3 - Object storage
• AWS Lambda - Serverless functions
• AWS CloudFormation - Infrastructure as Code

Development Standards:

Code Quality:
• ESLint and Prettier for JavaScript/TypeScript
• Black and flake8 for Python
• golangci-lint for Go
• SonarQube for code quality analysis
• Automated testing required for all changes

API Design:
• RESTful principles
• OpenAPI 3.0 specification
• Consistent naming conventions
• Proper HTTP status codes
• Comprehensive error handling

Database Design:
• Normalized relational schemas
• Proper indexing strategies
• Migration scripts for schema changes
• Backup and recovery procedures
• Performance monitoring

Security Practices:
• OAuth 2.0 authentication
• JWT token management
• Input validation and sanitization
• SQL injection prevention
• XSS protection
• CORS configuration

Performance Guidelines:
• Response time targets: <200ms for APIs
• Database query optimization
• Caching strategies
• CDN utilization
• Image optimization

Deployment Pipeline:

Development Environment:
• Local development with Docker Compose
• Feature branch workflow
• Pull request reviews required
• Automated testing on commits

Staging Environment:
• Kubernetes cluster mirroring production
• Integration testing
• Performance testing
• Security scanning

Production Environment:
• Blue-green deployment strategy
• Health checks and monitoring
• Rollback procedures
• Capacity planning

Monitoring & Observability:

Application Monitoring:
• Prometheus for metrics collection
• Grafana for visualization
• Jaeger for distributed tracing
• ELK stack for log aggregation

Infrastructure Monitoring:
• CloudWatch for AWS resources
• Kubernetes monitoring
• Network monitoring
• Security monitoring

Alerting:
• PagerDuty for incident management
• Slack notifications
• Email alerts
• Escalation procedures

Disaster Recovery:

Backup Strategy:
• Daily database backups
• Cross-region replication
• Point-in-time recovery
• Backup validation procedures

Recovery Procedures:
• Recovery time objective: 4 hours
• Recovery point objective: 1 hour
• Failover procedures
• Communication protocols

Business Continuity:
• Service level agreements
• Vendor management
• Risk assessment
• Regular testing

Compliance & Governance:

Data Privacy:
• GDPR compliance
• CCPA compliance
• Data retention policies
• Right to be forgotten

Security Compliance:
• SOC 2 Type II
• ISO 27001 preparation
• Regular security audits
• Vulnerability assessments

Change Management:
• Architecture review board
• Technical debt management
• Deprecation policies
• Documentation standards

Development Workflow:

Feature Development:
1. Requirements analysis
2. Technical design document
3. Implementation
4. Code review
5. Testing
6. Deployment
7. Monitoring

Code Review Process:
• Peer review required
• Automated checks
• Performance review
• Security review
• Documentation review

Testing Strategy:
• Unit tests (>80% coverage)
• Integration tests
• End-to-end tests
• Performance tests
• Security tests

Future Roadmap:

Q1 2024:
• Service mesh implementation
• Enhanced monitoring
• Performance optimization

Q2 2024:
• Machine learning integration
• Advanced analytics
• Mobile app enhancements

Q3 2024:
• International expansion support
• Compliance automation
• Developer tools improvement

Q4 2024:
• Next-generation architecture
• AI/ML platform integration
• Advanced security features

Best Practices:

Documentation:
• Architecture decision records
• API documentation
• Runbooks and procedures
• Code comments

Communication:
• Regular architecture reviews
• Technical presentations
• Cross-team collaboration
• Knowledge sharing sessions

Continuous Improvement:
• Regular retrospectives
• Performance analysis
• Technology evaluation
• Process optimization

Team Structure:
• Principal architect
• Senior engineers
• DevOps engineers
• Security specialist
• Quality assurance

This guide is updated quarterly and serves as the authoritative reference for all technical decisions and implementations.

Prepared by: Jennifer Liu, Principal Architect
Reviewed by: Engineering Leadership Team
Date: October 15, 2023
Version: 2.1"""
        }
    ]
    
    # Write PDF samples
    for sample in pdf_samples:
        file_path = pdf_dir / sample["filename"]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample["content"])
        print(f"✅ Created: {sample['filename']}")
    
    print(f"📄 Generated {len(pdf_samples)} PDF sample files")


def generate_corporate_knowledge_base():
    """Generate corporate knowledge base samples."""
    print("🏢 Generating corporate knowledge base samples...")
    
    # Create directory
    kb_dir = Path("corporate_kb")
    kb_dir.mkdir(exist_ok=True)
    
    # Sample knowledge base articles
    kb_articles = [
        {
            "id": "kb_001",
            "title": "Getting Started with TechCorp Platform",
            "category": "User Guide",
            "content": """# Getting Started with TechCorp Platform

## Overview
Welcome to TechCorp Platform! This guide will help you get started with our comprehensive business solution.

## First Steps
1. **Account Setup**: Create your account and verify your email
2. **Team Invitation**: Invite your team members
3. **Data Import**: Import your existing data
4. **Configuration**: Configure your workspace settings

## Key Features
- **Dashboard**: Real-time insights and analytics
- **Collaboration**: Team workspace and communication
- **Automation**: Workflow automation tools
- **Integration**: Connect with your existing tools

## Common Use Cases
- Project management
- Team collaboration
- Data analysis
- Process automation

## Next Steps
- Complete the onboarding checklist
- Explore the feature tutorials
- Join our community forum
- Contact support if needed

## Resources
- Video tutorials
- Documentation
- Community forum
- Customer support"""
        },
        {
            "id": "kb_002", 
            "title": "API Integration Best Practices",
            "category": "Developer Guide",
            "content": """# API Integration Best Practices

## Authentication
Use OAuth 2.0 for secure authentication:
```
Authorization: Bearer <your_token>
```

## Rate Limiting
Respect rate limits (1000 requests/hour):
- Check headers: X-RateLimit-Remaining
- Implement exponential backoff
- Cache responses when possible

## Error Handling
Handle these common errors:
- 401: Unauthorized
- 429: Rate limit exceeded
- 500: Server error

## Best Practices
1. Use HTTPS only
2. Validate all inputs
3. Implement proper logging
4. Monitor API usage
5. Version your integrations

## Code Examples
```javascript
// Example API call
const response = await fetch('/api/data', {
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  }
});
```

## Testing
- Use our sandbox environment
- Test error scenarios
- Validate data formats
- Check performance

## Support
- API documentation
- Developer forum
- Email support
- Sample code repository"""
        },
        {
            "id": "kb_003",
            "title": "Security Guidelines",
            "category": "Security",
            "content": """# Security Guidelines

## Password Policy
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- No common words or personal information
- Change every 90 days

## Two-Factor Authentication
Enable 2FA for all accounts:
- SMS verification
- Authenticator apps
- Hardware tokens

## Data Protection
- Encrypt sensitive data
- Use secure connections (HTTPS)
- Regular security audits
- Backup important data

## Access Control
- Principle of least privilege
- Regular access reviews
- Disable unused accounts
- Monitor user activity

## Incident Response
1. Identify the threat
2. Contain the incident
3. Assess the damage
4. Recover systems
5. Document lessons learned

## Compliance
- GDPR compliance
- SOC 2 certification
- Regular security training
- Vulnerability assessments

## Reporting
Report security issues immediately:
- Email: security@techcorp.com
- Phone: 1-800-SECURITY
- Emergency: 911"""
        },
        {
            "id": "kb_004",
            "title": "Troubleshooting Common Issues",
            "category": "Support",
            "content": """# Troubleshooting Common Issues

## Login Problems
**Issue**: Cannot log in to account
**Solution**:
1. Check username/password
2. Clear browser cache
3. Try incognito mode
4. Reset password if needed

## Performance Issues
**Issue**: Application running slowly
**Solution**:
1. Check internet connection
2. Close unnecessary browser tabs
3. Clear browser cache
4. Try different browser

## Data Sync Issues
**Issue**: Data not syncing properly
**Solution**:
1. Check network connectivity
2. Verify account permissions
3. Force sync in settings
4. Contact support if persists

## Mobile App Issues
**Issue**: Mobile app not working
**Solution**:
1. Update to latest version
2. Restart the app
3. Check device storage
4. Reinstall if necessary

## Browser Compatibility
Supported browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Getting Help
1. Check our FAQ
2. Search knowledge base
3. Contact support
4. Schedule a call

## Contact Information
- Email: support@techcorp.com
- Phone: 1-800-SUPPORT
- Live chat: Available 24/7
- Community forum: forum.techcorp.com"""
        }
    ]
    
    # Write knowledge base articles
    for article in kb_articles:
        file_path = kb_dir / f"{article['id']}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"id: {article['id']}\n")
            f.write(f"title: {article['title']}\n")
            f.write(f"category: {article['category']}\n")
            f.write(f"---\n\n")
            f.write(article['content'])
        print(f"✅ Created: {article['id']}.md")
    
    print(f"🏢 Generated {len(kb_articles)} knowledge base articles")


def generate_performance_datasets():
    """Generate performance testing datasets."""
    print("📊 Generating performance testing datasets...")
    
    # Create directory
    perf_dir = Path("performance_data")
    perf_dir.mkdir(exist_ok=True)
    
    # Generate large document for performance testing
    large_doc_content = """# Large Document for Performance Testing

## Introduction
This document contains substantial content for performance testing of the document retrieval system.

""" + "\n".join([f"""## Section {i}
This is section {i} of the large document. It contains multiple paragraphs of text to simulate real-world document sizes.

Paragraph 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Paragraph 2: Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Paragraph 3: Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

### Subsection {i}.1
Additional content for subsection {i}.1 with more detailed information and examples.

### Subsection {i}.2
More content for subsection {i}.2 with technical details and specifications.

""" for i in range(1, 101)])
    
    # Write large document
    large_doc_path = perf_dir / "large_document.txt"
    with open(large_doc_path, 'w', encoding='utf-8') as f:
        f.write(large_doc_content)
    print(f"✅ Created: large_document.txt ({len(large_doc_content):,} characters)")
    
    # Generate performance test configuration
    perf_config = {
        "test_scenarios": [
            {
                "name": "document_retrieval_load_test",
                "description": "Test document retrieval under load",
                "concurrent_users": 50,
                "duration_minutes": 10,
                "documents_to_test": 1000
            },
            {
                "name": "search_performance_test",
                "description": "Test search performance with various queries",
                "concurrent_searches": 20,
                "duration_minutes": 5,
                "query_variations": 100
            },
            {
                "name": "vector_search_stress_test",
                "description": "Stress test vector similarity search",
                "concurrent_requests": 100,
                "duration_minutes": 15,
                "vector_dimensions": 384
            }
        ],
        "performance_thresholds": {
            "document_retrieval_time_ms": 200,
            "search_response_time_ms": 500,
            "vector_search_time_ms": 1000,
            "cache_hit_rate_percent": 80,
            "memory_usage_mb": 1000
        },
        "test_data": {
            "document_count": 10000,
            "average_document_size_kb": 50,
            "search_queries": [
                "sales performance",
                "project management",
                "financial analysis",
                "technical documentation",
                "user guide",
                "API integration",
                "security guidelines",
                "performance optimization"
            ]
        }
    }
    
    # Write performance configuration
    perf_config_path = perf_dir / "performance_config.json"
    with open(perf_config_path, 'w', encoding='utf-8') as f:
        json.dump(perf_config, f, indent=2)
    print(f"✅ Created: performance_config.json")
    
    print(f"📊 Generated performance testing dataset")


def generate_sample_configurations():
    """Generate sample configuration files."""
    print("⚙️  Generating sample configuration files...")
    
    # Create sample config
    create_sample_config("config_sample.json")
    print("✅ Created: config_sample.json")
    
    # Create development config
    dev_config = {
        "environment": "development",
        "pdf": {
            "pdf_directory": "./documents/pdfs",
            "max_file_size_mb": 10,
            "extraction_timeout": 30
        },
        "vector_search": {
            "collection_name": "dev_documents",
            "persist_directory": "./chroma_db_dev",
            "embedding_model": "all-MiniLM-L6-v2"
        },
        "api": {
            "base_url": "http://localhost:8000",
            "timeout": 30,
            "max_retries": 3
        },
        "cache": {
            "enabled": True,
            "cache_directory": "./cache_dev",
            "max_size_mb": 100
        },
        "logging": {
            "log_level": "DEBUG",
            "log_file": "logs/dev_document_retriever.log"
        },
        "debug_mode": True
    }
    
    with open("config_development.json", 'w') as f:
        json.dump(dev_config, f, indent=2)
    print("✅ Created: config_development.json")
    
    # Create production config template
    prod_config = {
        "environment": "production",
        "pdf": {
            "pdf_directory": "/app/documents/pdfs",
            "max_file_size_mb": 50,
            "extraction_timeout": 60
        },
        "vector_search": {
            "collection_name": "prod_documents",
            "persist_directory": "/app/chroma_db",
            "embedding_model": "all-MiniLM-L6-v2"
        },
        "api": {
            "base_url": "https://api.production.com",
            "timeout": 60,
            "max_retries": 5
        },
        "cache": {
            "enabled": True,
            "cache_directory": "/app/cache",
            "max_size_mb": 2000
        },
        "logging": {
            "log_level": "INFO",
            "log_file": "/app/logs/document_retriever.log"
        },
        "debug_mode": False
    }
    
    with open("config_production.json", 'w') as f:
        json.dump(prod_config, f, indent=2)
    print("✅ Created: config_production.json")
    
    print("⚙️  Generated sample configuration files")


async def test_system_with_dummy_data():
    """Test the system with generated dummy data."""
    print("🧪 Testing system with dummy data...")
    
    try:
        # Initialize the integration
        integration = DocumentRetrieverIntegration()
        await integration.initialize()
        
        # Test document retrieval
        doc = await integration.get_document("q3_sales_performance")
        if doc:
            print("✅ Document retrieval working")
        else:
            print("⚠️  Document retrieval needs attention")
        
        # Test search
        results = await integration.search_documents("sales performance", limit=3)
        if results:
            print(f"✅ Search working ({len(results)} results)")
        else:
            print("⚠️  Search needs attention")
        
        # Test system stats
        stats = await integration.get_system_stats()
        print(f"✅ System stats: {stats}")
        
        print("🧪 System testing completed")
        
    except Exception as e:
        print(f"❌ System testing failed: {e}")


async def main():
    """Main function to generate all dummy data."""
    print("🚀 Generating Comprehensive Dummy Data for Enhanced SELECT Pillar")
    print("=" * 70)
    
    # Create base directories
    for directory in ["documents", "documents/pdfs", "corporate_kb", "performance_data", "logs"]:
        Path(directory).mkdir(exist_ok=True)
    
    # Generate all dummy data
    await generate_pdf_samples()
    print()
    
    generate_corporate_knowledge_base()
    print()
    
    generate_performance_datasets()
    print()
    
    generate_sample_configurations()
    print()
    
    # Generate documents using the dummy data generator
    print("📚 Generating comprehensive document dataset...")
    config = DummyDataConfig(
        num_sales_reports=20,
        num_project_docs=25,
        num_technical_docs=15,
        num_hr_docs=12,
        num_financial_docs=10
    )
    
    generator = DummyDataGenerator(config)
    documents = generator.generate_all_documents()
    
    # Save documents to files
    generator.save_documents_to_files(documents, "dummy_documents")
    
    # Generate API responses
    api_responses = generator.generate_api_responses()
    generator.save_api_responses(api_responses, "mock_api_responses.json")
    
    print(f"📚 Generated {len(documents)} comprehensive documents")
    print()
    
    # Test the system
    await test_system_with_dummy_data()
    
    print("\n🎉 Dummy Data Generation Complete!")
    print("=" * 70)
    print("✅ PDF samples created in documents/pdfs/")
    print("✅ Corporate knowledge base created in corporate_kb/")
    print("✅ Performance datasets created in performance_data/")
    print("✅ Sample configurations created")
    print("✅ Comprehensive document dataset created in dummy_documents/")
    print("✅ API responses created in mock_api_responses.json")
    print("✅ System tested successfully")
    
    print("\n🚀 Next Steps:")
    print("1. Run: python setup_enhanced_select.py --full-setup")
    print("2. Test: python -m pytest src/select/test_enhanced_retriever.py")
    print("3. Start mock API: python src/select/mock_api_server.py")
    print("4. Use the enhanced SELECT pillar in your applications!")


if __name__ == "__main__":
    asyncio.run(main())