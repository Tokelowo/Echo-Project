"""
Django Management Command for Product Intelligence Auto-Updates
Run with: python manage.py update_product_intelligence
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from research_agent.product_intelligence_updater import product_intelligence_updater
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update product intelligence data automatically'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force refresh even if data is not stale',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose logging',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting Product Intelligence Auto-Update...')
        )
        
        if options['verbose']:
            logger.setLevel(logging.DEBUG)
        
        try:
            if options['force']:
                self.stdout.write('🔄 Force refresh requested...')
                result = product_intelligence_updater.force_refresh()
            else:
                self.stdout.write('📊 Checking for stale data...')
                result = product_intelligence_updater.update_all_intelligence_data()
            
            if result['status'] == 'success':
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Product intelligence updated successfully!')
                )
                self.stdout.write(f'📅 Updated at: {result["updated_at"]}')
                self.stdout.write(f'🔄 Next update: {result["next_update"]}')
                self.stdout.write(f'📦 Components updated: {", ".join(result["components_updated"])}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Update failed: {result.get("error", "Unknown error")}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Command failed: {str(e)}')
            )
            logger.error(f"Product intelligence update command failed: {str(e)}")
        
        self.stdout.write(
            self.style.SUCCESS('🏁 Product Intelligence Auto-Update completed!')
        )
