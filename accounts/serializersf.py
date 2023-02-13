from rest_framework import serializers

from accounts.models import Doctor, Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        read_only_fields = ('role', 'status'),
        fields = ['id', 'username', 'email', 'password', 'role', 'status']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        read_only_fields = ('role', 'is_active'),
        fields = ['id', 'username', 'email', 'password', 'role', 'status']
        extra_kwargs = {
            'password': {'write_only': True}
        }
