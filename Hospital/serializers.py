from rest_framework import serializers

from Hospital.models import Appointment
from accounts.serializers import DoctorMiniSerializer, PatientMiniSerializer, DoctorSerializer, PatientSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    # doctor = DoctorSerializer(many=False, read_only=True)
    # patient = PatientSerializer(many=False, read_only=True)

    class Meta:
        model = Appointment
        read_only_fields = (
                               'status',
                           ),
        fields = ['id', 'patient', 'doctor', 'day', 'appointment_time', 'status']


class AppointmentMiniSerializer(serializers.ModelSerializer):
    doctor = DoctorMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        read_only_fields = ('doctor',),
        fields = ['id', 'doctor', 'day', 'appointment_time']
