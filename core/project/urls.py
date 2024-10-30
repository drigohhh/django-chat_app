from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # first page and logic routes
    path("", views.index, name="index"),
    path("send/", views.sendMessage, name="sendMessage"),
    path("receive/", views.receiveResponse, name="receiveResponse"),
    # admin page
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
