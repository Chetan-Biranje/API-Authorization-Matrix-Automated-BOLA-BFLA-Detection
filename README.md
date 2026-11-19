# API Authorization Research

Automated API authorization testing and research framework for detecting
Broken Object Level Authorization (BOLA) and Broken Function Level
Authorization (BFLA) in controlled environments.

## Research Objective

This project investigates whether API authorization inconsistencies can be
identified automatically by comparing an expected authorization policy against
the observed behavior of API endpoints.

The research workflow is:

OpenAPI Specification
        ↓
API Endpoint Inventory
        ↓
Authorization Matrix
        ↓
Automated Test Generation
        ↓
API Requests
        ↓
Expected vs Observed Analysis
        ↓
BOLA / BFLA Detection
        ↓
Security Report
        ↓
CI/CD Security Gate

## Security Scope

This project is intended for:

- APIs owned by the researcher
- Local Docker laboratories
- Intentionally vulnerable applications
- Authorized CTF environments
- Explicitly permitted security-testing programs

Do not use this framework against systems without authorization.

## Vulnerabilities

The current research focuses on:

- BOLA — Broken Object Level Authorization
- BFLA — Broken Function Level Authorization
- Object-property authorization failures
- Role-based authorization inconsistencies

## Example Authorization Model

| Endpoint | User | Admin |
|---|---|---|
| `/profile` | Allow | Allow |
| `/users/{id}` — own object | Allow | Allow |
| `/users/{id}` — another object | Deny | Allow |
| `/documents/{id}` — own document | Allow | Allow |
| `/admin/users` | Deny | Allow |

## Quick Start

```bash
pip install -r requirements.txt
pytest                       # 11 tests against the secure app

# Terminal 1: run the lab API with the authorization checks turned off
LAB_VULNERABLE=1 uvicorn app.main:app --port 8000

# Terminal 2: run the scanner
python -m scanner.run_experiment
```

`LAB_VULNERABLE=1` disables the object-level and function-level checks, so the
scanner has real flaws to find. Without it the app enforces them. Use it only
on your own machine.

### Result of the first experiment

3 roles, 3 endpoints, 10 generated cases, one run against each mode:

| Mode | Findings | Detail |
|---|---|---|
| Secure (default) | 0 | All 10 cases matched the policy |
| `LAB_VULNERABLE=1` | 3 | 1 BOLA (`user` reads another user), 2 BFLA (`user` and `manager` call `/admin/users`) |

The cases are few and the app is small, so this shows that the pipeline works.
It is not a measure of detection accuracy. See `docs/research-results.md`.

## Research Methodology

### 1. API Discovery

Identify API endpoints, HTTP methods, parameters and authentication
requirements from an OpenAPI specification or controlled application.

### 2. Authorization Modeling

Represent expected permissions using an authorization matrix:

```text
Role × Endpoint × Method × Object
````

### 3. Test Generation

Generate authorization test cases from the expected security policy.

Example:

```text
Role: User
Endpoint: GET /users/{id}
Object: Another User
Expected: DENY
```

### 4. Controlled Execution

Execute generated requests against an authorized API environment.

### 5. Differential Analysis

Compare:

```text
Expected Authorization
        vs
Observed Authorization
```

Example:

```text
Expected: DENY
Observed: ALLOW

Potential Finding: BOLA
```

### 6. Remediation

Identify the server-side authorization failure and implement the appropriate
authorization control.

### 7. Regression Testing

Re-run the authorization test after remediation to verify that the vulnerability
cannot be reintroduced.

## Project Architecture

```text
                 OpenAPI Specification
                          |
                          v
                   Endpoint Parser
                          |
                          v
                 Authorization Model
                          |
              +-----------+-----------+
              |           |           |
             Roles      Objects     Methods
              |           |           |
              +-----------+-----------+
                          |
                          v
                  Test Case Generator
                          |
                          v
                      HTTPX Client
                          |
                          v
                    Controlled API
                          |
                          v
                  Response Analyzer
                          |
                  +-------+-------+
                  |               |
             Expected          Observed
             Behavior          Behavior
                  |               |
                  +-------+-------+
                          |
                          v
                  Differential Test
                          |
                          v
                    Finding Engine
                          |
                          v
                   Security Report
