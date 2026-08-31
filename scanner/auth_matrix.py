import json
from dataclasses import dataclass


@dataclass
class AuthorizationCase:
    role: str
    method: str
    endpoint: str
    expected: str
    object_context: str | None = None


def load_policy(path: str = "roles.json") -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def resource_from_endpoint(endpoint: str) -> str:
    if endpoint.startswith("/admin/"):
        return "admin"

    if endpoint.startswith("/users"):
        return "users"

    if endpoint.startswith("/documents"):
        return "documents"

    return "unknown"


def expected_access(
    role: str,
    endpoint: str,
    policy: dict,
) -> tuple[str, str | None]:

    resource = resource_from_endpoint(endpoint)

    permissions = policy.get(role, {}).get(resource, [])

    if "all" in permissions:
        return "ALLOW", "all"

    if "own" in permissions:
        return "OWN_ONLY", "own"

    if "team" in permissions:
        return "TEAM_ONLY", "team"

    return "DENY", None


def generate_cases(
    endpoints: list[tuple[str, str]],
    policy: dict,
) -> list[AuthorizationCase]:

    cases = []

    for role in policy:
        for method, endpoint in endpoints:

            expected, context = expected_access(
                role,
                endpoint,
                policy,
            )

            if expected == "OWN_ONLY":
                cases.append(
                    AuthorizationCase(
                        role=role,
                        method=method,
                        endpoint=endpoint,
                        expected="OWN_ONLY",
                        object_context="own",
                    )
                )

                cases.append(
                    AuthorizationCase(
                        role=role,
                        method=method,
                        endpoint=endpoint,
                        expected="DENY",
                        object_context="another",
                    )
                )

            else:
                cases.append(
                    AuthorizationCase(
                        role=role,
                        method=method,
                        endpoint=endpoint,
                        expected=expected,
                        object_context=context,
                    )
                )

    return cases


if __name__ == "__main__":

    policy = load_policy()

    endpoints = [
        ("GET", "/me"),
        ("GET", "/users/{user_id}"),
        ("GET", "/admin/users"),
    ]

    cases = generate_cases(endpoints, policy)

    print(
        f"{'ROLE':<10}"
        f"{'METHOD':<8}"
        f"{'ENDPOINT':<25}"
        f"{'EXPECTED':<12}"
        f"OBJECT"
    )

    print("-" * 75)

    for case in cases:
        print(
            f"{case.role:<10}"
            f"{case.method:<8}"
            f"{case.endpoint:<25}"
            f"{case.expected:<12}"
            f"{case.object_context or '-'}"
        )
