from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views_simple
from . import views as main_views

# Register viewsets with DRF router
router = DefaultRouter()

urlpatterns = router.urls

# Add API endpoints - mixing real data views with simple fallbacks
urlpatterns += [
    path('health/', views_simple.health_check, name='health_check'),
    path('overview/', main_views.get_overview_data, name='get_overview_data'),
    path('market-trends/', views_simple.market_trends_simple, name='market_trends'),
    path('customer-reviews/', views_simple.customer_reviews_simple, name='customer_reviews'),
    path('competitive-metrics/', views_simple.competitive_metrics_simple, name='competitive_metrics'),
    path('product-intelligence/', views_simple.product_intelligence_simple, name='product_intelligence'),
    path('competitive-intelligence/', views_simple.competitive_intelligence_simple, name='competitive_intelligence'),
    path('enhanced-market-intelligence/', views_simple.enhanced_market_intelligence_simple, name='enhanced_market_intelligence'),
    path('real-market-trends-data/', views_simple.real_market_trends_data_simple, name='real_market_trends_data'),
    path('pipeline/', views_simple.pipeline_endpoint, name='pipeline'),
    path('reports/', views_simple.reports_simple, name='reports_simple'),
    
    # Email subscription management endpoints
    path('email-subscriptions/', main_views.email_subscriptions, name='email_subscriptions'),
    path('manage-subscriptions/', main_views.manage_subscriptions, name='manage_subscriptions'),
    path('subscription/<int:subscription_id>/update/', main_views.update_subscription, name='update_subscription'),
    path('subscription/<int:subscription_id>/unsubscribe/', main_views.unsubscribe, name='unsubscribe'),
    path('subscription/<int:subscription_id>/reactivate/', main_views.reactivate_subscription, name='reactivate_subscription'),
    path('unsubscribe-all/', main_views.unsubscribe_all, name='unsubscribe_all'),
]