# Glossary

**API.** A way for software to call another system. REST, GraphQL and gRPC are common styles.

**MCP (Model Context Protocol).** An open protocol that lets an AI client discover and call tools, read resources and use prompts on a server.

**MCP server.** A program that exposes tools to AI clients over MCP. Local servers usually speak over stdio. Remote ones over HTTP.

**MCP client.** The AI application (Claude, ChatGPT, Cursor, Codex) that connects to MCP servers.

**Tool.** One action an MCP server offers, with a name, a description and an input schema.

**`tools/list`.** The MCP request that returns the server's tools and their descriptions.

**`tools/call`.** The MCP request that runs one tool with arguments.

**JSON-RPC.** The message format MCP uses.

**Transport.** How messages travel: stdio for local servers, HTTP for remote ones.

**Function calling (tool use).** A model provider's feature that lets a model request a call to a function you defined in the request.

**OpenAPI.** A description format for REST APIs.

**SDK.** A library that wraps an API for a programming language.

**Webhook.** A request a system sends to your URL when something happens.

**OAuth.** A sign-in standard. In MCP it lets the assistant act as the signed-in person.

**Prompt injection.** Text a model reads that contains instructions meant to steer it.

**Idempotent.** Doing the same operation twice has the same effect as once.
