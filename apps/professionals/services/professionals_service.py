from django.db import transaction

from apps.professionals.repositories.profesisonals_repository import ProfessionalAddressRepository, ProfessionalContactRepository, ProfessionalRepository


class ProfessionalService:

    def __init__(self):
        self.professional_repo = ProfessionalRepository()
        self.address_repo = ProfessionalAddressRepository()
        self.contact_repo = ProfessionalContactRepository()

    @transaction.atomic
    def create_professional(self, professional_data, address_data, contact_data):
        professional_data.pop("address", None)
        professional_data.pop("contact", None)

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
        professional = self.professional_repo.get_by_id(professional_id)

        for field, value in (professional_data or {}).items():
            if value is not None:
                setattr(professional, field, value)
        professional.save()

        if address_data:
            self.address_repo.update_by_filter({"professional": professional}, **address_data)
        if contact_data:
            self.contact_repo.update_by_filter({"professional": professional}, **contact_data)

        return professional

    def delete_professional(self, professional_id):
        return self.professional_repo.delete(professional_id)