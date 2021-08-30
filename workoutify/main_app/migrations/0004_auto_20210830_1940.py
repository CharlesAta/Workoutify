# Generated by Django 3.2.6 on 2021-08-30 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_schedule_workout'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='', max_length=250)),
                ('reps', models.IntegerField()),
                ('sets', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='workout',
            name='exercises',
            field=models.ManyToManyField(to='main_app.Exercise'),
        ),
    ]
