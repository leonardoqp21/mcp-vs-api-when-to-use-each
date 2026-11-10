# Hybrid patterns: using both

## 1. MCP in front of an API (the common one)

```text
AI client -> MCP server -> your API -> your system
your code ----------------> your API
```

Keep the API as the source of truth. The MCP server is a thin, well-scoped layer. They share logic, validation and permissions. [`code/demo`](../code/demo) does exactly this with one `core.py`.

**Use when:** an API exists and AI clients need it.

## 2. Explore with MCP, run with an API

An assistant, through MCP, investigates a problem and works out the steps. Once the steps are known and stable, they move into code or a workflow that calls the API directly.

**Use when:** you are still learning what the job is. Once the decisions are identical every time, turn them into a deterministic flow.

## 3. Build with MCP, run without a model

An assistant uses MCP to **create** the automation (a sync, a workflow). The automation then runs on its own, with no model in the loop.

**Use when:** the one-time setup is open-ended, but the ongoing work is fixed. This is how the Stacksync MCP server is typically used: an assistant builds syncs and workflows, which then run without it.

## 4. An agent that calls vetted workflows as tools

The agent chooses **what** to do. Each action is a vetted, tested step with its own approvals and logs.

**Use when:** you want judgment about what to do and determinism in how it is done.

## 5. Webhooks wake the agent

An event starts a workflow or an agent. The agent may then use MCP tools to read context or act.

**Use when:** work starts from an event, not from a question.

## Rules for any hybrid

- **One source of truth.** Never two implementations of the same business rule.
- **One permission model.** Authorize on the server for every call, whichever door was used.
- **Read-only first** for AI clients.
- **Approval before writes** that are hard to undo.
- **Log both doors the same way.**

## Anti-pattern: MCP inside a hot loop

Do not call an MCP server from a backend loop that could call the API. You pay for the description and the protocol with no model involved.
