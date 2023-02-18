from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from Hospital.models import Appointment
from Hospital.serializers import AppointmentSerializer, AppointmentMiniSerializer
from accounts.models import Doctor, Patient
from accounts.serializers import DoctorMiniSerializer, PatientMiniSerializer, PatientSerializer, DoctorSerializer
from accounts.views import get_user


class Hospital(APIView):
    pass


class Reception(APIView):
    pass


class ReceptionCreateAppointments(generics.CreateAPIView):
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        user = get_user(self.request)
        doctor = Doctor.objects.filter(username=self.request.data.get('doctor', False))
        Appointment.objects.create(doctor=doctor, patient=user)
    # def post(self, request):
    #     serializer = AppointmentMiniSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = get_user(request)
    #
    #         appointment_time = request.data['appointment_time']
    #         day = request.data['day']
    #         doc = request.data['doctor']
    #
    #         doctor1 = Doctor.objects.filter(username=doc).first()
    #         doctor = DoctorMiniSerializer(doctor1)
    #         patient = PatientMiniSerializer(user)
    #
    #         appointment = {
    #             'pati': patient.data,
    #             'doct': doctor.data,
    #             'day': day,
    #             'appointment_time': appointment_time,
    #             'status': False
    #         }
    #
    #         # return Response(appointment)
    #         appointment_serializer = AppointmentSerializer(data=appointment)
    #         if appointment_serializer.is_valid():
    #             appointment_serializer.save()
    #             return Response(appointment_serializer.data)
    #
    #         return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceptionAppointmentDetail(APIView):
    def get(self, request, pk):
        appointment = Appointment.objects.filter(pk=pk).first()
        if not appointment:
            response = {'massage': 'Appointment Not Found!'}
            return Response(response)

        serializer = AppointmentSerializer(appointment)

        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        appointment = Appointment.objects.filter(pk=pk).first()
        if not appointment:
            response = {'massage': 'Appointment Not Found!'}
            return Response(response)
        response = {'massage': f'Appointment with id {appointment.id} deleted successfully!'}
        appointment.delete()

        return Response(response)


class ReceptionAppointmentsList(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class DoctorEndAppointment(APIView):
    def post(self, request, pk):
        appointment = Appointment.objects.filter(pk=pk).first()
        if not appointment:
            response = {'massage': 'Appointment Not Found!'}
            return Response(response)
        appointment.status = False
        appointment.save()
        response = {'massage': 'Appointment deactivated!'}
        return Response(response)


class DoctorActiveAppointment(APIView):
    def post(self, request, pk):
        appointment = Appointment.objects.filter(pk=pk).first()
        if not appointment:
            response = {'massage': 'Appointment Not Found!'}
            return Response(response)
        appointment.status = True
        appointment.save()
        response = {'massage': 'Appointment deactivated!'}
        return Response(response)


class Doctors(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.filter(parent_user__status=True)
    serializer_class = DoctorSerializer


class Patients(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.filter(parent_user__status=True)
    serializer_class = PatientSerializer
