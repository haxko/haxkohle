from django.urls import path
from membershipfees import views
from .admin import MatchTransactions, ImportCamt

urlpatterns = [
    path('admin/match_transactions/', MatchTransactions.as_view()),
    path('admin/import_camt/', ImportCamt.as_view()),
    path('me/', views.user_status, name='membershipfees_me'),
    path('members/', views.members_status, name='membershipfees_members'),
    path('sections/', views.home, name='membershipfees_sections'),
]
