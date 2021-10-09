from snippets.models import Snippet
from snippets.models import User
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from rest_framework import generics
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from .permissions import Check_API_KEY_Auth
from rest_framework_api_key.crypto import KeyGenerator


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        keyGenerator = KeyGenerator(prefix_length=2, secret_key_length=32)
        serializer.save(token=keyGenerator.get_secret_key())


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserVerification(generics.ListCreateAPIView):
 
    serializer_class = UserSerializer
    
    def get_queryset(self):
        id = self.request.POST.get('id')
        token = self.request.POST.get('token')
        
        queryset = User.objects.filter(id = id).filter(token = token)
        
        #if we have a user that match the id and the token then it returns all the data from the user
        #Otherwise it returns an empty JSON
        return queryset

