from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('negotiation.urls')),
    path('negotiation/', include("negotiation.urls")),
    path('admin/', admin.site.urls),
]