from typing import Dict, Any

from rest_framework import serializers
from .models import User, Physiotherapist


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        username = data.pop('username')
        data: dict[str, Any | None] = {'id': data['id'], 'username': username, **data}

        return data
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups']


class ProfessionalSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Physiotherapist
        fields = ['user']

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
        }
