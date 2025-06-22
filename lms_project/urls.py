# lms_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Ensure Django's built-in authentication URLs are included under the 'accounts' namespace
    path('accounts/', include('django.contrib.auth.urls')),
]
