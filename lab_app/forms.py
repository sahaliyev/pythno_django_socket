from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput

from .models import UploadImage


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    username = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']
        widgets = {
            'password': PasswordInput(),
            'confirm_password': PasswordInput()
        }

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            raise forms.ValidationError('This email already in use!')

        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not len(password) > 4:
            raise forms.ValidationError('less than 5')

        if not password == confirm_password:
            raise forms.ValidationError('Passwords must match')
        return password


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['title', 'image']

