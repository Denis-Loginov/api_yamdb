from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.send_mail, name='send_mail'),
]
