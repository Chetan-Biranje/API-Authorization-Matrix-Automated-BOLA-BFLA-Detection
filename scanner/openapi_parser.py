import json
from pathlib import Path


def load_openapi(path: str) -> dict:
    """Load an OpenAPI JSON specification."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"OpenAPI file not found: {path}")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_endpoints(spec: dict) -> list[dict]:
    """Extract HTTP endpoints from an OpenAPI specification."""
    endpoints = []

    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method.lower() not in {
                "get",
                "post",
                "put",
                "patch",
                "delete",
                "options",
                "head",
            }:
                continue

            endpoints.append(
                {
                    "path": path,
                    "method": method.upper(),
                    "operation_id": operation.get("operationId"),
                    "summary": operation.get("summary"),
                }
            )

    return endpoints


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python scanner/openapi_parser.py <openapi.json>")
        raise SystemExit(1)

    spec = load_openapi(sys.argv[1])
    endpoints = extract_endpoints(spec)

    print(f"Found {len(endpoints)} endpoints")

    for endpoint in endpoints:
        print(
            f"{endpoint['method']:6} "
            f"{endpoint['path']}"
        )
