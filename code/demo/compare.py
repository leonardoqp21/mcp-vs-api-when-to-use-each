"""Call the same capability through the REST API and through MCP, side by side.

    python compare.py

It starts the REST server in a thread and the MCP server as a subprocess, asks both for the open
invoices of customer C-2, and prints what each caller had to KNOW and what each one was TOLD.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import threading
import urllib.request

import rest_server

HERE = pathlib.Path(__file__).parent


def call_rest(port: int) -> list:
    req = urllib.request.Request(f"http://127.0.0.1:{port}/customers/C-2/invoices?status=open", headers={"Authorization": f"Bearer {rest_server.TOKEN}"})
    with urllib.request.urlopen(req) as res:
        return json.load(res)


class McpClient:
    """The smallest possible MCP client over stdio."""

    def __init__(self):
        self.proc = subprocess.Popen([sys.executable, str(HERE / "mcp_server.py")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        self._id = 0

    def request(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}}) + "\n")
        self.proc.stdin.flush()
        return json.loads(self.proc.stdout.readline())

    def notify(self, method: str) -> None:
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method}) + "\n")
        self.proc.stdin.flush()

    def close(self) -> None:
        self.proc.stdin.close()
        self.proc.wait(timeout=5)


def main() -> None:
    server = rest_server.make_server(0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]

    print("REST API")
    print("  The caller had to KNOW: the path, the query parameter, the auth header and the response shape.")
    print("  Result:", call_rest(port), "\n")

    client = McpClient()
    init = client.request("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "demo", "version": "0"}})
    client.notify("notifications/initialized")
    tools = client.request("tools/list")["result"]["tools"]
    result = client.request("tools/call", {"name": "list_open_invoices", "arguments": {"customer_id": "C-2"}})["result"]
    client.close()

    print("MCP")
    print(f"  Server says: {init['result']['serverInfo']['name']}, protocol {init['result']['protocolVersion']}")
    print("  The caller was TOLD (tools/list):")
    for t in tools:
        print(f"    - {t['name']}: {t['description']}")
    print("  Result:", json.loads(result["content"][0]["text"]))
    print("\nSame data. The API assumes the caller already knows how to use it. MCP describes itself to the caller.")
    server.shutdown()


if __name__ == "__main__":
    main()
