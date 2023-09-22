from rest_framework import serializers

from .models import User, Physiotherapist, Patient


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        username = data.pop('username')
        data = {'id': data['id'], 'username': username, **data}

        return data

    class Meta:
        model = User
        exclude = ['user_permissions', 'groups']
        extra_kwargs = {'password': {'write_only': True}}


class PhysiotherapistSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Physiotherapist
        fields = ['user', 'subscription_type']

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'is_superuser': user.is_superuser,

        }


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['user']

    def get_user(self, obj):
        user = obj.user

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'is_superuser': user.is_superuser,
        }
