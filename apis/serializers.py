# apis/serializers.py
from rest_framework import serializers
from flashcard_app import models


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