from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('workouts/', views.WorkoutList.as_view(), name='workouts_index'),
    path('workouts/create/', views.WorkoutCreate.as_view(), name='workouts_create'),
    path('workouts/<int:pk>/', views.WorkoutDetail.as_view(), name='workouts_detail'),
    path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workouts_delete'),
    path('workouts/<int:workout_id>/add_schedule/', views.add_schedule, name='add_schedule'),
    path('workouts/<int:workout_id>/delete_schedule/', views.delete_schedule, name='delete_schedule'),
    path('accounts/signup/', views.signup, name='signup'),
]