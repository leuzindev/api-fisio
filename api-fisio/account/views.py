from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Physiotherapist, Patient
from .serializers import UserSerializer, PhysiotherapistSerializer, PatientSerializer


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


class PhysiotherapistViewSet(viewsets.ModelViewSet):
    queryset = Physiotherapist.objects.all()
    serializer_class = PhysiotherapistSerializer
    permission_classes = (IsAuthenticated,)


class PatientViewSet(viewsets.ModelViewSet):
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

            if physiotherapist.subscription_type == Physiotherapist.FREE and physiotherapist.patients.count() >= 5:
                return Response({'message': 'Cannot add more patients. Free subscription allows up to 5 patients.'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif physiotherapist.subscription_type == Physiotherapist.BRONZE and physiotherapist.patients.count() >= 20:
                return Response({'message': 'Cannot add more patients. Bronze subscription allows up to 20 patients.'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif physiotherapist.subscription_type == Physiotherapist.SILVER and physiotherapist.patients.count() >= 40:
                return Response({'message': 'Cannot add more patients. Silver subscription allows up to 40 patients.'},
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


class UpdatePhysiotherapistSubscriptionView(generics.UpdateAPIView):
    queryset = Physiotherapist.objects.all()
    serializer_class = PhysiotherapistSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        physiotherapist_id = self.kwargs.get('pk')
        return Physiotherapist.objects.get(pk=physiotherapist_id)
