from django.db.models.query import QuerySet
from snippets.models import User
from snippets.serializers import UserSerializer
from rest_framework import generics
from django.conf import settings
from django.db.models.signals import post_save
from snippets.serializers import ChangePasswordSerializer
from rest_framework_api_key.crypto import KeyGenerator
from rest_framework.response import Response
from rest_framework.decorators import api_view

class UserList(generics.ListCreateAPIView):
    #GET return all the users
    #POST create a user
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

class UserLogin(generics.ListCreateAPIView):
 
    serializer_class = UserSerializer
    
    def get_queryset(self):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        
        queryset = User.objects.filter(email = email).filter(password = password)
        
        #if we have a user that match the email and the password then it returns all the data from the user
        #Otherwise it returns an empty JSON
        return queryset

@api_view(['PUT'])
def user_detail_api_view(request,pk=None):

    if request.method == 'PUT':
        user = User.objects.filter(id = pk).first()
        user_serializer = UserSerializer(user,data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)
    
    
  #  def get_queryset(self):
      #  id = self.request.POST.get('id')
      #  token = self.request.POST.get('token')
        
       # queryset = User.objects.filter(id = id).filter(token = token)
        
       # return queryset
        

   # def get_queryset(self):
     #   id = self.request.data.get('id')
        #queryset = User.objects.filter(id = id)
        #return queryset
        
    #def ChangePass(self):
        #new_pass = self.request.data.get('new_password')