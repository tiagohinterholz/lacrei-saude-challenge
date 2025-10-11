from django.db import models
from apps.common.models import BaseModel


class Professional(BaseModel):
    social_name = models.CharField(max_length=120)
    profession = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.social_name} - {self.profession}"


class ProfessionalAddress(BaseModel):
    professional = models.OneToOneField(
        Professional, on_delete=models.CASCADE, related_name="address"
    )
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Brazil")

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}"


class ProfessionalContact(BaseModel):
    professional = models.OneToOneField(
        Professional, on_delete=models.CASCADE, related_name="contact"
    )
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.email} - {self.phone}"
