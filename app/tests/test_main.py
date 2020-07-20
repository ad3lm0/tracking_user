from flask import Flask
import json

alias_good_dict = {"newUserId": "65t241s", "originalUserId": "abc", "timestampUTC": 1}
alias_bad_dict = {"newUserId": 123, "originalUserId": "abc", "timestampUTC": 1}
profile_good_dict = {
    "userId": "hueBRBR",
    "attributes": {"name": "fulano"},
    "timestampUTC": 0,
}

track_good_dict = {
    "userId": "huehueBRBR",
    "events": [
        {
            "eventName": "meme",
            "metadata": {"something": "otherthing"},
            "timestampUTC": 0,
        },
    ],
}

track_bad_dict = {
    "userId": "huehueBRBR",
    "events": [
        {"eventName": 1, "metadata": {"something": "otherthing"}, "timestampUTC": 0,},
    ],
}


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200


def test_profile(client):
    response = client.post(
        "/profile/", data=json.dumps(profile_good_dict), content_type="application/json"
    )

    assert response.status_code == 200


def test_profile_fail(client):
    response = client.post(
        "/profile/", data=json.dumps(track_good_dict), content_type="application/json"
    )

    assert response.status_code == 400


def test_track(client):
    response = client.post(
        "/track/", data=json.dumps(track_good_dict), content_type="application/json"
    )

    assert response.status_code == 200


def test_track_wrong_field1(client):
    response = client.post(
        "/track/",
        data=json.dumps({"user": "huebr", "events": "[]"}),
        content_type="application/json",
    )

    assert response.status_code == 500


def test_track_wrong_field2(client):
    response = client.post(
        "/track/",
        data=json.dumps({"userId": "huebr", "event": "[]"}),
        content_type="application/json",
    )

    assert response.status_code == 500


def test_alias(client):
    response = client.post(
        "/alias/", data=json.dumps(alias_good_dict), content_type="application/json"
    )

    assert response.status_code == 200


def test_alias_fail(client):
    response = client.post(
        "/alias/", data=json.dumps(track_good_dict), content_type="application/json"
    )

    assert response.status_code == 400


def test_alias_bad_data(client):
    response = client.post(
        "/alias/", data=json.dumps(track_good_dict), content_type="application/json"
    )

    assert response.status_code == 400
