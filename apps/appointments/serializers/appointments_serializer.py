from rest_framework import serializers
from apps.appointments.models import Appointment
from apps.professionals.models import Professional


class ProfessionalNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["id", "social_name", "profession"]


class AppointmentSerializer(serializers.ModelSerializer):
    professional = ProfessionalNestedSerializer(read_only=True)
    professional_id = serializers.PrimaryKeyRelatedField(
        queryset=Professional.objects.filter(is_active=True),
        source="professional",
        write_only=True,
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "scheduled_at",
            "status",
            "notes",
            "professional",
            "professional_id",
            "created_at",
            "updated_at",
        ]