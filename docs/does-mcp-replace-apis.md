# Does MCP replace APIs?

**No.** MCP does not replace APIs. Most MCP servers are built **on top of** an API. MCP is a different way to reach a capability, shaped for AI clients. The API stays.

## What each one is

- **An API** (REST, GraphQL, gRPC, an SDK) is how **software** talks to a system. A developer reads the documentation at build time and writes code that makes a fixed call.
- **MCP (Model Context Protocol)** is an open protocol, introduced by Anthropic in late 2024 and now supported by many AI clients, that lets an **AI assistant or agent** discover and call tools on a server at **run time**. The server describes its tools (names, descriptions, input schemas), and the model decides which to use.

## The one difference that matters

| | API | MCP |
|---|---|---|
| **Who decides what to call** | A developer, in advance | An AI model, at run time |
| **How the caller learns what exists** | Documentation, read once | The server describes itself (`tools/list`) |
| **Typical caller** | Your code | An AI client (Claude, ChatGPT, Cursor, Codex) |
| **Best at** | Fixed, repeatable, high volume work | Open-ended, assistant-driven work |

## A mental model

```text
          your code ----------------------->  API  ---->  the system
   AI client (the model) ---> MCP server ---> API  ---->  the system
```

The MCP server is a thin, AI-friendly front door in front of the same logic. [`code/demo`](../code/demo) runs both and shows the same data coming back.

## Why people think it replaces APIs

- Demos show an assistant doing in a chat what used to need code, so it looks like the API disappeared. It is still there, one layer down.
- "Connect your AI to X" sounds like a replacement for "integrate X". It is a new kind of client for X.

## Why it cannot replace them

| Need | Why an API is still the right tool |
|---|---|
| A nightly job that must do the exact same thing | A model in the loop adds variation and cost for no benefit |
| High volume or latency-sensitive calls | Tool descriptions and a model's turn add overhead |
| A mobile app or a backend service | Code calling code does not need a model to choose |
| A public developer platform | Developers expect stable, documented endpoints |
| Event-driven pushes | Webhooks and queues, not a request a model initiates |

## When MCP is the better door

- A person asks questions or gives instructions in natural language, and the model has to choose what to call.
- The set of useful actions is large and the right one depends on the request.
- The assistant should act **as the signed-in person**, with their permissions.

## The honest answer

Use the API for software. Use MCP for AI clients. If both exist, build one on top of the other so they share logic and permissions. See [the decision table](decision-table.md) and [hybrid patterns](hybrid-patterns.md).
