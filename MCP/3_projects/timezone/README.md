# A time zone MCP server

My own MCP server, written with MCPServer from MCP's official Python SDK (mcp 2.x). It offers one of each MCP primitive over Streamable HTTP: A tool that converts a time between time zones (with daylight saving handled), a resource that lists our offices, and a prompt that plans a meeting. It runs locally or in Docker.

## Files

- **`server.py`:** The server, on port 8060. The tool is `convert_time`, the resource is `zones://offices`, and the prompt is `plan_meeting`. The host comes from the `HOST` environment variable, and is `127.0.0.1` when it isn't set.
- **`client.py`:** A host that connects the server to an OpenAI model. The resource goes into the system message, the prompt becomes the user's message, and the model calls the tool in a loop until it answers.
- **`probe.py`:** A health check in plain `httpx`. It sends the JSON-RPC handshake and `tools/list`, and prints PASS if the server answers 200 and lists `convert_time`.
- **`Dockerfile` and `requirements.txt`:** The server's image.
- **`Server_Implementation_Details.ipynb` and `Client_Implementation_Details.ipynb`:** They explain the server and the client step by step, with real output.

## Running it locally

It runs in MCP_env. `client.py` also needs `OPENAI_API_KEY` in a `.env` file in this folder. Start the server in one terminal:

```bash
conda activate MCP_env
python server.py
```

Then, in a second terminal in this folder:

```bash
python probe.py
python client.py
```

## Running it in Docker

With Docker Desktop running, and the local server stopped (both use port 8060):

```bash
docker build -t timezone-mcp .
docker run --rm --name timezone-mcp -p 127.0.0.1:8060:8060 timezone-mcp
```

The address doesn't change, so `python probe.py` and `python client.py` work on the container as they are. Stop it with `Ctrl+C` or `docker stop timezone-mcp`.
