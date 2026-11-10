# Prompts for Claude, ChatGPT or Cursor

## 1. Decide for my case

```text
Help me decide between MCP, a plain API, or both for this need: <describe it>. Ask me, one at a time: who or what calls it (an AI assistant or my own code), whether it must be repeatable, how much volume, whether it must act as the signed-in person, and whether it is event-driven. Then recommend one option and say why. Do not recommend a vendor.
```

## 2. Design the tools

```text
I have this API: <paste the endpoints or an OpenAPI summary>. Design an MCP server for AI clients. Do NOT mirror every endpoint. Propose a small set of task-shaped tools. For each give a name, a short description that says when to use it, an input schema, and whether it is read-only. Start read-only. Tell me which write tools I could add later and what approval each would need.
```

## 3. Review an MCP server

```text
Review this MCP server's tool list: <paste tools/list output>. Check: too many tools, near-duplicate tools, descriptions that do not say when to use the tool, tools that can delete or change too much, results that would be huge, and missing authorization. List each problem and the smallest fix.
```

## 4. Explain it to my team

```text
Explain the difference between MCP and an API to a non-technical product team in 150 words, with one example from our product. Say clearly that MCP does not replace the API.
```

## 5. Check my security

```text
Review this plan for letting an AI assistant use our API through MCP: <paste>. Check: authentication (OAuth per person vs a shared key), whose permissions it uses, read-only by default, approval before hard-to-undo changes, logging, rate limits, and prompt injection from data the tools return. List what is missing.
```
