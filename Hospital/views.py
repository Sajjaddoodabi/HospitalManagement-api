from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from Hospital.models import Appointment
from Hospital.serializers import AppointmentSerializer
from accounts.models import Doctor, Patient
from accounts.serializers import DoctorSerializer, PatientSerializer


class Hospital(APIView):
    pass


class Reception(APIView):
    pass


class ReceptionCreateAppointments(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceptionAppointmentDetail(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class ReceptionAppointmentsLst(APIView):
    def get(self, request):
        pass

class Doctors(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.filter(status=True)
    serializer_class = DoctorSerializer


class Patients(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.filter(status=True)
    serializer_class = PatientSerializer
