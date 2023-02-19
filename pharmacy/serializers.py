from rest_framework import serializers

from pharmacy.models import Prescription, Medicine
from accounts.serializers import PatientMiniSerializer, DoctorMiniSerializer


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        read_only_fields = ('is_active',)
        fields = ('id', 'title', 'is_active')


class PrescriptionSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(many=True)
    patient = PatientMiniSerializer(read_only=True)
    doctor = DoctorMiniSerializer(read_only=True)

    class Meta:
        model = Prescription
        read_only_fields = ('is_active', 'status')
        fields = ('id', 'doctor', 'patient', 'medicine', 'is_active', 'status')
