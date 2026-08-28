from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    role: str


USERS = {
    "user-token": User(
        id=1,
        username="alice",
        role="user",
    ),
    "manager-token": User(
        id=2,
        username="bob",
        role="manager",
    ),
    "admin-token": User(
        id=3,
        username="admin",
        role="admin",
    ),
}


def get_current_user(token: str) -> User:
    user = USERS.get(token)

    if user is None:
        raise ValueError("Invalid authentication token")

    return user
