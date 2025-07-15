"""
Dummy data generator for the enhanced document retriever.

This module creates realistic dummy data for testing and demonstration purposes,
including PDF content, API responses, and various document types.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import uuid

from .enhanced_document_retriever import Document, DocumentMetadata


@dataclass
class DummyDataConfig:
    """Configuration for dummy data generation."""
    num_sales_reports: int = 12
    num_project_docs: int = 15
    num_technical_docs: int = 10
    num_hr_docs: int = 8
    num_financial_docs: int = 6
    date_range_months: int = 24


class DummyDataGenerator:
    """Generates realistic dummy data for the document retriever system."""
    
    def __init__(self, config: DummyDataConfig = None):
        self.config = config or DummyDataConfig()
        self.companies = [
            "TechCorp", "DataSys", "CloudFlow", "InnovateLabs", "GlobalTech",
            "StartupX", "MegaCorp", "SmartSolutions", "NextGen", "FutureTech"
        ]
        self.departments = [
            "Sales", "Engineering", "Marketing", "HR", "Finance", "Operations",
            "Product", "Support", "Legal", "Strategy"
        ]
        self.product_names = [
            "Phoenix", "Titan", "Nexus", "Quantum", "Stellar", "Horizon",
            "Apex", "Vertex", "Prism", "Catalyst", "Aurora", "Zenith"
        ]
        self.metrics = [
            "Revenue", "Conversion Rate", "Customer Satisfaction", "Response Time",
            "User Engagement", "Market Share", "Cost per Acquisition", "Retention Rate"
        ]
    
    def generate_sales_reports(self) -> List[Document]:
        """Generate dummy sales reports."""
        documents = []
        
        for i in range(self.config.num_sales_reports):
            date = datetime.now() - timedelta(days=random.randint(30, 730))
            quarter = f"Q{((date.month - 1) // 3) + 1}"
            year = date.year
            
            revenue = random.randint(8000000, 15000000)
            target = random.randint(7000000, 12000000)
            customers = random.randint(15, 40)
            deal_size = random.randint(30000, 80000)
            
            content = f"""
{quarter} {year} Sales Performance Report

Executive Summary:
The {quarter} {year} quarter shows {"strong" if revenue > target else "challenging"} performance for our sales organization.
{"We exceeded our targets" if revenue > target else "We faced headwinds but maintained steady growth"} driven by 
{"enterprise segment growth" if random.choice([True, False]) else "improved conversion rates"}.

Key Metrics:
- Total Revenue: ${revenue:,} ({int((revenue/target)*100)}% of target)
- New Enterprise Customers: {customers} ({random.randint(80, 130)}% of target)
- Average Deal Size: ${deal_size:,} ({random.randint(90, 120)}% of target)
- Sales Cycle: {random.randint(45, 120)} days (avg)

Regional Performance:
- North America: ${int(revenue * 0.6):,} ({random.randint(85, 115)}% of target)
- Europe: ${int(revenue * 0.25):,} ({random.randint(90, 110)}% of target)
- Asia-Pacific: ${int(revenue * 0.15):,} ({random.randint(95, 125)}% of target)

Product Performance:
- {random.choice(self.product_names)} Platform: {random.randint(40, 60)}% of total revenue
- Professional Services: {random.randint(15, 25)}% of total revenue
- Support & Maintenance: {random.randint(20, 30)}% of total revenue

Key Achievements:
- Closed {random.randint(3, 8)} enterprise deals > $100K
- {"Exceeded" if random.choice([True, False]) else "Met"} customer satisfaction targets (4.{random.randint(1, 8)}/5)
- Launched {random.randint(1, 3)} new product features
- {"Expanded" if random.choice([True, False]) else "Maintained"} into {random.randint(1, 4)} new market segments

Challenges & Opportunities:
- {"Competitive pressure" if random.choice([True, False]) else "Market saturation"} in core segments
- {"Longer sales cycles" if random.choice([True, False]) else "Pricing pressure"} observed
- Opportunity to {"expand internationally" if random.choice([True, False]) else "enhance product offering"}

