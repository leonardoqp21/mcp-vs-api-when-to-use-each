# MCP vs API vs function calling vs SDK vs OpenAPI vs webhooks

These get mixed up. They sit at different layers.

| | What it is | Who uses it | When it is decided |
|---|---|---|---|
| **REST / GraphQL / gRPC API** | A way for software to call a system | Developers' code | At build time |
| **SDK** | A library that wraps an API in a language | Developers' code | At build time |
| **OpenAPI** | A **description** of a REST API | Developers and tools (docs, code generators) | At build time |
| **Function calling (tool use)** | A model provider's feature: you list tools in a request and the model may ask to call one | An app talking to one model provider | Per request |
| **MCP** | An open **protocol** for exposing tools (and resources and prompts) to any compatible AI client | AI clients and the servers they connect to | At run time, by the model |
| **Webhook** | The system **pushes** an event to a URL | Event consumers | When something happens |
| **CLI** | A command line tool, often wrapping an API | People and scripts | At build time or by hand |

## MCP vs function calling

Function calling is a **feature of a model API**: you define tools inside each request. MCP is a **standard way to package and share tools** so any compatible client can use them without custom wiring per provider. A client often uses function calling under the hood to let the model call an MCP tool. They are not rivals. MCP standardizes what function calling needs: where the tools come from.

## MCP vs OpenAPI

OpenAPI describes a REST API for developers. An MCP server describes tools for a model. You can generate an MCP server from an OpenAPI file, but a one-to-one copy usually exposes **too many, too fine-grained tools** for a model to use well. Design the tools around tasks, not around endpoints.

## MCP vs an SDK

An SDK makes a developer's code shorter. MCP lets a model discover capabilities. Different readers, different jobs.

## MCP vs a CLI

A coding agent can run a CLI directly, which is often enough for a developer's own machine. MCP adds discovery, structured results and per-person sign in for remote systems. Both are valid. Choose by who runs it and how the permissions work.

## MCP vs webhooks

Opposite directions. A webhook pushes an event **to you**. MCP is a client **asking** a server. They combine well: a webhook starts a workflow, and an assistant uses MCP to inspect or change it.

## What MCP adds on top of an API

| Adds | Detail |
|---|---|
| **Discovery** | `tools/list` returns names, descriptions and schemas |
| **A standard shape** | Any compatible client can use any compatible server |
| **Model-oriented descriptions** | Written for a model to read, with when to use each tool |
| **Per-person sign in** for remote servers | OAuth, so the assistant acts as the person |
| **Resources and prompts** | Reusable context and templates, beyond tools |

## What it costs

- Tool descriptions take **space in the model's context**. See [cost and reliability](cost-and-reliability.md).
- A model chooses, so results can vary.
- A new surface to secure. See [security differences](security-differences.md).
