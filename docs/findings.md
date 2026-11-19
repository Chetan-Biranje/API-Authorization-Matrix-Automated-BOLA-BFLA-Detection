# Findings

Findings in the lab app are seeded on purpose and only appear with `LAB_VULNERABLE=1`.

| ID | Type | Endpoint | Role | Expected | Observed |
|---|---|---|---|---|---|
| LAB-001 | BOLA | `GET /users/{id}` (another user) | user | DENY | ALLOW |
| LAB-002 | BFLA | `GET /admin/users` | user | DENY | ALLOW |
| LAB-003 | BFLA | `GET /admin/users` | manager | DENY | ALLOW |

Fix for LAB-001: compare the caller's id with the requested id before returning the object.
Fix for LAB-002 and LAB-003: require the `read_all` permission on the route.
Both fixes are the default behavior of the app.
