from django import forms
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserCreationForm


from videxapp.models import *

User = get_user_model()

class RemoveErrorsFromForm(ErrorList):
    def __str__(self):
        return ''


class UserFormLogin(forms.ModelForm):
    class Meta:
        model = VidexUser
        fields = ['username', 'password']

        help_texts = {
            'username': "نام کاربری",
            'password': "کلمهٔ عبور"
        }


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'national_id',
            'telephone_number',
            'first_name',
            'last_name',
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("نام کاربری شما در سیستم موجود است")

    def clean_password2(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError("گذرواژه و تکرار گذرواژه یکسان نیستند")



class MakeCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MakeCourseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = (
            'name',
        )


class MakeExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MakeExamForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Exam
        fields = (
            'name',
            'release_date',
            'deadline_date',
            'min_grade',
        )
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MakeSessionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MakeSessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = (
            'name',
            'text',
        )

class MakeMultipleChoiceQuestionForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(MakeMultipleChoiceQuestionForm, self).__init__(*args, **kwargs)

    CHOICES = (
        ("1", "first choice"),
        ("2", "second choice"),
        ("3", "third choice"),
        ("4", "forth choice"),
    )

    answer_id = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = MultipleChoiceQuestion
        fields = (
            'question_text',
            'choice1',
            'choice2',
            'choice3',
            'choice4',
        )

class MakeWrittenQuestionForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(MakeWrittenQuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = WrittenQuestion
        fields = (
            'question_text',
        )
    def clean(self):
        super(MakeWrittenQuestionForm, self).clean()
        question_text = self.cleaned_data.get('question_text')
        print(f'THIS IS THE QUESITON: {question_text}')
        if question_text is None:
            raise forms.ValidationError('the question is not specified')

class MakeSingleAnswerQuestionForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(MakeSingleAnswerQuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SingleAnswerQuestion
        fields = (
            'question_text',
            'answer',
        )
