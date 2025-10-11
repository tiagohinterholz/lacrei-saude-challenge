from rest_framework import serializers
from apps.professionals.models import Professional, ProfessionalAddress, ProfessionalContact


class ProfessionalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalAddress
        fields = [
            "id",
            "street",
            "number",
            "complement",
            "district",
            "city",
            "state",
            "postal_code",
            "country",
        ]


class ProfessionalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalContact
        fields = ["id", "email", "phone"]


class ProfessionalSerializer(serializers.ModelSerializer):
    address = ProfessionalAddressSerializer()
    contact = ProfessionalContactSerializer()

    class Meta:
        model = Professional
        fields = [
            "id",
            "social_name",
            "profession",
            "is_active",
            "address",
            "contact",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        contact_data = validated_data.pop("contact")

        professional = Professional.objects.create(**validated_data)
        ProfessionalAddress.objects.create(professional=professional, **address_data)
        ProfessionalContact.objects.create(professional=professional, **contact_data)
        return professional

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        contact_data = validated_data.pop("contact", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        if contact_data:
            contact = instance.contact
            for attr, value in contact_data.items():
                setattr(contact, attr, value)
            contact.save()

        return instance