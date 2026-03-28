from __future__ import annotations

import random


class MockSupplierAPI:
    """Simulates a marketplace or supplier sync response."""

    @staticmethod
    def fetch_stock_updates() -> list[dict]:
        return [
            {"sku": "SKU-1001", "stock_delta": random.randint(3, 10)},
            {"sku": "SKU-1003", "stock_delta": random.randint(5, 15)},
            {"sku": "SKU-1007", "stock_delta": random.randint(8, 20)},
        ]
