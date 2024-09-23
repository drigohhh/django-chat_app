from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # primeira página
    path("", views.index, name="index"),
    path("send/", views.sendMessage, name="sendMessage"),
    # página de admin
    path("admin/", admin.site.urls),
]
