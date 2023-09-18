from django.urls import path
from .views import PlanViewSet

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

]
