from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FIOValidator(validators.RegexValidator):
    regex = r"[а-яёА-ЯЁ-]+\s+[а-яёА-ЯЁ-]+(?:\s+[а-яёА-ЯЁ-]+)?"
    message = _(
        "Введите действительное имя-отчество. Это значение может содержать только буквы, дефис и пробелы."
    )
    flags = 0