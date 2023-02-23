from rest_framework import serializers

from Hospital.models import Appointment, AppointmentTime, TimesForTheDay
from accounts.serializers import DoctorMiniSerializer, PatientMiniSerializer


class AppointmentTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentTime
        read_only_fields = ('is_active',)
        fields = ('id', 'time', 'is_active')


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorMiniSerializer(read_only=True)
    patient = PatientMiniSerializer(read_only=True)
    appointment_time = AppointmentTimeSerializer(read_only=True)

    class Meta:
        model = Appointment
        read_only_fields = (
                               'status', 'patient', 'doctor'
                           ),
        fields = ('id', 'patient', 'doctor', 'day', 'appointment_time', 'status')


class AppointmentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'status')


class TimesForTheDaySerializer(serializers.ModelSerializer):
    doctor = DoctorMiniSerializer(read_only=True)
    times = AppointmentTimeSerializer(read_only=True)

    class Meta:
        model = TimesForTheDay
        fields = ('id', 'times', 'day', 'doctor')
