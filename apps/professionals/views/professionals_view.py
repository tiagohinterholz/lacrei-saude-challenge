from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.professionals.serializers.professionals_serializer import ProfessionalSerializer
from apps.professionals.services.professionals_service import ProfessionalService
from rest_framework.permissions import IsAuthenticated

class ProfessionalListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfessionalSerializer
    service = ProfessionalService()

    def get(self, request):
        professionals = self.service.list_professionals()
        serializer = self.serializer_class(professionals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                professional_data = {
                    "social_name": serializer.validated_data["social_name"],
                    "profession": serializer.validated_data["profession"],
                }
                address_data = serializer.validated_data["address"]
                contact_data = serializer.validated_data["contact"]

                professional = self.service.create_professional(professional_data, address_data, contact_data)
                return Response(self.serializer_class(professional).data, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessionalDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfessionalSerializer
    service = ProfessionalService()

    def get(self, request, professional_id):
        try:
            professional = self.service.get_professional(professional_id)
            serializer = self.serializer_class(professional)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"error": "Professional not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, professional_id):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                professional_data = {
                    "social_name": serializer.validated_data.get("social_name"),
                    "profession": serializer.validated_data.get("profession"),
                }
                address_data = serializer.validated_data.get("address")
                contact_data = serializer.validated_data.get("contact")

                professional = self.service.update_professional(professional_id, professional_data, address_data, contact_data)
                return Response(self.serializer_class(professional).data, status=status.HTTP_200_OK)

            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, professional_id):
        try:
            self.service.delete_professional(professional_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
