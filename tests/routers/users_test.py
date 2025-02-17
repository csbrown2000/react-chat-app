from fastapi.testclient import TestClient
import datetime
from backend.main import app

def test_get_all_users():
	client = TestClient(app)
	response = client.get("/users")
	assert response.status_code == 200

	meta = response.json()["meta"]
	users = response.json()["users"]

	assert meta["count"] == len(users)
	assert  users == sorted(users, key=lambda user: user["id"])

def test_get_user_ripley():
	expected = {
		"user": {
			"id": "ripley",
			"created_at": "2008-06-08T14:32:08"
		}
	}

	client = TestClient(app)
	response = client.get("/users/ripley")
	assert response.status_code == 200

	user = response.json()

	assert user == expected

def test_get_user_doolittle():
	expected = {
		"user": {
			"id": "doolittle",
			"created_at": "2003-05-21T06:14:11"
		}
	}

	client = TestClient(app)
	response = client.get("/users/doolittle")
	assert response.status_code == 200

	user = response.json()

	assert user == expected

def test_create_user():
	new_user = {
		"id": "testuser1"
	}

	client = TestClient(app)
	response = client.post("/users", json=new_user)

	assert response.status_code == 200

	data = response.json()
	user = data["user"]
	assert new_user["id"] == user["id"]

	response = client.get("/users/testuser1")

	assert response.status_code == 200

	data = response.json()
	user = data["user"]
	assert new_user["id"] == user["id"]

def test_get_doolittle_chats():
	client = TestClient(app)
	response = client.get("/users/doolittle/chats")

	assert response.status_code == 200

	meta = response.json()["meta"]
	chats = response.json()["chats"]

	assert meta["count"] == len(chats)
	assert  chats == sorted(chats, key=lambda chat: chat["name"])

def test_get_sarah_chats():
	client = TestClient(app)
	response = client.get("/users/sarah/chats")

	assert response.status_code == 200

	meta = response.json()["meta"]
	chats = response.json()["chats"]

	assert meta["count"] == len(chats)
	assert  chats == sorted(chats, key=lambda chat: chat["name"])

def test_exception_on_bad_user_id():
	client = TestClient(app)
	response = client.get("/users/5eutygouih2345")
	assert response.status_code == 404

def test_create_user_juniper():
	test_client = TestClient(app)
	"""Test response for `POST /users` with id: \"juniper\"."""
	lower_bound = datetime.datetime.now()
	upper_bound = lower_bound + datetime.timedelta(seconds=5)

	response = test_client.post("/users", json={"id": "juniper"})
	assert response.status_code == 200

	data = response.json()
	assert isinstance(data, dict)
	assert "user" in data
	user = data["user"]
	assert isinstance(user, dict)
	assert set(user.keys()) == {"id", "created_at"}
	assert user["id"] == "juniper"

	# test that created_at datetime is no more between 0 and 5 seconds
	# after the http request
	created_at = datetime.datetime.fromisoformat(user["created_at"])
	assert lower_bound <= created_at <= upper_bound
	# assert datetime.datetime(2024, 1, 30, 2, 45, 4, 523868) <= datetime.datetime(2024, 1, 30, 0, 0)

def test_create_user_invalid_id():
	"""Test response for `POST /users` with id: \"ripley\"."""
	test_client = TestClient(app)
	response = test_client.post("/users", json={"id": "ripley"})
	assert response.status_code == 422