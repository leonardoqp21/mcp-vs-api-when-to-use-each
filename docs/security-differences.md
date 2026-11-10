# Security differences: MCP and APIs

Same systems, different callers. The risks shift when a **model** chooses what to call.

## Authentication and whose permissions

| | Typical API | Remote MCP server |
|---|---|---|
| **Credential** | An API key or an OAuth client for an application | OAuth sign in by the person, in the AI client |
| **Acts as** | The application, often with broad access | The signed-in person, with their role |
| **Revoke** | Rotate or revoke the key | Revoke the person's session |
| **Risk** | A shared key that sees everything | A tool that does more than the person should delegate |

Prefer **per-person OAuth** over a shared key for anything an assistant uses. A static key pasted into a chat or a config file is hard to revoke and easy to leak.

## New risks when a model chooses

| Risk | What it means | Control |
|---|---|---|
| **Prompt injection** | Text the model reads (a ticket, an email, a web page) contains instructions aimed at the assistant | Treat tool results as untrusted. Do not combine untrusted input with broad write access without a human approval |
| **Over-broad tools** | A tool can delete or change far more than the task needs | Small, task-shaped tools. Read-only by default |
| **Misleading tool descriptions** | A server's descriptions steer the model. A malicious or sloppy one can mislead it | Use servers you trust. Review descriptions. Pin versions |
| **Confused deputy** | The assistant uses its access on behalf of someone who should not have it | Per-person permissions. Check authorization on the server for every call |
| **Data leaving your control** | Prompts and tool results go to the model provider | Decide what may be sent. Know which providers process it |
| **Runaway loops** | A model calls a tool repeatedly | Rate limits and step limits |

## What stays the same

- Authentication, authorization and input validation still belong **on the server**, on every call.
- Rate limits, logging and least privilege matter just as much.
- A tool that is unsafe as an API endpoint is unsafe as an MCP tool.

## A practical checklist for any MCP server

- [ ] OAuth sign in, not a static key in a chat or a repo
- [ ] Acts with the signed-in person's permissions
- [ ] A **read-only** option, and writes off by default
- [ ] Approval before changes that are hard to undo
- [ ] A log of every call, and a way to revoke a session
- [ ] Rate limits
- [ ] Few, well-scoped tools
- [ ] Authorization checked on the server for every call, not by hiding tools

## In Stacksync's MCP server

The assistant signs in with the person's Stacksync login through OAuth and acts with that person's role. It can be limited to read access at sign-in, a workspace owner can require a preview and approval for every change, sessions can be revoked, and each user and each workspace API key can make up to 120 tool calls per minute. Apps are connected through a secure sign-in link, never by pasting a secret into the chat. See [Stacksync MCP](https://www.stacksync.com/mcp).

This repo makes no compliance claims.
