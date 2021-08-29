from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Workout(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('workouts_detail', kwargs={'pk':self.id})

class Schedule(models.Model):
    date = models.DateField('workout date')
    time = models.TimeField('workout time')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

    def __str__(self):
        return f"Workout scheduled for {self.date} at {self.time}"
    
    class Meta:
        ordering = ['-date']