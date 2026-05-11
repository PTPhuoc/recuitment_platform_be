from rest_framework import serializers
from app.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'phone_number', 'role', 'status', 'date_created']


class RoleUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['candidate', 'employer'])


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
