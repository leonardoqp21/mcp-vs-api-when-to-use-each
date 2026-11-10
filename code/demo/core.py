"""The business logic. One place. Both the REST API and the MCP server call it.

That is the point of the demo: MCP is not a second system. It is a second way to reach the same
capability, shaped for an AI client. Synthetic data. Standard library only. Python 3.9 or newer.
"""
from __future__ import annotations

CUSTOMERS = {
    "C-1": {"id": "C-1", "name": "Umbrella Inc", "tier": "growth"},
    "C-2": {"id": "C-2", "name": "Globex Corp", "tier": "enterprise"},
}
INVOICES = [
    {"id": "INV-1", "customer": "C-1", "amount": "120.00", "status": "open"},
    {"id": "INV-2", "customer": "C-1", "amount": "80.00", "status": "paid"},
    {"id": "INV-3", "customer": "C-2", "amount": "950.00", "status": "open"},
    {"id": "INV-4", "customer": "C-2", "amount": "40.00", "status": "open"},
]


class NotFound(Exception):
    pass


def get_customer(customer_id: str) -> dict:
    if customer_id not in CUSTOMERS:
        raise NotFound(f"no customer {customer_id}")
    return CUSTOMERS[customer_id]


def list_open_invoices(customer_id: str) -> list[dict]:
    get_customer(customer_id)
    return [i for i in INVOICES if i["customer"] == customer_id and i["status"] == "open"]
