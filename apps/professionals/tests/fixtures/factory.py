import pytest
from apps.professionals.models import Professional, ProfessionalAddress, ProfessionalContact


@pytest.fixture
def professional_factory(db):
    def create_professional(
        *,
        social_name="Dr. Alex Silva",
        profession="Psychologist",
        email="alex@clinic.com",
        phone="+55 11 99999-9999",
        city="São Paulo",
        state="SP",
        country="Brazil",
        count=1,
        **extra
    ):
        objs = []
        for _ in range(count):
            professional = Professional.objects.create(
                social_name=social_name,
                profession=profession,
                **extra,
            )
            ProfessionalAddress.objects.create(
                professional=professional,
                street="Av. Paulista",
                number="1000",
                city=city,
                state=state,
                country=country,
            )
            ProfessionalContact.objects.create(
                professional=professional,
                email=email,
                phone=phone,
            )
            objs.append(professional)
        return objs if count > 1 else objs[0]

    return create_professional
