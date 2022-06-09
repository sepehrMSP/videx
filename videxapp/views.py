from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from videxapp.forms import MakeCourseForm, RegisterForm, RemoveErrorsFromForm, UserFormLogin
from videxapp.models import Course


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


@user_passes_test(lambda u: u.is_superuser)
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
