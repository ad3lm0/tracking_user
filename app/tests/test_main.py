from flask import Flask
import json

good_event = {
    "eventName": "meme",
    "metadata": {"something": "otherthing"},
    "timestampUTC": 0,
}

bad_event = {
    "event": "meme",
    "metadata": {"something": "otherthing"},
    "timestampUTC": 0,
}

good_track = {
    "userId": "huehueBRBR",
    "events": [good_event],
}


bad_track = {
    "userId": "huehueBRBR",
    "events": [bad_event],
}


def test_pass_helloWorld(client):
    response = client.get("/")
    assert response.status_code == 200


def test_pass_profile(client):
    response = client.post(
        "/profile/",
        data=json.dumps(
            {"userId": "hueBRBR", "attributes": {"name": "fulano"}, "timestampUTC": 0,}
        ),
        content_type="application/json",
    )

    assert response.status_code == 200


def test_fail_profile_fieldName(client):
    response = client.post(
        "/profile/",
        data=json.dumps(
            {"user": "hueBRBR", "attributes": {"name": "fulano"}, "timestampUTC": 0,}
        ),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_profile_attributeError(client):
    response = client.post(
        "/profile/",
        data=json.dumps({"userId": "hueBRBR", "attributes": "", "timestampUTC": "0",}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_pass_track(client):
    response = client.post(
        "/track/", data=json.dumps(good_track), content_type="application/json"
    )

    assert response.status_code == 200


def test_fail_track_fieldName(client):
    response = client.post(
        "/track/",
        data=json.dumps({"user": "huebr", "events": "[]"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_track_nestedEventFieldName(client):
    response = client.post(
        "/track/", data=json.dumps(bad_track), content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_track_wrongFieldName(client):
    response = client.post(
        "/track/",
        data=json.dumps({"userId": "huebr", "eve": "[]"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_track_emptyEvent(client):
    response = client.post(
        "/track/",
        data=json.dumps({"userId": "huebr", "events": "[]"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_pass_alias(client):
    response = client.post(
        "/alias/",
        data=json.dumps({"newUserId": 123, "originalUserId": "abc", "timestampUTC": 1}),
        content_type="application/json",
    )

    assert response.status_code == 200


def test_fail_alias_fieldName(client):
    response = client.post(
        "/alias/",
        data=json.dumps({"userId": 123, "originalUserId": "abc", "timestampUTC": 1}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_alias_badData(client):
    response = client.post(
        "/alias/",
        data=json.dumps({"newUserId": 123, "originalUserId": "abc"}),
        content_type="application/json",
    )

    assert response.status_code == 400
