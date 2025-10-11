from django.db import models
from apps.common.models import BaseModel
from apps.professionals.models import Professional


class AppointmentStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    CANCELED = "CANCELED", "Canceled"
    COMPLETED = "COMPLETED", "Completed"


class Appointment(BaseModel):
    professional = models.ForeignKey(
        Professional, on_delete=models.CASCADE, related_name="appointments"
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED,
    )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.professional.social_name} - {self.scheduled_at:%Y-%m-%d %H:%M}"
