"""
Internal Microsoft Defender for Office 365 Knowledge Base
Contains comprehensive information about MDO features, capabilities, and market positioning
"""

MDO_INTERNAL_KNOWLEDGE = {
    "product_overview": {
        "name": "Microsoft Defender for Office 365",
        "version": "Plan 1 & Plan 2",
        "last_updated": "2025-06-18",
        "market_position": "Enterprise Email Security Leader"
    },
    
    "core_features": {
        "safe_attachments": {
            "name": "Safe Attachments",
            "description": "Advanced threat protection for email attachments using dynamic analysis",
            "release_date": "2016-04-01",
            "latest_update": "2025-05-15",
            "capabilities": [
                "Zero-day malware detection",
                "Dynamic file analysis in sandbox",
                "Real-time threat intelligence",
                "Integration with Microsoft Graph Security API"
            ],
            "market_advantage": "Industry-leading detection rates for unknown threats",
            "adoption_rate": 89.2,
            "customer_satisfaction": 4.6
        },
        
        "safe_links": {
            "name": "Safe Links", 
            "description": "Real-time URL scanning and protection against malicious links",
            "release_date": "2016-04-01",
            "latest_update": "2025-06-10",
            "capabilities": [
                "Real-time URL reputation checking",
                "Time-of-click protection",
                "Link wrapping and rewriting",
                "Integration with Office applications"
            ],
            "market_advantage": "Fastest time-of-click protection in the industry",
            "adoption_rate": 92.8,
            "customer_satisfaction": 4.7
        },
        
        "anti_phishing": {
            "name": "Anti-Phishing Protection",
            "description": "Advanced protection against phishing campaigns and impersonation attacks",
            "release_date": "2017-09-01", 
            "latest_update": "2025-06-01",
            "capabilities": [
                "Machine learning-based detection",
                "Impersonation protection",
                "Spoof intelligence",
                "DMARC, SPF, DKIM validation"
            ],
            "market_advantage": "99.9% phishing detection accuracy",
            "adoption_rate": 94.5,
            "customer_satisfaction": 4.8
        },
        
        "attack_simulation": {
            "name": "Attack Simulation Training",
            "description": "Automated phishing simulation and security awareness training",
            "release_date": "2020-03-01",
            "latest_update": "2025-05-20",
            "capabilities": [
                "Automated phishing campaigns",
                "Customizable training content",
                "Real-time reporting and analytics",
                "Integration with Microsoft Learn"
            ],
            "market_advantage": "Only native simulation platform in major email security suite",
            "adoption_rate": 76.3,
            "customer_satisfaction": 4.5
        }
    },
    
    "recent_releases": {
        "2025_q2": [
            {
                "feature": "Enhanced Zero Trust Integration",
                "release_date": "2025-06-15",
                "description": "Deeper integration with Microsoft Zero Trust architecture",
                "impact": "Improved conditional access and identity-based policies"
            },
            {
                "feature": "AI-Powered Threat Hunting",
                "release_date": "2025-05-30",
                "description": "Advanced AI capabilities for proactive threat detection",
                "impact": "40% improvement in advanced persistent threat detection"
            },
            {
                "feature": "Enhanced Mobile Protection",
                "release_date": "2025-05-15",
                "description": "Extended protection for mobile email clients",
                "impact": "Complete mobile email security coverage"
            }
        ]
    },
    
    "competitive_advantages": {
        "integration": "Native integration with Microsoft 365 ecosystem",
        "ai_ml": "Advanced AI/ML models trained on Microsoft's global threat intelligence",
        "zero_trust": "Built-in Zero Trust security architecture",
        "scalability": "Handles enterprise-scale deployments with minimal latency",
        "compliance": "Comprehensive compliance coverage (SOC2, ISO27001, GDPR, HIPAA)"
    },
    
    "market_metrics": {
        "market_share": 23.4,  # Percentage of enterprise email security market
        "customer_count": 350000,  # Number of organizations using MDO
        "threat_detection_rate": 99.94,  # Percentage of threats detected
        "false_positive_rate": 0.002,  # Percentage of false positives
        "uptime": 99.99  # Service uptime percentage
    },
    
    "key_competitors": {
        "proofpoint": {
            "market_share": 21.8,
            "strengths": ["Advanced threat protection", "Data loss prevention"],
            "weaknesses": ["Complex deployment", "Higher cost per user"]
        },
        "mimecast": {
            "market_share": 15.6,
            "strengths": ["Email archiving", "Backup and recovery"],
            "weaknesses": ["Limited scalability", "Older technology stack"]
        },
        "abnormal_security": {
            "market_share": 8.2,
            "strengths": ["AI-based detection", "API integration"],
            "weaknesses": ["Limited feature set", "Newer player"]
        },
        "crowdstrike": {
            "market_share": 6.1,
            "strengths": ["Endpoint integration", "Threat intelligence"],
            "weaknesses": ["Email not core focus", "Limited email features"]
        }
    }
}

INTERNAL_THREAT_INTELLIGENCE = {
    "latest_threats": [
        {
            "threat_name": "BEC 3.0 Campaigns",
            "first_detected": "2025-06-10",
            "severity": "High",
            "mdo_protection": "Blocked by Anti-Phishing with 99.8% accuracy",
            "description": "Advanced business email compromise using AI-generated content"
        },
        {
            "threat_name": "Zero-Font Phishing",
            "first_detected": "2025-06-05",
            "severity": "Medium",
            "mdo_protection": "Detected by Safe Links and content analysis",
            "description": "Phishing emails using zero-width fonts to evade detection"
        }
    ],
    
    "protection_effectiveness": {
        "q2_2025": {
            "threats_blocked": 2400000000,
            "new_threats_detected": 156000,
            "zero_day_protection": 99.7,
            "customer_incidents_prevented": 450000
        }
    }
}
