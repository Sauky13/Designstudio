# Generated by Django 4.2.6 on 2023-11-17 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_application'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('A', 'Новая'), ('B', 'Принято в работу'), ('C', 'Выполнено')], default='новая', max_length=100),
        ),
        migrations.AlterField(
            model_name='application',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category'),
        ),
    ]
