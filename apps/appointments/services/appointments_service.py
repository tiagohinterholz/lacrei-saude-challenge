from django.db import transaction
from apps.appointments.repositories.appointments_repository import AppointmentsRepository


class AppointmentService:

    def __init__(self):
        self.appointment_repo = AppointmentsRepository()

    @transaction.atomic
    def create_appointment(self, data):
        professional_id = data.get("professional_id")
        scheduled_at = data.get("scheduled_at")

        if self.appointment_repo.exists_at_same_time(professional_id, scheduled_at):
            raise ValueError("This professional already has an appointment at this time.")

        return self.appointment_repo.create(**data)

    def list_appointments(self):
        return self.appointment_repo.get_all()

    def get_appointment(self, appointment_id):
        return self.appointment_repo.get_by_id(appointment_id)

    def get_appointments_by_professional(self, professional_id):
        return self.appointment_repo.get_by_professional(professional_id)

    def get_future_appointments(self):
        return self.appointment_repo.get_future_appointments()

    def update_appointment(self, appointment_id, data):
        professional_id = data.get("professional_id")
        scheduled_at = data.get("scheduled_at")

        if professional_id and scheduled_at:
            if self.appointment_repo.exists_at_same_time(professional_id, scheduled_at):
                raise ValueError("This professional already has an appointment at this time.")

        return self.appointment_repo.update(appointment_id, **data)

    def delete_appointment(self, appointment_id):
        return self.appointment_repo.delete(appointment_id)