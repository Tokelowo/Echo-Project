"""
Django management command to refresh market intelligence data daily
Run this command via cron or task scheduler to ensure daily updates
"""

from django.core.management.base import BaseCommand
from django.core.cache import cache
from research_agent.views import get_cached_market_intelligence
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Refresh market intelligence data by clearing cache and fetching fresh data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force refresh even if cache is valid'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting daily market intelligence refresh...')
        )
        
        try:
            # Force refresh market intelligence data
            force_refresh = options.get('force', True)
            intelligence_data = get_cached_market_intelligence(force_refresh=force_refresh)
            
            total_articles = (
                len(intelligence_data.get('microsoft_news', [])) +
                sum(len(articles) for articles in intelligence_data.get('competitor_news', {}).values())
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Market intelligence refreshed successfully!\n'
                    f'   📰 Total articles: {total_articles}\n'
                    f'   📅 Last updated: {intelligence_data.get("last_updated", "Unknown")}\n'
                    f'   🔄 Cache refreshed: {"Yes" if force_refresh else "No"}'
                )
            )
            
        except Exception as e:
            logger.error(f"Daily refresh failed: {e}")
            self.stdout.write(
                self.style.ERROR(f'❌ Daily refresh failed: {e}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('Daily market intelligence refresh completed!')
        )