```

## Technology Stack

### Application (implemented)

* Python
* FastAPI
* In-memory users with static bearer tokens (lab only)

Planned: a database and JWT authentication.

### Security Testing

* pytest
* OWASP API Security methodology

### Automation

* HTTPX
* OpenAPI (parser in progress)
* Python
* JSON

### DevSecOps

* GitHub Actions
* Gitleaks
* Semgrep
* Trivy
* Dependency scanning

## Repository Structure

```text
api-authorization-research/
│
├── app/
│
├── scanner/
│   ├── analyzer.py
│   ├── openapi_parser.py
│   ├── auth_matrix.py
│   └── reporter.py
│
├── tests/
│   ├── authorization/
│   ├── integration/
│   └── regression/
│
├── lab/
│   ├── vulnerable/
│   ├── fixed/
│   └── complex/
│
├── research/
│   ├── methodology.md
│   ├── experiments.md
│   ├── results.csv
│   └── analysis.md
│
├── docs/
│   ├── threat-model.md
│   ├── architecture.md
│   └── findings.md
│
├── .github/
│   └── workflows/
│       └── security.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── SECURITY.md
└── README.md
```

## Security Testing

The framework should validate scenarios such as:

```text
User → Own Object          = ALLOW
User → Another Object      = DENY
User → Admin Function      = DENY
Admin → Admin Function     = ALLOW
```

### BOLA Test

```text
User A
  |
  +----> GET /users/A
  |       Expected: ALLOW
  |
  +----> GET /users/B
          Expected: DENY
```

### BFLA Test

```text
Normal User
     |
     +----> GET /admin/users
             Expected: DENY

Admin
     |
     +----> GET /admin/users
             Expected: ALLOW
```

## DevSecOps Integration

The project is designed to integrate authorization testing into CI/CD.

```text
Pull Request
     |
     +--> Secret Scanning
     |
     +--> SAST
     |
     +--> Dependency Scanning
     |
     +--> Container Scanning
     |
     +--> Unit Tests
     |
     +--> Authorization Tests
              |
              v
        Security Gate
          /       \
       PASS       FAIL
```

Example security gates:

```text
BOLA regression       → FAIL
BFLA regression       → FAIL
Secret detected       → FAIL
Critical SAST finding → FAIL
Critical dependency   → FAIL
```

## Research Evaluation

The project will be evaluated using measurable security-research metrics.

### Coverage

* Number of endpoints tested
* Number of HTTP methods tested
* Number of roles tested
* Number of objects tested
* Number of authorization combinations

### Detection Accuracy

* True positives
* False positives
* False negatives

### Performance

* Number of requests generated
* Total execution time
* Average test duration

### Security Effectiveness

* Findings before remediation
* Findings after remediation
* Regression vulnerabilities detected

## Experimental Design

Three controlled API environments will be evaluated.

### Version A — Vulnerable

Contains known BOLA/BFLA vulnerabilities.

### Version B — Fixed

Contains corrected server-side authorization controls.

### Version C — Complex

Contains:

* Multiple roles
* Resource ownership
* Administrative privileges
* Object-property restrictions
* Multiple resource types

The same authorization analyzer will be evaluated against each version.

## Research Question

> How accurately can automated authorization testing detect BOLA and BFLA
> vulnerabilities as API authorization complexity increases?

## Current Status

### Completed

* Authorization matrix baseline (`roles.json`)
* Test case generation from the matrix
* Expected-vs-observed analysis with BOLA and BFLA classification
* Lab API with a switchable vulnerable mode
* 11 pytest tests
* CI workflow (tests, Gitleaks, Semgrep, Trivy)

### In Progress

* OpenAPI endpoint parsing (`scanner/openapi_parser.py`)
* Report generation from experiment runs (`scanner/reporter.py`)
* More endpoints, roles and POST/PUT/DELETE methods

### Future Work

* OAuth scope analysis
* ABAC support
* GraphQL authorization testing
* Microservice authorization
* Multi-tenant authorization
* Policy-as-code
* Automated test generation
* False-positive reduction
* Distributed authorization analysis

## Responsible Security Research

All security testing must be performed only against systems for which the
researcher has explicit authorization.

This project is designed for defensive security research, AppSec engineering,
security automation and controlled vulnerability research.

## Author

Chetan Biranje

Cybersecurity | Application Security | DevSecOps | Security Research

## License

MIT. Use it for education and authorized security research only.
