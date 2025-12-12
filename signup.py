# auth/signup.py
import json
from auth.hasher import hash_password

USERS_FILE = "auth/users.json"

def register_user(username, password):
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except:
        users = {}

    if username in users:
        return False, "Username already exists!"

    users[username] = {
        "password": hash_password(password)
    }

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    return True, "Account created!"
