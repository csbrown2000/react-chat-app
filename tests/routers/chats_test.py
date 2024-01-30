from fastapi.testclient import TestClient
from datetime import date
from backend.main import app

def test_get_all_chats():
	client = TestClient(app)
	response = client.get("/chats")
	assert response.status_code == 200

	meta = response.json()["meta"]
	chats = response.json()["chats"]

	assert meta["count"] == len(chats)
	assert  chats == sorted(chats, key=lambda chat: chat["name"])


def test_get_chat_by_id():
	expected = {
		"chat": {
			"id": "6215e6864e884132baa01f7f972400e2",
			"name": "skynet",
			"user_ids": [
				"sarah",
				"terminator"
			],
			"owner_id": "sarah",
			"created_at": "2023-07-08T18:46:47"
		}
	}

	client = TestClient(app)
	response = client.get("/chats/6215e6864e884132baa01f7f972400e2")
	assert response.status_code == 200

	chat = response.json()

	assert chat == expected

def test_update_chat():
	client = TestClient(app)
	# Fetch
	response = client.get("/chats/660c7a6bc1324e4488cafabc59529c93")
	assert response.status_code == 200

	chat = response.json()["chat"]
	assert chat["name"] == "terminators"

	# update
	new_name = {
		"name": "terminators!!!"
	}
	response = client.put("/chats/660c7a6bc1324e4488cafabc59529c93", json=new_name)

	assert response.status_code == 200

	updated_chat = response.json()["chat"]
	assert updated_chat["name"] == new_name

def test_exception_on_bad_chat_id():
	client = TestClient(app)
	response = client.get("/chats/5eutygouih2345")
	assert response.status_code == 404

def test_exception_on_bad_chat_id_update():
	new_name = {
		"name": "this test failed"
	}
	client = TestClient(app)
	response = client.put("/chats/reallygoodtest", json=new_name)
	assert response.status_code == 404


def test_get_messages_by_chat_id():
	client = TestClient(app)
	response = client.get("chats/6215e6864e884132baa01f7f972400e2/messages")
	assert response.status_code == 200
	meta = response.json()["meta"]
	messages = response.json()["messages"]

	assert meta["count"] == len(messages)
	assert messages == sorted(messages, key=lambda message: message["created_at"])

def test_get_users_by_chat_id():
	client = TestClient(app)
	response = client.get("chats/6215e6864e884132baa01f7f972400e2/users")
	assert response.status_code == 200
	meta = response.json()["meta"]
	users = response.json()["users"]

	assert meta["count"] == len(users)
	assert users == sorted(users, key=lambda user: user["id"])