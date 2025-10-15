from django.urls import path
from apps.appointments.views.appointments_view import (
    AppointmentListView,
    AppointmentDetailView,
    AppointmentByProfessionalView,
)

urlpatterns = [
    path("", AppointmentListView.as_view(), name="appointment-list"),
    path("<uuid:appointment_id>/", AppointmentDetailView.as_view(),
         name="appointment-detail"),
    path("professional/<uuid:professional_id>/",
         AppointmentByProfessionalView.as_view(), name="appointment-by-professional"),
]
