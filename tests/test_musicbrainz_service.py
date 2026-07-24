from unittest.mock import patch

import pytest
import responses
from music.services.musicbrainz import search_release_groups

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/release-group/"

@pytest.fixture(autouse=True)
def no_sleep():
    with patch("music.services.musicbrainz.time.sleep"):
        yield

@pytest.fixture
def mock_musicbrainz_response():
    return {
        "count": 3504,
        "created": "2026-07-08T22:41:25.592Z",
        "offset": 0,
        "release-groups": [
            {
                "artist-credit": [
                    {
                        "artist": {
                            "aliases": [
                                {
                                    "begin-date": None,
                                    "end-date": None,
                                    "locale": None,
                                    "name": "Lemâitre",
                                    "primary": None,
                                    "sort-name": "Lemâitre",
                                    "type": "Artist name",
                                    "type-id": "894afba6-2816-3c24-8072-eadb66bd04bc",
                                }
                            ],
                            "disambiguation": "Oslo‐based, Norwegian indie‐electronica duo",
                            "id": "7bc012a7-c5cc-4e7a-9ca6-15db02bbcde4",
                            "name": "Lemaitre",
                            "sort-name": "Lemaitre",
                        },
                        "joinphrase": " & ",
                        "name": "Lemaitre",
                    },
                    {
                        "artist": {
                            "aliases": [
                                {
                                    "begin-date": None,
                                    "end-date": None,
                                    "locale": None,
                                    "name": "Rebecca Sophia Moe",
                                    "primary": None,
                                    "sort-name": "Moe, Rebecca Sophia",
                                    "type": "Legal name",
                                    "type-id": "d4dcd0c0-b341-3612-a332-c0ce797b25cf",
                                }
                            ],
                            "id": "481ae6c0-d3cc-4ae7-9995-5850fbf15479",
                            "name": "RebMoe",
                            "sort-name": "RebMoe",
                        },
                        "name": "RebMoe",
                    },
                ],
                "artist-credit-id": "cafc529d-3603-3705-956c-5926a8e2ad40",
                "count": 1,
                "first-release-date": "2021-08-20",
                "id": "a5e4bd1a-63c9-4dfc-9e63-ed0c3dc049be",
                "primary-type": "Single",
                "primary-type-id": "d6038452-8ee0-3f68-affc-2de9a1ede0b9",
                "releases": [
                    {
                        "id": "de3726da-05b8-4c1a-a19d-1bf53b7889ea",
                        "status": "Official",
                        "status-id": "4e304316-386d-3409-af2e-78857eec5cfe",
                        "title": "Ok Computer",
                    }
                ],
                "score": 100,
                "title": "Ok Computer",
                "type-id": "d6038452-8ee0-3f68-affc-2de9a1ede0b9",
            },
            {
                "artist-credit": [
                    {
                        "artist": {
                            "aliases": [
                                {
                                    "begin-date": None,
                                    "end-date": None,
                                    "locale": None,
                                    "name": "Radiohead & Thom Yorke",
                                    "primary": None,
                                    "sort-name": "Radiohead & Thom Yorke",
                                    "type": "Search hint",
                                    "type-id": "1937e404-b981-3cb7-8151-4c86ebfc8d8e",
                                },
                                {
                                    "begin-date": None,
                                    "end-date": None,
                                    "locale": None,
                                    "name": "Radio Head",
                                    "primary": None,
                                    "sort-name": "Radio Head",
                                    "type": "Search hint",
                                    "type-id": "1937e404-b981-3cb7-8151-4c86ebfc8d8e",
                                },
                            ],
                            "id": "a74b1b7f-71a5-4011-9441-d0b5e4122711",
                            "name": "Radiohead",
                            "sort-name": "Radiohead",
                        },
                        "name": "Radiohead",
                    }
                ],
                "artist-credit-id": "021661c1-84c5-30d7-9bb2-f0766affb734",
                "count": 38,
                "first-release-date": "1997-05-21",
                "id": "b1392450-e666-3926-a536-22c65f834433",
                "primary-type": "Album",
                "primary-type-id": "f529b476-6e62-324f-b0aa-1f3e33d313fc",
                "releases": [
                    {
                        "id": "8e2b5322-f9a6-4ab7-b3f4-f65e7ddbc9e4",
                        "status": "Official",
                        "status-id": "4e304316-386d-3409-af2e-78857eec5cfe",
                        "title": "OK Computer: OKNOTOK 1997 2017",
                    },
                    {
                        "id": "30702389-5c67-4438-9ea0-2351c8de0f1d",
                        "status": "Official",
                        "status-id": "4e304316-386d-3409-af2e-78857eec5cfe",
                        "title": "OK Computer",
                    },
                ],
                "score": 100,
                "tags": [
                    {"count": 13, "name": "rock"},
                    {"count": 2, "name": "electronic"},
                ],
                "title": "OK Computer",
                "type-id": "f529b476-6e62-324f-b0aa-1f3e33d313fc",
            },
        ],
    }


