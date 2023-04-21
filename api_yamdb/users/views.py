from django.core.mail import send_mail

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from users.models import User
from .tokens import get_tokens_for_user
from .tokens import PasswordResetTokenGenerator
from .serializers import UserSerializer


app_name = 'users'

chekcode = PasswordResetTokenGenerator.make_token()


def send_mail(request):
    # if request.method == 'POST':
    to_email = request.POST['email']
    send_mail(
        'Регистрация YaMDB',
        f'Ваш код подтверждения для регистрации на YaMDB:{chekcode}',
        'from@example.com',  # Это поле "От кого"
        to_email,  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(request, serializer):
        if request.user.role == 'ADMIN':
            serializer.save()


class UserMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(request, serializer):
        if request.user.role == 'USER':
            serializer.save()


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(request, serializer):
        if request.method == 'POST':
            send_mail()
            serializer.save(confirmation_code=chekcode)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return get_tokens_for_user()
