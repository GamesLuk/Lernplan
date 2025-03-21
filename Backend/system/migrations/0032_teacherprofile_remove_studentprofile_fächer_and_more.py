# Generated by Django 5.1.5 on 2025-02-15 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0031_alter_studentprofile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_ID', models.IntegerField(db_index=True, null=True, unique=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('first_name', models.CharField(db_index=True, max_length=255)),
                ('last_name', models.CharField(db_index=True, max_length=255)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('teams', models.JSONField(db_index=True, default=list, null=True)),
                ('klassen', models.JSONField(db_index=True)),
                ('role', models.CharField(db_index=True, max_length=255)),
                ('fächer', models.JSONField(db_index=True, default=list)),
                ('beschreibung', models.TextField(default=None, null=True)),
                ('kürzel', models.CharField(db_index=True, default=None, max_length=10, null=True)),
                ('profile_picture', models.TextField(blank=True, null=True)),
                ('lernzeiten', models.JSONField(db_index=True, default=list)),
            ],
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='fächer',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='kürzel',
        ),
    ]
