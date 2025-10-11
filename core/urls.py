from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointments/', include('apps.appointments.urls')),
    path('professionals/', include('apps.professionals.urls')),
    path('api/auth/', include('apps.users.urls'))
]
