from django.urls import path, include
from doctors.views import (
    DoctorRegistrationView,
    DoctorProfileAPI,
    DoctorListAPI,
    DoctorAppointmentsAPI,
    MessageAPI,
)

urlpatterns = [
    path("registration/", DoctorRegistrationView.as_view(), name="doctor_registration"),
    path("profile/", DoctorProfileAPI.as_view(), name="doctor_profile"),
    path("doctors-list/", DoctorListAPI.as_view(), name="doctor_list"),
    path("appointment/", DoctorAppointmentsAPI.as_view(), name="appointment"),
    path("message/<int:patient_id", MessageAPI.as_view(), name="message_doctor"),
]
