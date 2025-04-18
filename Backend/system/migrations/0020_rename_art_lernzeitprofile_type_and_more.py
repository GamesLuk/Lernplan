# Generated by Django 5.1.5 on 2025-02-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0019_alter_studentprofile_school_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lernzeitprofile',
            old_name='art',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='lernzeitprofile',
            name='teacher_school_ID',
        ),
        migrations.AddField(
            model_name='lernzeitprofile',
            name='teacher',
            field=models.CharField(db_index=True, default=' ', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lernzeitprofile',
            name='fach',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='lernzeitprofile',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
