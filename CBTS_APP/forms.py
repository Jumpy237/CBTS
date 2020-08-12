from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Test, Topic, Subject, Question, Choice


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username' , 'email', 'password1', 'password2']


class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        widgets = {'author': forms.HiddenInput()}

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
        widgets = {'subject': forms.HiddenInput()}

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {'teacher': forms.HiddenInput()}

class QuestionForm(ModelForm):
   

    class Meta:
        model = Question
        fields = '__all__'
        widgets = {'subject': forms.HiddenInput()}

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'
        