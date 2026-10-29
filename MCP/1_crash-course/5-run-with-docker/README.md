# Part 5: Running the MCP server in Docker

This folder runs the Part 2 calculator server inside a Docker container, over Streamable HTTP, and connects to it from a client on your machine. The notebook `docker.ipynb` explains each step, with real output from a build and a run.

## Files

- **`server.py`:** The calculator server on Streamable HTTP. It listens on `0.0.0.0`, because inside a container `127.0.0.1` would make it unreachable from outside.
- **`client.py`:** The Part 2 Streamable HTTP client, pointed at `http://127.0.0.1:8050/mcp`.
- **`Dockerfile`:** Python 3.12 slim, the pinned requirements, then the server.
- **`requirements.txt`:** `mcp==1.27.0`, plus `pydantic-settings==2.14.0`, which stops a startup warning that newer versions print.

## Running it

1. Start Docker Desktop.
2. Build the image, from this folder:

   ```bash
   docker build -t mcp-server .
   ```

3. Run a container. `-p 127.0.0.1:8050:8050` publishes the port to your own computer only:

   ```bash
   docker run --rm --name mcp-server -p 127.0.0.1:8050:8050 mcp-server
   ```

4. In a second terminal, with MCP_env active, run the client:

   ```bash
   python client.py
   ```

   It prints `add`, `Add two numbers together` and `5`.

5. Stop the container with `Ctrl+C`, or `docker stop mcp-server`.

## If it doesn't connect

- **Is the container running?** `docker ps` should list `mcp-server` with `127.0.0.1:8050->8050/tcp`.
- **What did the server say?** `docker logs mcp-server` shows its startup lines and every request.
- **Is port 8050 already taken?** Stop whatever else uses it, for example a `python server.py` from Part 2.
