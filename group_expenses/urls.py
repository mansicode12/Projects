# # from django.urls import path, include
# # from rest_framework.routers import DefaultRouter
# # from . import views

# # # Create the router and register the viewsets
# # router = DefaultRouter()
# # router.register(r'groups', views.GroupViewSet)
# # #router.register(r'group-expenses', views.GroupExpenseViewSet)
# # router.register(r'expenses', views.GroupExpenseViewSet)  
# # router.register(r'group-members', views.GroupMemberViewSet)
# # router.register(r'settlements', views.SettlementViewSet)

# # # Define the URL patterns
# # urlpatterns = [
# #     # Include the router-generated URLs for the API endpointspath('api/', include(router.urls)),

# #     path('', include(router.urls)),  # ← NEW (remove 'api/' to avoid double api)
# #     # Frontend views
# #     path('group-expenses/', views.group_expenses_view, name='group_expenses'),
# #     path('add-expense/', views.add_expense, name='add_expense'),
# # ]
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# # Create the router and register the viewsets
# router = DefaultRouter()
# router.register(r'groups', views.GroupViewSet, basename='group')
# router.register(r'expenses', views.GroupExpenseViewSet, basename='expense')
# router.register(r'members', views.GroupMemberViewSet, basename='member')
# router.register(r'settlements', views.SettlementViewSet, basename='settlement')

# # Define the URL patterns
# urlpatterns = [
#     # API endpoints - THIS WILL NOW WORK

#     #path('api/', include(router.urls)),  # Add back 'api/' prefix
#     path('', include(router.urls)),  # Remove 'api/' prefix
#     # Frontend views
#     path('group-expenses/', views.group_expenses_view, name='group_expenses'),
#     path('add-expense/<int:group_id>/', views.add_expense, name='add_expense'),  # Added group_id parameter
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create the router and register the viewsets
router = DefaultRouter()
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'expenses', views.GroupExpenseViewSet, basename='expense')
router.register(r'members', views.GroupMemberViewSet, basename='member')
router.register(r'settlements', views.SettlementViewSet, basename='settlement')

# Define the URL patterns
urlpatterns = [
    # API endpoints - This will create URLs like /groups/, /expenses/, etc.
    path('', include(router.urls)),
    
    # Frontend views
    path('group-expenses/', views.group_expenses_view, name='group_expenses'),
    path('add-expense/<int:group_id>/', views.add_expense, name='add_expense'),
]