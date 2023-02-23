from django.urls import path
from .views import *

urlpatterns = [
    path('register/doctor/', DoctorRegisterView.as_view()),
    path('register/patient/', PatientRegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('user/change-password/', ChangePassword.as_view()),
    path('doctor-category/', DoctorCategories.as_view()),
    path('doctor-category/<int:pk>/', DoctorCategoryDetail.as_view()),
    path('doctor-category/add-category/', AddDoctorCategory.as_view()),
]
