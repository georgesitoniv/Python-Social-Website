from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LogInForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_validate = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email')

    def clean_password_validate(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_validate']:
            raise forms.ValidationError("Passwords does not match")
        return cd['password_validate']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
