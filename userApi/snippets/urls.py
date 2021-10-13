from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.urls import path, include

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('verify-user/', views.UserVerification.as_view()),
    path('change_pass/<int:pk>/', views.user_detail_api_view, name = 'Cambio contraseña'),
    path('login/', views.UserLogin.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)