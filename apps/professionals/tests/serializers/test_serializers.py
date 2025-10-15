import pytest
from apps.professionals.serializers.professionals_serializer import ProfessionalSerializer


@pytest.mark.django_db
class TestProfessionalSerializer:
    def test_professional_serializer_output(self, professional_obj):
        data = ProfessionalSerializer(instance=professional_obj).data

        assert data["id"] == str(professional_obj.id)
        assert data["social_name"] == professional_obj.social_name
        assert "address" in data
        assert "contact" in data

    def test_professional_serializer_validation(self, professional_base_dict):
        serializer = ProfessionalSerializer(data=professional_base_dict)
        assert serializer.is_valid(), serializer.errors
