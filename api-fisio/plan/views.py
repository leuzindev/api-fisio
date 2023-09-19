from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics

from .models import Plan
from .serializers import PlanSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientPlanView(generics.ListCreateAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        patient_username = self.kwargs['patient_username']
        return Plan.objects.filter(patient__user__username=patient_username)

    def perform_create(self, serializer):
        patient_username = self.kwargs['patient_username']
        patient = Patient.objects.get(user__username=patient_username)
        serializer.save(patient=patient)


class PatientPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        patient_username = self.kwargs['patient_username']
        return Plan.objects.filter(patient__user__username=patient_username)
