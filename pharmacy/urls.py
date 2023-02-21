from django.urls import path
from .views import *

urlpatterns = [
    path('add-prescription/', AddPrescription.as_view()),
    path('add-prescription/add-medicine/', AddMedicine.as_view()),
    path('prescription/', PrescriptionList.as_view()),
    path('prescription/<int:pk>', PrescriptionDetail.as_view()),
    path('prescription/change-status/<int:pk>', UpdatePrescriptionStatus.as_view()),
    path('medicin/', MedicineList.as_view()),
    path('medicin/<int:pk>', MedicineDetail.as_view()),
]
