# Cost, speed and reliability

No numbers here on purpose. They depend on your model, your tools and your traffic. Measure.

## Where MCP costs more

| Cost | Why |
|---|---|
| **Context** | Tool descriptions are text the model reads. Many tools or long descriptions take space in the conversation. In most clients that is paid whenever the server is connected, unless the client loads definitions on demand |
| **Model turns** | The model must decide, call, read the result and decide again. Each step takes time and tokens |
| **Variation** | A model might pick a different tool or argument than yesterday |
| **Chatty results** | Large tool outputs fill the context too |

See the shape of it: `python code/demo/context_cost.py`. The estimate uses a rough characters-per-token rule and is **an approximation**, not a measurement.

## Where an API costs more

| Cost | Why |
|---|---|
| **Build time** | A developer writes and maintains the integration |
| **Rigidity** | A new use needs new code |
| **Discovery** | Someone must read the docs |

## Reliability

| | API | MCP |
|---|---|---|
| **Same input, same call** | Yes | Not guaranteed |
| **Testable in a unit test** | Yes | The server is. The model's choices need behavior tests |
| **Failure handling** | Your code decides | The model reads the error and may retry or recover |
| **Rate limits** | Enforced per caller | Same, plus a model that may loop |

A good MCP server reports tool failures **in the result** so the model can read the message and recover, and it keeps errors clear and short. See the `isError` case in [`code/demo/mcp_server.py`](../code/demo/mcp_server.py).

## Keep an MCP server cheap

- **Few tools**, shaped around tasks.
- **Short, precise descriptions** that say when to use each tool.
- **Small results**: return what is needed, not whole records.
- **Pagination and filters** instead of huge lists.
- **No near-duplicate tools.**

## Keep an API reliable

- Stable versions and clear errors.
- Idempotency for writes.
- Rate limits and retries with backoff.

## The trade

An API gives repeatability and low overhead. MCP gives flexibility and discovery. Choose by the job. See [the decision table](decision-table.md).
