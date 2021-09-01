from django.contrib import admin
from .models import Workout, Schedule, Exercise, Weather

# Register your models here.
admin.site.register(Workout)
admin.site.register(Schedule)
admin.site.register(Exercise)
admin.site.register(Weather)