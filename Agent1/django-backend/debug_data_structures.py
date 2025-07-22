#!/usr/bin/env python
"""
Debug the exact data structure causing the '.get() on list' error
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')

try:
    django.setup()
except Exception as e:
    print(f"Django setup error: {e}")

from research_agent.cybersecurity_news_service_new import CybersecurityNewsService
from research_agent.formatting_agent import FormattingAgent
import json

def debug_data_structures():
    """Debug the exact data structures being passed to the formatting agent"""
    print("🔍 Debugging data structures for formatting agent...")
    
    try:
        # Initialize services
        news_service = CybersecurityNewsService()
        formatting_agent = FormattingAgent()
        
        # Get test data
        print("📰 Fetching cybersecurity news...")
        articles = news_service.fetch_cybersecurity_news(max_articles=10)
        print(f"✅ Found {len(articles)} articles")
        
        # Analyze data
        print("🔍 Analyzing all data types...")
        market_presence = news_service.analyze_market_presence(articles)
        competitive_landscape = news_service.analyze_competitive_landscape(articles)
        tech_trends = news_service.analyze_technology_trends(articles)
        threat_landscape = news_service.analyze_threat_landscape(articles)
        
        # Create comprehensive report data
        report_data = {
            'title': 'Debug Test Report',
            'executive_summary': f'Debug analysis of current cybersecurity landscape.',
            'articles_analyzed': len(articles),
            'articles': articles[:5],
            'market_presence': market_presence,
            'technology_trends': tech_trends,
            'threat_landscape': threat_landscape,
            'competitive_landscape': competitive_landscape,
            'generated_at': '2024-12-26T12:00:00Z',
            'agent_type': 'comprehensive_research'
        }
        
        print("\n📊 Deep data structure analysis:")
        
        def analyze_structure(data, name, depth=0):
            indent = "  " * depth
            print(f"{indent}{name}: {type(data)}")
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)) and depth < 3:
                        analyze_structure(value, f"{name}['{key}']", depth + 1)
                    elif isinstance(value, list) and value and depth < 3:
                        print(f"{indent}  {name}['{key}'] contains {len(value)} items")
                        if value:
                            analyze_structure(value[0], f"{name}['{key}'][0]", depth + 2)
                    else:
                        print(f"{indent}  {name}['{key}']: {type(value)} = {str(value)[:50]}...")
                        
            elif isinstance(data, list):
                print(f"{indent}  Length: {len(data)}")
                if data and depth < 3:
                    analyze_structure(data[0], f"{name}[0]", depth + 1)
        
        # Analyze each major section
        print("\n1. Market Presence Structure:")
        analyze_structure(market_presence, "market_presence")
        
        print("\n2. Competitive Landscape Structure:")
        analyze_structure(competitive_landscape, "competitive_landscape")
        
        print("\n3. Technology Trends Structure:")
        analyze_structure(tech_trends, "technology_trends")
        
        print("\n4. Threat Landscape Structure:")
        analyze_structure(threat_landscape, "threat_landscape")
        
        # Now try to create a docx and see exactly where it fails
        print("\n🧪 Testing DOCX generation...")
        try:
            docx_stream = formatting_agent.create_professional_docx_report(
                report_data, "Debug User"
            )
            print("✅ DOCX generation successful!")
            return True
            
        except Exception as e:
            print(f"❌ DOCX generation failed: {str(e)}")
            
            # Find the exact line causing the error
            import traceback
            print("\n🔍 Full traceback:")
            print(traceback.format_exc())
            
            # Try to identify the specific data causing issues
            error_msg = str(e)
            if "'list' object has no attribute 'get'" in error_msg:
                print("\n🎯 Found the '.get() on list' error!")
                print("🔍 This means somewhere in the data, we have a list where a dict is expected")
                
                # Look for lists in the data that might be problematic
                def find_problematic_lists(data, path=""):
                    issues = []
                    if isinstance(data, dict):
                        for key, value in data.items():
                            current_path = f"{path}.{key}" if path else key
                            if isinstance(value, list) and value:
                                # Check if list contains dicts (this might be the issue)
                                first_item = value[0]
                                if not isinstance(first_item, dict):
                                    issues.append(f"{current_path}: List of {type(first_item)} (expected dict?)")
                                else:
                                    issues.extend(find_problematic_lists(value, current_path))
                            elif isinstance(value, dict):
                                issues.extend(find_problematic_lists(value, current_path))
                    elif isinstance(data, list):
                        for i, item in enumerate(data[:3]):  # Check first 3 items
                            current_path = f"{path}[{i}]"
                            issues.extend(find_problematic_lists(item, current_path))
                    return issues
                
                print("\n🔍 Searching for problematic data structures:")
                issues = find_problematic_lists(report_data)
                if issues:
                    for issue in issues:
                        print(f"  ⚠️  {issue}")
                else:
                    print("  ✅ No obvious problematic structures found")
            
            return False
        
    except Exception as e:
        print(f"❌ Debug failed with exception: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("🔍 Data Structure Debug for '.get() on list' Error")
    print("=" * 60)
    
    success = debug_data_structures()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ DEBUG COMPLETE - No errors found")
    else:
        print("❌ DEBUG COMPLETE - Error identified")
