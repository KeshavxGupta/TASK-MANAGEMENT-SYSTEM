from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('TASKMASTERAPP.urls')),
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls', namespace='shop')),
]

# Add this only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)