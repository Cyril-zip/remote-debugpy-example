import json
import pytest
from datetime import datetime as dt
from app.api import crud


def get_current_datetime():
    return dt.now().strftime("%Y-%m-%d %H:%M")


def test_create_note(test_app, monkeypatch):
    payloads = {
        "request": {
            "title": "something",
            "description": "something else",
            "completed": False,
            "created_date": get_current_datetime()
        },
        "response": {
            "id": 1,
            "title": "something",
            "description": "something else",
            "completed": False,
            "created_date": get_current_datetime()
        }
    }

    test_request_payload = payloads["request"]

    test_response_payload = payloads["response"]

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notes/", data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "test_id, test_payload, expected_status",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar", "created_date": get_current_datetime(), "completed": True}, 201],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422]
    ]
)
def test_create_note_invalid(test_app, monkeypatch, test_id, test_payload, expected_status):
    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notes/", data=json.dumps(test_payload))
    assert response.status_code == expected_status


# These tests should be run in order
def test_read_note(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1, "completed": False,
                 "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/notes/0/")
    assert response.status_code == 422


def read_all_notes(test_app, monkeypatch):
    test_data = [{"title": "something", "description": "something else", "id": 1, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")},
                 {"title": "something", "description": "something else", "id": 2, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar", "created_date": dt.now().strftime("%Y-%m-%d %H:%M"),
               "completed": True}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}/", data=json.dumps(payload), )
    assert response.status_code == status_code


# Test for DELETE route
def test_remove_note_200(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1, "completed": False,
                 "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}

    async def mock_get(id):
        return test_data

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "get", mock_get)
    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/notes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/notes/0/")
    assert response.status_code == 422


def test_remove_note_invalid_id(test_app, monkeypatch):
    response = test_app.delete("/notes/one/")
    assert response.status_code == 422


def test_read_note_by_title(test_app, monkeypatch):
    test_data = [{"title": "something", "description": "something else", "id": 1, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}]

    async def mock_get_by_title(title):
        return test_data

    monkeypatch.setattr(crud, "get_by_title", mock_get_by_title)

    response = test_app.get("/notes/title/something/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_all_completed_notes(test_app, monkeypatch):
    test_data = [{"title": "something", "description": "something else", "id": 1, "completed": True,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")},
                 {"title": "something", "description": "something else", "id": 2, "completed": True,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}]

    async def mock_get_completed():
        return test_data

    monkeypatch.setattr(crud, "get_completed", mock_get_completed)

    response = test_app.get("/notes/completed/{completed}")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_all_not_completed_notes(test_app, monkeypatch):
    test_data = [{"title": "Test", "description": "something else", "id": 1, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")},
                 {"title": "something", "description": "something else", "id": 2, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}]

    async def mock_get_not_completed():
        return test_data

    monkeypatch.setattr(crud, "get_not_completed", mock_get_not_completed)

    response = test_app.get("/notes/not_completed/{not_completed}")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_by_description(test_app, monkeypatch):
    test_data = [{"title": "something", "description": "something else", "id": 1, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}]

    async def mock_get_by_description(description):
        return test_data

    monkeypatch.setattr(crud, "get_by_description", mock_get_by_description)

    response = test_app.get("/notes/description/something else/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_by_date(test_app, monkeypatch):
    test_data = [{"title": "something", "description": "something else", "id": 1, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}]

    async def mock_get_by_date(created_date):
        return test_data

    monkeypatch.setattr(crud, "get_by_date", mock_get_by_date)

    response = test_app.get("/notes/date/2021-06-17 18:00/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_by_date_invalid(test_app, monkeypatch):
    test_data = [{"title": "something", "description": "something else", "id": 1, "completed": False,
                  "created_date": dt.now().strftime("%Y-%m-%d %H:%M")}]

    async def mock_get_by_date(created_date):
        return test_data

    monkeypatch.setattr(crud, "get_by_date", mock_get_by_date)

    response = test_app.get("/notes/date/2021-06-17 18:00:00/")
    assert response.status_code == 200

