# Part 6: Lifecycle management

Every MCP connection goes through three phases: Initialization (the handshake), operation (listing and calling tools), and shutdown. A server can also run its own code at startup and shutdown, called a lifespan, to open a resource once and close it cleanly. The notebook `lifecycle.ipynb` shows all of it, with real output.

## Files

- **`server.py`:** A notes server. Its lifespan opens an in-memory SQLite database at startup and closes it at shutdown. Its two tools, `count_notes` and `add_note`, share that one database through `ctx.request_context.lifespan_context`.
- **`client.py`:** Counts the notes, adds one, counts again, then prints the server's log.

## Running it

Run from this folder, with the environment active (`conda activate MCP_env`):

```bash
python client.py
```

The count goes from 2 to 3, and the server's log starts with "Startup: Opening the database" and ends with "Shutdown: Closed the database".

## The key ideas

- **Client side:** `initialize()` is phase 1, the tool calls are phase 2, and leaving the `async with` blocks is phase 3. The newest spec (2026-07-28) drops the handshake: See the appendix of `../1-understanding-mcp/README.md`.
- **Server side:** A lifespan is an async context manager. The code before `yield` runs at startup, the code after it runs at shutdown, and what it yields is shared with every tool.
