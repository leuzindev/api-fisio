from django.urls import path

from .views import UserViewSet, UserMeRetrieveAPIView, ProfessionalViewSet

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
    path('accounts/professionals', ProfessionalViewSet.as_view({
         'get': 'list',
         'post': 'create'
    })),
    # path('accounts/professionals/<int:pk>', ProfessionalRetrieveAPIView.as_view()),
]

