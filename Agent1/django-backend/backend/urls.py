from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('research_agent.urls')),
    path('research-agent/', include('research_agent.urls')),  # For prefixed requests
    path('', include('research_agent.urls')),  # For root-level requests
]