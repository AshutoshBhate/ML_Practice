# A client for the official filesystem server

This folder has no server of its own. `client.py` starts the official MCP filesystem server, a Node.js program published on npm, and calls its tools to write, read, move and search files inside one folder, `sandbox/`. The notebook `client.ipynb` explains each step, with real output.

## How the server starts

The client runs `npx -y @modelcontextprotocol/server-filesystem@2.0.1 <sandbox folder>` as a stdio child process:

- **`npx`** comes with Node.js. It downloads the package from npm on the first run, then uses the cached copy.
- **`@2.0.1`** pins the version, so the tools don't change under you.
- **The sandbox folder** is the only folder the server may touch. A path outside it comes back as an error: "Access denied".

npm only supplies the code. The server itself runs on your laptop, as a child of the client, and the messages go through its stdin and stdout, not over the network.

## Running it

You need Node.js. Version 2.0.1 of the server asks for Node 24, but it also runs on Node 20 with an npm warning. Run from this folder, with the environment active (`conda activate MCP_env`):

```bash
python client.py
```

It creates `sandbox/`, writes `hello.txt`, reads it back, moves it into `sandbox/subdir/`, finds it with a search, and shows the server refusing to read `client.py`, which is outside the sandbox. The server's log goes to `server_log.txt`.
