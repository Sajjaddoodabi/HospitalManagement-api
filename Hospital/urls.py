from django.urls import path
from .views import *

urlpatterns = [
    path('appointment/add-appointment/', ReceptionCreateAppointments.as_view()),
    path('appointment/', ReceptionAppointmentsList.as_view()),
    path('appointment/<int:pk>', ReceptionAppointmentDetail.as_view()),
    path('appointment/change-status/<int:pk>', UpdateAppointmentStatus.as_view()),
]
