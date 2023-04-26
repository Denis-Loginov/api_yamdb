from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet, RegisterView,
    ReviewViewSet, TitleViewSet,
    TokenView, UserViewSet
)

router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='user')


auth_urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('token/', TokenView.as_view()),

]
urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(router.urls)),
]
