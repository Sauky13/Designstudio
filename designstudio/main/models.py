from audioop import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal
from .validators import FIOValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

user_registrated = Signal('instance')


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    full_name_validator = FIOValidator()
    full_name = models.CharField(max_length=255, verbose_name='ФИО', validators=[full_name_validator],
                                 help_text='только кириллические буквы, дефис и пробелы;')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, help_text='Введите название категории')

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class StatusApplication(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status


def validate_image_extension(value):
    """
    Функция валидации изображения
    """
    allowed_extensions = ['png', 'jpg', 'jpeg', 'bmp']
    ext = value.name.split('.')[-1].lower()
    if not ext in allowed_extensions:
        raise ValidationError(_('Не правильный формат изображеня! Поддерживаемый формат: jpg, jpeg, png, bmp.'))


class Application(models.Model):
    STATUS_CHOICES = [
        ('A', 'Новая'),
        ('B', 'Принято в работу'),
        ('C', 'Выполнено'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(help_text='Описание заявки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', validators=[validate_image_extension], max_length=2 * 1024 * 1024)
    completed_image = models.ImageField(upload_to='completed_images', null=True, blank=True,
                                        validators=[validate_image_extension])
    time_mark = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('application', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def get_status_display(self):
        return dict(Application.STATUS_CHOICES).get(self.status, "Неизвестный статус")
