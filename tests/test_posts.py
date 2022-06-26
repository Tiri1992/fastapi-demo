"""Tests for creating, reading, deleting posts"""


def test_get_all_posts(authorised_client):
    res = authorised_client.get("/posts/")
    print(res.json())

    assert res.status_code == 200
