from scanner.analyzer import analyze, classify_observed


def result(expected, status, context=None, endpoint="/users/{user_id}"):
    return analyze(
        role="user",
        method="GET",
        endpoint=endpoint,
        expected=expected,
        status_code=status,
        object_context=context,
    )


def test_status_codes_map_to_allow_or_deny():
    assert classify_observed(200) == "ALLOW"
    assert classify_observed(401) == "DENY"
    assert classify_observed(403) == "DENY"
    assert classify_observed(500) == "HTTP_500"


def test_another_users_object_allowed_is_bola():
    assert result("DENY", 200, "another").finding == "BOLA"


def test_own_only_endpoint_allowing_another_object_is_bola():
    assert result("OWN_ONLY", 200, "another").finding == "BOLA"


def test_forbidden_function_allowed_is_bfla():
    assert result("DENY", 200, None, "/admin/users").finding == "BFLA"


def test_correct_deny_is_not_a_finding():
    assert result("DENY", 403, "another").finding == "NONE"


def test_legitimate_access_blocked_is_mismatch():
    assert result("ALLOW", 403, None, "/me").finding == "AUTHORIZATION_MISMATCH"
