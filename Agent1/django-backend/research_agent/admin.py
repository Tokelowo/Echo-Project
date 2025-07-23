from django.contrib import admin
from .models import Agent, Report, ReportSubscription, ReportRequest, EmailDelivery

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Agent model.
    """
    list_display = ('id', 'name', 'agent_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('agent_type', 'is_active', 'created_at')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin configuration for Report model.
    """
    list_display = ('id', 'title', 'agent', 'confidence_score', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('agent', 'created_at')

@admin.register(ReportRequest)
class ReportRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for ReportRequest model.
    """
    list_display = ('id', 'user_email', 'agent', 'status', 'priority', 'created_at')
    search_fields = ('user_email', 'query')
    list_filter = ('status', 'priority', 'agent', 'created_at')

@admin.register(EmailDelivery)
class EmailDeliveryAdmin(admin.ModelAdmin):
    """
    Admin configuration for EmailDelivery model.
    """
    list_display = ('id', 'recipient_email', 'subject', 'status', 'sent_at')
    search_fields = ('recipient_email', 'subject')
    list_filter = ('status', 'sent_at')

@admin.register(ReportSubscription)
class ReportSubscriptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for ReportSubscription model.
    """
    list_display = ('id', 'user_email', 'agent_type', 'frequency', 'is_active', 'created_at')
    search_fields = ('user_email',)
    list_filter = ('agent_type', 'frequency', 'is_active', 'created_at')
