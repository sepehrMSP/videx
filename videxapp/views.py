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


def get_rule(request, exam):
    rule = "anonymous"
    if request.user.registered_courses.filter(id=exam.course.id).exists():
        rule = "student"
    if exam.course.instructor == request.user:
        rule = "instructor"

    return rule


@login_required
def exam_page_view(request, course_id: int, exam_id: int):
    def answer_of_question(q, user):
        qs = Answer.objects.filter(question=q, user=user)
        if not qs.first() is None:
            return qs.first().value
        else:
            return None
    exam: Exam = Exam.objects.get(id=exam_id)
    written_questions = [{
        "type": "written",
        "text": x.question_text,
        "answer": answer_of_question(x, request.user),
    } for x in WrittenQuestion.objects.filter(exam=exam)]
    multiple_choice_questions = [{
        "type": "multi_choice",
        "text": x.question_text,
        "choices": [x.choice1, x.choice2, x.choice3, x.choice4],
        "answer": answer_of_question(x, request.user),
    } for x in MultipleChoiceQuestion.objects.filter(exam=exam)]
    single_answer_questions = [{
        "type": "single_answer",
        "text": x.question_text,
        "answer": answer_of_question(x, request.user),
    } for x in SingleAnswerQuestion.objects.filter(exam=exam)]
    questions = [*written_questions, *multiple_choice_questions, *single_answer_questions]
    if exam.course.id != course_id:
        raise PermissionDenied()
    rule = get_rule(request, exam)

    if rule == "anonymous":
        raise PermissionDenied()

    now = timezone.now()
    time_state = "before_release" if now < exam.release_date else "before_deadline" if now < exam.deadline_date else "after_deadline"
    return render(request, 'pages/exam_page.html', {
        'rule': rule,
        'exam': exam,
        'questions': questions,
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


@login_required
def add_multiple_choice_question_view(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.filter(course=course).get(id=exam_id)
    rule = get_rule(request, exam)
    if rule != 'instructor':
        raise PermissionDenied()

    if request.method == 'POST':
        multiple_choice_question_form = MakeMultipleChoiceQuestionForm(
            request.POST)
        if multiple_choice_question_form.is_valid():
            question_text = multiple_choice_question_form.cleaned_data['question_text']
            choice1 = multiple_choice_question_form.cleaned_data['choice1']
            choice2 = multiple_choice_question_form.cleaned_data['choice2']
            choice3 = multiple_choice_question_form.cleaned_data['choice3']
            choice4 = multiple_choice_question_form.cleaned_data['choice4']

            answer_id = multiple_choice_question_form.cleaned_data['correct_answer_id']

        MultipleChoiceQuestion(exam=exam, question_text=question_text, choice1=choice1,
                               choice2=choice2, choice3=choice3, choice4=choice4, correct_answer_id=answer_id).save()
        return redirect('exam_page', course_id=course_id, exam_id=exam_id)

    elif request.method == 'GET':
        multiple_choice_question_form = MakeMultipleChoiceQuestionForm()

        return render(request, 'pages/make_new_multiple_answer_question.html', {
            'multiple_choice_question_form': multiple_choice_question_form,
        })


@login_required
def add_single_answer_question_view(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.filter(course=course).get(id=exam_id)
    rule = get_rule(request, exam)
    if rule != 'instructor':
        raise PermissionDenied()

    if request.method == 'POST':
        single_answer_form = MakeSingleAnswerQuestionForm(request.POST)
        if single_answer_form.is_valid():
            question_text = single_answer_form.cleaned_data['question_text']
            answer = single_answer_form.cleaned_data['answer']

        SingleAnswerQuestion(
            exam=exam, question_text=question_text, answer=answer).save()
        return redirect('exam_page', course_id=course_id, exam_id=exam_id)

    elif request.method == 'GET':
        single_answer_form = MakeSingleAnswerQuestionForm()

        return render(request, 'pages/make_new_single_answer_question.html', {
            'single_answer_question_form': single_answer_form,
        })


@login_required
def add_written_question_view(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.filter(course=course).get(id=exam_id)
    rule = get_rule(request, exam)
    if rule != 'instructor':
        raise PermissionDenied()

    if request.method == 'POST':
        written_question_form = MakeWrittenQuestionForm(request.POST)
        if written_question_form.is_valid():
            question_text = written_question_form.cleaned_data['question_text']

        WrittenQuestion(exam=exam, question_text=question_text).save()
        return redirect('exam_page', course_id=course_id, exam_id=exam_id)

    elif request.method == 'GET':
        written_question_form = MakeWrittenQuestionForm()

        return render(request, 'pages/make_new_written_question.html', {
            'written_question_form': written_question_form,
        })


@login_required
def choose_question_type_view(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.filter(course=course).get(id=exam_id)

    rule = get_rule(request, exam)
    if rule != 'instructor':
        raise PermissionDenied()

    return render(request, 'pages/choose_question_type.html')
