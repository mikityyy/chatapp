from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser, Message


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','thumbnail',)

class LoginForm(AuthenticationForm):
    pass
    

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message',)
        widgets = {
            'message':forms.Textarea(attrs={"autocomplete": "off"}),
        }


class UsernameChangeForm (forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['username']


class EmailChangeForm (forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['email']

class EmailChangeForm (forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['email']


class ThumbnailChangeForm (forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['thumbnail']



class PasswordChangeForm(PasswordChangeForm):
    pass
   