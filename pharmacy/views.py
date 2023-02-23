from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from Hospital.models import Appointment
from Hospital.serializers import AppointmentSerializer
from accounts.models import Doctor
from accounts.views import get_user
from pharmacy.models import Prescription, Medicine
from pharmacy.serializers import PrescriptionSerializer, MedicineSerializer, PrescriptionMiniSerializer


class Pharmacy(APIView):
    pass


class AddPrescription(APIView):
    def post(self, request):
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            if user.role == 'DOC':
                doctor = Doctor.objects.filter(parent_user=user).first()
                appointment = Appointment.objects.filter(doctor=doctor, status='DO').first()

                prescription = Prescription.objects.create(patient=appointment.patient, doctor=doctor)
                prescription_ser = PrescriptionSerializer(prescription)

                return Response(prescription_ser.data)
            else:
                response = {'massage': 'only doctor can add prescription'}
                return Response(response)
        return Response(serializer.errors)


class PrescriptionDetail(APIView):
    def get(self, request, pk):
        prescription = Prescription.objects.filter(pk=pk).first()
        if prescription is not None:
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data)

        response = {'massage': 'prescription does not exist!'}
        return Response(response)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        prescription = Prescription.objects.filter(pk=pk).first()
        if prescription is not None:
            prescription.delete()
            response = {'massage': f'prescription with id {prescription.id} deleted!'}
            return Response(response)

        response = {'massage': 'prescription does not exist!'}
        return Response(response)


class PrescriptionList(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class AddMedicine(APIView):

    def post(self, request):
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            pass


class MedicineDetail(APIView):
    def get(self, request, pk):
        medicine = Medicine.objects.filter(pk=pk).first()
        if medicine is not None:
            serializer = MedicineSerializer(medicine)
            return Response(serializer.data)
        response = {'massage': 'medicine does not exist!'}
        return Response(response)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        medicine = Medicine.objects.filter(pk=pk).first()
        if medicine is not None:
            medicine.delete()
            response = {'massage': f'medicine with id {medicine.id} deleted!'}
            return Response(response)
        response = {'massage': 'medicine does not exist!'}
        return Response(response)


class MedicineList(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class UpdatePrescriptionStatus(APIView):
    def put(self, request, pk):
        serializer = PrescriptionMiniSerializer(data=request.data)
        if serializer.is_valid():
            prescription_status = request.data['status']
            prescription = Prescription.objects.filter(pk=pk).first()
            if prescription is not None:
                prescription.status = prescription_status
                prescription.save()

                prescription_ser = PrescriptionSerializer(prescription)
                return Response(prescription_ser.data, status.HTTP_200_OK)

            response = {'massage': 'prescription does not exist!'}
            return Response(response)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
