# Generated by Django 5.1.5 on 2025-01-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_alter_studentprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.TextField(max_length=16000, null=True),
        ),
    ]
