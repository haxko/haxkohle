from django.urls import path
from membershipfees import views

urlpatterns = [
    path('me/', views.user_status, name='membershipfees_me'),
    path('members/', views.members_status, name='membershipfees_members'),
    path('sections/', views.home, name='membershipfees_sections'),
]
