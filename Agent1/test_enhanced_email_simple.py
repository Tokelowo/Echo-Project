"""
Test Enhanced Email Content - Generate a sample email to preview enhancements
"""
from datetime import datetime

# Simple test without Django dependencies
class MockEnhancedEmailFormatter:
    """Mock version for testing the email template structure"""
    
    def __init__(self):
        self.microsoft_blue = '#0078d4'
        self.microsoft_gray = '#605e5c'
        self.microsoft_light_gray = '#f3f2f1'
    
    def create_enhanced_email_summary(self, report_data, user_name=None, docx_filename=None):
        """Create enhanced email summary for testing"""
        
        # Generate email subject with personalization
        report_title = report_data.get('title', 'Intelligence Report')
        is_subscription = report_data.get('is_subscription_email', False)
        subscription_frequency = report_data.get('subscription_frequency', '')
        
        if is_subscription and subscription_frequency:
            subject = f"📊 Your {subscription_frequency.title()} Intelligence Report - {report_title}"
        else:
            subject = f"Microsoft Defender for Office 365 - {report_title}"
        
        # Generate personalized greeting
        greeting = f"Dear {user_name}," if user_name else "Dear Valued Customer,"
        
        # Extract key data
        executive_summary = report_data.get('executive_summary', 'Comprehensive analysis.')
        gen_time = report_data.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        articles_analyzed = report_data.get('articles_analyzed', 0)
        
        # Count threat categories
        threat_analysis = report_data.get('threat_analysis', [])
        threat_count = len(threat_analysis) if isinstance(threat_analysis, list) else 0
        
        # Count competitive insights
        competitive_analysis = report_data.get('competitive_analysis', [])
        competitive_count = len(competitive_analysis) if isinstance(competitive_analysis, list) else 0
        
        # Create engagement metrics
        engagement_metrics = {
            'data_sources': articles_analyzed,
            'threat_categories': threat_count,
            'competitive_insights': competitive_count,
            'freshness_score': 'Real-Time',
            'confidence_level': 'High'
        }
        
        # Generate key insights
        key_insights = [
            f"📈 Market showing strong growth with {articles_analyzed} sources analyzed",
            f"⚠️ {threat_count} active threat categories identified requiring immediate attention",
            f"🏆 Competitive intelligence from {competitive_count} market leaders analyzed",
            "🚀 AI-powered threat detection capabilities showing 23% improvement",
            "⏰ Real-time intelligence update ensuring maximum relevance and actionability"
        ]
        
        # Generate recommendations
        recommendations = [
            {
                'action': 'Enhanced Security Monitoring',
                'description': f'With {threat_count} threat categories detected, implement proactive monitoring protocols'
            },
            {
                'action': 'Strategic Market Analysis',
                'description': 'Leverage comprehensive intelligence for strategic decision-making'
            },
            {
                'action': 'Team Intelligence Briefing',
                'description': 'Share critical insights with security team for coordinated response'
            }
        ]
        
        # Build enhanced HTML content
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft Defender for Office 365 - Enhanced Intelligence Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; line-height: 1.6; }}
        .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.12); }}
        .header {{ background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 600; }}
        .logo {{ font-size: 18px; margin-bottom: 15px; letter-spacing: 1px; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .greeting {{ font-size: 16px; margin-bottom: 25px; color: #323130; }}
        .engagement-metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric-card {{ background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #e1dfdd; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .metric-number {{ font-size: 28px; font-weight: bold; color: #0078d4; margin-bottom: 8px; }}
        .metric-label {{ font-size: 14px; color: #605e5c; font-weight: 500; }}
        .insights-section {{ background: linear-gradient(135deg, #fff8e1 0%, #fff3c4 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #ff9800; }}
        .recommendations-section {{ background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #9c27b0; }}
        .section-title {{ margin-top: 0; color: #333; font-size: 20px; margin-bottom: 15px; }}
        .insight-item, .recommendation-item {{ margin-bottom: 12px; padding: 12px; background: rgba(255,255,255,0.7); border-radius: 8px; }}
        .cta-button {{ background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600; margin: 10px 8px; }}
        .footer {{ background: linear-gradient(135deg, #605e5c 0%, #484644 100%); color: white; padding: 30px; text-align: center; }}
        .real-data-badge {{ background: linear-gradient(135deg, #107c10 0%, #0e6b0e 100%); color: white; padding: 12px 20px; border-radius: 8px; font-weight: bold; margin-bottom: 25px; display: inline-block; }}
        @media (max-width: 600px) {{
            .engagement-metrics {{ grid-template-columns: 1fr; }}
            .content {{ padding: 25px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🔷 MICROSOFT DEFENDER FOR OFFICE 365</div>
            <h1>{report_title}</h1>
            <p style="margin: 8px 0; opacity: 0.9;">Generated: {gen_time}</p>
        </div>
        
        <div class="content">
            <div class="greeting">{greeting}</div>
            
            <div style="background: linear-gradient(135deg, #e7f3ff 0%, #cce7ff 100%); padding: 20px; border-radius: 8px; margin-bottom: 25px;">
                <h3 style="margin-top: 0; color: #0078d4;">👋 Hello {user_name if user_name else 'Valued Customer'}!</h3>
                <p style="margin-bottom: 0;">Your {subscription_frequency} intelligence briefing is ready. We've analyzed the latest market data to keep you ahead of emerging threats.</p>
            </div>
            
            <div class="real-data-badge">✓ 100% Real-Time Intelligence Analysis</div>
            
            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #4caf50;">
                <h3 style="margin-top: 0; color: #2e7d32;">📊 Executive Intelligence Summary</h3>
                <p style="margin: 0; font-size: 16px; line-height: 1.8;">{executive_summary}</p>
            </div>
            
            <div class="engagement-metrics">
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['data_sources']}</div>
                    <div class="metric-label">Sources Analyzed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['threat_categories']}</div>
                    <div class="metric-label">Threat Categories</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['competitive_insights']}</div>
                    <div class="metric-label">Competitive Insights</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['freshness_score']}</div>
                    <div class="metric-label">Data Freshness</div>
                </div>
            </div>
            
            <div class="insights-section">
                <h3 class="section-title">🔍 Key Intelligence Insights</h3>
                {"".join([f'<div class="insight-item">• {insight}</div>' for insight in key_insights[:4]])}
            </div>
            
            <div class="recommendations-section">
                <h3 class="section-title">🎯 Personalized Recommendations</h3>
                {"".join([f'<div class="recommendation-item"><strong>{rec["action"]}:</strong> {rec["description"]}</div>' for rec in recommendations[:3]])}
            </div>
            
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 25px; border-radius: 12px; border-left: 5px solid #2196f3; margin: 25px 0;">
                <h3 style="margin-top: 0; color: #1976d2;">📎 Complete Intelligence Report</h3>
                <p>Your comprehensive analysis is attached as <strong>{docx_filename or 'Intelligence_Report.docx'}</strong> with detailed insights, charts, and strategic recommendations.</p>
                <p style="margin-bottom: 0;"><strong>💡 Pro Tip:</strong> Share key insights with your security team for maximum organizational impact.</p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <h3 style="color: #333; margin-bottom: 20px;">🚀 Take Action Now</h3>
                <a href="https://localhost:3001/subscriptions" class="cta-button">📧 Manage Subscriptions</a>
                <a href="https://security.microsoft.com" class="cta-button">🛡️ Security Dashboard</a>
                <a href="https://docs.microsoft.com/defender" class="cta-button">📚 Learn More</a>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 0; font-size: 18px; font-weight: 600;">Microsoft Defender for Office 365</p>
            <p style="margin: 8px 0; opacity: 0.9;">Intelligent email security for the modern workplace</p>
            <div style="margin: 20px 0;">
                <a href="https://security.microsoft.com" style="color: #ffffff; text-decoration: none; margin: 0 15px;">Security Center</a>
                <a href="https://docs.microsoft.com/defender" style="color: #ffffff; text-decoration: none; margin: 0 15px;">Documentation</a>
                <a href="https://aka.ms/defendersupport" style="color: #ffffff; text-decoration: none; margin: 0 15px;">Support</a>
            </div>
            
            <div style="background-color: #f8f9fa; color: #605e5c; padding: 20px; margin-top: 20px; border-radius: 8px; font-size: 13px; text-align: center;">
                <p style="margin: 8px 0; font-weight: 500;">📧 Subscription Management</p>
                <p style="margin: 8px 0;">You're receiving {subscription_frequency} intelligence reports to stay ahead of emerging threats.</p>
                <p style="margin: 8px 0;">
                    <a href="https://localhost:3001/subscriptions" style="color: #0078d4; text-decoration: none;">Update preferences</a> | 
                    <a href="https://localhost:3001/unsubscribe" style="color: #0078d4; text-decoration: none;">Unsubscribe</a>
                </p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        # Build plain text version
        plain_text_body = f"""
🔷 MICROSOFT DEFENDER FOR OFFICE 365
Enhanced Intelligence Report
Generated: {gen_time}
{"="*70}

{greeting}

👋 PERSONALIZED BRIEFING FOR {user_name.upper() if user_name else 'VALUED CUSTOMER'}
Your {subscription_frequency} intelligence report is ready with the latest
market data to keep you ahead of emerging threats and opportunities.
{"-"*50}

✓ 100% REAL-TIME INTELLIGENCE ANALYSIS

📊 EXECUTIVE INTELLIGENCE SUMMARY
{executive_summary}

🎯 ENGAGEMENT METRICS
• Sources Analyzed: {engagement_metrics['data_sources']}
• Threat Categories: {engagement_metrics['threat_categories']}
• Competitive Insights: {engagement_metrics['competitive_insights']}
• Data Freshness: {engagement_metrics['freshness_score']}
• Analysis Confidence: {engagement_metrics['confidence_level']}

🔍 KEY INTELLIGENCE INSIGHTS
{chr(10).join([f'• {insight}' for insight in key_insights[:4]])}

🎯 PERSONALIZED RECOMMENDATIONS
{chr(10).join([f'• {rec["action"]}: {rec["description"]}' for rec in recommendations[:3]])}

📎 COMPLETE INTELLIGENCE REPORT ATTACHED
Your comprehensive analysis is attached as {docx_filename or 'Intelligence_Report.docx'} with:
• Detailed threat landscape analysis
• Competitive positioning charts
• Strategic recommendations
• Market trend visualizations

💡 Pro Tip: Share key insights with your security team for maximum impact.

🚀 TAKE ACTION NOW
1. Review the comprehensive attached report
2. Share critical insights with your security team
3. Update threat monitoring protocols
4. Manage subscriptions: https://localhost:3001/subscriptions

📞 SUPPORT & RESOURCES
• Security Dashboard: https://security.microsoft.com
• Documentation: https://docs.microsoft.com/defender
• Support: https://aka.ms/defendersupport

📧 SUBSCRIPTION MANAGEMENT
You're receiving {subscription_frequency} intelligence reports to stay ahead
of emerging email security threats.
• Update preferences: https://localhost:3001/subscriptions
• Unsubscribe: https://localhost:3001/unsubscribe

---
Microsoft Defender for Office 365
Intelligent email security for the modern workplace
© {datetime.now().year} Microsoft Corporation. All rights reserved.
        """
        
        return {
            'subject': subject,
            'html_body': html_body.strip(),
            'plain_text_body': plain_text_body.strip(),
            'from_name': 'Microsoft Defender Intelligence Team',
            'from_email': 'defender-intelligence@microsoft.com',
            'engagement_score': len(key_insights) + len(recommendations),
            'personalization_level': 'high' if user_name else 'standard'
        }

def test_enhanced_email():
    """Test the enhanced email formatter with sample data"""
    
    # Create sample report data
    sample_report_data = {
        'title': 'Weekly Email Security Intelligence Report',
        'executive_summary': 'This week\'s analysis reveals significant evolution in email-based threats, with phishing attacks increasing by 23% and new ransomware variants targeting Office 365 environments. Market consolidation continues as organizations prioritize integrated security solutions.',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M UTC'),
        'articles_analyzed': 147,
        'market_analysis': {
            'growth_rate': 'Strong 18% YoY increase in email security investments',
            'growth_drivers': 'Remote work expansion and sophisticated threat evolution'
        },
        'threat_analysis': [
            {'threat_type': 'Advanced Phishing Campaigns', 'severity': 'high'},
            {'threat_type': 'Business Email Compromise', 'severity': 'critical'},
            {'threat_type': 'Ransomware Delivery via Email', 'severity': 'high'},
            {'threat_type': 'Account Takeover Attacks', 'severity': 'medium'},
            {'threat_type': 'Supply Chain Email Attacks', 'severity': 'high'}
        ],
        'competitive_analysis': [
            {'company': 'Proofpoint', 'market_share': '22%'},
            {'company': 'Mimecast', 'market_share': '18%'},
            {'company': 'Barracuda', 'market_share': '15%'}
        ],
        'technology_trends': {
            'emerging_technologies': ['AI-powered threat detection', 'Zero-trust email architecture', 'Behavioral analytics']
        },
        # Subscription-specific data
        'is_subscription_email': True,
        'subscription_frequency': 'weekly',
        'subscription_agent': 'intelligence_agent',
        'unsubscribe_url': 'https://localhost:3001/unsubscribe?token=sample123&email=test@example.com',
        'manage_subscription_url': 'https://localhost:3001/subscriptions?email=test@example.com'
    }
    
    # Create enhanced formatter
    formatter = MockEnhancedEmailFormatter()
    
    # Generate enhanced email content
    email_content = formatter.create_enhanced_email_summary(
        sample_report_data, 
        'John Smith',  # User name for personalization
        'Microsoft_Defender_Intelligence_Report_20250102_1430.docx'
    )
    
    # Save HTML content for preview
    html_file_path = 'c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Agent 1\\enhanced_email_preview.html'
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(email_content['html_body'])
    
    # Save plain text content for preview
    text_file_path = 'c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Agent 1\\enhanced_email_preview.txt'
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(email_content['plain_text_body'])
    
    print("✅ Enhanced Email Content Generated Successfully!")
    print(f"📧 Subject: {email_content['subject']}")
    print(f"📊 Engagement Score: {email_content.get('engagement_score', 'N/A')}")
    print(f"🎯 Personalization Level: {email_content.get('personalization_level', 'N/A')}")
    print(f"📄 HTML Preview: {html_file_path}")
    print(f"📝 Text Preview: {text_file_path}")
    print("\n" + "="*60)
    print("📋 EMAIL PREVIEW - First 800 characters:")
    print("="*60)
    print(email_content['plain_text_body'][:800] + "...")
    
    return email_content

if __name__ == "__main__":
    test_enhanced_email()
