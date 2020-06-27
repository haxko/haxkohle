from django.urls import path
from membershipfees import views
from .admin import match_transactions, import_camt

urlpatterns = [
    path('admin/match_transactions/', match_transactions),
    path('admin/import_camt/', import_camt),
    path('me/', views.user_status, name='membershipfees_me'),
    path('members/', views.members_status, name='membershipfees_members'),
    path('sections/', views.home, name='membershipfees_sections'),
]
