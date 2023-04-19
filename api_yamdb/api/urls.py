from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
	CategoryViewSet, CommentViewSet, 
	GenreViewSet, ReviewViewSet, 
	TitleViewSet
)


app_name = 'api'

router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
