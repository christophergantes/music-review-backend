from rest_framework.serializers import ModelSerializer

from music.models import Album, Artist


class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "mbid", "name"]


class AlbumSerializer(ModelSerializer):
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Album
        fields = ["id", "mbid", "title", "artist", "release_date", "cover_art_url"]
