from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.Registration.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('', views.Login.as_view(), name='login'),
]
