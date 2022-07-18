from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from videxapp.forms import *
from videxapp.models import Course, VidexUser

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
        form = RegisterForm(request.POST, request.FILES, error_class=RemoveErrorsFromForm)
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
            course = form.save(commit=False)
            instructor = request.user
            course.instructor = instructor
            course.save()
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
            instructor = request.user
            Session(name=name, text=text, course=course).save()
            return redirect(f"/course/{course_id}/")
    else:
        form = MakeSessionForm()
    return render(request, 'pages/make_new_session.html', {
        'form': form
    })


@login_required
def make_new_video_view(request, course_id):
    course: Course = Course.objects.get(id=course_id)
    if request.user != course.instructor:
        raise PermissionDenied()
    if request.method == 'POST':
        form = MakeVideoForm(request.POST, request.FILES, error_class=RemoveErrorsFromForm)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            content = form.cleaned_data['content']
            Video(name=name, text=text, content=content, course=course).save()
            return redirect(f"/course/{course_id}/")
        else:
            HttpResponse(form.errors)
    else:
        form = MakeVideoForm(error_class=RemoveErrorsFromForm)
    return render(request, 'pages/make_new_video.html', {
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
        'videos': None if rule == "anonymous" else Video.objects.filter(course=course),
        'students': VidexUser.objects.filter(registered_courses__id=course.course_id),
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

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES, instance=request.user, error_class=RemoveErrorsFromForm)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            HttpResponse(form.errors)
    else:
        form = RegisterForm(instance=request.user, error_class=RemoveErrorsFromForm)
    return render(request, 'pages/edit_profile.html', {'form': form})
