# Part 2: A simple MCP server and its clients

This folder has one MCP server, `server.py`, with one tool (`add`), and one client for each transport. Each client comes as a `.py` script for quick lookup and a notebook that explains it step by step, with real outputs.

## Reading order

1. **`server.ipynb`:** The server, line by line. How a tool is registered, and how the transport is chosen.
2. **`client-stdio.ipynb`:** stdio. The client starts the server itself, as a child process.
3. **`client-streamable-http.ipynb`:** Streamable HTTP. You start the server, and the client sends each message as a POST to `/mcp`.
4. **`client-sse.ipynb`:** SSE, the old HTTP transport that Streamable HTTP replaced. Read it last.

## Running it

Run every command from this folder, with the environment active (`conda activate MCP_env`). The notebooks use the MCP_env kernel.

- **stdio:** `python client-stdio.py`. Nothing needs to be started first.
- **Streamable HTTP:** Start `python server.py` in one terminal, then run `python client-streamable-http.py` in a second one.
- **SSE:** Start `python server.py sse` in one terminal, then run `python client-sse.py` in a second one.

Each client prints the tool's name, its description and the result of `add(2, 3)`:

```text
add
Add two numbers together
5
```

Over stdio, the server's startup line appears on the same screen first.
