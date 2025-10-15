import pytest
from apps.appointments.serializers.appointments_serializer import AppointmentSerializer
from apps.appointments.models import AppointmentStatus


@pytest.mark.django_db
class TestAppointmentSerializer:

    def test_appointment_serializer_output(self, appointment_obj):
        serializer = AppointmentSerializer(appointment_obj)
        data = serializer.data

        assert data["professional"]["id"] == str(appointment_obj.professional.id)
        assert data["professional"]["social_name"] == appointment_obj.professional.social_name
        assert data["status"] == AppointmentStatus.SCHEDULED
        assert "scheduled_at" in data
        assert "notes" in data

    def test_appointment_serializer_validation(self, appointment_dict):
        serializer = AppointmentSerializer(data=appointment_dict)
        assert serializer.is_valid(), serializer.errors

        validated = serializer.validated_data
        assert validated["professional"].id == appointment_dict["professional_id"]
        assert validated["status"] == appointment_dict.get("status", AppointmentStatus.SCHEDULED)
        assert "scheduled_at" in validated

    def test_partial_update_serializer(self, appointment_obj, appointment_partial_dict):
        serializer = AppointmentSerializer(
            appointment_obj, data=appointment_partial_dict, partial=True
        )
        assert serializer.is_valid(), serializer.errors
        updated = serializer.save()
        assert updated.status == appointment_partial_dict["status"]
