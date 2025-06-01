# from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = "core.views.error_handlers.global_404_handler"


urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{settings.API_PATH_PREFIX}/", include("blogapi.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Should be changed before deployment
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += debug_toolbar_urls()
