from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from rest_framework.fields import NullBooleanField
from snippets.models import User
from snippets.serializers import UserSerializer
from rest_framework import generics, serializers
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework_api_key.crypto import KeyGenerator
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class UserVerification(generics.ListCreateAPIView):
 
    serializer_class = UserSerializer
    
    def get_queryset(self):
        id = self.request.POST.get('id')
        token = self.request.POST.get('token')
        
        queryset = User.objects.filter(id = id).filter(token = token)
        
        #if we have a user that match the id and the token then it returns all the data from the user
        #Otherwise it returns an empty JSON
        return queryset

keyGenerator = KeyGenerator(prefix_length=2, secret_key_length=32)

@api_view(['GET','POST'])
def all_users_api_view(request,pk=None):

    if request.method == 'GET':
        user = User.objects.all()
        user_serializer = UserSerializer(user, many = True)
        return Response(user_serializer.data, status = status.HTTP_200_OK)

    if request.method == 'POST':
        user = request.data
        user_serializer = UserSerializer(data = user)
        if user_serializer.is_valid():
            user_serializer.save(token=keyGenerator.get_secret_key())
            return Response((user_serializer.data.get('id'),user_serializer.data.get('token') ), status = status.HTTP_201_CREATED)
        return Response(user_serializer.errors)

@api_view(['POST'])
def user_login(request, pk=None):
    user = request.data
    user_serializer = UserSerializer(data = user)

    #login with email and password
    if user_serializer.is_valid():
        if (user_serializer.data.get('email') == None or user_serializer.data.get('password') == None):
            return Response({'message':'Please check your credentials and try again'},status = status.HTTP_400_BAD_REQUEST)
        else:
            if(User.objects.filter(email = user['email']).filter(password = user['password']).exists()):
                user = User.objects.filter(email = user['email']).first()
                user_serializer = UserSerializer(user)
                return Response((user_serializer.data.get('id'),user_serializer.data.get('token')), status = status.HTTP_200_OK)

    #login with id and token
    if not user_serializer.is_valid():
        if (request.POST.get('id') == None or request.POST.get('token') == None):
            return Response({'message':'Please check your credentials and try again'},status = status.HTTP_400_BAD_REQUEST)
            
        else:
            if(User.objects.filter(id = user['id']).filter(token = user['token']).exists()):
                user = User.objects.filter(id = user['id']).first()
                user_serializer = UserSerializer(user)
                return Response((user_serializer.data.get('id'),user_serializer.data.get('token')), status = status.HTTP_200_OK)
            

    return Response({'message':'Please check your credentials and try again'},status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def user_detail_api_view(request, pk=None):

    if request.method == 'GET':
        user = User.objects.filter(id = pk).first()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status = status.HTTP_201_CREATED)


    if request.method == 'PUT':
        user_serializer = UserSerializer(data = request.data)

        if user_serializer.is_valid():
            if (user_serializer.data.get('email') == None or user_serializer.data.get('password') == None):
                if (user_serializer.data.get('num') == None or user_serializer.data.get('token') == None):
                    return Response({'message':'Please check your credentials and try again'},status = status.HTTP_400_BAD_REQUEST)
                else:
                    if(User.objects.filter(id = user_serializer.data.get('num')).filter(token = User.objects.get('token')).exists()):
                        user_serializer.save(password = user_serializer.data.get('password'),token=keyGenerator.get_secret_key())

                        return Response(user_serializer.data)
            #else: 
               # if(User.objects.filter(email = user['email']).filter(password = user['password']).exists()):
                 #   if(User.objects.filter(email =request.data['email'] ).filter(password= request.data['password']).exists()):
                   #     user_serializer.save(password = request.data['passwordNew'],token=keyGenerator.get_secret_key())
                    #    return Response(user_serializer.data)           
        return Response(user_serializer.errors)