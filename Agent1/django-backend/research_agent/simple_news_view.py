from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def get_real_cybersecurity_news(request):
    """Simple endpoint to test real cybersecurity news"""
    try:
        from .cybersecurity_news_service import CybersecurityNewsService
        
        print("=== FETCHING REAL CYBERSECURITY NEWS ===")
        news_service = CybersecurityNewsService()
        
        # Get real news directly without threading complexity
        cybersecurity_news = news_service.get_mdo_specific_news(max_articles=5)
        
        # Format for frontend
        formatted_reports = []
        for i, article in enumerate(cybersecurity_news):
            formatted_reports.append({
                'id': f'news_{i+1}',
                'title': article['title'],
                'agent_name': article['source'],
                'agent_type': article['category'],
                'created_at': article['published_date'],
                'summary': article['summary'],
                'url': article['url'],
                'priority': article['priority'],
                'category': article['category'],
                'relevance_score': article['relevance_score']
            })
        
        print(f"✅ SUCCESS: Returning {len(formatted_reports)} real news articles")
        for report in formatted_reports:
            print(f"  - {report['title'][:60]}...")
        
        return JsonResponse({
            'success': True,
            'count': len(formatted_reports),
            'cybersecurity_reports': formatted_reports,
            'last_updated': datetime.now().isoformat(),
            'data_source': 'Real-time RSS feeds'
        })
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'success': False,
            'error': str(e),
            'cybersecurity_reports': [],
            'last_updated': datetime.now().isoformat(),
            'data_source': 'Error - fallback needed'
        }, status=500)
