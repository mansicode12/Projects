"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from . import api_views  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication Routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Group Expenses - points to group_expenses/urls.py
    path('api/group-expenses/', include('group_expenses.urls')),
    path('', include('frontend.urls')),
    
    # API endpoints for charts and transactions
    path('api/category-breakdown/', api_views.category_breakdown, name='category_breakdown'),
    path('api/monthly-trend/', api_views.monthly_trend, name='monthly_trend'),
    path('api/delete-transaction/<int:id>/', api_views.delete_transaction, name='delete_transaction'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)