# lms_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # THIS LINE IS CRUCIAL: Ensure 'namespace='accounts'' is explicitly set here,
    # and pass django.contrib.auth.urls as a 2-tuple.
    path('accounts/', include(('django.contrib.auth.urls', 'accounts'), namespace='accounts')),
]
