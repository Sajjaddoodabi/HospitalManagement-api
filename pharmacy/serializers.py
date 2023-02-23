from rest_framework import serializers

from pharmacy.models import Prescription, Medicine
from accounts.serializers import PatientMiniSerializer, DoctorMiniSerializer


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        read_only_fields = ('is_active',)
        fields = ('id', 'prescription', 'title', 'is_active')


class MedicineMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        read_only_fields = ('is_active',)
        fields = ('id', 'title', 'is_active')


class MedicineCountSerializer(serializers.ModelSerializer):
    medicine_count = serializers.CharField(required=True)

    class Meta:
        model = Medicine
        fields = ('medicine_count',)


class PrescriptionSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(many=True)
    patient = PatientMiniSerializer(read_only=True)
    doctor = DoctorMiniSerializer(read_only=True)

    class Meta:
        model = Prescription
        read_only_fields = ('is_active', 'status')
        fields = ('id', 'doctor', 'patient', 'medicine', 'is_active', 'status')


class PrescriptionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ('id', 'status')
