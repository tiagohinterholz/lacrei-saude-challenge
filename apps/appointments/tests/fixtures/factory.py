from datetime import datetime, timedelta
from apps.professionals.tests.fixtures.factory import create_professional
from apps.appointments.models import Appointment, AppointmentStatus


def create_appointment(professional=None, **kwargs):
    if not professional:
        professional = create_professional()

    defaults = {
        "professional": professional,
        "scheduled_at": datetime.now() + timedelta(days=1),
        "status": AppointmentStatus.SCHEDULED,
        "notes": "Consulta de rotina",
    }
    defaults.update(kwargs)
    return Appointment.objects.create(**defaults)
