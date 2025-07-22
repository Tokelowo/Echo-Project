from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views_simple as views

# Register viewsets with DRF router
router = DefaultRouter()

urlpatterns = router.urls

# Add simple API endpoints
urlpatterns += [
    path('health/', views.health_check, name='health_check'),
    path('overview/', views.get_overview_data, name='get_overview_data'),
    path('market-trends/', views.market_trends_simple, name='market_trends'),
    path('customer-reviews/', views.customer_reviews_simple, name='customer_reviews'),
    path('competitive-metrics/', views.competitive_metrics_simple, name='competitive_metrics'),
    path('product-intelligence/', views.product_intelligence_simple, name='product_intelligence'),
    path('competitive-intelligence/', views.competitive_intelligence_simple, name='competitive_intelligence'),
    path('enhanced-market-intelligence/', views.enhanced_market_intelligence_simple, name='enhanced_market_intelligence'),
    path('real-market-trends-data/', views.real_market_trends_data_simple, name='real_market_trends_data'),
]