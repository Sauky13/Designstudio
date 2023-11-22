# Generated by Django 4.2.6 on 2023-11-20 08:46

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_application_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='completed_image',
            field=models.ImageField(blank=True, null=True, upload_to='completed_images', validators=[main.models.validate_image_extension]),
        ),
    ]
