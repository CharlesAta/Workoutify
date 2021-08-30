from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import UserForm, ScheduleForm
from .models import Workout

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class WorkoutCreate(CreateView):
    model = Workout
    fields = ['name', 'location']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutList(ListView):
    model = Workout

class WorkoutDetail(DetailView):
    model = Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule_form'] = ScheduleForm()
        return context

class WorkoutDelete(DeleteView):
    model = Workout
    success_url = '/workouts/'

def add_schedule(request, workout_id):
    form = ScheduleForm(request.POST)
    if form.is_valid():
        new_schedule = form.save(commit=False)
        new_schedule.workout_id = workout_id
        new_schedule.save()
    return redirect('workouts_detail', pk=workout_id)

def delete_schedule(request, workout_id):
    pass
    # return redirect('workouts_detail', pk=workout_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)