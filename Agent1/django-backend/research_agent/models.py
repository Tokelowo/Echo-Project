from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    AGENT_TYPE_CHOICES = [
        ('competitive_intelligence', 'Competitive Intelligence Agent'),
        ('product_intelligence', 'Product Intelligence Agent'),
        ('market_trends', 'Market Trends Agent'),
        ('formatting_agent', 'Formatting Agent'),
        ('delivery_agent', 'Delivery Agent'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    agent_type = models.CharField(
        max_length=32,
        choices=AGENT_TYPE_CHOICES,
        default='competitive_intelligence'
    )
    model_name = models.CharField(max_length=100, default='gpt-4o')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class ReportRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    DELIVERY_FORMAT_CHOICES = [
        ('email', 'Email Only'),
        ('pdf', 'PDF Attachment'),
        ('docx', 'Word Document'),
        ('both', 'Email + Attachment'),
    ]
    
    SCHEDULE_TYPE_CHOICES = [
        ('immediate', 'Immediate'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='report_requests')
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100, default='User')
    query = models.TextField(help_text='The research query or topic')
    focus_areas = models.JSONField(default=list, blank=True, help_text='Specific areas to focus on')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    delivery_format = models.CharField(max_length=20, choices=DELIVERY_FORMAT_CHOICES, default='email')
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPE_CHOICES, default='immediate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user_email} - {self.query[:50]}"


class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    request = models.ForeignKey(ReportRequest, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)
    source_url = models.URLField(blank=True, help_text='Source URL for the report content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class EmailDelivery(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]
    
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='email_deliveries')
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.recipient_email} - {self.subject}"


class ReportSubscription(models.Model):
    AGENT_TYPE_CHOICES = [
        ('competitive_intelligence_agent', 'Competitive Intelligence'),
        ('product_intelligence_agent', 'Product Intelligence'),
        ('market_trends_agent', 'Market Trends'),
        ('comprehensive_research', 'Comprehensive Multi-Agent Research'),
    ]
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    agent_type = models.CharField(max_length=50, choices=AGENT_TYPE_CHOICES, default='comprehensive_research')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    query_template = models.TextField(help_text='Template query for periodic reports')
    focus_areas = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    next_run_date = models.DateTimeField()
    last_run_date = models.DateTimeField(null=True, blank=True)
    delivery_format = models.CharField(max_length=20, default='email')
    time_zone = models.CharField(max_length=50, default='UTC')
    preferred_time = models.TimeField(default='09:00:00', help_text='Preferred delivery time')
    total_reports_sent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user_email', 'agent_type', 'frequency')
        indexes = [
            models.Index(fields=['next_run_date', 'is_active']),
            models.Index(fields=['user_email']),
        ]
    
    def __str__(self):
        return f"{self.user_email} - {self.agent_type} - {self.frequency}"
    
    def get_next_delivery_local_time(self):
        """Get the next delivery time formatted in local timezone"""
        if not self.next_run_date:
            return "Not scheduled"
        
        try:
            from django.utils import timezone
            from zoneinfo import ZoneInfo
            
            # Convert to specified timezone
            if self.time_zone and self.time_zone != 'UTC':
                try:
                    local_tz = ZoneInfo(self.time_zone)
                    local_time = self.next_run_date.replace(tzinfo=timezone.utc).astimezone(local_tz)
                    return local_time.strftime('%Y-%m-%d %H:%M %Z')
                except:
                    pass
            
            # Fallback to UTC
            return self.next_run_date.strftime('%Y-%m-%d %H:%M UTC')
        except:
            return str(self.next_run_date)
    
    def calculate_next_run_date(self):
        """Calculate the next run date based on frequency and preferred time"""
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        now = timezone.now()
        
        # Start with today's date at preferred time
        today = now.date()
        preferred_datetime = datetime.combine(today, self.preferred_time)
        next_run = timezone.make_aware(preferred_datetime)
        
        # If the time has already passed today, move to the next period
        if next_run <= now:
            if self.frequency == 'daily':
                next_run += timedelta(days=1)
            elif self.frequency == 'weekly':
                next_run += timedelta(weeks=1)
            elif self.frequency == 'monthly':
                # Add approximately 30 days for monthly
                next_run += timedelta(days=30)
        
        return next_run
    
    def update_next_run_date(self):
        """Update the next run date after sending a report"""
        from django.utils import timezone
        self.last_run_date = timezone.now()
        self.next_run_date = self.calculate_next_run_date()
        self.total_reports_sent += 1
        self.save()
