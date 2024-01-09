# apis/serializers.py
from rest_framework import serializers
from flashcard_app import models
from django.contrib.auth.models import User


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'file',
            'user',
            'public'
        )
        model = models.Dictionary
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
    
    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        )
        model = User