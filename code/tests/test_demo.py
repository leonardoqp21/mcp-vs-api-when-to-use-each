import json
import pathlib
import subprocess
import sys
import threading
import unittest
import urllib.error
import urllib.request

CODE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE / "demo"))

import context_cost  # noqa: E402
import core  # noqa: E402
import mcp_server  # noqa: E402
import rest_server  # noqa: E402
from compare import McpClient  # noqa: E402


class CoreTests(unittest.TestCase):
    def test_open_invoices(self):
        self.assertEqual([i["id"] for i in core.list_open_invoices("C-2")], ["INV-3", "INV-4"])
        self.assertEqual([i["id"] for i in core.list_open_invoices("C-1")], ["INV-1"])

    def test_unknown_customer(self):
        with self.assertRaises(core.NotFound):
            core.get_customer("C-9")


class RestTests(unittest.TestCase):
    def setUp(self):
        self.server = rest_server.make_server(0)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def get(self, path, token=rest_server.TOKEN):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return urllib.request.urlopen(urllib.request.Request(self.base + path, headers=headers))

    def test_invoices(self):
        with self.get("/customers/C-2/invoices?status=open") as res:
            self.assertEqual(len(json.load(res)), 2)

    def test_auth_is_required(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.get("/customers/C-1", token=None)
        self.assertEqual(ctx.exception.code, 401)

    def test_unknown_customer_is_404(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.get("/customers/C-9")
        self.assertEqual(ctx.exception.code, 404)


class McpHandlerTests(unittest.TestCase):
    def req(self, method, params=None, msg_id=1):
        return mcp_server.handle({"jsonrpc": "2.0", "id": msg_id, "method": method, "params": params or {}})

    def test_initialize_declares_the_tools_capability(self):
        r = self.req("initialize")["result"]
        self.assertIn("tools", r["capabilities"])
        self.assertEqual(r["protocolVersion"], mcp_server.PROTOCOL_VERSION)

    def test_tools_list_describes_every_tool_with_a_schema(self):
        tools = self.req("tools/list")["result"]["tools"]
        self.assertEqual({t["name"] for t in tools}, {"get_customer", "list_open_invoices"})
        for t in tools:
            self.assertTrue(t["description"].strip())
            self.assertEqual(t["inputSchema"]["type"], "object")
            self.assertIn("customer_id", t["inputSchema"]["required"])

    def test_tools_call_returns_content(self):
        r = self.req("tools/call", {"name": "list_open_invoices", "arguments": {"customer_id": "C-1"}})["result"]
        self.assertFalse(r["isError"])
        self.assertEqual(json.loads(r["content"][0]["text"])[0]["id"], "INV-1")

    def test_a_tool_failure_is_reported_in_the_result_so_the_model_can_recover(self):
        r = self.req("tools/call", {"name": "get_customer", "arguments": {"customer_id": "C-9"}})["result"]
        self.assertTrue(r["isError"])
        self.assertIn("no customer", r["content"][0]["text"])

    def test_bad_arguments_are_a_tool_error_too(self):
        r = self.req("tools/call", {"name": "get_customer", "arguments": {}})["result"]
        self.assertTrue(r["isError"])

    def test_unknown_tool_and_unknown_method_are_protocol_errors(self):
        self.assertEqual(self.req("tools/call", {"name": "nope"})["error"]["code"], -32602)
        self.assertEqual(self.req("nope")["error"]["code"], -32601)

    def test_notifications_get_no_reply(self):
        self.assertIsNone(mcp_server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))


class McpOverStdioTests(unittest.TestCase):
    def test_a_real_handshake_and_call_over_stdio(self):
        client = McpClient()
        try:
            init = client.request("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}})
            client.notify("notifications/initialized")
            tools = client.request("tools/list")["result"]["tools"]
            result = client.request("tools/call", {"name": "list_open_invoices", "arguments": {"customer_id": "C-2"}})["result"]
        finally:
            client.close()
        self.assertEqual(init["result"]["serverInfo"]["name"], "demo-invoices")
        self.assertEqual(len(tools), 2)
        self.assertEqual(len(json.loads(result["content"][0]["text"])), 2)

    def test_rest_and_mcp_return_the_same_data(self):
        server = rest_server.make_server(0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{server.server_address[1]}/customers/C-2/invoices?status=open", headers={"Authorization": f"Bearer {rest_server.TOKEN}"})
            via_rest = json.load(urllib.request.urlopen(req))
        finally:
            server.shutdown()
            server.server_close()
        via_mcp = json.loads(mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "list_open_invoices", "arguments": {"customer_id": "C-2"}}})["result"]["content"][0]["text"])
        self.assertEqual(via_rest, via_mcp)


class ContextCostTests(unittest.TestCase):
    def test_more_tools_cost_more(self):
        cost = context_cost.tools_cost(mcp_server.TOOLS)
        self.assertEqual(cost["tools"], 2)
        self.assertGreater(cost["total"], 0)
        self.assertEqual(context_cost.scale(mcp_server.TOOLS, 10), cost["total"] * 10)

    def test_longer_descriptions_cost_more(self):
        short = [{"name": "a", "description": "x", "inputSchema": {}}]
        long = [{"name": "a", "description": "x" * 400, "inputSchema": {}}]
        self.assertGreater(context_cost.approx_tokens(long), context_cost.approx_tokens(short))


class HygieneTests(unittest.TestCase):
    def test_no_em_dashes(self):
        for path in CODE.parent.rglob("*.md"):
            self.assertNotIn(chr(0x2014), path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
