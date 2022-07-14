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
    path('course/<int:course_id>/exam/add', make_new_exam_view, name='make_new_exam'),
    path('course/<int:course_id>/exam/<int:exam_id>', exam_page_view, name='exam_page'),
    path('course/<int:course_id>/exam/<int:exam_id>/edit', edit_exam_view, name='exam_edit'),
    path('course/<int:course_id>/exam/<int:exam_id>/submit', exam_submit_view, name='exam_submit_answer'),
    path('course/<int:course_id>/exam/<int:exam_id>/question/add', choose_question_type_view, name='choose_question'),
    path('course/<int:course_id>/exam/<int:exam_id>/question/add/multiple-choice', add_multiple_choice_question_view, name='add_multiple_choice_question'),
    path('course/<int:course_id>/exam/<int:exam_id>/question/add/single-answer', add_single_answer_question_view, name='add_single_answer_question'),
    path('course/<int:course_id>/exam/<int:exam_id>/question/add/written', add_written_question_view, name='add_question'),

    path('course/<int:course_id>/session/add', make_new_session_view, name='make_new_session'),
    path('course/<int:course_id>/remove', remove_course_view, name='remove_course'),
    path('course/<int:course_id>/register', register_course_view, name='register_course'),
    path('course/<int:course_id>/', course_page_view, name='course_page'),
    path('course/add', make_new_course_view, name='make_new_course'),
]

urlpatterns += staticfiles_urlpatterns()
