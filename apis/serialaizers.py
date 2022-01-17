from apis.models import Person
from rest_framework import serializers

class personSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        depth = 3

        



