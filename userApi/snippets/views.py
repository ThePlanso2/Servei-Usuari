from django.db.models.query import QuerySet
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

#from .permissions import Check_API_KEY_Auth


class SnippetList(generics.ListCreateAPIView):
    #permission_classes = [HasAPIKey]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    #def perform_create(self, serializer):
       # serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [HasAPIKey]
    #queryset = Snippet.objects.all()
    #serializer_class = SnippetSerializer
    print("class deprecated")

class UserList(generics.ListCreateAPIView):
    #GET return all the users
    #POST create a user
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(token=APIKey.objects.create_key(name="my-remote-service"))


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    #GET return all the users
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserVerification(generics.ListCreateAPIView):
    
    serializer_class = UserSerializer
    
    def get_queryset(self):
        # Agafem els parametres del body
        selects = ('password')
        email = self.request.POST.get('email')
        nickName = self.request.POST.get('nickName')
        #filtrem el queryset pels parametres seleccionats
        queryset = User.objects.filter(email = email).filter(nickName = nickName)
        #retornem la fila obtinguda, ens falta ser capaços de retornar un parametre concret
        return queryset
    
    
    

