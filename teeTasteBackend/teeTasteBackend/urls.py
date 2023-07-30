"""teeTasteBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import CreateUserView, UserAuthenticationView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("save_interaction/", views.save_interaction, name="save_interaction"),
    path("fetch_next_shoes/", views.fetch_next_shoes, name="fetch_next_shoes"),

    path('users/create/', CreateUserView.as_view(), name='create_user'),  # URL for user creation
    path('users/login/', UserAuthenticationView.as_view(), name='login'),
    path('users/logout/', UserAuthenticationView.as_view(), name='logout'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)