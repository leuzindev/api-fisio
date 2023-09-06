from rest_framework import serializers
from professional.models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["name", "email"]