Forecast:
Next quarter projection: ${random.randint(int(revenue * 0.9), int(revenue * 1.2)):,}
Full year outlook: {"Optimistic" if random.choice([True, False]) else "Cautiously optimistic"}
            """
            
            metadata = DocumentMetadata(
                id=f"sales_report_{quarter.lower()}_{year}_{i}",
                title=f"{quarter} {year} Sales Performance Report",
                source="sales_department",
                content_type="pdf",
                created_at=date.isoformat(),
                modified_at=date.isoformat(),
                author=f"{random.choice(['Sarah Johnson', 'Mike Chen', 'Lisa Rodriguez', 'David Kim'])}",
                keywords=["sales", "performance", quarter.lower(), str(year), "revenue", "targets"],
                file_size=random.randint(50000, 200000),
                page_count=random.randint(8, 25)
            )
            
            documents.append(Document(metadata=metadata, content=content.strip()))
        
        return documents
    
    def generate_project_documents(self) -> List[Document]:
        """Generate dummy project documents and retrospectives."""
        documents = []
        
        for i in range(self.config.num_project_docs):
            project_name = f"Project {random.choice(self.product_names)}"
            date = datetime.now() - timedelta(days=random.randint(30, 365))
            doc_type = random.choice(["retrospective", "planning", "status_update", "requirements"])
            
            if doc_type == "retrospective":
                content = f"""
{project_name} - Retrospective ({date.strftime('%B %Y')})

Project Overview:
{project_name} aimed to {"enhance user experience" if random.choice([True, False]) else "improve system performance"} 
through {"new feature development" if random.choice([True, False]) else "architectural improvements"}.

Timeline:
- Project Duration: {random.randint(3, 12)} months
- Team Size: {random.randint(5, 15)} members
- Budget: ${random.randint(50000, 500000):,}

What Went Well:
- {"On-time delivery" if random.choice([True, False]) else "Strong team collaboration"}
- {"Exceeded performance targets" if random.choice([True, False]) else "Effective stakeholder communication"}
- {"Smooth deployment process" if random.choice([True, False]) else "Comprehensive testing coverage"}
- {"Positive user feedback" if random.choice([True, False]) else "Efficient resource utilization"}

What Could Be Improved:
- {"Initial requirements gathering" if random.choice([True, False]) else "Resource allocation planning"}
- {"Communication with stakeholders" if random.choice([True, False]) else "Technical documentation"}
- {"Risk assessment process" if random.choice([True, False]) else "Quality assurance procedures"}

Key Metrics:
- User Adoption: {random.randint(60, 95)}% of target users
- Performance Improvement: {random.randint(10, 50)}% faster response times
- Bug Report Volume: {random.randint(5, 25)} issues post-launch
- Customer Satisfaction: {random.randint(3, 5)}.{random.randint(0, 9)}/5

Lessons Learned:
- {"Early stakeholder engagement is crucial" if random.choice([True, False]) else "Automated testing saves time"}
- {"Regular retrospectives improve team dynamics" if random.choice([True, False]) else "Clear requirements prevent scope creep"}
- {"Cross-team collaboration enhances outcomes" if random.choice([True, False]) else "Continuous deployment reduces risk"}

Action Items for Future Projects:
- {"Implement better requirements tracking" if random.choice([True, False]) else "Enhance automated testing"}
- {"Improve stakeholder communication" if random.choice([True, False]) else "Standardize documentation"}
- {"Regular architecture reviews" if random.choice([True, False]) else "Enhanced monitoring and alerting"}
                """
            
            elif doc_type == "planning":
                content = f"""
{project_name} - Project Planning Document

Project Scope:
Develop and deploy {"a new customer portal" if random.choice([True, False]) else "an enhanced analytics dashboard"} 
to {"improve user experience" if random.choice([True, False]) else "increase operational efficiency"}.

Objectives:
- {"Reduce customer support tickets by 30%" if random.choice([True, False]) else "Improve system performance by 40%"}
- {"Increase user satisfaction scores" if random.choice([True, False]) else "Streamline internal processes"}
- {"Launch within {random.randint(3, 8)} months" if random.choice([True, False]) else "Stay within budget constraints"}

Technical Requirements:
- {"React/Node.js technology stack" if random.choice([True, False]) else "Python/Django framework"}
- {"Cloud deployment on AWS" if random.choice([True, False]) else "On-premise infrastructure"}
- {"Integration with existing systems" if random.choice([True, False]) else "Standalone application"}
- {"Mobile-responsive design" if random.choice([True, False]) else "Desktop-first approach"}

Team Structure:
- Project Manager: {random.choice(['Alex Thompson', 'Jennifer Liu', 'Roberto Martinez'])}
- Tech Lead: {random.choice(['Emily Chen', 'Michael Rodriguez', 'Sarah Kim'])}
- Developers: {random.randint(3, 8)} full-stack engineers
- QA Engineers: {random.randint(1, 3)} testers
- UX Designer: {random.choice(['Design Team', 'External Consultant'])}

