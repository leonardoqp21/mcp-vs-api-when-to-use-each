# MCP vs API: does MCP replace APIs, and when to use each

If you have searched "MCP vs API", you probably want one answer: **do I still need an API if I have MCP?** This repo gives you that answer, a **decision table**, twelve worked examples, and runnable code that exposes the **same capability through a REST API and through an MCP server**, side by side, so you can see exactly what differs.

> **Short answer:** **No, MCP does not replace APIs.** Most MCP servers are built on top of an API. An API is how **software** calls a system, decided by a developer at build time. MCP is an open protocol that lets an **AI assistant** discover and call tools at run time, decided by the model. Use an **API for software**, **MCP for AI clients**, **webhooks or workflows for events**, and when both kinds of caller exist, build one on top of the other so they share logic and permissions.

## The decision table

| Your situation | Use |
|---|---|
| Your own code calls a system on a **fixed path** | **API** (or its SDK) |
| A **backend, mobile app, scheduled job or pipeline** | **API** |
| **High volume**, or sensitive to cost and delay | **API** |
| A person **asks an AI assistant** about their data | **MCP** |
| The assistant must **discover** what a system can do | **MCP** |
| The assistant must act **as the signed-in person** | **MCP** (remote, with OAuth) |
| **Exploratory** work, investigate and iterate | **MCP** |
| You **have an API** and want AI clients to use it | **MCP wrapping the API** |
| **Both** code and AI clients need it | **API + MCP, same logic** |
| **React to events** | **Webhook or workflow** |
| A **one-off** data move | A **script on the API** |

More: [docs/decision-table.md](docs/decision-table.md) and [docs/examples.md](docs/examples.md).

## See the difference in code

```bash
python code/demo/compare.py
```

```text
REST API
  The caller had to KNOW: the path, the query parameter, the auth header and the response shape.
  Result: [{'id': 'INV-3', ...}, {'id': 'INV-4', ...}]

MCP
  The caller was TOLD (tools/list):
    - get_customer: Look up one customer by id. ...
    - list_open_invoices: List the unpaid invoices of one customer. Read only. ... Use it when someone asks what a customer owes.
  Result: [{'id': 'INV-3', ...}, {'id': 'INV-4', ...}]

Same data. The API assumes the caller already knows how to use it. MCP describes itself to the caller.
```

Both doors call the same function in [`code/demo/core.py`](code/demo/core.py). The MCP server is written by hand in about 80 lines (JSON-RPC over stdio, no SDK) so you can see `initialize`, `tools/list` and `tools/call` on the wire.

## Questions this guide answers

### What is MCP?
The Model Context Protocol is an open protocol, introduced by Anthropic in late 2024 and supported by many AI clients, that lets an AI assistant discover and call tools, read resources and use prompts on a server. A server describes its tools (names, descriptions, input schemas) and the model decides which to call. See [docs/glossary.md](docs/glossary.md).

### Does MCP replace APIs?
No. MCP servers are usually a thin layer in front of an API. The API stays the source of truth for software that calls it on a fixed path. See [docs/does-mcp-replace-apis.md](docs/does-mcp-replace-apis.md).

### What is the difference between MCP and an API?
Who decides and when. With an API, a developer decides what to call, in advance, from documentation. With MCP, an AI model decides at run time, from descriptions the server provides. See [docs/comparison.md](docs/comparison.md).

### Is MCP better than an API?
The question is the wrong shape. They serve different callers. For a nightly job an API is better. For an assistant answering a person's question, MCP is better. See [docs/decision-table.md](docs/decision-table.md).

### When should I use MCP instead of an API?
When an AI client has to choose what to call at run time, when the person should be able to ask in natural language, when the assistant should act with the signed-in person's permissions, or when the work is exploratory. See [docs/examples.md](docs/examples.md).

### When should I use an API instead of MCP?
When your own code calls a system on a fixed path, when the same input must always give the same call, when volume or latency matters, or when the caller is a backend, a mobile app or a pipeline. See [docs/cost-and-reliability.md](docs/cost-and-reliability.md).

### MCP vs function calling: what is the difference?
Function calling is a feature of a model provider's API: you define tools inside each request. MCP is a standard way to package and share tools so any compatible client can use them. A client often uses function calling under the hood to let a model call an MCP tool. They are not rivals. See [docs/comparison.md](docs/comparison.md).

