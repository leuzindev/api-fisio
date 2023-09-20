from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .models import Plan, ExerciseVideo, Exercise
from .serializers import PlanSerializer, ExerciseVideoSerializer, ExerciseSerializer


class PlanListSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Plan
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at']


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return PlanListSerializer
        return PlanSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientPlanView(generics.ListCreateAPIView):
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        patient_username = self.kwargs['patient_username']
        return Plan.objects.filter(patient__user__username=patient_username)

    def perform_create(self, serializer):
        patient_username = self.kwargs['patient_username']
        patient = Patient.objects.get(user__username=patient_username)
        serializer.save(patient=patient)


class PatientPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        patient_username = self.kwargs['patient_username']
        return Plan.objects.filter(patient__user__username=patient_username)


class UploadVideoAPI(CreateAPIView):
    serializer_class = ExerciseVideoSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        exercise_id = kwargs.get('exercise_id')

        try:
            exercise = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            return Response(
                {'message': 'O exercício com o ID fornecido não foi encontrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ExerciseVideo.objects.filter(exercise_id=exercise_id).count() >= 3:
            return Response(
                {'message': 'Já existem três vídeos associados a este exercício.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        video_name = request.FILES['video_file'].name

        video = ExerciseVideo.objects.create(
            name=video_name,
            video_file=request.FILES['video_file'],
            exercise=exercise
        )

        serializer = ExerciseVideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

