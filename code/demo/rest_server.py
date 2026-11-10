"""The same capability as a plain REST API.

    GET /customers/{id}
    GET /customers/{id}/invoices?status=open

The caller must already know these paths, parameters and the response shape. It learned them from
documentation (an OpenAPI file, a developer guide) at BUILD time. Nothing in the API tells a model
at RUN time what is available or when to use it. Standard library only.
"""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

import core

TOKEN = "demo-token"  # a static key, shared by every caller. Fine for a demo


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: dict | list) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            return self._send(401, {"error": "unauthorized"})
        path = self.path.split("?", 1)[0]
        try:
            if m := re.fullmatch(r"/customers/([\w-]+)", path):
                return self._send(200, core.get_customer(m.group(1)))
            if m := re.fullmatch(r"/customers/([\w-]+)/invoices", path):
                if "status=open" not in self.path:
                    return self._send(400, {"error": "only status=open is supported"})
                return self._send(200, core.list_open_invoices(m.group(1)))
        except core.NotFound as err:
            return self._send(404, {"error": str(err)})
        self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


def make_server(port: int = 0) -> HTTPServer:
    return HTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    server = make_server(8000)
    print("REST API on http://127.0.0.1:8000")
    server.serve_forever()