Timeline:
- Phase 1 (Planning): {random.randint(2, 4)} weeks
- Phase 2 (Development): {random.randint(8, 16)} weeks
- Phase 3 (Testing): {random.randint(2, 6)} weeks
- Phase 4 (Deployment): {random.randint(1, 3)} weeks

Budget Allocation:
- Personnel: {random.randint(60, 80)}% (${random.randint(100000, 400000):,})
- Infrastructure: {random.randint(10, 20)}% (${random.randint(20000, 80000):,})
- Tools & Licenses: {random.randint(5, 15)}% (${random.randint(10000, 50000):,})
- Contingency: {random.randint(5, 10)}% (${random.randint(15000, 40000):,})

Risk Assessment:
- {"Technical complexity" if random.choice([True, False]) else "Resource availability"}: Medium Risk
- {"Stakeholder alignment" if random.choice([True, False]) else "Timeline constraints"}: Low Risk
- {"Integration challenges" if random.choice([True, False]) else "Budget constraints"}: High Risk
                """
            
            else:  # status_update or requirements
                content = f"""
{project_name} - {"Status Update" if doc_type == "status_update" else "Requirements Document"}

{"Current Status:" if doc_type == "status_update" else "Business Requirements:"}
{"Project is currently {random.randint(25, 85)}% complete" if doc_type == "status_update" else "System must support {random.randint(1000, 10000)} concurrent users"}

{"Recent Accomplishments:" if doc_type == "status_update" else "Functional Requirements:"}
- {"Completed user authentication module" if random.choice([True, False]) else "Implemented data visualization features"}
- {"Integrated with payment gateway" if random.choice([True, False]) else "Deployed staging environment"}
- {"Conducted user acceptance testing" if random.choice([True, False]) else "Optimized database queries"}

{"Upcoming Milestones:" if doc_type == "status_update" else "Technical Requirements:"}
- {"Complete API development" if random.choice([True, False]) else "Finalize mobile responsiveness"}
- {"Deploy to production" if random.choice([True, False]) else "Implement security features"}
- {"Conduct performance testing" if random.choice([True, False]) else "Complete documentation"}

{"Current Challenges:" if doc_type == "status_update" else "Non-Functional Requirements:"}
- {"Third-party API limitations" if random.choice([True, False]) else "Performance optimization needs"}
- {"Resource constraints" if random.choice([True, False]) else "Security compliance requirements"}
- {"Scope creep concerns" if random.choice([True, False]) else "Scalability considerations"}
                """
            
            metadata = DocumentMetadata(
                id=f"project_{project_name.lower().replace(' ', '_')}_{doc_type}_{i}",
                title=f"{project_name} - {doc_type.replace('_', ' ').title()}",
                source="project_management",
                content_type="text",
                created_at=date.isoformat(),
                modified_at=date.isoformat(),
                author=random.choice(['Project Manager', 'Tech Lead', 'Product Owner']),
                keywords=["project", project_name.lower(), doc_type, "development", "planning"],
                file_size=random.randint(30000, 120000)
            )
            
            documents.append(Document(metadata=metadata, content=content.strip()))
        
        return documents
    
    def generate_technical_documents(self) -> List[Document]:
        """Generate dummy technical documentation."""
        documents = []
        
        for i in range(self.config.num_technical_docs):
            doc_type = random.choice(["api_documentation", "architecture", "deployment", "troubleshooting"])
            system_name = f"{random.choice(self.product_names)} System"
            date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            if doc_type == "api_documentation":
                content = f"""
{system_name} API Documentation

Overview:
The {system_name} API provides {"RESTful endpoints" if random.choice([True, False]) else "GraphQL interface"} for 
{"data management" if random.choice([True, False]) else "user authentication"} and {"reporting capabilities" if random.choice([True, False]) else "system integration"}.

Base URL: https://api.{system_name.lower().replace(' ', '')}.com/v{random.randint(1, 3)}

Authentication:
- Method: {"Bearer Token" if random.choice([True, False]) else "API Key"}
- Header: {"Authorization: Bearer <token>" if random.choice([True, False]) else "X-API-Key: <key>"}

Main Endpoints:

GET /users
- Description: Retrieve user information
- Parameters: limit (int), offset (int), filter (string)
- Response: 200 OK with user data array

POST /users
- Description: Create new user
- Body: {{"name": "string", "email": "string", "role": "string"}}
- Response: 201 Created with user object