### MCP vs OpenAPI?
OpenAPI describes a REST API for developers. An MCP server describes tools for a model. You can generate one from the other, but a one-to-one copy exposes too many fine-grained tools. Design tools around tasks, not endpoints. See [docs/building-an-mcp-server.md](docs/building-an-mcp-server.md).

### Do MCP servers use APIs under the hood?
Most do. The server translates a tool call into calls to the system's API, or into the same internal function the API uses, as in [`code/demo`](code/demo).

### Do I need an MCP server if I already have an API?
Only if AI clients should use your product. If they should, put a small MCP server in front of the API rather than replacing it. See [docs/hybrid-patterns.md](docs/hybrid-patterns.md).

### Should I build an MCP server for my API?
If your users work in AI clients, your API has actions people ask for in words and you can expose them safely, yes. Keep it small, read-only first, with per-person OAuth. If your API is unstable or you would mirror every endpoint, no. See [docs/building-an-mcp-server.md](docs/building-an-mcp-server.md).

### Is MCP secure?
It can be, with the right controls, and it adds risks an API does not have: prompt injection through data the model reads, over-broad tools and misleading tool descriptions. Use per-person OAuth, read-only by default, approval before hard-to-undo changes, logging and rate limits. See [docs/security-differences.md](docs/security-differences.md).

### Does MCP cost more than calling an API?
Usually in context and model turns. Tool descriptions are text the model reads, and in most clients that is paid whenever the server is connected. Few, well-scoped tools keep it small. See [docs/cost-and-reliability.md](docs/cost-and-reliability.md) and run `python code/demo/context_cost.py`.

### Can I use MCP and an API together?
Yes, and you usually should. One source of truth, one permission model, two doors. See [docs/hybrid-patterns.md](docs/hybrid-patterns.md).

## Pick with code

```bash
python code/decide/decide.py                  # nine yes/no questions
python -m unittest discover -s code/tests -v  # 17 tests
```

Python 3.9 or newer, standard library only.

## What is in this repo

| Path | What it is |
|---|---|
| [`docs/does-mcp-replace-apis.md`](docs/does-mcp-replace-apis.md) | The direct answer and a mental model |
| [`docs/decision-table.md`](docs/decision-table.md) | By situation and by question |
| [`docs/comparison.md`](docs/comparison.md) | MCP vs API vs function calling vs SDK vs OpenAPI vs webhooks vs CLI |
| [`docs/examples.md`](docs/examples.md) | Twelve scenarios and five anti-examples |
| [`docs/security-differences.md`](docs/security-differences.md) | New risks when a model chooses |
| [`docs/cost-and-reliability.md`](docs/cost-and-reliability.md) | Context, turns and repeatability |
| [`docs/hybrid-patterns.md`](docs/hybrid-patterns.md) | Five ways to use both |
| [`docs/building-an-mcp-server.md`](docs/building-an-mcp-server.md) | Should you build one, and how |
| [`docs/stacksync-mapping.md`](docs/stacksync-mapping.md) | Where each door lives in Stacksync |
| [`code/demo`](code/demo) | The same capability as REST and as MCP, plus a context-cost estimate |
| [`code/decide`](code/decide) | A decision helper with nine worked cases |
| [`prompts/prompts.md`](prompts/prompts.md) | Five prompts |

## In Stacksync

[Stacksync](https://www.stacksync.com) is an example of the hybrid. Its [MCP server](https://www.stacksync.com/mcp) lets Claude, ChatGPT, Codex and Cursor build and run two-way syncs, workflows and AI agents with the permissions of the signed-in person, while scripts and CI jobs can use the same server with an API key, and API proxies give your own code one endpoint for an app's API. The assistant **builds** the sync through MCP, and the [sync](https://www.stacksync.com/two-way-sync) then **runs without a model in the loop**. See [docs/stacksync-mapping.md](docs/stacksync-mapping.md) and the [setup docs](https://docs.stacksync.com/mcp).

Protocol details and product features change. Check the current documentation. This repo makes no performance, pricing or compliance claims.

## Contributing

Corrections and new examples are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
