from apis.models import Conversation, Person
from rest_framework import serializers

class personSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        depth = 3

class conversationSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
        depth = 3

        



