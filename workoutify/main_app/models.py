from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250, default='')
    reps = models.IntegerField()
    sets = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    def __str__(self):
        return f"Exercise {self.name} created for {self.sets} sets and {self.reps} reps"
    def get_absolute_url(self):
        return reverse('exercises_detail', kwargs={'pk':self.id})

# Create your models here.
class Workout(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('workouts_detail', kwargs={'pk':self.id})
    

class Schedule(models.Model):
    date = models.DateField('workout date')
    time = models.TimeField('workout time')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='schedules')

    

    def __str__(self):
        return f"Workout scheduled for {self.date} at {self.time}"
    
    class Meta:
        ordering = ['-date']


