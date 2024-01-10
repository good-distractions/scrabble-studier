from rest_framework import serializers
from flashcard_app import models
from django.contrib.auth.models import User

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'title',
            'description',
            'file',
            'user',
            'public',
            'filter_all'
        ]
        model = models.Dictionary
        
        
class UserSerializer(serializers.ModelSerializer):
    dictionaries = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Dictionary.objects.all())
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password', 
            'dictionaries'
        ]
        