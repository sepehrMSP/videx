from django.db import models
from django.contrib.auth.models import AbstractUser

class Course(models.Model):
    name = models.CharField(max_length=64, verbose_name="course name")
    instructor = models.ForeignKey('VidexUser', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @property
    def course_id(self):
        return self.id

    @property
    def number_of_registered_students(self):
        return VidexUser.objects.filter(registered_courses__id=self.course_id).count()

class Session(models.Model):
    name = models.CharField(max_length=64, verbose_name="session name")
    text = models.TextField(verbose_name="session content")
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=64, verbose_name="exam name")
    release_date = models.DateTimeField()
    deadline_date = models.DateTimeField()
    min_grade = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class VidexUser(AbstractUser):
    national_id = models.IntegerField(null=True, blank=True, verbose_name="ID Number")
    telephone_number = models.CharField(null=True, max_length=11, verbose_name='cellphone number')
    balance = models.IntegerField(verbose_name='balance', default=0)
    registered_courses = models.ManyToManyField(Course, related_name='registered_courses')
    finished_courses = models.ManyToManyField(Course, related_name='finished_courses')

class Question(models.Model):
    question_text = models.TextField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

class Answer(models.Model):
    value = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey('VidexUser', on_delete=models.CASCADE)

class MultipleChoiceQuestion(Question):
    choice1 = models.TextField()
    choice2 = models.TextField()
    choice3 = models.TextField()
    choice4 = models.TextField()
    CHOICES = (
        (1, 'one'),
        (2, 'two'),
        (3, 'three'),
        (4, 'four'),
    )
    correct_answer_id = models.IntegerField(choices=CHOICES, default=1)

class WrittenQuestion(Question):
    pass

class SingleAnswerQuestion(Question):
    correct_answer = models.CharField(max_length=100)
