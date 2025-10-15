import pytest
from rest_framework import status
from apps.common.misc.request_mixin import AuthRequestMixin
from django.urls import reverse


@pytest.mark.django_db
class TestProfessionalView(AuthRequestMixin):
    base_uri = "/professionals/"

    def test_get_professional_list(self, api_client, professional_factory, superuser):
        professional_factory(count=2)
        url = reverse("professional-list")
        response = self.auth_get(client=api_client, admin=superuser, uri=url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_professional(self, api_client, professional_base_dict, superuser):
        url = reverse("professional-list")
        response = self.auth_post(
            client=api_client, admin=superuser, uri=url, body=professional_base_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["social_name"] == "Dr. Ana Paula"

    def test_patch_professional(self, api_client, professional_obj, superuser):
        url = reverse("professional-detail", args=[professional_obj.id])
        body = {"social_name": "Dr. Ana Souza"}
        response = self.auth_patch(
            client=api_client, obj=professional_obj, admin=superuser, body=body, uri=url
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["social_name"] == "Dr. Ana Souza"

    def test_delete_professional(self, api_client, professional_obj, superuser):
        url = reverse("professional-detail", args=[professional_obj.id])
        response = self.auth_delete(
            client=api_client, obj=professional_obj, admin=superuser, uri=url
        )

        assert response.status_code in [
            status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
