from dataclasses import dataclass


@dataclass
class AuthorizationCase:
    role: str
    endpoint: str
    method: str
    expected: str
    reason: str


AUTHORIZATION_MATRIX = [
    AuthorizationCase(
        role="user",
        endpoint="/me",
        method="GET",
        expected="ALLOW",
        reason="Authenticated user can access own profile",
    ),
    AuthorizationCase(
        role="user",
        endpoint="/users/{user_id}",
        method="GET",
        expected="OWN_ONLY",
        reason="User can access only their own object",
    ),
    AuthorizationCase(
        role="user",
        endpoint="/admin/users",
        method="GET",
        expected="DENY",
        reason="Administrative function requires admin permission",
    ),
    AuthorizationCase(
        role="manager",
        endpoint="/me",
        method="GET",
        expected="ALLOW",
        reason="Authenticated manager can access own profile",
    ),
    AuthorizationCase(
        role="manager",
        endpoint="/users/{user_id}",
        method="GET",
        expected="ALL",
        reason="Manager can access user records in this lab",
    ),
    AuthorizationCase(
        role="manager",
        endpoint="/admin/users",
        method="GET",
        expected="DENY",
        reason="Administrative function requires admin permission",
    ),
    AuthorizationCase(
        role="admin",
        endpoint="/me",
        method="GET",
        expected="ALLOW",
        reason="Authenticated admin can access own profile",
    ),
    AuthorizationCase(
        role="admin",
        endpoint="/users/{user_id}",
        method="GET",
        expected="ALL",
        reason="Admin can access all user objects",
    ),
    AuthorizationCase(
        role="admin",
        endpoint="/admin/users",
        method="GET",
        expected="ALLOW",
        reason="Admin has administrative permission",
    ),
]


def build_matrix() -> list[AuthorizationCase]:
    """Return the expected authorization policy."""
    return AUTHORIZATION_MATRIX


def print_matrix(cases: list[AuthorizationCase]) -> None:
    print(
        f"{'ROLE':10} "
        f"{'METHOD':7} "
        f"{'ENDPOINT':22} "
        f"{'EXPECTED':12}"
    )
    print("-" * 60)

    for case in cases:
        print(
            f"{case.role:10} "
            f"{case.method:7} "
            f"{case.endpoint:22} "
            f"{case.expected:12}"
        )


if __name__ == "__main__":
    matrix = build_matrix()
    print_matrix(matrix)
