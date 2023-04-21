from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet, ReviewViewSet, RegisterView,
    UserViewSet, MeView, TokenView)


router = DefaultRouter()

app_name = 'api'

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register(r'auth/signup', RegisterView, basename='auth')
router.register(r'auth/token', TokenView, basename='token')
router.register(r'user', UserViewSet, basename='user')
router.register(r'user/me', MeView, basename='userme')


urlpatterns = [
    path('v1/', include(router.urls)),
]
