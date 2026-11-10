# MCP or API: the decision table

## By situation

| Your situation | Use | Why |
|---|---|---|
| Your own code calls a system on a **fixed path** | **API** (or its SDK) | Deterministic and cheap. No model needed |
| A **backend or mobile app** needs data | **API** | Code calling code |
| A **scheduled job or pipeline** | **API** (or a sync or workflow) | Same result every run |
| **High volume**, or sensitive to cost and delay | **API** | No tool-description overhead, no model turn |
| A person **asks an AI assistant** about their data | **MCP** | The model chooses the right call |
| An agent must **discover** what a system can do | **MCP** | The server describes itself |
| The assistant must act **as the signed-in person** | **MCP** (remote, with OAuth) | Per-person permissions, not a shared key |
| **Exploratory** work: investigate, try, iterate | **MCP** | Flexible, conversational |
| You **have an API** and want AI clients to use it | **MCP wrapping the API** | Keep the API as the source of truth |
| **Both** code and AI clients need it | **API + MCP, same logic** | One set of rules and permissions |
| **React to events** (a deal closes, a file lands) | **Webhook or workflow** | Neither a request-response API nor MCP leads |
| **Build an integration** by describing it in chat | **MCP** | The assistant uses tools to build it |
| A **one-off** data move | A **script on the API** | One run. No ongoing need |

## By question

| Ask yourself | If yes |
|---|---|
| Will a model decide what to call at run time? | Lean **MCP** |
| Must the same input always give the same call? | Lean **API** |
| Is it thousands of calls an hour? | Lean **API** |
| Must it use the person's own permissions? | Lean **MCP** with OAuth |
| Do I already have a good API? | **API first. MCP on top if AI clients need it** |
| Is a person in the conversation? | Lean **MCP** |
| Is it triggered by an event? | **Webhook or workflow** |

Run the helper:

```bash
python code/decide/decide.py
```

It asks nine yes/no questions and returns one or more options with the reasons. Nine worked cases are in [`code/decide/cases.json`](../code/decide/cases.json).

## The rule of thumb

**API for software. MCP for AI clients. Webhooks for events. If two apply, build one on top of the other.**

## When the answer is "neither yet"

If you do not have a stable API, build that first. An MCP server on a shaky foundation inherits every problem and adds new ones.
