from django.urls import path

from .views import UserViewSet, UserMeRetrieveAPIView, PhysiotherapistSerializerViewSet, PatientSerializerViewSet

urlpatterns = [
    path('accounts/me', UserMeRetrieveAPIView.as_view()),
    path('accounts', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('accounts/<int:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),

    path('accounts/professionals', PhysiotherapistSerializerViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('accounts/patients', PatientSerializerViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),


]

