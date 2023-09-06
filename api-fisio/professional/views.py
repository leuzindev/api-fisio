
from rest_framework import viewsets
from professional.serializers import ProfessionalSerializer
from professional.models import Professional
from rest_framework.permissions import IsAuthenticated


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = (IsAuthenticated,)
