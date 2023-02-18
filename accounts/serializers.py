from rest_framework import serializers

from accounts.models import Doctor, Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        read_only_fields = ('role', 'status'),
        fields = ['id', 'username', 'email', 'password', 'role', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class DoctorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'username']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        read_only_fields = ('role', 'is_active'),
        fields = ['id', 'username', 'email', 'password', 'role', 'status']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PatientMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'username']
