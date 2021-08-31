from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import UserForm, ScheduleForm
from .models import Workout, Schedule, Exercise
from django.http import JsonResponse
from django.forms.models import model_to_dict

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

def workouts_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    exercises_workout_doesnt_have = Exercise.objects.exclude(id__in = workout.exercises.all().values_list('id'))
    schedule_form = ScheduleForm()
    return render(request, 'main_app/workout_detail.html', {
        'workout': workout, 'schedule_form': schedule_form,
        # Add the toys to be displayed
        'exercises': exercises_workout_doesnt_have
    })

def assoc_exercise(request, workout_id, exercise_id):
    Workout.objects.get(id=workout_id).exercises.add(exercise_id)
    return redirect('workouts_detail', workout_id=workout_id)

def unassoc_exercise(request, workout_id, exercise_id):
    Workout.objects.get(id=workout_id).exercises.remove(exercise_id)
    return redirect('workouts_detail', workout_id=workout_id)

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

class ExerciseList(ListView):
    model = Exercise

class ExerciseDetail(DetailView):
    model = Exercise

class ExerciseDelete(DeleteView):
    model = Exercise
    success_url = '/exercises/'

class ExerciseUpdate(UpdateView):
    model = Exercise
    fields = ['name', 'description', 'sets', 'reps']

def add_schedule(request, workout_id):
    if request.is_ajax() and request.method == "POST":
        form = ScheduleForm(request.POST)
        print("form", form)
        if form.is_valid():
            new_schedule = form.save(commit=False)
            new_schedule.workout_id = workout_id
            instance = new_schedule.save()
            dict_obj = model_to_dict(instance)
            serialized = json.dumps(dict_obj)
            print(serialized)
            # return JsonResponse({"new_schedule": new_schedule}, status=200)
    # else:
    #     errors = form.errors.as_json()
    #     return JsonResponse({"errors": errors}, status=400)
    # return redirect('workouts_detail', workout_id=workout_id)

def delete_schedule(request, workout_id, schedule_id):
    Schedule.objects.filter(id=schedule_id).delete()
    return redirect('workouts_detail', workout_id=workout_id)
    
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