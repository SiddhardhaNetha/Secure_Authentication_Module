import json
from auth.hasher import hash_password, verify_password

USERS_FILE = "auth/users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = {"password": hash_password(password)}
    save_users(users)
    return True, "Account created"

def verify_user(username, password):
    users = load_users()
    if username in users and verify_password(password, users[username]["password"]):
        return True
    return False
