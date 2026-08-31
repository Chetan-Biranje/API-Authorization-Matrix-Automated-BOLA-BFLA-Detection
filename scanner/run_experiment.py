import time
from dataclasses import asdict

from scanner.auth_matrix import generate_cases, load_policy
from scanner.analyzer import analyze, request_endpoint, resolve_endpoint


BASE_URL = "http://127.0.0.1:8000"


def load_endpoints():
    return [
        ("GET", "/me"),
        ("GET", "/users/{user_id}"),
        ("GET", "/admin/users"),
    ]


def main():

    policy = load_policy()
    endpoints = load_endpoints()

    cases = generate_cases(
        endpoints=endpoints,
        policy=policy,
    )

    results = []

    start = time.perf_counter()

    for case in cases:

        resolved_endpoint = resolve_endpoint(
            endpoint=case.endpoint,
            role=case.role,
            object_context=case.object_context,
        )

        try:
            status_code = request_endpoint(
                base_url=BASE_URL,
                role=case.role,
                method=case.method,
                endpoint=resolved_endpoint,
            )

            result = analyze(
                role=case.role,
                method=case.method,
                endpoint=case.endpoint,
                expected=case.expected,
                status_code=status_code,
                object_context=case.object_context,
            )

            results.append(result)

            print(
                f"{result.role:<10}"
                f"{result.method:<6}"
                f"{result.endpoint:<25}"
                f"{str(result.object_context):<10}"
                f"{result.expected:<12}"
                f"{result.observed:<10}"
                f"{result.finding}"
            )

        except Exception as exc:
            print(
                f"[ERROR] "
                f"{case.role} "
                f"{case.method} "
                f"{resolved_endpoint}: "
                f"{exc}"
            )

    elapsed = time.perf_counter() - start

    findings = [
        result
        for result in results
        if result.finding != "NONE"
    ]

    print()
    print("========== RESEARCH METRICS ==========")
    print(f"Endpoints: {len(endpoints)}")
    print(f"Roles: {len(policy)}")
    print(f"Authorization cases: {len(cases)}")
    print(f"Requests completed: {len(results)}")
    print(f"Findings: {len(findings)}")
    print(f"Execution time: {elapsed:.4f}s")

    if results:
        print(
            f"Average request time: "
            f"{elapsed / len(results):.4f}s"
        )

    print("=======================================")

    return results


if __name__ == "__main__":
    main()
