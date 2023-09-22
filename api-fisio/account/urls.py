from django.urls import path

from .views import (
    UserViewSet,
    UserMeRetrieveAPIView,
    PhysiotherapistViewSet,
    PatientViewSet,
    PhysiotherapistPatientsListAPIView,
    AddPatientToPhysiotherapistAPIView,
    RemovePatientFromPhysiotherapistAPIView,
    UpdatePhysiotherapistSubscriptionView
)

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

    path('accounts/professionals', PhysiotherapistViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('accounts/patients', PatientViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('accounts/professional/<int:pk>/patients/',
         PhysiotherapistPatientsListAPIView.as_view()
         ),
    path('accounts/professional/<int:physiotherapist_id>/add_patient/<int:patient_id>/',
         AddPatientToPhysiotherapistAPIView.as_view()),
    path('accounts/professional/<int:physiotherapist_id>/remove_patient/<int:patient_id>/',
         RemovePatientFromPhysiotherapistAPIView.as_view()),
    path('professional/<int:pk>/subscription/', UpdatePhysiotherapistSubscriptionView.as_view()),

]
