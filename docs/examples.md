# Twelve examples: which door for which job

| # | Scenario | Use | Why |
|---|---|---|---|
| 1 | A nightly job copies orders from the shop into the warehouse | **API** (or a sync) | Fixed, repeatable, high volume |
| 2 | A support lead asks Claude "which tickets are overdue, and why?" | **MCP** | The model chooses the calls. The person is in the loop |
| 3 | You have a billing API and customers want to use it from ChatGPT | **MCP wrapping the API** | Keep the API. Add a small, scoped MCP server |
| 4 | A mobile app shows a customer's invoices | **API** | Code calling code. A model adds nothing |
| 5 | An analyst explores a warehouse with an assistant, as themselves | **MCP**, read only, per-person sign in | Exploratory work with the person's own permissions |
| 6 | A CI job posts a build result to an internal system | **API** with a key | Fixed payload, runs unattended |
| 7 | "Keep Salesforce and NetSuite matched" | **A sync**, set up through **MCP** | Ongoing state is a sync. Setting it up in chat is MCP |
| 8 | "Tell Slack when a deal closes" | **Workflow or webhook** | An event, not a question |
| 9 | A public developer platform | **API** first | Developers expect stable endpoints. MCP is optional |
| 10 | An agent acts for thousands of end users with their own permissions | **Remote MCP with OAuth**, or an API with delegated OAuth | Avoid a shared key that sees everything |
| 11 | A one-off migration of 2 million records | **A script on the API** | One run. No model in the loop |
| 12 | An internal team wants an assistant to query one internal service | **A small read-only MCP server** | Keep it to a few task-shaped tools |

## What they have in common

- **If code decides, use an API. If a model decides, use MCP.**
- Ongoing consistency between systems is a **sync**, not a series of calls from either one.
- Events are **webhooks and workflows**.
- Start **read-only** for anything an AI client touches.

## Anti-examples

| Mistake | Better |
|---|---|
| Putting a model between two systems that need the same result every time | An API, a sync or a workflow |
| Exposing every endpoint as a tool | A few task-shaped tools |
| Giving an assistant a shared admin key | A remote server with per-person sign in |
| Calling an MCP server from a hot loop in your backend | The API behind it |
| Building an MCP server before you have a stable API | The API first |

Try the demo: `python code/demo/compare.py`.
