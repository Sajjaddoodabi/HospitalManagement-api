from rest_framework import serializers

from Hospital.models import Appointment
from accounts.serializers import DoctorMiniSerializer, PatientMiniSerializer, DoctorSerializer, PatientSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    doct = DoctorMiniSerializer(read_only=True)
    pati = PatientMiniSerializer(read_only=True)

    class Meta:
        model = Appointment
        read_only_fields = (
                               'status', 'doct', 'pati'
                           ),
        fields = ('id', 'pati', 'doct', 'day', 'appointment_time', 'status')


class AppointmentMiniSerializer(serializers.ModelSerializer):
    doctor = DoctorMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        read_only_fields = ('doctor',),
        fields = ('id', 'doctor', 'day', 'appointment_time')
