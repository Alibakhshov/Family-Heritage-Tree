from django.urls import path
from . import views
urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('confirmation/', views.registration_confirmation, name='register_confirmation'),
    path('confirm_email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),

    path('reset/', views.password_reset_request, name='password_reset_request'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/complete/', views.password_reset_complete, name='password_reset_complete'),


    
]