GET /data/{random.choice(['reports', 'metrics', 'analytics'])}
- Description: Fetch {"reports" if random.choice([True, False]) else "analytics"} data
- Parameters: date_range, format, filters
- Response: 200 OK with data payload

Error Codes:
- 400: Bad Request - Invalid parameters
- 401: Unauthorized - Invalid or missing authentication
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource not found
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Server error

Rate Limiting:
- Limit: {random.randint(100, 1000)} requests per minute
- Headers: X-RateLimit-Limit, X-RateLimit-Remaining

Examples:
curl -H "Authorization: Bearer <token>" https://api.example.com/v1/users?limit=10
                """
            
            elif doc_type == "architecture":
                content = f"""
{system_name} Architecture Documentation

System Overview:
{system_name} is a {"microservices-based" if random.choice([True, False]) else "monolithic"} application designed for
{"high availability" if random.choice([True, False]) else "scalability"} and {"performance" if random.choice([True, False]) else "maintainability"}.

Architecture Pattern:
- {"Event-driven architecture" if random.choice([True, False]) else "Layered architecture"}
- {"Service mesh" if random.choice([True, False]) else "API gateway"} for service communication
- {"CQRS pattern" if random.choice([True, False]) else "Repository pattern"} for data access

Technology Stack:
- Backend: {"Python/Django" if random.choice([True, False]) else "Node.js/Express"}
- Database: {"PostgreSQL" if random.choice([True, False]) else "MongoDB"}
- Cache: {"Redis" if random.choice([True, False]) else "Memcached"}
- Message Queue: {"RabbitMQ" if random.choice([True, False]) else "Apache Kafka"}
- Frontend: {"React" if random.choice([True, False]) else "Vue.js"}

Infrastructure:
- Cloud Provider: {"AWS" if random.choice([True, False]) else "Google Cloud"}
- Containerization: {"Docker" if random.choice([True, False]) else "Kubernetes"}
- CI/CD: {"Jenkins" if random.choice([True, False]) else "GitLab CI"}
- Monitoring: {"Prometheus/Grafana" if random.choice([True, False]) else "DataDog"}

Security:
- Authentication: {"OAuth 2.0" if random.choice([True, False]) else "JWT tokens"}
- Authorization: {"RBAC" if random.choice([True, False]) else "ACL"}
- Encryption: {"TLS 1.3" if random.choice([True, False]) else "AES-256"} for data in transit

Performance:
- {"Load balancing" if random.choice([True, False]) else "Auto-scaling"} for high availability
- {"CDN" if random.choice([True, False]) else "Edge computing"} for content delivery
- {"Database sharding" if random.choice([True, False]) else "Read replicas"} for scalability

Deployment:
- {"Blue-green deployment" if random.choice([True, False]) else "Rolling updates"}
- {"Automated testing" if random.choice([True, False]) else "Canary releases"}
- {"Infrastructure as Code" if random.choice([True, False]) else "Configuration management"}
                """
            
            else:  # deployment or troubleshooting
                content = f"""
{system_name} - {"Deployment Guide" if doc_type == "deployment" else "Troubleshooting Guide"}

{"Prerequisites:" if doc_type == "deployment" else "Common Issues:"}
{"- Docker installed and running" if doc_type == "deployment" else "- System performance degradation"}
{"- Kubernetes cluster access" if doc_type == "deployment" else "- Authentication failures"}
{"- Required environment variables" if doc_type == "deployment" else "- Database connection issues"}

{"Installation Steps:" if doc_type == "deployment" else "Troubleshooting Steps:"}
{"1. Clone repository" if doc_type == "deployment" else "1. Check system logs"}
{"2. Configure environment" if doc_type == "deployment" else "2. Verify service status"}
{"3. Build Docker images" if doc_type == "deployment" else "3. Test database connectivity"}
{"4. Deploy to cluster" if doc_type == "deployment" else "4. Restart failed services"}

{"Configuration:" if doc_type == "deployment" else "Monitoring:"}
{"- Database connection string" if doc_type == "deployment" else "- CPU usage: < 80%"}
{"- API keys and secrets" if doc_type == "deployment" else "- Memory usage: < 85%"}
{"- Resource limits" if doc_type == "deployment" else "- Response time: < 500ms"}

