import pytest
from apps.appointments.services.appointments_service import AppointmentService
from apps.appointments.models import AppointmentStatus
from datetime import timedelta


@pytest.mark.django_db
class TestAppointmentService:
    def setup_method(self):
        self.service = AppointmentService()

    def test_create_appointment(self, appointment_dict):
        appointment = self.service.create_appointment(appointment_dict)
        assert appointment.id is not None
        assert appointment.status == AppointmentStatus.SCHEDULED

    def test_create_appointment_conflict(self, appointment_obj):
        conflict_data = {
            "professional_id": appointment_obj.professional.id,
            "scheduled_at": appointment_obj.scheduled_at,
            "status": AppointmentStatus.SCHEDULED,
            "notes": "Tentativa de conflito",
        }
        with pytest.raises(ValueError, match="already has an appointment"):
            self.service.create_appointment(conflict_data)

    def test_list_appointments(self, appointment_obj):
        results = self.service.list_appointments()
        assert appointment_obj in results

    def test_get_appointment(self, appointment_obj):
        result = self.service.get_appointment(appointment_obj.id)
        assert result == appointment_obj

    def test_update_appointment(self, appointment_obj):
        data = {"status": AppointmentStatus.CANCELED}
        updated = self.service.update_appointment(appointment_obj.id, data)
        assert updated.status == AppointmentStatus.CANCELED

    def test_delete_appointment(self, appointment_obj):
        self.service.delete_appointment(appointment_obj.id)
        from apps.appointments.models import Appointment

        deleted = Appointment.objects.get(id=appointment_obj.id)
        assert deleted.is_active is False
