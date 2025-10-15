from datetime import timezone
from apps.appointments.models.appointments_model import Appointment
from apps.common.repositories.common_repository import CommonRepository


class AppointmentsRepository(CommonRepository):
    def __init__(self):
        super().__init__(Appointment)

    def get_by_professional(self, professional_id):
        return self.model.objects.filter(professional_id=professional_id, is_active=True)

    def get_future_appointments(self):
        return self.model.objects.filter(scheduled_at__gte=timezone.now(), is_active=True)

    def exists_at_same_time(self, professional_id, scheduled_at):
        return self.model.objects.filter(
            professional_id=professional_id,
            scheduled_at=scheduled_at,
            is_active=True
        ).exists()
