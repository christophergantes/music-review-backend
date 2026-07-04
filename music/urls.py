from django.urls import path
from rest_framework import routers

from .views import AlbumDetailView, AlbumSearchView, AlbumView

router = routers.SimpleRouter()
router.register(r"album", AlbumView)

urlpatterns = [
    path("album/search/", AlbumSearchView.as_view()),
    path("album/external/<str:mbid>/", AlbumDetailView.as_view()),
]
urlpatterns += router.urls
