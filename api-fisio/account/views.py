from django.shortcuts import render

from rest_framework import viewsets
from account.serializers import UserSerializer
from account.models import User
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
