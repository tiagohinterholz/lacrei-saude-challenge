import pytest

from apps.professionals.models.professionals_model import Professional, ProfessionalAddress, ProfessionalContact


@pytest.fixture
def professional_base_dict():
    return {
        "social_name": "Dr. Ana Paula",
        "profession": "Cardiologist",
        "address": {
            "street": "Rua das Flores",
            "number": "12A",
            "district": "Centro",
            "city": "Curitiba",
            "state": "PR",
            "postal_code": "80000-000",
            "country": "Brazil",
        },
        "contact": {
            "email": "ana.paula@clinic.com",
            "phone": "+55 41 98888-7777"
        }
    }


@pytest.fixture
def professional_partial_dict():
    return {
        "social_name": "Dr. Ana P. Souza",
        "contact": {"phone": "+55 41 97777-8888"}
    }


@pytest.fixture
def professional_obj():
    professional = Professional.objects.create(
        social_name="Dr. Ana Paula",
        profession="Cardiologist",
    )

    ProfessionalAddress.objects.create(
        professional=professional,
        street="Rua das Flores",
        number="12A",
        city="Curitiba",
        state="PR",
        country="Brazil",
    )

    ProfessionalContact.objects.create(
        professional=professional,
        email="ana.paula@clinic.com",
        phone="+55 41 98888-7777",
    )

    return professional
