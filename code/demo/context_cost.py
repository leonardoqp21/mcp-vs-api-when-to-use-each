"""Why MCP is not free: tool descriptions are read by the model, so they take space in its context.

A REST call you hard-coded costs the model nothing. An MCP server's `tools/list` output is text the
model has to read. More tools and longer descriptions mean more to read, in most clients on every
conversation that has the server connected (some clients load tool definitions on demand).

This estimates the size with a rough characters-per-token rule. It is an APPROXIMATION to show the
shape of the trade-off, not a measurement of any model's tokenizer.

    python context_cost.py
"""
from __future__ import annotations

import json

import mcp_server

CHARS_PER_TOKEN = 4  # a rough rule of thumb for English text and JSON


def approx_tokens(obj) -> int:
    return round(len(json.dumps(obj, separators=(",", ":"))) / CHARS_PER_TOKEN)


def tools_cost(tools: list[dict]) -> dict:
    per_tool = {t["name"]: approx_tokens(t) for t in tools}
    return {"tools": len(tools), "total": sum(per_tool.values()), "per_tool": per_tool}


def scale(tools: list[dict], copies: int) -> int:
    """What a server with `copies` times as many tools of this size would cost."""
    return tools_cost(tools)["total"] * copies


def main() -> None:
    cost = tools_cost(mcp_server.TOOLS)
    print(f"This demo server: {cost['tools']} tools, about {cost['total']} tokens of descriptions ({cost['per_tool']}).")
    for n in (10, 50, 200):
        print(f"A server with {n} tools of this size: about {scale(mcp_server.TOOLS, n // len(mcp_server.TOOLS))} tokens.")
    print("\nThat space is usually paid in every conversation that has the server connected, before any work is done,")
    print("unless the client loads tool definitions on demand.")
    print("A hard-coded REST call costs the model nothing until it is used.")
    print("Fewer, well-scoped tools with short descriptions keep it small.")


if __name__ == "__main__":
    main()
