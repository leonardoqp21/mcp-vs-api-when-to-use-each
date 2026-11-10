# Should you build an MCP server for your API?

## Build one if

- Your users already work in AI clients and ask for your product there.
- Your API has actions a person would naturally ask for in words.
- You can expose them safely, with per-person permissions.

## Do not build one if

- Nobody uses AI clients with your product yet. An API is enough.
- Your API is unstable, undocumented or has no authorization model. Fix that first.
- You would only mirror every endpoint one to one.

## Design rules

1. **Design tools around tasks, not endpoints.** "Find overdue invoices for a customer", not a tool per field.
2. **Few tools.** Every tool is text a model reads. Fewer, clearer tools work better.
3. **Write descriptions for a model.** Say what it does, what it returns and **when to use it**. Keep them short.
4. **Read-only first.** Add writes one at a time, with approval for anything hard to undo.
5. **Return small, useful results.** Filters and pagination, not whole tables.
6. **Report failures in the result** with a message the model can act on.
7. **Per-person OAuth** for remote servers. Avoid shared keys.
8. **Authorize on the server** for every call.
9. **Rate limit and log** every call.
10. **Version it** and say what changed.

## Test it

- Unit test the tools like any code.
- Test the **model's behavior**: does it pick the right tool, refuse the wrong ones, recover from errors?
- Try adversarial input in the data the tools return.
- Check the size of `tools/list`. See [`code/demo/context_cost.py`](../code/demo/context_cost.py).

## Use an SDK

The demo in this repo speaks the protocol by hand to show what is on the wire. For a real server use an official SDK for your language. It handles the protocol, the transports and the authorization flow.

## Minimal shape

```python
# the capability, once
def list_open_invoices(customer_id): ...

# the API door
GET /customers/{id}/invoices?status=open

# the MCP door: describe it, then call the same function
{"name": "list_open_invoices",
 "description": "List the unpaid invoices of one customer. Read only. Use it when someone asks what a customer owes.",
 "inputSchema": {"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}}
```

Full working version: [`code/demo`](../code/demo).
