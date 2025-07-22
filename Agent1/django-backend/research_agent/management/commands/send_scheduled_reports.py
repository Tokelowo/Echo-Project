from django.core.management.base import BaseCommand
from django.utils import timezone
from research_agent.models import ReportSubscription
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send scheduled email reports to subscribers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )
        parser.add_argument(
            '--timezone',
            type=str,
            help='Filter subscriptions by timezone',
        )

    def handle(self, *args, **options):
        """Process all due subscriptions and send reports"""
        dry_run = options['dry_run']
        target_timezone = options.get('timezone')
        
        # Find all subscriptions that are due for delivery
        now = timezone.now()
        due_subscriptions = ReportSubscription.objects.filter(
            is_active=True,
            next_run_date__lte=now
        )
        
        if target_timezone:
            due_subscriptions = due_subscriptions.filter(time_zone=target_timezone)
        
        if not due_subscriptions.exists():
            self.stdout.write(self.style.SUCCESS('No subscriptions due for delivery.'))
            return
        
        self.stdout.write(f'Found {due_subscriptions.count()} subscriptions due for delivery.')
        
        success_count = 0
        error_count = 0
        
        for subscription in due_subscriptions:
            try:
                if dry_run:
                    self.stdout.write(
                        f'DRY RUN: Would send {subscription.get_agent_type_display()} '
                        f'report to {subscription.user_email} '
                        f'(Next: {subscription.get_next_delivery_local_time()})'
                    )
                else:
                    # Send the actual report
                    result = self.send_subscription_report(subscription)
                    if result['success']:
                        success_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Sent {subscription.get_agent_type_display()} '
                                f'report to {subscription.user_email}'
                            )
                        )
                        # Update next run date
                        subscription.update_next_run_date()
                    else:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'✗ Failed to send report to {subscription.user_email}: '
                                f'{result.get("error", "Unknown error")}'
                            )
                        )
                        
            except Exception as e:
                error_count += 1
                logger.error(f'Error processing subscription {subscription.id}: {str(e)}')
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error processing subscription for {subscription.user_email}: {str(e)}'
                    )
                )
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Completed: {success_count} sent, {error_count} failed'
                )
            )

    def send_subscription_report(self, subscription):
        """Generate and send a report for a specific subscription"""
        try:
            from research_agent.views import full_agent_pipeline
            from django.http import HttpRequest
            from django.test import RequestFactory
            import json
            
            # Create a proper request using RequestFactory
            factory = RequestFactory()
            
            # Prepare the request data
            query_data = {
                'input': subscription.query_template or f'Generate a {subscription.get_agent_type_display()} report',
                'agent_type': subscription.agent_type,
                'user_email': subscription.user_email,
                'user_name': subscription.user_name,
                'focus_areas': subscription.focus_areas,
                'delivery': {
                    'email': True,
                    'format': subscription.delivery_format
                }
            }
            
            # Create a POST request with JSON data
            request = factory.post(
                '/research-agent/full-agent-pipeline/',
                data=json.dumps(query_data),
                content_type='application/json'
            )
            
            # Call the pipeline
            response = full_agent_pipeline(request)
            
            if response.status_code == 200:
                return {'success': True, 'data': response.data}
            else:
                return {'success': False, 'error': f'Pipeline error: {response.status_code}'}
                
        except Exception as e:
            logger.error(f'Error in send_subscription_report: {str(e)}')
            return {'success': False, 'error': str(e)}
