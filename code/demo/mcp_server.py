"""The same capability as an MCP server, speaking JSON-RPC 2.0 over stdio. No SDK.

Three messages are enough to show the difference:

    initialize   the client and server agree on a protocol version and capabilities
    tools/list   the server DESCRIBES what it can do: names, descriptions, input schemas
    tools/call   the client asks for one tool by name with arguments

`tools/list` is the part a plain API does not have. A model reads those descriptions at run time
and decides which tool to call. Messages are one JSON object per line, as the stdio transport defines.

This is a teaching implementation. For real servers use an official SDK. Standard library only.
"""
from __future__ import annotations

import json
import sys

import core

PROTOCOL_VERSION = "2025-03-26"

TOOLS = [
    {
        "name": "get_customer",
        "description": "Look up one customer by id. Returns the name and tier. Use it to confirm who a customer is before asking about their invoices.",
        "inputSchema": {"type": "object", "properties": {"customer_id": {"type": "string", "description": "A customer id such as C-1"}}, "required": ["customer_id"]},
    },
    {
        "name": "list_open_invoices",
        "description": "List the unpaid invoices of one customer. Read only. Returns invoice id and amount. Use it when someone asks what a customer owes.",
        "inputSchema": {"type": "object", "properties": {"customer_id": {"type": "string", "description": "A customer id such as C-1"}}, "required": ["customer_id"]},
    },
]
HANDLERS = {"get_customer": core.get_customer, "list_open_invoices": core.list_open_invoices}


def handle(message: dict) -> dict | None:
    """Return a response for a request, or None for a notification."""
    method, msg_id = message.get("method"), message.get("id")
    if msg_id is None:  # a notification, such as notifications/initialized: no reply
        return None

    def ok(result):
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    def error(code, text):
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": text}}

    if method == "initialize":
        return ok({"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}}, "serverInfo": {"name": "demo-invoices", "version": "0.1.0"}})
    if method == "tools/list":
        return ok({"tools": TOOLS})
    if method == "tools/call":
        params = message.get("params", {})
        handler = HANDLERS.get(params.get("name"))
        if handler is None:
            return error(-32602, f"unknown tool: {params.get('name')}")
        try:
            data = handler(**params.get("arguments", {}))
            return ok({"content": [{"type": "text", "text": json.dumps(data)}], "isError": False})
        except (core.NotFound, TypeError) as err:
            # a tool failure is reported IN the result so the model can read it and recover
            return ok({"content": [{"type": "text", "text": str(err)}], "isError": True})
    if method == "ping":
        return ok({})
    return error(-32601, f"method not found: {method}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        reply = handle(json.loads(line))
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
