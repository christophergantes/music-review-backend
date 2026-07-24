import logging
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

from music.models import Album, Artist

load_dotenv()

MB_BASE_URL = "https://musicbrainz.org/ws/2"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
if not ADMIN_EMAIL:
    raise RuntimeError("ADMIN_EMAIL environment variable is required")
HEADERS = {"User-Agent": f"MusicReviewApp/0.1.0 ({ADMIN_EMAIL})"}


def get_request(url: str, params: dict = None):
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    logging.debug(response.url)
    response.raise_for_status()

    time.sleep(1)

    return response.json()


def _extract_primary_artist(artist_credit):
    if not artist_credit:
        return None
    credit = artist_credit[0]
    return {"name": credit["name"], "mbid": credit["artist"]["id"]}


def search_release_groups(query: str, limit: int = 5):
    url = f"{MB_BASE_URL}/release-group/"
    params = {
        "query": query,
        "limit": limit,
        "fmt": "json",
    }

    data = get_request(url, params)

    return [
        {
            "mbid": rg["id"],
            "title": rg["title"],
            "artist": _extract_primary_artist(rg.get("artist-credit", None)),
            "release_date": rg.get("first-release-date", None),
        }
        for rg in data.get("release-groups", [])
    ]


def get_release_group_details(mbid: str):
    url = f"{MB_BASE_URL}/release-group/{mbid}"
    params = {
        "inc": "artist-credits",
        "fmt": "json",
    }

    data = get_request(url, params)


    return {
        "mbid": data["id"],
        "title": data["title"],
        "artist": _extract_primary_artist(data["artist-credit"]),
        "release_date": data.get("first-release-date", None),
    }


def parse_release_date(date_str: str):
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None


def get_or_create_album(mbid: str):
    try:
        return Album.objects.get(mbid=mbid)
    except Album.DoesNotExist:
        pass

    data = get_release_group_details(mbid)

    try:
        artist_data = data["artist"]
    except (KeyError, IndexError):
        raise ValueError(f"No artist data found for release-group {mbid}")
    artist, _ = Artist.objects.get_or_create(
        mbid=artist_data["mbid"], defaults={"name": artist_data["name"]}
    )

    album = Album.objects.create(
        mbid=data["mbid"],
        title=data["title"],
        artist=artist,
        release_date=parse_release_date(data.get("release_date")),
    )

    return album
