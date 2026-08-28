from dataclasses import dataclass


@dataclass
class AuthorizationResult:
    role: str
    method: str
    endpoint: str
    expected: str
    observed: str
    finding: str


def analyze(
    role: str,
    method: str,
    endpoint: str,
    expected: str,
    status_code: int,
) -> AuthorizationResult:

    if status_code in (401, 403):
        observed = "DENY"
    elif 200 <= status_code < 300:
        observed = "ALLOW"
    else:
        observed = f"HTTP_{status_code}"

    finding = "NONE"

    if expected == "DENY" and observed == "ALLOW":
        finding = "BFLA"

    elif expected == "OWN_ONLY" and observed == "ALLOW":
        finding = "BOLA"

    return AuthorizationResult(
        role=role,
        method=method,
        endpoint=endpoint,
        expected=expected,
        observed=observed,
        finding=finding,
    )


if __name__ == "__main__":
    result = analyze(
        role="user",
        method="GET",
        endpoint="/users/{user_id}",
        expected="OWN_ONLY",
        status_code=200,
    )

    print(result)