{"Post-Deployment:" if doc_type == "deployment" else "Escalation:"}
{"- Verify all services are running" if doc_type == "deployment" else "- Contact: DevOps team"}
{"- Run health checks" if doc_type == "deployment" else "- Severity levels: Low/Medium/High"}
{"- Monitor system metrics" if doc_type == "deployment" else "- On-call rotation schedule"}
                """
            
            metadata = DocumentMetadata(
                id=f"tech_doc_{system_name.lower().replace(' ', '_')}_{doc_type}_{i}",
                title=f"{system_name} - {doc_type.replace('_', ' ').title()}",
                source="engineering",
                content_type="text",
                created_at=date.isoformat(),
                modified_at=date.isoformat(),
                author=random.choice(['DevOps Engineer', 'Software Architect', 'Senior Developer']),
                keywords=["technical", "documentation", system_name.lower(), doc_type, "engineering"],
                file_size=random.randint(40000, 150000)
            )
            
            documents.append(Document(metadata=metadata, content=content.strip()))
        
        return documents
    
    def generate_hr_documents(self) -> List[Document]:
        """Generate dummy HR documents."""
        documents = []
        
        for i in range(self.config.num_hr_docs):
            doc_type = random.choice(["policy", "handbook", "benefits", "training", "onboarding"])
            date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            if doc_type == "policy":
                policy_name = random.choice(["Remote Work", "Code of Conduct", "Data Privacy", "Leave", "Performance Review"])
                content = f"""
{policy_name} Policy

Effective Date: {date.strftime('%B %d, %Y')}
Policy Number: HR-{random.randint(100, 999)}

Purpose:
This policy establishes guidelines for {"remote work arrangements" if policy_name == "Remote Work" else "employee conduct"} 
to ensure {"productivity and collaboration" if policy_name == "Remote Work" else "a respectful workplace"}.

Scope:
This policy applies to {"all employees" if random.choice([True, False]) else "full-time employees"} 
{"regardless of location" if random.choice([True, False]) else "in all departments"}.

Policy Statement:
{"Employees may work remotely" if policy_name == "Remote Work" else "All employees must maintain professional conduct"} 
{"with manager approval" if random.choice([True, False]) else "in accordance with company values"}.

Guidelines:
- {"Maintain regular communication" if policy_name == "Remote Work" else "Treat colleagues with respect"}
- {"Use secure network connections" if policy_name == "Remote Work" else "Follow confidentiality requirements"}
- {"Participate in team meetings" if policy_name == "Remote Work" else "Report policy violations promptly"}

Responsibilities:
- Employees: {"Follow remote work guidelines" if policy_name == "Remote Work" else "Adhere to policy requirements"}
- Managers: {"Provide necessary support" if policy_name == "Remote Work" else "Ensure policy compliance"}
- HR: {"Monitor policy effectiveness" if policy_name == "Remote Work" else "Investigate violations"}

Violations:
Policy violations may result in {"coaching" if random.choice([True, False]) else "disciplinary action"} 
up to and including {"performance improvement plans" if random.choice([True, False]) else "termination"}.

Review:
This policy will be reviewed {"annually" if random.choice([True, False]) else "every two years"} 
or {"as needed" if random.choice([True, False]) else "based on feedback"}.
                """
            
            elif doc_type == "benefits":
                content = f"""
Employee Benefits Guide

Health Insurance:
- Medical: {"Comprehensive coverage" if random.choice([True, False]) else "Basic health plan"}
- Dental: {"Full dental coverage" if random.choice([True, False]) else "Basic dental plan"}
- Vision: {"Eye care coverage" if random.choice([True, False]) else "Vision plan available"}
- Premium: {"Company pays 80%" if random.choice([True, False]) else "50/50 cost sharing"}

Retirement:
- 401(k) Plan: {"Company matches up to 6%" if random.choice([True, False]) else "4% company match"}
- Vesting: {"Immediate vesting" if random.choice([True, False]) else "3-year vesting schedule"}
- Investment Options: {"20+ mutual funds" if random.choice([True, False]) else "Diversified portfolio"}

Time Off:
- Vacation: {random.randint(15, 25)} days annually
- Sick Leave: {random.randint(5, 10)} days annually
- Personal Days: {random.randint(2, 5)} days annually
- Holidays: {random.randint(10, 15)} company holidays

Additional Benefits:
- {"Flexible work arrangements" if random.choice([True, False]) else "Remote work options"}
- {"Professional development" if random.choice([True, False]) else "Training budget"}
- {"Wellness programs" if random.choice([True, False]) else "Gym membership"}
- {"Employee assistance program" if random.choice([True, False]) else "Mental health support"}

