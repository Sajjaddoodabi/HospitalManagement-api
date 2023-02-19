from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from Hospital.models import Appointment
from Hospital.serializers import AppointmentSerializer, AppointmentMiniSerializer
from accounts.models import Doctor, Patient, TimesForTheDay
from accounts.serializers import DoctorMiniSerializer, PatientMiniSerializer, PatientSerializer, DoctorSerializer
from accounts.views import get_user


class Hospital(APIView):
    pass


class Reception(APIView):
    pass


class ReceptionCreateAppointments(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            if user.role == 'PAT':
                appointment_time = request.data['appointment_time']
                day = request.data['day']
                doc = request.data['doctor']

                doctor = Doctor.objects.filter(parent_user__username=doc).first()
                patient = Patient.objects.filter(parent_user=user).first()
                isExist = TimesForTheDay.objects.filter(
                    day=day,
                    times=appointment_time).exists()

                if isExist:
                    response = {'massage': 'Doctor is busy in that time!'}
                    return Response(response)

                appointment = Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    appointment_time=appointment_time,
                    day=day
                )
                TimesForTheDay.objects.create(Doctor=doctor, times=appointment_time, day=day)
                appointment_ser = AppointmentSerializer(appointment)
                return Response(appointment_ser.data, status=status.HTTP_201_CREATED)
            else:
                response = {'massage': 'user should be patient to add appointment'}
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
