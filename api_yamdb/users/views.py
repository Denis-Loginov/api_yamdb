# from django.shortcuts import render

from django.core.mail import send_mail


app_name = 'users'


def send_mail(request, email):
    to_email = request.email
    send_mail(
        'Регистрация YaMDB',
        'Ваш код подтверждения для регистрации на YaMDB: ',
        'from@example.com',  # Это поле "От кого"
        to_email,  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False
    )
