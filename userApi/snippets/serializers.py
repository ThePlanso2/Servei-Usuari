from django.db.models.fields import NullBooleanField, TextField
from rest_framework import serializers
from django import forms
from rest_framework.fields import EmailField, IntegerField
from rest_framework import serializers
from snippets.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email','password', 'nickName','token','num']