class TestSearchReleaseGroups:
    @responses.activate
    def test_returns_transformed_list_shape(self, mock_musicbrainz_response):
        """The service should return defined shape, not MB's raw shape."""
        responses.add(
            responses.GET, MUSICBRAINZ_URL, json=mock_musicbrainz_response, status=200
        )

        results = search_release_groups("OK Computer")

        assert isinstance(results, list)
        assert len(results) == 2
        assert results[1] == {
            "mbid": "b1392450-e666-3926-a536-22c65f834433",
            "title": "OK Computer",
            "artist":
                {
                    "mbid": "a74b1b7f-71a5-4011-9441-d0b5e4122711",
                    "name": "Radiohead",
                },
            "release_date": "1997-05-21",
        }

    @responses.activate
    def test_does_not_leak_mb_fields(self, mock_musicbrainz_response):
        """The service should not leak MB fields."""
        responses.add(responses.GET, MUSICBRAINZ_URL, json=mock_musicbrainz_response, status=200)

        results = search_release_groups("OK Computer")

        assert "count" not in results
        assert "created" not in results

        for album in results:
            assert "primary-type" not in album
            assert "type-id" not in album
            assert "count"  not in album
            assert "score" not in album
            assert "first-release-date" not in album

    @responses.activate
    def test_empty_release_groups_returns_empty_list(self):
        responses.add(
            responses.GET,
            MUSICBRAINZ_URL,
            json={"created": "...", "count": 0, "offset": 0, "release-groups": []},
            status=200,
        )

        results = search_release_groups("empty-results-asdasfa")

        assert results == []

    @responses.activate
    def test_missing_optional_fields_default_to_none(self):
        """Some release-groups omit first-release-date entirely."""
        responses.add(
            responses.GET,
            MUSICBRAINZ_URL,
            json={
                "release-groups": [
                    {
                        "id": "a5e4bd1a-63c9-4dfc-9e63-ed0c3dc049be",
                        "title": "Untitled Release",
                        "primary-type": "Single",
                        "score": 50,
                        # no "first-release-date" key
                    }
                ]
            },
            status=200,
        )

        results = search_release_groups("Untitled")

        assert results[0]["release_date"] is None

    @responses.activate
    def test_raises_on_musicbrainz_error_status(self):
        responses.add(
            responses.GET,
            MUSICBRAINZ_URL,
            json={"error": "Internal error"},
            status=500,
        )

        with pytest.raises(Exception):  # tighten to requests.HTTPError if that's what you raise_for_status with
            search_release_groups("OK Computer")

    @responses.activate
    def test_query_param_sent_to_musicbrainz(self, mock_musicbrainz_response):
        """Confirms we're actually passing the search title through."""
        responses.add(
            responses.GET,
            MUSICBRAINZ_URL,
            json=mock_musicbrainz_response,
            status=200,
        )

        search_release_groups("OK Computer")

        assert len(responses.calls) == 1
        request_url = responses.calls[0].request.url
        assert "query=OK+Computer" in request_url or "query=OK%20Computer" in request_url


class TestGetReleaseGroups:
    pass

class TestGetOrCreateAlbum:
    pass