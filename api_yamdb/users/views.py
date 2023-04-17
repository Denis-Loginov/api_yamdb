# from django.shortcuts import render
import datetime
from django.core.mail import send_mail

from datetime import date

from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36


app_name = 'users'


def make_token(self, user):
    return self._make_token_with_timestamp(user, self._num_days(self._today()))


def send_mail(request):
    if request.method == 'POST':
        to_email = request.POST['email']
    token = make_token()
    send_mail(
        'Регистрация YaMDB',
        f'Ваш код подтверждения для регистрации на YaMDB:{token}',
        'from@example.com',  # Это поле "От кого"
        to_email,  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False
    )
