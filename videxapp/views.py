from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from videxapp.forms import *
from videxapp.models import *

from django.utils import timezone

User = get_user_model()


def login_view(request):
    print('adsfasdfasdfasdf'*10)
    if request.method == 'GET':
        return render(request, 'pages/login.html',
                      {
                          'form': UserFormLogin(error_class=RemoveErrorsFromForm)
                      })
    elif request.method == 'POST':
        form = UserFormLogin(request.POST, error_class=RemoveErrorsFromForm)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return render(request, 'pages/home.html')
            else:
                return HttpResponse("Wrong creds" + "        " + form.cleaned_data['password'])
        else:
            return HttpResponse(form.errors)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=RemoveErrorsFromForm)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            HttpResponse(form.errors)
    else:
        form = RegisterForm(error_class=RemoveErrorsFromForm)
    return render(request, 'pages/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile_view(request):
    return render(request, "pages/profile.html")


@login_required
def make_new_course_view(request):
    if request.method == 'POST':
        form = MakeCourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            instructor = request.user
            Course(instructor=instructor, name=name).save()
            return redirect("/")
    else:
        form = MakeCourseForm()
    return render(request, 'pages/make_new_course.html', {
        'form': form
    })


@login_required
def make_new_session_view(request, course_id):
    course: Course = Course.objects.get(id=course_id)
    if request.user != course.instructor:
        raise PermissionDenied()
    if request.method == 'POST':
        form = MakeSessionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            Session(name=name, text=text, course=course).save()
            return redirect(f"/course/{course_id}/")
    else:
        form = MakeSessionForm()
    return render(request, 'pages/make_new_session.html', {
        'form': form
    })


@login_required
def make_new_exam_view(request, course_id):
    course: Course = Course.objects.get(id=course_id)
    if request.user != course.instructor:
        raise PermissionDenied()
    if request.method == 'POST':
        form = MakeExamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            release_date = form.cleaned_data['release_date']
            deadline_date = form.cleaned_data['deadline_date']
            min_grade = form.cleaned_data['min_grade']
            Exam(name=name, release_date=release_date, deadline_date=deadline_date,
                 min_grade=min_grade, course=course).save()
            return redirect(f"/course/{course_id}/")
    else:
        form = MakeExamForm()
    return render(request, 'pages/make_new_exam.html', {
        'form': form
    })


@login_required
def register_course_view(request, course_id: int):
    course = Course.objects.get(id=course_id)
    user: VidexUser = request.user
    user.registered_courses.add(course)
    user.save()
    return redirect(f'/course/{course.id}/')


@login_required
def course_page_view(request, course_id: int):
    course: Course = Course.objects.get(id=course_id)
    rule = "anonymous"
    if request.user.registered_courses.filter(id=course.id).exists():
        rule = "student"
    if course.instructor == request.user:
        rule = "instructor"

    return render(request, 'pages/course_page.html', {
        'rule': rule,
        'course': course,
        'lectures': None if rule == "anonymous" else Session.objects.filter(course=course),
        'exams': None if rule == "anonymous" else Exam.objects.filter(course=course),
        'students': VidexUser.objects.filter(registered_courses__id=course.course_id),
    })


@login_required
def exam_page_view(request, course_id: int, exam_id: int):
    exam: Exam = Exam.objects.get(id=exam_id)
    if exam.course.id != course_id:
        raise PermissionDenied()
    rule = "anonymous"
    if request.user.registered_courses.filter(id=exam.course.id).exists():
        rule = "student"
    if exam.course.instructor == request.user:
        rule = "instructor"

    if rule == "anonymous":
        raise PermissionDenied()

    now = timezone.now()
    time_state = "before_release" if now < exam.release_date else "before_deadline" if now < exam.deadline_date else "after_deadline"
    return render(request, 'pages/exam_page.html', {
        'rule': rule,
        'exam': exam,
        "time_state": time_state,
    })


@login_required
def courses_search_view(request):
    all_courses = Course.objects.all()
    registered_courses = request.user.registered_courses
    my_courses = all_courses.filter(instructor=request.user)
    return render(request, 'pages/courses.html', {
        'all_courses': all_courses,
        'my_courses': my_courses,
        'registered_courses': registered_courses,
    })


@login_required
def remove_course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    user: VidexUser = request.user
    user.registered_courses.remove(course)
    user.save()
    return redirect('courses')
