from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .forms import NewUserForm, ScheduleForm, WeatherForm, ModelForm
from .models import Workout, Schedule, Exercise, Weather
import requests
import os
import datetime


SECRET_KEY = os.environ['WEATHER_API_KEY']

cities = {
    'C': 5913490,
    'S': 6141256,
    'V': 6173331,
    'T': 6167865,
    'M': 6077246
}

# Create your views here.

def auto_weather(user_id):
    weather = Weather.objects.get(user=user_id)
    if weather.date != datetime.date.today():
        cities_id = weather.city_id
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?id={ cities_id }&appid={SECRET_KEY}')
        weatherdata = response.json()
        weather.temperature = int(weatherdata['main']['temp'] - 273.15)
        weather.description = weatherdata['weather'][0]['main']
        weather.icon = f"https://openweathermap.org/img/wn/{weatherdata['weather'][0]['icon']}@2x.png"
        weather.date = datetime.date.today()
        weather.save()

def auto_schedule():
    try:
        Schedule.objects.filter(date__lt=datetime.date.today()).delete()
    except Schedule.DoesNotExist:
        pass

def get_todays_workout(todays_date, user_id):
    todays_workouts = Workout.objects.filter(id__in = Schedule.objects.filter(date=todays_date).values("workout_id"))
    return todays_workouts

def get_weeks_workout(todays_date, user_id):
    start_date = todays_date + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=6)
    weeks_workouts = Workout.objects.filter(id__in = Schedule.objects.filter(date__range=[start_date, end_date]).values("workout_id"))
    return weeks_workouts
 

def home(request):
    user_id = request.user.id
    auto_schedule()
    todays_date = datetime.date.today()
    todays_workouts = get_todays_workout(todays_date, user_id)
    weeks_workouts = get_weeks_workout(todays_date, user_id)
    current_weather = Weather.objects.filter(user=user_id)
    if current_weather:
        auto_weather(user_id)
        form = WeatherForm(initial={'city': current_weather[0].city})
        current_weather = current_weather[0]
    else:
        form = WeatherForm()
        current_weather = None

    context = {
        'weather_form': form, 'weather': current_weather,
        'todays_workouts': todays_workouts, 'weeks_workouts': weeks_workouts
        }
    return render(request, 'home.html', context)


class WeatherForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['city']

def about(request):
    return render(request, 'about.html')

class WorkoutCreate(CreateView):
    model = Workout
    fields = ['name', 'location']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def workout_index(request):
    workout_list = Workout.objects.filter(user=request.user)
    return render(request, 'main_app/workout_list.html', {'workout_list': workout_list})

class WorkoutDetail(DetailView):
    model = Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule_form'] = ScheduleForm()
        return context

def workouts_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    exercises = Exercise.objects.filter(user=request.user)
    exercises_workout_doesnt_have = exercises.exclude(id__in = workout.exercises.all().values_list('id'))
    schedule_form = ScheduleForm()
    return render(request, 'main_app/workout_detail.html', {
        'workout': workout, 'schedule_form': schedule_form,
        'exercises': exercises_workout_doesnt_have
    })

def assoc_exercise(request, workout_id, exercise_id):
    if request.is_ajax() and request.method == "POST":
        workout = Workout.objects.get(id=workout_id)
        workout.exercises.add(exercise_id)
        exercise = Exercise.objects.get(id=exercise_id)
        return JsonResponse({"exercise": model_to_dict(exercise)}, status=200)
    return JsonResponse({"error": ""}, status=400)

def unassoc_exercise(request, workout_id, exercise_id):
    if request.is_ajax() and request.method == "POST":
        workout = Workout.objects.get(id=workout_id)
        workout.exercises.remove(exercise_id)
        exercise = Exercise.objects.get(id=exercise_id)
        return JsonResponse({"exercise": model_to_dict(exercise)}, status=200)
    return JsonResponse({"error": ""}, status=400)

class WorkoutDelete(DeleteView):
    model = Workout
    success_url = '/workouts/'

class WorkoutUpdate(UpdateView):
    model = Workout
    fields = ['name', 'location']

class ExerciseCreate(CreateView):
    model = Exercise
    fields = ['name', 'description', 'sets', 'reps']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def exercise_index(request):
    exercise_list = Exercise.objects.filter(user=request.user)
    return render(request, 'main_app/exercise_list.html', {'exercise_list': exercise_list})

class ExerciseDetail(DetailView):
    model = Exercise

class ExerciseDelete(DeleteView):
    model = Exercise
    success_url = '/exercises/'

class ExerciseUpdate(UpdateView):
    model = Exercise
    fields = ['name', 'description', 'sets', 'reps']

def update_weather(request):
    form = WeatherForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cities_id = cities[data['city']]
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?id={ cities_id }&appid={SECRET_KEY}')
        weatherdata = response.json()
        user_id = request.user
        
        obj, created = Weather.objects.update_or_create(
            user = user_id,
            defaults={
                'city_id': cities_id,
                'temperature':int(weatherdata['main']['temp'] - 273.15),
                'description':weatherdata['weather'][0]['main'],
                'city': data['city'],
                'icon': f"https://openweathermap.org/img/wn/{weatherdata['weather'][0]['icon']}@2x.png",
                'date': datetime.date.today()
            }
        )
    return redirect('home')

def add_schedule(request, workout_id):
    if request.is_ajax() and request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            new_schedule = form.save(commit=False)
            new_schedule.workout_id = workout_id
            new_schedule.save()
            return JsonResponse({"schedule": model_to_dict(new_schedule)}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)
    return JsonResponse({"error": ""}, status=400)

def delete_schedule(request, workout_id, schedule_id):
    if request.is_ajax() and request.method == "POST":
        sched = Schedule.objects.get(id=schedule_id)
        sched.delete()
        return JsonResponse({"result": "ok"}, status=200)
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = NewUserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


    