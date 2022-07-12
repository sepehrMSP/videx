"""videx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from videxapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),

    path('login', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
    path('profile', profile_view, name='profile'),

    path('course/all', courses_search_view, name='courses'),
    path('course/<int:course_id>/session/add', make_new_session_view, name='make_new_session'),
    path('course/<int:course_id>/remove', remove_course_view, name='remove_course'),
    path('course/<int:course_id>/register', register_course_view, name='register_course'),
    path('course/<int:course_id>/', course_page_view, name='course_page'),
    path('course/add', make_new_course_view, name='make_new_course'),
    path('edit_profile', edit_profile_view, name='edit_profile'),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
