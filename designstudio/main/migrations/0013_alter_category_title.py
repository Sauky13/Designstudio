# Generated by Django 4.2.7 on 2023-11-30 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_application_completed_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(help_text='Введите название категории', max_length=50, unique=True),
        ),
    ]