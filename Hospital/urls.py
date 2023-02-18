from django.urls import path
from .views import *

urlpatterns = [
    path('add-appointment/', ReceptionCreateAppointments.as_view()),
    path('all-appointments/', ReceptionAppointmentsList.as_view()),
    path('appointment/<int:pk>', ReceptionAppointmentDetail.as_view()),
    path('end-appointment/<int:pk>', DoctorEndAppointment.as_view()),
]
