#!/usr/bin/env python3
"""
Generate a test report with the updated FormattingAgent to verify content
"""
import os
import sys

# Add the django-backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from research_agent.formatting_agent import FormattingAgent
from research_agent.cybersecurity_news_service_new import CybersecurityNewsService
from datetime import datetime

def generate_test_report():
    """Generate a test report to verify content"""
    
    print("🔍 Generating Test Report with Real Data")
    print("=" * 50)
    
    try:
        # Initialize services
        formatting_agent = FormattingAgent()
        news_service = CybersecurityNewsService()
        
        # Fetch real data
        print("📰 Fetching real cybersecurity news...")
        articles = news_service.fetch_cybersecurity_news(max_articles=25)
        print(f"✅ Fetched {len(articles)} articles")
        
        # Create real report data structure (similar to views.py)
        current_date = datetime.now()
        total_articles = len(articles)
        
        # Real data extraction variables
        phishing_mentions = 0
        ransomware_mentions = 0
        ai_threat_mentions = 0
        real_threat_count = 0
        
        ai_ml_mentions = 0
        zero_trust_mentions = 0
        cloud_security_mentions = 0
        
        microsoft_articles = 0
        proofpoint_articles = 0
        mimecast_articles = 0
        
        growth_keywords = 0
        investment_mentions = 0
        market_expansion_mentions = 0
        
        # Process each article for real data extraction
        for article in articles:
            title = article.get('title', '').lower()
            content = article.get('content', '').lower()
            full_text = f"{title} {content}"
            
            # Count real threat mentions
            if any(word in full_text for word in ['phishing', 'phish', 'spear phish']):
                phishing_mentions += 1
                real_threat_count += 1
            if any(word in full_text for word in ['ransomware', 'crypto', 'encryption attack']):
                ransomware_mentions += 1
                real_threat_count += 1
            if any(word in full_text for word in ['ai threat', 'artificial intelligence attack', 'deepfake']):
                ai_threat_mentions += 1
                real_threat_count += 1
            
            # Count real technology adoption mentions
            if any(word in full_text for word in ['artificial intelligence', 'machine learning', 'ai detection', 'ml detection']):
                ai_ml_mentions += 1
            if any(word in full_text for word in ['zero trust', 'zero-trust']):
                zero_trust_mentions += 1
            if any(word in full_text for word in ['cloud security', 'cloud-native', 'cloud protection']):
                cloud_security_mentions += 1
            
            # Count real competitive mentions
            if any(word in full_text for word in ['microsoft', 'defender', 'office 365']):
                microsoft_articles += 1
            if 'proofpoint' in full_text:
                proofpoint_articles += 1
            if 'mimecast' in full_text:
                mimecast_articles += 1
            
            # Count real growth indicators
            if any(word in full_text for word in ['growth', 'expand', 'increase', 'rising', 'surge']):
                growth_keywords += 1
            if any(word in full_text for word in ['investment', 'funding', 'acquisition', 'merger']):
                investment_mentions += 1
            if any(word in full_text for word in ['market', 'industry growth', 'sector expansion']):
                market_expansion_mentions += 1
        
        # Calculate real market intelligence from parsed data only
        threat_intensity = (real_threat_count / max(total_articles, 1)) * 100
        growth_sentiment = (growth_keywords / max(total_articles, 1)) * 100
        ai_adoption_indicator = (ai_ml_mentions / max(total_articles, 1)) * 100
        
        # Real competitive landscape percentages based on actual mentions
        total_vendor_mentions = microsoft_articles + proofpoint_articles + mimecast_articles
        if total_vendor_mentions > 0:
            microsoft_share = (microsoft_articles / total_vendor_mentions) * 100
            proofpoint_share = (proofpoint_articles / total_vendor_mentions) * 100
            mimecast_share = (mimecast_articles / total_vendor_mentions) * 100
            others_share = 100 - (microsoft_share + proofpoint_share + mimecast_share)
        else:
            microsoft_share = 0
            proofpoint_share = 0
            mimecast_share = 0
            others_share = 0
        
        # Get technology trends and market presence
        tech_trends = news_service.analyze_technology_trends(articles)
        market_presence = news_service.analyze_market_presence(articles)
        
        # Create comprehensive report data structure
        report_data = {
            'title': 'Real-Time Email Security Market Intelligence Report',
            'executive_summary': f'Live market analysis based on {total_articles} real cybersecurity articles. Threat intensity at {threat_intensity:.1f}%, with {real_threat_count} threat mentions across sources. Microsoft mentioned in {microsoft_articles} articles ({microsoft_share:.1f}% of vendor coverage). Market growth sentiment at {growth_sentiment:.1f}% based on {growth_keywords} growth indicators. Data extracted from real cybersecurity news sources on {current_date.strftime("%Y-%m-%d")}.',
            'market_intelligence': {
                'data_source': 'real_time_cybersecurity_news',
                'articles_analyzed': total_articles,
                'data_collection_timestamp': current_date.isoformat(),
                'real_threat_metrics': {
                    'total_threat_mentions': real_threat_count,
                    'phishing_articles': phishing_mentions,
                    'ransomware_articles': ransomware_mentions,
                    'ai_threat_articles': ai_threat_mentions,
                    'threat_intensity_percentage': round(threat_intensity, 1)
                },
                'real_technology_adoption': {
                    'ai_ml_mentions': ai_ml_mentions,
                    'zero_trust_mentions': zero_trust_mentions,
                    'cloud_security_mentions': cloud_security_mentions,
                    'ai_adoption_indicator': round(ai_adoption_indicator, 1)
                },
                'real_competitive_landscape': {
                    'microsoft_articles': microsoft_articles,
                    'proofpoint_articles': proofpoint_articles,
                    'mimecast_articles': mimecast_articles,
                    'total_vendor_mentions': total_vendor_mentions,
                    'microsoft_mention_share': round(microsoft_share, 1),
                    'proofpoint_mention_share': round(proofpoint_share, 1),
                    'mimecast_mention_share': round(mimecast_share, 1),
                    'others_mention_share': round(others_share, 1)
                },
                'real_market_indicators': {
                    'growth_keyword_mentions': growth_keywords,
                    'investment_mentions': investment_mentions,
                    'market_expansion_mentions': market_expansion_mentions,
                    'growth_sentiment_score': round(growth_sentiment, 1)
                },
                'parsed_data_summary': {
                    'sources_analyzed': len(set([article.get('source', 'unknown') for article in articles])),
                    'latest_article_date': max([article.get('published_date', current_date.isoformat()) for article in articles]) if articles else current_date.isoformat(),
                    'oldest_article_date': min([article.get('published_date', current_date.isoformat()) for article in articles]) if articles else current_date.isoformat()
                }
            },
            'technology_trends': tech_trends,
            'market_presence': market_presence,
            'articles_analyzed': total_articles,
            'generated_at': current_date.isoformat(),
            'agent_type': 'comprehensive_research',
            'data_validation': {
                'real_data_only': True,
                'no_synthetic_values': True,
                'source_verification': 'live_cybersecurity_feeds'
            }
        }
        
        print("📄 Generating .docx report...")
        
        # Generate the .docx report
        docx_stream = formatting_agent.create_professional_docx_report(report_data, "Test User")
        
        # Save to file for verification
        filename = f"test_report_updated_{current_date.strftime('%Y%m%d_%H%M%S')}.docx"
        with open(filename, 'wb') as f:
            f.write(docx_stream.read())
        
        print(f"✅ Report generated successfully: {filename}")
        print(f"📊 File size: {os.path.getsize(filename):,} bytes")
        
        # Print data summary
        print("\n📊 Real Data Content Summary:")
        print(f"  • Articles analyzed: {total_articles}")
        print(f"  • Threat mentions: {real_threat_count} (Intensity: {threat_intensity:.1f}%)")
        print(f"  • Phishing: {phishing_mentions}, Ransomware: {ransomware_mentions}, AI threats: {ai_threat_mentions}")
        print(f"  • Microsoft articles: {microsoft_articles} ({microsoft_share:.1f}% market share)")
        print(f"  • AI/ML mentions: {ai_ml_mentions}, Zero Trust: {zero_trust_mentions}, Cloud: {cloud_security_mentions}")
        print(f"  • Growth indicators: {growth_keywords} ({growth_sentiment:.1f}% sentiment)")
        print(f"  • Vendor mentions: Microsoft {microsoft_articles}, Proofpoint {proofpoint_articles}, Mimecast {mimecast_articles}")
        print(f"  • Technology trends: {len(tech_trends)} categories")
        print(f"  • Market presence: {len(market_presence)} vendors")
        
        print(f"\n✅ Test report saved as: {filename}")
        print("🎉 All sections should now contain real backend data!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_test_report()
