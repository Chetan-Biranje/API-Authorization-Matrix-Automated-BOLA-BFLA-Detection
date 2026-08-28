from app.auth.authentication import User


ROLE_PERMISSIONS = {
    "user": {
        "read_own",
    },
    "manager": {
        "read_own",
        "read_team",
    },
    "admin": {
        "read_own",
        "read_team",
        "read_all",
        "delete_all",
    },
}


def has_permission(user: User, permission: str) -> bool:
    permissions = ROLE_PERMISSIONS.get(user.role, set())

    return permission in permissions


def require_permission(user: User, permission: str) -> None:
    if not has_permission(user, permission):
        raise PermissionError(
            f"Role '{user.role}' lacks permission '{permission}'"
        )
