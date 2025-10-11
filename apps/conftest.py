import pytest
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def superuser():
    return User.objects.create_superuser(
        email="root@example.com",
        password="Pass@123",
        username="Root"
    )


@pytest.fixture
@pytest.mark.django_db
def regular_user():
    return User.objects.create_user(
        email="user@example.com",
        password="Pass@123",
        username="User"
    )


@pytest.fixture
def superuser_client(api_client, superuser):
    return api_client


@pytest.fixture
def regular_client(api_client, regular_user):
    return api_client
