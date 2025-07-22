from rest_framework import serializers
from .models import Agent, Report, ReportSubscription


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'title', 'content', 'agent', 'created_at', 'updated_at']


class ReportSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSubscription
        fields = ['id', 'email', 'frequency', 'is_active', 'created_at', 'updated_at']
