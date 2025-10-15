import pytest
from datetime import datetime
from apps.appointments.models import AppointmentStatus


@pytest.mark.django_db
class TestAppointmentModel:
    def test_str_returns_correct_format(self, appointment_obj):
        expected = f"{appointment_obj.professional.social_name} - {appointment_obj.scheduled_at:%Y-%m-%d %H:%M}"
        assert str(appointment_obj) == expected

    def test_default_status_is_scheduled(self, appointment_obj):
        assert appointment_obj.status == AppointmentStatus.SCHEDULED

    def test_can_update_status(self, appointment_obj):
        appointment_obj.status = AppointmentStatus.COMPLETED
        appointment_obj.save()
        assert appointment_obj.status == AppointmentStatus.COMPLETED
