"""
URL configuration for LITRevue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
import authentication.views
import main_feed.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication.views.LogginPage.as_view(), name="login"),
    path("logout/", authentication.views.LoggingOutView.as_view(), name="logout"),
    path("home/", main_feed.views.home, name="homepage"),
    path("signup/", authentication.views.SignUpPage.as_view(), name="signup"),
    path("ticket/new/", main_feed.views.create_ticket, name="create_ticket"),
    path("review/new/", main_feed.views.create_review, name="create_review")
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
