from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from Hospital.models import Appointment
from Hospital.serializers import AppointmentSerializer, AppointmentMiniSerializer
from accounts.models import Doctor, Patient, TimesForTheDay
from accounts.serializers import DoctorMiniSerializer, PatientMiniSerializer, PatientSerializer, DoctorSerializer
from accounts.views import get_user


class Hospital(APIView):
    pass


class Reception(APIView):
    pass


class ReceptionCreateAppointments(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            if user.role == 'PAT':
                appointment_time = request.data['appointment_time']
                day = request.data['day']
                doc = request.data['doctor']

                doctor = Doctor.objects.filter(parent_user__username=doc).first()
                patient = Patient.objects.filter(parent_user=user).first()
                isExist = TimesForTheDay.objects.filter(
                    Doctor=doctor,
                    day=day,
                    times=appointment_time).exists()

                if isExist:
                    response = {'massage': 'Doctor is busy in that time!'}
                    return Response(response)

                appointment = Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    appointment_time=appointment_time,
                    day=day
                )
                TimesForTheDay.objects.create(Doctor=doctor, times=appointment_time, day=day)
                appointment_ser = AppointmentSerializer(appointment)
                return Response(appointment_ser.data, status=status.HTTP_201_CREATED)
            else:
                response = {'massage': 'user should be patient to add appointment'}
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceptionAppointmentDetail(APIView):
    def get(self, request, pk):
        appointment = Appointment.objects.filter(pk=pk).first()
        if not appointment:
            response = {'massage': 'Appointment Not Found!'}
            return Response(response)

        serializer = AppointmentSerializer(appointment)

        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        appointment = Appointment.objects.filter(pk=pk).first()
        if not appointment:
            response = {'massage': 'Appointment Not Found!'}
            return Response(response)
        response = {'massage': f'Appointment with id {appointment.id} deleted successfully!'}
        appointment.delete()

        return Response(response)


class ReceptionAppointmentsList(ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class UpdateAppointmentStatus(APIView):
    def put(self, request, pk):
        serializer = AppointmentMiniSerializer(data=request.data)
        if serializer.is_valid():
            appointment_status = request.data['status']
            appointment = Appointment.objects.filter(pk=pk).first()
            appointment.status = appointment_status
            if appointment_status == 'DON' or appointment_status == 'DEN':
                appointment.is_active = False
            appointment.save()

            appointment_ser = AppointmentSerializer(appointment)
            return Response(appointment_ser.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
