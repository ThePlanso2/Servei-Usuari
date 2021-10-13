from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.urls import path, include

urlpatterns = [
    path('users/', views.all_users_api_view, name = 'Users'),
    path('users/<int:pk>/', views.user_detail_api_view, name = 'Concrete user'),
    path('verify-user/', views.UserVerification.as_view()),
    path('change_pass/<int:pk>/', views.user_detail_api_view, name = 'Update password'),
    path('login/', views.user_login, name = 'Login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)