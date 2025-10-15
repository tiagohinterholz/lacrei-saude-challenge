import pytest
from datetime import datetime, timedelta
from apps.appointments.models.appointments_model import AppointmentStatus
from apps.appointments.tests.fixtures.factory import create_appointment


@pytest.fixture
def appointment_dict(professional_obj):
    return {
        "professional_id": professional_obj.id,
        "scheduled_at": (datetime.now() + timedelta(days=2)).isoformat(),
        "status": AppointmentStatus.SCHEDULED,
        "notes": "Retorno de consulta",
    }


@pytest.fixture
def appointment_partial_dict():
    return {
        "status": "CANCELED",
        "notes": "Paciente desmarcou a consulta"
    }


@pytest.fixture
def appointment_obj(db, professional_obj):
    return create_appointment(professional=professional_obj)
