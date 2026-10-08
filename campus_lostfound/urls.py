from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import system_health_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('items.urls')),
    path('accounts/', include('accounts.urls')),
    path('claims/', include('claims.urls')),
    path('system-health/', system_health_view, name='system_health'),
    path('health/', system_health_view, name='health'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
