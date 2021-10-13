from django import urls
from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.urls import path, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Jaseci API",
        default_version='v1',
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

#    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here

urlpatterns = [
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  #<-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  #<-- Here
    path('users/', views.all_users_api_view, name = 'Users'),
    path('users/<int:pk>/', views.user_detail_api_view, name = 'Concrete user'),
    path('verify-user/', views.UserVerification.as_view()),
    path('change_pass/<int:pk>/', views.user_detail_api_view, name = 'Update password'),
    path('login/', views.user_login), 
]

urlpatterns = format_suffix_patterns(urlpatterns)