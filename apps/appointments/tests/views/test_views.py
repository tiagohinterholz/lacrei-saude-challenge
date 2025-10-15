import pytest
from rest_framework import status
from apps.common.misc.request_mixin import AuthRequestMixin
from django.urls import reverse


@pytest.mark.django_db
class TestAppointmentView(AuthRequestMixin):
    base_uri = "/appointments/"

    def test_get_appointment_list(self, api_client, appointment_obj, superuser):
        url = reverse("appointment-list")
        response = self.auth_get(client=api_client, admin=superuser, uri=url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_appointment(self, api_client, appointment_dict, superuser):
        url = reverse("appointment-list")
        response = self.auth_post(
            client=api_client, admin=superuser, uri=url, body=appointment_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "SCHEDULED"

    def test_patch_appointment(self, api_client, appointment_obj, superuser):
        url = reverse("appointment-detail", args=[appointment_obj.id])
        body = {"status": "CANCELED"}
        response = self.auth_patch(
            client=api_client, obj=appointment_obj, admin=superuser, body=body, uri=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "CANCELED"

    def test_delete_appointment(self, api_client, appointment_obj, superuser):
        url = reverse("appointment-detail", args=[appointment_obj.id])
        response = self.auth_delete(
            client=api_client, obj=appointment_obj, admin=superuser, uri=url)

        assert response.status_code in [
            status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

        from apps.appointments.models import Appointment
        deleted = Appointment.objects.get(id=appointment_obj.id)
        assert deleted.is_active is False

    def test_create_appointment_invalid(self, api_client, superuser):
        url = reverse("appointment-list")
        invalid_data = {"notes": "Sem profissional"}
        response = self.auth_post(
            client=api_client, admin=superuser, uri=url, body=invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "professional_id" in response.data or "scheduled_at" in response.data

    def test_unauthorized_access(self, api_client):
        url = reverse("appointment-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
