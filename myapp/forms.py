from django import forms
from django.contrib.auth.forms import  PasswordChangeForm
from .models import CustomUser, Message
#from allauth.account.forms import SignupForm


#class CustomSignupForm(SignupForm):
    #thumbnail=forms.ImageField(label='アイコン画像', required=False)
    #class Meta:
        #model=CustomUser
        #fields=('username, password1, password2, email, thumbnail')


class FriendSearchForm(forms.Form):
    keyword = forms.CharField(
        label='フレンド検索', 
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        )  
        

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
   