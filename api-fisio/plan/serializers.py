from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(source='created_by.username')

    class Meta:
        model = Plan
        fields = ['id', 'created_by', 'title', 'description']
