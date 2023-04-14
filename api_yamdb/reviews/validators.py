from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    message = 'Год создания произведения не может быть больше текущего!'
    if year > datetime.now().year:
        raise ValidationError(message)
