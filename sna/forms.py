from SocialNetworkApp import settings
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from taggit.forms import TagWidget
from .models import CustomUser, UserPost, CommentPost


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'login-user',
        'placeholder': 'Enter Password', }))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(attrs={
        'class': 'login-user',
        'placeholder': 'Confirm Password'}))
    dob = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={
        'class': 'login-user',
        'placeholder': 'dd/mm/yyyy'
    }))

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "dob"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'login-user',
                'placeholder': 'Enter Username'}),
            'email': forms.TextInput(attrs={
                'class': 'login-user',
                'placeholder': 'Enter Email'}),
        }


class CreatePostForm(ModelForm):
    image = forms.ImageField(error_messages={'invalid': (
        'Image files only')}, required=False, widget=forms.FileInput(attrs={
            'class': 'upload-image',
        }))

    class Meta:
        model = UserPost
        fields = ["message", "image"]
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'message-post',
                'placeholder': 'Write a post here...'
            })
        }


class CreateCommentForm(ModelForm):
    class Meta:
        model = CommentPost
        fields = ["message"]
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'message-comment',
                'placeholder': 'Write a comment here...'
            })
        }


class AccountSettingForm(ModelForm):
    profile_img = forms.ImageField(error_messages={
        'invalid': ('Image files only')}, label='Profile Image', widget=forms.FileInput)
    dob = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={
        'class': 'form-input',
        'placeholder': 'dd/mm/yyyy'
    }))

    class Meta:
        model = CustomUser
        fields = ["username", "email", "dob",
                  "bio", "profile_img", "interests"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email'}),
            'bio': forms.Textarea(attrs={
                'class': 'bio',
                'placeholder': 'Bio'}),
            'interests': TagWidget(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Your Interests... (Seperated by commas or whitespace)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].widget.format = '%d/%m/%Y'
