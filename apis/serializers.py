from rest_framework import serializers
from flashcard_app import models
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class DictionarySerializer(serializers.ModelSerializer):
  class Meta:
      fields = [
          'id',
          'title',
          'description',
          'file',
          'public',
          'words_q1',
          'words_q2',
          'words_q3',
          'words_q4',
          'preview',
          'user_username'
      ]
      model = models.Dictionary     
      
class DictionaryFullSerializer(serializers.ModelSerializer):
  class Meta:
      fields = [
          'id',
          'title',
          'description',
          'file',
          'public',
          'words_full',
          'preview',
          'user_username'
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

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  class Meta:
    model = User
    fields = ('username', 'password', 
         'email', 'first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }

  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user
  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name", "id")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )