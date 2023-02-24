from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from Hospital.models import Appointment
from accounts.models import Doctor
from accounts.views import get_user
from pharmacy.models import Prescription, Medicine
from pharmacy.serializers import PrescriptionSerializer, MedicineSerializer, PrescriptionMiniSerializer, \
    MedicineMiniSerializer


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
                response = {'message': 'only doctor can add prescription'}
                return Response(response)
        return Response(serializer.errors)


class PrescriptionDetail(APIView):
    def get(self, request, pk):
        prescription = Prescription.objects.filter(pk=pk).first()
        if prescription is not None:
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data)

        response = {'message': 'prescription does not exist!'}
        return Response(response)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        prescription = Prescription.objects.filter(pk=pk).first()
        if prescription is not None:
            prescription.delete()
            response = {'message': f'prescription with id {prescription.id} deleted!'}
            return Response(response)

        response = {'message': 'prescription does not exist!'}
        return Response(response)


class PrescriptionList(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class AddMedicine(APIView):
    def post(self, request):
        serializer = MedicineMiniSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']
            medicine = Medicine.objects.create(title=title)
            medicine_ser = MedicineSerializer(medicine)

            return Response(medicine_ser.data)
        return Response(serializer.errors)


class AddMedicineToPrescription(APIView):
    def post(self, request):
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']

            user = get_user(request)
            doctor = Doctor.objects.filter(parent_user=user).first()

            appointment = Appointment.objects.filter(doctor=doctor, status='DO').first()
            prescription = Prescription.objects.filter(doctor__appointment=appointment).first()

            medicine = Medicine.objects.filter(title=title).first()
            if medicine is not None:
                medicine.prescription = prescription
                medicine_ser = MedicineSerializer(medicine)

                return Response(medicine_ser.data)

            # medicine = Medicine.objects.create(title=title, prescription_id=prescription.id, count=1)
            # medicine_ser = MedicineSerializer(medicine)
            #
            # return Response(medicine_ser.data)
            response = {'message': 'prescription does not exist!'}
            return Response(response)

        return Response(serializer.errors)


class RemoveMedicineFromPrescription(APIView):
    def delete(self, request, pk):
        medicine = Medicine.objects.filter(pk=pk).first()

        if medicine is not None:
            medicine.delete()

            response = {'message': f'medicine with id {medicine.id} deleted!'}
            return Response(response)

        response = {'message': 'Medicine does not exist!'}
        return Response(response)


class ChangeMedicineCount(APIView):
    def put(self, request, pk):
        medicine = Medicine.objects.filter(pk=pk).first()
        if medicine is not None:
            if medicine.prescription is not None:

                count_status = request.data['medicine_count']
                if count_status == 'reduce':
                    medicine.count -= 1

                    if medicine.count == 0:
                        medicine.delete()
                        response = {'message': f'medicine with id {medicine.id} deleted!'}
                        return Response(response)

                elif count_status == 'increase':
                    medicine.count += 1

                else:
                    response = {'message': 'status not allowed'}
                    return Response(response)

                medicine_ser = MedicineSerializer(medicine)
                return Response(medicine_ser.data)

            response = {'message': 'Medicine does not belong to any prescription!'}
            return Response(response)

        response = {'message': 'Medicine does not exist!'}
        return Response(response)


class MedicineDetail(APIView):
    def get(self, request, pk):
        medicine = Medicine.objects.filter(pk=pk).first()
        if medicine is not None:
            serializer = MedicineMiniSerializer(medicine)
            return Response(serializer.data)
        response = {'message': 'medicine does not exist!'}
        return Response(response)

    def put(self, request, pk):
        medicine = Medicine.objects.filter(pk=pk).first()
        if medicine is not None:
            title = request.data['title']
            is_Exist = Medicine.objects.filter(title=title).exists()

            if is_Exist:
                response = {'message': 'medicine with this name already exist!'}
                return Response(response)

            medicine.title = title
            serializer = MedicineSerializer(medicine)
            return Response(serializer.data)

        response = {'message': 'medicine does not exist!'}
        return Response(response)

    def delete(self, request, pk):
        medicine = Medicine.objects.filter(pk=pk).first()
        if medicine is not None:
            medicine.delete()
            response = {'message': f'medicine with id {medicine.id} deleted!'}
            return Response(response)
        response = {'message': 'medicine does not exist!'}
        return Response(response)


class MedicineList(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineMiniSerializer


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

            response = {'message': 'prescription does not exist!'}
            return Response(response)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
