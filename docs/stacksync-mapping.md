# Where each door lives in Stacksync

If you use Stacksync, the ideas in this guide map to different parts of the product. Check the current docs.

| Need | In Stacksync |
|---|---|
| **An AI assistant builds and runs things** | The [Stacksync MCP server](https://www.stacksync.com/mcp) (`https://mcp.stacksync.com/mcp`). Claude, ChatGPT, Codex, Cursor and others sign in with OAuth and can build and run two-way syncs, workflows and Genies, investigate sync issues and resolve them, with the permissions of the signed-in person |
| **A script or CI job, no OAuth** | The same MCP server accepts a Stacksync API key in the `Authorization: Bearer <key>` header |
| **Your own code calls an app's API** | **API proxies**: one HTTPS endpoint and one access token for the API of a connected app (for example Salesforce, HubSpot, Pipedrive, Attio or Airtable), so the code never holds the app's login |
| **Keep two systems consistent** | [Two-way sync](https://www.stacksync.com/two-way-sync). Ongoing state is a sync, not a series of calls |
| **React to events** | [Workflow automation](https://www.stacksync.com/workflow-automation) |
| **An agent that acts across systems, with approvals** | [Genies](https://www.stacksync.com/ai-agents) |
| **Teach the assistant how to work safely** | [Skills](https://github.com/stacksyncdata/skills): the MCP server does the work, a skill says how |

## Why this is a good example of the hybrid

One server, two kinds of caller: assistants sign in with OAuth, scripts use a key. The assistant **builds** a sync or a workflow through MCP, and the sync or workflow then **runs without a model in the loop**. That is [pattern 3](hybrid-patterns.md).

## Controls worth knowing

- The assistant acts with the person's role and sees only what they can see.
- Sign in read-only by clearing "Make changes".
- A workspace owner can require a preview and approval for every change.
- Sessions can be revoked.
- Each user and each workspace API key can make up to 120 tool calls per minute.
- Apps connect through a secure sign-in link. No password or key goes into the chat.

Setup for every client: [docs.stacksync.com/mcp](https://docs.stacksync.com/mcp).

This repo makes no performance or compliance claims. Check the docs and test on non-production data.
