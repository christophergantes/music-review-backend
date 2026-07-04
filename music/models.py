from django.db import models


class Artist(models.Model):
    mbid = models.CharField(max_length=36, unique=True, db_index=True)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    mbid = models.CharField(max_length=36, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField(null=True, blank=True)
    cover_art_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-release_date"]

    def __str__(self):
        return f"{self.title} - {self.artist}"
