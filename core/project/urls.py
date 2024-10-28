from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # first page and logic routes
    path("", views.index, name="index"),
    path("send/", views.sendMessage, name="sendMessage"),
    # admin page
    path("admin/", admin.site.urls),
]
