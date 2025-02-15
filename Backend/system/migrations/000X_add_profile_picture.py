from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        # ...existing code...
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(upload_to='profile_pictures/', null=True, blank=True),
        ),
    ]
