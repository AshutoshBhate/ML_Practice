# MCP Crash Course for Python Developers

**MCP (Model Context Protocol) is an open standard for connecting LLM apps to tools and data.** This course explains it from zero, then builds servers and clients in Python with the official SDK (mcp 1.27.0). Every script has a notebook next to it that explains it step by step, with real outputs.

## The parts

1. **[Understanding MCP](./1-understanding-mcp/README.md):** What MCP is, the host, client and server, tools, resources and prompts, the JSON-RPC messages and the transports. Its appendix covers the 2026-07-28 spec and mcp 2.x.
2. **[A simple server and its clients](./2-simple-server-setup/README.md):** A calculator server, with a client for stdio, Streamable HTTP and SSE.
3. **[An OpenAI model using MCP tools](./3-openai-integration/README.md):** A host that hands an MCP server's tools to an OpenAI model.
4. **[MCP vs plain function calling](./4-mcp-vs-function-calling/README.md):** The same tool, used both ways.
5. **[Running the server in Docker](./5-run-with-docker/README.md):** The server in a container, over Streamable HTTP.
6. **[Lifecycle management](./6-lifecycle-management/README.md):** The three phases of a connection, and a lifespan that opens and closes a database.

Also in the `MCP` folder:

- **[mcp_filesystem_client](../mcp_filesystem_client/README.md):** A Python client for the official Node.js filesystem server.
- **[servers/youtube](../servers/youtube/README.md):** A YouTube transcript server, rewritten from a tutorial.

## Setup

Everything runs in one conda environment, MCP_env, with Python 3.12:

```bash
conda create -n MCP_env python=3.12
conda activate MCP_env
pip install -r requirements.txt
```

`requirements.txt` pins mcp 1.27.0 and openai 2.32.0. Parts 3 and 4 call OpenAI, so they need `OPENAI_API_KEY` in `crash-course/.env`. Run each part's commands from that part's folder, and use the MCP_env kernel for the notebooks.

A few parts need one more thing:

- **Part 5:** Docker Desktop.
- **mcp_filesystem_client:** Node.js, for `npx`.
- **servers/youtube:** `pip install youtube-transcript-api==1.2.4`.

## Resources

- [MCP documentation](https://modelcontextprotocol.io)
- [The spec, version 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25), which mcp 1.27.0 speaks
- [The spec, version 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28), the newest
- [Python SDK on GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [Official servers](https://github.com/modelcontextprotocol/servers)
