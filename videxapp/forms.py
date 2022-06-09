from django import forms
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserCreationForm


from videxapp.models import VidexUser

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
