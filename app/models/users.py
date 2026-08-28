from dataclasses import dataclass


@dataclass
class UserRecord:
    id: int
    username: str
    email: str
    role: str


USER_RECORDS = {
    1: UserRecord(
        id=1,
        username="alice",
        email="alice@example.local",
        role="user",
    ),
    2: UserRecord(
        id=2,
        username="bob",
        email="bob@example.local",
        role="manager",
    ),
    3: UserRecord(
        id=3,
        username="admin",
        email="admin@example.local",
        role="admin",
    ),
}
