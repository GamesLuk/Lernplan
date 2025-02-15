from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        # ...existing code...
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='profile_picture_url',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
    ]
