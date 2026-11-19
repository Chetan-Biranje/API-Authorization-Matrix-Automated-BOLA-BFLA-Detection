# Methodology

1. **Policy.** `roles.json` lists, for each role, which object scopes it may reach
   (`own`, `team`, `all`) on `users`, `documents` and `admin`.
2. **Case generation.** `scanner/auth_matrix.py` turns the policy and an endpoint list
   into cases: role, method, endpoint, object context (`own`, `another`, `all`) and the
   expected outcome (`ALLOW`, `DENY`, `OWN_ONLY`).
3. **Execution.** `scanner/analyzer.py` resolves `{user_id}` to a real id for the role,
   sends the request with that role's token, and maps the status code to `ALLOW`
   (2xx) or `DENY` (401/403).
4. **Differential analysis.** Expected and observed outcomes are compared:

   | Expected | Observed | Context | Finding |
   |---|---|---|---|
   | DENY / OWN_ONLY | ALLOW | another user's object | BOLA |
   | DENY | ALLOW | whole function | BFLA |
   | ALLOW / own object | DENY | any | AUTHORIZATION_MISMATCH |

5. **Regression.** The same cases run in CI. The secure app must give 0 findings and
   the vulnerable mode must give exactly 3, so a change that breaks either the app or
   the scanner fails the build.

## Limits

* Status codes are the only signal. A 200 that returns an empty body still counts as ALLOW.
* Only GET endpoints are covered so far.
* Three roles and three endpoints is a small sample.
