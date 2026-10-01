import sys
from typing import Any

import requests

BASE_URL = "http://127.0.0.1:8000"


def request_json(url: str) -> Any:
    response = requests.get(url, timeout=10)
    print(f"URL: {url}")
    print(f"STATUS: {response.status_code}")
    print(response.text)
    response.raise_for_status()
    return response.json()


def main() -> None:
    try:
        health = request_json(f"{BASE_URL}/health")
        assert health.get("status") == "ok", health

        transactions = request_json(f"{BASE_URL}/transactions?limit=2")
        assert isinstance(transactions, list), type(transactions)
        assert len(transactions) > 0, "No transaction rows returned"
        first = transactions[0]
        assert "transaction_id" in first, first
        assert "amount" in first, first
        print("API smoke check passed.")
    except Exception as exc:  # pragma: no cover - CLI test harness
        print(f"API smoke check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
