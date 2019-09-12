from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('token/', views.token, name='login'),
    path('token/refresh/', views.refresh_token, name='refresh'),
    path('token/revoke/', views.revoke_token, name='revoke'),
]