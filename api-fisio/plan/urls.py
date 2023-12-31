from django.urls import path
from .views import (
    PlanViewSet,
    PatientPlanView,
    PatientPlanDetailView,
    UploadVideoAPI,
    ExerciseViewSet,
    AddExerciseToPlanAPIView,
    RemoveExerciseFromPlanAPIView
)

urlpatterns = [
    path('plans', PlanViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('plans/<int:pk>', PlanViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('plans/<str:patient_username>/', PatientPlanView.as_view()),
    path('plans/<str:patient_username>/<int:pk>/', PatientPlanDetailView.as_view()),

    path('exercises', ExerciseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('exercises/<int:pk>/', ExerciseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('exercises/<int:exercise_id>/upload_video', UploadVideoAPI.as_view()),
    path('plans/<int:plan_id>/add_exercise/<int:exercise_id>/', AddExerciseToPlanAPIView.as_view()),
    path('plans/<int:plan_id>/remove_exercise/<int:exercise_id>/', RemoveExerciseFromPlanAPIView.as_view()),

]
