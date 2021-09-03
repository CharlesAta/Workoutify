from django.forms import ModelForm
from .models import Schedule, Weather
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'time']

class WeatherForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['city']
        