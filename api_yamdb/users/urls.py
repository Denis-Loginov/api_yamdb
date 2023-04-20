from django.urls import path
from .views import (
    AuthCreateTokenViewSet, AuthViewSet, UserViewSet, UserMeViewSet
)


urlpatterns = [
    path('', UserViewSet),
    path('me/', UserMeViewSet),
    path('signup/', AuthViewSet),
    path('token/', AuthCreateTokenViewSet),
]
