from .serializers import UserSerializer, PhysiotherapistSerializer, PatientSerializer
from .models import User, Physiotherapist, Patient
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets, status
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


class PhysiotherapistSerializerViewSet(viewsets.ModelViewSet):
    queryset = Physiotherapist.objects.all()
    serializer_class = PhysiotherapistSerializer
    permission_classes = (IsAuthenticated,)


class PatientSerializerViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)


class PhysiotherapistPatientsListAPIView(generics.ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        physiotherapist_id = self.kwargs['pk']
        return Patient.objects.filter(physiotherapist__user_id=physiotherapist_id)


class AddPatientToPhysiotherapistAPIView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        physiotherapist_id = self.kwargs.get('physiotherapist_id')
        patient_id = self.kwargs.get('patient_id')


        try:
            physiotherapist = Physiotherapist.objects.get(user_id=physiotherapist_id)
            patient = Patient.objects.get(user_id=patient_id)

            if patient.physiotherapist:
                return Response({'message': 'Patient already has a physiotherapist.'},
                                status=status.HTTP_400_BAD_REQUEST)

            patient.physiotherapist = physiotherapist
            patient.save()

            return Response({'message': 'Patient added to physiotherapist successfully.'}, status=status.HTTP_200_OK)
        except Physiotherapist.DoesNotExist:
            return Response({'message': 'Physiotherapist not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({'message': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)


class RemovePatientFromPhysiotherapistAPIView(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        physiotherapist_id = self.kwargs.get('physiotherapist_id')
        patient_id = self.kwargs.get('patient_id')

        try:
            physiotherapist = Physiotherapist.objects.get(user_id=physiotherapist_id)
            patient = Patient.objects.get(user_id=patient_id)

            if patient.physiotherapist != physiotherapist:
                return Response(
                {'message': 'Patient is not associated with this physiotherapist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            patient.physiotherapist = None
            patient.save()

            return Response(
                {'message': 'Patient removed from physiotherapist successfully.'},
                status=status.HTTP_200_OK
            )
        except Physiotherapist.DoesNotExist:
            return Response({'message': 'Physiotherapist not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({'message': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
