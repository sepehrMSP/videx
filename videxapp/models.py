from django.db import models
from django.contrib.auth.models import AbstractUser


class Course(models.Model):
    name = models.CharField(max_length=64, verbose_name="course name")
    LEVELS = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]
    level = models.CharField(max_length=12, choices=LEVELS, default='Intermediate')
    cost = models.PositiveIntegerField(default=0, verbose_name='Course cost')
    creators = models.TextField(null=True, blank=True, verbose_name='Creators')
    ex_len = models.PositiveIntegerField(null=True, blank=True, verbose_name='Expected length', help_text='In weeks')
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


class VidexUser(AbstractUser):
    national_id = models.IntegerField(null=True, blank=True, verbose_name="ID Number")
    telephone_number = models.CharField(null=True, max_length=11, verbose_name='cellphone number')
    balance = models.IntegerField(verbose_name='Account balance', default=0)
    registered_courses = models.ManyToManyField(Course, related_name='registered_courses')
    finished_courses = models.ManyToManyField(Course, related_name='finished_courses')
    user_img = models.ImageField(default='blank-profile.png', blank=True, upload_to='images/', verbose_name='Profile picture')
    resume = models.FileField(null=True, blank=True, upload_to='resume', verbose_name='CV')
    card_number = models.CharField(null=True, blank=True, max_length=16, verbose_name='Credit card number')
