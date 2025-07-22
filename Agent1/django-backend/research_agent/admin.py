from django.contrib import admin
from .models import Agent, Report, ReportSubscription

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Agent model.
    """
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin configuration for Report model.
    """
    list_display = ('id', 'title', 'agent', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('agent', 'created_at')

@admin.register(ReportSubscription)
class ReportSubscriptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for ReportSubscription model.
    """
    list_display = ('id', 'email', 'frequency', 'is_active', 'created_at')
    search_fields = ('email',)
    list_filter = ('frequency', 'is_active', 'created_at')
