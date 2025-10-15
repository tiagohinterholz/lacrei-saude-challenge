import pytest
from apps.professionals.services.professionals_service import ProfessionalService


@pytest.mark.django_db
class TestProfessionalService:
    def test_create_professional(self, professional_base_dict):
        service = ProfessionalService()
        professional = service.create_professional(
            professional_base_dict,
            professional_base_dict["address"],
            professional_base_dict["contact"],
        )

        assert professional.social_name == "Dr. Ana Paula"
        assert professional.address.city == "Curitiba"
        assert professional.contact.email == "ana.paula@clinic.com"

    def test_list_professionals(self, professional_factory):
        professional_factory(count=3)
        service = ProfessionalService()
        result = service.list_professionals()
        assert len(result) == 3
