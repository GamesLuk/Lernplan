# Generated by Django 5.1.5 on 2025-01-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_alter_studentprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.CharField(db_index=True, max_length=5000, null=True),
        ),
    ]
