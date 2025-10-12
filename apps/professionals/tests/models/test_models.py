import pytest


@pytest.mark.django_db
class TestProfessionalModel:
     def test_str_returns_social_name(self, professional_obj):
        assert str(professional_obj) == "Dr. Ana Paula - Cardiologist"