Eligibility:
- Full-time employees: {"All benefits" if random.choice([True, False]) else "Most benefits"}
- Part-time employees: {"Limited benefits" if random.choice([True, False]) else "No benefits"}
- Contractors: {"No benefits" if random.choice([True, False]) else "Limited access"}
                """
            
            else:  # handbook, training, or onboarding
                content = f"""
{"Employee Handbook" if doc_type == "handbook" else "Training Program" if doc_type == "training" else "Onboarding Guide"}

{"Welcome" if doc_type == "handbook" else "Overview" if doc_type == "training" else "New Employee Orientation"}:
{"Welcome to our company!" if doc_type == "handbook" else "This training covers essential skills" if doc_type == "training" else "Welcome to your first day!"}

{"Company Culture" if doc_type == "handbook" else "Learning Objectives" if doc_type == "training" else "First Week Schedule"}:
- {"Innovation and collaboration" if doc_type == "handbook" else "Develop technical skills" if doc_type == "training" else "IT setup and accounts"}
- {"Respect and integrity" if doc_type == "handbook" else "Understand company processes" if doc_type == "training" else "Meet your team"}
- {"Customer focus" if doc_type == "handbook" else "Improve productivity" if doc_type == "training" else "Review job responsibilities"}

{"Workplace Policies" if doc_type == "handbook" else "Training Modules" if doc_type == "training" else "Key Contacts"}:
- {"Dress code guidelines" if doc_type == "handbook" else "Module 1: Company overview" if doc_type == "training" else "Direct Manager: [Name]"}
- {"Communication standards" if doc_type == "handbook" else "Module 2: Technical training" if doc_type == "training" else "HR Representative: [Name]"}
- {"Performance expectations" if doc_type == "handbook" else "Module 3: Practical exercises" if doc_type == "training" else "IT Support: [Contact]"}

{"Resources" if doc_type == "handbook" else "Assessment" if doc_type == "training" else "Resources"}:
- {"Employee portal" if doc_type == "handbook" else "Quiz and practical test" if doc_type == "training" else "Employee handbook"}
- {"HR support" if doc_type == "handbook" else "Certification upon completion" if doc_type == "training" else "Company directory"}
- {"IT helpdesk" if doc_type == "handbook" else "Ongoing support available" if doc_type == "training" else "Benefits information"}
                """
            
            metadata = DocumentMetadata(
                id=f"hr_doc_{doc_type}_{i}",
                title=f"HR - {doc_type.replace('_', ' ').title()}" + (f" ({policy_name})" if doc_type == "policy" else ""),
                source="human_resources",
                content_type="text",
                created_at=date.isoformat(),
                modified_at=date.isoformat(),
                author=random.choice(['HR Manager', 'HR Business Partner', 'HR Generalist']),
                keywords=["hr", "human resources", doc_type, "policy", "employee"],
                file_size=random.randint(25000, 100000)
            )
            
            documents.append(Document(metadata=metadata, content=content.strip()))
        
        return documents
    
    def generate_financial_documents(self) -> List[Document]:
        """Generate dummy financial documents."""
        documents = []
        
        for i in range(self.config.num_financial_docs):
            doc_type = random.choice(["budget", "forecast", "expense_report", "financial_statement"])
            date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            if doc_type == "budget":
                department = random.choice(self.departments)
                content = f"""
{department} Department Budget - FY{date.year}

Budget Summary:
Total Allocated Budget: ${random.randint(500000, 2000000):,}
Spent to Date: ${random.randint(200000, 1500000):,}
Remaining Budget: ${random.randint(100000, 800000):,}

Personnel Costs:
- Salaries: ${random.randint(300000, 1200000):,} ({random.randint(60, 80)}% of budget)
- Benefits: ${random.randint(60000, 240000):,} ({random.randint(12, 20)}% of budget)
- Contractors: ${random.randint(20000, 120000):,} ({random.randint(4, 10)}% of budget)

Operational Expenses:
- Software Licenses: ${random.randint(10000, 80000):,}
- Equipment: ${random.randint(15000, 60000):,}
- Travel: ${random.randint(5000, 30000):,}
- Training: ${random.randint(8000, 40000):,}
- Office Supplies: ${random.randint(2000, 15000):,}

Quarterly Breakdown:
- Q1: ${random.randint(100000, 400000):,} ({random.randint(20, 30)}% of annual)
- Q2: ${random.randint(120000, 450000):,} ({random.randint(25, 35)}% of annual)
- Q3: ${random.randint(110000, 420000):,} ({random.randint(22, 32)}% of annual)
- Q4: ${random.randint(100000, 380000):,} ({random.randint(18, 28)}% of annual)

