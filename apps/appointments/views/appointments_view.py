from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.appointments.serializers.appointments_serializer import AppointmentSerializer
from apps.appointments.services.appointments_service import AppointmentService
from rest_framework.permissions import IsAuthenticated

class AppointmentListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    service = AppointmentService()

    def get(self, request):
        appointments = self.service.list_appointments()
        serializer = self.serializer_class(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                appointment = self.service.create_appointment(serializer.validated_data)
                return Response(self.serializer_class(appointment).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    service = AppointmentService()

    def get(self, request, appointment_id):
        try:
            appointment = self.service.get_appointment(appointment_id)
            serializer = self.serializer_class(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, appointment_id):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                appointment = self.service.update_appointment(appointment_id, serializer.validated_data)
                return Response(self.serializer_class(appointment).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, appointment_id):
        try:
            self.service.delete_appointment(appointment_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentByProfessionalView(APIView):
    serializer_class = AppointmentSerializer
    service = AppointmentService()

    def get(self, request, professional_id):
        appointments = self.service.get_appointments_by_professional(professional_id)
        serializer = self.serializer_class(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
