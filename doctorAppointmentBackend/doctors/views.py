from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from doctors.models import DoctorProfile, Message
from patient.models import Appointment
from doctors.serializers import (
    DoctorCustomRegistrationSerializer,
    DoctorSerializer,
    AppointPatientSerializer,
    MessageSerializer,
)
from doctors.serializers import AppointmentSerializer


# Agent Registration
class DoctorRegistrationView(RegisterView):
    serializer_class = DoctorCustomRegistrationSerializer


class DoctorListAPI(APIView):
    serializer_class = DoctorSerializer

    def get(self, request, format=None, *args, **kwargs):
        instance = DoctorProfile.objects.all()
        serialized_data = self.serializer_class(instance, many=True)
        return Response(serialized_data.data)


class DoctorProfileAPI(APIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        instance = DoctorProfile.objects.get(doctor=request.user)
        serialized_data = self.serializer_class(instance)
        return Response(serialized_data.data)

    def put(self, request, format=None, *args, **kwargs):
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid(raise_exception=True):
            DoctorProfile.objects.filter(doctor=request.user).update(
                **serialized_data.data
            )

        return Response({"status": "successfully updated"})


class DoctorAppointmentsAPI(APIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        instance = Appointment.objects.filter(doctor=request.user.doctor)
        serialized_data = self.serializer_class(instance, many=True)
        return Response(serialized_data.data)

    def post(self, request, format=None, *args, **kwargs):
        serialized_data = AppointPatientSerializer(data=request.data)

        if serialized_data.is_valid(raise_exception=True):
            appointment = Appointment.objects.get(
                id=serialized_data.data.get("appointment_id")
            )
            appointment.appointment_time = serialized_data.data.get("time")
            appointment.appointment_status = serialized_data.data.get("status")
            appointment.save()

            print(serialized_data.data.get("time"), serialized_data.data.get("status"))

            message = f"Dear {appointment.patient.name},\n\n An appointment with {appointment.doctor.name} has been scheduled at {appointment.appointment_time}."

            send_mail(
                "Appointment update",
                message,
                "noreply.service.tanimsk@gmail.com",
                [appointment.patient.patient.email],
                fail_silently=False,
            )

        return Response({"status": "successful"})


class MessageAPI(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id=None, format=None, *args, **kwargs):
        if patient_id is None:
            return Response({"status": "patient ID missing"})

        instances = Message.objects.filter(
            patient=patient_id, doctor=request.user.doctor
        )
        return Response(self.serializer_class(instances, many=True).data)

    def post(self, request, patient_id=None, format=None, *args, **kwargs):
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid(raise_exception=True):
            Message.objects.create(
                doctor=request.user.doctor, patient=patient_id, **serialized_data.data
            )

        return Response({"status": "success"})
