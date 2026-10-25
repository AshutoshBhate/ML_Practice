# Part 3: An OpenAI model using MCP tools

This folder connects an OpenAI model to an MCP server. The server, `server.py`, offers one tool, `get_knowledge_base`, which returns five company-policy questions and answers from `data/kb.json`. The client lists the server's tools, converts them into OpenAI's tool format, and runs the normal function-calling loop: The model decides whether to call a tool, the client runs that call on the MCP server, and the model answers from the result.

Each script comes as a `.py` for quick lookup and a notebook that explains it step by step, with real outputs.

## Reading order

1. **`server.ipynb`:** The knowledge base tool: Its data, its schema, and what it returns.
2. **`client-simple.ipynb`:** The full loop in plain functions, answering one question.
3. **`client.ipynb`:** The same client as a class that connects once and answers several questions over one connection.

## Running it

Run from this folder, with the environment active (`conda activate MCP_env`). The OpenAI key comes from `crash-course/.env`, which `load_dotenv()` finds by searching the folders above.

- `python client-simple.py` asks one question.
- `python client.py` asks three questions over one connection.

Both clients start the server themselves over stdio, so there's nothing to start first. The server's log goes to `server_log.txt`. The server is a separate process: The client starts it as a child process. To run it on another machine instead, you'd serve it over Streamable HTTP (Part 2) and connect with `streamable_http_client`.
