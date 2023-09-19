from django.urls import path
from .views import PlanViewSet, PatientPlanView, PatientPlanDetailView

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

]
