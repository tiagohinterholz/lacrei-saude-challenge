from django.urls import path
from apps.professionals.views.professionals_view import (
    ProfessionalListView,
    ProfessionalDetailView,
)

urlpatterns = [
    path("", ProfessionalListView.as_view(), name="professional-list"),
    path("<uuid:professional_id>/", ProfessionalDetailView.as_view(),
         name="professional-detail"),
]
