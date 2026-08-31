from dataclasses import dataclass

import httpx


@dataclass
class AuthorizationResult:
    role: str
    method: str
    endpoint: str
    object_context: str | None
    expected: str
    observed: str
    finding: str
    status_code: int


TOKENS = {
    "user": "user-token",
    "manager": "manager-token",
    "admin": "admin-token",
}


OBJECTS = {
    "user": {
        "own": 1,
        "another": 2,
    },
    "manager": {
        "own": 2,
        "another": 1,
    },
    "admin": {
        "own": 3,
        "another": 1,
    },
}


def classify_observed(status_code: int) -> str:
    if status_code in (401, 403):
        return "DENY"

    if 200 <= status_code < 300:
        return "ALLOW"

    return f"HTTP_{status_code}"


def analyze(
    role: str,
    method: str,
    endpoint: str,
    expected: str,
    status_code: int,
    object_context: str | None = None,
) -> AuthorizationResult:

    observed = classify_observed(status_code)

    finding = "NONE"

    if expected == "DENY" and observed == "ALLOW":
        finding = "BFLA"

    elif expected == "OWN_ONLY":
        if object_context == "own" and observed != "ALLOW":
            finding = "AUTHORIZATION_MISMATCH"

        elif object_context == "another" and observed == "ALLOW":
            finding = "BOLA"

    elif expected == "ALLOW" and observed == "DENY":
        finding = "AUTHORIZATION_MISMATCH"

    return AuthorizationResult(
        role=role,
        method=method,
        endpoint=endpoint,
        object_context=object_context,
        expected=expected,
        observed=observed,
        finding=finding,
        status_code=status_code,
    )


def resolve_endpoint(
    endpoint: str,
    role: str,
    object_context: str | None,
) -> str:

    if "{user_id}" not in endpoint:
        return endpoint

    if object_context == "own":
        user_id = OBJECTS[role]["own"]

    else:
        user_id = OBJECTS[role]["another"]

    return endpoint.replace(
        "{user_id}",
        str(user_id),
    )


def request_endpoint(
    base_url: str,
    role: str,
    method: str,
    endpoint: str,
) -> int:

    token = TOKENS[role]

    response = httpx.request(
        method=method,
        url=f"{base_url.rstrip('/')}{endpoint}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=5.0,
    )

    return response.status_code
