import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from music.models import Album
from music.serializers import AlbumSerializer
from music.services.musicbrainz import get_or_create_album, search_release_groups


class AlbumView(ReadOnlyModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.prefetch_related("artists")


class AlbumSearchView(APIView):
    def get(self, request):
        title = request.query_params.get("title")

        if not title:
            return Response(
                {"error": "Title required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            data = search_release_groups(title)
        except requests.RequestException:
            return Response(
                {"error": "MusicBrainz API could not be reached"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(data)


class AlbumDetailView(APIView):
    def get(self, request, mbid):
        try:
            album = get_or_create_album(mbid)
        except requests.RequestException:
            return Response(
                {"error": "MusicBrainz API could not be reached"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except ValueError:
            return Response(
                {"error": "Artist creation failed"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        serializer = AlbumSerializer(album)
        return Response(serializer.data)
