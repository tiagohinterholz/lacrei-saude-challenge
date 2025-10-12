from apps.common.repositories.common_repository import CommonRepository
from apps.professionals.models.professionals_model import Professional, ProfessionalAddress, ProfessionalContact


class ProfessionalRepository(CommonRepository):
    def __init__(self):
        super().__init__(Professional)


class ProfessionalAddressRepository(CommonRepository):
    def __init__(self):
        super().__init__(ProfessionalAddress)


class ProfessionalContactRepository(CommonRepository):
    def __init__(self):
        super().__init__(ProfessionalContact)