Variance Analysis:
- {"Over budget" if random.choice([True, False]) else "Under budget"} by {random.randint(2, 15)}%
- {"Higher than expected" if random.choice([True, False]) else "Lower than expected"} personnel costs
- {"Increased" if random.choice([True, False]) else "Decreased"} software licensing expenses
                """
            
            elif doc_type == "forecast":
                content = f"""
Financial Forecast - Next 12 Months

Revenue Projections:
- Q1: ${random.randint(2000000, 5000000):,}
- Q2: ${random.randint(2200000, 5500000):,}
- Q3: ${random.randint(2100000, 5200000):,}
- Q4: ${random.randint(2400000, 5800000):,}
- Total Annual: ${random.randint(8500000, 21000000):,}

Growth Assumptions:
- {"Organic growth" if random.choice([True, False]) else "Market expansion"}: {random.randint(10, 25)}%
- {"New product launches" if random.choice([True, False]) else "Customer acquisition"}: {random.randint(5, 15)}%
- {"Market penetration" if random.choice([True, False]) else "Pricing optimization"}: {random.randint(3, 12)}%

Cost Structure:
- Cost of Goods Sold: {random.randint(40, 60)}% of revenue
- Operating Expenses: {random.randint(25, 40)}% of revenue
- Research & Development: {random.randint(8, 15)}% of revenue

Key Metrics:
- Gross Margin: {random.randint(40, 65)}%
- Operating Margin: {random.randint(15, 30)}%
- Net Margin: {random.randint(8, 20)}%

Risk Factors:
- {"Economic downturn" if random.choice([True, False]) else "Competitive pressure"}
- {"Supply chain disruption" if random.choice([True, False]) else "Regulatory changes"}
- {"Currency fluctuations" if random.choice([True, False]) else "Technology shifts"}

Opportunities:
- {"New market entry" if random.choice([True, False]) else "Strategic partnerships"}
- {"Product innovation" if random.choice([True, False]) else "Operational efficiency"}
- {"Digital transformation" if random.choice([True, False]) else "Acquisitions"}
                """
            
            else:  # expense_report or financial_statement
                content = f"""
{"Monthly Expense Report" if doc_type == "expense_report" else "Financial Statement"} - {date.strftime('%B %Y')}

{"Expense Categories:" if doc_type == "expense_report" else "Income Statement:"}
{"- Travel & Entertainment: $" + str(random.randint(5000, 25000)) if doc_type == "expense_report" else "- Revenue: $" + str(random.randint(1000000, 5000000))}
{"- Office Supplies: $" + str(random.randint(1000, 8000)) if doc_type == "expense_report" else "- Cost of Sales: $" + str(random.randint(400000, 2000000))}
{"- Software & Tools: $" + str(random.randint(3000, 15000)) if doc_type == "expense_report" else "- Gross Profit: $" + str(random.randint(500000, 2500000))}
{"- Training & Development: $" + str(random.randint(2000, 12000)) if doc_type == "expense_report" else "- Operating Expenses: $" + str(random.randint(300000, 1500000))}

{"Department Breakdown:" if doc_type == "expense_report" else "Balance Sheet:"}
{"- Engineering: $" + str(random.randint(8000, 30000)) if doc_type == "expense_report" else "- Assets: $" + str(random.randint(2000000, 10000000))}
{"- Sales: $" + str(random.randint(12000, 40000)) if doc_type == "expense_report" else "- Liabilities: $" + str(random.randint(800000, 4000000))}
{"- Marketing: $" + str(random.randint(6000, 25000)) if doc_type == "expense_report" else "- Equity: $" + str(random.randint(1000000, 5000000))}

