# Generated by Django 4.0.2 on 2022-03-15 17:17

from django.db import migrations, models
import house.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('image', models.FileField(blank=True, null=True, upload_to=house.models.GenerateHouseImagePath())),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('points', models.IntegerField(default=0)),
                ('completed_tasks_count', models.IntegerField(default=0)),
                ('notcompleted_tasks_count', models.IntegerField(default=0)),
            ],
        ),
    ]
