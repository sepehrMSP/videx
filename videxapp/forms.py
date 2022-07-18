from django import forms
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserCreationForm


from videxapp.models import Course, VidexUser, Session, Video

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
            'user_img',
            'resume',
            'card_number'
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

    def clean_user_img(self):
        user_img = self.cleaned_data['user_img']
        if not user_img:
            user_img = 'blank-profile.png'
        return user_img

    def clean_resume(self):
        resume = self.cleaned_data['resume']
        if not resume:
            return resume
        if resume.content_type != 'application/pdf':
            raise forms.ValidationError("CV must be PDF")
        return resume

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number:
            return card_number
        if not card_number.isnumeric():
            raise forms.ValidationError('Credit card number consists only of numbers')
        if len(card_number) != 16:
            raise forms.ValidationError('Credit card number must be exactly 16 digits')
        return card_number


class MakeCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MakeCourseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = (
            'name',
            'level',
            'cost',
            'creators',
            'ex_len',
            'description'
        )


class MakeSessionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MakeSessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = (
            'name',
            'text',
        )


class MakeVideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MakeVideoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Video
        fields = (
            'name',
            'text',
            'content',
        )

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content:
            raise forms.ValidationError('You must upload a video!')
        if content.content_type != 'video/mp4':
            raise forms.ValidationError("Your video file must be mp4")
        return content

