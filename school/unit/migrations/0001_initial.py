# Generated by Django 2.2.15 on 2021-03-18 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('uuid', models.UUIDField(editable=False, help_text='Unique ID', primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('uuid', models.UUIDField(editable=False, help_text='Unique ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('uuid', models.UUIDField(editable=False, help_text='Unique ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('number', models.CharField(max_length=32, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('class_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='unit.ClassRoom')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='classroom',
            name='teachers',
            field=models.ManyToManyField(related_name='class_rooms', to='unit.Teacher'),
        ),
        migrations.CreateModel(
            name='ClassHomeWork',
            fields=[
                ('uuid', models.UUIDField(editable=False, help_text='Unique ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, null=True)),
                ('description', models.TextField()),
                ('class_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_works', to='unit.ClassRoom')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_works', to='unit.Teacher')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
