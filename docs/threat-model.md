# Threat model

**Asset:** user records (id, username, email, role) served by the lab API.

**Actors:** `user` (alice), `manager` (bob), `admin`. Authentication uses fixed bearer
tokens. This is a lab shortcut, not a design to copy.

| Threat | Where | Control in the secure app |
|---|---|---|
| BOLA: a user reads another user's record | `GET /users/{id}` | Role `user` may only request its own id |
| BFLA: a non-admin calls an admin function | `GET /admin/users` | `read_all` permission required |
| Missing authentication | all except `/`, `/health` | 401 when the header or token is missing |

**Out of scope:** token theft, injection, rate limiting, mass assignment, anything on
the network layer.

**Lab switch:** `LAB_VULNERABLE=1` removes the first two controls so the scanner has
something to find.
