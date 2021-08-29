from django.forms import ModelForm
from .models import User, Schedule
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'time']

# class SettingsForm(forms.Form):
#     time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'timepicker'}))