import json

from music.services.musicbrainz import (
    get_artist_details,
    get_release_group_details,
    get_release_groups,
)


def test_mb():
    results = get_release_groups("In Rainbows")
    # print(json.dumps(results, indent=2))

    mbid = results["release-groups"][0]["id"]

    result = get_release_group_details(mbid)
    print(json.dumps(result, indent=2))

    mbid = result["artist-credit"][0]["artist"]["id"]

    result = get_artist_details(mbid)
    print(json.dumps(result, indent=2))

    assert True
