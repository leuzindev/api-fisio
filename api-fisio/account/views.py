from .serializers import UserSerializer, ProfessionalSerializer
from .models import User, Physiotherapist
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserMeRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(),
            pk=self.request.user.pk
        )
        self.check_object_permissions(self.request, obj)
        return obj


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Physiotherapist.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = (IsAuthenticated,)
