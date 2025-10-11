from django.db import transaction
from apps.common.repositories.common_repository import CommonRepository
from apps.professionals.models import Professional, ProfessionalAddress, ProfessionalContact


class ProfessionalService:

    def __init__(self):
        self.professional_repo = CommonRepository(Professional)
        self.address_repo = CommonRepository(ProfessionalAddress)
        self.contact_repo = CommonRepository(ProfessionalContact)

    @transaction.atomic
    def create_professional(self, professional_data, address_data, contact_data):
        professional = self.professional_repo.create(**professional_data)
        self.address_repo.create(professional=professional, **address_data)
        self.contact_repo.create(professional=professional, **contact_data)
        return professional

    def list_professionals(self):
        return self.professional_repo.get_all()

    def get_professional(self, professional_id):
        return self.professional_repo.get_by_id(professional_id)

    @transaction.atomic
    def update_professional(self, professional_id, professional_data=None, address_data=None, contact_data=None):
        professional = self.professional_repo.update(professional_id, **(professional_data or {}))

        if address_data:
            self.address_repo.update(professional.address.id, **address_data)

        if contact_data:
            self.contact_repo.update(professional.contact.id, **contact_data)

        return professional

    def delete_professional(self, professional_id):
        return self.professional_repo.delete(professional_id)