# Part 4: MCP vs plain function calling

This folder answers "Calculate 25 + 17" twice, with the same `add` function from `tools.py`: Once with plain function calling, and once through an MCP server. The notebook `mcp-vs-function-calling.ipynb` puts the two side by side, with real outputs.

## Files

- **`tools.py`:** The `add` function both versions use.
- **`function-calling.py`:** Plain function calling. The schema is written by hand, and `add` is called directly.
- **`server.py`:** An MCP server that serves the same `add`, registered with `mcp.add_tool(add)`.
- **`mcp-calling.py`:** The same question through the MCP server. It starts the server itself over stdio.

## Running it

Run from this folder, with the environment active (`conda activate MCP_env`):

```bash
python function-calling.py
python mcp-calling.py
```

Both print `The model called: add {'a': 25, 'b': 17}`, then the model's answer.

## When to use which

- **Plain function calling:** One self-contained app with a few tools of its own, where every call should be as fast as possible, or an early prototype.
- **MCP:** The same tools serve several apps or teams, a ready-made server already exists, or the tool should run somewhere else, like a container, another machine, or another team's service.