{"Approvals:" if doc_type == "expense_report" else "Cash Flow:"}
{"- Manager Approved: " + str(random.randint(80, 95)) + "%" if doc_type == "expense_report" else "- Operating Cash Flow: $" + str(random.randint(200000, 1000000))}
{"- Pending Review: " + str(random.randint(2, 10)) + "%" if doc_type == "expense_report" else "- Investing Cash Flow: $" + str(random.randint(-200000, 100000))}
{"- Rejected: " + str(random.randint(1, 8)) + "%" if doc_type == "expense_report" else "- Financing Cash Flow: $" + str(random.randint(-100000, 500000))}
                """
            
            metadata = DocumentMetadata(
                id=f"finance_doc_{doc_type}_{i}",
                title=f"Finance - {doc_type.replace('_', ' ').title()}" + (f" ({department})" if doc_type == "budget" else ""),
                source="finance",
                content_type="text",
                created_at=date.isoformat(),
                modified_at=date.isoformat(),
                author=random.choice(['CFO', 'Finance Manager', 'Financial Analyst']),
                keywords=["finance", "financial", doc_type, "budget", "expenses"],
                file_size=random.randint(20000, 80000)
            )
            
            documents.append(Document(metadata=metadata, content=content.strip()))
        
        return documents
    
    def generate_all_documents(self) -> List[Document]:
        """Generate all dummy documents."""
        all_documents = []
        
        print("Generating sales reports...")
        all_documents.extend(self.generate_sales_reports())
        
        print("Generating project documents...")
        all_documents.extend(self.generate_project_documents())
        
        print("Generating technical documents...")
        all_documents.extend(self.generate_technical_documents())
        
        print("Generating HR documents...")
        all_documents.extend(self.generate_hr_documents())
        
        print("Generating financial documents...")
        all_documents.extend(self.generate_financial_documents())
        
        return all_documents
    
    def save_documents_to_files(self, documents: List[Document], output_dir: str = "dummy_documents"):
        """Save documents to text files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for doc in documents:
            file_path = output_path / f"{doc.metadata.id}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {doc.metadata.title}\n")
                f.write(f"Source: {doc.metadata.source}\n")
                f.write(f"Content Type: {doc.metadata.content_type}\n")
                f.write(f"Created: {doc.metadata.created_at}\n")
                f.write(f"Author: {doc.metadata.author}\n")
                f.write(f"Keywords: {', '.join(doc.metadata.keywords)}\n")
                f.write("=" * 50 + "\n\n")
                f.write(doc.content)
        
        print(f"Saved {len(documents)} documents to {output_path}")
    
    def generate_api_responses(self) -> Dict[str, Any]:
        """Generate sample API responses for testing."""
        documents = self.generate_all_documents()
        
        # Convert to API response format
        api_responses = {
            "documents": [
                {
                    "id": doc.metadata.id,
                    "title": doc.metadata.title,
                    "source": doc.metadata.source,
                    "content_type": doc.metadata.content_type,
                    "created_at": doc.metadata.created_at,
                    "author": doc.metadata.author,
                    "keywords": doc.metadata.keywords,
                    "file_size": doc.metadata.file_size,
                    "content": doc.content
                }
                for doc in documents
            ]
        }
        
        # Generate search responses
        search_queries = [
            "sales performance", "project retrospective", "technical documentation",
            "HR policy", "financial forecast", "budget analysis", "quarterly results"
        ]
        
        api_responses["search_results"] = {}
        for query in search_queries:
            matching_docs = [
                doc for doc in documents 
                if any(keyword in query.lower() for keyword in doc.metadata.keywords)
            ][:5]  # Limit to 5 results
            
            api_responses["search_results"][query] = {
                "query": query,
                "total_results": len(matching_docs),
                "results": [
                    {
                        "id": doc.metadata.id,
                        "title": doc.metadata.title,
                        "source": doc.metadata.source,
                        "content": doc.content[:500] + "..." if len(doc.content) > 500 else doc.content,
                        "relevance_score": random.uniform(0.6, 0.99)
                    }
                    for doc in matching_docs
                ]
            }
        
        return api_responses
    
    def save_api_responses(self, api_responses: Dict[str, Any], output_file: str = "api_responses.json"):
        """Save API responses to JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(api_responses, f, indent=2, ensure_ascii=False)
        
        print(f"Saved API responses to {output_file}")


# Example usage
if __name__ == "__main__":
    config = DummyDataConfig(
        num_sales_reports=15,
        num_project_docs=20,
        num_technical_docs=12,
        num_hr_docs=10,
        num_financial_docs=8
    )
    
    generator = DummyDataGenerator(config)
    
    # Generate all documents
    documents = generator.generate_all_documents()
    print(f"Generated {len(documents)} total documents")
    
    # Save to files
    generator.save_documents_to_files(documents)
    
    # Generate API responses
    api_responses = generator.generate_api_responses()
    generator.save_api_responses(api_responses)
    
    print("Dummy data generation completed!")
    print(f"Documents by type:")
    from collections import Counter
    sources = Counter(doc.metadata.source for doc in documents)
    for source, count in sources.items():
        print(f"  {source}: {count} documents")