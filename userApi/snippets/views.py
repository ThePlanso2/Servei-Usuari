from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from .permissions import Check_API_KEY_Auth


class SnippetList(generics.ListCreateAPIView):
    permission_classes = [HasAPIKey]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [HasAPIKey]

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #def perform_create(self, serializer):
        #serializer.save(token=Token.objects.create(user=self.request.user))


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExampleView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)