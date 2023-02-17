from rest_framework import serializers

from Hospital.models import Appointment
from accounts.serializers import DoctorSerializer, PatientSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    doc = DoctorSerializer(many=True)
    pat = PatientSerializer(many=True)

    class Meta:
        model = Appointment
        fields = ['id', 'pat', 'doc', 'status']
