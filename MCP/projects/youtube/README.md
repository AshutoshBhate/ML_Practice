# A YouTube transcript MCP server

`server.py` offers one tool, `get_transcript`. Give it a YouTube link or video ID, and it returns the video's captions as plain text, so a host like Claude Desktop can summarize a video without you watching it. It's based on a tutorial and rewritten in this repo's style. The notebook `Implementation_Details.ipynb` explains it, with real output.

## Files

- **`server.py`:** The server. `extract_video_id` pulls the 11-character ID out of a URL, and `get_transcript` fetches the captions with the `youtube-transcript-api` library.
- **`client.py`:** Starts the server over stdio and calls `get_transcript` for one video.

## Running it

It runs in MCP_env, which has `youtube-transcript-api==1.2.4`. From this folder:

```bash
conda activate MCP_env
python client.py
```

It prints the transcript's length and its first 300 characters. The server's log goes to `server_log.txt`.

## Adding it to Claude Code or Claude Desktop

These steps aren't run here. Use full paths, because these hosts start the server from their own folder.

**Claude Code:**

```bash
claude mcp add youtube -- C:\Users\ashut\anaconda3\envs\MCP_env\python.exe C:\Users\ashut\ML_Practice\MCP\projects\youtube\server.py
claude mcp list
```

**Claude Desktop:** In Settings, Developer, Edit Config, add this to `claude_desktop_config.json` and restart Claude Desktop. JSON needs each backslash doubled:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "C:\\Users\\ashut\\anaconda3\\envs\\MCP_env\\python.exe",
      "args": ["C:\\Users\\ashut\\ML_Practice\\MCP\\projects\\youtube\\server.py"]
    }
  }
}
```

## If transcripts stop working

YouTube blocks transcript requests from many cloud providers' IP addresses. That's why the original version could route requests through a paid proxy. From your own computer, requests come from your home connection, so this version has no proxy.
