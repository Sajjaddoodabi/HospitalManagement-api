from django.urls import path
from .views import *

urlpatterns = [
    path('prescription/', PrescriptionList.as_view()),
    path('prescription/<int:pk>', PrescriptionDetail.as_view()),
    path('prescription/add-prescription/', AddPrescription.as_view()),
    path('prescription/add-prescription/add-medicine/', AddMedicineToPrescription.as_view()),
    path('prescription/change-status/<int:pk>', UpdatePrescriptionStatus.as_view()),
    path('medicine/', MedicineList.as_view()),
    path('medicine/<int:pk>/', MedicineDetail.as_view()),
    path('medicine/remove/<int:pk>/', RemoveMedicineFromPrescription.as_view()),
    path('medicine/change-count/<int:pk>/', ChangeMedicineCount.as_view()),
]
